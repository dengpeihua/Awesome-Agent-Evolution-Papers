import json
from dataclasses import replace
from datetime import UTC, date, datetime

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.models import Paper


def make_paper(arxiv_id: str, *, topics: tuple[str, ...]) -> Paper:
    return Paper(
        arxiv_id=arxiv_id,
        title=f"Paper {arxiv_id}",
        abstract=(
            "We train large language models with reinforcement learning."
            if "reinforcement-learning" in topics
            else "A concise abstract."
        ),
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
        [make_eligible_paper("2607.00001", topics=("agent-llm-self-evolution",))],
    )

    daily = tmp_path / "papers" / "2026" / "07" / "2026-07-16.md"
    assert result.daily_path == daily
    assert daily.exists()
    assert "## Agent & LLM Self-Evolution" in daily.read_text(encoding="utf-8")
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
    first = make_eligible_paper("2607.00001", topics=("agent-llm-self-evolution",))
    second = make_eligible_paper("2607.00001", topics=("agent-llm-self-evolution",))

    archive.update(date(2026, 7, 15), [first])
    result = archive.update(date(2026, 7, 16), [second])

    assert result.new_papers == ()
    dataset = json.loads((tmp_path / "data" / "papers.json").read_text(encoding="utf-8"))
    assert len(dataset) == 1
    assert dataset[0]["topics"] == ["agent-llm-self-evolution"]


def test_update_records_an_empty_day(tmp_path) -> None:
    result = ArchiveRepository(tmp_path).update(date(2026, 7, 16), [])

    assert result.new_papers == ()
    text = result.daily_path.read_text(encoding="utf-8")
    assert "No new papers were discovered" in text


