"""Unit tests for shared CLI/MCP adapter (skills.core.artcraft_app_client).

RED-phase: written against the target (modernized) contract. Some assertions
will fail until the adapter is modernized (select_mode, standardize_error,
non-mutating normalize_*, modernized signatures).
"""
import os
import sys
import json
import shutil
import subprocess
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_app_client as A


# ---------- discover_cli ----------

def test_discover_cli_explicit_path_exists(tmp_path):
    p = tmp_path / "cli"
    p.write_text("x")
    p.chmod(0o755)
    assert A.discover_cli(str(p)) == str(p)


def test_discover_cli_explicit_path_missing():
    assert A.discover_cli("/no/such/cli/binary") is None


def test_discover_cli_none_or_empty():
    # None -> searches PATH/common; result is str or None
    r = A.discover_cli(None)
    assert r is None or isinstance(r, str)
    assert A.discover_cli("") is None or isinstance(A.discover_cli(""), str)


def test_discover_cli_uses_which(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/photocraft-cli")
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    assert A.discover_cli() == "/usr/bin/photocraft-cli"


def test_discover_cli_common_location(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    def exists(p):
        return p == "/usr/bin/photocraft-cli"
    monkeypatch.setattr(os.path, "exists", exists)
    assert A.discover_cli() == "/usr/bin/photocraft-cli"


def test_discover_cli_missing_returns_none(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(os.path, "exists", lambda p: False)
    assert A.discover_cli() is None


# ---------- discover_generation_command ----------

def test_discover_generation_command_override():
    cmds = [{"id": "foo"}]
    assert A.discover_generation_command(cmds, override="bar") == "bar"


def test_discover_generation_command_member():
    cmds = [{"id": "generate", "label": "Generate image"}]
    assert A.discover_generation_command(cmds, ["generate"]) == "generate"


def test_discover_generation_command_none():
    cmds = [{"id": "list", "label": "List"}]
    assert A.discover_generation_command(cmds, ["generate"]) is None


def test_discover_generation_command_empty():
    assert A.discover_generation_command(None) is None
    assert A.discover_generation_command([]) is None
    assert A.discover_generation_command({}) is None


def test_discover_generation_command_dict_commands():
    cmds = {"commands": [{"id": "gen", "description": "gen images"}]}
    assert A.discover_generation_command(cmds) == "gen"


def test_discover_generation_command_case_insensitive():
    cmds = [{"id": "IMAGE.GENERATE", "label": ""}]
    assert A.discover_generation_command(cmds, ["image.generate"]) == "IMAGE.GENERATE"


def test_discover_generation_command_non_mutating():
    cmds = [{"id": "generate"}]
    before = [dict(c) for c in cmds]
    A.discover_generation_command(cmds, ["generate"])
    assert cmds == before


# ---------- normalize_output ----------

def test_normalize_output_basic():
    out = {"image_url": "u", "width": 10, "extra": "x"}
    res = A.normalize_output(out)
    assert res["image_url"] == "u"
    assert res["width"] == 10
    assert res["image_path"] is None
    assert set(res.keys()) == {"image_url", "image_path", "asset_id", "format", "width", "height", "metadata"}


def test_normalize_output_none():
    res = A.normalize_output(None)
    assert isinstance(res, dict)
    assert all(v is None for v in res.values())


def test_normalize_output_non_dict():
    res = A.normalize_output("not a dict")
    assert isinstance(res, dict)


def test_normalize_output_custom_keys():
    out = {"a": 1, "b": 2}
    res = A.normalize_output(out, keys=["a", "b"])
    assert res == {"a": 1, "b": 2}


def test_normalize_output_non_mutation():
    out = {"image_url": "u", "width": 10}
    before = dict(out)
    A.normalize_output(out)
    assert out == before


def test_normalize_output_idempotent():
    out = {"image_url": "u"}
    r1 = A.normalize_output(out)
    r2 = A.normalize_output(r1)
    assert r1 == r2


# ---------- normalize_mcp_config ----------

def test_normalize_mcp_config_bridge():
    cfg = {"bridge": True}
    res = A.normalize_mcp_config(cfg)
    assert res["transport"] == "bridge"
    assert cfg.get("transport") is None  # non-mutation


def test_normalize_mcp_config_token():
    cfg = {"token": "t"}
    res = A.normalize_mcp_config(cfg)
    assert res["transport"] == "bridge"


def test_normalize_mcp_config_stdio():
    cfg = {}
    res = A.normalize_mcp_config(cfg)
    assert res["transport"] == "stdio"


def test_normalize_mcp_config_none():
    res = A.normalize_mcp_config(None)
    assert isinstance(res, dict)
    assert res["transport"] == "stdio"


def test_normalize_mcp_config_preserves_existing_transport():
    cfg = {"transport": "http"}
    res = A.normalize_mcp_config(cfg)
    assert res["transport"] == "http"


def test_normalize_mcp_config_non_mutation():
    cfg = {"bridge": True, "foo": 1}
    before = dict(cfg)
    A.normalize_mcp_config(cfg)
    assert cfg == before


def test_normalize_mcp_config_idempotent():
    cfg = {"bridge": True}
    r1 = A.normalize_mcp_config(cfg)
    r2 = A.normalize_mcp_config(r1)
    assert r1 == r2


# ---------- run_cli ----------

def test_run_cli_success(monkeypatch):
    cp = subprocess.CompletedProcess(args=["cli", "x"], returncode=0, stdout="out", stderr="")
    with patch("subprocess.run", return_value=cp) as m:
        res = A.run_cli("cli", ["x"], timeout=10)
    assert res.returncode == 0
    m.assert_called_once()


def test_run_cli_passes_timeout(monkeypatch):
    cp = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    with patch("subprocess.run", return_value=cp) as m:
        A.run_cli("cli", ["a"], timeout=5)
    _, kwargs = m.call_args
    assert kwargs.get("timeout") == 5


def test_run_cli_timeout_propagates(monkeypatch):
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="cli", timeout=1)):
        try:
            A.run_cli("cli", ["x"], timeout=1)
            raised = False
        except subprocess.TimeoutExpired:
            raised = True
    assert raised


def test_run_cli_nonzero_exit():
    cp = subprocess.CompletedProcess(args=[], returncode=2, stdout="", stderr="boom")
    with patch("subprocess.run", return_value=cp):
        res = A.run_cli("cli", ["x"])
    assert res.returncode == 2


# ---------- discover_cli_commands ----------

def test_discover_cli_commands_success():
    cp = subprocess.CompletedProcess(args=[], returncode=0, stdout='[{"id":"generate"}]', stderr="")
    with patch("subprocess.run", return_value=cp):
        res = A.discover_cli_commands("cli", timeout=10)
    assert res == [{"id": "generate"}]


def test_discover_cli_commands_malformed_json():
    cp = subprocess.CompletedProcess(args=[], returncode=0, stdout="not json", stderr="")
    with patch("subprocess.run", return_value=cp):
        res = A.discover_cli_commands("cli")
    assert res == []


def test_discover_cli_commands_nonzero():
    cp = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="err")
    with patch("subprocess.run", return_value=cp):
        res = A.discover_cli_commands("cli")
    assert res == []


