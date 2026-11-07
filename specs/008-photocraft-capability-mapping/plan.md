# Implementation Plan: PhotoCraft MCP capability mapping (engine/editor)

**Branch**: `008-photocraft-capability-mapping` | **Date**: 2026-11-06 | **Spec**: `specs/008-photocraft-capability-mapping/spec.md`
**Input**: Feature specification from `specs/008-photocraft-capability-mapping/spec.md`

## Summary

Deliver a **docs-only** Speckit slice that maps PhotoCraft MCP capabilities (discovery, engine commands, document/preview operations, roots, progress, cancellation, error semantics, format/protocol limits) with defensive gating and explicit exclusions (no AI generation, no stateful cross-call, no bridge/UI headless scope, no CI/default real smoke). Reuse 006 adapter contracts (FR-005/FR-006) and 007 safety patterns; **no changes** to `skills/`, `tests/`, or `scripts/`.

## Technical Context

**Language/Version**: Markdown/JSON documentation (repo Python 3 skill suite unchanged).
**Primary Dependencies**: Existing `skills/core/artcraft_app_client.py` (v0.3.0, reference only), `skills/core/creative_skill.py` (reference only), 006/007 specs, `.specify/memory/constitution.md` v2.0.0, `.specify/templates/*`.
**Storage**: N/A (documentation artifacts only).
**Testing**: Existing default gates as regression guard: `PYTHONPATH=. python -m pytest -q` (expect 412 passed, 23 deselected or documented baseline), `python scripts/validate_all_skills.py` (12/12). No new tests; no test files modified.
**Target Platform**: Documentation for maintainers/agents; optional future real validation local opt-in only (007 pattern).
**Project Type**: Spec Kit documentation slice within Python skill-suite repo.
**Performance Goals**: N/A.
**Constraints**: Docs-only; defensive capability gating (no exact tool counts/catalog equality); no AI/provider/model/prompt claim; no stateful cross-call/artifact cycle; no bridge/UI; no CI/default real MCP smoke; preserve public schemas, `SkillResult`, FR-005/FR-006, CLI/fallback.
**Scale/Scope**: 1 assessment directory + 1 spec directory; capability tiers P1/P2/P3; contracts for mapping entries.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. Crafting Over Generating | PASS | Maps engine/editor capabilities; excludes AI generation claims. |
| II. Artist-Centric Design | PASS | Transparent limits and defensive gating; no false capability promises. |
| III. Open Source, Vendor-Neutral, Interoperable | PASS | MCP stdio reference; PhotoCraft as observed/documented target, not lock-in. |
| IV. Composability and Modularity | PASS | Capability reference supports future composable skills; no monolithic runtime change. |
| V. Performance and Native Execution | PASS | N/A (docs); future work bounded by existing adapter patterns. |
| VI. Quality Through Intentional Craft | PASS | Evidence tiers (observed/documented/unverified), minimal brittle assertions. |
| VII. Transparency, Reproducibility, Cost Awareness | PASS | Explicit limits, opt-in real validation only, no secrets/PII. |
| VIII. Extensibility Without Unnecessary Complexity | PASS | No new runtime deps/APIs; defers stateful/SDK migration. |

**Quality gates alignment**: functionality unchanged (gates green); documentation complete; compatibility preserved; composability unaffected; security/safety preserved (opt-in/roots/limits documented); graceful error semantics referenced (FR-006).

**Gate result (pre/post design)**: **PASS** — no violations. Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
.specify/assessments/008-photocraft-capability-mapping/
├── intake.md
├── problem.md
├── research.md
├── concept.md
└── decision.md

specs/008-photocraft-capability-mapping/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── spec.md
├── tasks.md
├── contracts/
│   └── capability-map-contract.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
# UNCHANGED by 008 (docs-only slice)
skills/core/artcraft_app_client.py   # reference: MCP stdio/FR-005/FR-006
skills/core/creative_skill.py        # reference: discover→resolve→invoke→normalize→degrade
tests/**                             # no changes
scripts/**                           # no changes
```

**Structure Decision**: Single spec/assessment documentation slice. No production code, no test code, no script changes. Future implementation (if any) requires a separate spec/task after 008 review.

## Phase 0: Research Output

- `specs/008-photocraft-capability-mapping/research.md` — consolidates 006/007 evidence, observed PhotoCraft 0.20.1 tools, public `storytold/photocraft` MCP docs, MCP 2025-11-25/2026-07-28 limits, SDK v2 backlog note.

## Phase 1: Design & Contracts Output

- `data-model.md` — Capability Map Entry, Tier, Safety Boundary, Evidence Record, Validation constraints.
- `contracts/capability-map-contract.md` — schema/fields for mapping entries, defensive gating rules, evidence statuses, exclusion rules.
- `quickstart.md` — how to review/use the map; future opt-in real validation pattern (007 controls), not executed now.
- `checklists/requirements.md` — reviewer checklist for FR/SC/limits.

## Implementation Notes (docs-only)

- No `src/`/`skills/`/`tests/` edits. Implementation tasks create/review documentation only.
- Preserve 006/007 references; do not renumber or rewrite history.
- Any future runtime follow-up (progress/cancel support, stateful Option B, SDK migration, skill mapping) = separate spec.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |