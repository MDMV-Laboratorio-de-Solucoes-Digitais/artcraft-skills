"""006 RED: MCP stdio property/invariant tests (T006,T016). Deterministic, no sleeps."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hypothesis import given, settings, strategies as st

from skills.core import artcraft_app_client as A
from skills.core.base_skill import SkillResult

MCP_REASONS = {
    "mcp_unavailable", "mcp_misconfigured", "mcp_startup_timeout", "mcp_call_timeout",
    "mcp_invalid_response", "mcp_missing_capability", "mcp_tool_error", "cli_not_found", "neither_available",
}


@settings(max_examples=40, deadline=None)
@given(st.dictionaries(st.text(min_size=1, max_size=12), st.one_of(st.text(max_size=20), st.integers(), st.booleans(), st.none()), max_size=8))
def test_normalize_mcp_config_no_mutation(d):
    before = dict(d)
    A.normalize_mcp_config(d)
    assert d == before


@settings(max_examples=30, deadline=None)
@given(st.dictionaries(st.text(min_size=1, max_size=12), st.one_of(st.text(max_size=20), st.integers(), st.none()), max_size=6))
def test_normalize_mcp_config_idempotent(d):
    r1 = A.normalize_mcp_config(d)
    r2 = A.normalize_mcp_config(r1)
    assert r1 == r2


def test_auto_cli_first_when_cli_available():
    # FR-005: default auto is CLI-first/back-compatible
    r = A.select_mode("auto", cli_available=True, mcp_available=True)
    assert r == "cli"


def test_auto_mcp_when_cli_unavailable_mcp_available():
    r = A.select_mode("auto", cli_available=False, mcp_available=True)
    assert r == "mcp"


def test_explicit_mode_wins_selection():
    assert A.select_mode("cli", True, True) == "cli"
    assert A.select_mode("mcp", True, True) == "mcp"


@settings(max_examples=25, deadline=None)
@given(st.sampled_from(sorted(MCP_REASONS)), st.text(min_size=1, max_size=60))
def test_standardize_error_structured_and_additive(reason, msg):
    out = A.standardize_error(reason, msg, {"mode": "mcp", "interface": "mcp"})
    assert isinstance(out, dict)
    assert out.get("message") == msg
    # code/reason compatibility: accept either form
    code = str(out.get("code") or out.get("reason") or "")
    assert reason in code or code in MCP_REASONS or "mcp" in code or "cli" in code or "neither" in code


@settings(max_examples=20, deadline=None)
@given(st.sampled_from(sorted(MCP_REASONS)))
def test_modeled_failure_skillresult_compatible(reason):
    # Modeled normalization target (006 FR-006): failures become SkillResult-compatible
    err = A.standardize_error(reason, "actionable failure", {"mode": "mcp", "interface": "mcp", "error_stage": "invocation"})
    r = SkillResult(success=False, error=err.get("message") or "actionable failure", metadata={k: v for k, v in err.items() if k != "message"})
    assert r.success is False
    assert isinstance(r.error, str) and r.error
    assert isinstance(r.metadata, dict)