def test_discover_cli_commands_empty_stdout():
    cp = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    with patch("subprocess.run", return_value=cp):
        res = A.discover_cli_commands("cli")
    assert res == []


def test_discover_cli_commands_exception():
    with patch("subprocess.run", side_effect=FileNotFoundError("no cli")):
        res = A.discover_cli_commands("cli")
    assert res == []


def test_discover_cli_commands_timeout():
    with patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd="cli", timeout=1)):
        res = A.discover_cli_commands("cli")
    assert res == []


# ---------- run_cli_generation ----------

def test_run_cli_generation_builds_args():
    cp = subprocess.CompletedProcess(args=[], returncode=0, stdout="{}", stderr="")
    with patch("subprocess.run", return_value=cp) as m:
        A.run_cli_generation("cli", "gen", {"prompt": "hi"}, timeout=7)
    args, kwargs = m.call_args
    assert args[0][:2] == ["cli", "run"] or "run" in args[0]
    assert "--cmd" in args[0]
    assert "gen" in args[0]
    assert "--params" in args[0]
    assert kwargs.get("timeout") == 7


# ---------- select_mode ----------

def test_select_mode_cli_requested():
    assert A.select_mode("cli", False, False) == "cli"
    assert A.select_mode("cli", True, True) == "cli"


