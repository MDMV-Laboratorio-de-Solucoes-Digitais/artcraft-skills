"""Contract tests for scene-composition skill implementation (T104)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.base_skill import BaseSkill, SkillResult


def test_scene_composition_module_contract():
    from importlib.util import module_from_spec, spec_from_file_location
    path = os.path.join(os.path.dirname(__file__), "../../skills/integration/scene-composition/skill.py")
    spec = spec_from_file_location("scene_composition_skill", path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    skill = mod.SceneCompositionSkill()
    assert isinstance(skill, BaseSkill)
    r = skill.execute({"assets": [{"id": "x", "type": "image"}]})
    assert isinstance(r, SkillResult)
    assert r.success is True
