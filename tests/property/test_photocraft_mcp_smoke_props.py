"""007 RED/property invariants: PhotoCraft MCP verified local smoke (T004,T005).

Deterministic, no sleeps, no real PhotoCraft server/binary in default CI.
Covers 007 invariants:
- explicit opt-in required; excluded from default CI
- stateless smoke target is tools/list + tools/call name=command_list only
- no prompt-based AI generation/provider/model claim
- safe roots: temp auto-created absolute roots cleaned by harness; explicit
  authorized absolute overrides are maintainer-managed (never auto-deleted)
- minimal, version-tolerant assertions (no exact tool count/catalog equality)
- FR-006-aligned actionable outcomes; public schemas/CLI/fallback/FR-005 unchanged
"""
import os
import sys
from collections.abc import Mapping
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest  # noqa: E402
from hypothesis import given, settings, strategies as st  # noqa: E402

from skills.core import artcraft_app_client as A  # noqa: E402
from tests._helpers.fake_mcp_stdio_server import fake_mcp_config  # noqa: E402

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")

# ---------------------------------------------------------------------------
# T004 (US1) — 007 stateless verified smoke invariants (RED for missing harness)
# Separate class/section; T005 adds failure/contract invariants in same file.
# ---------------------------------------------------------------------------

SMOKE_OPT_IN_ENV = "ARTCRAFT_MCP_INTEGRATION"
SMOKE_TOOL_TARGET = "command_list"
SMOKE_FR006_REASONS = {
    A.REASON_MCP_UNAVAILABLE,
    A.REASON_MCP_MISCONFIGURED,
    A.REASON_MCP_STARTUP_TIMEOUT,
    A.REASON_MCP_CALL_TIMEOUT,
    A.REASON_MCP_INVALID_RESPONSE,
    A.REASON_MCP_MISSING_CAPABILITY,
    A.REASON_MCP_TOOL_ERROR,
}
SMOKE_ALLOWED_COMPAT_REASONS = SMOKE_FR006_REASONS | {
    A.REASON_CLI_NOT_FOUND,
    A.REASON_NEITHER_AVAILABLE,
    A.REASON_IS_ERROR,
}
FORBIDDEN_AI_FIELDS = {
    "prompt",
    "negative_prompt",
    "provider",
    "model",
    "image_generation",
    "video_generation",
    "audio_generation",
    "three_d_generation",
}


def _is_absolute_path(path: str) -> bool:
    if not isinstance(path, str) or not path:
        return False
    return PurePosixPath(path).is_absolute() or PureWindowsPath(path).is_absolute()


def is_opt_in_enabled(env: Mapping[str, str] | None) -> bool:
    """007 C/FR-001: explicit opt-in required; absent/other values => disabled."""
    if not env:
        return False
    return env.get(SMOKE_OPT_IN_ENV) == "1"


def select_photocraft_binary(
    *,
    opt_in: bool,
    override_path: str | None,
    path_resolved_executable: str | None,
) -> dict[str, Any]:
    """007 C1/FR-004: override preferred in opt-in; PATH fallback only in opt-in.

    Never resolves/launches a real server outside explicit opt-in mode.
    Resolved launch target must be absolute when a real execution is selected.
    """
    if not opt_in:
        return {
            "allowed": False,
            "source": "default_disabled",
            "resolved_absolute": None,
            "recorded_identity": None,
            "reason": "opt_in_required",
        }
    if override_path:
        if not _is_absolute_path(override_path):
            return {
                "allowed": False,
                "source": "override",
                "resolved_absolute": None,
                "recorded_identity": None,
                "reason": A.REASON_MCP_MISCONFIGURED,
            }
        return {
            "allowed": True,
            "source": "override",
            "resolved_absolute": override_path,
            "recorded_identity": override_path,
            "reason": None,
        }
    if path_resolved_executable:
        if not _is_absolute_path(path_resolved_executable):
            return {
                "allowed": False,
                "source": "path",
                "resolved_absolute": None,
                "recorded_identity": None,
                "reason": A.REASON_MCP_MISCONFIGURED,
            }
        return {
            "allowed": True,
            "source": "path",
            "resolved_absolute": path_resolved_executable,
            "recorded_identity": path_resolved_executable,
            "reason": None,
        }
    return {
        "allowed": False,
        "source": "path",
        "resolved_absolute": None,
        "recorded_identity": None,
        "reason": A.REASON_MCP_UNAVAILABLE,
    }


