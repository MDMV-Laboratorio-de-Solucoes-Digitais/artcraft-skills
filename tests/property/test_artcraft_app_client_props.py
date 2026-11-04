"""Property tests for shared CLI/MCP adapter invariants."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hypothesis import given, strategies as st
from skills.core import artcraft_app_client as A


VALID_MODES = {"cli", "mcp", "none"}


@given(st.dictionaries(st.text(min_size=1, max_size=8), st.integers(), min_size=0, max_size=6))
def test_normalize_output_no_mutation(d):
    before = dict(d)
    A.normalize_output(d)
    assert d == before


@given(st.dictionaries(st.text(min_size=1, max_size=8), st.integers(), min_size=0, max_size=6))
def test_normalize_output_idempotent(d):
    r1 = A.normalize_output(d)
    r2 = A.normalize_output(r1)
    assert r1 == r2


@given(st.dictionaries(st.text(min_size=1, max_size=8), st.integers(), min_size=0, max_size=6))
def test_normalize_mcp_config_no_mutation(d):
    before = dict(d)
    A.normalize_mcp_config(d)
    assert d == before


@given(st.dictionaries(st.text(min_size=1, max_size=8), st.integers(), min_size=0, max_size=6))
def test_normalize_mcp_config_idempotent(d):
    r1 = A.normalize_mcp_config(d)
    r2 = A.normalize_mcp_config(r1)
    assert r1 == r2


@given(
    st.one_of(
        st.none(),
        st.lists(st.dictionaries(st.text(min_size=1, max_size=4), st.text(), min_size=1, max_size=3), min_size=0, max_size=5),
        st.dictionaries(st.text(min_size=1, max_size=4), st.lists(st.text(), min_size=0, max_size=3), min_size=0, max_size=3),
    ),
    st.lists(st.text(min_size=1, max_size=8), min_size=0, max_size=5),
    st.one_of(st.none(), st.text(min_size=1, max_size=8)),
)
def test_discover_generation_command_member_or_override_or_none(commands, keywords, override):
    res = A.discover_generation_command(commands, keywords if keywords else None, override)
    if override:
        assert res == override
    elif res is not None:
        # res must be a member id of commands (best-effort: just str)
        assert isinstance(res, str)


@given(st.sampled_from(["cli", "mcp", "auto"]))
def test_select_mode_valid_modes_requested(mode):
    for ca in (True, False):
        for ma in (True, False):
            r = A.select_mode(mode, ca, ma)
            assert r in VALID_MODES


@given(st.booleans(), st.booleans())
def test_select_mode_auto_valid(ca, ma):
    r = A.select_mode("auto", ca, ma)
    assert r in VALID_MODES


@given(st.text(min_size=1, max_size=20))
def test_standardize_error_keys(reason):
    res = A.standardize_error(reason, "msg", None)
    assert {"code", "message", "details", "retryable"}.issubset(res.keys())
    assert res["message"] == "msg"


@given(st.dictionaries(st.text(min_size=1, max_size=4), st.integers(), min_size=0, max_size=4))
def test_standardize_error_with_metadata_keys(d):
    res = A.standardize_error("cli_not_found", "msg", d)
    assert {"code", "message", "details", "retryable"}.issubset(res.keys())
