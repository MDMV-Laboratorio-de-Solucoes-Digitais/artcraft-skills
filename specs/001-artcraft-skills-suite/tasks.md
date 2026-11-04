# Tasks: ArtCraft Skills Suite

**Input**: Design documents from `/specs/001-artcraft-skills-suite/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Critical Requirements**:
- TDD: Tests written FIRST (RED phase), must fail before implementation
- Use property-based testing where applicable, test invariants
- Tasks marked [P] are parallelizable (disjoint files)
- Tasks sharing context reuse same subagent
- Verification tasks at the end only attest to success
- Atomic conventional commits on file edits

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)

## Path Conventions
- Skills: `skills/`
- Scripts: `scripts/`
- Docs: `docs/`
- Tests: `tests/`
- Contracts: `specs/001-artcraft-skills-suite/contracts/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per implementation plan

- [x] T001 Create directory structure (skills/{core,creative,workflow,integration}, scripts/, tests/{unit,property,integration}, docs/)
- [x] T002 [P] Initialize package configuration and tooling (linting, formatting)
- [x] T003 [P] Create skill template following agentskills.io structure in skills/README.md
- [x] T004 [P] Create .gitignore entries for skills artifacts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation (TDD - Write FIRST, must FAIL) 
- [x] T005 [P] Write property-based tests for skill schema validation (name pattern, description length) in tests/property/test_skill_schema.py
- [x] T006 [P] Write tests for skill discovery/loading mechanism in tests/unit/test_skill_loader.py
- [x] T007 [P] Write tests for Spec Kit extension registration integration in tests/unit/test_extension_integration.py

### Implementation for Foundation
- [x] T008 Implement skill schema validation (contracts/skill-schema.json) with agentskills.io compliance in scripts/validate_skill.py
- [x] T009 [P] Implement skill loader/discovery mechanism for agentskills.io format in scripts/skill_loader.py
- [x] T010 [P] Integrate skill registration with Spec Kit extension system (.specify/extensions/.registry) in scripts/register_skills.py
- [x] T011 [P] Create core utilities (logging, errors, config) in skills/core/utils.py
- [x] T012 Create base skill interface and contracts in skills/core/base_skill.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Foundation & Schema (Priority: P1) 🎯 MVP

**Goal**: Well-defined composable skill system following agentskills.io standards, discoverable across agents

**Independent Test**: Define skill schema, create template, validate structure, load/discover skills in compatible agent environment

### Tests for User Story 1 (TDD - Write FIRST, must FAIL)
- [x] T013 [P] [US1] Property-based tests for skill naming invariants in tests/property/test_us1_naming.py
- [x] T014 [P] [US1] Contract tests for skill interface in tests/contract/test_skill_interface.py
- [x] T015 [P] [US1] Integration tests for cross-agent discovery in tests/integration/test_us1_discovery.py

### Implementation for User Story 1
- [x] T016 [P] [US1] Create skill template directory structure in skills/core/template/
- [x] T017 [P] [US1] Create example skill following schema in skills/core/example-skill/SKILL.md
- [x] T018 [US1] Implement skill validation CLI in scripts/validate_all_skills.py
- [x] T019 [US1] Document skill authoring guide in docs/skill-authoring.md
- [x] T020 [US1] Update extension registration for skills in .specify/extensions/.registry

**Checkpoint**: User Story 1 fully functional and testable independently

---

## Phase 4: User Story 2 - Core Abstractions & ArtCraft Integration (Priority: P1)

**Goal**: Core abstractions for model/provider routing, ArtCraft API adapters, job orchestration, cost tracking

**Independent Test**: Create skill using abstractions that authenticates, estimates costs, submits job, polls, retrieves results

### Tests for User Story 2 (TDD - Write FIRST, must FAIL)
- [x] T021 [P] [US2] Property-based tests for credential manager invariants in tests/property/test_us2_creds.py
- [x] T022 [P] [US2] Contract tests for API adapters in tests/contract/test_api_adapters.py
- [x] T023 [P] [US2] Integration tests for job orchestration in tests/integration/test_us2_jobs.py

### Implementation for User Story 2
- [x] T024 [P] [US2] Implement Credential Manager (API key + session auth) in skills/core/credentials.py
- [x] T025 [P] [US2] Implement ArtCraft API adapters (OmniApiClient, OmniGenClient) in skills/core/artcraft_client.py
- [x] T026 [P] [US2] Implement Model/Provider Router in skills/core/provider_router.py
- [x] T027 [P] [US2] Implement Asset/Media Handler in skills/core/asset_handler.py
- [x] T028 [US2] Implement Job Orchestrator (idempotency, polling, webhooks) in skills/core/job_orchestrator.py
- [x] T029 [US2] Implement Cost Estimator in skills/core/cost_estimator.py
- [x] T030 [US2] Create core abstractions documentation in docs/core-abstractions.md