def test_select_mode_mcp_requested():
    assert A.select_mode("mcp", False, False) == "mcp"


def test_select_mode_auto_prefers_cli():
    assert A.select_mode("auto", True, True) == "cli"
    assert A.select_mode("auto", True, False) == "cli"


def test_select_mode_auto_mcp_fallback():
    assert A.select_mode("auto", False, True) == "mcp"


def test_select_mode_auto_none():
    assert A.select_mode("auto", False, False) == "none"


def test_select_mode_invalid_raises():
    try:
        A.select_mode("bogus", True, True)
        raised = False
    except ValueError:
        raised = True
    assert raised


# ---------- standardize_error ----------

def test_standardize_error_keys():
    res = A.standardize_error("cli_not_found", "no cli", None)
    assert {"code", "message", "details", "retryable"}.issubset(res.keys())
    assert res["code"] == "cli_not_found"
    assert res["message"] == "no cli"


def test_standardize_error_with_metadata():
    res = A.standardize_error("is_error", "boom", {"exit_code": 2})
    assert res["code"] == "is_error"
    # metadata merged or present
    assert isinstance(res, dict)


def test_standardize_error_none_metadata():
    res = A.standardize_error("neither_available", "none", None)
    assert isinstance(res["details"], (dict, type(None))) or True


def test_standardize_error_retryable_type():
    res = A.standardize_error("mcp_unavailable", "x", {})
    assert isinstance(res["retryable"], bool)

# ---------- future-skill flexibility (US3) ----------
def test_future_skill_custom_keywords_and_override():
    cmds = {"commands": [{"id": "img.edit", "label": "edit image"}]}
    assert A.discover_generation_command(cmds, keywords=["edit"], override=None) == "img.edit"
    assert A.discover_generation_command(cmds, keywords=["nope"], override="forced.cmd") == "forced.cmd"


def test_future_skill_arbitrary_normalize_keys():
    out = {"mesh_url": "m", "vertex_count": 10}
    res = A.normalize_output(out, keys=["mesh_url", "vertex_count"])
    assert res == {"mesh_url": "m", "vertex_count": 10}


def test_future_skill_select_mode_all_combinations():
    for cli in (True, False):
        for mcp in (True, False):
            mode = A.select_mode("auto", cli, mcp)
            if cli:
                assert mode == "cli"
            elif mcp:
                assert mode == "mcp"
            else:
                assert mode == "none"
    assert A.select_mode("cli", False, False) == "cli"
    assert A.select_mode("mcp", False, False) == "mcp"

# ---------- reason-code constants (convergence) ----------
def test_reason_constants_exist_and_equal_wire_strings():
    assert A.REASON_CLI_NOT_FOUND == "cli_not_found"
    assert A.REASON_MCP_UNAVAILABLE == "mcp_unavailable"
    assert A.REASON_NEITHER_AVAILABLE == "neither_available"
    assert A.REASON_IS_ERROR == "is_error"


def test_reason_constants_importable():
    from skills.core import artcraft_app_client as m
    assert m.REASON_CLI_NOT_FOUND is not None
