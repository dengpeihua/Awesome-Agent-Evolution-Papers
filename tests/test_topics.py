from dataclasses import replace

from agent_paper_digest.topics import (
    SELF_EVOLUTION_TOPIC,
    infer_topics,
    normalize_topics,
)
from tests.test_archive import make_paper


def test_migrates_legacy_agent_self_evolving_topic() -> None:
    assert normalize_topics(("agent-self-evolving", "agent-memory")) == (
        "agent-llm-self-evolution",
        "agent-memory",
    )


def test_detects_recursive_llm_self_improvement() -> None:
    paper = replace(
        make_paper("2609.10001", topics=()),
        title="Recursive Self-Improvement for Large Language Models",
        abstract="The language model edits its own training procedure over repeated cycles.",
    )

    assert SELF_EVOLUTION_TOPIC in infer_topics(paper)


def test_detects_agent_self_improvement_and_self_reinforcement() -> None:
    paper = replace(
        make_paper("2609.10002", topics=()),
        title="Learning to Improve",
        abstract=(
            "We introduce a self-improving LLM agent that uses reinforcement learning "
            "from self-generated feedback to refine its policy."
        ),
    )

    assert infer_topics(paper) == ("agent-llm-self-evolution",)


def test_detects_llm_continual_post_training() -> None:
    paper = replace(
        make_paper("2609.10003", topics=()),
        title="Continual Post-Training of Foundation Models",
        abstract="We mitigate catastrophic forgetting during lifelong model adaptation.",
    )

    assert infer_topics(paper) == ("llm-continual-training",)


def test_does_not_treat_generic_evolutionary_optimization_as_self_improvement() -> None:
    paper = replace(
        make_paper("2609.10004", topics=()),
        title="An Evolution Strategy for Warehouse Scheduling",
        abstract="A genetic algorithm optimizes a classical scheduling benchmark.",
    )

    assert infer_topics(paper) == ()


def test_preserves_agent_memory_as_a_separate_direction() -> None:
    paper = replace(
        make_paper("2609.10005", topics=()),
        title="Long-Term Episodic Memory for LLM Agents",
    )

    assert infer_topics(paper) == ("agent-memory",)