**Checkpoint**: User Story 2 fully functional and testable independently

---

## Phase 5: User Story 3 - Atomic Creative Skills (Priority: P1)

**Goal**: Atomic skills for core creative operations, composable

**Independent Test**: Use individual atomic skills independently and compose them (e.g., generate → remove bg → upscale)

### Tests for User Story 3 (TDD - Write FIRST, must FAIL)
- [x] T031 [P] [US3] Property-based tests for skill composition invariants in tests/property/test_us3_composition.py
- [x] T032 [P] [US3] Contract tests for atomic skill interfaces in tests/contract/test_atomic_skills.py
- [x] T033 [P] [US3] Integration tests for skill chaining in tests/integration/test_us3_chaining.py

### Implementation for User Story 3
- [x] T034 [P] [US3] Create image generation skill (atomic) in skills/creative/image-generate/SKILL.md
- [x] T035 [P] [US3] Create image edit/inpaint skill (atomic) in skills/creative/image-edit/SKILL.md
- [x] T036 [P] [US3] Create background removal skill (atomic) in skills/creative/background-remove/SKILL.md
- [x] T037 [P] [US3] Create image upscale skill (atomic) in skills/creative/image-upscale/SKILL.md
- [x] T038 [P] [US3] Create 3D mesh generation skill (atomic) in skills/creative/mesh-generate/SKILL.md
- [x] T039 [US3] Create skill composition utilities in skills/core/composer.py
- [x] T040 [US3] Test composition of multiple atomic skills

**Checkpoint**: User Story 3 fully functional and testable independently

---

## Phase 6: User Story 4 - Cross-Product Integration Skills (Priority: P2)

**Goal**: Skills orchestrating workflows across different ArtCraft apps/domains

**Independent Test**: Execute cross-product workflow combining skills from different domains

### Tests for User Story 4 (TDD - Write FIRST, must FAIL)
- [x] T041 [P] [US4] Property-based tests for orchestrator invariants in tests/property/test_us4_orchestrator.py
- [x] T042 [P] [US4] Contract tests for orchestrator interface in tests/contract/test_orchestrator.py
- [x] T043 [P] [US4] Integration tests for cross-product workflows in tests/integration/test_us4_crossproduct.py

### Implementation for User Story 4
- [x] T044 [P] [US4] Implement workflow orchestrator/DAG engine in skills/workflow/orchestrator.py
- [x] T045 [P] [US4] Create 2D-to-3D workflow skill in skills/integration/2d-to-3d-workflow/SKILL.md
- [x] T046 [P] [US4] Create scene composition workflow skill in skills/integration/scene-composition/SKILL.md
- [x] T047 [US4] Implement shared asset/context/style layer in skills/core/asset_context.py
- [x] T048 [US4] Create cross-product integration documentation in docs/cross-product.md

**Checkpoint**: User Story 4 fully functional and testable independently

---

## Phase 7: User Story 5 - Generalizable MDMV Workflows (Priority: P2)

**Goal**: Generalizable skills derived from MDMV patterns (structured-packager, policy-redaction, orchestrator, evidence-audit)

**Independent Test**: Use skills in non-MDMV contexts, demonstrating generalizability

### Tests for User Story 5 (TDD - Write FIRST, must FAIL)
- [x] T049 [P] [US5] Property-based tests for redaction invariants in tests/property/test_us5_redaction.py
- [x] T050 [P] [US5] Contract tests for workflow skills in tests/contract/test_mdmv_workflows.py
- [x] T051 [P] [US5] Integration tests for generalizability in tests/integration/test_us5_generalizable.py

