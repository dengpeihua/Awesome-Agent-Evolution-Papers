import importlib.util
import sys
import types
from pathlib import Path

import pytest


@pytest.fixture
def plugin_module(monkeypatch):
    class Star:
        def __init__(self, context, config=None):
            self.context = context

    class Filter:
        @staticmethod
        def command(_name):
            return lambda function: function

    def register(*_args, **_kwargs):
        return lambda cls: cls

    api = types.ModuleType("astrbot.api")
    api.logger = types.SimpleNamespace(info=lambda *_: None, error=lambda *_: None)
    event = types.ModuleType("astrbot.api.event")
    event.filter = Filter()
    event.AstrMessageEvent = object
    star = types.ModuleType("astrbot.api.star")
    star.Context = object
    star.Star = Star
    star.register = register
    monkeypatch.setitem(sys.modules, "astrbot", types.ModuleType("astrbot"))
    monkeypatch.setitem(sys.modules, "astrbot.api", api)
    monkeypatch.setitem(sys.modules, "astrbot.api.event", event)
    monkeypatch.setitem(sys.modules, "astrbot.api.star", star)

    main_path = Path(__file__).parents[1] / "main.py"
    spec = importlib.util.spec_from_file_location("digest_plugin_main", main_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
async def test_plugin_registers_daily_cron_and_shuts_down(plugin_module, tmp_path) -> None:
    plugin = plugin_module.AgentPaperDigestPlugin(
        context=object(),
        config={
            "archive_dir": str(tmp_path),
            "schedule_hour": 8,
            "schedule_minute": 15,
            "timezone": "Asia/Shanghai",
        },
    )

    await plugin.initialize()

    job = plugin.scheduler.get_job("agent-paper-digest-daily")
    assert job is not None
    assert "hour='8'" in str(job.trigger)
    assert "minute='15'" in str(job.trigger)

    await plugin.terminate()
    assert plugin.scheduler is None


@pytest.mark.asyncio
async def test_scheduled_failure_registers_retry(plugin_module, tmp_path, monkeypatch):
    plugin = plugin_module.AgentPaperDigestPlugin(
        context=object(),
        config={"archive_dir": str(tmp_path), "run_on_startup": False},
    )
    await plugin.initialize()

    async def fail():
        raise RuntimeError("arXiv temporarily unavailable")

    monkeypatch.setattr(plugin, "_run_once", fail)
    monkeypatch.setattr(plugin_module.logger, "exception", lambda *_: None, raising=False)
    await plugin._scheduled_run()
    assert plugin.scheduler.get_job("agent-paper-digest-retry") is not None
    await plugin.terminate()
