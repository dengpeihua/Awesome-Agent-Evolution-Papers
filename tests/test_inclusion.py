import json
from dataclasses import replace
from datetime import UTC, date, datetime

import pytest

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.inclusion import inclusion_reasons, paper_record
from agent_paper_digest.models import Paper
from agent_paper_digest.wecom import build_digest_markdown


@pytest.fixture
def paper(monkeypatch):
    monkeypatch.setattr("agent_paper_digest.highlight.EXCLUDED_PAPER_IDS", frozenset())
    return Paper(
        arxiv_id="2607.99991",
        title="Self-improving language agents for long-horizon tasks",
        abstract="We fine-tune a language model on its own verified agent trajectories.",
        authors=("Researcher",),
        published=datetime(2026, 7, 1, tzinfo=UTC),
        updated=datetime(2026, 7, 1, tzinfo=UTC),
        url="https://arxiv.org/abs/2607.99991v1",
        pdf_url="https://arxiv.org/pdf/2607.99991v1",
        primary_category="cs.AI",
        categories=("cs.AI",),
        topics=(),
    )


def test_reasons_include_each_actual_topic_and_original_evidence(paper):
    reasons = inclusion_reasons(paper)
    assert {r.topic for r in reasons} == {"agent-llm-self-evolution", "long-horizon-agent"}
    assert all(r.training_evidence == paper.abstract for r in reasons)
    assert all(r.topic_evidence == paper.title and r.source == paper.url for r in reasons)
    assert all("非全文核验" in r.evidence_level for r in reasons)


@pytest.mark.parametrize(
    "changes",
    [
        {"abstract": "We use a frozen language model without training."},
        {"abstract": "We train a language model with reinforcement learning."},
        {"topics": ("agent-memory",)},
        {"venue_type": "journal"},
        {"published": datetime(2025, 4, 30, tzinfo=UTC)},
    ],
)
def test_priority_cannot_produce_inclusion_reason_for_excluded_paper(paper, changes):
    excluded = replace(paper, citation_count=1000, **changes)
    assert inclusion_reasons(excluded) == ()


def test_requested_paper_does_not_fabricate_topic_or_training(paper):
    requested = replace(
        paper,
        title="Teacher routing",
        abstract="Analysis of multiple teachers.",
        topics=("user-requested",),
    )
    (reason,) = inclusion_reasons(requested)
    assert reason.topic == "user-requested"
    assert reason.training_evidence == ""
    assert "用户指定" in reason.reason


def test_archive_rebuild_refreshes_reasons_and_all_reader_surfaces(tmp_path, paper):
    archive = ArchiveRepository(tmp_path)
    archive.update(date(2026, 7, 2), [paper])
    values = json.loads((tmp_path / "data/papers.json").read_text("utf-8"))
    values[0]["inclusion_reasons"] = [{"reason": "stale explanation"}]
    (tmp_path / "data/papers.json").write_text(json.dumps(values), encoding="utf-8")
    new_abstract = "We distill a student model from verified long-horizon agent trajectories."
    archive.replace_dataset([replace(p, abstract=new_abstract) for p in archive._load()])
    (record,) = json.loads((tmp_path / "data/papers.json").read_text("utf-8"))
    assert all(r["training_evidence"] == new_abstract for r in record["inclusion_reasons"])
    for name in (
        "README.md",
        "data/inclusion_reasons.md",
        "papers/2026/07/README.md",
        "papers/2026/07/2026-07-02.md",
    ):
        text = (tmp_path / name).read_text("utf-8")
        assert "收录理由" in text
        assert "stale explanation" not in text
    report = (tmp_path / "data/inclusion_reasons.md").read_text("utf-8")
    assert new_abstract in report
    assert 'id="paper-2607-99991"' in report
    assert "收录理由" in build_digest_markdown([paper], archive_url="", max_papers=8)
    assert "inclusion_reasons" in paper_record(paper)
