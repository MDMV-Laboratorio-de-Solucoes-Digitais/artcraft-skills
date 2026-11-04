# Implementation Plan: Implement Python Creative Skills

**Branch**: `004-implement-python-creative-skills` | **Date**: 2026-11-04 | **Spec**: specs/004-implement-python-creative-skills/spec.md

**Input**: Feature specification from `/specs/004-implement-python-creative-skills/spec.md`

## Summary

Implement executable Python `skill.py` files for four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) that currently exist only as declarative `SKILL.md` scaffolds, using the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) and `image-generate/skill.py` as the template.

## Technical Context

**Language/Version**: Python 3.x

**Primary Dependencies**: None external (uses Python standard library and existing `skills/core/` modules)

**Storage**: Filesystem (skill definitions, assets); integration with `.specify/` structure

**Testing**: pytest (project uses pytest)

**Target Platform**: Python 3.x compatible environment where `photocraft-cli` is available

**Project Type**: Skills suite / agent capabilities library (documentation + skill definitions + utilities)

**Performance Goals**: Fast skill discovery/loading, efficient CLI invocation with timeout

**Constraints**: Must follow Constitution v2.0.0, vendor-neutral where possible, secure credential handling, no MDMV branding

**Scale/Scope**: 4 creative skills (image-edit, background-remove, image-upscale, mesh-generate)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**ArtCraft Skills Constitution v2.0.0 compliance:**
- [x] I. Crafting Over Generating - composition-first, build before generating philosophy
- [x] II. Artist-Centric Design - precise control, flexibility
- [x] III. Open Source, Vendor-Neutral, Interoperable - MIT/Apache-2.0, multi-agent, ArtCraft integration
- [x] IV. Composability and Modularity - atomic skills + orchestrators, clear contracts
- [x] V. Performance and Native Execution - efficient processing, resource awareness
- [x] VI. Quality Through Intentional Craft - iteration, refinement, control
- [x] VII. Transparency, Reproducibility, Cost Awareness - model/provider/cost visibility
- [x] VIII. Extensibility Without Unnecessary Complexity - clear patterns, discoverable

## Project Structure

### Documentation (this feature)

```text
specs/004-implement-python-creative-skills/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
skills/
├── core/
│   └── creative_skill.py        # NEW: Shared base class
├── creative/
│   ├── image-edit/
│   │   └── skill.py             # NEW: Image edit skill implementation
│   ├── background-remove/
│   │   └── skill.py             # NEW: Background remove skill implementation
│   ├── image-upscale/
│   │   └── skill.py             # NEW: Image upscale skill implementation
│   └── mesh-generate/
│   │   └── skill.py             # NEW: Mesh generate skill implementation
```

**Structure Decision**: Single project layout within existing `skills/core/` and `skills/creative/` directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations.