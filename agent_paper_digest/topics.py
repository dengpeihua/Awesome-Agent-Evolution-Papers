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
    REINFORCEMENT_LEARNING_TOPIC,
    LONG_HORIZON_TOPIC,
    REQUESTED_TOPIC,
)
TOPIC_TITLES: Final = {
    SELF_EVOLUTION_TOPIC: "Recursive Self-Improvement",
    REINFORCEMENT_LEARNING_TOPIC: "Reinforcement Learning",
    LONG_HORIZON_TOPIC: "Long-Horizon Task Agents",
    REQUESTED_TOPIC: "Explicitly Requested Papers",
}
TOPIC_SHORT: Final = {
    SELF_EVOLUTION_TOPIC: "Recursive Self-Improvement",
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
    topics = set(normalize_topics(existing)) - {
        SELF_EVOLUTION_TOPIC,
        REINFORCEMENT_LEARNING_TOPIC,
        LONG_HORIZON_TOPIC,
    }
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
    if (
        AGENT_LLM_PATTERN.search(text)
        and SELF_EVOLUTION_PATTERN.search(text)
        and model_training_evidence(title, abstract)
    ):
        topics.add(SELF_EVOLUTION_TOPIC)
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


def is_continual_training(paper: Paper) -> bool:
    """Exclude the retired track even when another topic also matches."""
    text = f"{paper.title}\n{paper.abstract}"
    return CONTINUAL_TRAINING_TOPIC in paper.topics or bool(
        LLM_PATTERN.search(text) and CONTINUAL_TRAINING_PATTERN.search(text)
    )


def is_self_improvement(paper: Paper) -> bool:
    """Include legacy labels when checking the training requirement."""
    return SELF_EVOLUTION_TOPIC in normalize_topics(paper.topics) or bool(
        AGENT_LLM_PATTERN.search(f"{paper.title}\n{paper.abstract}")
        and SELF_EVOLUTION_PATTERN.search(f"{paper.title}\n{paper.abstract}")
    )


def model_training_evidence(title: str, abstract: str) -> str:
    """Return an explicit method sentence about training the language model/policy.

    Missing evidence is not proof of API-only operation: it is insufficient for
    admission. Baseline training, prompt/code optimization, and inference-only
    refinement cannot establish model training. Keep the evidence for auditing.
    """
    if not LANGUAGE_CONTEXT.search(f"{title}\n{abstract}"):
        return ""
    if re.search(r"\b(?:training[- ]free|tuning[- ]free|inference[- ]only|survey)\b", title, re.I):
        return ""
    method_started = False
    for sentence in re.split(r"(?<=[.!?])\s+|\n+", abstract):
        method_started = method_started or bool(
            re.search(
                r"\b(?:we\s+(?:\w+\s+){0,2}(?:propose|introduce|present|develop|train|"
                r"fine[- ]tune|study|investigate|distill|update|fix|reformulate|address|construct)|"
                r"our (?:method|framework|"
                r"approach|model|self[- ]improving agent))\b",
                sentence,
                re.I,
            )
        )
        if re.search(
            r"\b(?:training[- ]free|tuning[- ]free|gradient[- ]free|inference[- ]only|"
            r"parameter[- ]update[- ]free|rather than|instead of|"
            r"without\b.{0,70}(?:train\w*|tun\w*|gradient\w*|updat\w*)|"
            r"without\b.{0,70}chang\w*.{0,35}(?:parameter|weight)\w*|"
            r"(?:no|does not|do not|never)\b.{0,35}(?:train\w*|tun\w*|updat\w*)|"
            r"(?:unlike|prior work|previous work|existing (?:methods|agents)|"
            r"baseline\w*|future work))\b",
            sentence,
            re.I,
        ):
            continue
        # Require a claim about this method, not a background statement that RL
        # or training generally improves LLMs.
        if not method_started:
            continue
        training_sentence = re.sub(r"\bpre[- ]?trained\b", "existing", sentence, flags=re.I)
        if re.search(
            r"\b(?:optimi[sz]\w*|updat\w*|evol\w*)\s+(?:the |our |a |an )?"
            r"(?:prompts?|harness\w*|workflows?|code|programs?|instructions?)\b",
            training_sentence,
            re.I,
        ) and not re.search(
            r"\b(?:fine[- ]?tun\w*|retrain\w*|distill\w*)\b", training_sentence, re.I
        ):
            continue
        if re.search(
            r"\b(?:train|trains|fine[- ]?tun\w*|retrain\w*)\s+"
            r"(?:(?!(?:data|setup|environment|procedure|capability|signal|prompt|harness)\b)"
            r"[\w-]+\s+){0,7}(?:models?|llms?|vlms?|students?|polic(?:y|ies)|"
            r"adapters?|LoRA|Qwen\w*|Llama\w*|GLM\w*|DeepSeek\w*|Gemma\w*)\b|"
            r"\b(?:update|optimi[sz]e)\s+(?:the |our |model )*(?:parameters|weights)\b|"
            r"\bdistill\w*\s+(?:a |the |our )?(?:small |language )*student\b|"
            r"\bdistill\w*\b.{0,100}\b(?:into|back into)\s+(?:the |a |our )?"
            r"(?:base |student |policy )?(?:model|policy|weights)\b",
            training_sentence,
            re.I,
        ) or re.search(
            r"\b(?:model|llm|vlm|student|agent|policy)\w*\b.{0,70}"
            r"\b(?:fine[- ]?tun\w*|retrain\w*|self[- ]train\w*|"
            r"(?:uses?|using|via|with|through)\s+(?:\w+\s+){0,3}"
            r"(?:reinforcement learning|GRPO|RLHF|RLVR|PPO|supervised fine[- ]?tuning))\b",
            training_sentence,
            re.I,
        ):
            return sentence.strip()
        if re.search(
            r"\b(?:performs?|applies?|coordinates?)\s+(?:joint |alternating )?"
            r"(?:parameter|weight) updates\b",
            training_sentence,
            re.I,
        ):
            return sentence.strip()
        if re.search(r"\b(?:apply|use)\b.{0,40}\bloss masking\b", training_sentence, re.I):
            return sentence.strip()
        if (
            re.search(
                r"\b(?:supervised fine[- ]?tuning|on[- ]policy (?:self[- ])?distillation|"
                r"policy gradients?|GRPO|RLHF|RLVR|OPD|SFT)\b",
                training_sentence,
                re.I,
            )
            and re.search(
                r"\b(?:we|our|train\w*|updat\w*|learn\w*|optimi[sz]\w*|"
                r"propos\w*|introduc\w*|framework|method)\b",
                training_sentence,
                re.I,
            )
            and not re.search(
                r"\b(?:compar\w*|outperform\w*|versus|vs|better than|over|TF[- ]GRPO)\b",
                training_sentence,
                re.I,
            )
        ):
            return sentence.strip()
    return ""


def scope_exclusion_reasons(paper: Paper) -> tuple[str, ...]:
    reasons = []
    if is_continual_training(paper):
        reasons.append("llm_continual_training")
    if is_self_improvement(paper) and not model_training_evidence(paper.title, paper.abstract):
        reasons.append("self_improvement_without_model_training_evidence")
    return tuple(reasons)