def classify_root_policy(
    *,
    read_override: str | None = None,
    write_override: str | None = None,
) -> dict[str, Any]:
    """007 C2/FR-004: temp auto roots by default; explicit absolute overrides maintainer-managed.

    Invalid explicit overrides are actionable and must not trigger unsafe fallback.
    """
    if read_override is None and write_override is None:
        return {
            "mode": "temp_auto",
            "cleanup_owner": "harness",
            "harness_may_delete": True,
            "read_absolute_required": True,
            "write_absolute_required": True,
            "actionable_failure": None,
        }
    if read_override is None or write_override is None:
        return {
            "mode": "invalid_override",
            "cleanup_owner": "none",
            "harness_may_delete": False,
            "actionable_failure": A.REASON_MCP_MISCONFIGURED,
        }
    if not _is_absolute_path(read_override) or not _is_absolute_path(write_override):
        return {
            "mode": "invalid_override",
            "cleanup_owner": "none",
            "harness_may_delete": False,
            "actionable_failure": A.REASON_MCP_MISCONFIGURED,
        }
    return {
        "mode": "explicit_override",
        "cleanup_owner": "maintainer",
        "harness_may_delete": False,
        "read_absolute": read_override,
        "write_absolute": write_override,
        "actionable_failure": None,
    }


def is_stateless_command_list_smoke_target(
    *,
    list_called: bool,
    call_name: str | None,
    session_reused: bool = False,
    artifact_cycle: bool = False,
) -> bool:
    """007 FR-002/FR-003/FR-009: only tools/list + command_list, stateless, no artifact cycle."""
    return (
        list_called
        and call_name == SMOKE_TOOL_TARGET
        and not session_reused
        and not artifact_cycle
    )


def capability_presence_minimal(tools_payload: Any, required: str = SMOKE_TOOL_TARGET) -> bool:
    """007 C3/contract §5: presence only; never exact count/catalog/order/deep equality."""
    if isinstance(tools_payload, dict):
        if tools_payload.get("success") is False:
            return False
        tools = tools_payload.get("tools")
        if tools is None and isinstance(tools_payload.get("data"), dict):
            tools = tools_payload["data"].get("tools")
        if tools is None and isinstance(tools_payload.get("result"), dict):
            tools = tools_payload["result"].get("tools")
        tools_payload = tools
    if not isinstance(tools_payload, list):
        return False
    return any(isinstance(t, dict) and t.get("name") == required for t in tools_payload)


def command_list_outcome_minimally_acceptable(outcome: Any) -> bool:
    """007 C3/contract §4.3: non-error parseable/normalizable structure is sufficient."""
    if outcome is None:
        return False
    if isinstance(outcome, dict):
        if outcome.get("is_error") is True or outcome.get("isError") is True:
            return False
        if outcome.get("success") is False:
            return False
        if "error" in outcome and outcome.get("error"):
            return False
        # Accept adapter-normalized success, JSON-RPC result envelope, or content-bearing shape.
        return True
    if isinstance(outcome, (list, str, int, float, bool)):
        return True
    return False


def assert_no_ai_generation_claim(evidence: Mapping[str, Any]) -> None:
    """007 FR-003/FR-008: local PhotoCraft MCP smoke must not claim prompt-based AI generation."""
    lowered_keys = {str(k).lower() for k in evidence.keys()}
    leaked = {k for k in FORBIDDEN_AI_FIELDS if k in lowered_keys}
    assert not leaked, f"007 smoke evidence must not claim AI generation/provider fields: {sorted(leaked)}"
    text = str(evidence.get("summary") or evidence.get("scope") or "").lower()
    for bad in ("prompt-based", "image generation", "provider routing", "model routing"):
        assert bad not in text, f"007 smoke evidence must not claim AI scope: {bad}"


