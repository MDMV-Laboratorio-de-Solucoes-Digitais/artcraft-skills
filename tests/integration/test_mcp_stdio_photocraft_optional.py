"""007 PhotoCraft MCP verified local smoke — optional integration (T006 RED, T007).

US1 (T006): stateless `tools/list` + `tools/call name=command_list` proof with
version-tolerant assertions, resolved binary/version context, safe temp roots
(cleaned) vs explicit authorized overrides (maintainer-managed, never auto-deleted),
no session reuse/artifact cycle, no AI-generation claim.
US2 (T007): opt-in/skip/failure/FR-006 mapping — RED tests added in T007.

Default CI: excluded by `@pytest.mark.integration` / `pytest.ini -m "not integration"`.
No real PhotoCraft required for default collection or fake/monkeypatched tests.
Harness API stubs below are intentionally RED until 007 implementation.

Run explicitly (real server, when implemented/authorized):
  PYTHONPATH=. ARTCRAFT_MCP_INTEGRATION=1 python -m pytest -q -m integration \
    tests/integration/test_mcp_stdio_photocraft_optional.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Mapping, Optional

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.artcraft_app_client import mcp_tools_call, mcp_tools_list  # noqa: E402
from tests._helpers.fake_mcp_stdio_server import fake_mcp_config, fake_server_command  # noqa: E402

pytestmark = pytest.mark.integration

ARTCRAFT_MCP_INTEGRATION_ENV = "ARTCRAFT_MCP_INTEGRATION"
PHOTOCRAFT_BINARY_OVERRIDE_ENV = "ARTCRAFT_MCP_PHOTOCRAFT_BIN"  # 007-preferred override
READ_ROOT_ENV = "ARTCRAFT_MCP_READ_ROOT"
WRITE_ROOT_ENV = "ARTCRAFT_MCP_WRITE_ROOT"


def _integration_enabled() -> bool:
    return os.environ.get(ARTCRAFT_MCP_INTEGRATION_ENV) == "1"


def _skip_unless_enabled() -> None:
    if not _integration_enabled():
        pytest.skip(
            f"optional: set {ARTCRAFT_MCP_INTEGRATION_ENV}=1 to enable PhotoCraft MCP smoke tests"
        )


# ---------------------------------------------------------------------------
# 007 harness stubs — collectible RED (T006/T007). Implementation will replace
# these with real behavior while preserving contracts and safety controls.
# ---------------------------------------------------------------------------


def resolve_photocraft_binary(
    *,
    override_env: str = PHOTOCRAFT_BINARY_OVERRIDE_ENV,
    path_name: str = "photocraft-cli",
) -> Dict[str, Any]:
    """007 RED stub: resolve authorized PhotoCraft binary (opt-in mode only).

    Intended (007): prefer override env; else PATH resolution only in opt-in mode;
    return resolved absolute executable path and version/identity context when
    available; never used for default CI.
    """
    raise NotImplementedError(
        "007 RED: resolve_photocraft_binary not implemented "
        "(override env preferred, opt-in-only PATH -> resolved absolute executable + version)"
    )


@contextmanager
def provision_smoke_roots(
    *,
    read_override: Optional[str] = None,
    write_override: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    """007 RED stub: provision safe read/write roots.

    Intended (007): default auto-create isolated temporary absolute roots and
    clean them up on completion/failure; explicit authorized absolute override
    roots are maintainer-managed and MUST NOT be auto-deleted.
    """
    raise NotImplementedError(
        "007 RED: provision_smoke_roots not implemented "
        "(temp auto-create+cleanup; explicit authorized overrides maintainer-managed)"
    )
    yield {}  # pragma: no cover


def parse_command_list_result(result: Any) -> Dict[str, Any]:
    """007 RED stub: defensively parse/normalize `command_list` result.

    Intended (007): accept adapter-normalized/JSON-RPC result, MCP `content`
    (text/serialized JSON), `structuredContent`, and `isError`/error shapes;
    return a version-tolerant non-error parseable/normalizable summary without
    exact tool count/catalog/order assertions.
    """
    raise NotImplementedError(
        "007 RED: parse_command_list_result not implemented "
        "(version-tolerant defensive parse of MCP command_list shapes)"
    )


def run_photocraft_mcp_smoke(
    *,
    mcp_config: Optional[Mapping[str, Any]] = None,
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
    """007 RED stub: stateless tools/list then tools/call command_list smoke.

    Intended (007): full MCP session per adapter call (stateless, no reuse),
    `mcp_tools_list` then `mcp_tools_call(..., 'command_list', {})`, bounded
    timeout, resolved binary/version context when available, minimal
    version-tolerant capability/invocation evidence, no AI-generation claim,
    no artifact-producing cycle.
    """
    raise NotImplementedError(
        "007 RED: run_photocraft_mcp_smoke not implemented "
        "(stateless tools/list + tools/call command_list, bounded timeout, FR-006 aligned)"
    )


def classify_photocraft_mcp_smoke_outcome(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """007 RED stub: deterministic US2 outcome classification hook.

    Intended: map missing opt-in/prereq/unsafe boundaries/timeouts/invalid
    responses/missing capability/tool errors to FR-006-aligned actionable
    outcomes or skips with safe cleanup semantics.
    """
    # Incomplete on purpose (RED): T005 expects FR-006 reason/error_stage mapping.
    return {"outcome": "red", "implemented": False, "args_seen": bool(args or kwargs)}


def map_photocraft_mcp_smoke_error(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """007 RED stub alias for US2 outcome/error mapping hook."""
    return classify_photocraft_mcp_smoke_outcome(*args, **kwargs)

def _fake_command_list_mcp_config(timeout: int = 5) -> Dict[str, Any]:
    """Deterministic fake MCP config exposing `command_list` (no real server)."""
    return {
        "transport": "stdio",
        "command": sys.executable,
        "args": fake_server_command("tools_call_success", tool_name="command_list"),
        "timeout": timeout,
    }


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
# Existing/coherent opt-in behavior (007-aligned, import/collection safe)
# ---------------------------------------------------------------------------


def test_optional_photocraft_mcp_smoke_requires_explicit_opt_in():
    """007/006: default excluded; explicit opt-in required (coherent skip)."""
    _skip_unless_enabled()
    # When explicitly enabled, harness logic is exercised by 007 tests below.
    # This test remains a minimal opt-in coherence check and is safe under fakes.
    assert _integration_enabled() is True


# ---------------------------------------------------------------------------
# T006 (US1) RED integration tests — stateless smoke, fake/monkeypatched
# ---------------------------------------------------------------------------


class TestUS1StatelessSmokeRED:
    """T006 US1: intended 007 stateless smoke behavior (RED until implemented)."""

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
                "resolved_executable": "/abs/fake/photocraft-cli",
                "version": "photocraft-cli 0.0.0-test",
                "source": "override",
            },
        )

        @contextmanager
        def fake_roots(**k):
            yield {
                "mode": "temp_auto",
                "read_root": str(tmp_path / "r"),
                "write_root": str(tmp_path / "w"),
                "cleanup_owner": "harness",
                "cleaned": False,
            }

        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.provision_smoke_roots", fake_roots
        )

        result = run_photocraft_mcp_smoke(mcp_config=cfg, timeout=5)

        # RED expected until harness implemented: result must be evidence-rich.
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
        # Version-tolerant: supports command_list; never exact count/catalog equality.
        assert caps.get("supports_command_list") is True or "command_list" in json.dumps(caps)
        assert "tool_count" not in json.dumps(result).lower() or result.get("version_tolerant") is True
        invocation = result.get("invocation") or result.get("command_list") or {}
        assert invocation.get("ok") is True or invocation.get("is_error") is False
        assert invocation.get("normalizable") is True or invocation.get("parsed") is not None
        roots = result.get("roots") or {}
        assert roots.get("mode") == "temp_auto"
        assert roots.get("cleaned") is True
        _assert_no_ai_generation_claim(result)

    def test_us1_resolve_binary_prefers_override_and_records_absolute_version(self, monkeypatch):
        """US1: binary override preferred; resolved absolute path + version context."""
        monkeypatch.setenv(ARTCRAFT_MCP_INTEGRATION_ENV, "1")
        monkeypatch.setenv(PHOTOCRAFT_BINARY_OVERRIDE_ENV, "/opt/photocraft/bin/photocraft-cli")
        monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/photocraft-cli")

        info = resolve_photocraft_binary()

        assert os.path.isabs(info.get("resolved_executable", ""))
        assert info.get("resolved_executable") == "/opt/photocraft/bin/photocraft-cli"
        assert info.get("source") in ("override", "override_env")
        assert "version" in info or "version_context" in info

    def test_us1_temp_roots_auto_created_and_cleaned(self, tmp_path):
        """US1: temp auto-created absolute roots cleaned after completion/failure."""
        base = tmp_path / "base"
        base.mkdir()
        read_created = base / "r"
        write_created = base / "w"

        with provision_smoke_roots() as roots:
            assert roots.get("mode") == "temp_auto"
            assert os.path.isabs(roots.get("read_root", ""))
            assert os.path.isabs(roots.get("write_root", ""))
            assert roots.get("cleanup_owner") == "harness"
            # If implementation creates real temp dirs, they should exist in context.
            read_created.mkdir(exist_ok=True)
            write_created.mkdir(exist_ok=True)

        # RED expected: harness must report/perform cleanup of temp roots.
        assert roots.get("cleaned") is True
        assert not read_created.exists() or roots.get("temp_paths_removed") is True
        assert not write_created.exists() or roots.get("temp_paths_removed") is True

    def test_us1_explicit_authorized_override_roots_not_auto_deleted(self, tmp_path):
        """US1: explicit authorized override roots are maintainer-managed, never auto-deleted."""
        read_root = tmp_path / "authorized-read"
        write_root = tmp_path / "authorized-write"
        read_root.mkdir()
        write_root.mkdir()
        sentinel = write_root / "keep.txt"
        sentinel.write_text("maintainer")

        with provision_smoke_roots(
            read_override=str(read_root), write_override=str(write_root)
        ) as roots:
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
        # Force the intended result shape to be validated once implemented.
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.mcp_tools_list",
            lambda c, timeout=None: {"tools": [{"name": "command_list"}]},
        )
        monkeypatch.setattr(
            "tests.integration.test_mcp_stdio_photocraft_optional.mcp_tools_call",
            lambda c, t, a=None, timeout=None: {"content": [{"type": "text", "text": "{}"}], "isError": False},
        )
        result = run_photocraft_mcp_smoke(mcp_config=_fake_command_list_mcp_config(), timeout=5)
        _assert_no_ai_generation_claim(result)
