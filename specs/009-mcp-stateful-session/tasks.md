---
description: "Tasks for MCP stateful session (009 / 007 Option B, docs-only)"
---

# Tasks: MCP stateful session helper (007 Option B)

**Input**: `specs/009-mcp-stateful-session/`, `.specify/assessments/009-mcp-stateful-session/`
**Tests**: N/A (docs-only). Future runtime implementation requires TDD/mock-first (see plan/quickstart).

## Phase 1: Setup

- [x] T001 Confirm GO decision and 007 Option B scope in assessment `decision.md` and `spec.md`.
- [x] T002 [P] Create/verify spec directory structure (`contracts/`, `checklists/`).

## Phase 2: Foundational

- [x] T003 [P] Define session lifecycle/data model in `data-model.md`.
- [x] T004 [P] Define additive contract in `contracts/stateful-session-contract.md`.
- [x] T005 [P] Consolidate protocol/006-008 constraints in `research.md`.

## Phase 3: US1 — Additive stateful contract (P1)

- [x] T006 [US1] Author FR/SC for lifecycle, cleanup, FR-006, additive API in `spec.md`.
- [x] T007 [P] [US1] Document review/future implementation checklist in `quickstart.md`.

## Phase 4: US2 — Deterministic engine/editor cycle + safety (P1)

- [x] T008 [US2] Specify gated deterministic cycle and safety controls in `spec.md` and `contracts/stateful-session-contract.md`.
- [x] T009 [P] [US2] Complete reviewer checklist in `checklists/requirements.md`.

## Phase 5: US3 — Protocol/contract compatibility (P2)

- [x] T010 [US3] Document MCP 2026-07-28 limits, FR-005/FR-006/schema preservation in `plan.md`, `research.md`, `spec.md`.

## Phase 6: Polish

- [x] T011 [P] Update `OBJETIVO.md`, `ROADMAP.md`, `docs/AVALIACAO_ANDAMENTO_SPECKIT.md` for 009 status (docs-only, factual).
- [x] T012 Verify gates: pytest default + `validate_all_skills.py`; confirm no `skills/`/`tests/`/`scripts/` changes.

## Notes

- Docs-only. No AI generation, no bridge/UI, no CI/default real, no server-side session assumption (2026-07-28 path). Preserve 006 stateless APIs.