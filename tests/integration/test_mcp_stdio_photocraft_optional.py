"""007 PhotoCraft MCP verified local smoke — optional integration (T006-T012).

US1 (T006/T009-T011): stateless `tools/list` + `tools/call name=command_list`
proof with version-tolerant assertions, resolved binary/version context,
safe temp roots (cleaned) vs explicit authorized overrides (maintainer-managed,
never auto-deleted), bounded timeout, no session reuse/artifact cycle, no
AI-generation claim. Reuses `skills.core.artcraft_app_client` (006) and
preserves FR-005/FR-006 contracts/public schemas/CLI/fallback behavior.

US2 (T007/T012): opt-in/skip/failure/FR-006-aligned mapping for missing
opt-in/prereq/binary/unsafe roots/timeout/invalid response/missing capability/
tool error; safe cleanup; no silent CLI/fallback reroute.

Default CI: excluded by `@pytest.mark.integration` / `pytest.ini -m "not integration"`.
No real PhotoCraft required for default collection or fake/monkeypatched tests.

Run explicitly (real server, when implemented/authorized):
  PYTHONPATH=. ARTCRAFT_MCP_INTEGRATION=1 python -m pytest -q -m integration \
    tests/integration/test_mcp_stdio_photocraft_optional.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Optional

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A  # noqa: E402
from skills.core.artcraft_app_client import mcp_tools_call, mcp_tools_list  # noqa: E402
from tests._helpers.fake_mcp_stdio_server import fake_server_command  # noqa: E402

pytestmark = pytest.mark.integration

ARTCRAFT_MCP_INTEGRATION_ENV = "ARTCRAFT_MCP_INTEGRATION"
PHOTOCRAFT_BINARY_OVERRIDE_ENV = "ARTCRAFT_MCP_PHOTOCRAFT_BIN"  # 007-preferred override
READ_ROOT_ENV = "ARTCRAFT_MCP_READ_ROOT"
WRITE_ROOT_ENV = "ARTCRAFT_MCP_WRITE_ROOT"
SMOKE_TOOL = "command_list"
FR006_SMOKE_REASONS = {
    A.REASON_MCP_UNAVAILABLE,
    A.REASON_MCP_MISCONFIGURED,
    A.REASON_MCP_STARTUP_TIMEOUT,
    A.REASON_MCP_CALL_TIMEOUT,
    A.REASON_MCP_INVALID_RESPONSE,
    A.REASON_MCP_MISSING_CAPABILITY,
    A.REASON_MCP_TOOL_ERROR,
}


def _integration_enabled() -> bool:
    return os.environ.get(ARTCRAFT_MCP_INTEGRATION_ENV) == "1"


def _skip_unless_enabled() -> None:
    if not _integration_enabled():
        pytest.skip(
            f"optional: set {ARTCRAFT_MCP_INTEGRATION_ENV}=1 to enable PhotoCraft MCP smoke tests"
        )


def _is_absolute_path(value: Any) -> bool:
    try:
        return isinstance(value, str) and bool(value) and Path(value).is_absolute()
    except Exception:
        return False


def _capture_version(binary_path: str) -> Optional[str]:
    if not binary_path:
        return None
    for args in ([binary_path, "--version"], [binary_path, "version"], [binary_path, "-V"]):
        try:
            proc = subprocess.run(args, capture_output=True, text=True, timeout=2, check=False)
            text = (proc.stdout or proc.stderr or "").strip()
            if text:
                return text.splitlines()[0][:200]
        except Exception:
            continue
    return None


# ---------------------------------------------------------------------------
# 007 harness (test-only, opt-in). Preserves 006/FR-005/FR-006 contracts.
# ---------------------------------------------------------------------------


def resolve_photocraft_binary(
    *,
    override_env: str = PHOTOCRAFT_BINARY_OVERRIDE_ENV,
    path_name: str = "photocraft-cli",
    opt_in: Optional[bool] = None,
) -> Dict[str, Any]:
    """Resolve authorized PhotoCraft binary (opt-in mode only)."""
    enabled = _integration_enabled() if opt_in is None else bool(opt_in)
    if not enabled:
        return {
            "available": False,
            "resolved_executable": None,
            "version": None,
            "version_context": None,
            "source": "opt_in_required",
            "reason": "opt_in_required",
            "actionable": True,
        }
    override = os.environ.get(override_env)
    if override:
        p = str(Path(override))
        if not _is_absolute_path(p) or not Path(p).exists():
            return {
                "available": False,
                "resolved_executable": None,
                "version": None,
                "version_context": None,
                "source": "override_env",
                "reason": A.REASON_MCP_MISCONFIGURED,
                "actionable": True,
                "error_stage": "prereq",
            }
        abs_p = str(Path(p).resolve())
        return {
            "available": True,
            "resolved_executable": abs_p,
            "version": _capture_version(abs_p),
            "version_context": {"binary": abs_p},
            "source": "override_env",
            "reason": None,
            "actionable": True,
        }
    resolved = shutil.which(path_name)
    if not resolved:
        return {
            "available": False,
            "resolved_executable": None,
            "version": None,
            "version_context": None,
            "source": "path",
            "reason": A.REASON_MCP_UNAVAILABLE,
            "actionable": True,
            "error_stage": "prereq",
        }
    abs_path = str(Path(resolved).resolve())
    return {
        "available": True,
        "resolved_executable": abs_path,
        "version": _capture_version(abs_path),
        "version_context": {"binary": abs_path},
        "source": "path",
        "reason": None,
        "actionable": True,
    }


@contextmanager
def provision_smoke_roots(
    *,
    read_override: Optional[str] = None,
    write_override: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    """Provision safe read/write roots. Temp auto roots cleaned; explicit overrides kept."""
    read_override = read_override if read_override is not None else os.environ.get(READ_ROOT_ENV)
    write_override = write_override if write_override is not None else os.environ.get(WRITE_ROOT_ENV)
    if read_override is not None or write_override is not None:
        if not (_is_absolute_path(read_override) and _is_absolute_path(write_override)):
            raise ValueError(f"{A.REASON_MCP_MISCONFIGURED}: explicit root overrides must be absolute authorized paths")
        read_abs = str(Path(read_override).resolve())
        write_abs = str(Path(write_override).resolve())
        for p in (read_abs, write_abs):
            Path(p).mkdir(parents=True, exist_ok=True)
        yield {
            "mode": "explicit_override",
            "read_root": read_abs,
            "write_root": write_abs,
            "cleanup_owner": "maintainer",
            "auto_deleted_override": False,
            "cleaned": False,
            "temp_paths_removed": False,
        }
        return

    base = Path(tempfile.mkdtemp(prefix="photocraft-mcp-smoke-007-"))
    read_root = base / "read"
    write_root = base / "write"
    read_root.mkdir(parents=True, exist_ok=True)
    write_root.mkdir(parents=True, exist_ok=True)
    info: Dict[str, Any] = {
        "mode": "temp_auto",
        "read_root": str(read_root),
        "write_root": str(write_root),
        "cleanup_owner": "harness",
        "cleaned": False,
        "temp_paths_removed": False,
    }
    try:
        yield info
    finally:
        try:
            shutil.rmtree(base, ignore_errors=True)
        except Exception:
            pass
        info["cleaned"] = not base.exists()
        info["temp_paths_removed"] = not base.exists()


def _extract_tool_names(tools_payload: Any) -> List[str]:
    data = tools_payload
    if isinstance(data, dict):
        if isinstance(data.get("data"), dict):
            data = data["data"]
        if isinstance(data.get("result"), dict):
            data = data["result"]
        if isinstance(data.get("tools"), list):
            data = data["tools"]
    names: List[str] = []
    if isinstance(data, list):
        for t in data:
            if isinstance(t, dict) and t.get("name"):
                names.append(str(t["name"]))
    return names


def _capability_presence(tools_payload: Any) -> Dict[str, Any]:
    names = _extract_tool_names(tools_payload)
    return {
        "supports_command_list": SMOKE_TOOL in names,
        "required_capability_present": SMOKE_TOOL in names,
        "observed_tool_names_sample": [n for n in names if n == SMOKE_TOOL][:1],
        "version_tolerant": True,
    }


def parse_command_list_result(result: Any) -> Dict[str, Any]:
    """Defensively parse/normalize command_list result (version-tolerant)."""
    if result is None:
        return {"ok": False, "is_error": True, "normalizable": False, "reason": A.REASON_MCP_INVALID_RESPONSE}
    if isinstance(result, dict):
        if result.get("is_error") is True or result.get("isError") is True:
            return {"ok": False, "is_error": True, "normalizable": True, "parsed": result, "reason": A.REASON_MCP_TOOL_ERROR}
        if result.get("success") is False:
            reason = str(((result.get("metadata") or {}).get("reason")) or result.get("reason") or A.REASON_MCP_INVALID_RESPONSE)
            return {"ok": False, "is_error": True, "normalizable": True, "parsed": result, "reason": reason}
        data = result
        if isinstance(result.get("result"), dict):
            data = result["result"]
        elif "data" in result and result.get("data") is not None:
            data = result.get("data")
        parsed: Any = data
        content = data.get("content") if isinstance(data, dict) else result.get("content")
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text = item.get("text")
                    texts.append(text)
                    if isinstance(text, str):
                        try:
                            parsed = json.loads(text)
                            break
                        except Exception:
                            parsed = text
            if texts and parsed is data:
                parsed = texts[0] if len(texts) == 1 else texts
        if isinstance(data, dict) and "structuredContent" in data:
            parsed = data.get("structuredContent")
        return {
            "ok": True,
            "is_error": False,
            "normalizable": True,
            "parsed": parsed,
            "summary": {"type": type(parsed).__name__},
        }
    if isinstance(result, (list, str, int, float, bool)):
        return {"ok": True, "is_error": False, "normalizable": True, "parsed": result, "summary": {"type": type(result).__name__}}
    return {"ok": False, "is_error": True, "normalizable": False, "reason": A.REASON_MCP_INVALID_RESPONSE}


def classify_photocraft_mcp_smoke_outcome(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Deterministic US2 outcome classification hook (FR-006-aligned)."""
    reason = kwargs.get("reason")
    if args and reason is None:
        reason = args[0]
    reason = str(reason or "opt_in_required")
    mcp_attempted = bool(kwargs.get("mcp_attempted"))
    opt_in = kwargs.get("opt_in")
    if opt_in is False or reason == "opt_in_required":
        return {
            "outcome": "skipped",
            "reason": "opt_in_required",
            "actionable": True,
            "mcp_attempted": False,
            "error_stage": kwargs.get("error_stage") or "prereq",
            "cleanup_safe": True,
        }
    if not mcp_attempted and reason in {A.REASON_MCP_MISCONFIGURED, A.REASON_MCP_UNAVAILABLE}:
        outcome = "skipped" if reason == A.REASON_MCP_UNAVAILABLE else "failed"
        return {
            "outcome": outcome,
            "reason": reason,
            "actionable": True,
            "mcp_attempted": False,
            "error_stage": kwargs.get("error_stage") or "prereq",
            "cleanup_safe": True,
        }
    stage = kwargs.get("error_stage")
    if not stage:
        stage = {
            A.REASON_MCP_UNAVAILABLE: "prereq",
            A.REASON_MCP_MISCONFIGURED: "config",
            A.REASON_MCP_STARTUP_TIMEOUT: "launch",
            A.REASON_MCP_CALL_TIMEOUT: "call",
            A.REASON_MCP_INVALID_RESPONSE: "parse",
            A.REASON_MCP_MISSING_CAPABILITY: "capability_check",
            A.REASON_MCP_TOOL_ERROR: "call",
        }.get(reason, "call")
    normalized_reason = reason if reason in FR006_SMOKE_REASONS else A.REASON_MCP_TOOL_ERROR
    mapped = A.standardize_error(normalized_reason, str(kwargs.get("message") or reason), {"mode": "mcp", "interface": "mcp", "error_stage": stage, "tool": SMOKE_TOOL})
    details = mapped.get("details") or mapped.get("metadata") or {}
    return {
        "outcome": "failed",
        "reason": mapped.get("reason") or normalized_reason,
        "error_stage": details.get("error_stage") or stage,
        "actionable": True,
        "mcp_attempted": True,
        "cleanup_safe": bool(kwargs.get("cleanup_safe", True)),
        "metadata": details,
    }


