from pathlib import Path

import pytest

from agent_paper_digest.settings import DigestSettings


def test_settings_resolve_archive_and_validate_schedule(tmp_path) -> None:
    settings = DigestSettings.from_mapping(
        {
            "archive_dir": str(tmp_path),
            "timezone": "Asia/Shanghai",
            "schedule_hour": 8,
            "schedule_minute": 30,
            "lookback_days": 3,
            "historical_backfill_days": 730,
            "wecom_webhook_url": "",
        },
        default_archive_dir=Path("unused"),
    )

    assert settings.archive_dir == tmp_path.resolve()
    assert settings.schedule_hour == 8
    assert settings.schedule_minute == 30
    assert settings.lookback_days == 3
    assert settings.historical_backfill_days == 730
    assert settings.timezone.key == "Asia/Shanghai"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schedule_hour", 24),
        ("schedule_minute", 60),
        ("lookback_days", 0),
        ("historical_backfill_days", 0),
    ],
)
def test_settings_reject_invalid_numeric_values(field, value, tmp_path) -> None:
    with pytest.raises(ValueError):
        DigestSettings.from_mapping(
            {field: value},
            default_archive_dir=tmp_path,
        )


def test_settings_reject_unknown_timezone(tmp_path) -> None:
    with pytest.raises(ValueError, match="timezone"):
        DigestSettings.from_mapping(
            {"timezone": "Mars/Olympus"},
            default_archive_dir=tmp_path,
        )
