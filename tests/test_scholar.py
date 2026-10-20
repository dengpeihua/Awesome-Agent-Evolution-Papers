import json
from dataclasses import replace

import httpx
import pytest

from agent_paper_digest.highlight import classify_highlights
from agent_paper_digest.scholar import SemanticScholarEnricher
from tests.test_archive import make_paper


@pytest.mark.asyncio
async def test_semantic_scholar_batches_venue_and_author_profile_affiliations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        if request.url.path.endswith("/paper/batch"):
            assert body == {"ids": ["ARXIV:2608.00001"]}
            return httpx.Response(
                200,
                json=[
                    {
                        "title": "Paper 2608.00001",
                        "venue": "",
                        "publicationVenue": {
                            "name": "International Conference on Machine Learning 2026"
                        },
                        "authors": [{"authorId": "A1", "name": "A. Researcher"}],
                        "citationCount": 17,
                    }
                ],
            )
        assert request.url.path.endswith("/author/batch")
        assert body == {"ids": ["A1"]}
        return httpx.Response(
            200,
            json=[
                {
                    "authorId": "A1",
                    "name": "A. Researcher",
                    "affiliations": ["Google DeepMind"],
                }
            ],
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        papers = await SemanticScholarEnricher(client=client).enrich(
            [make_paper("2608.00001", topics=("agent-llm-self-evolution",))]
        )

    paper = classify_highlights(papers[0])
    assert paper.venue == "International Conference on Machine Learning 2026"
    assert paper.venue_source == "Semantic Scholar publication metadata"
    assert paper.venue_tier == "ccf-a"
    assert paper.citation_count == 17
    assert paper.citation_source == "Semantic Scholar"
    assert paper.affiliations == ("Google DeepMind",)
    assert paper.first_author_affiliations == ("Google DeepMind",)
    assert paper.affiliation_source == "Semantic Scholar author profiles"


@pytest.mark.asyncio
async def test_semantic_scholar_does_not_mix_profiles_into_paper_affiliations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/paper/batch"):
            return httpx.Response(
                200,
                json=[
                    {
                        "authors": [{"authorId": "A1"}],
                        "citationCount": 2,
                    }
                ],
            )
        return httpx.Response(
            200,
            json=[{"authorId": "A1", "affiliations": ["Google DeepMind"]}],
        )

    source = replace(
        make_paper("2608.00002", topics=("agent-llm-self-evolution",)),
        affiliations=("Tsinghua University",),
        affiliation_source="arXiv author metadata",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        paper = (await SemanticScholarEnricher(client=client).enrich([source]))[0]

    assert paper.affiliations == ("Tsinghua University",)
    assert paper.first_author_affiliations == ()
    assert paper.affiliation_source == "arXiv author metadata"


@pytest.mark.asyncio
async def test_semantic_scholar_continues_after_one_rate_limited_chunk() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429)
        body = json.loads(request.content)
        assert body == {"ids": ["DOI:10.1000/example"]}
        return httpx.Response(200, json=[{"authors": [], "citationCount": 12}])

    papers = [
        make_paper(f"2608.{index:05d}", topics=("agent-llm-self-evolution",))
        for index in range(500)
    ]
    papers.append(
        replace(make_paper("external", topics=("agent-llm-self-evolution",)), doi="10.1000/example")
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        enriched = await SemanticScholarEnricher(client=client).enrich(papers)

    assert enriched[0].citation_count is None
    assert enriched[-1].citation_count == 12


@pytest.mark.asyncio
async def test_publication_metadata_replaces_preprint_placeholder():
    def handler(request):
        return httpx.Response(200, json=[{"venue": "ICLR 2026", "authors": []}])

    paper = replace(
        make_paper("2608.12345", topics=("reinforcement-learning",)),
        venue="arXiv.org",
        venue_source="arXiv",
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        enriched = (await SemanticScholarEnricher(client=client).enrich([paper]))[0]
    assert enriched.venue == "ICLR 2026"
    assert classify_highlights(enriched).venue_tier == "selected-extra"