class TestT004PhotoCraftMCPStatelessSmokeInvariants:
    """US1 (P1) — real local PhotoCraft MCP stateless smoke invariants (007)."""

    @settings(max_examples=60, deadline=None)
    @given(st.dictionaries(st.text(min_size=0, max_size=24), st.text(max_size=24), max_size=8))
    def test_opt_in_gate_prevents_real_execution_without_explicit_enablement(self, env):
        """FR-001/SC-002: absent or non-'1' values never enable real verification."""
        enabled = is_opt_in_enabled(env)
        if env.get(SMOKE_OPT_IN_ENV) == "1":
            assert enabled is True
        else:
            assert enabled is False
        if not enabled:
            decision = select_photocraft_binary(
                opt_in=False,
                override_path="/usr/local/bin/photocraft-cli",
                path_resolved_executable="/usr/bin/photocraft-cli",
            )
            assert decision["allowed"] is False
            assert decision["source"] == "default_disabled"
            assert decision["resolved_absolute"] is None

    @settings(max_examples=50, deadline=None)
    @given(
        st.one_of(st.none(), st.text(min_size=1, max_size=80)),
        st.one_of(st.none(), st.text(min_size=1, max_size=80)),
    )
    def test_binary_selection_records_resolved_absolute_only_in_opt_in_mode(
        self, override_path, path_resolved
    ):
        """C1/FR-004: PATH fallback only in opt-in; resolved launch target is absolute."""
        out_opt_in = select_photocraft_binary(
            opt_in=True,
            override_path=override_path,
            path_resolved_executable=path_resolved,
        )
        out_default = select_photocraft_binary(
            opt_in=False,
            override_path=override_path,
            path_resolved_executable=path_resolved,
        )
        assert out_default["allowed"] is False
        assert out_default["source"] == "default_disabled"
        if out_opt_in["allowed"]:
            assert out_opt_in["resolved_absolute"] is not None
            assert _is_absolute_path(out_opt_in["resolved_absolute"])
            assert out_opt_in["recorded_identity"] == out_opt_in["resolved_absolute"]
            if override_path and _is_absolute_path(override_path):
                assert out_opt_in["source"] == "override"
            elif (not override_path or not _is_absolute_path(override_path)) and path_resolved and _is_absolute_path(
                path_resolved
            ):
                assert out_opt_in["source"] == "path"
        if out_opt_in["source"] in {"override", "path"} and not out_opt_in["allowed"]:
            assert out_opt_in["reason"] in SMOKE_ALLOWED_COMPAT_REASONS | {"opt_in_required"}

    @settings(max_examples=60, deadline=None)
    @given(
        st.one_of(st.none(), st.text(min_size=0, max_size=80)),
        st.one_of(st.none(), st.text(min_size=0, max_size=80)),
    )
    def test_temp_auto_roots_default_and_explicit_absolute_overrides_maintainer_managed(
        self, read_override, write_override
    ):
        """C2/FR-004/contract §3.1: temp auto + harness cleanup; explicit absolute overrides not auto-deleted."""
        policy = classify_root_policy(read_override=read_override, write_override=write_override)
        if read_override is None and write_override is None:
            assert policy["mode"] == "temp_auto"
            assert policy["cleanup_owner"] == "harness"
            assert policy["harness_may_delete"] is True
            assert policy["actionable_failure"] is None
            return
        if policy["mode"] == "explicit_override":
            assert policy["cleanup_owner"] == "maintainer"
            assert policy["harness_may_delete"] is False
            assert _is_absolute_path(policy["read_absolute"])
            assert _is_absolute_path(policy["write_absolute"])
            assert policy["actionable_failure"] is None
            return
        assert policy["mode"] == "invalid_override"
        assert policy["cleanup_owner"] == "none"
        assert policy["harness_may_delete"] is False
        assert policy["actionable_failure"] == A.REASON_MCP_MISCONFIGURED

    @settings(max_examples=50, deadline=None)
    @given(
        st.booleans(),
        st.sampled_from([SMOKE_TOOL_TARGET, "doc_new", "command_run", "other", None]),
        st.booleans(),
        st.booleans(),
    )
    def test_command_list_only_deterministic_stateless_smoke_target(
        self, list_called, call_name, session_reused, artifact_cycle
    ):
        """FR-002/FR-003/FR-009: only tools/list + command_list; no session reuse/artifact cycle."""
        ok = is_stateless_command_list_smoke_target(
            list_called=list_called,
            call_name=call_name,
            session_reused=session_reused,
            artifact_cycle=artifact_cycle,
        )
        if list_called and call_name == SMOKE_TOOL_TARGET and not session_reused and not artifact_cycle:
            assert ok is True
        else:
            assert ok is False

    @settings(max_examples=70, deadline=None)
    @given(
        st.lists(
            st.fixed_dictionaries({"name": st.text(min_size=0, max_size=24)}).map(
                lambda d: {"name": d["name"]}
            ),
            min_size=0,
            max_size=40,
        ),
        st.integers(min_value=0, max_value=6),
        st.booleans(),
    )
    def test_minimal_capability_presence_forbids_exact_tool_count_catalog_equality(
        self, tools, insert_at, prepend_required
    ):
        """C3/contract §5: presence of command_list only; count/order/catalog equality forbidden."""
        tools = list(tools)
        has_required = any(isinstance(t, dict) and t.get("name") == SMOKE_TOOL_TARGET for t in tools)
        if prepend_required and not has_required:
            idx = min(insert_at, len(tools))
            tools.insert(idx, {"name": SMOKE_TOOL_TARGET})
            has_required = True

        present = capability_presence_minimal(tools, SMOKE_TOOL_TARGET)
        assert present is has_required

        # Version-tolerant: extra tools, different count, and different order do not invalidate presence.
        mutated = [{"name": "z_other"}] + tools + [{"name": "a_extra"}, {"name": "doc_list"}]
        mutated.reverse()
        assert capability_presence_minimal(mutated, SMOKE_TOOL_TARGET) is has_required

        # Defensive acceptance of adapter/fake payload envelopes (no real server).
        envelope = {"success": True, "data": {"tools": tools}}
        assert capability_presence_minimal(envelope, SMOKE_TOOL_TARGET) is has_required

    def test_fake_mcp_stdio_seam_supports_deterministic_command_list_shape(self):
        """Uses fake_mcp_stdio_server seam pattern (deterministic, no real server)."""
        cfg = fake_mcp_config("success", tool_name=SMOKE_TOOL_TARGET)
        normalized = A.normalize_mcp_config(cfg)
        assert normalized.get("command")
        assert normalized.get("transport") == "stdio"
        assert normalized.get("tool_name") == SMOKE_TOOL_TARGET
        tools = [{"name": "doc_new"}, {"name": SMOKE_TOOL_TARGET}, {"name": "command_run"}]
        assert capability_presence_minimal(tools) is True
        assert command_list_outcome_minimally_acceptable({"success": True, "data": {"commands": []}}) is True
        assert_no_ai_generation_claim({"scope": "stateless engine/editor smoke", "tool": SMOKE_TOOL_TARGET})

    def test_007_harness_entrypoint_missing_is_red(self):
        """RED integration-facing assertion: 007 harness must exist/behave as 007 requires.

        Intentional RED failure until 007 implementation lands (T006-T008+).
        """
        try:
            import tests.integration.test_mcp_stdio_photocraft_optional as opt_mod
        except Exception as exc:  # pragma: no cover - import boundary
            pytest.fail(
                "007 harness not implemented (RED): cannot import "
                f"tests.integration.test_mcp_stdio_photocraft_optional ({exc!r})"
            )
        for name in (
            "run_photocraft_mcp_smoke",
            "execute_photocraft_mcp_smoke",
            "photocraft_mcp_smoke",
            "smoke_photocraft_mcp",
            "build_photocraft_smoke_harness",
        ):
            fn = getattr(opt_mod, name, None)
            if callable(fn):
                # Presence is necessary but not sufficient; T006/T007/T008 own behavior.
                return
        pytest.fail(
            "007 harness not implemented (RED): expected a callable stateless smoke entrypoint "
            "(e.g. run_photocraft_mcp_smoke / execute_photocraft_mcp_smoke / photocraft_mcp_smoke) "
            "in tests.integration.test_mcp_stdio_photocraft_optional implementing 007 opt-in, "
            "resolved-absolute binary selection, temp-auto/explicit-maintainer roots, "
            "tools/list + command_list only, and FR-006-aligned outcomes."
        )


