from dataclasses import replace

import pytest

from agent_paper_digest.arxiv import ArxivSource
from agent_paper_digest.highlight import classify_highlights, is_eligible
from agent_paper_digest.models import Paper
from agent_paper_digest.topics import LONG_HORIZON_TOPIC, TOPIC_TITLES
from tests.test_archive import make_paper


@pytest.mark.parametrize(
    "abstract,expected",
    [
        ("We fine-tune a language model on expert demonstrations for multi-step tasks.", True),
        ("We distill a student language model using API teacher trajectories.", True),
        ("We call an LLM API to complete multi-step tasks without training.", False),
        ("We use a policy already fine-tuned on atomic tasks, keeping its weights fixed.", False),
        ("We train a language model with GRPO on long-horizon tasks.", False),
        ("We train a VLM using reinforcement learning for robotic manipulation.", False),
        ("We fine-tune language models on demonstrations without reinforcement learning.", True),
    ],
)
def test_long_horizon_training_and_rl_exclusion(abstract, expected):
    p = replace(
        make_paper("new-scope", topics=(LONG_HORIZON_TOPIC, "user-requested")),
        title="Long-Horizon Language Agents",
        abstract=abstract,
    )
    assert is_eligible(p) is expected
    assert is_eligible(classify_highlights(classify_highlights(p))) is expected


def test_rl_legacy_labels_are_excluded_and_not_active():
    p = make_paper("new-scope", topics=("agent-llm-self-evolution",))
    p = replace(p, topics=(*p.topics, "reinforcement-learning"))
    assert not is_eligible(Paper.from_dict(classify_highlights(p).to_dict()))
    assert "reinforcement-learning" not in TOPIC_TITLES
    assert "reinforcement-learning" not in ArxivSource.topic_queries()
    assert TOPIC_TITLES[LONG_HORIZON_TOPIC] == "Long-Horizon Agents"
