# Tasks: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

**Input**: Design documents from `/specs/005-resiliencia-creativeskill/`
**Prerequisites**: plan.md (required), spec.md (required), research.md

**Tests**: Tests are OPTIONAL - follow TDD approach per user request.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2)

## Path Conventions
- **Core**: `skills/core/creative_skill.py`
- **Tests**: `tests/`

## Reconciliation Note (2026-11-06, doc hygiene — evidence-based)

T001–T015 were historically left as `- [ ] ... [X]` placeholders; **implementation and FR/SC satisfaction are evidenced by the 2026-11-05 convergence closure (T016–T018)** and by current repository state. Markers below are reconciled to `[x]` **only on that recorded evidence** (not a new implementation pass): `skills/core/creative_skill.py` contains bounded semaphore/retry+backoff+jitter in CLI execution path; resilience tests and full gates have passing evidence (`373 passed, 12/12` at closure; default gates re-verified 2026-11-06 as `412 passed, 23 deselected, 12/12 valid`). History preserved; no code/contracts changed by this note.

---

## Phase 1: Setup
**Purpose**: Project preparation
- [x] T001 Review current `skills/core/creative_skill.py` implementation and existing tests *(reconciled 2026-11-06 with T016–T018 convergence evidence)*

---

## Phase 2: Foundational
**Purpose**: Core infrastructure - no foundational blocking needed

---

## Phase 3: User Story 1 - Skills resilientes a falhas transientes (Priority: P1) 🎯 MVP
**Goal**: Add retry with exponential backoff + jitter and concurrency semaphore to CreativeSkill
**Independent Test**: Skills retry on transient CLI failures and respect concurrency limits

### Tests for User Story 1 (TDD - Write FIRST, RED phase)
- [x] T002 [P] [US1] Add property test for retry behavior in `tests/property/test_creative_skills_resilience_props.py` (RED) *(reconciled 2026-11-06; evidence: resilience tests pass, convergence T016–T018)*
- [x] T003 [P] [US1] Add characterization tests for retry/backoff/semaphore in `tests/characterization/test_creative_skills_resilience_behavior.py` (RED) *(reconciled 2026-11-06; evidence: resilience tests pass, convergence T016–T018)*

### Implementation for User Story 1
- [x] T004 [US1] Add imports (`threading`, `time`, `random`) to `skills/core/creative_skill.py` *(reconciled 2026-11-06; implementation present, T016–T018)*
- [x] T005 [US1] Add semaphore (`threading.BoundedSemaphore(3)`) as instance attribute in `CreativeSkill.__init__` *(reconciled 2026-11-06; implementation present, T016–T018)*
- [x] T006 [US1] Implement retry logic with exponential backoff + jitter (max 3 attempts) in `CreativeSkill._execute_cli` *(reconciled 2026-11-06; implementation present in CLI fallback execution path, T016–T018)*
- [x] T007 [US1] Wrap CLI execution with semaphore in `CreativeSkill._execute_cli` *(reconciled 2026-11-06; implementation present, T016–T018)*
- [x] T008 [US1] Ensure TimeoutExpired and appropriate errors are retried, preserving metadata on final failure *(reconciled 2026-11-06; evidence T016–T018 FR-003)*

**Checkpoint**: User Story 1 should be functional and testable independently *(evidenced 2026-11-05/06)*

---

## Phase 4: User Story 2 - Backward compatibility (Priority: P1)
**Goal**: Ensure no breaking changes to existing contracts
**Independent Test**: All existing tests pass

### Implementation for User Story 2
- [x] T009 [US2] Ensure `SkillResult` structure unchanged and metadata preserved *(reconciled 2026-11-06; evidence T016–T018 FR-004/SC-004)*
- [x] T010 [US2] Verify mocks in existing tests continue to work *(reconciled 2026-11-06; regression gates pass)*
- [x] T011 [US2] Run existing creative skills tests to confirm backward compatibility *(reconciled 2026-11-06; full suite/regression evidence)*

**Checkpoint**: Backward compatibility maintained *(evidenced)*

---

## Phase 5: Polish & Cross-Cutting Concerns
**Purpose**: Final verification

- [x] T012 Run resilience tests: `python -m pytest tests/property/test_creative_skills_resilience_props.py tests/characterization/test_creative_skills_resilience_behavior.py -v` *(reconciled 2026-11-06; 6 passed recorded at closure; repo gates green 2026-11-06)*
- [x] T013 Run full test suite: `python -m pytest -q` to ensure no regressions (target: 351+ tests passing) *(reconciled 2026-11-06; 373 passed at closure; 412 passed, 23 deselected re-verified 2026-11-06)*
- [x] T014 Verify all 5 creative skills benefit from base class changes *(reconciled 2026-11-06; CreativeSkill base path evidenced, FR-005/SC-005)*
- [x] T015 Atomic commit with detailed summary of edits made *(reconciled 2026-11-06; implementation committed in feature history; this doc reconciliation committed separately)*

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: No dependencies
- **User Story 1 (Phase 3)**: Can start after Setup (tests first)
- **User Story 2 (Phase 4)**: Depends on User Story 1
- **Polish (Phase 5)**: Depends on all user stories complete

### Parallel Opportunities
- T002, T003 can run in parallel (different test files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1
2. Write tests T002-T003 (RED)
3. Implement T004-T008
4. Verify tests pass
5. Ensure backward compatibility (Phase 4)


## Phase 6: Convergence

**Purpose**: Formal closure via converge process

- [x] T016 Run `/speckit.converge` validation for feature 005
- [x] T017 Verify all FR-001 through FR-005 and SC-001 through SC-005 are satisfied
- [x] T018 Document convergence completion


**Evidence (2026-11-05, T016-T018 / convergence closure)**:
- `skills/core/creative_skill.py`: `_cli_semaphore = threading.BoundedSemaphore(3)`, retry loop (max 3) with exponential backoff + jitter (`_retry_backoff_base * 2**attempt + random.uniform(0,0.1)`), retries on timeout/transient CLI failures, semaphore wraps CLI execution.
- Resilience tests pass: `6 passed` (`tests/property/test_creative_skills_resilience_props.py`, `tests/characterization/test_creative_skills_resilience_behavior.py`).
- Backward compatibility: `373 passed`, `12/12 skills validated` (full suite/regression check 2026-11-05). SkillResult contract preserved.
- FR coverage: FR-001 retry+backoff+jitter (max 3) ✓; FR-002 semaphore max 3 ✓; FR-003 transient timeout/error retry ✓; FR-004 additive/contract-preserving ✓; FR-005 benefits all CreativeSkill heirs ✓.
- SC coverage: SC-001 transient timeout retry ✓; SC-002 concurrency limited to 3 ✓; SC-003 existing tests pass (373) ✓; SC-004 SkillResult unchanged ✓; SC-005 centralized in base class ✓.

- Convergence check (2026-11-05): no new gaps found; feature 005 satisfied per FR-001..FR-005 and SC-001..SC-005 with implementation+test evidence above. No additional Phase appended.
