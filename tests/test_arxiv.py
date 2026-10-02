from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest

from agent_paper_digest.arxiv import ArxivSource, parse_arxiv_feed


def test_parse_arxiv_feed_normalizes_fields_and_versioned_id() -> None:
    xml = (Path(__file__).parent / "fixtures" / "arxiv_feed.xml").read_text(encoding="utf-8")

    papers = parse_arxiv_feed(xml, topic="agent-memory")

    assert len(papers) == 1
    paper = papers[0]
    assert paper.arxiv_id == "2607.01234"
    assert paper.title == "Memory for Self-Evolving Agents"
    assert paper.abstract == "We study durable memory. The agent improves over time."
    assert paper.authors == ("Alice Example", "Bob Example")
    assert paper.published == datetime(2026, 7, 14, 8, tzinfo=UTC)
    assert paper.primary_category == "cs.AI"
    assert paper.categories == ("cs.AI", "cs.CL")
    assert paper.topics == ("agent-memory",)
    assert paper.doi == "10.0000/example"
    assert paper.comment == "Accepted to ACL 2026"
    assert paper.journal_ref == "Proceedings of ACL 2026"
    assert paper.first_author_affiliations == ("Google DeepMind",)
    assert paper.affiliations == ("Google DeepMind",)


def test_build_query_contains_precise_topic_terms() -> None:
    queries = ArxivSource.topic_queries()

    assert set(queries) == {
        "agent-llm-self-evolution",
        "agent-memory",
        "llm-continual-training",
        "reinforcement-learning",
    }
    assert '"self-evolving"' in queries["agent-llm-self-evolution"]
    assert '"recursive self-improvement"' in queries["agent-llm-self-evolution"]
    assert '"self-improving language model"' in queries["agent-llm-self-evolution"]
    assert '"self-generated feedback"' in queries["agent-llm-self-evolution"]
    assert '"agent memory"' in queries["agent-memory"]
    assert '"agentic memory"' in queries["agent-memory"]
    assert '"large language model"' in queries["llm-continual-training"]
    assert '"continual pre-training"' in queries["llm-continual-training"]
    assert '"continual post-training"' in queries["llm-continual-training"]
    assert '"life-long learning"' in queries["llm-continual-training"]


@pytest.mark.asyncio
async def test_fetch_pages_until_the_complete_catch_up_window(monkeypatch) -> None:
    def feed(entries: list[tuple[str, str]]) -> str:
        body = "".join(
            f"""
            <entry xmlns="http://www.w3.org/2005/Atom">
              <id>http://arxiv.org/abs/{paper_id}v1</id>
              <updated>{updated}</updated><published>{updated}</published>
              <title>Paper {paper_id}</title><summary>Agent memory.</summary>
              <author><name>Alice</name></author>
              <category term="cs.AI" />
            </entry>
            """
            for paper_id, updated in entries
        )
        return f'<feed xmlns="http://www.w3.org/2005/Atom">{body}</feed>'

    responses = [
        feed(
            [
                ("2607.00003", "2026-07-16T08:00:00Z"),
                ("2607.00002", "2026-07-15T08:00:00Z"),
            ]
        ),
        feed([("2607.00001", "2026-07-10T08:00:00Z")]),
    ]

    class FakeClient:
        def __init__(self) -> None:
            self.starts: list[int] = []

        async def get(self, _url, *, params):
            self.starts.append(params["start"])
            request = httpx.Request("GET", "https://export.arxiv.org/api/query")
            return httpx.Response(200, text=responses.pop(0), request=request)

    client = FakeClient()
    monkeypatch.setattr(
        ArxivSource,
        "topic_queries",
        staticmethod(lambda: {"agent-memory": 'all:"agent memory"'}),
    )

    papers = await ArxivSource(client=client, request_delay_seconds=0).fetch(
        since=datetime(2026, 7, 14, tzinfo=UTC),
        max_results_per_topic=2,
    )

    assert [paper.arxiv_id for paper in papers] == ["2607.00003", "2607.00002"]
    assert client.starts == [0, 2]


@pytest.mark.asyncio
async def test_fetch_retries_arxiv_rate_limits(monkeypatch) -> None:
    xml = (Path(__file__).parent / "fixtures" / "arxiv_feed.xml").read_text(encoding="utf-8")

    class RetryClient:
        def __init__(self) -> None:
            self.calls = 0

        async def get(self, _url, *, params):
            self.calls += 1
            request = httpx.Request("GET", "https://export.arxiv.org/api/query")
            if self.calls == 1:
                return httpx.Response(429, headers={"Retry-After": "0"}, request=request)
            return httpx.Response(200, text=xml, request=request)

    client = RetryClient()
    monkeypatch.setattr(
        ArxivSource,
        "topic_queries",
        staticmethod(lambda: {"agent-memory": 'all:"agent memory"'}),
    )

    papers = await ArxivSource(
        client=client,
        request_delay_seconds=0,
        retry_base_seconds=0,
    ).fetch(
        since=datetime(2026, 7, 14, tzinfo=UTC),
        max_results_per_topic=20,
    )

    assert len(papers) == 1
    assert client.calls == 2


@pytest.mark.asyncio
async def test_fetch_retries_transient_network_errors(monkeypatch) -> None:
    xml = (Path(__file__).parent / "fixtures" / "arxiv_feed.xml").read_text(encoding="utf-8")

    class RetryClient:
        def __init__(self) -> None:
            self.calls = 0

        async def get(self, _url, *, params):
            self.calls += 1
            request = httpx.Request("GET", "https://export.arxiv.org/api/query")
            if self.calls == 1:
                raise httpx.ReadTimeout("temporary timeout", request=request)
            return httpx.Response(200, text=xml, request=request)

    client = RetryClient()
    monkeypatch.setattr(
        ArxivSource,
        "topic_queries",
        staticmethod(lambda: {"agent-memory": 'all:"agent memory"'}),
    )

    papers = await ArxivSource(
        client=client,
        request_delay_seconds=0,
        retry_base_seconds=0,
    ).fetch(
        since=datetime(2026, 7, 14, tzinfo=UTC),
        max_results_per_topic=20,
    )

    assert len(papers) == 1
    assert client.calls == 2
