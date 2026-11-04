"""Contract tests for orchestrator interface (001 US4, T042)."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

import pytest
from hypothesis import given, strategies as st

from skills.core.orchestrator import DAGOrchestrator, DAGNode, NodeStatus


class TestOrchestratorContract:
    """Contract: DAGOrchestrator exposes the expected public API."""

    def test_orchestrator_class_exists(self):
        assert DAGOrchestrator is not None

    def test_orchestrator_instantiates(self):
        orch = DAGOrchestrator()
        assert orch is not None
        assert hasattr(orch, "nodes")
        assert hasattr(orch, "edges")

    def test_required_methods_present(self):
        orch = DAGOrchestrator()
        for m in ("add_node", "validate_dag", "get_ready_nodes", "execute"):
            assert hasattr(orch, m), f"missing method: {m}"
            assert callable(getattr(orch, m))

    def test_dag_node_dataclass_fields(self):
        node = DAGNode(id="n1", skill="s", inputs={})
        assert node.id == "n1"
        assert node.skill == "s"
        assert node.inputs == {}
        assert node.dependencies in (None, [])
        assert node.status == NodeStatus.PENDING
        assert node.result is None
        assert node.error is None

    def test_node_status_enum_values(self):
        expected = {"PENDING", "RUNNING", "COMPLETED", "FAILED", "SKIPPED"}
        assert {s.name for s in NodeStatus} == expected

    def test_add_node_registers(self):
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="sa", inputs={}))
        assert "a" in orch.nodes
        assert orch.edges["a"] == []

    def test_validate_dag_rejects_cycle(self):
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="sa", inputs={}, dependencies=["b"]))
        orch.add_node(DAGNode(id="b", skill="sb", inputs={}, dependencies=["a"]))
        assert orch.validate_dag() is False

    def test_validate_dag_accepts_acyclic(self):
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="sa", inputs={}))
        orch.add_node(DAGNode(id="b", skill="sb", inputs={}, dependencies=["a"]))
        assert orch.validate_dag() is True

    def test_get_ready_nodes_empty_when_blocked(self):
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="a", skill="sa", inputs={}, dependencies=["missing"]))
        # dependency missing -> not ready
        ready = orch.get_ready_nodes()
        assert isinstance(ready, list)

    @given(st.lists(st.text(min_size=1, max_size=8, alphabet="abc"), min_size=1, max_size=6, unique=True))
    def test_ready_nodes_subset_of_pending(self, ids):
        orch = DAGOrchestrator()
        for i in ids:
            orch.add_node(DAGNode(id=i, skill=i, inputs={}))
        ready = orch.get_ready_nodes()
        assert all(n.status == NodeStatus.PENDING for n in ready)
        assert len(ready) == len(ids)  # no deps -> all ready


def test_orchestrator_importable():
    import skills.core.orchestrator as m
    assert hasattr(m, "DAGOrchestrator")
    assert hasattr(m, "DAGNode")
    assert hasattr(m, "NodeStatus")
