from __future__ import annotations

from datetime import datetime
from typing import Any

from .archive import ArchiveRepository, ArchiveResult
from .candidates import CandidateRepository
from .highlight import classify_highlights, highlight_priority, is_eligible
from .state import DigestStateStore
from .wecom import build_digest_markdown


class DailyDigestPipeline:
    """Orchestrate paper retrieval, archival, publishing, and notification."""

    def __init__(
        self,
        *,
        source: Any,
        archive: ArchiveRepository,
        notifier: Any | None,
        git_sync: Any | None,
        enricher: Any | None = None,
        lookback_days: int = 2,
        max_results_per_topic: int = 20,
        max_push_papers: int = 8,
        notify_when_empty: bool = True,
        finalize_success: bool = True,
    ) -> None:
        self.source = source
        self.archive = archive
        self.notifier = notifier
        self.git_sync = git_sync
        self.enricher = enricher
        self.lookback_days = lookback_days
        self.max_results_per_topic = max_results_per_topic
        self.max_push_papers = max_push_papers
        self.notify_when_empty = notify_when_empty
        self.finalize_success = finalize_success

    async def run(self, now: datetime) -> ArchiveResult:
        """Execute a complete idempotent daily run.

        Args:
            now: Timezone-aware execution instant; its calendar date labels the archive.

        Returns:
            Archive result including newly discovered papers.

        Raises:
            ValueError: If ``now`` is naive or lookback configuration is invalid.
        """
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if self.lookback_days < 1:
            raise ValueError("lookback_days must be at least 1")
        state_store = DigestStateStore(self.archive.root)
        state = state_store.load()
        since = state_store.coverage_start(now, fallback_days=self.lookback_days)
        fetched = await self.source.fetch(
            since=since,
            max_results_per_topic=self.max_results_per_topic,
        )
        candidate_repository = CandidateRepository(self.archive.root)
        # Keep topical but not-yet-qualified papers locally so later citation or
        # publication evidence can promote them without exposing them publicly.
        papers = candidate_repository.merge([*self.archive._load(), *fetched])
        if self.enricher is not None:
            papers = await self.enricher.enrich(papers)
        papers = [classify_highlights(paper) for paper in papers]
        papers.sort(key=highlight_priority, reverse=True)
        candidate_repository.save(papers)
        result = self.archive.update(
            now.date(),
            [paper for paper in papers if is_eligible(paper)],
            carryover_ids=state.pending_paper_ids,
            coverage_start=since,
            coverage_end=now,
        )
        pending_ids = tuple(paper.arxiv_id for paper in result.digest_papers)
        state_store.stage(now, pending_ids)
        if self.git_sync is not None:
            await self.git_sync.sync(now.date())
        if self.notifier is not None and (result.digest_papers or self.notify_when_empty):
            markdown = build_digest_markdown(
                result.digest_papers,
                archive_url=result.daily_url,
                max_papers=self.max_push_papers,
                coverage_start=since,
                coverage_end=now,
            )
            await self.notifier.send(markdown)
        if self.finalize_success:
            state_store.complete(now)
            if self.git_sync is not None:
                await self.git_sync.sync(now.date())
        return result
