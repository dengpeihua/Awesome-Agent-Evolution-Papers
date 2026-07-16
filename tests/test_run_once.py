import json

from scripts.run_once import load_config


def test_load_config_accepts_utf8_bom(tmp_path) -> None:
    config_path = tmp_path / "astrbot_config.json"
    config_path.write_text(
        json.dumps({"timezone": "Asia/Shanghai", "schedule_hour": 9}),
        encoding="utf-8-sig",
    )

    assert load_config(config_path) == {
        "timezone": "Asia/Shanghai",
        "schedule_hour": 9,
    }


def test_load_config_returns_empty_mapping_for_missing_file(tmp_path) -> None:
    assert load_config(tmp_path / "missing.json") == {}
