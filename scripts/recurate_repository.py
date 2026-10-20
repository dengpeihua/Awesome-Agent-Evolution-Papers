from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agent_paper_digest.archive import ArchiveRepository  # noqa: E402
from agent_paper_digest.candidates import CandidateRepository  # noqa: E402
from agent_paper_digest.highlight import (  # noqa: E402
    HIGH_CITATION_COUNT,
    classify_highlights,
    qualification_reasons,
)
from agent_paper_digest.models import Paper  # noqa: E402
from agent_paper_digest.topics import (  # noqa: E402
    MIN_PUBLICATION_DATE,
    REINFORCEMENT_LEARNING_TOPIC,
    TOPIC_TITLES,
    rl_relevance_evidence,
)


def _write_audit(root: Path, candidates: list[Paper], papers: tuple[Paper, ...]) -> None:
    reason_counts = Counter(reason for paper in papers for reason in qualification_reasons(paper))
    audit = {
        "generated_at": datetime.now(UTC).isoformat(),
        "policy": {
            "required_topics": list(TOPIC_TITLES),
            "first_publication_on_or_after": MIN_PUBLICATION_DATE.date().isoformat(),
            "rl_scope": "Substantive RL directly related to language models or language agents",
            "highlight_signals": [
                "CCF-A Artificial Intelligence Full/Regular paper",
                "Selected top venue, including ECCV, EMNLP and ICLR",
                "verified big-tech paper or first-author affiliation",
                f"at least {HIGH_CITATION_COUNT} citations",
            ],
            "code_stars_are_qualifying": False,
        },
        "candidate_count": len(candidates),
        "candidate_topic_counts": {
            topic: sum(topic in paper.topics for paper in candidates) for topic in TOPIC_TITLES
        },
        "public_paper_count": len(papers),
        "topic_counts": {
            topic: sum(topic in paper.topics for paper in papers) for topic in TOPIC_TITLES
        },
        "qualification_counts": dict(sorted(reason_counts.items())),
        "notes": [
            "Qualification counts overlap when one paper meets multiple criteria.",
            "All topical papers are public; highlight signals do not gate inclusion.",
            "Citation counts are source-attributed snapshots and may change over time.",
        ],
    }
    (root / "data" / "curation_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (root / "data" / "rl_screening.json").write_text(
        json.dumps(
            {
                "policy": "Language-model context AND substantive RL evidence; "
                "inherited tags ignored",
                "evidence_level": "Automated title/abstract screening, not full-paper verification",
                "papers": [
                    {
                        "id": p.arxiv_id,
                        "published": p.published.isoformat(),
                        "evidence": rl_relevance_evidence(p.title, p.abstract),
                    }
                    for p in papers
                    if REINFORCEMENT_LEARNING_TOPIC in p.topics
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_report(root: Path, candidates: list[Paper], papers: tuple[Paper, ...]) -> None:
    reasons = Counter(reason for paper in papers for reason in qualification_reasons(paper))
    lines = [
        "# Agent Evolution Curated Corpus Audit",
        "",
        "## Scope",
        "",
        "The public corpus covers five directions plus explicit requests: "
        "papers address Agent/LLM "
        "self-evolution, self-improving systems, recursive self-improvement, Agent Memory, "
        "LLM continual training, language-model/agent Reinforcement Learning, "
        "or long-horizon agents. "
        "First publication must be on or after 2025-01-01. Priority evidence is optional.",
        "",
        "## Current result",
        "",
        f"- Topic candidates evaluated: **{len(candidates)}**",
        f"- Papers retained in the public repository: **{len(papers)}**",
        f"- CCF-A (Artificial Intelligence): **{reasons['CCF-A']}**",
        f"- Selected top venues: **{reasons['Selected venue']}**",
        f"- Big-tech affiliation: **{reasons['Industry']}**",
        f"- At least {HIGH_CITATION_COUNT} citations: **{reasons['Highly cited']}**",
        "",
        "Counts overlap because one paper may satisfy multiple qualifiers. GitHub stars "
        "are displayed as context but do not qualify a paper for inclusion.",
        "",
        "## Evidence boundaries",
        "",
        "- Venue qualification uses CCF-A venues in the Artificial Intelligence category, "
        "plus the selected venues in docs/curation.md.",
        "- Only main-track Full/Regular conference papers qualify by venue; Findings, "
        "workshop, demo, short, submitted, and under-review records do not.",
        "- Big-tech status requires paper-specific affiliation evidence or a first-author "
        "industry profile; a generic coauthor profile is insufficient.",
        "- Topical preprints are included without an industry or citation requirement.",
        "- Missing evidence is never inferred.",
        "",
    ]
    (root / "allinone.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path) -> tuple[Paper, ...]:
    archive = ArchiveRepository(root)
    candidates = CandidateRepository(root)
    pool = candidates.merge(archive._load())
    classified = [classify_highlights(paper) for paper in pool]
    candidates.save(classified)
    public = archive.replace_dataset(classified)
    _write_audit(root, classified, public)
    _write_report(root, classified, public)
    return public


if __name__ == "__main__":
    result = run(PROJECT_ROOT)
    print(f"Retained {len(result)} topical papers")
