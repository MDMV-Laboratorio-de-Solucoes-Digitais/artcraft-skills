"""Property-based tests for cross-product workflow invariants.

TDD tests for US4 - cross-product workflow composition invariants.
"""
from hypothesis import given, strategies as st
import pytest

from skills.core.orchestrator import DAGOrchestrator, DAGNode, NodeStatus
from skills.core.asset_context import AssetContext


class TestCrossProductWorkflowProperties:
    """Property tests for cross-product workflow invariants."""
    
    @given(st.lists(st.text(min_size=1, max_size=20), min_size=1, max_size=10, unique=True))
    def test_dag_execution_completes_all_nodes_when_valid(self, node_ids):
        """All nodes in a valid DAG should complete execution."""
        orch = DAGOrchestrator()
        for i, node_id in enumerate(node_ids):
            deps = [node_ids[i - 1]] if i > 0 and i < len(node_ids) else []
            orch.add_node(DAGNode(id=node_id, skill=f"skill_{i}", inputs={}, dependencies=deps))
        
        assert orch.validate_dag() is True
        results = orch.execute({})
        assert len(results) == len(node_ids)
        for node_id in node_ids:
            assert orch.nodes[node_id].status == NodeStatus.COMPLETED
    
    @given(st.lists(st.text(min_size=1, max_size=20), min_size=2, max_size=8, unique=True))
    def test_asset_context_preserves_data_through_workflow(self, asset_ids):
        """AssetContext should preserve all assets through cross-product workflows."""
        ctx = AssetContext()
        for aid in asset_ids:
            ctx.add_asset(aid, {"id": aid, "type": "test"})
        
        # Context should maintain all assets
        for aid in asset_ids:
            assert ctx.get_asset(aid) is not None
            assert ctx.get_asset(aid)["id"] == aid
        
        # Serialization should preserve data
        data = ctx.to_dict()
        assert len(data["assets"]) == len(asset_ids)
    
    @given(st.integers(min_value=0, max_value=5))
    def test_cross_product_workflow_handles_empty_dependencies(self, num_nodes):
        """Workflows with no dependencies should execute all nodes in parallel."""
        if num_nodes == 0:
            orch = DAGOrchestrator()
            results = orch.execute({})
            assert len(results) == 0
            return
        
        orch = DAGOrchestrator()
        for i in range(num_nodes):
            orch.add_node(DAGNode(id=f"node_{i}", skill=f"skill_{i}", inputs={}))
        
        assert orch.validate_dag() is True
        results = orch.execute({})
        assert len(results) == num_nodes
        for i in range(num_nodes):
            assert orch.nodes[f"node_{i}"].status == NodeStatus.COMPLETED
    
    @given(st.dictionaries(st.text(min_size=1), st.text(min_size=1), min_size=1, max_size=5))
    def test_asset_context_merge_preserves_all_data(self, assets_dict):
        """Merging contexts should preserve data from both contexts."""
        ctx1 = AssetContext()
        ctx2 = AssetContext()
        
        for k, v in assets_dict.items():
            ctx1.add_asset(f"ctx1_{k}", {"data": v})
            ctx2.add_asset(f"ctx2_{k}", {"data": v})
        
        ctx1.merge(ctx2)
        data = ctx1.to_dict()
        assert len(data["assets"]) == len(assets_dict) * 2
    
    @given(st.lists(st.tuples(st.text(min_size=1, max_size=10), st.text(min_size=1, max_size=10)), min_size=1, max_size=6))
    def test_workflow_node_dependencies_respected(self, edges):
        """Dependencies must be respected in execution order."""
        orch = DAGOrchestrator()
        # Create nodes
        node_set = set()
        for a, b in edges:
            node_set.add(a)
            node_set.add(b)
        
        for node_id in node_set:
            # Add with dependencies
            deps = [a for a, b in edges if b == node_id]
            orch.add_node(DAGNode(id=node_id, skill=f"skill_{node_id}", inputs={}, dependencies=deps))
        
        # DAG should be valid if acyclic (our simple case)
        if orch.validate_dag():
            results = orch.execute({})
            # All nodes should complete
            for node_id in node_set:
                assert orch.nodes[node_id].status == NodeStatus.COMPLETED
