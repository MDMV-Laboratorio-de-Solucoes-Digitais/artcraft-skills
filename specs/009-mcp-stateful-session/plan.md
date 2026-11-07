# Implementation Plan: MCP stateful session helper (007 Option B)

**Branch**: `009-mcp-stateful-session` | **Date**: 2026-11-06 | **Spec**: `specs/009-mcp-stateful-session/spec.md`

## Summary

Docs-only Speckit slice specifying an **additive** MCP stateful session helper for deterministic engine/editor cross-call cycles (007 Option B), reusing 006 transport/FR-005/FR-006 patterns and 007/008 safety/gating constraints. **No runtime changes** to `skills/`, `tests/`, or `scripts/` in this slice.

## Technical Context

**Language/Version**: Markdown/JSON docs (Python repo unchanged).
**Primary Dependencies (reference only)**: `skills/core/artcraft_app_client.py` (006 stateless), `CreativeSkill`/`SkillResult`, specs 006/007/008, constitution v2.0.0.
**Storage**: N/A.
**Testing**: Regression guard only — existing gates (`PYTHONPATH=. python -m pytest -q`, `python scripts/validate_all_skills.py`). Future implementation MUST add mock-first deterministic session tests before runtime code.
**Target Platform**: Docs; future runtime local opt-in only.
**Project Type**: Spec Kit documentation slice.
**Constraints**: Additive helper; preserve 006 stateless APIs, schemas, FR-005/FR-006, CLI/fallback; engine/editor only; no AI; no bridge/UI; no CI/default real; opt-in real with 007 controls; MCP 2026-07-28 aware (client-retained process state).
**Scale/Scope**: 1 assessment + 1 spec directory.

## Constitution Check

| Principle | Status | Notes |
|---|---|---|
| I. Crafting Over Generating | PASS | Deterministic engine/editor cycle; no AI claim. |
| II. Artist-Centric Design | PASS | Transparent limits, structured failures. |
| III. Open Source/Vendor-Neutral | PASS | MCP stdio; PhotoCraft reference target only. |
| IV. Composability/Modularity | PASS | Additive helper; stateless APIs preserved. |
| V. Performance/Native | PASS | Bounded timeouts/cleanup required in contract. |
| VI. Quality/Intentional Craft | PASS | Defensive gating, evidence honesty. |
| VII. Transparency/Reproducibility | PASS | Mock-first future, opt-in real evidence. |
| VIII. Extensibility/Simplicity | PASS | Narrow 007 Option B scope; no SDK migration in slice. |

**Gate**: PASS. No violations.

## Project Structure

### Documentation

```text
.specify/assessments/009-mcp-stateful-session/{intake,problem,research,concept,decision}.md
specs/009-mcp-stateful-session/
├── spec.md plan.md research.md data-model.md quickstart.md tasks.md
├── contracts/stateful-session-contract.md
└── checklists/requirements.md
```

### Source (UNCHANGED)

`skills/`, `tests/`, `scripts/` — no modifications in 009 docs slice.

## Phase Outputs

- **Research**: 006 stateless boundary, 007/008 deferrals, MCP 2025-11-25/2026-07-28 limits.
- **Data model**: `MCPStatefulSession`, `SessionStepResult`, lifecycle, safety boundary.
- **Contract**: additive API shape (conceptual), lifecycle, FR-006 mapping, cleanup, gating.
- **Quickstart**: review steps; future implementation checklist (TDD/mock-first) and opt-in real pattern (007) — not executed.

## Future Implementation Notes (separate slice)

- Add helper in `skills/core/` (or test-local first) without breaking 006 exports.
- TDD: write failing deterministic session tests (fake stdio retained process) → implement → green; property tests for cleanup/id correlation where useful.
- Opt-in real smoke only with explicit authorization. No CI/default real.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| None | — | — |