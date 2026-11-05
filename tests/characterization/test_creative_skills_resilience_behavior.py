import os, sys, json, subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from skills.core.base_skill import SkillResult

import importlib.util

def _load_skill(name, class_name):
    path = f'/home/luis/development/artcraft-skills/skills/creative/{name}/skill.py'
    spec = importlib.util.spec_from_file_location(f'skill_{name.replace("-", "_")}_res_char', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f'skill_{name.replace("-", "_")}_res_char'] = mod
    spec.loader.exec_module(mod)
    return getattr(mod, class_name)


SKILLS = [
    (_load_skill('image-edit', 'ImageEditSkill'), {"image": "/x.png", "prompt": "make blue"}),
    (_load_skill('background-remove', 'BackgroundRemoveSkill'), {"image": "/x.png"}),
    (_load_skill('image-upscale', 'ImageUpscaleSkill'), {"image": "/x.png", "scale": 2}),
    (_load_skill('mesh-generate', 'MeshGenerateSkill'), {"prompt": "a tree"}),
]


@pytest.mark.parametrize("idx", [0, 1, 2, 3])
def test_creative_skill_timeout_retries_or_fails_gracefully(idx, monkeypatch):
    cls, base = SKILLS[idx]
    s = cls()
    cli = "/bin/photocraft-cli"
    s._discover_cli = lambda x=None: cli
    cmds = {"commands": [{"id": "doit", "label": "do something"}]}
    
    call_count = [0]
    def fake_run(args, *a, **k):
        if len(args) > 1 and args[1] == "commands":
            return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
        call_count[0] += 1
        raise subprocess.TimeoutExpired(cmd=args, timeout=300)
    
    monkeypatch.setattr("subprocess.run", fake_run)
    res = s._execute_cli(base, cli, "cli")
    assert isinstance(res, SkillResult)
    assert res.success is False
    # After implementation, should retry up to 3 times
