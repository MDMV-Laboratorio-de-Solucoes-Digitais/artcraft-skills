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

- [ ] T001 Create directory structure (skills/{core,creative,workflow,integration}, scripts/, tests/{unit,property,integration}, docs/)
- [ ] T002 [P] Initialize package configuration and tooling (linting, formatting)
- [ ] T003 [P] Create skill template following agentskills.io structure in skills/README.md
- [ ] T004 [P] Create .gitignore entries for skills artifacts

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundation (TDD - Write FIRST, must FAIL) 
- [ ] T005 [P] Write property-based tests for skill schema validation (name pattern, description length) in tests/property/test_skill_schema.py
- [ ] T006 [P] Write tests for skill discovery/loading mechanism in tests/unit/test_skill_loader.py
- [ ] T007 [P] Write tests for Spec Kit extension registration integration in tests/unit/test_extension_integration.py

### Implementation for Foundation
- [ ] T008 Implement skill schema validation (contracts/skill-schema.json) with agentskills.io compliance in scripts/validate_skill.py
- [ ] T009 [P] Implement skill loader/discovery mechanism for agentskills.io format in scripts/skill_loader.py
- [ ] T010 [P] Integrate skill registration with Spec Kit extension system (.specify/extensions/.registry) in scripts/register_skills.py
- [ ] T011 [P] Create core utilities (logging, errors, config) in skills/core/utils.py
- [ ] T012 Create base skill interface and contracts in skills/core/base_skill.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Foundation & Schema (Priority: P1) 🎯 MVP

**Goal**: Well-defined composable skill system following agentskills.io standards, discoverable across agents

**Independent Test**: Define skill schema, create template, validate structure, load/discover skills in compatible agent environment

### Tests for User Story 1 (TDD - Write FIRST, must FAIL)
- [ ] T013 [P] [US1] Property-based tests for skill naming invariants in tests/property/test_us1_naming.py
- [ ] T014 [P] [US1] Contract tests for skill interface in tests/contract/test_skill_interface.py
- [ ] T015 [P] [US1] Integration tests for cross-agent discovery in tests/integration/test_us1_discovery.py

### Implementation for User Story 1
- [ ] T016 [P] [US1] Create skill template directory structure in skills/core/template/
- [ ] T017 [P] [US1] Create example skill following schema in skills/core/example-skill/SKILL.md
- [ ] T018 [US1] Implement skill validation CLI in scripts/validate_all_skills.py
- [ ] T019 [US1] Document skill authoring guide in docs/skill-authoring.md
- [ ] T020 [US1] Update extension registration for skills in .specify/extensions/.registry

**Checkpoint**: User Story 1 fully functional and testable independently

---

## Phase 4: User Story 2 - Core Abstractions & ArtCraft Integration (Priority: P1)

**Goal**: Core abstractions for model/provider routing, ArtCraft API adapters, job orchestration, cost tracking

**Independent Test**: Create skill using abstractions that authenticates, estimates costs, submits job, polls, retrieves results

### Tests for User Story 2 (TDD - Write FIRST, must FAIL)
- [ ] T021 [P] [US2] Property-based tests for credential manager invariants in tests/property/test_us2_creds.py
- [ ] T022 [P] [US2] Contract tests for API adapters in tests/contract/test_api_adapters.py
- [ ] T023 [P] [US2] Integration tests for job orchestration in tests/integration/test_us2_jobs.py

### Implementation for User Story 2
- [ ] T024 [P] [US2] Implement Credential Manager (API key + session auth) in skills/core/credentials.py
- [ ] T025 [P] [US2] Implement ArtCraft API adapters (OmniApiClient, OmniGenClient) in skills/core/artcraft_client.py
- [ ] T026 [P] [US2] Implement Model/Provider Router in skills/core/provider_router.py
- [ ] T027 [P] [US2] Implement Asset/Media Handler in skills/core/asset_handler.py
- [ ] T028 [US2] Implement Job Orchestrator (idempotency, polling, webhooks) in skills/core/job_orchestrator.py
- [ ] T029 [US2] Implement Cost Estimator in skills/core/cost_estimator.py
- [ ] T030 [US2] Create core abstractions documentation in docs/core-abstractions.md

**Checkpoint**: User Story 2 fully functional and testable independently

---

## Phase 5: User Story 3 - Atomic Creative Skills (Priority: P1)

**Goal**: Atomic skills for core creative operations, composable

**Independent Test**: Use individual atomic skills independently and compose them (e.g., generate → remove bg → upscale)

