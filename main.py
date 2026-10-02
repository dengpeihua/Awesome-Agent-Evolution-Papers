from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register

if __package__:
    from .agent_paper_digest.archive import ArchiveRepository
    from .agent_paper_digest.arxiv import ArxivSource
    from .agent_paper_digest.git_sync import GitSync
    from .agent_paper_digest.pipeline import DailyDigestPipeline
    from .agent_paper_digest.scholar import SemanticScholarEnricher
    from .agent_paper_digest.settings import DigestSettings
    from .agent_paper_digest.wecom import WeComNotifier
else:
    from agent_paper_digest.archive import ArchiveRepository
    from agent_paper_digest.arxiv import ArxivSource
    from agent_paper_digest.git_sync import GitSync
    from agent_paper_digest.pipeline import DailyDigestPipeline
    from agent_paper_digest.scholar import SemanticScholarEnricher
    from agent_paper_digest.settings import DigestSettings
    from agent_paper_digest.wecom import WeComNotifier


@register(
    "agent_paper_digest",
    "Agent Paper Digest",
    "Daily Agent evolution, memory, LLM continual training, and reinforcement learning papers",
    "0.5.0",
)
class AgentPaperDigestPlugin(Star):
    """AstrBot lifecycle adapter for the daily research pipeline."""

    def __init__(self, context: Context, config: Any | None = None) -> None:
        super().__init__(context, config)
        plugin_root = Path(__file__).resolve().parent
        self.settings = DigestSettings.from_mapping(
            config or {},
            default_archive_dir=plugin_root,
        )
        self.scheduler: AsyncIOScheduler | None = None
        self._startup_task: asyncio.Task[None] | None = None
        self._run_lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Register the configured daily cron job when the plugin is enabled."""
        if not self.settings.enabled:
            logger.info("Agent paper digest plugin is disabled.")
            return
        self.scheduler = AsyncIOScheduler(timezone=self.settings.timezone)
        self.scheduler.add_job(
            self._scheduled_run,
            CronTrigger(
                hour=self.settings.schedule_hour,
                minute=self.settings.schedule_minute,
                timezone=self.settings.timezone,
            ),
            id="agent-paper-digest-daily",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=3600,
        )
        self.scheduler.start()
        logger.info(
            "Agent paper digest scheduled for %02d:%02d (%s).",
            self.settings.schedule_hour,
            self.settings.schedule_minute,
            self.settings.timezone.key,
        )
        if self.settings.run_on_startup:
            self._startup_task = asyncio.create_task(self._scheduled_run())

    def _build_pipeline(self) -> DailyDigestPipeline:
        notifier = (
            WeComNotifier(self.settings.wecom_webhook_url)
            if self.settings.wecom_webhook_url
            else None
        )
        git_sync = None
        if (self.settings.archive_dir / ".git").exists():
            git_sync = GitSync(
                self.settings.archive_dir,
                remote=self.settings.git_remote,
                branch=self.settings.git_branch,
                auto_push=self.settings.git_auto_push,
                author_name=self.settings.git_author_name,
                author_email=self.settings.git_author_email,
            )
        return DailyDigestPipeline(
            source=ArxivSource(),
            archive=ArchiveRepository(
                self.settings.archive_dir,
                repository_url=self.settings.repository_url,
            ),
            notifier=notifier,
            git_sync=git_sync,
            enricher=(
                SemanticScholarEnricher(api_key=self.settings.semantic_scholar_api_key)
                if self.settings.semantic_scholar_enrichment
                else None
            ),
            lookback_days=self.settings.lookback_days,
            historical_backfill_days=self.settings.historical_backfill_days,
            max_results_per_topic=self.settings.max_results_per_topic,
            max_push_papers=self.settings.max_push_papers,
            notify_when_empty=self.settings.notify_when_empty,
        )

    async def _run_once(self):
        async with self._run_lock:
            return await self._build_pipeline().run(datetime.now(self.settings.timezone))

    async def _scheduled_run(self) -> None:
        try:
            result = await self._run_once()
            logger.info(
                "Agent paper digest finished: %d new, %d total.",
                len(result.new_papers),
                len(result.all_papers),
            )
        except Exception:
            logger.exception("Agent paper digest scheduled run failed.")
            if self.scheduler is not None:
                self.scheduler.add_job(
                    self._scheduled_run,
                    "date",
                    run_date=datetime.now(self.settings.timezone) + timedelta(minutes=15),
                    id="agent-paper-digest-retry",
                    replace_existing=True,
                    misfire_grace_time=3600,
                )

    @filter.command("paper_digest")
    async def paper_digest(self, event: AstrMessageEvent):
        """Run paper discovery, archive, push, and Git sync immediately."""
        try:
            result = await self._run_once()
            yield event.plain_result(
                f"论文日报完成：新增 {len(result.new_papers)} 篇，"
                f"累计 {len(result.all_papers)} 篇。\n归档：{result.daily_url}"
            )
        except Exception as error:
            logger.exception("Manual agent paper digest run failed.")
            yield event.plain_result(f"论文日报运行失败：{error}")

    @filter.command("paper_digest_status")
    async def paper_digest_status(self, event: AstrMessageEvent):
        """Show schedule and integration readiness without exposing secrets."""
        webhook_status = "已配置" if self.settings.wecom_webhook_url else "未配置"
        remote_status = "开启" if self.settings.git_auto_push else "关闭"
        yield event.plain_result(
            f"论文日报：{'启用' if self.settings.enabled else '停用'}\n"
            f"计划：{self.settings.schedule_hour:02d}:{self.settings.schedule_minute:02d} "
            f"({self.settings.timezone.key})\n"
            f"企业微信 Webhook：{webhook_status}\n"
            f"Git 自动推送：{remote_status}"
        )

    async def terminate(self) -> None:
        """Cancel startup work and release the scheduler during plugin reload."""
        if self._startup_task and not self._startup_task.done():
            self._startup_task.cancel()
            await asyncio.gather(self._startup_task, return_exceptions=True)
        self._startup_task = None
        if self.scheduler is not None:
            self.scheduler.shutdown(wait=False)
            self.scheduler = None
