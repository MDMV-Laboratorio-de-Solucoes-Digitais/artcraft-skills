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

---

## Phase 1: Setup
**Purpose**: Project preparation
- [ ] T001 [X] Review current `skills/core/creative_skill.py` implementation and existing tests

---

## Phase 2: Foundational
**Purpose**: Core infrastructure - no foundational blocking needed

---

## Phase 3: User Story 1 - Skills resilientes a falhas transientes (Priority: P1) 🎯 MVP
**Goal**: Add retry with exponential backoff + jitter and concurrency semaphore to CreativeSkill
**Independent Test**: Skills retry on transient CLI failures and respect concurrency limits

### Tests for User Story 1 (TDD - Write FIRST, RED phase)
- [ ] T002 [X] [P] [US1] Add property test for retry behavior in `tests/property/test_creative_skills_resilience_props.py` (RED)
- [ ] T003 [X] [P] [US1] Add characterization tests for retry/backoff/semaphore in `tests/characterization/test_creative_skills_resilience_behavior.py` (RED)

### Implementation for User Story 1
- [ ] T004 [X] [US1] Add imports (`threading`, `time`, `random`) to `skills/core/creative_skill.py`
- [ ] T005 [X] [US1] Add semaphore (`threading.BoundedSemaphore(3)`) as instance attribute in `CreativeSkill.__init__`
- [ ] T006 [X] [US1] Implement retry logic with exponential backoff + jitter (max 3 attempts) in `CreativeSkill._execute_cli`
- [ ] T007 [X] [US1] Wrap CLI execution with semaphore in `CreativeSkill._execute_cli`
- [ ] T008 [X] [US1] Ensure TimeoutExpired and appropriate errors are retried, preserving metadata on final failure

**Checkpoint**: User Story 1 should be functional and testable independently

---

## Phase 4: User Story 2 - Backward compatibility (Priority: P1)
**Goal**: Ensure no breaking changes to existing contracts
**Independent Test**: All existing tests pass

### Implementation for User Story 2
- [ ] T009 [X] [US2] Ensure `SkillResult` structure unchanged and metadata preserved
- [ ] T010 [X] [US2] Verify mocks in existing tests continue to work
- [ ] T011 [X] [US2] Run existing creative skills tests to confirm backward compatibility

**Checkpoint**: Backward compatibility maintained

---

## Phase 5: Polish & Cross-Cutting Concerns
**Purpose**: Final verification

- [ ] T012 [X] Run resilience tests: `python -m pytest tests/property/test_creative_skills_resilience_props.py tests/characterization/test_creative_skills_resilience_behavior.py -v`
- [ ] T013 [X] Run full test suite: `python -m pytest -q` to ensure no regressions (target: 351+ tests passing)
- [ ] T014 [X] Verify all 5 creative skills benefit from base class changes
- [ ] T015 [X] Atomic commit with detailed summary of edits made

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

- [ ] T016 [X] Run `/speckit.converge` validation for feature 005
- [ ] T017 [X] Verify all FR-001 through FR-005 and SC-001 through SC-005 are satisfied
- [ ] T018 [X] Document convergence completion


**Evidence (2026-11-05, T016-T018 / convergence closure)**:
- `skills/core/creative_skill.py`: `_cli_semaphore = threading.BoundedSemaphore(3)`, retry loop (max 3) with exponential backoff + jitter (`_retry_backoff_base * 2**attempt + random.uniform(0,0.1)`), retries on timeout/transient CLI failures, semaphore wraps CLI execution.
- Resilience tests pass: `6 passed` (`tests/property/test_creative_skills_resilience_props.py`, `tests/characterization/test_creative_skills_resilience_behavior.py`).
- Backward compatibility: `373 passed`, `12/12 skills validated` (full suite/regression check 2026-11-05). SkillResult contract preserved.
- FR coverage: FR-001 retry+backoff+jitter (max 3) ✓; FR-002 semaphore max 3 ✓; FR-003 transient timeout/error retry ✓; FR-004 additive/contract-preserving ✓; FR-005 benefits all CreativeSkill heirs ✓.
- SC coverage: SC-001 transient timeout retry ✓; SC-002 concurrency limited to 3 ✓; SC-003 existing tests pass (373) ✓; SC-004 SkillResult unchanged ✓; SC-005 centralized in base class ✓.
