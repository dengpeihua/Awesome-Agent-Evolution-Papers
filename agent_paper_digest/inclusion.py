"""Explain admission from the same evidence used by the active scope rules."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .highlight import is_eligible
from .models import Paper
from .topics import (
    LONG_HORIZON_TOPIC,
    REQUESTED_TOPIC,
    SELF_EVOLUTION_PATTERN,
    SELF_EVOLUTION_TOPIC,
    infer_topics,
    model_training_evidence,
)


@dataclass(frozen=True, slots=True)
class InclusionReason:
    topic: str
    reason: str
    topic_evidence: str
    training_evidence: str
    source: str
    evidence_level: str = "标题／摘要自动筛选，非全文核验"


def inclusion_reasons(paper: Paper) -> tuple[InclusionReason, ...]:
    """Return traceable reasons only for papers that pass every exclusion."""
    if not is_eligible(paper):
        return ()
    sentences = re.split(r"(?<=[.!?])\s+|\n+", f"{paper.title}\n{paper.abstract}")
    training = model_training_evidence(paper.title, paper.abstract)
    reasons = []
    for topic in infer_topics(paper):
        if topic == SELF_EVOLUTION_TOPIC:
            evidence = next(s for s in sentences if SELF_EVOLUTION_PATTERN.search(s))
            reason = "涉及语言模型／Agent 的自我改进，摘要提供模型训练依据。"
        elif topic == LONG_HORIZON_TOPIC:
            evidence = next(
                s
                for s in sentences
                if re.search(
                    r"\b(?:long[- ]?horizon|long[- ](?:trajectories|running tasks)|"
                    r"multi[- ]step tasks|extended[- ]horizon)\b",
                    s,
                    re.I,
                )
            )
            reason = "涉及长程、多步语言 Agent 任务，摘要提供模型训练依据。"
        elif topic == REQUESTED_TOPIC:
            evidence = "用户明确指定收录；不等同于匹配两个研究主题。"
            reason = "用户指定补充论文，且通过当前排除规则。"
        else:
            continue
        reasons.append(InclusionReason(topic, reason, evidence, training, paper.url))
    return tuple(reasons)


def paper_record(paper: Paper) -> dict[str, object]:
    """Add regenerated evidence to public JSON without trusting stale explanations."""
    return {
        **paper.to_dict(),
        "inclusion_reasons": [asdict(reason) for reason in inclusion_reasons(paper)],
    }


def reason_summary(paper: Paper) -> str:
    """Concise admission explanation for tables and notifications."""
    return " ".join(dict.fromkeys(reason.reason for reason in inclusion_reasons(paper)))


def evidence_markdown(paper: Paper) -> list[str]:
    """Render paper-specific evidence independently of industry/venue priority."""
    lines = []
    for reason in inclusion_reasons(paper):
        lines.extend(
            [
                f"- **收录理由：** {reason.reason}",
                f"- **主题依据（标题／摘要）：** {reason.topic_evidence}",
            ]
        )
    training = model_training_evidence(paper.title, paper.abstract)
    if training:
        lines.append(f"- **训练依据（摘要）：** {training}")
    lines.append(
        f"- **依据来源：** [arXiv 原始记录]({paper.url})；标题／摘要自动筛选，非全文核验。"
    )
    return lines
