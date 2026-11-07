"""Contract tests for the shared ArtCraft app client adapter.

Verifies importability, presence of the full public API (9 functions plus
``__version__``/``__all__``), and a zero-diff comparison against the
committed snapshot ``tests/contract/artcraft_app_client_api.json``.
"""
import inspect
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import skills.core.artcraft_app_client as adapter

SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "artcraft_app_client_api.json")
EXPECTED_FUNCTIONS = [
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
    # 006 MCP stdio additive API
    "mcp_tools_list",
    "mcp_tools_call",
    "mcp_stateful_session",
    "MCPStatefulSession",
]


def _load_snapshot():
    with open(SNAPSHOT_PATH) as fh:
        return json.load(fh)


def test_module_importable():
    """The adapter module must be importable from skills.core."""
    import skills.core.artcraft_app_client as m

    assert m is not None
    assert m.__name__ == "skills.core.artcraft_app_client"


def test_all_expected_functions_present():
    """All expected public functions must exist and be callable."""
    for name in EXPECTED_FUNCTIONS:
        assert hasattr(adapter, name), f"missing function: {name}"
        assert callable(getattr(adapter, name)), f"not callable: {name}"


def test_function_count_at_least_expected():
    """Adapter exposes at least the expected documented functions."""
    present = [n for n in EXPECTED_FUNCTIONS if hasattr(adapter, n) and callable(getattr(adapter, n))]
    assert len(present) >= len(EXPECTED_FUNCTIONS)


def test_version_present_and_matches_snapshot():
    """__version__ must exist and match the committed snapshot."""
    snap = _load_snapshot()
    assert hasattr(adapter, "__version__")
    assert adapter.__version__ == snap["__version__"]


def test_all_present_and_matches_snapshot():
    """__all__ must exist and match the committed snapshot exactly."""
    snap = _load_snapshot()
    assert hasattr(adapter, "__all__")
    assert list(adapter.__all__) == list(snap["__all__"])


def test_parameter_names_match_snapshot():
    """Each function's parameter names must match the snapshot."""
    snap = _load_snapshot()
    for name, spec in snap["functions"].items():
        assert hasattr(adapter, name), f"missing function: {name}"
        sig = inspect.signature(getattr(adapter, name))
        actual = list(sig.parameters.keys())
        expected = [p["name"] for p in spec["params"]]
        assert actual == expected, f"{name}: params {actual} != {expected}"


def test_parameter_annotations_match_snapshot():
    """Each parameter annotation must match the snapshot's string form."""
    snap = _load_snapshot()
    for name, spec in snap["functions"].items():
        if not hasattr(adapter, name):
            continue
        sig = inspect.signature(getattr(adapter, name))
        for param_spec in spec["params"]:
            pname = param_spec["name"]
            actual = str(sig.parameters[pname].annotation)
            expected = param_spec["annotation"]
            assert actual == expected, (
                f"{name}.{pname}: annotation {actual!r} != {expected!r}"
            )


def test_return_annotations_match_snapshot():
    """Each function's return annotation must match the snapshot."""
    snap = _load_snapshot()
    for name, spec in snap["functions"].items():
        if not hasattr(adapter, name):
            continue
        sig = inspect.signature(getattr(adapter, name))
        actual = str(sig.return_annotation)
        expected = spec["return"]
        assert actual == expected, f"{name}: return {actual!r} != {expected!r}"


def test_concrete_defaults_match_snapshot():
    """Non-null snapshot defaults must be reproduced exactly."""
    snap = _load_snapshot()
    for name, spec in snap["functions"].items():
        if not hasattr(adapter, name):
            continue
        sig = inspect.signature(getattr(adapter, name))
        for param_spec in spec["params"]:
            pname = param_spec["name"]
            expected_default = param_spec["default"]
            if expected_default is None:
                continue
            actual_default = sig.parameters[pname].default
            # JSON snapshot cannot represent tuples; accept tuple/list equivalence.
            if isinstance(actual_default, tuple) and isinstance(expected_default, list):
                actual_cmp, expected_cmp = list(actual_default), expected_default
            elif isinstance(actual_default, tuple) and isinstance(expected_default, str):
                actual_cmp, expected_cmp = repr(actual_default), expected_default
            else:
                actual_cmp, expected_cmp = actual_default, expected_default
            assert actual_cmp == expected_cmp, (
                f"{name}.{pname}: default {actual_default!r} != {expected_default!r}"
            )


def test_snapshot_diff_zero():
    """Full structural diff against the committed snapshot must be empty."""
    snap = _load_snapshot()

    # Version / __all__ diff
    diffs = []
    if getattr(adapter, "__version__", None) != snap.get("__version__"):
        diffs.append(f"__version__: {getattr(adapter, '__version__', None)!r} != {snap.get('__version__')!r}")
    if list(getattr(adapter, "__all__", [])) != list(snap.get("__all__", [])):
        diffs.append(f"__all__: {getattr(adapter, '__all__', None)!r} != {snap.get('__all__')!r}")

    # Function set diff
    snap_funcs = set(snap.get("functions", {}).keys())
    actual_funcs = set(n for n in EXPECTED_FUNCTIONS if hasattr(adapter, n))
    if snap_funcs != actual_funcs:
        diffs.append(f"function set diff: missing={snap_funcs - actual_funcs}, extra={actual_funcs - snap_funcs}")

    # Per-function signature diff
    for name, spec in snap.get("functions", {}).items():
        if not hasattr(adapter, name):
            diffs.append(f"{name}: missing from module")
            continue
        sig = inspect.signature(getattr(adapter, name))
        actual_params = list(sig.parameters.keys())
        expected_params = [p["name"] for p in spec["params"]]
        if actual_params != expected_params:
            diffs.append(f"{name}: params {actual_params} != {expected_params}")
        for param_spec in spec["params"]:
            pname = param_spec["name"]
            if pname not in sig.parameters:
                continue
            if str(sig.parameters[pname].annotation) != param_spec["annotation"]:
                diffs.append(
                    f"{name}.{pname}: annotation {str(sig.parameters[pname].annotation)!r} "
                    f"!= {param_spec['annotation']!r}"
                )
        if str(sig.return_annotation) != spec["return"]:
            diffs.append(f"{name}: return {str(sig.return_annotation)!r} != {spec['return']!r}")

    assert not diffs, "Unreviewed API diff:\n" + "\n".join(diffs)
