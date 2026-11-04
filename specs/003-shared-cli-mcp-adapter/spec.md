# Feature Specification: Shared CLI/MCP Adapter

**Feature Branch**: 003-shared-cli-mcp-adapter  
**Created**: 2026-11-04  
**Status**: Draft  
**Input**: User description from assessment (shared-cli-mcp-adapter) - Extract CLI/MCP integration logic into shared adapter in skills/core/ and refactor image-generate

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Shared CLI/MCP Integration Layer (Priority: P1)

As a skill developer building creative skills for ArtCraft apps, I need a shared CLI/MCP integration adapter so I can reuse discovery, invocation, and normalization logic without duplicating code.

**Why this priority**: Core infrastructure - enables all future creative skills following Constitution v2.1.0 CLI/MCP-only approach.

**Independent Test**: Can be tested by importing the adapter and using it to discover/invoke CLI/MCP interfaces, and by verifying image-generate works through it.

**Acceptance Scenarios**:

1. **Given** the adapter module exists in `skills/core/`, **When** imported, **Then** it provides reusable functions for CLI/MCP discovery and invocation
2. **Given** CLI is available, **When** using adapter, **Then** it can discover commands and invoke them
3. **Given** MCP is available, **When** using adapter, **Then** it normalizes MCP config/output; discovery/invocation remain skill-level per FR-005.

### User Story 2 - Refactor image-generate to use shared adapter (Priority: P1)

As a maintainer, I need image-generate to use the shared adapter so that behavior is preserved while code is deduplicated.

**Why this priority**: Validates the adapter works correctly and maintains backward compatibility.

**Independent Test**: Run all existing image-generate tests - they must all pass.

**Acceptance Scenarios**:

1. **Given** image-generate refactored to use adapter, **When** running all image-generate tests, **Then** all 23 tests pass
2. **Given** image-generate uses adapter, **When** validated, **Then** it still passes validation
3. **Given** refactored code, **When** behavior tested, **Then** output format and behavior are identical to before: equality of `SkillResult.success`, canonicalized `data`, `error`, and `metadata` (mode, interface, command, exit_code, timeout_s, reason, is_error), with volatile timing pinned to `None`/`300`.

### User Story 3 - Enable future creative skills (Priority: P2)

As a skill developer, I need the adapter to be flexible enough for image-edit, background-remove, image-upscale, and mesh-generate so I can build them quickly.

**Why this priority**: Unlocks the creative skill family.

**Independent Test**: Can be tested by examining adapter API flexibility and documentation.

**Acceptance Scenarios**:

1. **Given** adapter API, **When** used by different skill types, **Then** it can be configured for different commands/tools
2. **Given** adapter, **When** extended, **Then** it follows core utilities patterns

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide `skills/core/artcraft_app_client.py` with reusable CLI/MCP integration functions
- **FR-002**: Adapter MUST extract CLI discovery logic (finding CLI binary, discovering commands via --help)
- **FR-003**: Adapter MUST extract command filtering/discovery logic for generation/image operations
- **FR-004**: Adapter MUST extract CLI invocation logic with timeout and error handling
- **FR-005**: Adapter MUST provide MCP config normalization (`normalize_mcp_config`) and output normalization helpers; MCP discovery/invocation and app-specific tool mapping remain skill-level (no universal MCP runtime in the adapter). Adapter MAY expose injectable helpers only.
- **FR-006**: Adapter MUST extract mode selection as a pure helper `select_mode(requested_mode, cli_available, mcp_available) -> str` (auto/cli/mcp/none); availability probing and `SkillResult` construction remain in the skill.
- **FR-007**: Adapter MUST extract output normalization logic; `normalize_output` and `normalize_mcp_config` MUST NOT mutate their inputs and MUST return new dicts; `normalize_output` MUST accept an optional list of expected keys defaulting to the current image keys (image_url, image_path, asset_id, format, width, height, metadata).
- **FR-008**: Adapter MUST extract error standardization as transport-neutral reason-code constants and a pure `standardize_error` helper; final `SkillResult` construction and exact user-facing error strings remain in the skill.
- **FR-009**: image-generate MUST be refactored to use the shared adapter with identical behavior
- **FR-010**: All existing image-generate tests (23/23) MUST continue to pass
- **FR-011**: `python scripts/validate_skill.py skills/creative/image-generate` MUST pass
- **FR-012**: `python scripts/validate_all_skills.py` MUST still show all skills valid
- **FR-013**: Adapter discovery/normalization helpers MUST return `None`/`[]` (never raise) when CLI/MCP is unavailable; invalid arguments MAY raise `ValueError`; `run_cli`/`run_cli_generation`/`discover_cli_commands` MUST propagate OS/timeout errors per contract. Skills MUST map unavailable results to reason codes `cli_not_found`, `mcp_unavailable`, `neither_available`, `is_error`.
- **FR-014**: Adapter MUST be a function-based, stateless module in `skills/core/artcraft_app_client.py` with no `ArtcraftAppClient` class required.
- **FR-015**: Adapter MUST expose `__all__` (public façade) and `__version__` (currently `0.2.0`; initial release `0.1.0`).
- **FR-016**: Equivalence MUST be verified by characterization (golden master) + differential (pre-refactor reference) + property-based tests comparing canonicalized `SkillResult` (success, data, error, metadata) for a curated scenario matrix.
- **FR-017**: Regression scope MUST include direct adapter unit tests, adapter property tests, all 23 image-generate tests, both validation scripts, and composer integration tests.

