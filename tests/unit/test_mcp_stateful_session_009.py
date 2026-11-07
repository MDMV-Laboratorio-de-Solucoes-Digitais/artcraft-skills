"""009 RED→GREEN: additive MCP stateful session (007 Option B), mock-first.

Covers FR-001/FR-002/FR-003/FR-006/FR-009 (docs contract): retained subprocess,
correlated JSON-RPC ids across multiple calls, lifecycle/cleanup, timeout,
invalid response, tool error, missing capability. Preserves 006 stateless APIs.
"""
import json
import os
import signal
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A

FAKE = Path(__file__).resolve().parents[1] / "_helpers" / "fake_mcp_stdio_server.py"


def cfg(scenario, **kw):
    c = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(FAKE), "--scenario", scenario],
        "timeout": kw.pop("timeout", 5),
    }
    c.update(kw)
    return c


def _get_session_api():
    # 009 additive API (contract: mcp_stateful_session / MCPStatefulSession)
    fn = getattr(A, "mcp_stateful_session", None)
    cls = getattr(A, "MCPStatefulSession", None)
    if fn is None and cls is None:
        pytest.fail(
            "009 RED: additive stateful API missing (expected mcp_stateful_session and/or MCPStatefulSession)",
            pytrace=False,
        )
    return fn, cls


def _open_session(scenario, **kw):
    fn, cls = _get_session_api()
    config = cfg(scenario, **kw.pop("cfg_overrides", {}) if False else {})
    # support either factory or direct class
    if fn is not None:
        return fn(config, **kw)
    return cls(config, **kw)


def _is_error(res):
    return isinstance(res, dict) and (res.get("is_error") or res.get("success") is False or res.get("error") or res.get("reason"))


def _assert_fr006_failure(res, expected_reason=None):
    assert isinstance(res, dict)
    assert _is_error(res)
    assert isinstance(res.get("error") or res.get("metadata", {}).get("message") or "", str)
    if expected_reason:
        reason = str((res.get("metadata") or {}).get("reason") or res.get("reason") or "").lower()
        assert expected_reason in reason


# --- US1: additive contract / retained multi-call / correlated ids / cleanup ---


def test_stateful_session_two_calls_same_retained_process():
    fn, _ = _get_session_api()
    with _open_session("stateful_session_marker") as session:
        l1 = session.list_tools()
        c1 = session.call_tool("image.edit", {"image": "in.png", "prompt": "a"})
        c2 = session.call_tool("image.edit", {"image": "in.png", "prompt": "b"})
    assert not _is_error(l1)
    assert isinstance(c1, dict) and not _is_error(c1)
    assert isinstance(c2, dict) and not _is_error(c2)
    m1 = ((c1.get("data") or {}).get("session_marker")) or ((c1.get("result") or {}).get("data") or {}).get("session_marker")
    m2 = ((c2.get("data") or {}).get("session_marker")) or ((c2.get("result") or {}).get("data") or {}).get("session_marker")
    assert m1 and m2 and m1 == m2, f"expected same retained process marker, got {m1!r} vs {m2!r}"
    id1 = ((c1.get("data") or {}).get("call_id")) or ((c1.get("result") or {}).get("data") or {}).get("call_id")
    id2 = ((c2.get("data") or {}).get("call_id")) or ((c2.get("result") or {}).get("data") or {}).get("call_id")
    assert id1 is not None and id2 is not None and id1 != id2, (id1, id2)


def test_stateful_session_explicit_close_cleans_process():
    session = _open_session("tools_call_success")
    session.__enter__()
    session.list_tools()
    session.close()
    # double close safe
    session.close()
    proc = getattr(session, "_process", None) or getattr(session, "process", None)
    if proc is not None:
        assert proc.poll() is not None


def test_stateless_006_apis_unchanged():
    # preservation: existing stateless functions still behave identically on 006 scenarios
    res = A.mcp_tools_list(cfg("tools_list_success"))
    assert isinstance(res, (dict, list))
    assert "image" in json.dumps(res).lower() or "edit" in json.dumps(res).lower()
    res2 = A.mcp_tools_call(cfg("tools_call_success"), "image.edit", {"image": "in.png", "prompt": "edit"})
    assert isinstance(res2, dict) and not res2.get("is_error")


# --- errors / safety ---


def test_stateful_session_tool_error_structured_fr006():
    with _open_session("tool_error") as session:
        session.list_tools()
        res = session.call_tool("image.edit", {"image": "in.png"})
    _assert_fr006_failure(res, "mcp_tool_error")
    md = res.get("metadata") or {}
    assert md.get("tool") == "image.edit" or "image.edit" in str(res)


def test_stateful_session_missing_capability_visible():
    with _open_session("missing_capability") as session:
        res = session.list_tools()
    # discovery result may be list/dict of tools (006 shape) or structured error; missing image.edit
    text = json.dumps(res, default=str).lower()
    assert "other.tool" in text or "image.edit" not in text or (isinstance(res, dict) and _is_error(res))


def test_stateful_session_invalid_json_structured_cleanup():
    session = _open_session("invalid_json")
    with session:
        res = session.list_tools()
    _assert_fr006_failure(res)
    proc = getattr(session, "_process", None) or getattr(session, "process", None)
    if proc is not None:
        deadline = time.time() + 3
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.05)
        assert proc.poll() is not None, "process leaked after invalid_json"


def test_stateful_session_call_timeout_bounded_cleanup():
    session = _open_session("timeout_hang_call", timeout=1)
    t0 = time.time()
    with session:
        session.list_tools()
        res = session.call_tool("image.edit", {"image": "in.png"})
    elapsed = time.time() - t0
    assert elapsed < 15, f"timeout not bounded: {elapsed}s"
    _assert_fr006_failure(res)
    reason = str((res.get("metadata") or {}).get("reason") or res.get("reason") or "").lower()
    assert "timeout" in reason or "mcp_call_timeout" in reason
    proc = getattr(session, "_process", None) or getattr(session, "process", None)
    if proc is not None:
        deadline = time.time() + 3
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.05)
        assert proc.poll() is not None, "process leaked after timeout"


def test_stateful_session_mid_session_exit_structured():
    session = _open_session("mid_session_exit")
    with session:
        session.list_tools()
        res = session.call_tool("image.edit", {"image": "in.png"})
    _assert_fr006_failure(res)
    proc = getattr(session, "_process", None) or getattr(session, "process", None)
    if proc is not None:
        deadline = time.time() + 3
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.05)
        assert proc.poll() is not None


def test_stateful_session_misconfigured_command_structured():
    bad = {"transport": "stdio", "command": "", "args": [], "timeout": 2}
    fn, cls = _get_session_api()
    # either factory raises-not-across-boundary? contract prefers structured; but __enter__/open may fail structured
    try:
        if fn is not None:
            ctx = fn(bad)
        else:
            ctx = cls(bad)
        with ctx as session:
            res = session.list_tools()
        _assert_fr006_failure(res, "mcp_misconfigured")
    except Exception as e:
        # acceptable only if clearly misconfiguration; but better structured - mark as design note via assertion
        pytest.fail(f"009: misconfiguration should be structured, got exception {e!r}")
