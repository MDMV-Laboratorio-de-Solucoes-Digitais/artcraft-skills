# Implementation Plan: Shared CLI/MCP Adapter

**Branch**: `003-shared-cli-mcp-adapter` | **Date**: 2026-11-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-shared-cli-mcp-adapter/spec.md`

## Summary

Extract CLI/MCP discovery, invocation, and normalization logic from `skills/creative/image-generate/skill.py` into a shared `skills/core/artcraft_app_client.py` module (function-based as clarified). Refactor image-generate to use the shared module while preserving exact behavior. This enables reuse across all creative skills (image-edit, background-remove, image-upscale, mesh-generate) following Constitution v2.1.0 (CLI/MCP-only).

## Technical Context

**Language/Version**: Python 3.x (stdlib only)  
**Primary Dependencies**: stdlib (json, os, shutil, subprocess)  
**Storage**: N/A  
**Testing**: pytest — unit/contract/integration/property suites; `python scripts/validate_skill.py skills/creative/image-generate`; `python scripts/validate_all_skills.py`.
**Target Platform**: Linux/macOS/Windows  
**Project Type**: Skill library (agentskills.io)  
**Performance Goals**: N/A (infrastructure)  
**Constraints**: No new dependencies, must maintain backward compatibility, all existing tests must pass  
**Scale/Scope**: Small refactor - extract ~150 lines, create new module in core

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principles:**
- I. Crafting Over Generating: ✅ Infrastructure supports composition
- II. Artist-Centric Design: ✅ Enables precise CLI/MCP control
- III. Open Source/Vendor-Neutral/Interoperable: ✅ CLI/MCP only per v2.1.0, no API
- IV. Composability and Modularity: ✅ Shared module enables composition
- V. Performance: ✅ No overhead added
- VI. Quality Through Intentional Craft: ✅ Preserves behavior
- VII. Transparency/Cost Awareness: ✅ N/A
- VIII. Extensibility Without Unnecessary Complexity: ✅ Simple function-based API

**Gates:** PASS

## Project Structure

### Documentation (this feature)
```
specs/003-shared-cli-mcp-adapter/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
    └── artcraft_app_client.md
```

### Source Code (repository root)
```
skills/
├── core/
│   ├── artcraft_app_client.py  # NEW - shared adapter
│   └── ...
└── creative/
    └── image-generate/
        └── skill.py            # MODIFIED - uses shared adapter
```

## Complexity Tracking

*No violations* - simple refactor following existing patterns.
