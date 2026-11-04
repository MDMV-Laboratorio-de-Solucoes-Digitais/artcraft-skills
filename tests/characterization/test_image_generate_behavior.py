import os, sys, json, subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import pytest
from skills.core.base_skill import SkillResult
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "creative", "image-generate")))
import skill as _ig_skill
ImageGenerateSkill = _ig_skill.ImageGenerateSkill
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_helpers')))
from canonicalize import canonicalize_skill_result

GOLDEN_DIR = os.path.join(os.path.dirname(__file__), '..', 'golden', 'image_generate')


def _canon(res):
    return canonicalize_skill_result(res)


def _run_cli_success(monkeypatch, inputs, cmds=None, stdout=None, rc=0, timeout_exc=False):
    s = ImageGenerateSkill()
    cli = "/bin/photocraft-cli"
    s._discover_cli = lambda x=None: cli
    if cmds is None:
        cmds = {"commands": [{"id": "generate", "label": "generate"}]}
    if stdout is None:
        stdout = {"image_path": "/tmp/img.png", "width": 64}

    def fake_run(args, *a, **k):
        if len(args) > 1 and args[1] == "commands":
            return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
        if timeout_exc:
            raise subprocess.TimeoutExpired(cmd=args, timeout=300)
        if rc != 0:
            return subprocess.CompletedProcess(args, rc, "", "boom")
        return subprocess.CompletedProcess(args, 0, json.dumps(stdout), "")

    monkeypatch.setattr("subprocess.run", fake_run)
    return s, inputs


SCENARIOS = [
    "cli_success",
    "cli_nonzero_exit",
    "cli_timeout",
    "missing_cli",
    "command_discovery_keyword",
    "command_discovery_override",
    "command_discovery_none",
    "output_normalization_missing_fields",
    "mcp_unavailable",
    "mcp_tool_error",
    "mcp_success",
    "auto_prefers_cli",
    "cli_mode",
    "mcp_mode",
    "neither_available",
    "invalid_inputs",
]


def run_scenario(name, monkeypatch):
    if name == "cli_success":
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"})
        return s.execute({**inp, "mode": "cli"})
    if name == "cli_nonzero_exit":
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, rc=1)
        return s._execute_cli({"prompt": "cat"}, "/bin/cli", "cli")
    if name == "cli_timeout":
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, timeout_exc=True)
        return s._execute_cli({"prompt": "cat"}, "/bin/cli", "cli")
    if name == "missing_cli":
        s = ImageGenerateSkill()
        s._discover_cli = lambda x=None: None
        return s.execute({"prompt": "x", "mode": "cli"})
    if name == "command_discovery_keyword":
        cmds = {"commands": [{"id": "foo", "label": "bar"}, {"id": "img.gen", "label": "generate image"}]}
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, cmds=cmds, stdout={"image_path": "/y.png"})
        # keyword match via command_keywords
        return s._execute_cli({"prompt": "cat", "command_keywords": ["generate"]}, "/bin/cli", "cli")
    if name == "command_discovery_override":
        cmds = {"commands": [{"id": "foo", "label": "bar"}]}
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, cmds=cmds, stdout={"image_path": "/z.png"})
        return s._execute_cli({"prompt": "cat", "generation_command": "forced"}, "/bin/cli", "cli")
    if name == "command_discovery_none":
        cmds = {"commands": [{"id": "foo", "label": "bar"}]}
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, cmds=cmds)
        return s._execute_cli({"prompt": "cat"}, "/bin/cli", "cli")
    if name == "output_normalization_missing_fields":
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"}, stdout={"image_path": "/x.png"})
        return s._execute_cli({"prompt": "cat"}, "/bin/cli", "cli")
    if name == "mcp_unavailable":
        s = ImageGenerateSkill()
        s._mcp_available = lambda cfg: False
        return s.execute({"prompt": "x", "mode": "mcp"})
    if name == "mcp_tool_error":
        s = ImageGenerateSkill()
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"is_error": True, "error": "bad tool"}
        return s.execute({"prompt": "x", "mode": "mcp"})
    if name == "mcp_success":
        s = ImageGenerateSkill()
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"image_path": "/m.png", "width": 10}
        return s.execute({"prompt": "x", "mode": "mcp"})
    if name == "auto_prefers_cli":
        s = ImageGenerateSkill()
        s._discover_cli = lambda x=None: "/bin/cli"
        cmds = {"commands": [{"id": "generate", "label": "generate"}]}

        def fake_run(args, *a, **k):
            if len(args) > 1 and args[1] == "commands":
                return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
            return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/y.png"}), "")
        monkeypatch.setattr("subprocess.run", fake_run)
        return s.execute({"prompt": "x", "mode": "auto"})
    if name == "cli_mode":
        s, inp = _run_cli_success(monkeypatch, {"prompt": "cat"})
        return s.execute({**inp, "mode": "cli"})
    if name == "mcp_mode":
        s = ImageGenerateSkill()
        s._mcp_available = lambda cfg: True
        s._mcp_command_list = lambda cfg: [{"id": "generate", "label": "generate"}]
        s._mcp_command_run = lambda cfg, tid, params, timeout: {"image_path": "/m.png"}
        return s.execute({"prompt": "x", "mode": "mcp"})
    if name == "neither_available":
        s = ImageGenerateSkill()
        s._discover_cli = lambda x=None: None
        s._mcp_available = lambda cfg: False
        return s.execute({"prompt": "x", "mode": "auto"})
    if name == "invalid_inputs":
        s = ImageGenerateSkill()
        return s.execute({})
    raise ValueError(name)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_image_generate_behavior(scenario, monkeypatch, update_golden):
    res = run_scenario(scenario, monkeypatch)
    canon = _canon(res)
    os.makedirs(GOLDEN_DIR, exist_ok=True)
    path = os.path.join(GOLDEN_DIR, f"{scenario}.json")
    if update_golden:
        with open(path, "w") as f:
            json.dump(canon, f, indent=2, sort_keys=True)
        return
    if not os.path.exists(path):
        pytest.fail(f"Missing golden file: {path} (run with --update-golden)")
    with open(path) as f:
        expected = json.load(f)
    assert canon == expected