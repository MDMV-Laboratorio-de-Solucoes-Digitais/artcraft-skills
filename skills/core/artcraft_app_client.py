"""Shared CLI/MCP adapter for ArtCraft apps.

Extracted from skills.creative.image-generate to enable reuse across
creative skills (image-edit, background-remove, image-upscale, mesh-generate, etc.)
following Constitution v2.1.0 (CLI/MCP only, no API).

006: minimal functional MCP stdio tools integration (`tools/list`, `tools/call`).
Stdout is protocol-only for newline-delimited JSON-RPC; stderr is diagnostics.
"""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import threading
import time
from collections.abc import Mapping, Sequence
from typing import Any

__version__ = "0.4.0"

REASON_CLI_NOT_FOUND = "cli_not_found"
REASON_MCP_UNAVAILABLE = "mcp_unavailable"
REASON_MCP_MISCONFIGURED = "mcp_misconfigured"
REASON_MCP_STARTUP_TIMEOUT = "mcp_startup_timeout"
REASON_MCP_CALL_TIMEOUT = "mcp_call_timeout"
REASON_MCP_INVALID_RESPONSE = "mcp_invalid_response"
REASON_MCP_MISSING_CAPABILITY = "mcp_missing_capability"
REASON_MCP_TOOL_ERROR = "mcp_tool_error"
REASON_NEITHER_AVAILABLE = "neither_available"
REASON_IS_ERROR = "is_error"

_MCP_TIMEOUT_REASONS = {REASON_MCP_STARTUP_TIMEOUT, REASON_MCP_CALL_TIMEOUT, "timeout"}


def discover_cli(cli_path: str | None = None) -> str | None:
    """Discover ArtCraft app CLI binary.

    Checks provided path, then ``shutil.which('photocraft-cli')``, then common
    locations. Returns ``None`` when unavailable (never raises).
    """
    if cli_path:
        if os.path.exists(cli_path):
            return cli_path
        return None
    path = shutil.which("photocraft-cli")
    if path:
        return path
    common = [
        "/usr/bin/photocraft-cli",
        os.path.expanduser("~/.local/bin/photocraft-cli"),
        "/Applications/PhotoCraft.app/Contents/MacOS/photocraft-cli",
    ]
    for c in common:
        if os.path.exists(c):
            return c
    return None


def discover_generation_command(
    commands: Mapping[str, Any] | Sequence[Any] | None = None,
    keywords: Sequence[str] | None = None,
    override: str | None = None,
) -> str | None:
    """Discover generation command/tool from a commands collection."""
    if override:
        return override
    if not keywords:
        keywords = ["generate", "gen", "image.generate"]
    cmd_list: list[Any] = []
    if isinstance(commands, Mapping):
        cmd_list = list(commands.get("commands") or commands.get("items") or commands.get("tools") or [])
    elif isinstance(commands, Sequence) and not isinstance(commands, (str, bytes)):
        cmd_list = list(commands)
    for cmd in cmd_list:
        if isinstance(cmd, Mapping):
            cid = cmd.get("id") or cmd.get("name") or cmd.get("tool") or ""
            label = cmd.get("label") or cmd.get("description") or ""
        else:
            cid = str(cmd)
            label = ""
        cid_l = str(cid).lower()
        label_l = str(label).lower()
        for k in keywords:
            k_l = str(k).lower()
            if k_l in cid_l or k_l in label_l:
                return str(cid) if cid is not None else None
    return None


