# Tasks: Integração de geração de assets com ArtCraft

**Input**: Design documents from `/specs/006-integracao-geracao-assets/`
**Prerequisites**: plan.md (required), spec.md (required)

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

## Path Conventions
- **Core**: `skills/core/`
- **Skills**: `skills/creative/`
- **Tests**: `tests/`

## Reconciliation & Disambiguation Note (2026-11-06, doc hygiene — evidence-based; no history rewrite)

**Historical numbering ambiguity:** this spec (`006-integracao-geracao-assets`) is **not** the same scope as [`../006-mcp-stdio-functional-integration/`](../006-mcp-stdio-functional-integration/) (MCP stdio mínimo viável, FR-005/FR-006, mock-first). Both share the `006-*` prefix in history; references should be explicit by full directory name.

**Status (reconciled with verifiable evidence, not a new implementation pass):** core implementation artifacts are present in the current tree — `generate_via_editing_commands` exists in `skills/core/artcraft_app_client.py` and in `tests/contract/artcraft_app_client_api.json`; fallback/editing-command paths are present in `skills/core/creative_skill.py` and `skills/creative/image-generate/skill.py`. Default gates re-verified **2026-11-06**: **412 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`), **12/12 skills validated** (`python scripts/validate_all_skills.py`). Markers below are reconciled on that evidence; if a dedicated convergence record for this exact spec is required, add it in a separate evidence pass without changing contracts.

---

## Phase 1: Setup
**Purpose**: Project preparation
- [x] T001 Review current implementation of artcraft_app_client and creative skills *(reconciled 2026-11-06 with codebase/gate evidence; original review timestamp not separately recorded in this file)*

---

## Phase 2: Foundational
**Purpose**: Core infrastructure
- [x] T002 Add `generate_via_editing_commands` to `skills/core/artcraft_app_client.py` *(reconciled 2026-11-06: symbol present)*
- [x] T003 Update contract snapshot `tests/contract/artcraft_app_client_api.json` *(reconciled 2026-11-06: entry present)*

---

## Phase 3: User Story 1 - Descobrir comandos de geração reais (Priority: P1)
**Goal**: Ensure discovery of real generation commands works via CLI/MCP
**Independent Test**: With generation commands available, skill uses them

### Implementation for User Story 1
- [x] T004 [US1] Enhance discovery to better support generation commands in `artcraft_app_client.py` *(reconciled 2026-11-06: implementation present in current adapter; dedicated per-scenario evidence may live outside this file)*
- [x] T005 [US1] Ensure keyword configuration works via inputs in creative skills *(reconciled 2026-11-06: CreativeSkill/adapter support keyword-driven config in current tree; see tests/gates)*

**Checkpoint**: Discovery of real generation commands functional *(evidence-based reconciliation)*

---

## Phase 4: User Story 2 - Fallback para comandos de edição (Priority: P1)
**Goal**: Add fallback using editing commands when no generation available
**Independent Test**: Without generation commands, skill generates pixel art via editing

### Implementation for User Story 2
- [x] T006 [US2] Add fallback logic to `skills/core/creative_skill.py` *(reconciled 2026-11-06: fallback path present)*
- [x] T007 [US2] Add fallback logic to `skills/creative/image-generate/skill.py` *(reconciled 2026-11-06: fallback usage present)*
- [x] T008 [US2] Ensure fallback respects dimensions and produces valid PNG *(reconciled 2026-11-06: implementation present; default gates green 2026-11-06)*

**Checkpoint**: Fallback functional *(evidence-based reconciliation)*

---

## Phase 5: Polish & Cross-Cutting Concerns
**Purpose**: Final verification

- [x] T009 Run all tests: `python -m pytest -q` to ensure no regressions *(reconciled 2026-11-06: 412 passed, 23 deselected)*
- [x] T010 Verify all 12 skills still valid: `python scripts/validate_all_skills.py` *(reconciled 2026-11-06: 12/12, all_valid=True)*
- [x] T011 Atomic commit with summary *(reconciled 2026-11-06: implementation merged in history; this reconciliation committed as doc hygiene)*

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Story 1 (Phase 3)**: Depends on Foundational
- **User Story 2 (Phase 4)**: Depends on Foundational
- **Polish (Phase 5)**: Depends on both user stories

### Parallel Opportunities
- T004, T005 can run in parallel (different concerns)
- T006, T007 can run in parallel (different files)
