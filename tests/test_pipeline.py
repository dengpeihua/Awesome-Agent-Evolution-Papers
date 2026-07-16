from datetime import UTC, datetime

import pytest

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.pipeline import DailyDigestPipeline
from tests.test_archive import make_paper


class FakeSource:
    async def fetch(self, *, since: datetime, max_results_per_topic: int):
        assert since.tzinfo is not None
        assert max_results_per_topic == 20
        return [make_paper("2607.00001", topics=("agent-memory",))]


class FakeNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    async def send(self, markdown: str) -> None:
        self.messages.append(markdown)


class FakeGitSync:
    def __init__(self) -> None:
        self.calls = 0

    async def sync(self, discovery_date) -> bool:
        self.calls += 1
        return True


@pytest.mark.asyncio
async def test_pipeline_fetches_archives_notifies_and_syncs(tmp_path) -> None:
    notifier = FakeNotifier()
    git_sync = FakeGitSync()
    pipeline = DailyDigestPipeline(
        source=FakeSource(),
        archive=ArchiveRepository(tmp_path, repository_url="https://github.com/example/repo"),
        notifier=notifier,
        git_sync=git_sync,
        lookback_days=2,
        max_results_per_topic=20,
        max_push_papers=8,
        notify_when_empty=True,
    )

    result = await pipeline.run(datetime(2026, 7, 16, 9, tzinfo=UTC))

    assert len(result.new_papers) == 1
    assert len(notifier.messages) == 1
    assert "Paper 2607.00001" in notifier.messages[0]
    assert git_sync.calls == 1


@pytest.mark.asyncio
async def test_pipeline_can_skip_empty_notification(tmp_path) -> None:
    class EmptySource:
        async def fetch(self, *, since: datetime, max_results_per_topic: int):
            return []

    notifier = FakeNotifier()
    pipeline = DailyDigestPipeline(
        source=EmptySource(),
        archive=ArchiveRepository(tmp_path),
        notifier=notifier,
        git_sync=None,
        notify_when_empty=False,
    )

    await pipeline.run(datetime(2026, 7, 16, 9, tzinfo=UTC))

    assert notifier.messages == []

