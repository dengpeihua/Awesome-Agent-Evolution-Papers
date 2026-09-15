import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from agent_paper_digest.archive import ArchiveRepository
from agent_paper_digest.pipeline import DailyDigestPipeline
from agent_paper_digest.state import DigestStateStore
from tests.test_archive import make_paper


class FakeSource:
    async def fetch(self, *, since: datetime, max_results_per_topic: int):
        assert since.tzinfo is not None
        assert max_results_per_topic == 20
        return [
            replace(
                make_paper("2607.00001", topics=("agent-memory",)),
                first_author_affiliations=("Google DeepMind",),
                affiliation_source="arXiv author metadata",
            )
        ]


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
    assert git_sync.calls == 2


@pytest.mark.asyncio
async def test_pipeline_retries_pending_digest_after_notification_failure(tmp_path) -> None:
    class FailingNotifier:
        async def send(self, _markdown: str) -> None:
            raise RuntimeError("temporary delivery error")

    pipeline = DailyDigestPipeline(
        source=FakeSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=FailingNotifier(),
        git_sync=None,
        notify_when_empty=False,
    )
    now = datetime(2026, 7, 16, 9, tzinfo=UTC)

    with pytest.raises(RuntimeError, match="delivery error"):
        await pipeline.run(now)

    state = json.loads((tmp_path / "data" / "digest_state.json").read_text(encoding="utf-8"))
    assert state["last_successful_run_at"] is None
    assert state["pending_paper_ids"] == ["2607.00001"]

    notifier = FakeNotifier()
    retry = DailyDigestPipeline(
        source=FakeSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=notifier,
        git_sync=None,
        notify_when_empty=False,
    )
    await retry.run(datetime(2026, 7, 17, 9, tzinfo=UTC))

    assert "Paper 2607.00001" in notifier.messages[0]
    completed = json.loads(
        (tmp_path / "data" / "digest_state.json").read_text(encoding="utf-8")
    )
    assert completed["last_successful_run_at"] == "2026-07-17T09:00:00+00:00"
    assert completed["pending_paper_ids"] == []


@pytest.mark.asyncio
async def test_pipeline_dry_run_keeps_pending_and_does_not_advance_cursor(tmp_path) -> None:
    pipeline = DailyDigestPipeline(
        source=FakeSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=None,
        git_sync=None,
        notify_when_empty=False,
        finalize_success=False,
    )

    await pipeline.run(datetime(2026, 7, 16, 9, tzinfo=UTC))

    state = json.loads((tmp_path / "data" / "digest_state.json").read_text(encoding="utf-8"))
    assert state["last_successful_run_at"] is None
    assert state["pending_paper_ids"] == ["2607.00001"]


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


@pytest.mark.asyncio
async def test_pipeline_propagates_query_revision_to_historical_rescan(tmp_path) -> None:
    class VersionedSource:
        discovery_revision = "query-v2"

        def __init__(self) -> None:
            self.since: datetime | None = None

        async def fetch(self, *, since: datetime, max_results_per_topic: int):
            self.since = since
            return []

    source = VersionedSource()
    now = datetime(2026, 9, 15, 9, tzinfo=UTC)
    pipeline = DailyDigestPipeline(
        source=source,
        archive=ArchiveRepository(tmp_path),
        notifier=None,
        git_sync=None,
        historical_backfill_days=730,
        notify_when_empty=False,
    )

    await pipeline.run(now)

    assert source.since == now - timedelta(days=730)
    state = json.loads((tmp_path / "data" / "digest_state.json").read_text("utf-8"))
    assert state["discovery_revision"] == "query-v2"


@pytest.mark.asyncio
async def test_failed_delivery_does_not_accept_new_discovery_revision(tmp_path) -> None:
    class VersionedSource:
        discovery_revision = "query-v2"

        async def fetch(self, *, since: datetime, max_results_per_topic: int):
            return [make_paper("2609.10001", topics=("agent-memory",))]

    class FailingNotifier:
        async def send(self, _markdown: str) -> None:
            raise RuntimeError("temporary delivery error")

    previous = datetime(2026, 9, 12, 9, tzinfo=UTC)
    DigestStateStore(tmp_path).complete(previous, discovery_revision="query-v1")
    pipeline = DailyDigestPipeline(
        source=VersionedSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=FailingNotifier(),
        git_sync=None,
        historical_backfill_days=730,
        notify_when_empty=True,
    )

    with pytest.raises(RuntimeError, match="delivery error"):
        await pipeline.run(datetime(2026, 9, 15, 9, tzinfo=UTC))

    state = DigestStateStore(tmp_path).load()
    assert state.last_successful_run_at == previous
    assert state.discovery_revision == "query-v1"


@pytest.mark.asyncio
async def test_pipeline_keeps_unqualified_candidate_for_later_promotion(tmp_path) -> None:
    class CandidateSource:
        async def fetch(self, *, since: datetime, max_results_per_topic: int):
            return [make_paper("2607.00009", topics=("agent-memory",))]

    class CitationEnricher:
        async def enrich(self, papers):
            return [replace(paper, citation_count=10) for paper in papers]

    first = DailyDigestPipeline(
        source=CandidateSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=None,
        git_sync=None,
        notify_when_empty=False,
    )
    initial = await first.run(datetime(2026, 7, 16, 9, tzinfo=UTC))
    assert initial.all_papers == ()
    assert (tmp_path / ".paper_digest" / "candidates.json").exists()

    promoted = DailyDigestPipeline(
        source=CandidateSource(),
        archive=ArchiveRepository(tmp_path),
        notifier=None,
        git_sync=None,
        enricher=CitationEnricher(),
        notify_when_empty=False,
    )
    result = await promoted.run(datetime(2026, 7, 17, 9, tzinfo=UTC))
    assert [paper.arxiv_id for paper in result.new_papers] == ["2607.00009"]
