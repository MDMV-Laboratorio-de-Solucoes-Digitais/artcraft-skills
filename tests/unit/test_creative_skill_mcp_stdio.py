"""006 RED: CreativeSkill MCP US1 acceptance tests (T004,T014)."""
import importlib.util
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"


def _cfg(scenario, timeout=5):
    return {"transport": "stdio", "command": sys.executable, "args": [str(FAKE), "--scenario", scenario], "timeout": timeout}


def _load_image_edit():
    try:
        from skills.creative.image_edit.skill import ImageEditSkill
        return ImageEditSkill
    except Exception:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../skills/creative/image-edit/skill.py"))
        spec = importlib.util.spec_from_file_location("image_edit_skill_006", path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        return mod.ImageEditSkill


def _base_inputs(scenario):
    schema = _load_image_edit().get_input_schema(_load_image_edit()) if False else _load_image_edit().get_input_schema.__func__(_load_image_edit()) if hasattr(_load_image_edit().get_input_schema, "__func__") else None
    inp = {"mode": "mcp", "mcp_config": _cfg(scenario), "image": "input.png", "prompt": "edit image"}
    return inp


def _assert_fr006_minimum_failure(r, reason_substr=None):
    assert r.success is False
    assert isinstance(r.error, str) and r.error
    md = r.metadata or {}
    assert md.get("mode") in ("mcp", "auto", None) or "mcp" in str(md.get("mode"))
    assert isinstance(md, dict)
    if reason_substr:
        assert reason_substr in str(md.get("reason", "")).lower()
    if md.get("interface") is not None:
        assert "mcp" in str(md.get("interface")).lower() or md.get("interface") == "mcp"


def test_us1_mcp_discovery_and_invocation_success():
    skill = _load_image_edit()()
    r = skill.execute(_base_inputs("tools_call_success"))
    assert r.success is True, getattr(r, "error", None)
    assert isinstance(r.data, dict)
    md = r.metadata or {}
    assert md.get("interface") == "mcp" or md.get("mode") in ("mcp", "auto")


def test_us1_missing_capability_structured_failure():
    skill = _load_image_edit()()
    r = skill.execute(_base_inputs("missing_capability"))
    _assert_fr006_minimum_failure(r, "mcp_missing_capability")


def test_us1_tool_error_structured_failure():
    skill = _load_image_edit()()
    r = skill.execute(_base_inputs("tool_error"))
    _assert_fr006_minimum_failure(r, "mcp_tool_error")
