from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True, slots=True)
class DigestSettings:
    """Validated configuration shared by the AstrBot plugin and one-shot CLI."""

    enabled: bool
    archive_dir: Path
    timezone: ZoneInfo
    schedule_hour: int
    schedule_minute: int
    lookback_days: int
    max_results_per_topic: int
    max_push_papers: int
    wecom_webhook_url: str
    repository_url: str
    git_remote: str
    git_branch: str
    git_auto_push: bool
    git_author_name: str
    git_author_email: str
    run_on_startup: bool
    notify_when_empty: bool

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, Any],
        *,
        default_archive_dir: Path,
    ) -> DigestSettings:
        """Build settings from AstrBot or JSON configuration.

        Args:
            values: Mapping with user-provided overrides.
            default_archive_dir: Repository root used when ``archive_dir`` is empty.

        Returns:
            Fully validated immutable settings.

        Raises:
            ValueError: If a schedule, limit, or timezone is invalid.
        """
        timezone_name = str(values.get("timezone", "Asia/Shanghai")).strip()
        try:
            timezone = ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"Unknown timezone: {timezone_name}") from error

        schedule_hour = int(values.get("schedule_hour", 9))
        schedule_minute = int(values.get("schedule_minute", 0))
        lookback_days = int(values.get("lookback_days", 2))
        max_results_per_topic = int(values.get("max_results_per_topic", 20))
        max_push_papers = int(values.get("max_push_papers", 8))
        if not 0 <= schedule_hour <= 23:
            raise ValueError("schedule_hour must be between 0 and 23")
        if not 0 <= schedule_minute <= 59:
            raise ValueError("schedule_minute must be between 0 and 59")
        if lookback_days < 1:
            raise ValueError("lookback_days must be at least 1")
        if max_results_per_topic < 1:
            raise ValueError("max_results_per_topic must be at least 1")
        if max_push_papers < 1:
            raise ValueError("max_push_papers must be at least 1")

        archive_value = str(values.get("archive_dir", "")).strip()
        archive_dir = Path(archive_value).expanduser() if archive_value else default_archive_dir
        return cls(
            enabled=bool(values.get("enabled", True)),
            archive_dir=archive_dir.resolve(),
            timezone=timezone,
            schedule_hour=schedule_hour,
            schedule_minute=schedule_minute,
            lookback_days=lookback_days,
            max_results_per_topic=max_results_per_topic,
            max_push_papers=max_push_papers,
            wecom_webhook_url=str(values.get("wecom_webhook_url", "")).strip(),
            repository_url=str(values.get("repository_url", "")).strip().rstrip("/"),
            git_remote=str(values.get("git_remote", "origin")).strip() or "origin",
            git_branch=str(values.get("git_branch", "main")).strip() or "main",
            git_auto_push=bool(values.get("git_auto_push", True)),
            git_author_name=(
                str(values.get("git_author_name", "Agent Paper Digest Bot")).strip()
                or "Agent Paper Digest Bot"
            ),
            git_author_email=(
                str(
                    values.get(
                        "git_author_email",
                        "agent-paper-digest@users.noreply.github.com",
                    )
                ).strip()
                or "agent-paper-digest@users.noreply.github.com"
            ),
            run_on_startup=bool(values.get("run_on_startup", False)),
            notify_when_empty=bool(values.get("notify_when_empty", True)),
        )
