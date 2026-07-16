from datetime import UTC, datetime
from pathlib import Path

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


def test_build_query_contains_precise_topic_terms() -> None:
    queries = ArxivSource.topic_queries()

    assert set(queries) == {"agent-self-evolving", "agent-memory", "llm-continual-training"}
    assert '"self-evolving agent"' in queries["agent-self-evolving"]
    assert '"agent memory"' in queries["agent-memory"]
    assert '"large language model"' in queries["llm-continual-training"]