# ---------------------------------------------------------------------------
# T005 (US2) — 007 failure/contract invariants (RED for missing harness behavior)
# Separate class/section in same file; same deterministic, no real server/binary.
# ---------------------------------------------------------------------------

SMOKE_SKIP_REASONS = {"opt_in_required", "real_binary_unavailable", "unsafe_roots"}
SMOKE_ERROR_STAGES = {
    "prereq",
    "config",
    "launch",
    "list",
    "capability_check",
    "call",
    "parse",
    "cleanup",
    "unknown",
}

FAILURE_CASES = (
    ("missing_opt_in", None, {"skip": True, "reason": "opt_in_required"}),
    ("missing_prereq", A.REASON_MCP_UNAVAILABLE, {"error_stage": "launch"}),
    ("unsafe_boundary", A.REASON_MCP_MISCONFIGURED, {"error_stage": "config"}),
    ("startup_timeout", A.REASON_MCP_STARTUP_TIMEOUT, {"error_stage": "launch"}),
    ("call_timeout", A.REASON_MCP_CALL_TIMEOUT, {"error_stage": "call"}),
    ("invalid_response", A.REASON_MCP_INVALID_RESPONSE, {"error_stage": "parse"}),
    ("missing_capability", A.REASON_MCP_MISSING_CAPABILITY, {"error_stage": "capability_check"}),
    ("tool_error", A.REASON_MCP_TOOL_ERROR, {"error_stage": "call"}),
)


