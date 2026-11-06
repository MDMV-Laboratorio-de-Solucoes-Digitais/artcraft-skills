"""006 RED: MCP stdio transport/client tests (T003,T012)."""
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A

FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"


def cfg(scenario, **kw):
    c = {"transport": "stdio", "command": sys.executable, "args": [str(FAKE), "--scenario", scenario], "timeout": kw.pop("timeout", 5)}
    c.update(kw)
    return c


def _call_tools_list(scenario, **kw):
    if not hasattr(A, "mcp_tools_list"):
        pytest.fail("006 RED: artcraft_app_client.mcp_tools_list missing", pytrace=False)
    return A.mcp_tools_list(cfg(scenario, **kw))


def _call_tools_call(scenario, tool_name="image.edit", arguments=None, **kw):
    if not hasattr(A, "mcp_tools_call"):
        pytest.fail("006 RED: artcraft_app_client.mcp_tools_call missing", pytrace=False)
    return A.mcp_tools_call(cfg(scenario, **kw), tool_name, arguments or {"image": "in.png", "prompt": "edit"})


def test_tools_list_success_returns_tools():
    res = _call_tools_list("tools_list_success")
    assert isinstance(res, (dict, list))
    text = json.dumps(res)
    assert "image" in text.lower() or "edit" in text.lower()


def test_tools_call_success_structured():
    res = _call_tools_call("tools_call_success")
    assert isinstance(res, dict)
    assert not res.get("is_error")
    assert res.get("success") is not False


def test_missing_capability_visible_in_discovery():
    res = _call_tools_list("missing_capability")
    text = json.dumps(res)
    assert "other.tool" in text or "image" not in text.lower() or res == [] or (isinstance(res, dict) and res.get("tools") == [])


def test_tool_error_structured():
    res = _call_tools_call("tool_error")
    assert isinstance(res, dict)
    assert res.get("is_error") or res.get("success") is False or "error" in res


def test_invalid_json_structured_failure():
    res = _call_tools_list("invalid_json")
    if isinstance(res, dict):
        assert res.get("is_error") or res.get("success") is False or res.get("error") or res.get("reason")


def test_stderr_diagnostics_clean_stdout_succeeds():
    res = _call_tools_list("stderr_diagnostics_clean_stdout")
    text = json.dumps(res)
    assert "tools" in text.lower() or "image" in text.lower() or isinstance(res, list)


def test_timeout_hang_bounded():
    res = _call_tools_call("timeout_hang", timeout=1)
    if isinstance(res, dict):
        assert res.get("is_error") or res.get("success") is False or "timeout" in str(res).lower() or res.get("reason")
