# Problem Definition: Creative skills lack executable implementations

- **Slug**: implement-python-creative-skills
- **Created**: 2026-11-04
- **Inputs used**: intake.md? yes | research.md? yes | user input only? yes

## Problem Statement

Four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) exist only as declarative `SKILL.md` scaffolds with no executable Python implementation. Agents that need to perform image editing, background removal, upscaling, or mesh generation cannot actually invoke those skills — they can only read their metadata. Meanwhile, the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) is built, tested, and converged but has only one real consumer (`image-generate`), so its reusability promise (SC-005) remains unproven. Feature 001 Phase 1 is stuck at ~25% Python implementation.

## Affected Users & Stakeholders

- **Users**: AI agent operators (Claude Code, Cursor, Codex, Gemini, OpenCode) who want to edit images, remove backgrounds, upscale, or generate 3D meshes through ArtCraft skills — [research.md: Users & Demand] (confidence: medium)
- **Stakeholders**: ArtCraft Skills Suite maintainers — responsible for feature 001 completion and adapter reusability evidence — [research.md: prior analysis in this session] (confidence: high)
- **Stakeholders**: MDMV team — uses generalizable workflows derived from feature 001 skills — [intake.md: Origin & Context] (confidence: medium)

## Goals

- Each of the 4 creative skills has an executable Python `skill.py` that agents can invoke
- Each skill reuses the shared adapter (`discover_cli`, `discover_generation_command`, `run_cli_generation`, `normalize_output`, `normalize_mcp_config`, `select_mode`, reason codes)
- Each skill degrades gracefully when CLI/MCP is unavailable (reason codes `cli_not_found`, `mcp_unavailable`, `neither_available`)
- Feature 001 Phase 1 advances from ~25% to ~80% Python implementation
- Adapter reusability (SC-005) is demonstrated with real consumers beyond `image-generate`

## Non-Goals

- Implementing MCP transport inside the adapter (FR-005 decision: MCP discovery/invocation remain skill-level)
- Creating new skill categories (video, audio, 3D beyond mesh-generate, CAD, documents) — those are Phases 3–5
- Building provider backends or reimplementing ArtCraft APIs — skills consume existing CLI/MCP surfaces
- Refactoring `image-generate/skill.py` — it already works and should remain unchanged

## Success Metrics

- 4/4 creative skills have executable `skill.py` files (baseline: 0/4) — measurable
- All 4 skills validate via `python scripts/validate_skill.py skills/creative/<name>` (baseline: they already validate as declarative, but now with executable code) — measurable
- Full test suite (278+ tests) continues to pass after implementation — measurable
- Each skill's `skill.py` follows the `image-generate` template pattern (discover → resolve command → invoke → normalize → degrade gracefully) — qualitative (assumption)
- Full convergence of feature 001 (97/97 tasks) maintained or improved — measurable (baseline: 97/97 complete)

## Cost of Inaction

- Feature 001 Phase 1 remains at ~25% Python implementation; only `image-generate` is executable
- The adapter's reusability promise (SC-005) stays unproven with only one consumer
- Agents cannot invoke image-edit, background-remove, upscaling, or mesh generation — they can only read skill metadata
- Downstream capabilities (cross-product workflows US4, MDMV workflows US5, Phases 2–5) remain blocked on executable creative skills

## Open Questions

- [NEEDS CLARIFICATION: exact input/output schema for each skill beyond what SKILL.md declares]
- [NEEDS CLARIFICATION: default `command_keywords` for each skill]
- [NEEDS CLARIFICATION: skill-specific params (mask for image-edit, scale for image-upscale, format for mesh-generate)]
- [NEEDS CLARIFICATION: whether to extract a shared base class to avoid duplication across the 4 skill.py files]
- [NEEDS CLARIFICATION: whether tests/contract/test_atomic_skills.py should be extended to cover the 4 new skills]
