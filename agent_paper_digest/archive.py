from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .models import Paper

TOPIC_TITLES = {
    "agent-self-evolving": "Agent Self-Evolving",
    "agent-memory": "Agent Memory",
    "llm-continual-training": "LLM Continual Training",
}


@dataclass(frozen=True, slots=True)
class ArchiveResult:
    """Artifacts produced by one discovery run."""

    discovery_date: date
    daily_path: Path
    daily_url: str
    new_papers: tuple[Paper, ...]
    all_papers: tuple[Paper, ...]


class ArchiveRepository:
    """Maintain daily Markdown pages, a JSON dataset, and an Awesome-style index."""

    def __init__(self, root: Path | str, repository_url: str = "") -> None:
        self.root = Path(root).resolve()
        self.repository_url = repository_url.rstrip("/")

    def _load(self) -> list[Paper]:
        dataset_path = self.root / "data" / "papers.json"
        if not dataset_path.exists():
            return []
        values = json.loads(dataset_path.read_text(encoding="utf-8"))
        return [Paper.from_dict(value) for value in values]

    def update(self, discovery_date: date, papers: list[Paper]) -> ArchiveResult:
        """Persist a run and rebuild all derived Markdown files.

        Args:
            discovery_date: Local calendar date assigned to this run.
            papers: Recent papers returned by the source.

        Returns:
            Paths and paper sets needed for notification and Git synchronization.
        """
        self.root.mkdir(parents=True, exist_ok=True)
        existing = {paper.arxiv_id: paper for paper in self._load()}
        known_ids = set(existing)
        new_papers: list[Paper] = []
        for paper in papers:
            current = existing.get(paper.arxiv_id)
            if current:
                existing[paper.arxiv_id] = current.merge(paper)
            else:
                existing[paper.arxiv_id] = paper
                new_papers.append(paper)

        all_papers = sorted(
            existing.values(),
            key=lambda item: (item.published, item.updated, item.arxiv_id),
            reverse=True,
        )
        data_dir = self.root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "papers.json").write_text(
            json.dumps([paper.to_dict() for paper in all_papers], ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )

        daily_path = (
            self.root
            / "papers"
            / str(discovery_date.year)
            / f"{discovery_date.month:02d}"
            / f"{discovery_date.isoformat()}.md"
        )
        daily_path.parent.mkdir(parents=True, exist_ok=True)
        daily_path.write_text(
            self._render_daily(discovery_date, new_papers),
            encoding="utf-8",
        )
        (self.root / "README.md").write_text(
            self._render_readme(all_papers),
            encoding="utf-8",
        )
        relative = daily_path.relative_to(self.root).as_posix()
        daily_url = (
            f"{self.repository_url}/blob/main/{relative}" if self.repository_url else relative
        )
        return ArchiveResult(
            discovery_date=discovery_date,
            daily_path=daily_path,
            daily_url=daily_url,
            new_papers=tuple(paper for paper in new_papers if paper.arxiv_id not in known_ids),
            all_papers=tuple(all_papers),
        )

    def _render_daily(self, discovery_date: date, papers: list[Paper]) -> str:
        lines = [
            f"# Daily Papers · {discovery_date.isoformat()}",
            "",
            f"> Discovered **{len(papers)}** new paper(s) across three research tracks.",
            "",
            "[← Back to index](../../../README.md)",
            "",
        ]
        if not papers:
            lines.extend(["No new papers were discovered in this run.", ""])
            return "\n".join(lines)
        for topic, title in TOPIC_TITLES.items():
            topic_papers = [paper for paper in papers if topic in paper.topics]
            if not topic_papers:
                continue
            lines.extend([f"## {title}", ""])
            for paper in topic_papers:
                authors = ", ".join(paper.authors)
                lines.extend(
                    [
                        f"### [{paper.title}]({paper.url})",
                        "",
                        f"- **Authors:** {authors}",
                        f"- **Published:** {paper.published.date().isoformat()}",
                        f"- **Categories:** {', '.join(paper.categories)}",
                        f"- **Links:** [Paper]({paper.url}) · [PDF]({paper.pdf_url})",
                        "",
                        paper.abstract,
                        "",
                    ]
                )
        return "\n".join(lines)

    def _render_readme(self, papers: list[Paper]) -> str:
        daily_paths = sorted((self.root / "papers").glob("*/*/*.md"), reverse=True)
        topic_counts = {
            topic: sum(topic in paper.topics for paper in papers) for topic in TOPIC_TITLES
        }
        lines = [
            "# Awesome Agent Evolution Papers",
            "",
            "<div align=\"center\">",
            "",
            "A daily collection of papers on **agent self-evolution**, **agent memory**,",
            "and **LLM continual training**, powered by AstrBot.",
            "",
            "![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)",
            "![AstrBot](https://img.shields.io/badge/AstrBot-4.26+-76bad9)",
            "![Update](https://img.shields.io/badge/update-daily-brightgreen)",
            "",
            "</div>",
            "",
            "## 🚀 Quick Start",
            "",
            "See [Deployment Guide](docs/deployment.md) to install the AstrBot plugin,",
            "configure an enterprise WeChat group webhook, and enable GitHub sync.",
            "",
            "## 📊 Statistics",
            "",
            "| Metric | Count |",
            "| --- | ---: |",
            f"| Total papers | {len(papers)} |",
            f"| Agent self-evolving | {topic_counts['agent-self-evolving']} |",
            f"| Agent memory | {topic_counts['agent-memory']} |",
            f"| LLM continual training | {topic_counts['llm-continual-training']} |",
            f"| Daily archives | {len(daily_paths)} |",
            "",
            "## 📋 Table of Contents",
            "",
            "- [Latest Papers](#-latest-papers)",
            "- [Daily Archive](#️-daily-archive)",
            "- [Dataset](data/papers.json)",
            "- [Deployment Guide](docs/deployment.md)",
            "",
            "## 📝 Latest Papers",
            "",
            "| Published | Track | Paper | Links |",
            "| --- | --- | --- | --- |",
        ]
        for paper in papers[:30]:
            topics = ", ".join(TOPIC_TITLES.get(topic, topic) for topic in paper.topics)
            title = paper.title.replace("|", "\\|")
            lines.append(
                f"| {paper.published.date().isoformat()} | {topics} | [{title}]({paper.url}) "
                f"| [Paper]({paper.url}) / [PDF]({paper.pdf_url}) |"
            )
        if not papers:
            lines.append("| - | - | No papers archived yet | - |")
        lines.extend(["", "## 🗓️ Daily Archive", ""])
        if daily_paths:
            for path in daily_paths:
                relative = path.relative_to(self.root).as_posix()
                lines.append(f"- [{path.stem}]({relative})")
        else:
            lines.append("No daily runs have been archived yet.")
        lines.extend(
            [
                "",
                "## 🔎 Search Scope",
                "",
                "- **Agent Self-Evolving:** self-evolving, self-improving, and evolving agents",
                "- **Agent Memory:** long-term, memory-augmented, and persistent agent memory",
                "- **LLM Continual Training:** continual, lifelong, and post-deployment "
                "LLM learning",
                "",
                "## License",
                "",
                "Code is released under the MIT License. Paper metadata remains subject "
                "to its source terms.",
                "",
            ]
        )
        return "\n".join(lines)
