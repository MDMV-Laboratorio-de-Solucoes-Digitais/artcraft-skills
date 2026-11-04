# Tasks: Shared CLI/MCP Adapter (003)

**Input**: Design documents from `/specs/003-shared-cli-mcp-adapter/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/artcraft_app_client.md, quickstart.md

**Tests**: TDD is REQUIRED. Every test task in the RED phase MUST be written first and MUST fail before its matching implementation task begins. Property-based tests use Hypothesis and assert invariants.

**Organization**: Tasks are grouped by user story (US1, US2, US3) to enable independent implementation and testing.

**Commit policy (deterministic hook)**: After EVERY file edit, create an atomic conventional commit (e.g. `feat(adapter): ...`, `test(adapter): ...`, `refactor(image-generate): ...`). Do not batch unrelated file changes into one commit. Verification tasks produce no commit unless a fix is required.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Adapter: `skills/core/artcraft_app_client.py`
- Skill: `skills/creative/image-generate/skill.py`
- Tests: `tests/unit/`, `tests/property/`, `tests/contract/`, `tests/characterization/`, `tests/reference/`
- Contract snapshot: `tests/contract/artcraft_app_client_api.json`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Capture baselines and prepare test scaffolding locations before any RED-phase test work.

- [x] T001 [P] Capture pre-refactor reference copy: copy `skills/creative/image-generate/skill.py` to `tests/reference/image_generate_original.py` (baseline for differential testing; do not modify after capture).
- [x] T002 [P] Create characterization directory scaffold `tests/characterization/` (with `__init__.py` if missing) for golden-master tests.
- [x] T003 Verify Hypothesis is available in the test environment (`python -c "import hypothesis"`); record version in `tests/property/test_artcraft_app_client_props.py` header if needed. No code change if already present.

**Checkpoint**: Baseline captured and test locations ready.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Contract snapshot and shared test helpers that ALL user-story test suites depend on. MUST complete before US1/US2/US3 implementation.

- [x] T004 [P] Create golden public-API snapshot `tests/contract/artcraft_app_client_api.json` listing the 9 public functions (`discover_cli`, `discover_generation_command`, `normalize_output`, `normalize_mcp_config`, `run_cli`, `discover_cli_commands`, `run_cli_generation`, `select_mode`, `standardize_error`) plus `__version__` and `__all__`, with expected signatures and return types per `contracts/artcraft_app_client.md`.
- [x] T005 [P] Add shared test helper utilities for canonicalizing `SkillResult` (success, data, error, metadata with timing pinned to `None`/`300`) under `tests/_helpers/` or inline in characterization tests; reusable by US2 differential/characterization suites.

**Checkpoint**: Foundation ready — user story work can begin.

---

## Phase 3: User Story 1 - Shared CLI/MCP Integration Layer (Priority: P1) 🎯 MVP

**Goal**: Deliver `skills/core/artcraft_app_client.py` as a function-based, stateless adapter with modernized, non-mutating signatures plus `select_mode`, `standardize_error`, `__version__`, `__all__`, and docstrings.

**Independent Test**: Import the adapter in an independent consumer module, exercise all 9 functions (edge cases + non-mutation), and confirm the public API matches the committed snapshot with zero unreviewed diff.

### Tests for User Story 1 (RED PHASE — write first, ensure FAIL) ⚠️

- [x] T010 [P] [US1] Unit tests in `tests/unit/test_artcraft_app_client.py`: cover each of the 9 functions (discover_cli, discover_generation_command, normalize_output, normalize_mcp_config, run_cli, discover_cli_commands, run_cli_generation, select_mode, standardize_error) including edge cases (None/empty inputs, missing CLI, nonzero exit, timeout, malformed JSON) and explicit non-mutation assertions for `normalize_output` and `normalize_mcp_config`.
- [x] T011 [P] [US1] Property tests in `tests/property/test_artcraft_app_client_props.py` (Hypothesis invariants): `normalize_output`/`normalize_mcp_config` never mutate input and are idempotent; `discover_generation_command` returns a member of input or override or None; `select_mode` returns only valid modes; `standardize_error` always contains keys {code, message, details, retryable}.
- [x] T012 [P] [US1] Contract tests in `tests/contract/test_artcraft_app_client.py`: importability from `skills.core`, presence of all 9 functions + `__version__`/`__all__`, snapshot diff against `tests/contract/artcraft_app_client_api.json` (zero unreviewed diff), and at least 7 distinct test functions.
- [x] T013 [US1] Run the US1 test suite and confirm RED (all new tests fail) before implementation; record failure summary in task notes. (No code changes.)

### Implementation for User Story 1

- [ ] T014 [US1] Update `skills/core/artcraft_app_client.py`: modernize signatures to `str | None`, `dict[str, Any]`, `list[str]`, `Mapping`/`Sequence` inputs with concrete returns; add Args/Returns/Raises/mutation docstrings; make `normalize_output(out=None, keys=None)` non-mutating and accept optional expected keys defaulting to image keys; make `normalize_mcp_config(cfg=None)` copy-first (no mutation); add `select_mode(requested_mode, cli_available, mcp_available) -> str` (pure, raises ValueError on invalid mode) and `standardize_error(reason, message, metadata=None) -> dict[str, Any]` (reason codes: cli_not_found, mcp_unavailable, neither_available, is_error); add `__version__ = "0.1.0"` and extend `__all__` to include all 9 functions. Preserve existing behavior of discover/run functions.
- [ ] T015 [US1] Update `contracts/artcraft_app_client.md` and `data-model.md` to reflect finalized signatures (verify; edit only if drift). 
- [ ] T016 [US1] Run US1 tests and confirm GREEN (all pass); fix any failures rooted in the adapter implementation (not tests).

**Checkpoint**: US1 adapter complete and independently testable.

---

## Phase 4: User Story 2 - Refactor image-generate to use shared adapter (Priority: P1)

**Goal**: Refactor `skills/creative/image-generate/skill.py` to delegate to adapter functions (including `select_mode`/`standardize_error`) while preserving exact behavior; all 23 tests pass.

**Independent Test**: Run all 23 existing image-generate tests + characterization golden master + differential (old vs new) + extended property tests; all pass.

### Tests for User Story 2 (RED PHASE — write first, ensure FAIL) ⚠️

- [ ] T020 [P] [US2] Characterization golden-master test in `tests/characterization/test_image_generate_behavior.py`: capture canonicalized `SkillResult` (success, data, error, metadata with mode/interface/command/exit_code/timeout_s/reason/is_error; timing pinned to None/300) for a curated scenario matrix (CLI success/failure/timeout, MCP unavailable, neither available, unsupported command, validation errors).
- [ ] T021 [P] [US2] Differential test in `tests/characterization/test_image_generate_differential.py`: import and run the pre-refactor reference from `tests/reference/image_generate_original.py` alongside the refactored skill; assert equality of canonicalized `SkillResult` across the same scenario matrix.
- [ ] T022 [P] [US2] Extend `tests/property/test_image_generate_props.py` with property tests covering adapter-backed paths (non-mutation of inputs, deterministic mode selection, equivalence under refactoring) while keeping existing 4 tests passing.
- [ ] T023 [US2] Run US2 test suites and confirm RED (characterization/differential/extended property fail) before refactoring; record failure summary.

### Implementation for User Story 2

- [ ] T024 [US2] Refactor `skills/creative/image-generate/skill.py`: delegate `_discover_cli`→`discover_cli`, `_discover_generation_command`→`discover_generation_command`, `_normalize_output`→`normalize_output`, `_normalize_mcp_config`→`normalize_mcp_config`; use `discover_cli_commands`/`run_cli_generation` in `_execute_cli`; replace inline mode decision with `select_mode`; use `standardize_error` for reason-code normalization; keep schemas, validation, param assembly, MCP stubs, orchestration, and `SkillResult` construction in the skill. Preserve exact output/error strings and metadata.
- [ ] T025 [US2] Remove any code in `skill.py` made obsolete by the cutover (duplicated discovery/normalization helpers) so no second convention remains; keep `_mcp_*` stubs.
- [ ] T026 [US2] Run US2 tests and confirm GREEN: all 23 existing image-generate tests pass, characterization + differential + extended property tests pass.

**Checkpoint**: US2 refactored and behaviorally equivalent.

---

## Phase 5: User Story 3 - Enable future creative skills (Priority: P2)

**Goal**: Demonstrate and verify adapter flexibility for future skills (image-edit, background-remove, image-upscale, mesh-generate) via documentation and a smoke example.

**Independent Test**: A minimal example consumer can import the adapter, configure custom keywords/override command, normalize arbitrary output keys, and select mode without skill-specific code.

### Tests for User Story 3 (RED PHASE — write first, ensure FAIL) ⚠️

- [ ] T030 [P] [US3] Add flexibility smoke test in `tests/unit/test_artcraft_app_client.py` (or new `tests/unit/test_artcraft_app_client_future_skills.py`) verifying custom keyword lists, `generation_command` override, arbitrary `keys` for `normalize_output`, and `select_mode` for all availability combinations.

### Implementation for User Story 3

- [ ] T031 [US3] Update `quickstart.md` with a future-skill usage example (custom keywords, override, arbitrary keys, mode selection) and note that future creative skills MUST use the shared adapter (no duplicated discovery/invocation).
- [ ] T032 [US3] Verify adapter has no skill-specific hardcoding (grep for image-generate-specific strings in adapter); document findings. No behavior change expected.

**Checkpoint**: US3 flexibility verified and documented.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and cleanup.

- [ ] T040 Run full pytest suite (`python -m pytest -q`) and confirm all suites green (unit, contract, integration, property, characterization), including `tests/integration/test_image_generate_composition.py`.
- [ ] T041 Run `python scripts/validate_skill.py skills/creative/image-generate` and confirm exit 0.
- [ ] T042 Run `python scripts/validate_all_skills.py` and confirm exit 0 (no regressions).
- [ ] T043 Verify all checklist items in `specs/003-shared-cli-mcp-adapter/checklists/` are marked `[x]`; re-mark any that the implementation now satisfies. (Already done in prior step; verify only.)
- [ ] T044 Review `git diff` for accidental changes, leftover scaffolding, or duplicated helpers; remove throwaway scripts. Confirm only intended files changed.
- [ ] T045 (Optional) Add CHANGELOG entry for adapter `__version__ = "0.1.0"` if a CHANGELOG exists; otherwise skip.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **US1 (Phase 3)**: Depends on Foundational. Blocks US2 (skill refactor depends on adapter API).
- **US2 (Phase 4)**: Depends on US1 implementation (T014 complete).
- **US3 (Phase 5)**: Depends on US1; can run in parallel with US2 test writing but implementation after adapter stable.
- **Polish (Phase 6)**: Depends on all user stories complete.

### User Story Dependencies

- **US1 (P1)**: No dependency on other stories.
- **US2 (P1)**: Depends on US1 adapter API; independently testable via characterization/differential.
- **US3 (P2)**: Depends on US1; independent of US2.

### Within Each User Story

- Tests (RED) MUST be written and FAIL before implementation.
- Implementation tasks are sequential within a story.
- Run tests (GREEN) only after implementation.

### Parallel Opportunities

- T001, T002, T003 (Setup) can run in parallel.
- T004, T005 (Foundational) can run in parallel.
- T010, T011, T012 (US1 RED tests) can run in parallel.
- T020, T021, T022 (US2 RED tests) can run in parallel.
- T030 (US3) can run in parallel with US2 test writing.
- Different user stories can be worked on in parallel by different developers after US1 implementation lands.

---

## Parallel Example: User Story 1

```bash
# Launch all US1 RED tests together:
Task: "Unit tests in tests/unit/test_artcraft_app_client.py"
Task: "Property tests in tests/property/test_artcraft_app_client_props.py"
Task: "Contract tests in tests/contract/test_artcraft_app_client.py"
```

## Parallel Example: User Story 2

```bash
# Launch all US2 RED tests together:
Task: "Characterization golden master in tests/characterization/test_image_generate_behavior.py"
Task: "Differential test in tests/characterization/test_image_generate_differential.py"
Task: "Extend property tests in tests/property/test_image_generate_props.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 (adapter)
4. **STOP and VALIDATE**: Run adapter unit/property/contract tests
5. Adapter usable by independent consumers

### Incremental Delivery

1. Setup + Foundational → ready
2. US1 → adapter complete (MVP)
3. US2 → image-generate refactored, behavior preserved
4. US3 → future-skill flexibility verified
5. Polish → all tests green, validators pass

### Parallel Team Strategy

With multiple developers:
1. Team completes Setup + Foundational together
2. Developer A: US1 (adapter) — blocks US2
3. Developer B: US2 test authoring (RED) while A implements
4. Developer C: US3 test authoring + docs

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Verify tests FAIL before implementing; verify GREEN after
- Commit after each task or logical group (atomic conventional commits)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence
- RED-phase test tasks (T010-T013, T020-T023, T030) must be completed and observed failing before their matching implementation tasks begin.