#!/usr/bin/env python3
"""Workflow orchestrator/DAG engine for skill composition."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class NodeStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DAGNode:
    """Node in a DAG workflow."""
    id: str
    skill: str
    inputs: Dict[str, Any]
    dependencies: List[str] = None
    status: NodeStatus = NodeStatus.PENDING
    result: Any = None
    error: Optional[str] = None


class DAGOrchestrator:
    """Orchestrate workflows as DAGs with dependency resolution."""
    
    def __init__(self):
        self.nodes: Dict[str, DAGNode] = {}
        self.edges: Dict[str, List[str]] = {}
    
    def add_node(self, node: DAGNode):
        """Add node to DAG."""
        if node.dependencies is None:
            node.dependencies = []
        self.nodes[node.id] = node
        self.edges[node.id] = node.dependencies
    
    def validate_dag(self) -> bool:
        """Validate DAG has no cycles."""
        # Simple cycle detection
        visited = set()
        rec_stack = set()
        
        def has_cycle(node_id, path):
            visited.add(node_id)
            rec_stack.add(node_id)
            for dep in self.edges.get(node_id, []):
                if dep not in visited:
                    if has_cycle(dep, path + [dep]):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.discard(node_id)
            return False
        
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle(node_id, []):
                    return False
        return True
    
    def get_ready_nodes(self) -> List[DAGNode]:
        """Get nodes ready to execute (all dependencies completed)."""
        ready = []
        for node in self.nodes.values():
            if node.status != NodeStatus.PENDING:
                continue
            deps_ok = all(
                self.nodes.get(dep) and self.nodes[dep].status == NodeStatus.COMPLETED
                for dep in node.dependencies
            )
            if deps_ok:
                ready.append(node)
        return ready
    
    def execute(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute DAG workflow."""
        if context is None:
            context = {}
        
        if not self.validate_dag():
            raise ValueError("DAG contains cycles")
        
        results = {}
        while True:
            ready = self.get_ready_nodes()
            if not ready:
                break
            
            # Execute ready nodes (could be parallelized)
            for node in ready:
                node.status = NodeStatus.RUNNING
                try:
                    # Execute skill (placeholder - would use skill loader)
                    node.result = {"status": "completed", "node": node.id}
                    node.status = NodeStatus.COMPLETED
                    results[node.id] = node.result
                except Exception as e:
                    node.status = NodeStatus.FAILED
                    node.error = str(e)
                    raise
        
        return results
