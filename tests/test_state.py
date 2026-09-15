import json
from datetime import UTC, datetime

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
