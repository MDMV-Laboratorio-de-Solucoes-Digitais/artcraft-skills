"""Deterministic fake MCP stdio server for 006 tests.

Speaks newline-delimited JSON-RPC-like MCP messages on stdout only.
All diagnostics go to stderr. No network, no credentials, no external binaries.

Scenarios (006 T002/T010/T011, spec/contracts):
- tools_list_success / tools_call_success: discovery + one tools/call success
- missing_capability: tools/list has no matching image/edit tool
- tool_error: tools/call returns isError/tool error payload
- invalid_json: first protocol response after a request is invalid JSON
- invalid_protocol: valid JSON but wrong/insufficient shape
- timeout_hang: no response to tools/call (bounded by test timeout)
- launch_failure: exit nonzero immediately with stderr diagnostic
- stderr_diagnostics_clean_stdout: stderr diagnostic + valid stdout protocol

Run: python tests/_helpers/fake_mcp_stdio_server.py --scenario <name>
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


def fake_server_command(scenario: str, tool_name: Optional[str] = None, extra_args: Optional[List[str]] = None) -> List[str]:
    path = str(Path(__file__).resolve())
    cmd = [sys.executable, path, "--scenario", scenario]
    if tool_name:
        cmd.extend(["--tool-name", tool_name])
    if extra_args:
        cmd.extend(list(extra_args))
    return cmd


def fake_mcp_config(scenario: str, **overrides: Any) -> Dict[str, Any]:
    cfg: Dict[str, Any] = {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(Path(__file__).resolve()), "--scenario", scenario],
        "timeout": 5,
    }
    cfg.update(overrides)
    return cfg


def _write(obj: Any) -> None:
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _diag(msg: str) -> None:
    sys.stderr.write(msg.rstrip() + "\n")
    sys.stderr.flush()


def _tool_list(tool_name: str) -> List[Dict[str, Any]]:
    return [
        {"name": tool_name, "description": "Fake image edit tool for 006 tests", "inputSchema": {"type": "object"}},
        {"name": "image.edit", "description": "Alias edit tool", "inputSchema": {"type": "object"}},
    ]


def _success_call_result(req_id: Any, tool_name: str) -> Dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "content": [{"type": "text", "text": "ok"}],
            "isError": False,
            "data": {
                "image_path": "/tmp/fake-mcp-edit.png",
                "image_url": "file:///tmp/fake-mcp-edit.png",
                "asset_id": "fake-asset-006",
                "format": "png",
                "width": 64,
                "height": 64,
                "metadata": {"source": "fake_mcp_stdio_server", "tool": tool_name},
            },
        },
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic fake MCP stdio server for 006 tests")
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--tool-name", default="image.edit")
    args = parser.parse_args(argv)

    scenario = args.scenario
    tool_name = args.tool_name

    if scenario == "launch_failure":
        _diag("fake_mcp_stdio_server: simulated launch/misconfiguration failure")
        return 2

    def on_term(signum: int, frame: Any) -> None:
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, on_term)
    try:
        signal.signal(signal.SIGINT, on_term)
    except Exception:
        pass

    if scenario == "stderr_diagnostics_clean_stdout":
        _diag("fake_mcp_stdio_server: diagnostic on stderr; stdout remains protocol-only")

    invalid_sent = False
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue
        if not isinstance(req, dict):
            continue
        req_id = req.get("id")
        method = req.get("method")

        if method == "initialize":
            _write({"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2025-11-25", "capabilities": {"tools": {}}, "serverInfo": {"name": "fake-006", "version": "0.0.0"}}})
            continue
        if method in ("notifications/initialized", "initialized"):
            continue
        if method == "tools/list":
            if scenario == "invalid_json" and not invalid_sent:
                sys.stdout.write("{not-json\n")
                sys.stdout.flush()
                invalid_sent = True
                continue
            if scenario == "invalid_protocol" and not invalid_sent:
                _write({"oops": True, "id": req_id})
                invalid_sent = True
                continue
            if scenario == "missing_capability":
                _write({"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "other.tool", "description": "no image/edit", "inputSchema": {"type": "object"}}]}})
            else:
                _write({"jsonrpc": "2.0", "id": req_id, "result": {"tools": _tool_list(tool_name)}})
            continue
        if method == "tools/call":
            if scenario == "timeout_hang":
                time.sleep(60)
                return 0
            if scenario == "invalid_json" and not invalid_sent:
                sys.stdout.write("{not-json\n")
                sys.stdout.flush()
                invalid_sent = True
                continue
            if scenario == "invalid_protocol" and not invalid_sent:
                _write({"unexpected": "shape", "id": req_id})
                invalid_sent = True
                continue
            if scenario == "tool_error":
                _write({"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "tool failed"}], "isError": True, "error": {"message": "fake tool error for 006"}}})
                continue
            # success/default
            called = (req.get("params") or {}).get("name") or tool_name
            _write(_success_call_result(req_id, str(called)))
            continue
        # unknown method: return JSON-RPC method-not-found-ish result to stay protocol-safe
        if req_id is not None:
            _write({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
