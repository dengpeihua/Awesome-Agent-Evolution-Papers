from __future__ import annotations

import logging
from dataclasses import replace

import httpx

from .highlight import PREPRINT_PATTERN
from .models import Paper

LOGGER = logging.getLogger(__name__)


def _chunks(values: list[object], size: int) -> list[list[object]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


class SemanticScholarEnricher:
    """Best-effort batched publication, citation, and author enrichment."""

    PAPER_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
    AUTHOR_BATCH_URL = "https://api.semanticscholar.org/graph/v1/author/batch"

    def __init__(
        self,
        *,
        api_key: str = "",
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_key = api_key
        self._client = client

    @staticmethod
    def _paper_id(paper: Paper) -> str:
        return f"DOI:{paper.doi}" if paper.doi else f"ARXIV:{paper.arxiv_id}"

    async def enrich(self, papers: list[Paper]) -> list[Paper]:
        if not papers:
            return []
        owns_client = self._client is None
        headers = {"x-api-key": self.api_key} if self.api_key else {}
        client = self._client or httpx.AsyncClient(
            timeout=httpx.Timeout(30),
            follow_redirects=True,
            headers={"User-Agent": "Awesome-Agent-Evolution-Papers/0.3", **headers},
        )
        enriched = list(papers)
        paper_authors: list[list[dict[str, object]]] = [[] for _ in papers]
        try:
            indexed = list(enumerate(papers))
            for raw_chunk in _chunks(indexed, 500):
                chunk = [(int(index), paper) for index, paper in raw_chunk]
                try:
                    response = await client.post(
                        self.PAPER_BATCH_URL,
                        params={
                            "fields": "title,venue,publicationVenue,journal,"
                            "publicationTypes,authors,citationCount"
                        },
                        json={"ids": [self._paper_id(paper) for _, paper in chunk]},
                        headers=headers,
                    )
                    response.raise_for_status()
                    records = response.json()
                except (httpx.HTTPError, ValueError, TypeError) as error:
                    LOGGER.warning("Semantic Scholar paper enrichment failed: %s", error)
                    continue

                for offset, (index, paper) in enumerate(chunk):
                    record = records[offset] if offset < len(records) and records[offset] else {}
                    authors = record.get("authors") or []
                    paper_authors[index] = authors
                    publication_venue = record.get("publicationVenue") or {}
                    journal = record.get("journal") or {}
                    venue = (
                        publication_venue.get("name")
                        or record.get("venue")
                        or journal.get("name")
                        or ""
                    )
                    citation_count = record.get("citationCount")
                    updates: dict[str, object] = {
                        "publication_types": tuple(
                            record.get("publicationTypes") or paper.publication_types
                        ),
                        "venue_type": str(publication_venue.get("type") or paper.venue_type),
                    }
                    if venue:
                        replace_venue = not paper.venue or bool(PREPRINT_PATTERN.match(paper.venue))
                        updates.update(
                            venue=str(venue) if replace_venue else paper.venue,
                            venue_source=(
                                "Semantic Scholar publication metadata"
                                if replace_venue
                                else paper.venue_source or "Semantic Scholar publication metadata"
                            ),
                        )
                    if citation_count is not None:
                        updates.update(
                            citation_count=int(citation_count),
                            citation_source="Semantic Scholar",
                        )
                    if updates:
                        enriched[index] = replace(paper, **updates)

            author_ids = list(
                dict.fromkeys(
                    str(author["authorId"])
                    for authors in paper_authors
                    for author in authors
                    if isinstance(author, dict) and author.get("authorId")
                )
            )
            profiles: dict[str, tuple[str, ...]] = {}
            for raw_chunk in _chunks(author_ids, 1_000):
                chunk = [str(value) for value in raw_chunk]
                try:
                    response = await client.post(
                        self.AUTHOR_BATCH_URL,
                        params={"fields": "name,affiliations"},
                        json={"ids": chunk},
                        headers=headers,
                    )
                    response.raise_for_status()
                    for profile in response.json():
                        if not profile or not profile.get("authorId"):
                            continue
                        profiles[str(profile["authorId"])] = tuple(
                            str(value).strip()
                            for value in profile.get("affiliations") or []
                            if str(value).strip()
                        )
                except (httpx.HTTPError, ValueError, TypeError) as error:
                    LOGGER.warning("Semantic Scholar author enrichment failed: %s", error)

            for index, authors in enumerate(paper_authors):
                per_author = [
                    profiles.get(str(author.get("authorId")), ())
                    for author in authors
                    if isinstance(author, dict)
                ]
                affiliations = tuple(
                    dict.fromkeys(
                        affiliation
                        for author_affiliations in per_author
                        for affiliation in author_affiliations
                    )
                )
                if affiliations and not enriched[index].affiliations:
                    enriched[index] = replace(
                        enriched[index],
                        affiliations=affiliations,
                        first_author_affiliations=(per_author[0] if per_author else ()),
                        affiliation_source="Semantic Scholar author profiles",
                    )
            return enriched
        finally:
            if owns_client:
                await client.aclose()