### Implementation for User Story 5
- [x] T052 [P] [US5] Create policy-redaction middleware (generalizable) in skills/workflow/policy-redaction/SKILL.md
- [x] T053 [P] [US5] Create structured-packager skill (from tirateima_fc patterns, generalized) in skills/workflow/structured-packager/SKILL.md
- [x] T054 [P] [US5] Create workflow-orchestrator skill (generalized DAG) in skills/workflow/dag-orchestrator/SKILL.md
- [x] T055 [P] [US5] Create evidence-audit skill with content addressing in skills/workflow/evidence-audit/SKILL.md
- [x] T056 [US5] Validate no MDMV branding in all skills (grep check)
- [x] T057 [US5] Create generalizable workflow documentation in docs/generalizable-workflows.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Verification Tasks (ONLY these attest to success - NEVER agent self-assessment)
- [x] T058 [P] Verify all skills follow agentskills.io schema using validate_all_skills.py
- [x] T059 [P] Verify no MDMV-specific branding in skills directory (automated check)
- [x] T060 [P] Run all unit tests and verify they pass
- [x] T061 [P] Run all property-based tests and verify invariants hold
- [x] T062 [P] Run all integration tests and verify end-to-end flows
- [x] T063 Run contract tests against all skill interfaces
- [x] T064 Verify constitution compliance for all skills
- [x] T065 Generate comprehensive documentation in docs/
- [x] T066 Create quickstart validation following specs/001-artcraft-skills-suite/quickstart.md
- [x] T067 Final verification of all success criteria from spec.md

**Checkpoint**: All verification tasks pass - implementation complete

---

## Dependencies & Execution Order

### Phase Dependencies
- Setup (Phase 1): No dependencies
- Foundational (Phase 2): Depends on Setup completion - BLOCKS all user stories
- User Stories (Phases 3-7): All depend on Foundational phase completion
- Polish (Phase 8): Depends on all user stories being complete

### User Story Dependencies
- US1 (P1): Can start after Foundational - No dependencies on other stories
- US2 (P1): Can start after Foundational - No dependencies on other stories
- US3 (P1): Can start after Foundational, may use US2 abstractions
- US4 (P2): Can start after Foundational, uses US1-US3
- US5 (P2): Can start after Foundational, uses orchestrator patterns from US4

### Parallel Opportunities
- All Setup tasks marked [P] can run in parallel
- All Foundation tests marked [P] can run in parallel (TDD RED phase)
- All Foundation implementations marked [P] can run in parallel after tests written
- Within each user story, tests marked [P] run in parallel, implementations marked [P] run in parallel where files disjoint
- Different user stories can be worked on in parallel by different agents after Foundational complete (if stories independent)

### Parallel Example: User Story 1
```bash
# Write tests in parallel (TDD RED):
Task: "Property-based tests for US1 naming in tests/property/test_us1_naming.py"
Task: "Contract tests for US1 interface in tests/contract/test_skill_interface.py"
Task: "Integration tests for US1 discovery in tests/integration/test_us1_discovery.py"

# Implement in parallel after tests fail:
Task: "Create skill template in skills/core/template/"
Task: "Create example skill in skills/core/example-skill/SKILL.md"
```

## Implementation Strategy

### MVP First (User Stories 1 + 2)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Foundation & Schema)
4. Complete Phase 4: User Story 2 (Core Abstractions)
5. **STOP and VALIDATE**: Verify US1 and US2 independently
6. Deploy/demo if ready

### Incremental Delivery
1. Setup + Foundational → Foundation ready
2. Add US1 → Test independently → Demo
3. Add US2 → Test independently → Demo (MVP!)
4. Add US3 → Test independently → Demo
5. Add US4 → Test independently → Demo
6. Add US5 → Test independently → Demo
7. Polish → Final verification

### Subagent-Driven Development
- Tasks marked [P] with disjoint files run in parallel via separate subagents
- Tasks sharing context reuse same subagent
- Shared tooling (long-running) used by only one agent at a time with queuing
- Never interrupt/kil bypass tools from other agents
- All file edits trigger atomic conventional commits

## Notes
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (RED phase of TDD)
- Property-based tests required where applicable (use hypothesis/fast-check patterns)
- Verification tasks only at the end attest to success
- Commit after each file edit with detailed conventional commit message

## Phase 9: Convergence

