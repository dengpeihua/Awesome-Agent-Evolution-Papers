import json
from dataclasses import replace
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


def make_eligible_paper(arxiv_id: str, *, topics: tuple[str, ...]) -> Paper:
    return replace(
        make_paper(arxiv_id, topics=topics),
        citation_count=10,
        citation_source="Semantic Scholar",
    )


def test_update_creates_daily_archive_dataset_and_awesome_index(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path, repository_url="https://github.com/example/repo")

    result = archive.update(
        date(2026, 7, 16),
        [make_eligible_paper("2607.00001", topics=("agent-memory",))],
    )

    daily = tmp_path / "papers" / "2026" / "07" / "2026-07-16.md"
    assert result.daily_path == daily
    assert daily.exists()
    assert "## Agent Memory" in daily.read_text(encoding="utf-8")
    monthly = tmp_path / "papers" / "2026" / "07" / "README.md"
    assert monthly.exists()
    assert "# 2026-07 Agent Evolution Papers" in monthly.read_text(encoding="utf-8")
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "# Awesome Agent Evolution Papers" in readme
    assert "## 📊 Statistics" in readme
    assert "## 🗓️ Daily Archive" in readme
    assert "papers/2026/07/2026-07-16.md" in readme
    assert "papers/2026/07/README.md" in readme
    dataset = json.loads((tmp_path / "data" / "papers.json").read_text(encoding="utf-8"))
    assert dataset[0]["arxiv_id"] == "2607.00001"


def test_update_deduplicates_across_days_and_merges_topics(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    first = make_eligible_paper("2607.00001", topics=("agent-memory",))
    second = make_eligible_paper("2607.00001", topics=("agent-self-evolving",))

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


def test_same_day_rerun_preserves_papers_already_discovered_that_day(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    paper = make_eligible_paper("2607.00001", topics=("agent-memory",))
    first = archive.update(date(2026, 7, 16), [paper])

    second = archive.update(date(2026, 7, 16), [])

    assert first.new_papers == (paper,)
    assert second.new_papers == ()
    text = second.daily_path.read_text(encoding="utf-8")
    assert "Paper 2607.00001" in text
    assert "No new papers were discovered" not in text
    discoveries = json.loads(
        (tmp_path / "data" / "discoveries.json").read_text(encoding="utf-8")
    )
    assert discoveries == {"2026-07-16": ["2607.00001"]}


def test_enrichment_round_trip_and_highlight_rendering(tmp_path) -> None:
    paper = replace(
        make_paper("2607.00002", topics=("agent-self-evolving",)),
        venue="ACL 2026 (Main)",
        venue_source="ACL Anthology",
        github_url="https://github.com/example/project",
        github_stars=1_234,
        citation_count=12,
        citation_source="Google Scholar",
        industry_affiliations=("Example Research",),
        verified_at="2026-08-12",
    )

    ArchiveRepository(tmp_path).replace_dataset([paper])

    restored = ArchiveRepository(tmp_path)._load()[0]
    assert restored.venue_tier == "ccf-a"
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "🔥 Very popular code" in readme
    assert "📈 Highly cited" in readme
    assert "🏢 Industry" in readme
    assert "🏆 CCF-A" in readme
    assert "Citations: 12 (Google Scholar)" in readme


def test_existing_paper_is_promoted_when_a_priority_signal_appears(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    paper = replace(
        make_paper("2607.00003", topics=("agent-memory",)),
        citation_count=10,
        citation_source="Semantic Scholar",
    )
    archive.update(date(2026, 7, 15), [paper])

    promoted = replace(
        paper,
        updated=datetime(2026, 7, 16, tzinfo=UTC),
        venue="ACL 2026",
        venue_source="arXiv comment",
        acceptance_evidence="arXiv comment: Accepted to ACL 2026",
    )
    result = archive.update(date(2026, 7, 16), [promoted])

    assert result.new_papers == ()
    actual = result.promoted_papers[0]
    assert actual.venue_tier == "ccf-a"
    assert result.digest_papers == (actual,)
    daily = result.daily_path.read_text(encoding="utf-8")
    assert "🚨 Priority Watch" in daily
    assert "🏆 CCF-A: ACL 2026" in daily


def test_public_dataset_rejects_plain_arxiv_and_popular_code_only(tmp_path) -> None:
    plain = make_paper("2607.00004", topics=("agent-memory",))
    popular = replace(plain, arxiv_id="2607.00005", github_stars=50_000)

    result = ArchiveRepository(tmp_path).replace_dataset([plain, popular])

    assert result == ()
    assert json.loads((tmp_path / "data" / "papers.json").read_text()) == []


def test_rebuild_prunes_old_daily_pages_when_paper_no_longer_qualifies(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    eligible = make_eligible_paper("2607.00006", topics=("agent-memory",))
    archive.update(date(2026, 7, 15), [eligible])

    archive.replace_dataset([make_paper("2607.00006", topics=("agent-memory",))])

    daily = tmp_path / "papers" / "2026" / "07" / "2026-07-15.md"
    assert "Paper 2607.00006" not in daily.read_text(encoding="utf-8")
