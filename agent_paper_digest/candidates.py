from __future__ import annotations

import json
from pathlib import Path

from .models import Paper


class CandidateRepository:
    """Keep non-public topic candidates for later venue/citation promotion."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.path = self.root / ".paper_digest" / "candidates.json"

    def load(self) -> list[Paper]:
        if not self.path.exists():
            return []
        values = json.loads(self.path.read_text(encoding="utf-8"))
        return [Paper.from_dict(value) for value in values]

    def merge(self, papers: list[Paper]) -> list[Paper]:
        merged = {paper.arxiv_id: paper for paper in self.load()}
        for paper in papers:
            current = merged.get(paper.arxiv_id)
            merged[paper.arxiv_id] = current.merge(paper) if current else paper
        return sorted(
            merged.values(),
            key=lambda item: (item.updated, item.published, item.arxiv_id),
            reverse=True,
        )

    def save(self, papers: list[Paper]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([paper.to_dict() for paper in papers], ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )
