"""Contract tests for cross-product workflows.

Tests verify that cross-product integration components follow expected contracts:
- AssetContext for shared asset/context/style management
- DAGOrchestrator for workflow orchestration
- Cross-product skill interfaces (2D→3D, scene composition)
"""
import os
import sys

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.asset_context import AssetContext
from skills.core.orchestrator import DAGNode, DAGOrchestrator, NodeStatus


def test_asset_context_has_required_methods():
    """AssetContext must implement required methods."""
    ctx = AssetContext()
    assert hasattr(ctx, 'add_asset')
    assert hasattr(ctx, 'get_asset')
    assert hasattr(ctx, 'add_style')
    assert hasattr(ctx, 'get_style')
    assert hasattr(ctx, 'merge')
    assert hasattr(ctx, 'to_dict')
    assert callable(ctx.add_asset)
    assert callable(ctx.get_asset)
    assert callable(ctx.merge)


def test_asset_context_add_and_get_asset():
    """AssetContext should store and retrieve assets."""
    ctx = AssetContext()
    asset = {"type": "image", "uri": "file://test.png"}
    ctx.add_asset("test_asset", asset)
    retrieved = ctx.get_asset("test_asset")
    assert retrieved == asset
    assert retrieved["type"] == "image"


def test_asset_context_add_and_get_style():
    """AssetContext should store and retrieve styles."""
    ctx = AssetContext()
    style = {"preset": "cartoon", "intensity": 0.8}
    ctx.add_style("test_style", style)
    retrieved = ctx.get_style("test_style")
    assert retrieved == style
    assert retrieved["preset"] == "cartoon"


def test_asset_context_merge():
    """AssetContext.merge should combine contexts."""
    ctx1 = AssetContext()
    ctx1.add_asset("asset1", {"type": "image"})
    ctx1.add_style("style1", {"name": "test"})

    ctx2 = AssetContext()
    ctx2.add_asset("asset2", {"type": "mesh"})
    
    ctx1.merge(ctx2)
    assert ctx1.get_asset("asset1") is not None
    assert ctx1.get_asset("asset2") is not None
    assert ctx1.get_style("style1") is not None


def test_asset_context_to_dict():
    """AssetContext.to_dict should serialize context."""
    ctx = AssetContext()
    ctx.add_asset("img", {"type": "image"})
    ctx.add_style("s1", {"name": "style"})
    result = ctx.to_dict()
    assert isinstance(result, dict)
    assert "assets" in result
    assert "styles" in result
    assert "metadata" in result
    assert "history" in result


def test_dag_orchestrator_has_required_methods():
    """DAGOrchestrator must implement required methods."""
    orch = DAGOrchestrator()
    assert hasattr(orch, 'add_node')
    assert hasattr(orch, 'validate_dag')
    assert hasattr(orch, 'get_ready_nodes')
    assert hasattr(orch, 'execute')
    assert callable(orch.add_node)
    assert callable(orch.validate_dag)
    assert callable(orch.get_ready_nodes)
    assert callable(orch.execute)


def test_dag_node_creation():
    """DAGNode should be creatable with required fields."""
    node = DAGNode(
        id="test_node",
        skill="integration/test-skill",
        inputs={"key": "value"},
        dependencies=[]
    )
    assert node.id == "test_node"
    assert node.skill == "integration/test-skill"
    assert node.inputs == {"key": "value"}
    assert node.dependencies == []


def test_dag_orchestrator_add_node():
    """DAGOrchestrator should accept nodes."""
    orch = DAGOrchestrator()
    node = DAGNode(id="n1", skill="test/skill", inputs={})
    orch.add_node(node)
    assert "n1" in orch.nodes


def test_dag_orchestrator_validate_dag():
    """DAGOrchestrator should validate DAG structure."""
    orch = DAGOrchestrator()
    orch.add_node(DAGNode(id="n1", skill="test/skill1", inputs={}))
    orch.add_node(DAGNode(id="n2", skill="test/skill2", inputs={}, dependencies=["n1"]))
    assert orch.validate_dag() is True


def test_dag_orchestrator_get_ready_nodes():
    """DAGOrchestrator should identify ready nodes."""
    orch = DAGOrchestrator()
    orch.add_node(DAGNode(id="n1", skill="test/skill1", inputs={}))
    orch.add_node(DAGNode(id="n2", skill="test/skill2", inputs={}, dependencies=["n1"]))
    ready = orch.get_ready_nodes()
    assert len(ready) == 1
    assert ready[0].id == "n1"


def test_dag_orchestrator_dependency_resolution():
    """DAGOrchestrator should resolve dependencies correctly."""
    orch = DAGOrchestrator()
    orch.add_node(DAGNode(id="n1", skill="test/skill1", inputs={}))
    orch.add_node(DAGNode(id="n2", skill="test/skill2", inputs={}, dependencies=["n1"]))
    ready = orch.get_ready_nodes()
    assert ready[0].id == "n1"
    orch.nodes["n1"].status = NodeStatus.COMPLETED
    ready = orch.get_ready_nodes()
    assert len(ready) == 1
    assert ready[0].id == "n2"


def test_cross_product_2d_to_3d_workflow_contract():
    """2D-to-3D workflow should follow cross-product contract."""
    ctx = AssetContext()
    ctx.add_asset("source", {"type": "image", "format": "png"})
    
    orch = DAGOrchestrator()
    node = DAGNode(
        id="image_to_3d",
        skill="integration/2d-to-3d-workflow",
        inputs={"asset_id": "source"},
        dependencies=[]
    )
    orch.add_node(node)
    assert orch.validate_dag() is True
    assert ctx.get_asset("source")["type"] == "image"


def test_cross_product_scene_composition_workflow_contract():
    """Scene composition workflow should follow cross-product contract."""
    ctx = AssetContext()
    ctx.add_asset("bg", {"type": "image"})
    ctx.add_asset("mesh", {"type": "mesh"})
    
    orch = DAGOrchestrator()
    node = DAGNode(
        id="compose",
        skill="integration/scene-composition",
        inputs={"asset_ids": ["bg", "mesh"]},
        dependencies=[]
    )
    orch.add_node(node)
    assert orch.validate_dag() is True
    assert len([a for a in [ctx.get_asset("bg"), ctx.get_asset("mesh")] if a]) == 2


def test_cross_product_workflow_chaining_contract():
    """Cross-product workflows should be chainable."""
    ctx = AssetContext()
    ctx.add_asset("input", {"type": "image"})
    
    orch = DAGOrchestrator()
    orch.add_node(DAGNode(id="step1", skill="integration/2d-to-3d-workflow", inputs={"asset_id": "input"}, dependencies=[]))
    orch.add_node(DAGNode(id="step2", skill="integration/scene-composition", inputs={"asset_ids": ["mesh"]}, dependencies=["step1"]))
    
    assert orch.validate_dag() is True
    ready = orch.get_ready_nodes()
    assert ready[0].id == "step1"
    orch.nodes["step1"].status = NodeStatus.COMPLETED
    ready = orch.get_ready_nodes()
    assert ready[0].id == "step2"
