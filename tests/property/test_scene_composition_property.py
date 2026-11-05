"""Property-based tests for scene-composition (T104)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hypothesis import given, strategies as st
from importlib.util import module_from_spec, spec_from_file_location


def _skill():
    path = os.path.join(os.path.dirname(__file__), "../../skills/integration/scene-composition/skill.py")
    spec = spec_from_file_location("scene_composition_skill", path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SceneCompositionSkill()


@given(st.lists(st.fixed_dictionaries({"id": st.text(min_size=1, max_size=12), "type": st.sampled_from(["image", "mesh", "video", "audio"])}), min_size=1, max_size=8))
def test_scene_composition_invariants(assets):
    skill = _skill()
    r = skill.execute({"assets": assets})
    assert r.success is True
    assert r.data["scene_id"]
    assert len(r.data["asset_ids"]) <= len(assets)
