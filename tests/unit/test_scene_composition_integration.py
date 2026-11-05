"""Integration-style unit test for scene-composition in DAG workflow (T104)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.asset_context import AssetContext
from skills.core.orchestrator import DAGNode, DAGOrchestrator, NodeStatus
from importlib.util import module_from_spec, spec_from_file_location


def _load_scene_skill():
    path = os.path.join(os.path.dirname(__file__), "../../skills/integration/scene-composition/skill.py")
    spec = spec_from_file_location("scene_composition_skill", path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SceneCompositionSkill()


def test_scene_composition_executes_with_asset_context_in_dag():
    ctx = AssetContext()
    ctx.add_asset("bg", {"type": "image"})
    ctx.add_asset("mesh", {"type": "mesh"})
    skill = _load_scene_skill()
    r = skill.execute({"assets": [ctx.get_asset("bg"), ctx.get_asset("mesh")], "context": ctx.to_dict()})
    assert r.success
    orch = DAGOrchestrator()
    orch.add_node(DAGNode(id="compose", skill="integration/scene-composition", inputs={"scene_id": r.data["scene_id"]}, dependencies=[]))
    assert orch.validate_dag() is True
    ready = orch.get_ready_nodes()
    assert ready[0].id == "compose"
    orch.nodes["compose"].status = NodeStatus.COMPLETED
    assert orch.get_ready_nodes() == []
