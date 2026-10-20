from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from .archive import ArchiveRepository, ArchiveResult
from .candidates import CandidateRepository
from .highlight import classify_highlights, is_eligible, promotion_signature
from .state import DigestStateStore
from .wecom import build_digest_messages


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
        historical_backfill_days: int = 730,
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
        self.historical_backfill_days = historical_backfill_days
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
        if self.historical_backfill_days < 1:
            raise ValueError("historical_backfill_days must be at least 1")
        state_store = DigestStateStore(self.archive.root)
        discovery_revision = str(getattr(self.source, "discovery_revision", ""))
        since = state_store.coverage_start(
            now,
            fallback_days=self.lookback_days,
            discovery_revision=discovery_revision,
            historical_backfill_days=self.historical_backfill_days,
        )
        fetched = await self.source.fetch(
            # Overlap indexed updates to catch delayed arXiv announcements.
            since=min(since, now - timedelta(days=self.lookback_days)),
            max_results_per_topic=self.max_results_per_topic,
        )
        candidate_repository = CandidateRepository(self.archive.root)
        # Recheck known papers too: an old preprint may gain acceptance evidence today.
        papers = candidate_repository.merge([*self.archive._load(), *fetched])
        if self.enricher is not None:
            papers = await self.enricher.enrich(papers)
        papers = [classify_highlights(paper) for paper in papers]
        papers.sort(key=lambda p: (p.published, p.updated, p.arxiv_id), reverse=True)
        candidate_repository.save([p for p in papers if is_eligible(p)])
        known = {p.arxiv_id: classify_highlights(p) for p in self.archive._load()}
        # Persist intent before writing the dataset so a crash during rendering
        # cannot turn an undelivered paper into an apparently completed one.
        queued = state_store.stage(
            now,
            tuple(
                p.arxiv_id
                for p in papers
                if is_eligible(p)
                and (
                    p.arxiv_id not in known
                    or promotion_signature(p) != promotion_signature(known[p.arxiv_id])
                )
            ),
        )
        result = self.archive.update(
            now.date(),
            [paper for paper in papers if is_eligible(paper)],
            carryover_ids=queued.pending_paper_ids,
            coverage_start=since,
            coverage_end=now,
        )
        pending_ids = tuple(paper.arxiv_id for paper in result.digest_papers)
        staged = state_store.stage(now, pending_ids)
        if self.git_sync is not None:
            await self.git_sync.sync(now.date())
        if self.notifier is not None and (result.digest_papers or self.notify_when_empty):
            messages = build_digest_messages(
                result.digest_papers,
                archive_url=result.daily_url,
                max_papers=self.max_push_papers,
                coverage_start=since,
                coverage_end=now,
            )
            for markdown in messages:
                await self.notifier.send(markdown)
        if (
            self.finalize_success
            and self.notifier is not None
            and self.git_sync is not None
            and getattr(self.git_sync, "auto_push", True)
        ):
            state_store.complete(now, discovery_revision=discovery_revision)
            try:
                await self.git_sync.sync(now.date())
            except BaseException:
                state_store.restore(staged)
                raise
        return result
