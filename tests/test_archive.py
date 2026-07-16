import json
from datetime import UTC, date, datetime

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.models import Paper


def make_paper(arxiv_id: str, *, topics: tuple[str, ...]) -> Paper:
    return Paper(
        arxiv_id=arxiv_id,
        title=f"Paper {arxiv_id}",
        abstract="A concise abstract.",
        authors=("A. Researcher",),
        published=datetime(2026, 7, 15, tzinfo=UTC),
        updated=datetime(2026, 7, 15, tzinfo=UTC),
        url=f"https://arxiv.org/abs/{arxiv_id}",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
        primary_category="cs.AI",
        categories=("cs.AI",),
        topics=topics,
    )


def test_update_creates_daily_archive_dataset_and_awesome_index(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path, repository_url="https://github.com/example/repo")

    result = archive.update(
        date(2026, 7, 16),
        [make_paper("2607.00001", topics=("agent-memory",))],
    )

    daily = tmp_path / "papers" / "2026" / "07" / "2026-07-16.md"
    assert result.daily_path == daily
    assert daily.exists()
    assert "## Agent Memory" in daily.read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "# Awesome Agent Evolution Papers" in readme
    assert "## 📊 Statistics" in readme
    assert "## 🗓️ Daily Archive" in readme
    assert "papers/2026/07/2026-07-16.md" in readme
    dataset = json.loads((tmp_path / "data" / "papers.json").read_text(encoding="utf-8"))
    assert dataset[0]["arxiv_id"] == "2607.00001"


def test_update_deduplicates_across_days_and_merges_topics(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    first = make_paper("2607.00001", topics=("agent-memory",))
    second = make_paper("2607.00001", topics=("agent-self-evolving",))

    archive.update(date(2026, 7, 15), [first])
    result = archive.update(date(2026, 7, 16), [second])

    assert result.new_papers == ()
    dataset = json.loads((tmp_path / "data" / "papers.json").read_text(encoding="utf-8"))
    assert len(dataset) == 1
    assert dataset[0]["topics"] == ["agent-memory", "agent-self-evolving"]


def test_update_records_an_empty_day(tmp_path) -> None:
    result = ArchiveRepository(tmp_path).update(date(2026, 7, 16), [])

    assert result.new_papers == ()
    text = result.daily_path.read_text(encoding="utf-8")
    assert "No new papers were discovered" in text

