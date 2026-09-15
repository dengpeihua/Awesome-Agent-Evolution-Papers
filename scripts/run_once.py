from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from agent_paper_digest.archive import ArchiveRepository  # noqa: E402
from agent_paper_digest.arxiv import ArxivSource  # noqa: E402
from agent_paper_digest.git_sync import GitSync  # noqa: E402
from agent_paper_digest.pipeline import DailyDigestPipeline  # noqa: E402
from agent_paper_digest.scholar import SemanticScholarEnricher  # noqa: E402
from agent_paper_digest.settings import DigestSettings  # noqa: E402
from agent_paper_digest.wecom import WeComNotifier  # noqa: E402


def load_config(path: Path) -> dict[str, object]:
    """Load JSON configuration written by AstrBot or a text editor.

    AstrBot's Windows configuration files may include a UTF-8 byte-order mark,
    so ``utf-8-sig`` is used to accept both BOM and non-BOM JSON files.
    """
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


async def main() -> int:
    """Run the complete pipeline once from a local JSON configuration."""
    parser = argparse.ArgumentParser(description="Run the agent paper digest once")
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "config.json")
    parser.add_argument("--no-notify", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args()
    values = load_config(args.config)
    settings = DigestSettings.from_mapping(values, default_archive_dir=PROJECT_ROOT)
    notifier = None
    if settings.wecom_webhook_url and not args.no_notify:
        notifier = WeComNotifier(settings.wecom_webhook_url)
    git_sync = None
    if (settings.archive_dir / ".git").exists():
        git_sync = GitSync(
            settings.archive_dir,
            remote=settings.git_remote,
            branch=settings.git_branch,
            auto_push=settings.git_auto_push and not args.no_push,
            author_name=settings.git_author_name,
            author_email=settings.git_author_email,
        )
    result = await DailyDigestPipeline(
        source=ArxivSource(),
        archive=ArchiveRepository(settings.archive_dir, settings.repository_url),
        notifier=notifier,
        git_sync=git_sync,
        enricher=(
            SemanticScholarEnricher(api_key=settings.semantic_scholar_api_key)
            if settings.semantic_scholar_enrichment
            else None
        ),
        lookback_days=settings.lookback_days,
        max_results_per_topic=settings.max_results_per_topic,
        max_push_papers=settings.max_push_papers,
        notify_when_empty=settings.notify_when_empty,
        finalize_success=not (
            (args.no_notify and bool(settings.wecom_webhook_url))
            or (args.no_push and settings.git_auto_push)
        ),
    ).run(datetime.now(settings.timezone))
    print(
        f"Digest completed: {len(result.new_papers)} new / "
        f"{len(result.all_papers)} total; {result.daily_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
