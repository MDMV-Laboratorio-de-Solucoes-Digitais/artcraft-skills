import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from hypothesis import given, strategies as st
from skills.core.base_skill import SkillResult
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "creative", "image-generate")))
import skill as _ig_skill
ImageGenerateSkill = _ig_skill.ImageGenerateSkill


@given(st.text(min_size=1, max_size=50))
def test_execute_returns_skillresult(prompt):
    s = ImageGenerateSkill()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda cfg: False
    r = s.execute({"prompt": prompt})
    assert isinstance(r, SkillResult)
    assert isinstance(r.success, bool)
    assert r.data is None or isinstance(r.data, dict)


@given(st.text(min_size=1, max_size=50))
def test_validation_deterministic(prompt):
    s = ImageGenerateSkill()
    a = s.validate_inputs({"prompt": prompt})
    b = s.validate_inputs({"prompt": prompt})
    assert a == b


@given(st.sampled_from(["cli", "mcp", "auto", "foo"]))
def test_mode_enum(mode):
    s = ImageGenerateSkill()
    ok = s.validate_inputs({"prompt": "x", "mode": mode}) if mode in ("cli","mcp","auto") else False
    # validate_inputs handles mode
    assert s.validate_inputs({"prompt": "x", "mode": mode}) == (mode in ("cli", "mcp", "auto"))


@given(st.dictionaries(st.text(min_size=1, max_size=5), st.integers(), min_size=1, max_size=5))
def test_composition_preserves_fields(data):
    from skills.core.composer import SkillComposer
    composer = SkillComposer()
    skill = ImageGenerateSkill()
    composer.register(skill)
    skill.validate_inputs = lambda inputs: True
    skill.execute = lambda inputs: SkillResult(success=True, data={**inputs, "done": True})
    res = composer.compose(["image-generate"], data)
    assert res.success
    for k, v in data.items():
        assert res.data[k] == v

from tests._helpers.canonicalize import canonicalize_skill_result
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reference')))
from image_generate_original import ImageGenerateSkill as OriginalImageGenerateSkill


@given(st.text(min_size=1, max_size=50))
def test_execute_does_not_mutate_inputs(prompt):
    s = ImageGenerateSkill()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda cfg: False
    inputs = {"prompt": prompt, "mode": "auto", "command_keywords": ["generate"]}
    before = dict(inputs)
    s.execute(inputs)
    assert inputs == before


@given(st.dictionaries(st.text(min_size=1, max_size=6), st.integers(), min_size=0, max_size=5))
def test_execute_does_not_mutate_mcp_config(cfg):
    s = ImageGenerateSkill()
    s._discover_cli = lambda x=None: None
    s._mcp_available = lambda c: False
    before = dict(cfg)
    s.execute({"prompt": "x", "mode": "mcp", "mcp_config": cfg})
    assert cfg == before


@given(st.sampled_from(["cli", "mcp", "auto"]), st.text(min_size=1, max_size=20))
def test_mode_selection_deterministic(mode, prompt):
    s1 = ImageGenerateSkill()
    s2 = ImageGenerateSkill()
    s1._discover_cli = lambda x=None: None
    s2._discover_cli = lambda x=None: None
    s1._mcp_available = lambda cfg: False
    s2._mcp_available = lambda cfg: False
    r1 = s1.execute({"prompt": prompt, "mode": mode})
    r2 = s2.execute({"prompt": prompt, "mode": mode})
    assert canonicalize_skill_result(r1) == canonicalize_skill_result(r2)


@given(st.text(min_size=1, max_size=20))
def test_equivalence_original_vs_refactored(prompt):
    orig = OriginalImageGenerateSkill()
    new = ImageGenerateSkill()
    orig._discover_cli = lambda x=None: None
    new._discover_cli = lambda x=None: None
    orig._mcp_available = lambda cfg: False
    new._mcp_available = lambda cfg: False
    ro = orig.execute({"prompt": prompt, "mode": "auto"})
    rn = new.execute({"prompt": prompt, "mode": "auto"})
    assert canonicalize_skill_result(ro) == canonicalize_skill_result(rn)


@given(st.text(min_size=1, max_size=20), st.sampled_from(["cli", "mcp", "auto"]))
def test_equivalence_original_vs_refactored_modes(prompt, mode):
    orig = OriginalImageGenerateSkill()
    new = ImageGenerateSkill()
    orig._discover_cli = lambda x=None: "/bin/cli"
    new._discover_cli = lambda x=None: "/bin/cli"
    import subprocess, json
    cmds = {"commands": [{"id": "generate", "label": "generate"}]}
    def fake_run(args, *a, **k):
        if len(args) > 1 and args[1] == "commands":
            return subprocess.CompletedProcess(args, 0, json.dumps(cmds), "")
        return subprocess.CompletedProcess(args, 0, json.dumps({"image_path": "/y.png"}), "")
    orig_run = subprocess.run
    subprocess.run = fake_run
    try:
        orig._mcp_available = lambda cfg: False
        new._mcp_available = lambda cfg: False
        ro = orig.execute({"prompt": prompt, "mode": mode})
        rn = new.execute({"prompt": prompt, "mode": mode})
    finally:
        subprocess.run = orig_run
    assert canonicalize_skill_result(ro) == canonicalize_skill_result(rn)