def map_photocraft_mcp_smoke_error(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """US2 outcome/error mapping hook alias."""
    return classify_photocraft_mcp_smoke_outcome(*args, **kwargs)


def _fake_command_list_mcp_config(timeout: int = 5) -> Dict[str, Any]:
    """Deterministic fake MCP config exposing `command_list` (no real server)."""
    return {
        "transport": "stdio",
        "command": sys.executable,
        "args": fake_server_command("tools_call_success", tool_name="command_list"),
        "timeout": timeout,
    }


def _build_mcp_config(binary_info: Mapping[str, Any], roots: Mapping[str, Any], timeout: int = 30) -> Dict[str, Any]:
    cmd = binary_info.get("resolved_executable") or "photocraft-cli"
    return A.normalize_mcp_config(
        {
            "transport": "stdio",
            "command": cmd,
            "args": ["mcp", "--automation-read-root", str(roots["read_root"]), "--automation-write-root", str(roots["write_root"])],
            "timeout": timeout,
        }
    )


def run_photocraft_mcp_smoke(
    *,
    mcp_config: Optional[Mapping[str, Any]] = None,
    timeout: Optional[int] = None,
    opt_in: Optional[bool] = None,
    binary_info: Optional[Mapping[str, Any]] = None,
    read_root_override: Optional[str] = None,
    write_root_override: Optional[str] = None,
    _tools_list=mcp_tools_list,
    _tools_call=mcp_tools_call,
) -> Dict[str, Any]:
    """Stateless tools/list then tools/call command_list smoke (007, opt-in)."""
    enabled = _integration_enabled() if opt_in is None else bool(opt_in)
    if not enabled:
        return {
            "outcome": "skipped",
            "reason": "opt_in_required",
            "actionable": True,
            "mcp_attempted": False,
            "stateless": True,
            "session_reuse": False,
            "artifact_cycle": False,
        }
    binary = dict(binary_info) if binary_info is not None else resolve_photocraft_binary(opt_in=True)
    if not binary.get("available", True) or not binary.get("resolved_executable"):
        out = classify_photocraft_mcp_smoke_outcome(
            reason=binary.get("reason") or A.REASON_MCP_UNAVAILABLE,
            mcp_attempted=False,
            opt_in=True,
            error_stage=binary.get("error_stage") or "prereq",
        )
        out.update({"binary": binary, "stateless": True, "session_reuse": False, "artifact_cycle": False})
        return out

    try:
        with provision_smoke_roots(read_override=read_root_override, write_override=write_root_override) as roots:
            cfg = A.normalize_mcp_config(dict(mcp_config)) if mcp_config is not None else _build_mcp_config(binary, roots, timeout or 30)
            t = timeout or int(cfg.get("timeout") or 30)
            listed = _tools_list(cfg, timeout=t)
            caps = _capability_presence(listed)
            if not caps.get("supports_command_list"):
                out = classify_photocraft_mcp_smoke_outcome(
                    reason=A.REASON_MCP_MISSING_CAPABILITY,
                    mcp_attempted=True,
                    opt_in=True,
                    error_stage="capability_check",
                    message="command_list capability not present",
                )
                out.update({"binary": binary, "roots": dict(roots), "capability_presence": caps, "capabilities": caps, "tools_list": listed, "stateless": True, "session_reuse": False, "artifact_cycle": False})
                return out
            called = _tools_call(cfg, SMOKE_TOOL, {}, timeout=t)
            invocation = parse_command_list_result(called)
            if not invocation.get("ok"):
                out = classify_photocraft_mcp_smoke_outcome(
                    reason=invocation.get("reason") or A.REASON_MCP_TOOL_ERROR,
                    mcp_attempted=True,
                    opt_in=True,
                    error_stage="call",
                    message="command_list invocation failed",
                )
                out.update({"binary": binary, "roots": dict(roots), "capability_presence": caps, "capabilities": caps, "invocation": invocation, "command_list": invocation, "stateless": True, "session_reuse": False, "artifact_cycle": False})
                return out
            result = {
                "outcome": "passed",
                "ok": True,
                "stateless": True,
                "session_reuse": False,
                "artifact_cycle": False,
                "mcp_attempted": True,
                "binary": binary,
                "roots": dict(roots),
                "capability_presence": caps,
                "capabilities": caps,
                "invocation": invocation,
                "command_list": invocation,
                "tool_target": SMOKE_TOOL,
                "version_tolerant": True,
            }
            _assert_no_ai_generation_claim(result)
            return result
    except ValueError as e:
        out = classify_photocraft_mcp_smoke_outcome(reason=A.REASON_MCP_MISCONFIGURED, mcp_attempted=False, opt_in=True, error_stage="config", message=str(e))
        out.update({"binary": binary, "stateless": True, "session_reuse": False, "artifact_cycle": False})
        return out
    except Exception as e:
        msg = str(e).lower()
        reason = A.REASON_MCP_CALL_TIMEOUT if "timeout" in msg else A.REASON_MCP_INVALID_RESPONSE if "json" in msg or "invalid" in msg else A.REASON_MCP_UNAVAILABLE
        stage = "call" if reason in {A.REASON_MCP_CALL_TIMEOUT, A.REASON_MCP_INVALID_RESPONSE} else "launch"
        out = classify_photocraft_mcp_smoke_outcome(reason=reason, mcp_attempted=True, opt_in=True, error_stage=stage, message=str(e))
        out.update({"binary": binary, "stateless": True, "session_reuse": False, "artifact_cycle": False})
        return out


def _assert_no_ai_generation_claim(payload: Any) -> None:
    blob = json.dumps(payload, default=str).lower()
    for forbidden in (
        "text-to-image",
        "text_to_image",
        "image_generation",
        "ai generation",
        "prompt-based generation",
        "provider=",
        "model=",
        "openai",
        "anthropic",
        "stable diffusion",
    ):
        assert forbidden not in blob, f"007 must not claim AI generation: found {forbidden!r}"


# ---------------------------------------------------------------------------
# Opt-in coherence (007-aligned, import/collection safe)
# ---------------------------------------------------------------------------


def test_optional_photocraft_mcp_smoke_requires_explicit_opt_in(monkeypatch=None):
    """007/006: default excluded; explicit opt-in required (coherent)."""
    if monkeypatch is not None:
        monkeypatch.delenv(ARTCRAFT_MCP_INTEGRATION_ENV, raising=False)
        assert _integration_enabled() is False
        return
    if not _integration_enabled():
        pytest.skip(
            f"optional: set {ARTCRAFT_MCP_INTEGRATION_ENV}=1 to enable PhotoCraft MCP smoke tests"
        )
    assert _integration_enabled() is True


# ---------------------------------------------------------------------------
# T006/T009-T011 (US1) — stateless smoke, fake/monkeypatched
# ---------------------------------------------------------------------------


class TestUS1StatelessSmoke:
    """US1: 007 stateless smoke behavior (deterministic seams)."""

    def test_us1_run_smoke_stateless_tools_list_then_command_list(self, monkeypatch, tmp_path):
        """US1: tools/list then tools/call(command_list), bounded, version-tolerant, no reuse."""
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        calls: List[Dict[str, Any]] = []
        cfg = _fake_command_list_mcp_config(timeout=5)

        def fake_list(c, timeout=None):
            calls.append({"op": "tools_list", "cfg": dict(c), "timeout": timeout})
            return {"tools": [{"name": "command_list", "inputSchema": {"type": "object"}}, {"name": "other"}]}

        def fake_call(c, tool_name, arguments=None, timeout=None):
            calls.append(
                {"op": "tools_call", "tool": tool_name, "arguments": dict(arguments or {}), "timeout": timeout}
            )
            return {"content": [{"type": "text", "text": json.dumps({"commands": ["paint.bucket"]})}], "isError": False}

        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.resolve_photocraft_binary",
            lambda **k: {
                "available": True,
                "resolved_executable": "/abs/fake/photocraft-cli",
                "version": "photocraft-cli 0.0.0-test",
                "version_context": {"binary": "/abs/fake/photocraft-cli"},
                "source": "override_env",
            },
        )

        @contextmanager
        def fake_roots(**k):
            info = {
                "mode": "temp_auto",
                "read_root": str(tmp_path / "r"),
                "write_root": str(tmp_path / "w"),
                "cleanup_owner": "harness",
                "cleaned": False,
            }
            yield info
            info["cleaned"] = True
            info["temp_paths_removed"] = True

        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", fake_roots)

        result = run_photocraft_mcp_smoke(mcp_config=cfg, timeout=5, _tools_list=fake_list, _tools_call=fake_call)

        assert [c["op"] for c in calls] == ["tools_list", "tools_call"]
        assert calls[1]["tool"] == "command_list"
        assert calls[1]["arguments"] == {}
        assert calls[0]["timeout"] == 5 and calls[1]["timeout"] == 5
        assert result.get("stateless") is True
        assert result.get("session_reuse") is False
        assert result.get("artifact_cycle") is False
        binary = result.get("binary") or {}
        assert binary.get("resolved_executable") == "/abs/fake/photocraft-cli"
        assert "version" in binary
        caps = result.get("capability_presence") or result.get("capabilities") or {}
        assert caps.get("supports_command_list") is True or "command_list" in json.dumps(caps)
        assert result.get("version_tolerant") is True
        invocation = result.get("invocation") or result.get("command_list") or {}
        assert invocation.get("ok") is True or invocation.get("is_error") is False
        assert invocation.get("normalizable") is True or invocation.get("parsed") is not None
        roots = result.get("roots") or {}
        assert roots.get("mode") == "temp_auto"
        assert roots.get("cleaned") is True
        _assert_no_ai_generation_claim(result)

    def test_us1_resolve_binary_prefers_override_and_records_absolute_version(self, monkeypatch, tmp_path):
        """US1: binary override preferred; resolved absolute path + version context."""
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        fake_bin = tmp_path / "photocraft-cli"
        fake_bin.write_text("#!/bin/sh\n")
        fake_bin.chmod(0o755)
        monkeypatch.setenv(PHOTOCRAFT_BINARY_OVERRIDE_ENV, str(fake_bin))
        monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/photocraft-cli")
        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional._capture_version", lambda p: "photocraft-cli 0.0.0-test")

        info = resolve_photocraft_binary(opt_in=True)

        assert os.path.isabs(info.get("resolved_executable", ""))
        assert info.get("resolved_executable") == str(fake_bin.resolve())
        assert info.get("source") in ("override", "override_env")
        assert "version" in info or "version_context" in info

    def test_us1_temp_roots_auto_created_and_cleaned(self):
        """US1: temp auto-created absolute roots cleaned after completion/failure."""
        with provision_smoke_roots() as roots:
            assert roots.get("mode") == "temp_auto"
            assert os.path.isabs(roots.get("read_root", ""))
            assert os.path.isabs(roots.get("write_root", ""))
            assert roots.get("cleanup_owner") == "harness"
            read_path = Path(roots["read_root"])
            write_path = Path(roots["write_root"])
            assert read_path.exists()
            assert write_path.exists()
            (write_path / "temp.txt").write_text("x")
        assert roots.get("cleaned") is True
        assert not read_path.exists()
        assert not write_path.exists()

    def test_us1_explicit_authorized_override_roots_not_auto_deleted(self, tmp_path):
        """US1: explicit authorized override roots are maintainer-managed, never auto-deleted."""
        read_root = tmp_path / "authorized-read"
        write_root = tmp_path / "authorized-write"
        read_root.mkdir()
        write_root.mkdir()
        sentinel = write_root / "keep.txt"
        sentinel.write_text("maintainer")

        with provision_smoke_roots(read_override=str(read_root), write_override=str(write_root)) as roots:
            assert roots.get("mode") == "explicit_override"
            assert roots.get("cleanup_owner") == "maintainer"
            assert roots.get("read_root") == str(read_root.resolve())
            assert roots.get("write_root") == str(write_root.resolve())

        assert read_root.exists()
        assert write_root.exists()
        assert sentinel.exists()
        assert roots.get("auto_deleted_override") is False

    @pytest.mark.parametrize(
        "raw",
        [
            {"content": [{"type": "text", "text": '{"commands": ["command_list"]}'}], "isError": False},
            {"structuredContent": {"commands": ["a"]}, "isError": False},
            {"result": {"content": [{"type": "text", "text": "ok"}], "isError": False}},
            {"commands": [{"name": "command_list"}], "isError": False},
        ],
    )
    def test_us1_parse_command_list_result_version_tolerant_non_error(self, raw):
        """US1: defensive, version-tolerant parse/normalization; no full catalog equality."""
        parsed = parse_command_list_result(raw)

        assert parsed.get("ok") is True
        assert parsed.get("is_error") is False
        assert parsed.get("normalizable") is True
        assert "parsed" in parsed or "summary" in parsed
        _assert_no_ai_generation_claim(parsed)

    def test_us1_smoke_result_contains_no_ai_generation_claim(self, monkeypatch):
        """US1: local PhotoCraft MCP smoke is engine/editor automation only."""
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.resolve_photocraft_binary",
            lambda **k: {"available": True, "resolved_executable": "/abs/fake/photocraft-cli", "version": "0", "source": "override_env"},
        )

        @contextmanager
        def fake_roots(**k):
            info = {"mode": "temp_auto", "read_root": "/tmp/r", "write_root": "/tmp/w", "cleanup_owner": "harness", "cleaned": True}
            yield info

        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", fake_roots)
        result = run_photocraft_mcp_smoke(
            mcp_config=_fake_command_list_mcp_config(),
            timeout=5,
            _tools_list=lambda c, timeout=None: {"tools": [{"name": "command_list"}]},
            _tools_call=lambda c, t, a=None, timeout=None: {"content": [{"type": "text", "text": "{}"}], "isError": False},
        )
        _assert_no_ai_generation_claim(result)