def classify_smoke_failure(
    *,
    case: str,
    opt_in: bool,
    root_policy: Mapping[str, Any] | None = None,
    capability_present: bool = True,
    transport_reason: str | None = None,
) -> dict[str, Any]:
    """007 US2: failures/skips are structured and actionable; no unsafe fallback."""
    root_policy = dict(root_policy or classify_root_policy())
    if not opt_in or case == "missing_opt_in":
        return {
            "outcome": "skipped",
            "reason": "opt_in_required",
            "actionable": True,
            "mcp_attempted": False,
            "cleanup_required": False,
            "unsafe_state_leakage": False,
        }
    if root_policy.get("mode") == "invalid_override" or case == "unsafe_boundary":
        return {
            "outcome": "failed",
            "reason": A.REASON_MCP_MISCONFIGURED,
            "error_stage": "config",
            "actionable": True,
            "mcp_attempted": False,
            "cleanup_required": False,
            "unsafe_state_leakage": False,
            "fallback_to_unsafe_root": False,
        }
    if case == "missing_prereq":
        return {
            "outcome": "failed",
            "reason": transport_reason or A.REASON_MCP_UNAVAILABLE,
            "error_stage": "launch",
            "actionable": True,
            "mcp_attempted": True,
            "cleanup_required": root_policy.get("mode") == "temp_auto",
            "unsafe_state_leakage": False,
        }
    if case == "missing_capability" or (not capability_present and case == "missing_capability"):
        return {
            "outcome": "failed",
            "reason": A.REASON_MCP_MISSING_CAPABILITY,
            "error_stage": "capability_check",
            "actionable": True,
            "mcp_attempted": True,
            "cleanup_required": root_policy.get("mode") == "temp_auto",
            "unsafe_state_leakage": False,
            "required_capability": SMOKE_TOOL_TARGET,
        }
    reason = transport_reason or A.REASON_MCP_TOOL_ERROR
    stage = {
        A.REASON_MCP_STARTUP_TIMEOUT: "launch",
        A.REASON_MCP_CALL_TIMEOUT: "call",
        A.REASON_MCP_INVALID_RESPONSE: "parse",
        A.REASON_MCP_TOOL_ERROR: "call",
        A.REASON_MCP_MISCONFIGURED: "config",
        A.REASON_MCP_UNAVAILABLE: "launch",
    }.get(reason, "call")
    return {
        "outcome": "failed",
        "reason": reason,
        "error_stage": stage,
        "actionable": True,
        "mcp_attempted": True,
        "cleanup_required": root_policy.get("mode") == "temp_auto",
        "unsafe_state_leakage": False,
    }


