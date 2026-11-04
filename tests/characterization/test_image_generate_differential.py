"""Differential test: pre-refactor reference vs current image-generate skill."""

import json
import subprocess
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_helpers')))
from canonicalize import canonicalize_skill_result
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reference')))
from image_generate_original import ImageGenerateSkill as OriginalSkill
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "creative", "image-generate")))
import skill as _ig_skill
RefactoredSkill = _ig_skill.ImageGenerateSkill


SCENARIOS = [
    "cli_success",
    "cli_nonzero_exit",
    "cli_timeout",
    "cli_missing",
    "cli_unsupported_command",
    "cli_keyword_discovery",
    "cli_override_command",
    "cli_output_minimal",
    "mcp_unavailable",
    "mcp_tool_error",
    "mcp_success",
    "auto_prefers_cli",
    "cli_mode",
    "mcp_mode",
    "neither_available",
    "invalid_inputs",
]


def _cmds():
    return {"commands": [{"id": "generate", "label": "generate image"}]}


def _configure(skill_cls, scenario, monkeypatch):
    s = skill_cls()

    if scenario == "cli_success":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/tmp/img.png", "width": 64}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli"}

    elif scenario == "cli_nonzero_exit":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 1, "", "boom")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli"}

    elif scenario == "cli_timeout":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            raise subprocess.TimeoutExpired(cmd=args, timeout=300)

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli"}

    elif scenario == "cli_missing":
        s._discover_cli = lambda x=None: None
        inputs = {"prompt": "x", "mode": "cli"}

    elif scenario == "cli_unsupported_command":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = {"commands": [{"id": "foo", "label": "bar"}]}

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, "{}", "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli"}

    elif scenario == "cli_keyword_discovery":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = {"commands": [{"id": "img.gen", "label": "generate image"}]}

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/k.png"}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli", "command_keywords": ["generate"]}

    elif scenario == "cli_override_command":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = {"commands": [{"id": "foo", "label": "bar"}]}

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/o.png"}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli", "generation_command": "forced"}

    elif scenario == "cli_output_minimal":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/m.png"}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "cat", "mode": "cli"}

    elif scenario == "mcp_unavailable":
        s._mcp_available = lambda cfg: False
        inputs = {"prompt": "x", "mode": "mcp"}

    elif scenario == "mcp_tool_error":
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"is_error": True, "error": "bad tool"}
        inputs = {"prompt": "x", "mode": "mcp"}

    elif scenario == "mcp_success":
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"image_path": "/mcp.png"}
        inputs = {"prompt": "x", "mode": "mcp"}

    elif scenario == "auto_prefers_cli":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/y.png"}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        s._mcp_available = lambda cfg: False
        inputs = {"prompt": "x", "mode": "auto"}

    elif scenario == "cli_mode":
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = _cmds()

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/c.png"}), "")

        monkeypatch.setattr("subprocess.run", fake_run)
        inputs = {"prompt": "x", "mode": "cli"}

    elif scenario == "mcp_mode":
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"image_path": "/m.png"}
        inputs = {"prompt": "x", "mode": "mcp"}

    elif scenario == "neither_available":
        s._discover_cli = lambda x=None: None
        s._mcp_available = lambda cfg: False
        inputs = {"prompt": "x", "mode": "auto"}

    elif scenario == "invalid_inputs":
        inputs = {}

    else:
        raise ValueError(scenario)

    return s, inputs


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_differential(scenario, monkeypatch):
    orig_skill, orig_inputs = _configure(OriginalSkill, scenario, monkeypatch)
    ref_skill, ref_inputs = _configure(RefactoredSkill, scenario, monkeypatch)
    r1 = orig_skill.execute(orig_inputs)
    r2 = ref_skill.execute(ref_inputs)
    assert canonicalize_skill_result(r1) == canonicalize_skill_result(r2)
