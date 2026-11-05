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

---

## Phase 1: Setup
**Purpose**: Project preparation
- [ ] T001 Review current implementation of artcraft_app_client and creative skills

---

## Phase 2: Foundational
**Purpose**: Core infrastructure
- [ ] T002 Add `generate_via_editing_commands` to `skills/core/artcraft_app_client.py`
- [ ] T003 Update contract snapshot `tests/contract/artcraft_app_client_api.json`

---

## Phase 3: User Story 1 - Descobrir comandos de geração reais (Priority: P1)
**Goal**: Ensure discovery of real generation commands works via CLI/MCP
**Independent Test**: With generation commands available, skill uses them

### Implementation for User Story 1
- [ ] T004 [US1] Enhance discovery to better support generation commands in `artcraft_app_client.py`
- [ ] T005 [US1] Ensure keyword configuration works via inputs in creative skills

**Checkpoint**: Discovery of real generation commands functional

---

## Phase 4: User Story 2 - Fallback para comandos de edição (Priority: P1)
**Goal**: Add fallback using editing commands when no generation available
**Independent Test**: Without generation commands, skill generates pixel art via editing

### Implementation for User Story 2
- [ ] T006 [US2] Add fallback logic to `skills/core/creative_skill.py`
- [ ] T007 [US2] Add fallback logic to `skills/creative/image-generate/skill.py`
- [ ] T008 [US2] Ensure fallback respects dimensions and produces valid PNG

**Checkpoint**: Fallback functional

---

## Phase 5: Polish & Cross-Cutting Concerns
**Purpose**: Final verification

- [ ] T009 Run all tests: `python -m pytest -q` to ensure no regressions
- [ ] T010 Verify all 12 skills still valid: `python scripts/validate_all_skills.py`
- [ ] T011 Atomic commit with summary

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