# ---------------------------------------------------------------------------
# T007/T012 (US2) — skips/failures/FR-006 mapping, deterministic
# ---------------------------------------------------------------------------


class TestUS2SafeFailuresAndContracts:
    """US2: opt-in/skip/failure behavior, FR-006 alignment, no unsafe fallback."""

    def test_us2_missing_opt_in_skips_without_real_execution(self, monkeypatch):
        monkeypatch.delenv(ARTCRAFT_MCP_INTEGRATION_ENV, raising=False)
        result = run_photocraft_mcp_smoke(mcp_config=_fake_command_list_mcp_config(), opt_in=False)
        assert result.get("outcome") == "skipped"
        assert result.get("reason") == "opt_in_required"
        assert result.get("mcp_attempted") is False

    def test_us2_missing_or_unresolvable_binary_is_actionable(self, monkeypatch):
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.delenv(PHOTOCRAFT_BINARY_OVERRIDE_ENV, raising=False)
        monkeypatch.setattr(shutil, "which", lambda name: None)
        info = resolve_photocraft_binary(opt_in=True)
        assert info.get("available") is False
        assert info.get("reason") == A.REASON_MCP_UNAVAILABLE
        assert info.get("actionable") is True

    def test_us2_unsafe_root_override_is_actionable(self):
        with pytest.raises(ValueError) as ei:
            with provision_smoke_roots(read_override="relative/read", write_override="/abs/write"):
                pass
        assert A.REASON_MCP_MISCONFIGURED in str(ei.value)

    @pytest.mark.parametrize(
        "reason",
        [
            A.REASON_MCP_UNAVAILABLE,
            A.REASON_MCP_MISCONFIGURED,
            A.REASON_MCP_STARTUP_TIMEOUT,
            A.REASON_MCP_CALL_TIMEOUT,
            A.REASON_MCP_INVALID_RESPONSE,
            A.REASON_MCP_MISSING_CAPABILITY,
            A.REASON_MCP_TOOL_ERROR,
        ],
    )
    def test_us2_fr006_reasons_are_actionable_and_staged(self, reason):
        out = classify_photocraft_mcp_smoke_outcome(reason=reason, mcp_attempted=True, opt_in=True)
        assert out.get("outcome") in {"failed", "skipped"}
        assert out.get("actionable") is True
        assert out.get("reason") == reason
        assert str(out.get("error_stage") or "")
        assert out.get("cleanup_safe") is True

    def test_us2_missing_capability_maps_to_fr006(self, monkeypatch):
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.resolve_photocraft_binary",
            lambda **k: {"available": True, "resolved_executable": "/abs/fake/photocraft-cli", "version": "0", "source": "override_env"},
        )

        @contextmanager
        def fake_roots(**k):
            info = {"mode": "temp_auto", "read_root": "/tmp/r", "write_root": "/tmp/w", "cleanup_owner": "harness", "cleaned": True}
            yield info

        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", fake_roots)
        result = run_photocraft_mcp_smoke(
            mcp_config=_fake_command_list_mcp_config(),
            timeout=5,
            _tools_list=lambda c, timeout=None: {"tools": [{"name": "not_command_list"}]},
            _tools_call=lambda c, t, a=None, timeout=None: pytest.fail("must not call when capability missing"),
        )
        assert result.get("reason") == A.REASON_MCP_MISSING_CAPABILITY
        assert result.get("error_stage") in {"capability_check", "call", "list"}

    def test_us2_tool_error_maps_to_fr006(self, monkeypatch):
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.resolve_photocraft_binary",
            lambda **k: {"available": True, "resolved_executable": "/abs/fake/photocraft-cli", "version": "0", "source": "override_env"},
        )

        @contextmanager
        def fake_roots(**k):
            info = {"mode": "temp_auto", "read_root": "/tmp/r", "write_root": "/tmp/w", "cleanup_owner": "harness", "cleaned": True}
            yield info

        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", fake_roots)
        result = run_photocraft_mcp_smoke(
            mcp_config=_fake_command_list_mcp_config(),
            timeout=5,
            _tools_list=lambda c, timeout=None: {"tools": [{"name": "command_list"}]},
            _tools_call=lambda c, t, a=None, timeout=None: {"isError": True, "content": [{"type": "text", "text": "boom"}]},
        )
        assert result.get("reason") == A.REASON_MCP_TOOL_ERROR

    def test_us2_temp_roots_cleaned_on_failure_path(self, monkeypatch):
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.resolve_photocraft_binary",
            lambda **k: {"available": True, "resolved_executable": "/abs/fake/photocraft-cli", "version": "0", "source": "override_env"},
        )
        seen: Dict[str, Any] = {}
        real_cm = provision_smoke_roots

        @contextmanager
        def tracking_roots(**k):
            with real_cm(**k) as info:
                seen["info"] = info
                seen["read"] = Path(info["read_root"])
                seen["write"] = Path(info["write_root"])
                yield info

        monkeypatch.setattr("tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", tracking_roots)
        result = run_photocraft_mcp_smoke(
            timeout=5,
            _tools_list=lambda c, timeout=None: (_ for _ in ()).throw(RuntimeError("timeout during list")),
            _tools_call=lambda c, t, a=None, timeout=None: pytest.fail("unreachable"),
        )
        assert result.get("outcome") == "failed"
        assert not seen["read"].exists()
        assert not seen["write"].exists()
