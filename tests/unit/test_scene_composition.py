"""Unit tests for scene-composition skill (T103/T104)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.base_skill import BaseSkill, SkillResult


def _load_skill():
    from importlib.util import module_from_spec, spec_from_file_location
    path = os.path.join(os.path.dirname(__file__), "../../skills/integration/scene-composition/skill.py")
    spec = spec_from_file_location("scene_composition_skill", path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SceneCompositionSkill()


def test_scene_composition_is_base_skill():
    skill = _load_skill()
    assert isinstance(skill, BaseSkill)


def test_scene_composition_schemas():
    skill = _load_skill()
    inp = skill.get_input_schema()
    out = skill.get_output_schema()
    assert "properties" in inp
    assert "assets" in inp["properties"]
    assert "scene_id" in out["properties"] or "scene_url" in out["properties"]


def test_scene_composition_execute_success():
    skill = _load_skill()
    result = skill.execute({"assets": [{"id": "bg", "type": "image"}, {"id": "mesh", "type": "mesh"}]})
    assert isinstance(result, SkillResult)
    assert result.success is True
    assert result.data is not None
    assert result.data.get("scene_id") or result.data.get("scene_url")


def test_scene_composition_rejects_missing_assets():
    skill = _load_skill()
    result = skill.execute({})
    assert result.success is False
    assert result.error


def test_scene_composition_preserves_asset_context_metadata():
    skill = _load_skill()
    result = skill.execute({
        "assets": [{"id": "a1", "type": "image"}],
        "context": {"styles": {"theme": "dark"}}
    })
    assert result.success is True
    assert result.metadata is not None
