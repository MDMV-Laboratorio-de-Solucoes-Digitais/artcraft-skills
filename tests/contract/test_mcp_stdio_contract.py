"""006 RED: MCP stdio adapter/CreativeSkill contract tests (T005,T013)."""
import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.base_skill import SkillResult

FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"


def _cfg(scenario, timeout=5):
    return {"transport": "stdio", "command": sys.executable, "args": [str(FAKE), "--scenario", scenario], "timeout": timeout}


def _load_image_edit():
    try:
        from skills.creative.image_edit.skill import ImageEditSkill
        return ImageEditSkill
    except Exception:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../skills/creative/image-edit/skill.py"))
        spec = importlib.util.spec_from_file_location("image_edit_skill_006_contract", path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        return mod.ImageEditSkill


def _minimal_inputs(scenario):
    skill = _load_image_edit()()
    schema = skill.get_input_schema()
    inp = {"mode": "mcp", "mcp_config": _cfg(scenario)}
    props = schema.get("properties", {})
    if "prompt" in props or "prompt" in schema.get("required", []):
        inp["prompt"] = "edit image"
    if "image" in props or "image" in schema.get("required", []):
        inp["image"] = "input.png"
    return inp


def _assert_fr006_failure_minimum(r: SkillResult, expected_reason=None):
    assert isinstance(r, SkillResult)
    assert r.success is False
    assert isinstance(r.error, str) and r.error.strip()
    md = r.metadata or {}
    assert isinstance(md, dict)
    if md.get("mode") is not None:
        assert str(md.get("mode")) in ("mcp", "auto")
    if expected_reason is not None:
        assert str(md.get("reason", "")).lower() == expected_reason or expected_reason in str(md.get("reason", "")).lower()
    # no secret/PII heuristics (best-effort)
    blob = (r.error or "") + str(md)
    assert "sk-" not in blob.lower()
    assert "password" not in blob.lower()


def test_image_edit_mcp_success_normalized_skillresult():
    skill = _load_image_edit()()
    r = skill.execute(_minimal_inputs("tools_call_success"))
    assert isinstance(r, SkillResult)
    assert r.success is True, r.error
    assert isinstance(r.data, dict)
    md = r.metadata or {}
    assert md.get("interface") == "mcp" or md.get("mode") == "mcp" or str(md.get("interface", "")).lower() == "mcp"


def test_missing_capability_has_fr006_minimum_metadata():
    skill = _load_image_edit()()
    r = skill.execute(_minimal_inputs("missing_capability"))
    _assert_fr006_failure_minimum(r, expected_reason="mcp_missing_capability")


def test_tool_error_has_fr006_minimum_metadata():
    skill = _load_image_edit()()
    r = skill.execute(_minimal_inputs("tool_error"))
    _assert_fr006_failure_minimum(r, expected_reason="mcp_tool_error")


def test_invalid_json_has_structured_failure():
    skill = _load_image_edit()()
    r = skill.execute(_minimal_inputs("invalid_json"))
    _assert_fr006_failure_minimum(r)
    reason = str((r.metadata or {}).get("reason", "")).lower()
    assert reason in ("mcp_invalid_response", "invalid_json", "invalid_protocol", "") or "invalid" in reason or "protocol" in reason
