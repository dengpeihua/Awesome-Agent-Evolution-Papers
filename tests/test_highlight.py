from dataclasses import replace

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
        make_paper("2608.00002", topics=("agent-memory",)),
        comment="Accepted to the ACL 2026 Workshop on Agent Memory",
    )
    submitted = replace(
        make_paper("2608.00003", topics=("agent-memory",)),
        comment="Submitted to ICML 2027; under review",
    )

    assert classify_highlights(workshop).venue_tier == ""
    assert classify_highlights(submitted).venue_tier == ""


def test_emnlp_preprint_is_normalized_but_colm_is_not_selected() -> None:
    emnlp = replace(
        make_paper("2608.00004", topics=("agent-memory",)),
        venue="arXiv.org",
        comment="Accepted to EMNLP 2026 as a full paper",
    )
    colm = replace(
        make_paper("2608.00005", topics=("agent-memory",)),
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
        make_paper("2608.00008", topics=("agent-memory",)),
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
