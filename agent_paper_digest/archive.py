from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, replace
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .highlight import (
    HIGH_CITATION_COUNT,
    classify_highlights,
    has_industry_qualification,
    is_eligible,
    promotion_signature,
    qualification_reasons,
)
from .models import Paper
from .topics import (
    CONTINUAL_TRAINING_TOPIC,
    LONG_HORIZON_TOPIC,
    MIN_PUBLICATION_DATE,
    REINFORCEMENT_LEARNING_TOPIC,
    SELF_EVOLUTION_TOPIC,
    TOPIC_SHORT,
    TOPIC_TITLES,
)

POPULAR_CODE_STARS = 100
VERY_POPULAR_CODE_STARS = 1_000
DAILY_PAGE_SIZE = 50


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
            if paper.venue_tier and not paper.acceptance_first_seen:
                # This is an observation date, never an inferred acceptance date.
                paper = replace(
                    paper,
                    acceptance_first_seen=(current.acceptance_first_seen if current else "")
                    or discovery_date.isoformat(),
                )
            if current:
                merged = current.merge(paper)
                merged = classify_highlights(merged)
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
        if coverage_start and coverage_end:
            windows_path = data_dir / "coverage_windows.json"
            windows = json.loads(windows_path.read_text("utf-8")) if windows_path.exists() else {}
            previous = windows.get(day_key, {})
            windows[day_key] = {
                "start": min(
                    previous.get("start", coverage_start.isoformat()), coverage_start.isoformat()
                ),
                "end": coverage_end.isoformat(),
            }
            windows_path.write_text(json.dumps(windows, indent=2) + "\n", encoding="utf-8")
            coverage_start = datetime.fromisoformat(windows[day_key]["start"])
        daily_path = (
            self.root
            / "papers"
            / str(discovery_date.year)
            / f"{discovery_date.month:02d}"
            / f"{discovery_date.isoformat()}.md"
        )
        self._write_daily_archives(discoveries, all_papers)
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
            digest_papers=tuple(paper for paper in all_papers if paper.arxiv_id in digest_ids),
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

    def _write_daily_archives(self, discoveries: dict[str, list[str]], papers: list[Paper]) -> None:
        indexed = {paper.arxiv_id: paper for paper in papers}
        windows_path = self.root / "data" / "coverage_windows.json"
        windows = json.loads(windows_path.read_text("utf-8")) if windows_path.exists() else {}
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
            ordered = sorted(
                [indexed[identifier] for identifier in identifiers if identifier in indexed],
                key=lambda p: (p.published, p.updated, p.arxiv_id),
                reverse=True,
            )
            batches = [
                ordered[i : i + DAILY_PAGE_SIZE] for i in range(0, len(ordered), DAILY_PAGE_SIZE)
            ] or [[]]
            page_dir = path.parent / day
            expected_pages: set[Path] = set()
            for index, batch in enumerate(batches):
                target = path if index == 0 else page_dir / f"page-{index + 1:03d}.md"
                expected_pages.add(target)
                target.parent.mkdir(parents=True, exist_ok=True)
                rendered = self._render_daily(
                    discovery_date,
                    batch,
                    coverage_start=(
                        datetime.fromisoformat(windows[day]["start"]) if day in windows else None
                    ),
                    coverage_end=(
                        datetime.fromisoformat(windows[day]["end"]) if day in windows else None
                    ),
                )
                if index:
                    rendered = rendered.replace("(../../../README.md)", "(../../../../README.md)")
                if len(batches) > 1:
                    links = []
                    for number in range(len(batches)):
                        href = (
                            (f"{day}.md" if index == 0 else f"../{day}.md")
                            if number == 0
                            else (f"{day}/" if index == 0 else "") + f"page-{number + 1:03d}.md"
                        )
                        links.append(f"[{number + 1}]({href})")
                    rendered = (
                        f"> **{len(ordered)} papers** · Page {index + 1}/{len(batches)} · "
                        "Newest first across all pages\n\n" + " · ".join(links) + "\n\n" + rendered
                    )
                target.write_text(rendered, encoding="utf-8")
            # Remove only generated numbered pages made obsolete by a rebuild.
            for obsolete in page_dir.glob("page-*.md"):
                if obsolete not in expected_pages:
                    obsolete.unlink()

    def _render_daily(
        self,
        discovery_date: date,
        papers: list[Paper],
        *,
        coverage_start: datetime | None = None,
        coverage_end: datetime | None = None,
    ) -> str:
        ordered = sorted(
            papers,
            key=lambda item: (item.published, item.updated, item.arxiv_id),
            reverse=True,
        )
        lines = [
            f"# Daily Papers · {discovery_date.isoformat()}",
            "",
            f"> Prepared **{len(papers)}** new, promoted, or retried paper(s) "
            "across four research tracks plus explicitly requested papers. "
            "Lists are newest publication first.",
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
        lines.extend(
            [
                "## All Updates · Newest First",
                "",
                "| Published | Track | Paper | Signals |",
                "| --- | --- | --- | --- |",
            ]
        )
        for paper in ordered:
            title = paper.title.replace("|", "\\|")
            tracks = ", ".join(TOPIC_SHORT[t] for t in paper.topics)
            fresh = (
                "🆕 New industry paper today<br>"
                if paper.published.astimezone(
                    coverage_end.tzinfo if coverage_end else ZoneInfo("Asia/Shanghai")
                ).date()
                == discovery_date
                and has_industry_qualification(paper)
                else ""
            )
            lines.append(
                f"| {paper.published.date()} | {tracks} | [{title}]({paper.url}) | "
                f"{fresh}{self._flags(paper)} |"
            )
        lines.append("")
        highlighted = [paper for paper in ordered if qualification_reasons(paper)]
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
                lines.append(f"| [{title}]({paper.url}) | {self._flags(paper)} | {evidence} |")
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
            flags.append("🏅 Selected top venue: " + (paper.venue or "verified"))
        if paper.acceptance_first_seen and paper.venue_tier:
            flags.append(
                "📣 Acceptance first observed: "
                + paper.acceptance_first_seen
                + " (actual acceptance date unverified)"
            )
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
        for old_index in (self.root / "papers").glob("*/*/README.md"):
            year_name = old_index.parent.parent.name
            if year_name.isdigit() and (int(year_name), int(old_index.parent.name)) < (
                MIN_PUBLICATION_DATE.year,
                MIN_PUBLICATION_DATE.month,
            ):
                old_index.unlink()
        grouped: dict[tuple[int, int], list[Paper]] = defaultdict(list)
        for paper in papers:
            grouped[(paper.published.year, paper.published.month)].append(paper)
        years = sorted(
            {paper.published.year for paper in papers}
            | {datetime.now(ZoneInfo("Asia/Shanghai")).date().year}
        )
        for year in years:
            months = range(1, 13)
            if year == datetime.now(ZoneInfo("Asia/Shanghai")).date().year:
                months = range(1, datetime.now(ZoneInfo("Asia/Shanghai")).date().month + 1)
            for month in months:
                if (year, month) < (MIN_PUBLICATION_DATE.year, MIN_PUBLICATION_DATE.month):
                    continue
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
            f"Agent/LLM Self-Improvement {topic_counts[SELF_EVOLUTION_TOPIC]} · "
            f"Continual Training {topic_counts[CONTINUAL_TRAINING_TOPIC]} · "
            f"Reinforcement Learning {topic_counts[REINFORCEMENT_LEARNING_TOPIC]} · "
            f"Long-Horizon {topic_counts[LONG_HORIZON_TOPIC]}",
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
        chronological = sorted(
            papers,
            key=lambda item: (item.published, item.updated, item.arxiv_id),
            reverse=True,
        )
        daily_paths = sorted(
            (path for path in (self.root / "papers").glob("*/*/*.md") if path.name != "README.md"),
            reverse=True,
        )
        topic_counts = {
            topic: sum(topic in paper.topics for paper in papers) for topic in TOPIC_TITLES
        }
        lines = [
            "# Awesome Agent Evolution Papers",
            "",
            '<div align="center">',
            "",
            "A daily collection of papers on **Agent/LLM self-evolution, self-improving "
            "systems, and recursive self-improvement**, **LLM "
            "continual training**, **Reinforcement Learning**, and **Long-Horizon Task Agents**,",
            "powered by AstrBot.",
            "",
            "The bot resumes from its last successful delivery after downtime, prioritizes",
            "verified industry-affiliated work (especially first authors), and marks explicit",
            "top-conference publications without promoting under-review claims.",
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
            f"| Agent/LLM self-evolution & self-improvement | "
            f"{topic_counts[SELF_EVOLUTION_TOPIC]} |",
            f"| LLM continual training | {topic_counts[CONTINUAL_TRAINING_TOPIC]} |",
            f"| Reinforcement Learning | {topic_counts[REINFORCEMENT_LEARNING_TOPIC]} |",
            f"| Long-Horizon Task Agents | {topic_counts[LONG_HORIZON_TOPIC]} |",
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
            "> Priority labels identify selected venues, industry affiliations, and citations. "
            "All topical papers remain eligible, including new preprints. Newest first.",
            "",
            "| Paper | Published | Venue | Why it matters | Metrics |",
            "| --- | --- | --- | --- | --- |",
        ]
        highlighted = [paper for paper in chronological if qualification_reasons(paper)]
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
                "| Month | Papers | Agent/LLM Self-Improvement | Continual Training | RL |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        month_keys = sorted(
            {(paper.published.year, paper.published.month) for paper in papers}
            | {
                (
                    datetime.now(ZoneInfo("Asia/Shanghai")).date().year,
                    datetime.now(ZoneInfo("Asia/Shanghai")).date().month,
                )
            },
            reverse=True,
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
                f"{sum(SELF_EVOLUTION_TOPIC in p.topics for p in month_papers)} | "
                f"{sum(CONTINUAL_TRAINING_TOPIC in p.topics for p in month_papers)} | "
                f"{sum(REINFORCEMENT_LEARNING_TOPIC in p.topics for p in month_papers)} |"
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
        for paper in chronological[:30]:
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
                "- **Agent & LLM Self-Evolution:** self-evolving, self-improving, recursive "
                "self-improvement, self-refinement, self-feedback reinforcement, and "
                "co-evolving agents or language models",
                "- **LLM Continual Training:** continual pre/post-training, lifelong and "
                "online adaptation, retention, and catastrophic-forgetting mitigation",
                "- **Long-Horizon Task Agents:** language agents executing extended, "
                "multi-step tasks",
                "- **Excluded:** Agent Memory papers (including cross-topic papers) "
                "and journal articles",
                "- **Date boundary:** first publication on or after 2025-05-01; "
                "a recent revision does not make an older paper eligible",
                "- **Reinforcement Learning:** substantive RL training or research directly "
                "related to language models / language agents, including RLHF, RLAIF, RLVR "
                "and GRPO; generic control/robotics RL and incidental mentions are excluded",
                "- **Public inclusion:** any of the four topics or an explicit user request; "
                "industry, venue, and citation "
                "signals highlight papers without excluding new preprints",
                "- **Acceptance dates:** first observed means newly detected by this bot; "
                "it does not establish the actual date of acceptance",
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