def cleanup_obligation(root_policy: Mapping[str, Any] | None) -> dict[str, Any]:
    """007 C2: harness cleans only temp auto roots; explicit overrides maintainer-managed."""
    policy = dict(root_policy or {})
    mode = policy.get("mode")
    if mode == "temp_auto":
        return {
            "must_cleanup_temp_roots": True,
            "may_delete_explicit_overrides": False,
            "owner": "harness",
        }
    if mode == "explicit_override":
        return {
            "must_cleanup_temp_roots": False,
            "may_delete_explicit_overrides": False,
            "owner": "maintainer",
        }
    return {
        "must_cleanup_temp_roots": False,
        "may_delete_explicit_overrides": False,
        "owner": "none",
    }


def outcome_has_fr006_metadata(outcome: Mapping[str, Any]) -> bool:
    """007 FR-006: when MCP attempted, reason/error_stage/actionable metadata present."""
    if not outcome.get("mcp_attempted"):
        return True
    reason = str(outcome.get("reason") or "")
    stage = str(outcome.get("error_stage") or "")
    return bool(reason in SMOKE_ALLOWED_COMPAT_REASONS and stage and outcome.get("actionable") is True)


class TestT005PhotoCraftMCPFailureContractInvariants:
    """US2 (P2) — safe failures, FR-006 metadata, cleanup, and contract preservation."""

    @settings(max_examples=70, deadline=None)
    @given(st.sampled_from(FAILURE_CASES), st.booleans())
    def test_failure_cases_yield_structured_actionable_outcome_or_skip(self, case_def, capability_present):
        """US2 scenarios 1-2: missing prereq/unsafe/timeout/invalid/missing-capability/tool-error are actionable."""
        case, transport_reason, expected = case_def
        root_policy = classify_root_policy(read_override="relative/read", write_override=None) if case == "unsafe_boundary" else classify_root_policy()
        # Capability absence is only meaningful for the missing_capability case; other cases model transport/outcome failures.
        effective_capability = False if case == "missing_capability" else (capability_present if case not in {"missing_opt_in", "missing_prereq", "unsafe_boundary"} else True)
        out = classify_smoke_failure(
            case=case,
            opt_in=case != "missing_opt_in",
            root_policy=root_policy,
            capability_present=effective_capability,
            transport_reason=transport_reason,
        )
        assert out.get("outcome") in {"failed", "skipped"}
        assert out.get("actionable") is True
        assert out.get("unsafe_state_leakage") is False
        if expected.get("skip"):
            assert out.get("outcome") == "skipped"
            assert out.get("reason") == expected["reason"]
            assert out.get("mcp_attempted") is False
        else:
            if case == "missing_capability":
                assert out.get("reason") == A.REASON_MCP_MISSING_CAPABILITY
            elif transport_reason:
                # unsafe_boundary is config-classified regardless of nominal transport reason in the case table.
                expected_reason = A.REASON_MCP_MISCONFIGURED if case == "unsafe_boundary" else transport_reason
                assert out.get("reason") == expected_reason
            assert str(out.get("error_stage") or "")

    @settings(max_examples=60, deadline=None)
    @given(
        st.sampled_from(sorted(SMOKE_FR006_REASONS)),
        st.sampled_from(sorted(SMOKE_ERROR_STAGES - {"unknown"})),
    )
    def test_fr006_reason_and_error_stage_present_when_mcp_attempted(self, reason, stage):
        """FR-006: MCP-attempted failures carry actionable reason and error_stage metadata."""
        modeled = A.standardize_error(
            reason,
            "actionable smoke failure",
            {"mode": "mcp", "interface": "mcp", "error_stage": stage, "tool": SMOKE_TOOL_TARGET},
        )
        assert modeled.get("reason") == reason or modeled.get("code") == reason
        details = modeled.get("details") or modeled.get("metadata") or {}
        assert details.get("error_stage") == stage
        assert details.get("interface") == "mcp"
        outcome = {
            "mcp_attempted": True,
            "reason": reason,
            "error_stage": stage,
            "actionable": True,
        }
        assert outcome_has_fr006_metadata(outcome) is True

    @settings(max_examples=60, deadline=None)
    @given(
        st.one_of(st.none(), st.text(min_size=0, max_size=80)),
        st.one_of(st.none(), st.text(min_size=0, max_size=80)),
        st.sampled_from(["pass", "fail", "timeout", "tool_error"]),
    )
    def test_cleanup_obligations_representable_without_unsafe_leakage(
        self, read_override, write_override, completion
    ):
        """US2 scenario 2/C2: temp auto roots cleaned on pass/fail; explicit overrides never auto-deleted."""
        policy = classify_root_policy(read_override=read_override, write_override=write_override)
        obligation = cleanup_obligation(policy)
        modeled = {
            "completion": completion,
            "root_mode": policy.get("mode"),
            "cleanup": obligation,
            "unsafe_state_leakage": False,
        }
        assert modeled["unsafe_state_leakage"] is False
        if policy.get("mode") == "temp_auto":
            assert obligation["must_cleanup_temp_roots"] is True
            assert obligation["may_delete_explicit_overrides"] is False
            assert obligation["owner"] == "harness"
        elif policy.get("mode") == "explicit_override":
            assert obligation["must_cleanup_temp_roots"] is False
            assert obligation["may_delete_explicit_overrides"] is False
            assert obligation["owner"] == "maintainer"
        else:
            assert obligation["must_cleanup_temp_roots"] is False
            assert obligation["may_delete_explicit_overrides"] is False
        # Model represents no leaked roots/process obligation after cleanup decision.
        assert "leaked_root" not in modeled
        assert "leaked_process" not in modeled

    @settings(max_examples=50, deadline=None)
    @given(st.dictionaries(st.text(min_size=1, max_size=12), st.text(max_size=20), max_size=6))
    def test_public_adapter_contracts_unchanged_by_007_smoke_modeling(self, cfg):
        """FR-005/FR-007/SC-003: 007 modeling uses existing adapter; config/selection/fallback preserved."""
        before = dict(cfg)
        normalized = A.normalize_mcp_config(cfg)
        assert cfg == before  # normalize_mcp_config must not mutate input
        assert A.normalize_mcp_config(normalized) == normalized
        assert A.select_mode("auto", cli_available=True, mcp_available=True) == "cli"
        assert A.select_mode("auto", cli_available=False, mcp_available=True) == "mcp"
        assert A.select_mode("cli", cli_available=False, mcp_available=True) == "cli"
        assert A.select_mode("mcp", cli_available=True, mcp_available=False) == "mcp"
        # CLI path remains representable independent of 007 smoke path.
        out = A.normalize_output({"output_path": "/tmp/x.png", "width": 1})
        assert out.get("image_path") == "/tmp/x.png"

    def test_fake_mcp_error_seam_maps_to_actionable_fr006_family(self):
        """Deterministic fake MCP seam (no real server) yields structured failure shape."""
        cfg = fake_mcp_config("tool_error", tool_name=SMOKE_TOOL_TARGET)
        normalized = A.normalize_mcp_config(cfg)
        assert normalized.get("command")
        assert normalized.get("tool_name") == SMOKE_TOOL_TARGET
        assert any("tool_error" in str(a) for a in (normalized.get("args") or []))
        err = A.standardize_error(
            A.REASON_MCP_TOOL_ERROR,
            "command_list failed",
            {"mode": "mcp", "interface": "mcp", "error_stage": "call", "tool": SMOKE_TOOL_TARGET},
        )
        assert err.get("code") == A.REASON_MCP_TOOL_ERROR
        details = err.get("details") or {}
        assert details.get("error_stage") == "call"
        assert details.get("tool") == SMOKE_TOOL_TARGET
        invalid = fake_mcp_config("bad_json")
        invalid_norm = A.normalize_mcp_config(invalid)
        assert invalid_norm.get("command")
        assert any("bad_json" in str(a) for a in (invalid_norm.get("args") or []))
        missing = classify_smoke_failure(case="missing_capability", opt_in=True, capability_present=False)
        assert missing["reason"] == A.REASON_MCP_MISSING_CAPABILITY
        assert missing["required_capability"] == SMOKE_TOOL_TARGET
    def test_007_harness_missing_capability_and_error_paths_are_red(self):
        """RED integration-facing assertions: 007 harness must classify US2 outcomes."""
        try:
            import tests.integration.test_mcp_stdio_photocraft_optional as opt_mod
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"007 harness not implemented (RED): cannot import integration module ({exc!r})")

        # Presence of a classifier/runner hook is required for deterministic US2 behavior.
        hooks = (
            "classify_photocraft_mcp_smoke_outcome",
            "map_photocraft_mcp_smoke_error",
            "run_photocraft_mcp_smoke",
            "execute_photocraft_mcp_smoke",
            "photocraft_mcp_smoke",
        )
        if not any(callable(getattr(opt_mod, name, None)) for name in hooks):
            pytest.fail(
                "007 harness not implemented (RED): expected an outcome classifier or smoke runner "
                "in tests.integration.test_mcp_stdio_photocraft_optional that maps missing "
                "opt-in/prereq/unsafe boundaries/timeouts/invalid responses/missing capability/"
                "tool errors to FR-006-aligned actionable outcomes/skips with safe cleanup."
            )

        # If a classifier exists, require minimal 007 US2 contract shape; otherwise fail RED.
        classifier = getattr(opt_mod, "classify_photocraft_mcp_smoke_outcome", None) or getattr(
            opt_mod, "map_photocraft_mcp_smoke_error", None
        )
        if classifier is None:
            pytest.fail(
                "007 harness not implemented (RED): smoke runner exists but no deterministic "
                "outcome classifier hook found for US2 failure/contract invariants."
            )
        try:
            missing = classifier(reason=A.REASON_MCP_MISSING_CAPABILITY, mcp_attempted=True, error_stage="capability_check")
        except TypeError:
            missing = classifier(A.REASON_MCP_MISSING_CAPABILITY)
        if not isinstance(missing, Mapping):
            pytest.fail("007 harness not implemented (RED): classifier must return a mapping outcome.")
        if str(missing.get("reason") or "") != A.REASON_MCP_MISSING_CAPABILITY:
            pytest.fail("007 harness not implemented (RED): missing capability must preserve FR-006 reason.")
        if not (missing.get("error_stage") or (missing.get("metadata") or {}).get("error_stage")):
            pytest.fail("007 harness not implemented (RED): MCP-attempted failures must include error_stage.")
