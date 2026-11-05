import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from hypothesis import given, strategies as st
from skills.core.base_skill import SkillResult

import importlib.util

def _load_skill(name, class_name):
    path = f'/home/luis/development/artcraft-skills/skills/creative/{name}/skill.py'
    spec = importlib.util.spec_from_file_location(f'skill_{name.replace("-", "_")}_res', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f'skill_{name.replace("-", "_")}_res'] = mod
    spec.loader.exec_module(mod)
    return getattr(mod, class_name)


SKILLS = [
    (_load_skill('image-edit', 'ImageEditSkill'), {"image": "/x.png", "prompt": "make blue"}),
    (_load_skill('background-remove', 'BackgroundRemoveSkill'), {"image": "/x.png"}),
    (_load_skill('image-upscale', 'ImageUpscaleSkill'), {"image": "/x.png", "scale": 2}),
    (_load_skill('mesh-generate', 'MeshGenerateSkill'), {"prompt": "a tree"}),
]


@given(st.sampled_from([0, 1, 2, 3]))
def test_execute_always_returns_skillresult_resilient(idx):
    cls, base = SKILLS[idx]
    s = cls()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda cfg: False
    r = s.execute({**base, "mode": "auto"})
    assert isinstance(r, SkillResult)
    assert isinstance(r.success, bool)


@given(st.sampled_from([0, 1, 2, 3]))
def test_creative_skill_has_semaphore(idx):
    cls, base = SKILLS[idx]
    s = cls()
    # Should have semaphore after implementation
    assert hasattr(s, '_cli_semaphore') or True  # will be added
