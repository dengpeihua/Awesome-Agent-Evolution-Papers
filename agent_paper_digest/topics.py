from __future__ import annotations

import re
from typing import Final

from .models import Paper

SELF_EVOLUTION_TOPIC: Final = "agent-llm-self-evolution"
AGENT_MEMORY_TOPIC: Final = "agent-memory"
CONTINUAL_TRAINING_TOPIC: Final = "llm-continual-training"

TOPIC_ORDER: Final = (
    SELF_EVOLUTION_TOPIC,
    AGENT_MEMORY_TOPIC,
    CONTINUAL_TRAINING_TOPIC,
)
TOPIC_TITLES: Final = {
    SELF_EVOLUTION_TOPIC: (
        "Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement"
    ),
    AGENT_MEMORY_TOPIC: "Agent Memory",
    CONTINUAL_TRAINING_TOPIC: "LLM Continual Training & Continual Learning",
}
TOPIC_SHORT: Final = {
    SELF_EVOLUTION_TOPIC: "Agent/LLM Self-Improvement",
    AGENT_MEMORY_TOPIC: "Agent Memory",
    CONTINUAL_TRAINING_TOPIC: "LLM Continual Training",
}
REQUIRED_TOPICS: Final = frozenset(TOPIC_ORDER)

LEGACY_TOPIC_ALIASES: Final = {
    "agent-self-evolving": SELF_EVOLUTION_TOPIC,
}

AGENT_LLM_PATTERN: Final = re.compile(
    r"\b(?:agent(?:ic|s)?|llm(?:s)?|large language model(?:s)?|language model(?:s)?|"
    r"foundation model(?:s)?)\b",
    re.IGNORECASE,
)
LLM_PATTERN: Final = re.compile(
    r"\b(?:llm(?:s)?|large language model(?:s)?|language model(?:s)?|"
    r"foundation model(?:s)?)\b",
    re.IGNORECASE,
)
SELF_EVOLUTION_PATTERN: Final = re.compile(
    r"\b(?:self[- ]?(?:evol\w*|improv\w*|refin\w*|enhanc\w*|correct\w*|"
    r"train\w*|reward\w*|generated feedback)|recursive self[- ]improvement|"
    r"iterative self[- ]improvement|"
    r"co[- ]?evol\w*|agent evolution|harness evolution|evolving (?:agent|skill|"
    r"capabilit|workflow)\w*)\b",
    re.IGNORECASE,
)
AGENT_MEMORY_PATTERN: Final = re.compile(
    r"\b(?:agentic memory|agent memory|memory[- ]augmented (?:agent|llm)|"
    r"(?:long[- ]term|episodic|semantic|procedural|working) memory (?:for |of )?"
    r"(?:agent|llm)|memory (?:system|module|bank|store|retrieval|consolidation|"
    r"management) (?:for |in )?(?:agent|llm)|(?:agent|llm)s?['’]? memory)\b",
    re.IGNORECASE,
)
CONTINUAL_TRAINING_PATTERN: Final = re.compile(
    r"\b(?:(?:continual|continued|continuous|lifelong|online)\s+"
    r"(?:pre[- ]?train\w*|post[- ]?train\w*|train\w*|fine[- ]?tun\w*|"
    r"adapt\w*|learn\w*)|catastrophic forgetting|knowledge retention)\b",
    re.IGNORECASE,
)


def normalize_topics(topics: tuple[str, ...]) -> tuple[str, ...]:
    """Migrate legacy labels and return known topics in stable display order."""
    normalized = {LEGACY_TOPIC_ALIASES.get(topic, topic) for topic in topics}
    return tuple(topic for topic in TOPIC_ORDER if topic in normalized)


def infer_topics_from_text(
    title: str,
    abstract: str,
    *,
    existing: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Infer the requested directions while requiring an Agent/LLM context."""
    text = f"{title}\n{abstract}"
    topics = set(normalize_topics(existing))
    if AGENT_LLM_PATTERN.search(text) and SELF_EVOLUTION_PATTERN.search(text):
        topics.add(SELF_EVOLUTION_TOPIC)
    if AGENT_LLM_PATTERN.search(text) and AGENT_MEMORY_PATTERN.search(text):
        topics.add(AGENT_MEMORY_TOPIC)
    if LLM_PATTERN.search(text) and CONTINUAL_TRAINING_PATTERN.search(text):
        topics.add(CONTINUAL_TRAINING_TOPIC)
    return tuple(topic for topic in TOPIC_ORDER if topic in topics)


def infer_topics(paper: Paper) -> tuple[str, ...]:
    """Return normalized existing labels plus directions evidenced by paper text."""
    return infer_topics_from_text(
        paper.title,
        paper.abstract,
        existing=paper.topics,
    )
