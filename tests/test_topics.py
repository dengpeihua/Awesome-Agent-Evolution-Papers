from dataclasses import replace

import pytest

from agent_paper_digest.topics import (
    SELF_EVOLUTION_TOPIC,
    infer_topics,
    normalize_topics,
    rl_relevance_evidence,
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

    assert infer_topics(paper) == ("agent-llm-self-evolution", "reinforcement-learning")


def test_detects_llm_reinforcement_from_self_generated_feedback() -> None:
    paper = replace(
        make_paper("2609.10006", topics=()),
        title="Reinforcement Learning from Self-Generated Feedback",
        abstract="A language model learns a stronger policy from its own critiques.",
    )

    assert infer_topics(paper) == ("agent-llm-self-evolution", "reinforcement-learning")


def test_detects_llm_continual_post_training() -> None:
    paper = replace(
        make_paper("2609.10003", topics=()),
        title="Continual Post-Training of Foundation Models",
        abstract="We mitigate catastrophic forgetting during lifelong model adaptation.",
    )

    assert infer_topics(paper) == ("llm-continual-training",)


def test_detects_hyphenated_life_long_learning_in_agent_world() -> None:
    paper = replace(
        make_paper("2604.18292", topics=()),
        title=(
            "Agent-World: Scaling Real-World Environment Synthesis for "
            "Evolving General Agent Intelligence"
        ),
        abstract=(
            "Large language models need principled mechanisms for life-long learning. "
            "We present a self-evolving training arena for general agents."
        ),
    )

    assert infer_topics(paper) == (
        "agent-llm-self-evolution",
        "llm-continual-training",
    )


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


@pytest.mark.parametrize(
    "title,abstract",
    [
        (
            "Traffic control with reinforcement learning",
            "We train PPO policies for traffic lights.",
        ),
        (
            "LLM Robot Planner",
            "We use a language model for planning. PPO trains the motor controller.",
        ),
        ("LLM Code Designer", "Our language model outperforms a reinforcement learning baseline."),
        ("LLM Data Security Survey", "This survey covers LLMs, RLHF, data cleaning and RAG."),
        (
            "Fetch My Beer",
            "Fluid simulation is too costly for reinforcement learning. "
            "We use a vision-language model to filter grasps.",
        ),
    ],
)
def test_rl_rejects_incidental_mentions_and_legacy_tags(title, abstract):
    paper = replace(
        make_paper("2609.001", topics=("reinforcement-learning",)), title=title, abstract=abstract
    )
    assert "reinforcement-learning" not in infer_topics(paper)
    assert not rl_relevance_evidence(title, abstract)


@pytest.mark.parametrize(
    "title,abstract",
    [
        ("Agentic RL", "We train an LLM agent using GRPO on tool-use trajectories."),
        ("LLM Reinforcement Learning", "Language models optimize a reward objective."),
        ("Credit Assignment", "Language models suffer sparse rewards. We introduce GRPO updates."),
    ],
)
def test_rl_keeps_explicit_language_policy_training(title, abstract):
    assert rl_relevance_evidence(title, abstract)
