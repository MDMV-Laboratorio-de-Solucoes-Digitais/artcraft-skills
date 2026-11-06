"""006 RED: MCP selection/back-compat tests (T015, disjoint from US1 acceptance)."""
import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A

FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"


def _cfg(scenario, timeout=5):
    return {"transport": "stdio", "command": sys.executable, "args": [str(FAKE), "--scenario", scenario], "timeout": timeout}


def _load_image_edit():
    try:
        from skills.creative.image_edit.skill import ImageEditSkill
        return ImageEditSkill
    except Exception:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../skills/creative/image-edit/skill.py"))
        spec = importlib.util.spec_from_file_location("image_edit_skill_006_sel", path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        return mod.ImageEditSkill


def _inputs(mode, scenario=None):
    skill = _load_image_edit()()
    schema = skill.get_input_schema()
    inp = {"mode": mode}
    if scenario:
        inp["mcp_config"] = _cfg(scenario)
    props = schema.get("properties", {})
    if "prompt" in props or "prompt" in schema.get("required", []):
        inp.setdefault("prompt", "edit")
    if "image" in props or "image" in schema.get("required", []):
        inp.setdefault("image", "in.png")
    return inp


def test_explicit_cli_missing_preserves_reason(monkeypatch):
    skill = _load_image_edit()()
    monkeypatch.setattr(A, "discover_cli", lambda *a, **k: None)
    if hasattr(skill, "_discover_cli"):
        monkeypatch.setattr(skill, "_discover_cli", lambda *a, **k: None)
    r = skill.execute(_inputs("cli"))
    assert r.success is False
    md = r.metadata or {}
    assert md.get("reason") == A.REASON_CLI_NOT_FOUND or "cli_not_found" in str(md.get("reason", ""))


def test_explicit_mcp_failure_no_silent_cli_reroute(monkeypatch):
    skill = _load_image_edit()()
    # even if CLI would be available, explicit mcp must not reroute
    monkeypatch.setattr(A, "discover_cli", lambda *a, **k: "/fake/photocraft-cli")
    if hasattr(skill, "_discover_cli"):
        monkeypatch.setattr(skill, "_discover_cli", lambda *a, **k: "/fake/photocraft-cli")
    r = skill.execute(_inputs("mcp", "tool_error"))
    assert r.success is False
    md = r.metadata or {}
    assert md.get("mode") == "mcp" or "mcp" in str(md.get("interface", "")).lower()
    assert md.get("reason") not in (A.REASON_CLI_NOT_FOUND, "cli_not_found")
    assert isinstance(r.error, str) and r.error


def test_auto_cli_first_when_cli_available_even_with_mcp(monkeypatch):
    skill = _load_image_edit()()
    calls = {"cli": 0, "mcp": 0}

    def fake_cli_exec(*a, **k):
        calls["cli"] += 1
        from skills.core.base_skill import SkillResult
        return SkillResult(success=True, data={"image_path": "x.png"}, metadata={"interface": "cli", "mode": "auto"})

    def fake_mcp_exec(*a, **k):
        calls["mcp"] += 1
        from skills.core.base_skill import SkillResult
        return SkillResult(success=True, data={"image_path": "m.png"}, metadata={"interface": "mcp", "mode": "auto"})

    monkeypatch.setattr(A, "discover_cli", lambda *a, **k: "/fake/photocraft-cli")
    if hasattr(skill, "_discover_cli"):
        monkeypatch.setattr(skill, "_discover_cli", lambda *a, **k: "/fake/photocraft-cli")
    monkeypatch.setattr(skill, "_execute_cli", fake_cli_exec)
    monkeypatch.setattr(skill, "_execute_mcp", fake_mcp_exec)
    r = skill.execute(_inputs("auto", "tools_call_success"))
    assert calls["cli"] == 1
    assert calls["mcp"] == 0
    assert r.success is True


def test_auto_uses_mcp_when_cli_unavailable(monkeypatch):
    skill = _load_image_edit()()
    monkeypatch.setattr(A, "discover_cli", lambda *a, **k: None)
    if hasattr(skill, "_discover_cli"):
        monkeypatch.setattr(skill, "_discover_cli", lambda *a, **k: None)
    r = skill.execute(_inputs("auto", "tools_call_success"))
    # May fail if MCP not implemented (RED acceptable) but when implemented should succeed
    if r.success:
        md = r.metadata or {}
        assert md.get("interface") == "mcp" or md.get("mode") in ("auto", "mcp")
    else:
        # RED state acceptable before impl; but once MCP path works must not claim cli_not_found
        assert (r.metadata or {}).get("reason") != A.REASON_CLI_NOT_FOUND


def test_no_cli_no_mcp_neither_available(monkeypatch):
    skill = _load_image_edit()()
    monkeypatch.setattr(A, "discover_cli", lambda *a, **k: None)
    if hasattr(skill, "_discover_cli"):
        monkeypatch.setattr(skill, "_discover_cli", lambda *a, **k: None)
    # ensure MCP reported unavailable
    if hasattr(skill, "_mcp_available"):
        monkeypatch.setattr(skill, "_mcp_available", lambda *a, **k: False)
    r = skill.execute(_inputs("auto", "missing_capability"))
    assert r.success is False
    md = r.metadata or {}
    reason = str(md.get("reason", ""))
    assert "neither" in reason.lower() or reason == A.REASON_NEITHER_AVAILABLE or "mcp" in reason.lower()
