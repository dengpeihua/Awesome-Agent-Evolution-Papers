import json
from datetime import UTC, datetime, timedelta

from agent_paper_digest.state import DigestStateStore


def test_state_migrates_resume_cursor_from_latest_discovery_day(tmp_path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "discoveries.json").write_text(
        json.dumps({"2026-07-16": [], "2026-07-28": ["2607.1"]}),
        encoding="utf-8",
    )

    since = DigestStateStore(tmp_path).coverage_start(
        datetime(2026, 8, 12, 9, tzinfo=UTC),
        fallback_days=2,
    )

    assert since == datetime(2026, 7, 28, tzinfo=UTC)


def test_state_rescans_history_when_discovery_revision_changes(tmp_path) -> None:
    store = DigestStateStore(tmp_path)
    previous = datetime(2026, 8, 12, 9, tzinfo=UTC)
    current = datetime(2026, 9, 15, 9, tzinfo=UTC)
    store.complete(previous, discovery_revision="query-v1")

    since = store.coverage_start(
        current,
        fallback_days=2,
        discovery_revision="query-v2",
        historical_backfill_days=730,
    )

    assert since == current - timedelta(days=730)


def test_state_uses_success_cursor_when_discovery_revision_matches(tmp_path) -> None:
    store = DigestStateStore(tmp_path)
    previous = datetime(2026, 8, 12, 9, tzinfo=UTC)
    current = datetime(2026, 9, 15, 9, tzinfo=UTC)
    store.complete(previous, discovery_revision="query-v2")

    since = store.coverage_start(
        current,
        fallback_days=2,
        discovery_revision="query-v2",
        historical_backfill_days=730,
    )

    assert since == previous
