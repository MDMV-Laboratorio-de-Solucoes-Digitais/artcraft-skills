# Tasks: Implement Python Creative Skills

**Input**: Design documents from `/specs/004-implement-python-creative-skills/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification. The spec does not explicitly request test tasks; implementation tasks take priority.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Skills**: `skills/creative/{name}/skill.py`
- **Core abstractions**: `skills/core/creative_skill.py`
- **Tests**: `tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per implementation plan

- [ ] T001 Verify skill directory structure exists for all 4 skills under `skills/creative/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 [P] [US1] Create `CreativeSkill` base class in `skills/core/creative_skill.py` encapsulating discover→resolve→invoke→normalize→degrade flow parameterized by name, description, keywords, and param builder

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Invoke image-edit skill through an agent (Priority: P1) 🎯 MVP

**Goal**: Build and validate the image-edit skill so an AI agent can edit images through the adapter

**Independent Test**: An agent can invoke image-edit with `{"image": "...", "prompt": "..."}` and receive a valid `SkillResult` with `image_url` or `image_path`

### Implementation for User Story 1

- [ ] T003 [P] [US1]: Create `skills/creative/image-edit/skill.py` with `ImageEditSkill(BaseSkill)` class skeleton, `__init__` with name="image-edit", and `__all__`
- [ ] T004 [US1]: Implement `ImageEditSkill.get_input_schema()` returning dict with required `image`, `prompt` and optional `mask`, `mode_edit`, `model`, `strength`, `width`, `height`, `aspect_ratio`, `seed`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`
- [ ] T005 [US1]: Implement `ImageEditSkill.get_output_schema()` returning dict with `image_url`, `image_path`, `asset_id`, `format`, `width`, `height`, `metadata`
- [ ] T006 [US1]: Implement `ImageEditSkill.validate_inputs()` checking required `image` and `prompt`, optional `mode` enum, `width`/`height` > 0
- [ ] T007 [P] [US1]: Implement `ImageEditSkill._discover_cli(cli_path)` delegating to `artcraft_app_client.discover_cli(cli_path)`
- [ ] T008 [P] [US1]: Implement `ImageEditSkill._discover_generation_command(commands, keywords, override)` delegating to `artcraft_app_client.discover_generation_command()` with keywords `['edit', 'inpaint', 'outpaint', 'composite', 'modify', 'change']`
- [ ] T009 [P] [US1]: Implement `ImageEditSkill._normalize_output(out)` delegating to `artcraft_app_client.normalize_output(out)`
- [ ] T010 [P] [US1]: Implement `ImageEditSkill._normalize_mcp_config(cfg)` delegating to `artcraft_app_client.normalize_mcp_config(cfg)`
- [ ] T011 [P] [US1]: Implement `ImageEditSkill._mcp_available(cfg)` returning `False` (default, MCP stub)
- [ ] T012 [P] [US1]: Implement `ImageEditSkill._mcp_command_list(cfg)` returning `[]` (default, MCP stub)
- [ ] T013 [P] [US1]: Implement `ImageEditSkill._mcp_command_run(cfg, tool_id, params, timeout)` returning `{"is_error": True, "error": "not implemented"}` (default, MCP stub)
- [ ] T014 [US1]: Implement `ImageEditSkill._execute_cli(inputs, cli_path, mode)` discovering CLI, resolving command, running generation, normalizing output, handling errors/timeouts
- [ ] T015 [US1]: Implement `ImageEditSkill._execute_mcp(inputs, mode)` delegating to MCP stubs with reason code `mcp_unavailable`
- [ ] T016 [US1]: Implement `ImageEditSkill.execute(inputs)` with mode selection via `select_mode`, CLI/MCP dispatch, and graceful degradation with reason codes
- [ ] T017 [US1]: Set `__all__ = ["ImageEditSkill"]` and verify module imports cleanly

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Invoke background-remove skill through an agent (Priority: P1)

**Goal**: Build and validate the background-remove skill so an AI agent can remove backgrounds from images through the adapter

