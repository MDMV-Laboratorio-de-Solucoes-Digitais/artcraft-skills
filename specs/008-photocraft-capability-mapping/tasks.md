---
description: "Task list for PhotoCraft MCP capability mapping (008)"
---

# Tasks: PhotoCraft MCP capability mapping (engine/editor)

**Input**: `specs/008-photocraft-capability-mapping/` + `.specify/assessments/008-photocraft-capability-mapping/`
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, assessment `decision.md` (GO)

**Tests**: **N/A (docs-only slice)**. No new automated tests. Regression guard = existing default gates (Phase 3). No files in `skills/`, `tests/`, or `scripts/` modified.

**Organization**: Tasks grouped by user story. All `[P]` tasks touch disjoint files.

## Format: `[ID] [P?] [Story?] Description`

## Phase 1: Setup (Assessment & Structure)

- [x] T001 Confirm GO decision and scope/limits in `.specify/assessments/008-photocraft-capability-mapping/decision.md` and `specs/008-photocraft-capability-mapping/spec.md` (docs-only; no runtime changes).
- [x] T002 [P] Create/verify directory structure `specs/008-photocraft-capability-mapping/{contracts,checklists}/` and assessment directory `.specify/assessments/008-photocraft-capability-mapping/`.

## Phase 2: Foundational (Mapping Contract)

- [x] T003 [P] Define capability entry schema/rules in `specs/008-photocraft-capability-mapping/contracts/capability-map-contract.md` (defensive gating, evidence tiers, exclusions).
- [x] T004 [P] Define entities/validation in `specs/008-photocraft-capability-mapping/data-model.md`.
- [x] T005 [P] Consolidate evidence/decisions in `specs/008-photocraft-capability-mapping/research.md`.

**Checkpoint**: Mapping contract/evidence model ready for user-story documentation.

## Phase 3: User Story 1 — Defensive capability map (P1) 🎯 MVP

**Goal**: Maintainers/agents can consume a defensible capability map with tiers, gating, constraints, and evidence.
**Independent Test**: Spec + contract answer tier/discovery/safety/exclusion questions (SC-004).

- [x] T006 [US1] Author capability map requirements and tiers in `specs/008-photocraft-capability-mapping/spec.md` (FR-001–FR-004, FR-007–FR-009, scenarios/edge cases).
- [x] T007 [P] [US1] Document review/runbook usage in `specs/008-photocraft-capability-mapping/quickstart.md`.

## Phase 4: User Story 2 — Contracts/safety preserved (P1)

**Goal**: Docs-only slice preserves 006/007/FR-005/FR-006/public contracts and opt-in safety.
**Independent Test**: No `skills/`/`tests/`/`scripts/` diffs; gates green (SC-002, SC-003).

- [x] T008 [US2] Record explicit exclusions/preservation in `specs/008-photocraft-capability-mapping/spec.md` and `specs/008-photocraft-capability-mapping/plan.md` (FR-005, FR-006; no AI/stateful/bridge/CI-default).
- [x] T009 [P] [US2] Complete reviewer checklist in `specs/008-photocraft-capability-mapping/checklists/requirements.md`.

## Phase 5: User Story 3 — Future evolution boundaries (P2)

**Goal**: Clear separation of 006 stateless adapter, 007 evidence, 008 mapping, and deferred Option B/SDK/adapter support.
**Independent Test**: Plan/quickstart/research point to correct deferrals (SC-005).

- [x] T010 [US3] Document deferrals and protocol limits in `specs/008-photocraft-capability-mapping/research.md`, `specs/008-photocraft-capability-mapping/plan.md`, and `specs/008-photocraft-capability-mapping/quickstart.md`.

## Phase 6: Polish & Cross-Cutting

- [x] T011 [P] Update `OBJETIVO.md` and `ROADMAP.md` references for 008 80/20 status (docs-only, factual).
- [x] T012 [P] Record Speckit assessment coverage in `.specify/assessments/008-photocraft-capability-mapping/{intake,problem,research,concept,decision}.md`.

## Dependencies & Execution Order

- Phase 1 → Phase 2 → US1/US2/US3 (US1/US2 P1 can proceed after Phase 2; file ownership: `spec.md` edited sequentially/same agent). → Phase 6.
- T003/T004/T005 parallel (disjoint files). T007/T009/T011/T012 parallel where disjoint.

## Notes

- **Docs-only**: MUST NOT modify `skills/`, `tests/`, `scripts/`.
- **Defensive gating**: no exact tool counts/catalog equality.
- **Exclusions**: no AI generation claim; no stateful cross-call (007 Option B deferred); no bridge/UI headless scope; no CI/default real MCP smoke.
- Validation real future: opt-in + autorização explícita + controles 007.