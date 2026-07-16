import importlib.util
import sys
import types
from pathlib import Path


def test_plugin_imports_core_as_an_astrbot_package(monkeypatch) -> None:
    class Star:
        def __init__(self, context, config=None):
            self.context = context

    class Filter:
        @staticmethod
        def command(_name):
            return lambda function: function

    api = types.ModuleType("astrbot.api")
    api.logger = types.SimpleNamespace(info=lambda *_: None, error=lambda *_: None)
    event = types.ModuleType("astrbot.api.event")
    event.filter = Filter()
    event.AstrMessageEvent = object
    star = types.ModuleType("astrbot.api.star")
    star.Context = object
    star.Star = Star
    star.register = lambda *_args, **_kwargs: lambda cls: cls
    monkeypatch.setitem(sys.modules, "astrbot", types.ModuleType("astrbot"))
    monkeypatch.setitem(sys.modules, "astrbot.api", api)
    monkeypatch.setitem(sys.modules, "astrbot.api.event", event)
    monkeypatch.setitem(sys.modules, "astrbot.api.star", star)

    project_root = Path(__file__).parents[1]
    monkeypatch.setattr(
        sys,
        "path",
        [path for path in sys.path if Path(path or ".").resolve() != project_root.resolve()],
    )
    for name in list(sys.modules):
        if name == "agent_paper_digest" or name.startswith("agent_paper_digest."):
            monkeypatch.delitem(sys.modules, name, raising=False)

    package_name = "data.plugins.astrbot_plugin_agent_paper_digest"
    package = types.ModuleType(package_name)
    package.__path__ = [str(project_root)]
    monkeypatch.setitem(sys.modules, "data", types.ModuleType("data"))
    monkeypatch.setitem(sys.modules, "data.plugins", types.ModuleType("data.plugins"))
    monkeypatch.setitem(sys.modules, package_name, package)
    spec = importlib.util.spec_from_file_location(f"{package_name}.main", project_root / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None

    spec.loader.exec_module(module)

    assert module.AgentPaperDigestPlugin.__name__ == "AgentPaperDigestPlugin"