**Independent Test**: An agent can invoke background-remove with `{"image": "..."}` and receive a valid `SkillResult` with `image_url` set

### Implementation for User Story 2

- [ ] T018 [P] [US2]: Create `skills/creative/background-remove/skill.py` with `BackgroundRemoveSkill(BaseSkill)` class skeleton, `__init__` with name="background-remove", and `__all__`
- [ ] T019 [US2]: Implement `BackgroundRemoveSkill.get_input_schema()` returning dict with required `image` and optional `model`, `return_mask`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`
- [ ] T020 [US2]: Implement `BackgroundRemoveSkill.get_output_schema()` returning dict with `image_url`, `image_path`, `mask_url`, `asset_id`, `format`, `metadata`
- [ ] T021 [US2]: Implement `BackgroundRemoveSkill.validate_inputs()` checking required `image`, optional `model`, `return_mask`, `mode` enum
- [ ] T022 [P] [US2]: Implement `BackgroundRemoveSkill._discover_cli(cli_path)` delegating to `artcraft_app_client.discover_cli(cli_path)`
- [ ] T023 [P] [US2]: Implement `BackgroundRemoveSkill._discover_generation_command(commands, keywords, override)` delegating to `artcraft_app_client.discover_generation_command()` with keywords `['background', 'remove', 'matting', 'cutout', 'isolate']`
- [ ] T024 [P] [US2]: Implement `BackgroundRemoveSkill._normalize_output(out)` delegating to `artcraft_app_client.normalize_output(out)`
- [ ] T025 [P] [US2]: Implement `BackgroundRemoveSkill._normalize_mcp_config(cfg)` delegating to `artcraft_app_client.normalize_mcp_config(cfg)`
- [ ] T026 [P] [US2]: Implement `BackgroundRemoveSkill._mcp_available(cfg)` returning `False` (default, MCP stub)
- [ ] T027 [P] [US2]: Implement `BackgroundRemoveSkill._mcp_command_list(cfg)` returning `[]` (default, MCP stub)
- [ ] T028 [P] [US2]: Implement `BackgroundRemoveSkill._mcp_command_run(cfg, tool_id, params, timeout)` returning `{"is_error": True, "error": "not implemented"}` (default, MCP stub)
- [ ] T029 [US2]: Implement `BackgroundRemoveSkill._execute_cli(inputs, cli_path, mode)` discovering CLI, resolving command, running generation, normalizing output, handling errors/timeouts
- [ ] T030 [US2]: Implement `BackgroundRemoveSkill._execute_mcp(inputs, mode)` delegating to MCP stubs with reason code `mcp_unavailable`
- [ ] T031 [US2]: Implement `BackgroundRemoveSkill.execute(inputs)` with mode selection via `select_mode`, CLI/MCP dispatch, and graceful degradation with reason codes
- [ ] T032 [US2]: Set `__all__ = ["BackgroundRemoveSkill"]` and verify module imports cleanly

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Invoke image-upscale and mesh-generate skills through an agent (Priority: P2)

**Goal**: Build and validate image-upscale and mesh-generate skills so an AI agent can upscale images and generate 3D meshes through the adapter

**Independent Test**: An agent can invoke each skill independently and receive valid `SkillResult` outputs

### Implementation for User Story 3 - Part A: image-upscale

- [ ] T033 [P] [US3]: Create `skills/creative/image-upscale/skill.py` with `ImageUpscaleSkill(BaseSkill)` class skeleton, `__init__` with name="image-upscale", and `__all__`
- [ ] T034 [US3]: Implement `ImageUpscaleSkill.get_input_schema()` returning dict with required `image` and optional `scale`, `model`, `enhance`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`
- [ ] T035 [US3]: Implement `ImageUpscaleSkill.get_output_schema()` returning dict with `image_url`, `image_path`, `asset_id`, `format`, `width`, `height`, `metadata`
- [ ] T036 [US3]: Implement `ImageUpscaleSkill.validate_inputs()` checking required `image`, optional `scale`, `model`, `enhance`, `mode` enum
- [ ] T037 [P] [US3]: Implement `ImageUpscaleSkill._discover_cli(cli_path)` delegating to `artcraft_app_client.discover_cli(cli_path)`
- [ ] T038 [P] [US3]: Implement `ImageUpscaleSkill._discover_generation_command(commands, keywords, override)` delegating to `artcraft_app_client.discover_generation_command()` with keywords `['upscale', 'enhance', 'super-resolution', 'scale', 'resize']`
- [ ] T039 [P] [US3]: Implement `ImageUpscaleSkill._normalize_output(out)` delegating to `artcraft_app_client.normalize_output(out)`
- [ ] T040 [P] [US3]: Implement `ImageUpscaleSkill._normalize_mcp_config(cfg)` delegating to `artcraft_app_client.normalize_mcp_config(cfg)`
- [ ] T041 [P] [US3]: Implement `ImageUpscaleSkill._mcp_available(cfg)` returning `False` (default, MCP stub)
- [ ] T042 [P] [US3]: Implement `ImageUpscaleSkill._mcp_command_list(cfg)` returning `[]` (default, MCP stub)
- [ ] T043 [P] [US3]: Implement `ImageUpscaleSkill._mcp_command_run(cfg, tool_id, params, timeout)` returning `{"is_error": True, "error": "not implemented"}` (default, MCP stub)
- [ ] T044 [US3]: Implement `ImageUpscaleSkill._execute_cli(inputs, cli_path, mode)` discovering CLI, resolving command, running generation, normalizing output, handling errors/timeouts
- [ ] T045 [US3]: Implement `ImageUpscaleSkill._execute_mcp(inputs, mode)` delegating to MCP stubs with reason code `mcp_unavailable`
- [ ] T046 [US3]: Implement `ImageUpscaleSkill.execute(inputs)` with mode selection via `select_mode`, CLI/MCP dispatch, and graceful degradation with reason codes
- [ ] T047 [US3]: Set `__all__ = ["ImageUpscaleSkill"]` and verify module imports cleanly