### Tests for User Story 3 (TDD - Write FIRST, must FAIL)
- [ ] T031 [P] [US3] Property-based tests for skill composition invariants in tests/property/test_us3_composition.py
- [ ] T032 [P] [US3] Contract tests for atomic skill interfaces in tests/contract/test_atomic_skills.py
- [ ] T033 [P] [US3] Integration tests for skill chaining in tests/integration/test_us3_chaining.py

### Implementation for User Story 3
- [ ] T034 [P] [US3] Create image generation skill (atomic) in skills/creative/image-generate/SKILL.md
- [ ] T035 [P] [US3] Create image edit/inpaint skill (atomic) in skills/creative/image-edit/SKILL.md
- [ ] T036 [P] [US3] Create background removal skill (atomic) in skills/creative/background-remove/SKILL.md
- [ ] T037 [P] [US3] Create image upscale skill (atomic) in skills/creative/image-upscale/SKILL.md
- [ ] T038 [P] [US3] Create 3D mesh generation skill (atomic) in skills/creative/mesh-generate/SKILL.md
- [ ] T039 [US3] Create skill composition utilities in skills/core/composer.py
- [ ] T040 [US3] Test composition of multiple atomic skills

**Checkpoint**: User Story 3 fully functional and testable independently

---

## Phase 6: User Story 4 - Cross-Product Integration Skills (Priority: P2)

**Goal**: Skills orchestrating workflows across different ArtCraft apps/domains

**Independent Test**: Execute cross-product workflow combining skills from different domains

### Tests for User Story 4 (TDD - Write FIRST, must FAIL)
- [ ] T041 [P] [US4] Property-based tests for orchestrator invariants in tests/property/test_us4_orchestrator.py
- [ ] T042 [P] [US4] Contract tests for orchestrator interface in tests/contract/test_orchestrator.py
- [ ] T043 [P] [US4] Integration tests for cross-product workflows in tests/integration/test_us4_crossproduct.py

### Implementation for User Story 4
- [ ] T044 [P] [US4] Implement workflow orchestrator/DAG engine in skills/workflow/orchestrator.py
- [ ] T045 [P] [US4] Create 2D-to-3D workflow skill in skills/integration/2d-to-3d-workflow/SKILL.md
- [ ] T046 [P] [US4] Create scene composition workflow skill in skills/integration/scene-composition/SKILL.md
- [ ] T047 [US4] Implement shared asset/context/style layer in skills/core/asset_context.py
- [ ] T048 [US4] Create cross-product integration documentation in docs/cross-product.md

**Checkpoint**: User Story 4 fully functional and testable independently

---

## Phase 7: User Story 5 - Generalizable MDMV Workflows (Priority: P2)

**Goal**: Generalizable skills derived from MDMV patterns (structured-packager, policy-redaction, orchestrator, evidence-audit)

**Independent Test**: Use skills in non-MDMV contexts, demonstrating generalizability

### Tests for User Story 5 (TDD - Write FIRST, must FAIL)
- [ ] T049 [P] [US5] Property-based tests for redaction invariants in tests/property/test_us5_redaction.py
- [ ] T050 [P] [US5] Contract tests for workflow skills in tests/contract/test_mdmv_workflows.py
- [ ] T051 [P] [US5] Integration tests for generalizability in tests/integration/test_us5_generalizable.py

### Implementation for User Story 5
- [ ] T052 [P] [US5] Create policy-redaction middleware (generalizable) in skills/workflow/policy-redaction/SKILL.md
- [ ] T053 [P] [US5] Create structured-packager skill (from tirateima_fc patterns, generalized) in skills/workflow/structured-packager/SKILL.md
- [ ] T054 [P] [US5] Create workflow-orchestrator skill (generalized DAG) in skills/workflow/dag-orchestrator/SKILL.md
- [ ] T055 [P] [US5] Create evidence-audit skill with content addressing in skills/workflow/evidence-audit/SKILL.md
- [ ] T056 [US5] Validate no MDMV branding in all skills (grep check)
- [ ] T057 [US5] Create generalizable workflow documentation in docs/generalizable-workflows.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

### Verification Tasks (ONLY these attest to success - NEVER agent self-assessment)
- [ ] T058 [P] Verify all skills follow agentskills.io schema using validate_all_skills.py
- [ ] T059 [P] Verify no MDMV-specific branding in skills directory (automated check)
- [ ] T060 [P] Run all unit tests and verify they pass
- [ ] T061 [P] Run all property-based tests and verify invariants hold
- [ ] T062 [P] Run all integration tests and verify end-to-end flows
- [ ] T063 Run contract tests against all skill interfaces
- [ ] T064 Verify constitution compliance for all skills
- [ ] T065 Generate comprehensive documentation in docs/
- [ ] T066 Create quickstart validation following specs/001-artcraft-skills-suite/quickstart.md
- [ ] T067 Final verification of all success criteria from spec.md

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
