"""009/B: version-tolerant MCP tool argument normalization (mock-first, additive).

Preserves 006/009 contracts: normalization is opt-in/pure helper; default
mcp_tools_call/call_tool behavior unchanged unless caller opts in.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A


def test_normalize_tool_arguments_doc_export_drops_overwrite_for_compat():
    if not hasattr(A, "normalize_mcp_tool_arguments"):
        pytest.fail("009/B: additive normalize_mcp_tool_arguments missing", pytrace=False)
    out = A.normalize_mcp_tool_arguments("doc_export", {"path": "/tmp/x.png", "format": "png", "overwrite": False})
    assert out["path"] == "/tmp/x.png"
    assert out["format"] == "png"
    assert "overwrite" not in out


def test_normalize_tool_arguments_preserves_unknown_and_non_target_tools():
    if not hasattr(A, "normalize_mcp_tool_arguments"):
        pytest.fail("009/B: additive normalize_mcp_tool_arguments missing", pytrace=False)
    inp = {"path": "/tmp/x.png", "overwrite": False, "foo": 1}
    out = A.normalize_mcp_tool_arguments("doc_save", inp)
    assert out == inp
    assert out is not inp  # no mutation


def test_stateful_call_tool_default_unchanged_contract():
    # existing deterministic scenario still behaves as before (tool_error on fake server path not involved)
    from pathlib import Path
    FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"
    cfg = {"transport": "stdio", "command": sys.executable, "args": [str(FAKE), "--scenario", "tools_call_success"], "timeout": 5}
    with A.mcp_stateful_session(cfg, timeout=5) as s:
        s.list_tools()
        r = s.call_tool("image.edit", {"image": "in.png", "prompt": "x"})
    assert isinstance(r, dict) and not r.get("is_error") and not r.get("isError")
