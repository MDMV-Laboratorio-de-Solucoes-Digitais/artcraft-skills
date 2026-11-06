# Implementation Plan: Integração de geração de assets com ArtCraft

**Branch**: `006-integracao-geracao-assets` | **Date**: 2026-11-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-integracao-geracao-assets/spec.md`

## Summary

Integrate asset generation into ArtCraft skills with discovery-first approach: try to find real generation commands via CLI/MCP, configure via `generation_command`/`command_keywords`. When none found, add fallback using editing commands (`paint.bucket`, `edit.fill`, `paint.stroke`) for simple pixel art. Maintain compatibility with `SkillResult` contracts and graceful degradation.

## Technical Context

**Language/Version**: Python 3.x  
**Primary Dependencies**: Python stdlib (subprocess, json, os, threading, time), PyYAML  
**Storage**: Filesystem (PNG outputs)  
**Testing**: pytest (unit/contract/integration/property/characterization)  
**Target Platform**: Linux  
**Project Type**: Library (skills core + creative skills)  
**Constraints**: Must follow constitution, vendor-neutral CLI/MCP only, maintain backward compatibility, all existing tests pass  
**Scale/Scope**: Affects `skills/core/artcraft_app_client.py`, `skills/core/creative_skill.py`, `skills/creative/image-generate/skill.py`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] I. Crafting Over Generating - Orchestrates real tools, doesn't replace
- [x] II. Artist-Centric Design - Provides practical solution
- [x] III. Open Source, Vendor-Neutral, Interoperable - Uses CLI/MCP, no vendor lock-in
- [x] IV. Composability and Modularity - Extends existing patterns
- [x] V. Performance and Native Execution - Uses native CLI
- [x] VI. Quality Through Intentional Craft - Maintains control
- [x] VII. Transparency, Reproducibility, Cost Awareness - Preserves metadata
- [x] VIII. Extensibility Without Unnecessary Complexity - Simple fallback

## Project Structure

### Source Code
```text
skills/
├── core/
│   ├── artcraft_app_client.py  # MODIFY: add generate_via_editing_commands
│   └── creative_skill.py       # MODIFY: add fallback in _execute_cli
└── creative/
    └── image-generate/
        └── skill.py            # MODIFY: add fallback
```

## Complexity Tracking
No violations.