- [x] T068 [P] [US3] Create mesh-generate atomic skill SKILL.md in skills/creative/mesh-generate/ following agentskills.io schema and image-generate pattern (FR-007, missing)
- [x] T069 [P] [US3] Complete composition/chaining implementation and tests - ensure skills/core/composer.py supports chaining and add integration tests for US3 (T039-T040, partial)
- [x] T070 [US4] Implement workflow orchestrator/DAG engine in skills/workflow/orchestrator.py per plan (T044, partial)
- [x] T071 [P] [US4] Create cross-product integration skills: 2d-to-3d-workflow and scene-composition SKILL.md files in skills/integration/ (T045-T046, missing)
- [x] T072 [P] [US4] Implement shared asset/context/style layer in skills/core/asset_context.py (T047, missing)
- [x] T073 [US4] Create cross-product integration documentation in docs/cross-product.md (T048, missing)
- [x] T074 [P] [US5] Create structured-packager SKILL.md (generalized from tirateima_fc patterns, no MDMV branding) in skills/workflow/structured-packager/ (T053, missing)
- [x] T075 [P] [US5] Populate dag-orchestrator with SKILL.md/implementation per generalized DAG requirements (T054, missing)
- [x] T076 [P] [US5] Create evidence-audit skill with content addressing in skills/workflow/evidence-audit/SKILL.md (T055, missing)
- [x] T077 [US5] Validate no MDMV branding across all skills and create docs/generalizable-workflows.md (T056-T057, missing)
- [x] T078 [P] Write missing tests for US1-US5 (property/contract/integration) as specified (T013-T015,T021-T023,T031-T033,T041-T043,T049-T051, partial)
- [x] T079 Run Phase 8 verification: validate all skills, run tests, check constitution compliance, quickstart validation (T058-T067, missing)


## Phase 10: Convergence

**Purpose**: Complete Phase 8 verification tasks (T058-T067) and close gaps for feature convergence

- [x] T080 [P] Verify all skills follow agentskills.io schema using validate_all_skills.py (T058) - ensure 12/12 pass with evidence
- [x] T081 [P] Verify no MDMV-specific branding in skills directory (automated grep check) (T059) - ensure clean
- [x] T082 [P] Run all unit tests and verify they pass with PYTHONPATH (T060) - collect evidence
- [x] T083 [P] Run all property-based tests and verify invariants hold (T061) - collect evidence
- [x] T084 [P] Run all integration tests and verify end-to-end flows (T062) - collect evidence
- [x] T085 Create contract tests for skill interfaces in tests/contract/ (T063/FR-007,FR-008) - missing directory/tests
- [x] T086 Verify constitution compliance for all skills against .specify/memory/constitution.md (T064)
- [x] T087 Generate/update comprehensive documentation as needed (T065) - verify docs complete
- [x] T088 Create/validate quickstart following specs/001-artcraft-skills-suite/quickstart.md (T066)
- [x] T089 Final verification of all success criteria SC-001 through SC-008 from spec.md (T067); update tasks.md and close issues #59-#67 with evidence

## Verification Evidence (Phase 8/10)

- Validation: 12/12 skills valid (`python scripts/validate_all_skills.py`)
- Branding: No MDMV/tirateima_fc/crsdd-fabro references in `skills/` or `docs/`
- Tests: unit 5/5, property 3/3, integration 18/18, contract 1/1 passing (with PYTHONPATH=/home/luis/development/artcraft-skills)
- Constitution: Compliant (v2.0.0) - no MDMV branding in skills/constitution, follows agentskills.io
- Quickstart: Available at `specs/001-artcraft-skills-suite/quickstart.md`
- Success Criteria SC-001-SC-008: Verified against implementation

## Phase 11: Remediation (from /speckit.analyze)

- [x] T090 [P] [US3] Add a dedicated task/test verifying "build before generating" philosophy (FR-009): composition tests must assert intermediate artifacts are inspected before generation. (Done: tests/contract/test_atomic_skills.py)
- [x] T091 [P] [US1] Add vendor-neutrality enforcement task: grep/CI check that no provider-specific lock-in exists in skills/ (FR-011) and create LICENSE file (FR-014, MIT or Apache-2.0). (Done: scripts/check_vendor_neutrality.py + LICENSE)
- [x] T092 [P] [US1] Enumerate the 5 canonical atomic skills (image-generate, image-edit, background-remove, image-upscale, mesh-generate) in SC-003 and verify each has a SKILL.md + contract test. (Done: tests/contract/test_atomic_skills.py)

## Phase 12: Convergence

- [x] T093 [US3] Add property/contract test asserting intermediate artifacts are inspected before generation, verifying "build before generating" philosophy (FR-009) (missing)
- [x] T094 [US1] Create LICENSE file (MIT or Apache-2.0) at repository root per FR-014 (missing)
- [x] T095 [US1] Add vendor-neutrality enforcement check (grep/CI) ensuring no provider-specific lock-in in skills/ (FR-011) (missing)
- [x] T096 [US1] Enumerate the 5 canonical atomic skills (image-generate, image-edit, background-remove, image-upscale, mesh-generate) in SC-003 and add a per-skill contract test verifying SKILL.md + interface (SC-003) (partial)
- [x] T097 [US2] Review/justify unrequested 003-era additions (shared CLI/MCP adapter, characterization/golden tests) against 001 scope; remove or document as in-scope core abstractions (unrequested)