def test_same_day_rerun_preserves_papers_already_discovered_that_day(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    paper = make_eligible_paper("2607.00001", topics=("agent-llm-self-evolution",))
    first = archive.update(date(2026, 7, 16), [paper])

    second = archive.update(date(2026, 7, 16), [])

    assert first.new_papers == (paper,)
    assert second.new_papers == ()
    text = second.daily_path.read_text(encoding="utf-8")
    assert "Paper 2607.00001" in text
    assert "No new papers were discovered" not in text
    discoveries = json.loads((tmp_path / "data" / "discoveries.json").read_text(encoding="utf-8"))
    assert discoveries == {"2026-07-16": ["2607.00001"]}


def test_enrichment_round_trip_and_highlight_rendering(tmp_path) -> None:
    paper = replace(
        make_paper("2607.00002", topics=("agent-llm-self-evolution",)),
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
        make_paper("2607.00003", topics=("agent-llm-self-evolution",)),
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


def test_public_dataset_includes_topical_new_preprints_without_priority(tmp_path) -> None:
    plain = make_paper("2607.00004", topics=("agent-llm-self-evolution",))
    popular = replace(plain, arxiv_id="2607.00005", github_stars=50_000)

    result = ArchiveRepository(tmp_path).replace_dataset([plain, popular])

    assert len(result) == 2
    assert len(json.loads((tmp_path / "data" / "papers.json").read_text())) == 2


def test_rebuild_prunes_old_daily_pages_when_paper_no_longer_qualifies(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    eligible = make_eligible_paper("2607.00006", topics=("agent-llm-self-evolution",))
    archive.update(date(2026, 7, 15), [eligible])

    archive.replace_dataset([make_paper("2607.00006", topics=("unrelated",))])

    daily = tmp_path / "papers" / "2026" / "07" / "2026-07-15.md"
    assert "Paper 2607.00006" not in daily.read_text(encoding="utf-8")


def test_public_paper_lists_are_ordered_by_published_time_descending(tmp_path) -> None:
    archive = ArchiveRepository(tmp_path)
    older_priority_paper = replace(
        make_paper("2606.00001", topics=("agent-llm-self-evolution",)),
        published=datetime(2026, 6, 1, tzinfo=UTC),
        updated=datetime(2026, 6, 1, tzinfo=UTC),
        first_author_affiliations=("ByteDance Seed",),
        affiliation_source="Official project page",
    )
    newer_cited_paper = replace(
        make_eligible_paper("2608.00001", topics=("agent-llm-self-evolution",)),
        published=datetime(2026, 8, 1, tzinfo=UTC),
        updated=datetime(2026, 8, 1, tzinfo=UTC),
    )

    result = archive.update(
        date(2026, 8, 2),
        [older_priority_paper, newer_cited_paper],
    )

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    highlighted = readme.split("## 🌟 Highlighted Papers", 1)[1].split("## 🗓️ Monthly Index", 1)[0]
    latest = readme.split("## 📝 Latest Papers", 1)[1].split("## 🗓️ Daily Archive", 1)[0]
    daily = result.daily_path.read_text(encoding="utf-8")

    assert highlighted.index("Paper 2608.00001") < highlighted.index("Paper 2606.00001")
    assert latest.index("Paper 2608.00001") < latest.index("Paper 2606.00001")
    assert daily.index("Paper 2608.00001") < daily.index("Paper 2606.00001")
    assert readme.index("[2026-08]") < readme.index("[2026-06]")


def test_acceptance_discovery_and_coverage_survive_rebuild(tmp_path):
    archive = ArchiveRepository(tmp_path)
    original = make_paper("2607.12345", topics=("reinforcement-learning",))
    archive.update(date(2026, 7, 16), [original])
    accepted = replace(original, comment="Accepted to ICLR 2027 as a full paper")
    start = datetime(2026, 9, 12, tzinfo=UTC)
    end = datetime(2026, 10, 3, tzinfo=UTC)
    result = archive.update(end.date(), [accepted], coverage_start=start, coverage_end=end)
    assert result.promoted_papers[0].acceptance_first_seen == "2026-10-03"
    archive.replace_dataset(list(result.all_papers))
    text = result.daily_path.read_text("utf-8")
    assert "2026-09-12T00:00:00+00:00" in text
    assert "Acceptance first observed: 2026-10-03" in text
    assert "actual acceptance date unverified" in text
    assert not archive.update(date(2026, 10, 4), [accepted]).promoted_papers


def test_large_daily_archive_paginates_without_losing_or_reordering_papers(tmp_path, monkeypatch):
    monkeypatch.setattr("agent_paper_digest.highlight.EXCLUDED_PAPER_IDS", frozenset())
    papers = [make_paper(f"2610.{i:05d}", topics=("reinforcement-learning",)) for i in range(125)]
    archive = ArchiveRepository(tmp_path)
    result = archive.update(date(2026, 10, 3), papers)
    first = result.daily_path.read_text("utf-8")
    second_path = result.daily_path.parent / "2026-10-03" / "page-002.md"
    second = second_path.read_text("utf-8")
    third = second_path.with_name("page-003.md").read_text("utf-8")
    assert "**125 papers**" in first
    assert "Paper 2610.00124" in first and "Paper 2610.00075" in first
    assert "Paper 2610.00074" not in first
    assert "Paper 2610.00074" in second and "Paper 2610.00025" in second
    assert "Paper 2610.00024" in third and "Paper 2610.00000" in third
    assert "(2026-10-03/page-002.md)" in first
    assert "(../2026-10-03.md)" in second
    assert "(../../../../README.md)" in second
    archive.replace_dataset(papers[:1])
    assert not second_path.exists()


def test_first_publication_cutoff_rejects_old_papers_even_if_recently_updated(tmp_path):
    old = replace(
        make_eligible_paper("2412.00001", topics=("agent-llm-self-evolution",)),
        published=datetime(2024, 12, 31, 23, 59, tzinfo=UTC),
        updated=datetime(2026, 10, 3, tzinfo=UTC),
    )
    boundary = replace(old, arxiv_id="2505.00001", published=datetime(2025, 5, 1, tzinfo=UTC))
    stale = tmp_path / "papers/2024/12/README.md"
    stale.parent.mkdir(parents=True)
    stale.write_text("Old paper list", encoding="utf-8")
    result = ArchiveRepository(tmp_path).replace_dataset([old, boundary])
    assert [p.arxiv_id for p in result] == ["2505.00001"]
    assert not stale.exists()


def test_recuration_removes_cached_rl_tags_without_losing_other_valid_topics(tmp_path):
    paper = replace(
        make_paper("2609.001", topics=("agent-llm-self-evolution",)),
        topics=("agent-llm-self-evolution", "reinforcement-learning"),
    )
    result = ArchiveRepository(tmp_path).replace_dataset([paper])
    assert result[0].topics == ("agent-llm-self-evolution",)