### Implementation for User Story 3 - Part B: mesh-generate

- [ ] T048 [P] [US3]: Create `skills/creative/mesh-generate/skill.py` with `MeshGenerateSkill(BaseSkill)` class skeleton, `__init__` with name="mesh-generate", and `__all__`
- [ ] T049 [US3]: Implement `MeshGenerateSkill.get_input_schema()` returning dict with optional `prompt`, `image` (at least one required), `model`, `format`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`
- [ ] T050 [US3]: Implement `MeshGenerateSkill.get_output_schema()` returning dict with `mesh_url`, `mesh_path`, `asset_id`, `format`, `metadata`
- [ ] T051 [US3]: Implement `MeshGenerateSkill.validate_inputs()` checking at least one of `prompt` or `image` provided, optional `model`, `format`, `mode` enum
- [ ] T052 [P] [US3]: Implement `MeshGenerateSkill._discover_cli(cli_path)` delegating to `artcraft_app_client.discover_cli(cli_path)`
- [ ] T053 [P] [US3]: Implement `MeshGenerateSkill._discover_generation_command(commands, keywords, override)` delegating to `artcraft_app_client.discover_generation_command()` with keywords `['mesh', '3d', 'mesh.generate', 'image-to-3d', 'model']`
- [ ] T054 [P] [US3]: Implement `MeshGenerateSkill._normalize_output(out)` delegating to `artcraft_app_client.normalize_output(out)`
- [ ] T055 [P] [US3]: Implement `MeshGenerateSkill._normalize_mcp_config(cfg)` delegating to `artcraft_app_client.normalize_mcp_config(cfg)`
- [ ] T056 [P] [US3]: Implement `MeshGenerateSkill._mcp_available(cfg)` returning `False` (default, MCP stub)
- [ ] T057 [P] [US3]: Implement `MeshGenerateSkill._mcp_command_list(cfg)` returning `[]` (default, MCP stub)
- [ ] T058 [P] [US3]: Implement `MeshGenerateSkill._mcp_command_run(cfg, tool_id, params, timeout)` returning `{"is_error": True, "error": "not implemented"}` (default, MCP stub)
- [ ] T059 [US3]: Implement `MeshGenerateSkill._execute_cli(inputs, cli_path, mode)` discovering CLI, resolving command, running generation, normalizing output, handling errors/timeouts
- [ ] T060 [US3]: Implement `MeshGenerateSkill._execute_mcp(inputs, mode)` delegating to MCP stubs with reason code `mcp_unavailable`
- [ ] T061 [US3]: Implement `MeshGenerateSkill.execute(inputs)` with mode selection via `select_mode`, CLI/MCP dispatch, and graceful degradation with reason codes
- [ ] T062 [US3]: Set `__all__ = ["MeshGenerateSkill"]` and verify module imports cleanly

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T063 [P] Run `python scripts/validate_skill.py skills/creative/image-edit` and verify passes
- [ ] T064 [P] Run `python scripts/validate_skill.py skills/creative/background-remove` and verify passes
- [ ] T065 [P] Run `python scripts/validate_skill.py skills/creative/image-upscale` and verify passes
- [ ] T066 [P] Run `python scripts/validate_skill.py skills/creative/mesh-generate` and verify passes
- [ ] T067 [P] Run `python scripts/validate_all_skills.py` and verify all 12 skills valid
- [ ] T068 [P] Run `python -m pytest` and verify no regressions (baseline 278 tests)
- [ ] T069 Verify `CreativeSkill` base class is importable from `skills.core`
- [ ] T070 [P] Review each skill's `SKILL.md` schema matches its `skill.py` `get_input_schema()`/`get_output_schema()` (SC-004)
- [ ] T071 [P] Verify each skill degrades gracefully with reason codes when CLI/MCP unavailable (SC-005)

**Checkpoint**: All 4 creative skills have executable `skill.py` files, all validate, and no regressions in the full test suite

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (image-edit, P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (background-remove, P1): Can start after Foundational - No dependencies on other stories
  - User Story 3 (image-upscale + mesh-generate, P2): Can start after Foundational - May use US1 patterns but independently testable
- **Polish (Final Phase)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational - Uses adapter patterns from US1 but independently testable

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if staffed)
- All tasks within a user story marked [P] can run in parallel (different skill files)
- Different user stories can be worked on in parallel by different team members

### Parallel Example: User Story 1

```bash
# Launch schema tasks together:
Task: "Implement ImageEditSkill.get_input_schema() in skills/creative/image-edit/skill.py"
Task: "Implement ImageEditSkill.get_output_schema() in skills/creative/image-edit/skill.py"

# Launch pure helper tasks together:
Task: "Implement ImageEditSkill._discover_cli() in skills/creative/image-edit/skill.py"
Task: "Implement ImageEditSkill._normalize_output() in skills/creative/image-edit/skill.py"
Task: "Implement ImageEditSkill._normalize_mcp_config() in skills/creative/image-edit/skill.py"
```

### Implementation Strategy

#### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (image-edit)
4. **STOP and VALIDATE**: Test image-edit skill independently
5. Deploy/demo if ready

#### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (image-edit) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (background-remove) → Test independently → Deploy/Demo
4. Add User Story 3 (image-upscale + mesh-generate) → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (image-edit)
   - Developer B: User Story 2 (background-remove)
   - Developer C: User Story 3 (image-upscale + mesh-generate)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are NOT included in this task list (not explicitly requested in spec.md)
- Implementation follows `image-generate/skill.py` template pattern
- All skills use `CreativeSkill` base class from `skills/core/creative_skill.py` (to be created in T002)
- All skills delegate to `skills/core/artcraft_app_client.py` for CLI/MCP operations
- Graceful degradation with reason codes required for all skills (FR-006)
- Input validation required for all skills (FR-007)
- SKILL.md schema must match skill.py schemas (FR-008)