### Key Entities

- **ArtcraftAppClient/adapter functions**: Shared utilities for CLI/MCP integration
- **CLI discovery/invocation**: Functions to find CLI, discover commands, run commands
- **MCP config/output normalization**: normalize_mcp_config, normalize_output (MCP discovery/invocation stay skill-level)
- **Mode & error helpers**: select_mode, standardize_error (pure helpers; orchestration stays in skill)
- **Boundary**: Adapter = stateless infrastructure (discovery, invocation, normalization, pure helpers). Skill = schemas, validation, param assembly, MCP stubs, orchestration, SkillResult construction.
- **Integration points (image-generate)**: `_discover_cli`→`discover_cli`; `_discover_generation_command`→`discover_generation_command`; `_normalize_output`→`normalize_output`; `_normalize_mcp_config`→`normalize_mcp_config`; `_execute_cli` uses `discover_cli_commands`/`run_cli_generation`; mode decision uses `select_mode`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Shared adapter module exists at `skills/core/artcraft_app_client.py`
- **SC-002**: All 23 existing image-generate tests pass after refactoring
- **SC-003**: Image-generate skill validation passes
- **SC-004**: All skills validation passes (no regressions)
- **SC-005**: Adapter is reusable: (a) importable directly by an independent consumer module, (b) its public API matches the committed snapshot (`tests/contract/artcraft_app_client_api.json`) with zero unreviewed diff, (c) >=7 contract tests pass, and (d) any public-signature change ships with a version bump and CHANGELOG entry.

## Clarifications

### Session 2026-11-04
- Q: Should the shared adapter be function-based (module with functions) or class-based (e.g., `ArtcraftAppClient` class)? → A: Function-based module (Option A) - simple, composable, matches current implementation and project needs.
- Q: Should the adapter implement real MCP discovery/invocation now? → A: No — amend FR-005; MCP discovery/invocation and app-specific tool mapping remain skill-level; adapter provides config/output normalization plus injectable helpers only.
- Q: Should select_mode and a transport-neutral error normalizer be added to the adapter? → A: Yes — add pure select_mode(requested_mode, cli_available, mcp_available) -> str and reason-code constants/standardize_error helper; orchestration and SkillResult construction stay in skill.
- Q: Should normalize_output generalize to accept optional expected keys? → A: Yes — generalize with optional keys param defaulting to current image keys; preserve exact image-generate output.
- Q: Should adapter start at 0.1.0 or 1.0.0? → A: Start at 0.1.0 (unstable); bumped to 0.2.0 with convergence (reason-code constants); promote to 1.0.0 when a second creative skill ships.
- Q: Should future creative skills be required to use the shared adapter? → A: Yes — required (no duplicated discovery/invocation).
- Autonomous: core pattern stays function-based, stateless (CHK005/CHK009); signatures modernized to str | None / dict[str, Any] / list[str] with concrete returns; normalize_mcp_config must not mutate input; equivalence = equality of SkillResult.success/data/error/metadata with timing pinned to None/300; missing CLI/MCP returns None/[] mapped to cli_not_found/mcp_unavailable/neither_available/is_error; regression gate = adapter unit + property + 23 image-generate tests + both validators + composer integration; reusability metric per SC-005; validate_all_skills.py is structural-only gate.
