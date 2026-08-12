from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .models import Paper

TOPIC_TITLES = {
    "agent-self-evolving": "Agent Self-Evolving",
    "agent-memory": "Agent Memory",
    "llm-continual-training": "LLM Continual Training",
}

TOPIC_SHORT = {
    "agent-self-evolving": "Self-Evolving",
    "agent-memory": "Memory",
    "llm-continual-training": "Continual Training",
}

POPULAR_CODE_STARS = 100
VERY_POPULAR_CODE_STARS = 1_000
HIGH_CITATION_COUNT = 10


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

    def _load_discoveries(self) -> dict[str, list[str]]:
        discovery_path = self.root / "data" / "discoveries.json"
        if discovery_path.exists():
            values = json.loads(discovery_path.read_text(encoding="utf-8"))
            return {str(day): list(ids) for day, ids in values.items()}

        # Migrate archives created before discovery tracking was introduced.
        discoveries: dict[str, list[str]] = {}
        for daily_path in (self.root / "papers").glob("*/*/*.md"):
            matches = re.findall(
                r"https://arxiv\.org/abs/([^)\s]+)",
                daily_path.read_text(encoding="utf-8"),
            )
            ids = sorted({re.sub(r"v\d+$", "", match) for match in matches})
            discoveries[daily_path.stem] = ids
        return discoveries

    def replace_dataset(self, papers: list[Paper]) -> tuple[Paper, ...]:
        """Replace the curated dataset and rebuild monthly and root indexes.

        This is intended for historical backfills. It deliberately leaves daily
        discovery records untouched so a backfill is not presented as one day's feed.
        """
        merged: dict[str, Paper] = {}
        for paper in papers:
            current = merged.get(paper.arxiv_id)
            merged[paper.arxiv_id] = current.merge(paper) if current else paper
        all_papers = sorted(
            merged.values(),
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
        self._write_monthly_archives(all_papers)
        (self.root / "README.md").write_text(
            self._render_readme(all_papers),
            encoding="utf-8",
        )
        return tuple(all_papers)

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
        discoveries = self._load_discoveries()
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

        day_key = discovery_date.isoformat()
        day_ids = discoveries.setdefault(day_key, [])
        for paper in new_papers:
            if paper.arxiv_id not in day_ids:
                day_ids.append(paper.arxiv_id)
        day_ids.sort()
        (data_dir / "discoveries.json").write_text(
            json.dumps(dict(sorted(discoveries.items())), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        daily_papers = [existing[arxiv_id] for arxiv_id in day_ids if arxiv_id in existing]

        daily_path = (
            self.root
            / "papers"
            / str(discovery_date.year)
            / f"{discovery_date.month:02d}"
            / f"{discovery_date.isoformat()}.md"
        )
        daily_path.parent.mkdir(parents=True, exist_ok=True)
        daily_path.write_text(
            self._render_daily(discovery_date, daily_papers),
            encoding="utf-8",
        )
        self._write_monthly_archives(all_papers)
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
                        f"- **Links:** [Paper]({paper.url}) · [PDF]({paper.pdf_url})"
                        + (f" · [Code]({paper.github_url})" if paper.github_url else ""),
                        "",
                        paper.abstract,
                        "",
                    ]
                )
        return "\n".join(lines)

    @staticmethod
    def _flags(paper: Paper) -> str:
        flags: list[str] = []
        if paper.github_stars is not None and paper.github_stars >= VERY_POPULAR_CODE_STARS:
            flags.append("🔥 Very popular code")
        elif paper.github_stars is not None and paper.github_stars >= POPULAR_CODE_STARS:
            flags.append("⭐ Popular code")
        if paper.citation_count is not None and paper.citation_count >= HIGH_CITATION_COUNT:
            flags.append("📈 Highly cited")
        if paper.industry_affiliations:
            flags.append("🏢 Industry")
        if paper.venue_tier == "top":
            flags.append("🏆 Top venue")
        flags.extend(reason for reason in paper.highlight_reasons if reason not in flags)
        return "<br>".join(flags) if flags else "—"

    @staticmethod
    def _metrics(paper: Paper) -> str:
        values: list[str] = []
        if paper.github_url:
            stars = f"{paper.github_stars:,}" if paper.github_stars is not None else "n/a"
            values.append(f"[GitHub ★ {stars}]({paper.github_url})")
        if paper.citation_count is not None:
            source = paper.citation_source or "citation source"
            values.append(f"Citations: {paper.citation_count} ({source})")
        return "<br>".join(values) if values else "—"

    def _write_monthly_archives(self, papers: list[Paper]) -> None:
        grouped: dict[tuple[int, int], list[Paper]] = defaultdict(list)
        for paper in papers:
            grouped[(paper.published.year, paper.published.month)].append(paper)
        years = sorted({paper.published.year for paper in papers} | {date.today().year})
        for year in years:
            months = range(1, 13)
            if year == date.today().year:
                months = range(1, date.today().month + 1)
            for month in months:
                month_papers = sorted(
                    grouped.get((year, month), []),
                    key=lambda item: (item.published, item.arxiv_id),
                    reverse=True,
                )
                path = self.root / "papers" / str(year) / f"{month:02d}" / "README.md"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    self._render_month(year, month, month_papers),
                    encoding="utf-8",
                )

    def _render_month(self, year: int, month: int, papers: list[Paper]) -> str:
        topic_counts = {
            topic: sum(topic in paper.topics for paper in papers) for topic in TOPIC_TITLES
        }
        lines = [
            f"# {year}-{month:02d} Agent Evolution Papers",
            "",
            "[← Back to main index](../../../README.md)",
            "",
            f"> {len(papers)} unique papers · "
            f"Self-Evolving {topic_counts['agent-self-evolving']} · "
            f"Memory {topic_counts['agent-memory']} · "
            f"Continual Training {topic_counts['llm-continual-training']}",
            "",
            "| Date | Track | Paper | Venue | Signals | Metrics |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for paper in papers:
            topics = "<br>".join(TOPIC_SHORT.get(topic, topic) for topic in paper.topics)
            title = paper.title.replace("|", "\\|")
            venue = paper.venue or "arXiv"
            links = f"[{title}]({paper.url})<br>[PDF]({paper.pdf_url})"
            lines.append(
                f"| {paper.published.date().isoformat()} | {topics} | {links} | {venue} | "
                f"{self._flags(paper)} | {self._metrics(paper)} |"
            )
        if not papers:
            lines.append("| — | — | No in-scope papers found in the verified corpus | — | — | — |")
        lines.extend(
            [
                "",
                "## Notes",
                "",
                "- A paper can appear in more than one track, but is counted once in the "
                "unique total.",
                "- Metrics are snapshots; see the main README for thresholds and "
                "verification policy.",
                "",
            ]
        )
        return "\n".join(lines)

    def _render_readme(self, papers: list[Paper]) -> str:
        daily_paths = sorted(
            (
                path
                for path in (self.root / "papers").glob("*/*/*.md")
                if path.name != "README.md"
            ),
            reverse=True,
        )
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
            "## 📚 Table of Contents",
            "",
            "- [Highlighted Papers](#highlighted-papers)",
            "- [2026 Monthly Index](#2026-monthly-index)",
            "- [Latest Papers](#latest-papers)",
            "- [Daily Archive](#daily-archive)",
            "- [Dataset](data/papers.json)",
            "- [Curation Policy](docs/curation.md)",
            "- [Literature Audit](allinone.md)",
            "- [Deployment Guide](docs/deployment.md)",
            "",
            "## 🌟 Highlighted Papers",
            "",
            "> Signals are independently verified. A paper is highlighted when it has popular "
            "code, strong citation traction, an industry affiliation, or a top-venue publication.",
            "",
            "| Paper | Published | Venue | Why it matters | Metrics |",
            "| --- | --- | --- | --- | --- |",
        ]
        highlighted = [paper for paper in papers if self._flags(paper) != "—"]
        highlighted.sort(
            key=lambda item: (
                item.venue_tier == "top",
                item.citation_count or -1,
                item.github_stars or -1,
                item.published,
            ),
            reverse=True,
        )
        for paper in highlighted[:30]:
            title = paper.title.replace("|", "\\|")
            lines.append(
                f"| [{title}]({paper.url}) | {paper.published.date().isoformat()} | "
                f"{paper.venue or 'arXiv'} | {self._flags(paper)} | {self._metrics(paper)} |"
            )
        if not highlighted:
            lines.append("| No highlighted papers yet | — | — | — | — |")
        lines.extend(
            [
                "",
                "## 🗓️ 2026 Monthly Index",
                "",
                "| Month | Papers | Self-Evolving | Memory | Continual Training |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for month in range(1, 9):
            month_papers = [
                paper
                for paper in papers
                if paper.published.year == 2026 and paper.published.month == month
            ]
            lines.append(
                f"| [{month:02d}](papers/2026/{month:02d}/README.md) | {len(month_papers)} | "
                f"{sum('agent-self-evolving' in p.topics for p in month_papers)} | "
                f"{sum('agent-memory' in p.topics for p in month_papers)} | "
                f"{sum('llm-continual-training' in p.topics for p in month_papers)} |"
            )
        lines.extend(
            [
                "",
                "## 📝 Latest Papers",
            "",
            "| Published | Track | Paper | Links |",
            "| --- | --- | --- | --- |",
            ]
        )
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
                "## 🔎 Scope and Verification",
                "",
                "- **Agent Self-Evolving:** self-evolving, self-improving, and evolving agents",
                "- **Agent Memory:** long-term, memory-augmented, and persistent agent memory",
                "- **LLM Continual Training:** continual, lifelong, and post-deployment "
                "LLM learning",
                "- **Very popular code:** at least 1,000 GitHub stars; **popular code:** at least "
                "100 stars",
                "- **Highly cited:** at least 10 citations for a 2026 paper; every count records "
                "its source and snapshot date",
                "- **Industry / top venue:** marked only when verified from the paper, publisher, "
                "or official project page",
                "- Missing metrics are shown as `n/a`, never guessed. Stars and citations are "
                "time-sensitive snapshots.",
                "",
                "## License",
                "",
                "Code is released under the MIT License. Paper metadata remains subject "
                "to its source terms.",
                "",
            ]
        )
        return "\n".join(lines)
