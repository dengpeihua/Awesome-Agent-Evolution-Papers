from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .highlight import (
    HIGH_CITATION_COUNT,
    classify_highlights,
    has_industry_qualification,
    highlight_priority,
    is_eligible,
    promotion_signature,
)
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
@dataclass(frozen=True, slots=True)
class ArchiveResult:
    """Artifacts produced by one discovery run."""

    discovery_date: date
    daily_path: Path
    daily_url: str
    new_papers: tuple[Paper, ...]
    promoted_papers: tuple[Paper, ...]
    digest_papers: tuple[Paper, ...]
    all_papers: tuple[Paper, ...]
    coverage_start: datetime | None = None
    coverage_end: datetime | None = None


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
        """Replace the public dataset with eligible papers and rebuild every index."""
        merged: dict[str, Paper] = {}
        for paper in papers:
            paper = classify_highlights(paper)
            if not is_eligible(paper):
                continue
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
        discoveries = self._prune_discoveries(self._load_discoveries(), all_papers)
        self._write_discoveries(discoveries)
        self._write_daily_archives(discoveries, all_papers)
        self._write_monthly_archives(all_papers)
        (self.root / "README.md").write_text(
            self._render_readme(all_papers),
            encoding="utf-8",
        )
        return tuple(all_papers)

    def update(
        self,
        discovery_date: date,
        papers: list[Paper],
        *,
        carryover_ids: tuple[str, ...] = (),
        coverage_start: datetime | None = None,
        coverage_end: datetime | None = None,
    ) -> ArchiveResult:
        """Persist a run and rebuild all derived Markdown files.

        Args:
            discovery_date: Local calendar date assigned to this run.
            papers: Recent papers returned by the source.

        Returns:
            Paths and paper sets needed for notification and Git synchronization.
        """
        self.root.mkdir(parents=True, exist_ok=True)
        existing = {
            paper.arxiv_id: paper
            for raw in self._load()
            if is_eligible(paper := classify_highlights(raw))
        }
        discoveries = self._prune_discoveries(self._load_discoveries(), list(existing.values()))
        known_ids = set(existing)
        new_papers: list[Paper] = []
        promoted_papers: list[Paper] = []
        for paper in papers:
            paper = classify_highlights(paper)
            if not is_eligible(paper):
                continue
            current = existing.get(paper.arxiv_id)
            if current:
                merged = current.merge(paper)
                existing[paper.arxiv_id] = merged
                if promotion_signature(merged) != promotion_signature(current):
                    promoted_papers.append(merged)
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
        digest_ids = tuple(
            dict.fromkeys(
                (
                    *carryover_ids,
                    *(paper.arxiv_id for paper in promoted_papers),
                    *(paper.arxiv_id for paper in new_papers),
                )
            )
        )
        for arxiv_id in digest_ids:
            if arxiv_id in existing and arxiv_id not in day_ids:
                day_ids.append(arxiv_id)
        day_ids.sort()
        self._write_discoveries(discoveries)
        daily_papers = [existing[arxiv_id] for arxiv_id in day_ids if arxiv_id in existing]

        daily_path = (
            self.root
            / "papers"
            / str(discovery_date.year)
            / f"{discovery_date.month:02d}"
            / f"{discovery_date.isoformat()}.md"
        )
        self._write_daily_archives(discoveries, all_papers)
        daily_path.parent.mkdir(parents=True, exist_ok=True)
        daily_path.write_text(
            self._render_daily(
                discovery_date,
                daily_papers,
                coverage_start=coverage_start,
                coverage_end=coverage_end,
            ),
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
            promoted_papers=tuple(promoted_papers),
            digest_papers=tuple(
                existing[paper_id] for paper_id in digest_ids if paper_id in existing
            ),
            all_papers=tuple(all_papers),
            coverage_start=coverage_start,
            coverage_end=coverage_end,
        )

    @staticmethod
    def _prune_discoveries(
        discoveries: dict[str, list[str]], papers: list[Paper]
    ) -> dict[str, list[str]]:
        eligible_ids = {paper.arxiv_id for paper in papers}
        return {
            day: sorted({identifier for identifier in identifiers if identifier in eligible_ids})
            for day, identifiers in sorted(discoveries.items())
        }

    def _write_discoveries(self, discoveries: dict[str, list[str]]) -> None:
        data_dir = self.root / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "discoveries.json").write_text(
            json.dumps(discoveries, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_daily_archives(
        self, discoveries: dict[str, list[str]], papers: list[Paper]
    ) -> None:
        indexed = {paper.arxiv_id: paper for paper in papers}
        for day, identifiers in discoveries.items():
            try:
                discovery_date = date.fromisoformat(day)
            except ValueError:
                continue
            path = (
                self.root
                / "papers"
                / str(discovery_date.year)
                / f"{discovery_date.month:02d}"
                / f"{day}.md"
            )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                self._render_daily(
                    discovery_date,
                    [indexed[identifier] for identifier in identifiers if identifier in indexed],
                ),
                encoding="utf-8",
            )

    def _render_daily(
        self,
        discovery_date: date,
        papers: list[Paper],
        *,
        coverage_start: datetime | None = None,
        coverage_end: datetime | None = None,
    ) -> str:
        ordered = sorted(papers, key=highlight_priority, reverse=True)
        lines = [
            f"# Daily Papers · {discovery_date.isoformat()}",
            "",
            f"> Prepared **{len(papers)}** new, promoted, or retried paper(s) "
            "across three research tracks.",
        ]
        if coverage_start and coverage_end:
            lines.append(
                f"> Catch-up window: **{coverage_start.isoformat()}** → "
                f"**{coverage_end.isoformat()}**."
            )
        lines.extend(["", "[← Back to index](../../../README.md)", ""])
        if not papers:
            lines.extend(["No new papers were discovered in this run.", ""])
            return "\n".join(lines)
        highlighted = [paper for paper in ordered if is_eligible(paper)]
        if highlighted:
            lines.extend(
                [
                    "## 🚨 Priority Watch",
                    "",
                    "| Paper | Signals | Venue / affiliation evidence |",
                    "| --- | --- | --- |",
                ]
            )
            for paper in highlighted:
                evidence = self._evidence(paper)
                title = paper.title.replace("|", "\\|")
                lines.append(
                    f"| [{title}]({paper.url}) | {self._flags(paper)} | {evidence} |"
                )
            lines.append("")
        for topic, title in TOPIC_TITLES.items():
            topic_papers = [paper for paper in ordered if topic in paper.topics]
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
                        f"- **Priority:** {self._flags(paper)}",
                        f"- **Venue:** {paper.venue or 'arXiv'}",
                        f"- **Affiliations:** {', '.join(paper.affiliations) or 'n/a'}",
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
    def _evidence(paper: Paper) -> str:
        values: list[str] = []
        if paper.acceptance_evidence:
            values.append(paper.acceptance_evidence.replace("|", "\\|"))
        if paper.first_author_affiliations:
            values.append(
                "First author: "
                + ", ".join(paper.first_author_affiliations).replace("|", "\\|")
                + (f" ({paper.affiliation_source})" if paper.affiliation_source else "")
            )
        elif paper.affiliations:
            values.append(", ".join(paper.affiliations).replace("|", "\\|"))
        if not values and (paper.github_stars is not None or paper.citation_count is not None):
            values.append("Verified metrics snapshot; see Metrics")
        return "<br>".join(values) if values else "See linked paper record"

    @staticmethod
    def _flags(paper: Paper) -> str:
        flags: list[str] = []
        if paper.github_stars is not None and paper.github_stars >= VERY_POPULAR_CODE_STARS:
            flags.append("🔥 Very popular code")
        elif paper.github_stars is not None and paper.github_stars >= POPULAR_CODE_STARS:
            flags.append("⭐ Popular code")
        if paper.citation_count is not None and paper.citation_count >= HIGH_CITATION_COUNT:
            flags.append("📈 Highly cited")
        if paper.industry_first_author_affiliations:
            label = (
                "🚨 First-author industry profile"
                if paper.affiliation_source == "Semantic Scholar author profiles"
                else "🚨 First-author industry affiliation"
            )
            flags.append(f"{label}: " + ", ".join(paper.industry_first_author_affiliations))
        elif has_industry_qualification(paper):
            flags.append("🏢 Industry: " + ", ".join(paper.industry_affiliations))
        if paper.venue_tier == "ccf-a":
            flags.append("🏆 CCF-A: " + (paper.venue or "verified"))
        elif paper.venue_tier == "selected-extra":
            flags.append("🏅 ECCV / EMNLP: " + (paper.venue or "verified"))
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
            "The bot resumes from its last successful delivery after downtime, prioritizes",
            "verified industry-affiliated work (especially first authors), and marks explicit",
            "top-conference or top-journal publications without promoting under-review claims.",
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
            "- [Monthly Index](#monthly-index)",
            "- [Latest Papers](#latest-papers)",
            "- [Daily Archive](#daily-archive)",
            "- [Dataset](data/papers.json)",
            "- [Curation Policy](docs/curation.md)",
            "- [Literature Audit](allinone.md)",
            "- [Deployment Guide](docs/deployment.md)",
            "",
            "## 🌟 Highlighted Papers",
            "",
            "> Every listed paper is topic-relevant and has at least one verified qualifier: "
            "CCF-A (AI), ECCV/EMNLP, big-tech affiliation, or high citation count.",
            "",
            "| Paper | Published | Venue | Why it matters | Metrics |",
            "| --- | --- | --- | --- | --- |",
        ]
        highlighted = [paper for paper in papers if is_eligible(paper)]
        highlighted.sort(
            key=lambda item: (
                *highlight_priority(item),
                item.citation_count or -1,
                item.github_stars or -1,
            ),
            reverse=True,
        )
        for paper in highlighted:
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
                "## 🗓️ Monthly Index",
                "",
                "| Month | Papers | Self-Evolving | Memory | Continual Training |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        month_keys = sorted(
            {(paper.published.year, paper.published.month) for paper in papers}
            | {(date.today().year, date.today().month)}
        )
        for year, month in month_keys:
            month_papers = [
                paper
                for paper in papers
                if paper.published.year == year and paper.published.month == month
            ]
            lines.append(
                f"| [{year}-{month:02d}](papers/{year}/{month:02d}/README.md) | "
                f"{len(month_papers)} | "
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
                "- **Public inclusion:** topic relevance plus CCF-A (AI), ECCV/EMNLP, verified "
                "big-tech affiliation, or at least 10 citations",
                "- **Conference papers:** only Full/Regular main-track papers qualify by venue; "
                "Findings, workshop, demo, and short papers do not",
                "- **Code stars:** displayed as context but never qualify a paper by themselves",
                "- **Industry / venue:** marked only when supported by publication metadata, the "
                "paper, a publisher, or an official project page",
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