def normalize_output(
    out: Mapping[str, Any] | None = None,
    keys: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Normalize CLI/MCP output to a standard format. Does not mutate input."""
    if not isinstance(out, Mapping):
        out = {}
    if not keys:
        keys = ["image_url", "image_path", "asset_id", "format", "width", "height", "metadata"]
    result: dict[str, Any] = {}
    nested = out.get("data") if isinstance(out.get("data"), Mapping) else {}
    for key in keys:
        if key in out and out.get(key) is not None:
            result[key] = out.get(key)
        elif key in nested and nested.get(key) is not None:
            result[key] = nested.get(key)
        else:
            result[key] = out.get(key)
    # common MCP/content wrappers: keep best-effort mapping
    if result.get("image_path") is None and isinstance(out.get("output_path"), str):
        result["image_path"] = out.get("output_path")
    return result


def normalize_mcp_config(cfg: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Normalize MCP configuration. Does not mutate input."""
    if not isinstance(cfg, Mapping):
        cfg = {}
    result = dict(cfg)
    if "transport" not in result:
        if result.get("bridge") or result.get("token"):
            result["transport"] = "bridge"
        else:
            result["transport"] = "stdio"
    # convenience: allow command+args already present; allow server.command form later
    if "timeout" in result and isinstance(result.get("timeout"), (int, float)):
        result["timeout"] = max(1, int(result["timeout"]))
    return result


def run_cli(cli_path: str, args: Sequence[str], timeout: int = 300) -> subprocess.CompletedProcess:
    """Run CLI command with standard error handling."""
    return subprocess.run([cli_path] + list(args), capture_output=True, text=True, timeout=timeout)


def discover_cli_commands(cli_path: str, timeout: int = 300) -> list[dict[str, Any]] | Any:
    """Discover available CLI commands."""
    try:
        res = run_cli(cli_path, ["commands"], timeout=timeout)
        if res.returncode == 0 and res.stdout:
            try:
                parsed = json.loads(res.stdout)
                return parsed
            except Exception:
                return []
        return []
    except Exception:
        return []


def run_cli_generation(
    cli_path: str,
    command_id: str,
    params: Mapping[str, Any],
    timeout: int = 300,
) -> subprocess.CompletedProcess:
    """Run generation via CLI."""
    args = ["run", "--cmd", command_id, "--params", json.dumps(params)]
    return run_cli(cli_path, args, timeout=timeout)


def select_mode(requested_mode: str, cli_available: bool, mcp_available: bool) -> str:
    """Pure mode decision (FR-005 back-compatible)."""
    if requested_mode not in ("auto", "cli", "mcp"):
        raise ValueError(f"Invalid mode: {requested_mode}")
    if requested_mode == "cli":
        return "cli"
    if requested_mode == "mcp":
        return "mcp"
    if cli_available:
        return "cli"
    if mcp_available:
        return "mcp"
    return "none"


def standardize_error(
    reason: str,
    message: str,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a transport-neutral error shape (additive, 006 FR-006 compatible)."""
    if metadata is None:
        metadata = {}
    md = dict(metadata)
    md.setdefault("reason", reason)
    result: dict[str, Any] = {
        "code": reason,
        "reason": reason,
        "message": message,
        "details": md,
        "retryable": reason in _MCP_TIMEOUT_REASONS or reason == "timeout",
        "metadata": md,
    }
    for k, v in md.items():
        if k not in result:
            result[k] = v
    return result


def _mcp_failure(
    reason: str,
    message: str,
    *,
    mode: str = "mcp",
    error_stage: str | None = None,
    interface: str = "mcp",
    tool: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    md: dict[str, Any] = {"mode": mode, "reason": reason, "interface": interface}
    if tool is not None:
        md["tool"] = tool
    if error_stage:
        md["error_stage"] = error_stage
    for k, v in extra.items():
        if v is not None:
            md[k] = v
    return {"success": False, "is_error": True, "error": message, "data": None, "metadata": md, "reason": reason}


def _terminate_process(proc: subprocess.Popen[Any] | None) -> None:
    if not proc:
        return
    try:
        if proc.stdin:
            proc.stdin.close()
    except Exception:
        pass
    try:
        proc.terminate()
        proc.wait(timeout=1)
    except Exception:
        try:
            proc.kill()
            proc.wait(timeout=1)
        except Exception:
            pass


def _mcp_stdio_call(cfg: Mapping[str, Any], method: str, params: Mapping[str, Any] | None = None, *, req_id: int = 1, timeout: int | None = None) -> dict[str, Any]:
    """Minimal synchronous stdio JSON-RPC call (006). Returns structured dict; never raises across boundary."""
    cfg_n = normalize_mcp_config(cfg)
    cmd = cfg_n.get("command")
    args = cfg_n.get("args") or []
    if not cmd or not isinstance(cmd, str):
        return _mcp_failure(REASON_MCP_MISCONFIGURED, "MCP stdio misconfigured: 'command' is required for stdio transport", error_stage="launch")
    if not isinstance(args, (list, tuple)):
        args = []
    env = os.environ.copy()
    extra_env = cfg_n.get("env")
    if isinstance(extra_env, Mapping):
        for k, v in extra_env.items():
            if isinstance(k, str) and v is not None:
                env[k] = str(v)
    cwd = cfg_n.get("cwd") if isinstance(cfg_n.get("cwd"), str) else None
    call_timeout = timeout or int(cfg_n.get("timeout") or cfg_n.get("call_timeout") or 30)
    try:
        proc = subprocess.Popen(
            [cmd] + [str(a) for a in args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            cwd=cwd,
            bufsize=1,
        )
    except FileNotFoundError as e:
        return _mcp_failure(REASON_MCP_MISCONFIGURED, f"MCP server command not found: {cmd}", error_stage="launch")
    except Exception as e:
        return _mcp_failure(REASON_MCP_UNAVAILABLE, f"Failed to launch MCP stdio server: {e}", error_stage="launch")

    stderr_lines: list[str] = []

    def _drain_stderr() -> None:
        try:
            if proc.stderr:
                for line in proc.stderr:
                    if line:
                        stderr_lines.append(line.rstrip("\n"))
        except Exception:
            pass

    t = threading.Thread(target=_drain_stderr, daemon=True)
    t.start()

    def _send(msg: dict[str, Any]) -> dict[str, Any] | None:
        try:
            assert proc.stdin is not None
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()
        except Exception as e:
            _terminate_process(proc)
            return _mcp_failure(REASON_MCP_INVALID_RESPONSE, f"Failed to write MCP request: {e}", error_stage="invocation")
        return None

    q: "queue.Queue[dict[str, Any] | Exception | None]" = queue.Queue()

    def _reader() -> None:
        try:
            assert proc.stdout is not None
            while True:
                line = proc.stdout.readline()
                if line == "":
                    q.put(None)
                    return
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    if isinstance(msg, dict):
                        q.put(msg)
                except Exception as e:
                    q.put(e)
                    return
        except Exception as e:
            q.put(e)

    rt = threading.Thread(target=_reader, daemon=True)
    rt.start()

    def _read_for_id(target_id: Any, stage_timeout: int, error_stage: str) -> dict[str, Any]:
        deadline = time.monotonic() + max(1, stage_timeout)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _terminate_process(proc)
                reason = REASON_MCP_STARTUP_TIMEOUT if error_stage == "initialize" else REASON_MCP_CALL_TIMEOUT
                return _mcp_failure(reason, f"MCP stdio timeout after {stage_timeout}s", error_stage=error_stage)
            try:
                item = q.get(timeout=min(0.2, remaining))
            except queue.Empty:
                if proc.poll() is not None:
                    _terminate_process(proc)
                    return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio process exited before response", error_stage=error_stage)
                continue
            if item is None:
                _terminate_process(proc)
                return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio stream closed before response", error_stage=error_stage)
            if isinstance(item, Exception):
                _terminate_process(proc)
                return _mcp_failure(REASON_MCP_INVALID_RESPONSE, f"MCP stdio invalid JSON/protocol: {item}", error_stage=error_stage)
            if item.get("id") == target_id:
                return item
            # ignore notifications/unsolicited messages; responses correlated by id

    # initialize (best-effort, short budget)
    init_budget = min(5, max(1, call_timeout))
    err = _send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "artcraft-skills", "version": __version__}}})
    if err:
        return err
    init_res = _read_for_id(1, init_budget, "initialize")
    if init_res.get("is_error"):
        if init_res.get("reason") == REASON_MCP_CALL_TIMEOUT:
            init_res["reason"] = REASON_MCP_STARTUP_TIMEOUT
            init_res.setdefault("metadata", {})["reason"] = REASON_MCP_STARTUP_TIMEOUT
            init_res["metadata"]["error_stage"] = "initialize"
        return init_res
    # initialized notification (no response expected)
    try:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
        proc.stdin.flush()
    except Exception:
        pass

    req_id_actual = req_id if req_id not in (1,) else 2
    err = _send({"jsonrpc": "2.0", "id": req_id_actual, "method": method, "params": params or {}})
    if err:
        err.setdefault("metadata", {})["error_stage"] = "invocation" if method == "tools/call" else "discovery"
        return err
    stage = "invocation" if method == "tools/call" else "discovery"
    res = _read_for_id(req_id_actual, call_timeout, stage)
    _terminate_process(proc)
    try:
        t.join(timeout=0.2)
        rt.join(timeout=0.2)
    except Exception:
        pass
    if stderr_lines and isinstance(res, dict):
        # diagnostics only; never protocol
        md = res.setdefault("metadata", {}) if isinstance(res.get("metadata"), dict) else {}
        if not isinstance(res.get("metadata"), dict):
            res["metadata"] = {"stderr_diagnostic": True}
        else:
            res["metadata"]["stderr_diagnostic"] = True
    return res


def mcp_tools_list(cfg: Mapping[str, Any], timeout: int | None = None) -> dict[str, Any] | list[Any]:
    """006: perform MCP stdio `tools/list`. Returns tools payload or structured error dict."""
    res = _mcp_stdio_call(cfg, "tools/list", {}, req_id=2, timeout=timeout)
    if not isinstance(res, dict):
        return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio returned invalid response", error_stage="discovery")
    if res.get("is_error"):
        return res
    if "error" in res and res.get("error"):
        md = {"mode": "mcp", "reason": REASON_MCP_INVALID_RESPONSE, "interface": "mcp", "error_stage": "discovery"}
        return {"success": False, "is_error": True, "error": str((res.get("error") or {}).get("message") or res.get("error")), "metadata": md, "reason": REASON_MCP_INVALID_RESPONSE}
    result = res.get("result")
    if isinstance(result, dict) and "tools" in result:
        return result
    if isinstance(result, list):
        return {"tools": result}
    if isinstance(res.get("tools"), list):
        return {"tools": res.get("tools")}
    return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP tools/list response missing tools", error_stage="discovery")


def mcp_tools_call(cfg: Mapping[str, Any], tool_name: str, arguments: Mapping[str, Any] | None = None, timeout: int | None = None) -> dict[str, Any]:
    """006: perform MCP stdio `tools/call`. Returns tool result or structured error dict."""
    res = _mcp_stdio_call(cfg, "tools/call", {"name": tool_name, "arguments": dict(arguments or {})}, req_id=3, timeout=timeout)
    if not isinstance(res, dict):
        return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio returned invalid response", error_stage="invocation", tool=tool_name)
    if res.get("is_error"):
        res.setdefault("metadata", {})
        if isinstance(res["metadata"], dict):
            res["metadata"].setdefault("tool", tool_name)
            res["metadata"].setdefault("interface", "mcp")
        return res
    if "error" in res and res.get("error"):
        msg = (res.get("error") or {}).get("message") if isinstance(res.get("error"), dict) else str(res.get("error"))
        return _mcp_failure(REASON_MCP_TOOL_ERROR, f"MCP tool error: {msg}", error_stage="invocation", tool=tool_name)
    result = res.get("result")
    if isinstance(result, dict):
        if result.get("isError") is True:
            err = result.get("error")
            msg = (err.get("message") if isinstance(err, dict) else None) or (result.get("content") or [{}])[0].get("text") if isinstance(result.get("content"), list) and result.get("content") else "MCP tool reported an error"
            return _mcp_failure(REASON_MCP_TOOL_ERROR, f"MCP tool error: {msg}", error_stage="invocation", tool=tool_name)
        return result
    if isinstance(res, dict) and res.get("isError") is True:
        return _mcp_failure(REASON_MCP_TOOL_ERROR, str(res.get("error") or "MCP tool error"), error_stage="invocation", tool=tool_name)
    return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP tools/call response missing result", error_stage="invocation", tool=tool_name)


def generate_via_editing_commands(
    cli_path: str,
    output_path: str,
    width: int = 16,
    height: int = 16,
    color: tuple = (101, 67, 33, 255),
    timeout: int = 300,
) -> subprocess.CompletedProcess:
    """Fallback: generate simple pixel art using available editing commands."""
    params = {"width": width, "height": height}
    args = ["run", "--new", json.dumps(params), "--cmd", "paint.bucket",
            "--params", json.dumps({"color": list(color)}), "--out", output_path]
    return run_cli(cli_path, args, timeout=timeout)



# --- 009: additive MCP stateful session (007 Option B, mock-first/runtime additive) ---
# Preserves 006 stateless APIs (mcp_tools_list/mcp_tools_call). Never raises across boundary.


class MCPStatefulSession:
    """Retain one MCP stdio subprocess for multiple correlated JSON-RPC calls.

    Additive 009 helper. Use as context manager; ``close()`` is idempotent and
    bounded. All public methods return structured dict/list payloads or FR-006-
    aligned failure dicts (never raise across boundary for protocol/transport).
    """

    def __init__(self, config: Mapping[str, Any], *, timeout: int | None = None):
        self._config_in = config
        self._cfg = normalize_mcp_config(config)
        self._call_timeout = int(timeout or self._cfg.get("timeout") or self._cfg.get("call_timeout") or 30)
        self._proc: subprocess.Popen[Any] | None = None
        self._q: "queue.Queue[dict[str, Any] | Exception | None] | None" = None
        self._stderr_lines: list[str] = []
        self._threads: list[threading.Thread] = []
        self._next_id = 2  # 1 reserved for initialize
        self._state = "new"
        self._init_error: dict[str, Any] | None = None

    # lifecycle
    def open(self) -> "MCPStatefulSession":
        if self._state in ("ready", "starting"):
            return self
        if self._state in ("closing", "closed", "failed"):
            return self
        self._state = "starting"
        self._init_error = self._start_and_initialize()
        if self._init_error:
            self._state = "failed"
            self.close()
        else:
            self._state = "ready"
        return self

    def __enter__(self) -> "MCPStatefulSession":
        return self.open()

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        self.close()
        return False

    def close(self) -> None:
        if self._state == "closed":
            return
        self._state = "closing"
        _terminate_process(self._proc)
        for t in self._threads:
            try:
                t.join(timeout=0.2)
            except Exception:
                pass
        self._proc = None
        self._q = None
        self._threads = []
        self._state = "closed"

    @property
    def state(self) -> str:
        return self._state

    # internals
    def _start_and_initialize(self) -> dict[str, Any] | None:
        cmd = self._cfg.get("command")
        args = self._cfg.get("args") or []
        if not cmd or not isinstance(cmd, str):
            return _mcp_failure(REASON_MCP_MISCONFIGURED, "MCP stdio misconfigured: 'command' is required for stdio transport", error_stage="launch")
        if not isinstance(args, (list, tuple)):
            args = []
        env = os.environ.copy()
        extra_env = self._cfg.get("env")
        if isinstance(extra_env, Mapping):
            for k, v in extra_env.items():
                if isinstance(k, str) and v is not None:
                    env[k] = str(v)
        cwd = self._cfg.get("cwd") if isinstance(self._cfg.get("cwd"), str) else None
        try:
            self._proc = subprocess.Popen(
                [cmd] + [str(a) for a in args],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                cwd=cwd,
                bufsize=1,
            )
        except FileNotFoundError:
            return _mcp_failure(REASON_MCP_MISCONFIGURED, f"MCP server command not found: {cmd}", error_stage="launch")
        except Exception as e:
            return _mcp_failure(REASON_MCP_UNAVAILABLE, f"Failed to launch MCP stdio server: {e}", error_stage="launch")

        self._stderr_lines = []
        proc = self._proc

        def _drain_stderr() -> None:
            try:
                if proc and proc.stderr:
                    for line in proc.stderr:
                        if line:
                            self._stderr_lines.append(line.rstrip("\n"))
            except Exception:
                pass

        t_err = threading.Thread(target=_drain_stderr, daemon=True)
        t_err.start()
        self._q = queue.Queue()

        def _reader() -> None:
            try:
                if proc and proc.stdout:
                    while True:
                        line = proc.stdout.readline()
                        if line == "":
                            self._q.put(None)  # type: ignore[union-attr]
                            return
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            msg = json.loads(line)
                            if isinstance(msg, dict):
                                self._q.put(msg)  # type: ignore[union-attr]
                        except Exception as e:
                            self._q.put(e)  # type: ignore[union-attr]
                            return
            except Exception as e:
                if self._q is not None:
                    self._q.put(e)

        t_rd = threading.Thread(target=_reader, daemon=True)
        t_rd.start()
        self._threads = [t_err, t_rd]

        init_budget = min(5, max(1, self._call_timeout))
        err = self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "artcraft-skills", "version": __version__}}})
        if err:
            return err
        init_res = self._read_for_id(1, init_budget, "initialize")
        if isinstance(init_res, dict) and init_res.get("is_error"):
            if init_res.get("reason") == REASON_MCP_CALL_TIMEOUT:
                init_res["reason"] = REASON_MCP_STARTUP_TIMEOUT
                init_res.setdefault("metadata", {})["reason"] = REASON_MCP_STARTUP_TIMEOUT
                init_res["metadata"]["error_stage"] = "initialize"
            return init_res
        try:
            if proc and proc.stdin:
                proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}) + "\n")
                proc.stdin.flush()
        except Exception:
            pass
        return None

    def _send(self, msg: dict[str, Any]) -> dict[str, Any] | None:
        proc = self._proc
        try:
            if not proc or not proc.stdin:
                return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio session has no stdin", error_stage="invocation")
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()
        except Exception as e:
            self.close()
            return _mcp_failure(REASON_MCP_INVALID_RESPONSE, f"Failed to write MCP request: {e}", error_stage="invocation")
        return None

    def _read_for_id(self, target_id: Any, stage_timeout: int, error_stage: str) -> dict[str, Any]:
        proc = self._proc
        q = self._q
        if q is None:
            return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio session has no reader", error_stage=error_stage)
        deadline = time.monotonic() + max(1, int(stage_timeout))
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                self.close()
                reason = REASON_MCP_STARTUP_TIMEOUT if error_stage == "initialize" else REASON_MCP_CALL_TIMEOUT
                return _mcp_failure(reason, f"MCP stdio timeout after {stage_timeout}s", error_stage=error_stage)
            try:
                item = q.get(timeout=min(0.2, remaining))
            except queue.Empty:
                if proc is not None and proc.poll() is not None:
                    self.close()
                    return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio process exited before response", error_stage=error_stage)
                continue
            if item is None:
                self.close()
                return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio stream closed before response", error_stage=error_stage)
            if isinstance(item, Exception):
                self.close()
                return _mcp_failure(REASON_MCP_INVALID_RESPONSE, f"MCP stdio invalid JSON/protocol: {item}", error_stage=error_stage)
            if item.get("id") == target_id:
                if self._stderr_lines and isinstance(item, dict):
                    if not isinstance(item.get("metadata"), dict):
                        item["metadata"] = {"stderr_diagnostic": True}
                    else:
                        item["metadata"]["stderr_diagnostic"] = True
                return item
            # ignore notifications/unsolicited messages

    def _rpc(self, method: str, params: Mapping[str, Any] | None, *, stage: str, tool_name: str | None = None) -> dict[str, Any]:
        if self._init_error and method != "initialize":
            return self._init_error
        if self._state == "new":
            self.open()
            if self._init_error:
                return self._init_error
        if self._state != "ready":
            return _mcp_failure(REASON_MCP_UNAVAILABLE, f"MCP stateful session not ready (state={self._state})", error_stage=stage, tool=tool_name)
        req_id = self._next_id
        self._next_id += 1
        err = self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}})
        if err:
            err.setdefault("metadata", {})["error_stage"] = stage
            if tool_name:
                err["metadata"].setdefault("tool", tool_name)
            return err
        return self._read_for_id(req_id, self._call_timeout, stage)

    # public ops (006-normalized shapes / FR-006)
    def list_tools(self) -> dict[str, Any] | list[Any]:
        res = self._rpc("tools/list", {}, stage="discovery")
        if not isinstance(res, dict):
            return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio returned invalid response", error_stage="discovery")
        if res.get("is_error"):
            return res
        if "error" in res and res.get("error"):
            md = {"mode": "mcp", "reason": REASON_MCP_INVALID_RESPONSE, "interface": "mcp", "error_stage": "discovery"}
            return {"success": False, "is_error": True, "error": str((res.get("error") or {}).get("message") or res.get("error")), "metadata": md, "reason": REASON_MCP_INVALID_RESPONSE}
        result = res.get("result")
        if isinstance(result, dict) and "tools" in result:
            return result
        if isinstance(result, list):
            return {"tools": result}
        if isinstance(res.get("tools"), list):
            return {"tools": res.get("tools")}
        return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP tools/list response missing tools", error_stage="discovery")

    def call_tool(self, tool_name: str, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
        res = self._rpc("tools/call", {"name": tool_name, "arguments": dict(arguments or {})}, stage="invocation", tool_name=tool_name)
        if not isinstance(res, dict):
            return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP stdio returned invalid response", error_stage="invocation", tool=tool_name)
        if res.get("is_error"):
            res.setdefault("metadata", {})
            if isinstance(res["metadata"], dict):
                res["metadata"].setdefault("tool", tool_name)
                res["metadata"].setdefault("interface", "mcp")
            return res
        if "error" in res and res.get("error"):
            msg = (res.get("error") or {}).get("message") if isinstance(res.get("error"), dict) else str(res.get("error"))
            return _mcp_failure(REASON_MCP_TOOL_ERROR, f"MCP tool error: {msg}", error_stage="invocation", tool=tool_name)
        result = res.get("result")
        if isinstance(result, dict):
            if result.get("isError") is True:
                err = result.get("error")
                msg = (err.get("message") if isinstance(err, dict) else None) or (result.get("content") or [{}])[0].get("text") if isinstance(result.get("content"), list) and result.get("content") else "MCP tool reported an error"
                return _mcp_failure(REASON_MCP_TOOL_ERROR, f"MCP tool error: {msg}", error_stage="invocation", tool=tool_name)
            return result
        if res.get("isError") is True:
            return _mcp_failure(REASON_MCP_TOOL_ERROR, str(res.get("error") or "MCP tool error"), error_stage="invocation", tool=tool_name)
        return _mcp_failure(REASON_MCP_INVALID_RESPONSE, "MCP tools/call response missing result", error_stage="invocation", tool=tool_name)


def mcp_stateful_session(config: Mapping[str, Any], *, timeout: int | None = None, **kwargs: Any) -> MCPStatefulSession:
    """009 additive: create a stateful MCP stdio session (context manager).

    ``kwargs`` accepted for forward/backward-compat (e.g. roots/opt_in_real hints
    reserved by contract; enforcement is harness/caller responsibility in 009
    runtime slice). Does not replace 006 stateless ``mcp_tools_list/call``.
    """
    return MCPStatefulSession(config, timeout=timeout)


__all__ = [
    "discover_cli",
    "discover_generation_command",
    "normalize_output",
    "normalize_mcp_config",
    "run_cli",
    "discover_cli_commands",
    "run_cli_generation",
    "select_mode",
    "standardize_error",
    "generate_via_editing_commands",
    "mcp_tools_list",
    "mcp_tools_call",
    "mcp_stateful_session",
    "MCPStatefulSession",
    "REASON_CLI_NOT_FOUND",
    "REASON_MCP_UNAVAILABLE",
    "REASON_MCP_MISCONFIGURED",
    "REASON_MCP_STARTUP_TIMEOUT",
    "REASON_MCP_CALL_TIMEOUT",
    "REASON_MCP_INVALID_RESPONSE",
    "REASON_MCP_MISSING_CAPABILITY",
    "REASON_MCP_TOOL_ERROR",
    "REASON_NEITHER_AVAILABLE",
    "REASON_IS_ERROR",
]
