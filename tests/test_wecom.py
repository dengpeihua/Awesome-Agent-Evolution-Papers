from agent_paper_digest.models import Paper
from agent_paper_digest.wecom import build_digest_markdown, split_markdown
from tests.test_archive import make_paper


def test_digest_markdown_groups_topics_and_limits_papers() -> None:
    papers: list[Paper] = [
        make_paper(f"2607.{index:05d}", topics=("agent-memory",)) for index in range(12)
    ]

    markdown = build_digest_markdown(
        papers,
        archive_url="https://github.com/example/repo/blob/main/papers/2026/07/2026-07-16.md",
        max_papers=5,
    )

    assert markdown.count("https://arxiv.org/abs/") == 5
    assert "Agent Memory" in markdown
    assert "7 more paper(s)" in markdown
    assert "查看完整归档" in markdown


def test_split_markdown_never_exceeds_wecom_limit() -> None:
    text = "# Digest\n" + "\n".join(f"- item {index} " + ("x" * 200) for index in range(50))

    chunks = split_markdown(text, limit=1000)

    assert len(chunks) > 1
    assert all(len(chunk.encode("utf-8")) <= 1000 for chunk in chunks)
    assert "item 49" in chunks[-1]

