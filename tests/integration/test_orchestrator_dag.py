"""Integration tests for DAG orchestrator (US4)."""

import pytest
from hypothesis import given, strategies as st

from skills.core.orchestrator import DAGOrchestrator, DAGNode, NodeStatus


class TestDAGOrchestrator:
    """Test DAG orchestration functionality."""
    
    def test_orchestrator_initialization(self):
        """Orchestrator should initialize correctly."""
        orch = DAGOrchestrator()
        assert orch is not None
        assert hasattr(orch, 'add_node')
        assert hasattr(orch, 'validate_dag')
        assert hasattr(orch, 'get_ready_nodes')
        assert hasattr(orch, 'execute')
    
    def test_add_node_and_validate_simple_dag(self):
        """Test adding nodes and validating simple DAG."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}, dependencies=["a"]))
        assert orch.validate_dag() is True
    
    def test_cycle_detection(self):
        """Test that cycles are detected."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}, dependencies=["b"]))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}, dependencies=["a"]))
        assert orch.validate_dag() is False
    
    def test_get_ready_nodes_no_dependencies(self):
        """Nodes with no dependencies should be ready."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}))
        ready = orch.get_ready_nodes()
        assert len(ready) == 2
        assert all(n.status == NodeStatus.PENDING for n in ready)
    
    def test_get_ready_nodes_with_dependencies(self):
        """Nodes should only be ready when dependencies complete."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}, dependencies=["a"]))
        
        ready = orch.get_ready_nodes()
        assert len(ready) == 1
        assert ready[0].id == "a"
        
        # Mark a as completed
        orch.nodes["a"].status = NodeStatus.COMPLETED
        ready = orch.get_ready_nodes()
        assert len(ready) == 1
        assert ready[0].id == "b"
    
    def test_execute_simple_dag(self):
        """Test executing a simple DAG."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}, dependencies=["a"]))
        
        results = orch.execute({})
        assert "a" in results
        assert "b" in results
        assert orch.nodes["a"].status == NodeStatus.COMPLETED
        assert orch.nodes["b"].status == NodeStatus.COMPLETED
    
    def test_execute_parallel_independent_nodes(self):
        """Test executing independent nodes."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="skill_a", inputs={}))
        orch.add_node(DAGNode(id="b", skill="skill_b", inputs={}))
        orch.add_node(DAGNode(id="c", skill="skill_c", inputs={}))
        
        results = orch.execute({})
        assert len(results) == 3
        assert all(orch.nodes[n].status == NodeStatus.COMPLETED for n in ["a", "b", "c"])
    
    @given(st.integers(min_value=1, max_value=5))
    def test_linear_chain_dependency_invariants(self, depth):
        """Test linear chain maintains dependency invariants."""
        orch = DAGOrchestrator()
        for i in range(depth):
            deps = [f"node_{i-1}"] if i > 0 else []
            orch.add_node(DAGNode(id=f"node_{i}", skill=f"skill_{i}", inputs={}, dependencies=deps))
        
        assert orch.validate_dag() is True
        results = orch.execute({})
        assert len(results) == depth
        for i in range(depth):
            assert orch.nodes[f"node_{i}"].status == NodeStatus.COMPLETED
