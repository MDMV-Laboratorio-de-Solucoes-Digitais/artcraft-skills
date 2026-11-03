

def test_2d_to_3d_workflow_dag_wiring():
    """Orchestrate 2d-to-3d workflow via DAG with shared AssetContext (US4)."""
    from skills.core.orchestrator import DAGNode, DAGOrchestrator
    from skills.core.asset_context import AssetContext

    ctx = AssetContext()
    ctx.add_asset("source_image", {"type": "image", "uri": "file://input.png"})

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
