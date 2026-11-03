---
name: dag-orchestrator
description: Execute workflows as DAGs with dependency resolution and parallel execution
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: workflow
---

# DAG Orchestrator

## Purpose
Execute complex workflows as directed acyclic graphs with dependency resolution, parallel execution, and state management.

## When to Use
When building multi-step workflows with dependencies between steps.

## Inputs
- `dag` (object, required): DAG definition with nodes and edges
- `context` (object, optional): Execution context

## Outputs
- `results` (object): Results from all nodes
- `status` (string): Execution status

## Usage
Generalizable DAG execution for any workflow.

## Limitations
Requires acyclic graphs with valid dependencies.
