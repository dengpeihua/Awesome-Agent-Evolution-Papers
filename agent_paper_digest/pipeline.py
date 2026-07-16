from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from .archive import ArchiveRepository, ArchiveResult
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
        lookback_days: int = 2,
        max_results_per_topic: int = 20,
        max_push_papers: int = 8,
        notify_when_empty: bool = True,
    ) -> None:
        self.source = source
        self.archive = archive
        self.notifier = notifier
        self.git_sync = git_sync
        self.lookback_days = lookback_days
        self.max_results_per_topic = max_results_per_topic
        self.max_push_papers = max_push_papers
        self.notify_when_empty = notify_when_empty

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
        papers = await self.source.fetch(
            since=now - timedelta(days=self.lookback_days),
            max_results_per_topic=self.max_results_per_topic,
        )
        result = self.archive.update(now.date(), papers)
        if self.git_sync is not None:
            await self.git_sync.sync(now.date())
        if self.notifier is not None and (result.new_papers or self.notify_when_empty):
            markdown = build_digest_markdown(
                result.new_papers,
                archive_url=result.daily_url,
                max_papers=self.max_push_papers,
            )
            await self.notifier.send(markdown)
        return result

