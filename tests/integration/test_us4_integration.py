"""Integration tests for cross-product workflows (US4)."""

from skills.core.orchestrator import DAGNode, DAGOrchestrator, NodeStatus
from skills.core.asset_context import AssetContext


class TestCrossProductIntegration:
    """Cross-product integration tests for US4."""

    def test_2d_to_3d_workflow_with_asset_context(self):
        """Orchestrate 2d-to-3d workflow with shared AssetContext."""
        ctx = AssetContext()
        ctx.add_asset("source_image", {"type": "image", "uri": "file://input.png", "format": "png"})

        orch = DAGOrchestrator()
        node = DAGNode(
            id="image_to_3d",
            skill="integration/2d-to-3d-workflow",
            inputs={"asset_id": "source_image"},
            dependencies=[],
        )
        orch.add_node(node)

        assert orch.validate_dag() is True
        ready = orch.get_ready_nodes()
        assert any(n.id == "image_to_3d" for n in ready)
        assert ctx.get_asset("source_image")["type"] == "image"

    def test_scene_composition_workflow_with_asset_context(self):
        """Orchestrate scene composition workflow with shared assets."""
        ctx = AssetContext()
        ctx.add_asset("bg", {"type": "image", "uri": "file://bg.png"})
        ctx.add_asset("mesh", {"type": "mesh", "uri": "file://model.glb"})

        orch = DAGOrchestrator()
        node = DAGNode(
            id="compose_scene",
            skill="integration/scene-composition",
            inputs={"asset_ids": ["bg", "mesh"]},
            dependencies=[],
        )
        orch.add_node(node)

        assert orch.validate_dag() is True
        ready = orch.get_ready_nodes()
        assert any(n.id == "compose_scene" for n in ready)
        assert ctx.get_asset("bg") is not None
        assert ctx.get_asset("mesh") is not None

    def test_cross_product_workflow_chaining(self):
        """Chain 2d-to-3d then scene composition with shared context."""
        ctx = AssetContext()
        ctx.add_asset("source_image", {"type": "image", "uri": "file://input.png"})

        orch = DAGOrchestrator()
        orch.add_node(DAGNode(
            id="image_to_3d",
            skill="integration/2d-to-3d-workflow",
            inputs={"asset_id": "source_image"},
            dependencies=[],
        ))
        orch.add_node(DAGNode(
            id="compose_scene",
            skill="integration/scene-composition",
            inputs={"asset_ids": ["generated_mesh"]},
            dependencies=["image_to_3d"],
        ))

        assert orch.validate_dag() is True
        ready = orch.get_ready_nodes()
        assert len(ready) == 1
        assert ready[0].id == "image_to_3d"

        orch.nodes["image_to_3d"].status = NodeStatus.COMPLETED
        ready = orch.get_ready_nodes()
        assert len(ready) == 1
        assert ready[0].id == "compose_scene"

    def test_asset_context_sharing_across_workflows(self):
        """AssetContext should share assets across workflow nodes."""
        ctx = AssetContext()
        ctx.add_asset("input", {"type": "image", "data": "base64..."})
        ctx.add_style("cartoon", {"preset": "toon", "intensity": 0.8})

        # Simulate passing context through workflow
        ctx2 = AssetContext()
        ctx2.merge(ctx)
        assert ctx2.get_asset("input")["type"] == "image"
        assert ctx2.get_style("cartoon")["preset"] == "toon"

    def test_cross_product_orchestrator_execution(self):
        """Execute cross-product workflow via orchestrator."""
        ctx = AssetContext()
        ctx.add_asset("source", {"type": "image"})

        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="step1", skill="integration/2d-to-3d-workflow", inputs={}))
        orch.add_node(DAGNode(id="step2", skill="integration/scene-composition", inputs={}, dependencies=["step1"]))

        results = orch.execute({})
        assert "step1" in results
        assert "step2" in results
