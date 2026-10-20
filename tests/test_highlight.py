from dataclasses import replace

import pytest

from agent_paper_digest.highlight import (
    classify_highlights,
    has_industry_qualification,
    is_eligible,
)
from tests.test_archive import make_paper


def test_highlighter_marks_first_author_industry_and_explicit_top_venue() -> None:
    paper = replace(
        make_paper("2608.00001", topics=("agent-llm-self-evolution",)),
        affiliations=("Google DeepMind", "Tsinghua University"),
        first_author_affiliations=("Google DeepMind",),
        affiliation_source="arXiv author metadata",
        comment="Accepted to NeurIPS 2026 as a spotlight",
    )

    highlighted = classify_highlights(paper)

    assert highlighted.industry_affiliations == ("Google / DeepMind",)
    assert highlighted.industry_first_author_affiliations == ("Google / DeepMind",)
    assert highlighted.venue == "NeurIPS 2026"
    assert highlighted.venue_tier == "ccf-a"
    assert highlighted.acceptance_evidence.startswith("arXiv comment:")


def test_highlighter_does_not_promote_workshops_or_under_review_claims() -> None:
    workshop = replace(
        make_paper("2608.00002", topics=("agent-llm-self-evolution",)),
        comment="Accepted to the ACL 2026 Workshop on Agent Memory",
    )
    submitted = replace(
        make_paper("2608.00003", topics=("agent-llm-self-evolution",)),
        comment="Submitted to ICML 2027; under review",
    )

    assert classify_highlights(workshop).venue_tier == ""
    assert classify_highlights(submitted).venue_tier == ""


def test_emnlp_preprint_is_normalized_but_colm_is_not_selected() -> None:
    emnlp = replace(
        make_paper("2608.00004", topics=("agent-llm-self-evolution",)),
        venue="arXiv.org",
        comment="Accepted to EMNLP 2026 as a full paper",
    )
    colm = replace(
        make_paper("2608.00005", topics=("agent-llm-self-evolution",)),
        venue="COLM 2026",
        venue_source="Semantic Scholar publication metadata",
    )

    accepted = classify_highlights(emnlp)
    assert accepted.venue == "EMNLP 2026"
    assert accepted.venue_tier == "selected-extra"
    assert is_eligible(accepted)
    assert is_eligible(classify_highlights(colm))
    assert classify_highlights(colm).venue_tier == ""


def test_first_author_big_tech_and_high_citations_qualify_independently() -> None:
    industry = replace(
        make_paper("2608.00006", topics=("agent-llm-self-evolution",)),
        first_author_affiliations=("Microsoft Research",),
        affiliation_source="Semantic Scholar author profiles",
    )
    cited = replace(
        make_paper("2608.00007", topics=("llm-continual-training",)),
        citation_count=10,
    )

    assert is_eligible(classify_highlights(industry))
    assert is_eligible(classify_highlights(cited))


def test_coauthor_profile_and_code_stars_do_not_qualify() -> None:
    paper = replace(
        make_paper("2608.00008", topics=("agent-llm-self-evolution",)),
        affiliations=("Google DeepMind",),
        affiliation_source="Semantic Scholar author profiles",
        github_stars=100_000,
    )

    assert is_eligible(classify_highlights(paper))
    assert not has_industry_qualification(classify_highlights(paper))


def test_unrelated_topic_does_not_qualify_even_with_citations() -> None:
    paper = replace(
        make_paper("2608.00009", topics=("other",)),
        citation_count=1_000,
    )

    assert not is_eligible(classify_highlights(paper))


@pytest.mark.parametrize("venue", ["Computer Science", "Data Science", "Nature Communications"])
def test_journal_watchlist_does_not_match_partial_names(venue):
    paper = replace(
        make_paper("2610.00001", topics=("reinforcement-learning",)),
        venue=venue,
        venue_source="Semantic Scholar publication metadata",
    )
    assert classify_highlights(paper).venue_tier == ""


@pytest.mark.parametrize("venue", ["Nature", "Science", "Nature Machine Intelligence", "ICLR"])
def test_new_selected_venues_accept_explicit_acceptance(venue):
    paper = replace(
        make_paper("2610.00002", topics=("reinforcement-learning",)),
        comment=f"Accepted to {venue} 2026",
    )
    assert classify_highlights(paper).venue_tier == "selected-extra"


def test_future_first_publication_is_not_eligible():
    from datetime import UTC, datetime, timedelta

    paper = replace(
        make_paper("future", topics=("user-requested",)),
        published=datetime.now(UTC) + timedelta(days=2),
    )
    assert not is_eligible(paper)


@pytest.mark.parametrize(
    "venue",
    [
        "TMLR",
        "Trans. Mach. Learn. Res.",
        "Advanced Intelligent Systems",
        "IEEE Control Systems Letters",
        "IEEE Computational Intelligence Magazine",
        "Computer",
        "JACS Au",
        "Proceedings of the ACM on Management of Data",
        "Nature Communications",
        "Pattern Recognition",
        "IEEE Transactions on Pattern Analysis and Machine Intelligence",
        "Journal of AI Research",
    ],
)
def test_journals_are_excluded_even_when_requested(venue):
    paper = replace(make_paper("2607.12345", topics=("user-requested",)), venue=venue)
    assert not is_eligible(paper)
    assert not is_eligible(classify_highlights(paper))


def test_conference_reference_and_doi_are_not_journal_evidence():
    paper = replace(
        make_paper("2607.12345", topics=("user-requested",)),
        venue="Conference on Computer Vision and Pattern Recognition",
        journal_ref="Proceedings of CVPR 2026",
        doi="10.1109/CVPR.2026.12345",
    )
    assert is_eligible(paper)


def test_journal_publication_type_survives_serialization_and_merge():
    from agent_paper_digest.models import Paper

    paper = replace(
        make_paper("2607.12345", topics=("user-requested",)), publication_types=("JournalArticle",)
    )
    restored = Paper.from_dict(paper.to_dict())
    assert not is_eligible(restored.merge(replace(paper, publication_types=())))


def test_memory_cross_topic_is_permanently_excluded_after_classification():
    paper = make_paper("2607.12345", topics=("agent-memory", "user-requested"))
    classified = classify_highlights(paper)
    assert not is_eligible(classified)
    assert not is_eligible(classify_highlights(classified))


def test_new_memory_paper_from_other_query_is_excluded():
    paper = replace(
        make_paper("2607.12345", topics=("user-requested",)),
        title="Agent Memory for Long-Horizon LLM Agents",
    )
    assert not is_eligible(paper)


@pytest.mark.parametrize("month,expected", [(1, False), (4, False), (5, True)])
def test_may_2025_date_boundary(month, expected):
    from datetime import UTC, datetime

    paper = replace(
        make_paper("2505.12345", topics=("user-requested",)),
        published=datetime(2025, month, 1, tzinfo=UTC),
    )
    assert is_eligible(paper) is expected


def test_removed_identifier_cannot_return_through_another_topic(monkeypatch):
    monkeypatch.setattr("agent_paper_digest.highlight.EXCLUDED_PAPER_IDS", frozenset({"removed"}))
    paper = make_paper("removed", topics=("user-requested",))
    assert not is_eligible(paper)
