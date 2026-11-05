import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from hypothesis import given, strategies as st
from skills.core.base_skill import SkillResult

import importlib.util

def _load_skill(name, class_name):
    path = f'/home/luis/development/artcraft-skills/skills/creative/{name}/skill.py'
    spec = importlib.util.spec_from_file_location(f'skill_{name.replace("-", "_")}', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f'skill_{name.replace("-", "_")}'] = mod
    spec.loader.exec_module(mod)
    return getattr(mod, class_name)


ImageEditSkill = _load_skill('image-edit', 'ImageEditSkill')
BackgroundRemoveSkill = _load_skill('background-remove', 'BackgroundRemoveSkill')
ImageUpscaleSkill = _load_skill('image-upscale', 'ImageUpscaleSkill')
MeshGenerateSkill = _load_skill('mesh-generate', 'MeshGenerateSkill')


SKILLS = [
    (ImageEditSkill, {"image": "/x.png", "prompt": "make blue"}),
    (BackgroundRemoveSkill, {"image": "/x.png"}),
    (ImageUpscaleSkill, {"image": "/x.png", "scale": 2}),
    (MeshGenerateSkill, {"prompt": "a tree"}),
]


@given(st.sampled_from([0, 1, 2, 3]), st.text(min_size=1, max_size=20))
def test_execute_returns_skillresult(idx, txt):
    cls, base = SKILLS[idx]
    s = cls()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda cfg: False
    inputs = dict(base)
    if "prompt" in inputs and isinstance(inputs["prompt"], str):
        inputs["prompt"] = txt
    r = s.execute(inputs)
    assert isinstance(r, SkillResult)
    assert isinstance(r.success, bool)
    assert r.data is None or isinstance(r.data, dict)


@given(st.sampled_from([0, 1, 2, 3]))
def test_validation_deterministic(idx):
    cls, base = SKILLS[idx]
    s = cls()
    a = s.validate_inputs(base)
    b = s.validate_inputs(base)
    assert a == b


@given(st.sampled_from([0, 1, 2, 3]), st.sampled_from(["cli", "mcp", "auto", "foo"]))
def test_mode_enum(idx, mode):
    cls, base = SKILLS[idx]
    s = cls()
    res = s.validate_inputs({**base, "mode": mode})
    assert res == (mode in ("cli", "mcp", "auto"))


@given(st.sampled_from([0, 1, 2, 3]))
def test_execute_does_not_mutate_inputs(idx):
    cls, base = SKILLS[idx]
    s = cls()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda cfg: False
    inputs = dict(base)
    if idx == 0:
        inputs.update({"mode": "auto", "command_keywords": ["edit"]})
    elif idx == 1:
        inputs.update({"mode": "auto", "command_keywords": ["remove"]})
    elif idx == 2:
        inputs.update({"mode": "auto", "command_keywords": ["upscale"]})
    else:
        inputs.update({"mode": "auto", "command_keywords": ["mesh"]})
    before = dict(inputs)
    s.execute(inputs)
    assert inputs == before


@given(st.sampled_from([0, 1, 2, 3]))
def test_execute_does_not_mutate_mcp_config(idx):
    cls, base = SKILLS[idx]
    s = cls()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda c: False
    cfg = {"url": "http://x"}
    before = dict(cfg)
    s.execute({**base, "mode": "mcp", "mcp_config": cfg})
    assert cfg == before


@given(st.sampled_from([0, 1, 2, 3]), st.sampled_from(["cli", "mcp", "auto"]))
def test_mode_selection_deterministic(idx, mode):
    cls, base = SKILLS[idx]
    s1 = cls()
    s2 = cls()
    s1._discover_cli = lambda x=None: None
    s2._discover_cli = lambda x=None: None
    s1._mcp_available = lambda cfg: False
    s2._mcp_available = lambda cfg: False
    r1 = s1.execute({**base, "mode": mode})
    r2 = s2.execute({**base, "mode": mode})
    from tests._helpers.canonicalize import canonicalize_skill_result
    assert canonicalize_skill_result(r1) == canonicalize_skill_result(r2)


@given(st.sampled_from([0, 1, 2, 3]))
def test_schemas_have_expected_fields(idx):
    cls, base = SKILLS[idx]
    s = cls()
    inp = s.get_input_schema()
    out = s.get_output_schema()
    assert isinstance(inp, dict) and isinstance(out, dict)
    assert "properties" in inp and "properties" in out
    if idx == 0:  # image-edit
        assert "image" in inp["properties"]
        assert "prompt" in inp["properties"]
        assert "image_url" in out["properties"] or "image_path" in out["properties"]
    elif idx == 1:  # background-remove
        assert "image" in inp["properties"]
        assert "image_url" in out["properties"]
    elif idx == 2:  # image-upscale
        assert "image" in inp["properties"]
        assert "image_url" in out["properties"]
    else:  # mesh-generate
        # at least one of prompt/image required
        assert "prompt" in inp["properties"] or "image" in inp["properties"]
        assert "mesh_url" in out["properties"] or "mesh_path" in out["properties"]
