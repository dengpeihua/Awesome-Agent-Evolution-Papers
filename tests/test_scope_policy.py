import json
from dataclasses import replace
from datetime import date, timedelta

import pytest

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.arxiv import ArxivSource
from agent_paper_digest.highlight import classify_highlights, is_eligible
from agent_paper_digest.models import Paper
from agent_paper_digest.topics import (
    SELF_EVOLUTION_TOPIC,
    TOPIC_TITLES,
    model_training_evidence,
)
from tests.test_archive import make_paper


@pytest.mark.parametrize(
    "abstract",
    [
        "We use a pretrained LLM API to evolve prompts and improve long-horizon agents.",
        "We optimize prompts for a language model using a self-improvement loop.",
        "We present self-evolving agents without updating model parameters.",
        "We optimize the navigation behavior of frozen LLMs through closed-loop experience.",
        "We evaluate training-free self-improvement. Prior work trains LLMs using RL.",
        "We study parameter-update-free self-evolution of a frozen language model.",
        "We use a pre-trained language model for self-improvement.",
        "Our model training environment generates data, but no model is trained.",
        "Our harness evolves rather than fine-tuning model weights.",
        "We study training setup, experience collection, and model evaluation.",
        "We propose an API harness and compare ACE, TF-GRPO and AHE on held-out tasks.",
        "We propose natural-language policy gradients without changing model parameters.",
        "We present an LLM agent that distills experience across clusters to improve models.",
    ],
)
def test_rsi_rejects_api_only_negation_background_and_no_evidence(abstract):
    paper = replace(
        make_paper("scope-test", topics=(SELF_EVOLUTION_TOPIC, "user-requested")),
        title="Recursive Self-Improvement for LLM Agents",
        abstract=abstract,
    )
    assert not model_training_evidence(paper.title, abstract)
    assert not is_eligible(paper)
    assert not is_eligible(classify_highlights(classify_highlights(paper)))


@pytest.mark.parametrize(
    "abstract",
    [
        "We fine-tune a self-improving language model on its own verified trajectories.",
        "We train an LLM agent using GRPO on self-generated tasks.",
        "We distill a student language model from API teacher responses across iterations.",
        "Our self-improving agent uses reinforcement learning to refine its policy.",
        "We update model weights using gradient descent on self-generated solutions.",
        "We introduce an agent training dataset. We fine-tune Qwen3.5-9B on these trajectories.",
        "We present a self-improving framework. GRPO then trains a LoRA adapter on agent traces.",
    ],
)
def test_rsi_keeps_actual_model_training_including_api_teachers(abstract):
    paper = replace(
        make_paper("scope-test", topics=(SELF_EVOLUTION_TOPIC,)),
        title="Recursive Self-Improvement for Language Models",
        abstract=abstract,
    )
    assert model_training_evidence(paper.title, abstract)
    assert is_eligible(classify_highlights(paper))


def test_continual_training_is_deleted_even_with_other_topics_and_training():
    paper = replace(
        make_paper("scope-test", topics=("llm-continual-training", "user-requested")),
        abstract="We train language models with GRPO to learn from self-generated feedback.",
    )
    classified = classify_highlights(paper)
    assert not is_eligible(classified)
    assert not is_eligible(Paper.from_dict(classified.to_dict()))
    text_only = replace(paper, topics=("user-requested",), title="Continual Post-Training of LLMs")
    assert not is_eligible(text_only)
    assert "llm-continual-training" not in ArxivSource.topic_queries()
    assert "llm-continual-training" not in TOPIC_TITLES


def test_no_training_requirement_for_unrelated_long_horizon_evaluation():
    paper = replace(
        make_paper("scope-test", topics=("long-horizon-agent",)),
        title="Evaluating Long-Horizon LLM Agents",
        abstract="We evaluate an API-based agent on multi-step tasks.",
    )
    assert is_eligible(paper)


