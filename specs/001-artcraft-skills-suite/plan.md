# Implementation Plan: ArtCraft Skills Suite

**Branch**: `001-artcraft-skills-suite` | **Date**: 2026-11-03 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-artcraft-skills-suite/spec.md`

## Summary

Build an extensive, composable suite of agent skills for creative asset creation, editing, manipulation, and development across all ArtCraft products (PhotoCraft, VectorCraft, FilmCraft, TextureCraft, CADCraft, DeckCraft, SoundCraft, etc.) with cross-product integration. Skills follow agentskills.io standard for broad agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode). Foundation-first approach: define skill schema/loader integrated with Spec Kit extension system, build core abstractions (model/provider routing, ArtCraft API adapters with abstraction layer, async job orchestration, cost tracking, credential management), then atomic skills + orchestrators. Initially serves MDMV needs with generalizable workflows (structured-packager, policy-redaction, workflow-orchestrator, evidence-audit) while remaining open-source and general-purpose.

## Technical Context

**Language/Version**: Markdown (SKILL.md), YAML frontmatter, plus supporting scripts in shell/Python/Node as needed for utilities; integration with existing Spec Kit tooling  
**Primary Dependencies**: agentskills.io standard, ArtCraft APIs (storyteller-web / Omni API), MCP where applicable (Blender, ComfyUI), Spec Kit extension framework  
**Storage**: Filesystem (skill definitions, assets, references); integration with existing `.specify/` structure  
**Testing**: Contract/schema validation, mocked providers for deterministic tests, fixture-based replay, property-based tests for deterministic components, evals for non-deterministic generation  
**Target Platform**: Cross-agent (Claude Code, Cursor, Codex, Gemini, OpenCode) and integration with ArtCraft ecosystem  
**Project Type**: Skills suite / agent capabilities library (documentation + skill definitions + utilities)  
**Performance Goals**: Fast skill discovery/loading, efficient composition, reasonable API call overhead  
**Constraints**: Must follow ArtCraft Skills Constitution v2.0.0, vendor-neutral where possible, secure credential handling, no MDMV-specific branding in skills  
**Scale/Scope**: Extensive suite covering all major asset types across 15 ArtCraft apps, composable architecture

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

**Development Workflow compliance:**
- [x] Research first, design for composition
- [x] Follow crafting philosophy
- [x] Test with real workflows
- [x] Document thoroughly
- [x] Quality gates defined

No violations identified.

## Project Structure

### Documentation (this feature)

```text
specs/001-artcraft-skills-suite/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
artcraft-skills/
├── .specify/                    # Spec Kit infrastructure (existing)
│   ├── extensions/              # Extensions including assess (existing)
│   ├── memory/constitution.md   # v2.0.0 (existing)
│   └── templates/               # Templates
├── skills/                      # NEW: Skill definitions following agentskills.io
│   ├── core/                    # Core abstractions and utilities
│   ├── creative/                # Creative asset skills (image, 3D, video, audio)
│   ├── workflow/                # Orchestrator/workflow skills
│   └── integration/             # Cross-product integration skills
├── scripts/                     # NEW: Utilities for skill validation/loading
└── docs/                        # NEW: Documentation
```

**Structure Decision**: Skills organized by category following composability principle. Core abstractions in `skills/core/`, domain skills in `skills/creative/`, workflows in `skills/workflow/`, cross-product integration in `skills/integration/`. Each skill follows agentskills.io structure (directory with SKILL.md + optional scripts/references/assets). Integration with Spec Kit via extension registration.

## Complexity Tracking

No violations to justify.
