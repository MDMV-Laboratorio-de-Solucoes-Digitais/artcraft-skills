# Cross-Product Integration

This document describes cross-product integration patterns for ArtCraft Skills.

## Overview
Skills can be composed across different domains (2D, 3D, video, etc.) using orchestrators and shared context.

## Patterns
- **Shared Asset Context**: Use `AssetContext` to share assets and styles across skills
- **Workflow Orchestration**: Use DAG orchestrator for complex multi-step workflows
- **Composition**: Chain atomic skills using the composer utilities

## Examples
- 2D to 3D workflow: Process image → Generate 3D mesh
- Scene composition: Combine multiple assets into unified scene
