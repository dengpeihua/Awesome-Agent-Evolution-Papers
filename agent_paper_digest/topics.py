from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Final

from .models import Paper

SELF_EVOLUTION_TOPIC: Final = "agent-llm-self-evolution"
AGENT_MEMORY_TOPIC: Final = "agent-memory"
CONTINUAL_TRAINING_TOPIC: Final = "llm-continual-training"
REINFORCEMENT_LEARNING_TOPIC: Final = "reinforcement-learning"
LONG_HORIZON_TOPIC: Final = "long-horizon-agent"
REQUESTED_TOPIC: Final = "user-requested"
MIN_PUBLICATION_DATE: Final = datetime(2025, 5, 1, tzinfo=UTC)

TOPIC_ORDER: Final = (
    SELF_EVOLUTION_TOPIC,
    CONTINUAL_TRAINING_TOPIC,
    REINFORCEMENT_LEARNING_TOPIC,
    LONG_HORIZON_TOPIC,
    REQUESTED_TOPIC,
)
TOPIC_TITLES: Final = {
    SELF_EVOLUTION_TOPIC: (
        "Agent & LLM Self-Evolution / Self-Improving / Recursive Self-Improvement"
    ),
    CONTINUAL_TRAINING_TOPIC: "LLM Continual Training & Continual Learning",
    REINFORCEMENT_LEARNING_TOPIC: "Reinforcement Learning",
    LONG_HORIZON_TOPIC: "Long-Horizon Task Agents",
    REQUESTED_TOPIC: "Explicitly Requested Papers",
}
TOPIC_SHORT: Final = {
    SELF_EVOLUTION_TOPIC: "Agent/LLM Self-Improvement",
    CONTINUAL_TRAINING_TOPIC: "LLM Continual Training",
    REINFORCEMENT_LEARNING_TOPIC: "Reinforcement Learning",
    LONG_HORIZON_TOPIC: "Long-Horizon Task Agents",
    REQUESTED_TOPIC: "Explicitly Requested Papers",
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
    r"\b(?:(?:continual|continued|continuous|life[- ]long|online)\s+"
    r"(?:pre[- ]?train\w*|post[- ]?train\w*|train\w*|fine[- ]?tun\w*|"
    r"adapt\w*|learn\w*)|catastrophic forgetting|knowledge retention)\b",
    re.IGNORECASE,
)

LANGUAGE_CONTEXT: Final = re.compile(
    r"\b(?:llms?|vlms?|(?:large |vision[- ]|multimodal )?language models?|"
    r"language[- ](?:model[- ])?agents?)\b",
    re.IGNORECASE,
)
RL_METHOD: Final = re.compile(
    r"\b(?:reinforcement[- ]learning|RLHF|RLAIF|RLVR|GRPO|PPO|"
    r"(?:group relative|proximal|group[- ]in[- ]group) policy optimi[sz]ation|"
    r"GiGPO|RL[- ](?:driven|trained))\b",
    re.IGNORECASE,
)
RL_CONTRIBUTION: Final = re.compile(
    r"\b(?:we |our |propos\w*|introduc\w*|develop\w*|present\w*|"
    r"train\w*|fine[- ]?tun\w*|post[- ]train\w*|optimi[sz]\w*|"
    r"analy[sz]\w*|stud\w*|investigat\w*|benchmark\w*)\b",
    re.IGNORECASE,
)
INCIDENTAL_RL: Final = re.compile(
    r"\b(?:without (?:using |any )?(?:reinforcement learning|RL)|RL[- ]free|"
    r"(?:reinforcement learning|RL) baselines?|too costly|(?:unlike|instead of) "
    r"(?:reinforcement learning|RL))\b",
    re.IGNORECASE,
)


def rl_relevance_evidence(title: str, abstract: str) -> str:
    """Require language-model context and substantive RL evidence, not query labels."""
    text = f"{title}\n{abstract}"
    if not LANGUAGE_CONTEXT.search(text):
        return ""
    if re.search(
        r"\b(?:robot(?:ic|ics)?|humanoid|manipulation|loco[- ]manipulation|"
        r"autonomous driving|motion planning|sim[- ]to[- ]real|VLA|"
        r"traffic (?:control|signal)|quantum networks?)\b",
        title,
        re.IGNORECASE,
    ):
        return ""
    if re.search(r"\bsurvey\b", text, re.IGNORECASE) and not RL_METHOD.search(title):
        return ""
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    for sentence in sentences:
        if not RL_METHOD.search(sentence) or INCIDENTAL_RL.search(sentence):
            continue
        # Title-level RL and an explicit language-model context form a strong
        # signal. Abstract-only mentions also require a contribution/training cue.
        if (
            sentence == title
            and LANGUAGE_CONTEXT.search(title)
            and not re.search(r"\bLLM[- ](?:guided|assisted)\b", title, re.IGNORECASE)
        ):
            return sentence
        if RL_CONTRIBUTION.search(sentence) and (
            LANGUAGE_CONTEXT.search(sentence)
            or (
                re.search(r"\b(?:we|our)\b", sentence, re.IGNORECASE)
                and re.search(r"\b(?:RLHF|RLAIF|RLVR|GRPO)\b", sentence, re.IGNORECASE)
            )
        ):
            return sentence
    if RL_METHOD.search(title):
        for sentence in sentences[1:]:
            if (
                LANGUAGE_CONTEXT.search(sentence)
                and re.search(
                    r"\b(?:train\w*|fine[- ]tun\w*|learn\w*)\b.{0,70}\b(?:policy|reward)\b",
                    sentence,
                    re.IGNORECASE,
                )
                and not INCIDENTAL_RL.search(sentence)
            ):
                return f"{title} — {sentence}"
    return ""


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
    topics = set(normalize_topics(existing)) - {REINFORCEMENT_LEARNING_TOPIC, LONG_HORIZON_TOPIC}
    if (
        LANGUAGE_CONTEXT.search(text)
        and re.search(r"\bagent(?:s|ic)?\b", text, re.I)
        and re.search(
            (
                r"\b(?:long[- ]?horizon|long[- ](?:trajectories|running tasks)|"
                r"multi[- ]step tasks|extended[- ]horizon)\b"
            ),
            text,
            re.I,
        )
    ):
        topics.add(LONG_HORIZON_TOPIC)
    if AGENT_LLM_PATTERN.search(text) and SELF_EVOLUTION_PATTERN.search(text):
        topics.add(SELF_EVOLUTION_TOPIC)
    if LLM_PATTERN.search(text) and CONTINUAL_TRAINING_PATTERN.search(text):
        topics.add(CONTINUAL_TRAINING_TOPIC)
    if rl_relevance_evidence(title, abstract):
        topics.add(REINFORCEMENT_LEARNING_TOPIC)
    return tuple(topic for topic in TOPIC_ORDER if topic in topics)


def infer_topics(paper: Paper) -> tuple[str, ...]:
    """Return normalized existing labels plus directions evidenced by paper text."""
    return infer_topics_from_text(
        paper.title,
        paper.abstract,
        existing=paper.topics,
    )


def is_agent_memory(paper: Paper) -> bool:
    """Reject both legacy memory tags and text-evidenced agent-memory papers."""
    text = f"{paper.title}\n{paper.abstract}"
    return AGENT_MEMORY_TOPIC in paper.topics or bool(
        AGENT_LLM_PATTERN.search(text) and AGENT_MEMORY_PATTERN.search(text)
    )
