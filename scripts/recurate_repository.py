from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agent_paper_digest.archive import TOPIC_TITLES, ArchiveRepository  # noqa: E402
from agent_paper_digest.candidates import CandidateRepository  # noqa: E402
from agent_paper_digest.highlight import (  # noqa: E402
    HIGH_CITATION_COUNT,
    classify_highlights,
    qualification_reasons,
)


def _write_audit(root: Path, candidates: int, papers: tuple) -> None:
    reason_counts = Counter(reason for paper in papers for reason in qualification_reasons(paper))
    audit = {
        "generated_at": datetime.now(UTC).isoformat(),
        "policy": {
            "required_topics": list(TOPIC_TITLES),
            "qualifiers": [
                "CCF-A Artificial Intelligence Full/Regular paper",
                "ECCV or EMNLP Full/Regular paper",
                "verified big-tech paper or first-author affiliation",
                f"at least {HIGH_CITATION_COUNT} citations",
            ],
            "code_stars_are_qualifying": False,
        },
        "candidate_count": candidates,
        "public_paper_count": len(papers),
        "topic_counts": {
            topic: sum(topic in paper.topics for paper in papers) for topic in TOPIC_TITLES
        },
        "qualification_counts": dict(sorted(reason_counts.items())),
        "notes": [
            "Qualification counts overlap when one paper meets multiple criteria.",
            "Unqualified topical candidates stay only in the ignored local candidate cache.",
            "Citation counts are source-attributed snapshots and may change over time.",
        ],
    }
    (root / "data" / "curation_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_report(root: Path, candidates: int, papers: tuple) -> None:
    reasons = Counter(reason for paper in papers for reason in qualification_reasons(paper))
    lines = [
        "# Agent Evolution Curated Corpus Audit",
        "",
        "## Scope",
        "",
        "The public corpus is a strict intersection: every paper must address Agent "
        "Self-Evolving, Agent Memory, or LLM Continual Training and meet at least one "
        "verified qualification criterion.",
        "",
        "## Current result",
        "",
        f"- Topic candidates evaluated: **{candidates}**",
        f"- Papers retained in the public repository: **{len(papers)}**",
        f"- CCF-A (Artificial Intelligence): **{reasons['CCF-A']}**",
        f"- ECCV / EMNLP: **{reasons['Selected venue']}**",
        f"- Big-tech affiliation: **{reasons['Industry']}**",
        f"- At least {HIGH_CITATION_COUNT} citations: **{reasons['Highly cited']}**",
        "",
        "Counts overlap because one paper may satisfy multiple qualifiers. GitHub stars "
        "are displayed as context but do not qualify a paper for inclusion.",
        "",
        "## Evidence boundaries",
        "",
        "- Venue qualification uses CCF-A venues in the Artificial Intelligence category, "
        "plus ECCV and EMNLP requested for this collection.",
        "- Only main-track Full/Regular conference papers qualify by venue; Findings, "
        "workshop, demo, short, submitted, and under-review records do not.",
        "- Big-tech status requires paper-specific affiliation evidence or a first-author "
        "industry profile; a generic coauthor profile is insufficient.",
        "- Pure arXiv/preprint records need an independent big-tech or citation qualifier.",
        "- Missing evidence is never inferred.",
        "",
    ]
    (root / "allinone.md").write_text("\n".join(lines), encoding="utf-8")


def run(root: Path) -> tuple:
    archive = ArchiveRepository(root)
    candidates = CandidateRepository(root)
    pool = candidates.merge(archive._load())
    classified = [classify_highlights(paper) for paper in pool]
    candidates.save(classified)
    public = archive.replace_dataset(classified)
    _write_audit(root, len(classified), public)
    _write_report(root, len(classified), public)
    return public


if __name__ == "__main__":
    result = run(PROJECT_ROOT)
    print(f"Retained {len(result)} strictly curated papers")