def test_refresh_removes_old_entry_when_new_metadata_disqualifies_it(tmp_path):
    archive = ArchiveRepository(tmp_path)
    old = make_paper("scope-test", topics=(SELF_EVOLUTION_TOPIC,))
    archive.update(date(2026, 11, 25), [old])
    new = replace(
        old,
        updated=old.updated + timedelta(days=1),
        abstract="We use a frozen LLM for training-free recursive self-improvement.",
    )
    result = archive.update(date(2026, 11, 26), [new])
    assert not result.all_papers
    assert not archive._load()
    assert not any(json.loads((tmp_path / "data/discoveries.json").read_text("utf-8")).values())
    assert all(
        "https://arxiv.org/abs/scope-test" not in path.read_text("utf-8")
        for path in (tmp_path / "papers").rglob("*.md")
    )


def test_recuration_purges_cross_topic_history_cache_and_pending_ids(tmp_path):
    from agent_paper_digest.candidates import CandidateRepository
    from agent_paper_digest.state import DigestStateStore
    from scripts.recurate_repository import run

    trained = make_paper("scope-trained", topics=(SELF_EVOLUTION_TOPIC,))
    continual = replace(
        trained, arxiv_id="scope-continual", topics=(SELF_EVOLUTION_TOPIC, "llm-continual-training")
    )
    api_only = replace(
        trained,
        arxiv_id="scope-api",
        topics=(SELF_EVOLUTION_TOPIC, "long-horizon-agent"),
        abstract="We use an LLM API for training-free long-horizon tasks.",
    )
    original = [trained, continual, api_only]
    (tmp_path / "data").mkdir()
    (tmp_path / "data/papers.json").write_text(
        json.dumps([p.to_dict() for p in original]), encoding="utf-8"
    )
    CandidateRepository(tmp_path).save(original)
    DigestStateStore(tmp_path).stage(trained.updated, tuple(p.arxiv_id for p in original))
    result = run(tmp_path)
    assert [p.arxiv_id for p in result] == [trained.arxiv_id]
    assert [p.arxiv_id for p in CandidateRepository(tmp_path).load()] == [trained.arxiv_id]
    assert DigestStateStore(tmp_path).load().pending_paper_ids == (trained.arxiv_id,)
    excluded = json.loads((tmp_path / "data/excluded_paper_ids.json").read_text("utf-8"))
    assert "llm_continual_training" in excluded[continual.arxiv_id]
    assert "self_improvement_without_model_training_evidence" in excluded[api_only.arxiv_id]
    assert "LLM continual training |" not in (tmp_path / "README.md").read_text("utf-8")


@pytest.mark.asyncio
async def test_automatic_pipeline_filters_new_records_and_stale_delivery_queue(tmp_path):
    from agent_paper_digest.candidates import CandidateRepository
    from agent_paper_digest.pipeline import DailyDigestPipeline
    from agent_paper_digest.state import DigestStateStore

    keep = make_paper("scope-trained", topics=(SELF_EVOLUTION_TOPIC,))
    api = replace(keep, arxiv_id="scope-api", abstract="We call an LLM API to evolve prompts.")
    retired = replace(keep, arxiv_id="scope-continual", title="Continual Training of LLMs")

    class Source:
        async def fetch(self, **kwargs):
            return [keep, api, retired]

    state = DigestStateStore(tmp_path)
    state.stage(keep.updated, (api.arxiv_id, retired.arxiv_id))
    result = await DailyDigestPipeline(
        source=Source(),
        archive=ArchiveRepository(tmp_path),
        notifier=None,
        git_sync=None,
    ).run(keep.updated)
    assert [p.arxiv_id for p in result.all_papers] == [keep.arxiv_id]
    assert [p.arxiv_id for p in CandidateRepository(tmp_path).load()] == [keep.arxiv_id]
    assert state.load().pending_paper_ids == (keep.arxiv_id,)
    assert state.load().last_successful_run_at is None
