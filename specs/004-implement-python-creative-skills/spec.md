# Feature Specification: Implement Python Creative Skills

**Feature Branch**: `specs/004-implement-python-creative-skills`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Implement executable Python `skill.py` files for four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) that currently exist only as declarative `SKILL.md` scaffolds, using the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) and `image-generate/skill.py` as the template."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Invoke image-edit skill through an agent (Priority: P1)

As an artist using an AI agent, I want to edit existing images through the image-edit skill so that I can modify specific regions, extend boundaries, or composite elements without leaving my agent workflow.

**Why this priority**: Image editing is the most frequently used creative operation after generation; providing an executable skill delivers immediate value and validates the adapter pattern.

**Independent Test**: An agent can invoke the image-edit skill with a source image and edit prompt, and receive a valid `SkillResult` with `image_url` or `image_path`.

**Acceptance Scenarios**:

1. **Given** the image-edit skill is installed and the shared adapter is available, **When** an agent invokes it with `{"image": "...", "prompt": "make it blue"}`, **Then** it returns a `SkillResult` with `success=true` and `data.image_url` or `data.image_path` set.
2. **Given** the CLI is unavailable, **When** the image-edit skill is invoked, **Then** it returns `success=false` with `metadata.reason` set to `cli_not_found` or `neither_available`.

---

### User Story 2 - Invoke background-remove skill through an agent (Priority: P1)

As a designer using an AI agent, I want to remove backgrounds from images through the background-remove skill so that I can isolate subjects for compositing without manual masking.

**Why this priority**: Background removal is a high-frequency, well-defined operation that cleanly demonstrates the adapter pattern's degradation handling.

**Independent Test**: An agent can invoke the background-remove skill with a source image and receive a valid `SkillResult` with `image_url` set.

**Acceptance Scenarios**:

1. **Given** the background-remove skill is installed and the shared adapter is available, **When** an agent invokes it with `{"image": "..."}`, **Then** it returns a `SkillResult` with `success=true` and `data.image_url` set.
2. **Given** neither CLI nor MCP is available, **When** the background-remove skill is invoked, **Then** it returns `success=false` with `metadata.reason` set to `neither_available`.

---

### User Story 3 - Invoke image-upscale and mesh-generate skills through an agent (Priority: P2)

As a creator using an AI agent, I want to upscale images and generate 3D meshes through dedicated skills so that I can produce higher-resolution assets and 3D models within my agent workflow.

**Why this priority**: Upscaling and mesh generation complete the Phase 1 creative skill set; they are lower-frequency than edit/background-remove but equally important for demonstrating adapter reusability across diverse skill domains.

**Independent Test**: An agent can invoke each skill independently and receive valid `SkillResult` outputs.

**Acceptance Scenarios**:

1. **Given** the image-upscale skill is installed, **When** an agent invokes it with `{"image": "...", "scale": 2}`, **Then** it returns a `SkillResult` with `success=true` and `data.image_url` set.
2. **Given** the mesh-generate skill is installed, **When** an agent invokes it with `{"prompt": "a low-poly tree"}`, **Then** it returns a `SkillResult` with `success=true` and `data.mesh_url` set.

### Edge Cases

- **CLI unavailable**: Each skill MUST return `SkillResult(success=False, error=..., metadata={"reason":"cli_not_found"})` and MUST NOT crash.
- **MCP unavailable**: Each skill MUST return `SkillResult(success=False, error=..., metadata={"reason":"mcp_unavailable"})` when MCP is the only available interface but is unreachable.
- **Neither available**: Each skill MUST return `SkillResult(success=False, error=..., metadata={"reason":"neither_available"})` when no interface is available.
- **Invalid inputs**: Each skill MUST validate inputs and return `SkillResult(success=False, error=..., metadata={})` for missing or malformed required parameters.
- **Timeout**: Each skill MUST propagate CLI timeout errors and return `SkillResult(success=False, error=..., metadata={"timeout_s": <value>})`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an executable Python `skill.py` for `image-edit` under `skills/creative/image-edit/` that implements the `BaseSkill` interface (`get_input_schema`, `get_output_schema`, `validate_inputs`, `execute`).
- **FR-002**: System MUST provide an executable Python `skill.py` for `background-remove` under `skills/creative/background-remove/` that implements the `BaseSkill` interface.
- **FR-003**: System MUST provide an executable Python `skill.py` for `image-upscale` under `skills/creative/image-upscale/` that implements the `BaseSkill` interface.
- **FR-004**: System MUST provide an executable Python `skill.py` for `mesh-generate` under `skills/creative/mesh-generate/` that implements the `BaseSkill` interface.
- **FR-005**: Each skill MUST reuse the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) for CLI discovery, command resolution, invocation, output normalization, and mode selection — not duplicate adapter logic.
- **FR-006**: Each skill MUST gracefully degrade when CLI/MCP is unavailable, returning reason codes `cli_not_found`, `mcp_unavailable`, or `neither_available` in metadata.
- **FR-007**: Each skill MUST validate its inputs and return clear errors for missing or malformed required parameters.
- **FR-008**: Each skill's `SKILL.md` input/output schema MUST match its `skill.py` `get_input_schema()`/`get_output_schema()` return values.
- **FR-009**: All 4 skills MUST pass `python scripts/validate_skill.py skills/creative/<name>` validation.

### Key Entities

- **Skill**: A composable capability with metadata, inputs/outputs schema, implementation (`skill.py`), and documentation (`SKILL.md`).
- **SkillResult**: The return type of `skill.execute()`, containing `success`, `data`, `error`, and `metadata`.
- **Adapter**: The shared CLI/MCP module (`skills/core/artcraft_app_client.py`) providing `discover_cli`, `discover_generation_command`, `run_cli_generation`, `normalize_output`, `normalize_mcp_config`, `select_mode`, and reason-code constants.
- **CLI**: The `photocraft-cli` binary discovered via `discover_cli()` and invoked via `run_cli_generation()`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 4 creative skills have executable `skill.py` files (baseline: 0/4, target: 4/4).
- **SC-002**: All 4 skills pass `python scripts/validate_skill.py skills/creative/<name>` (baseline: skills validate as declarative only; target: validate with executable code present).
- **SC-003**: Full test suite continues to pass (baseline: 278 tests passing; target: no regression, count maintained or increased).
- **SC-004**: Each skill's `SKILL.md` schema matches its `skill.py` `get_input_schema()`/`get_output_schema()` (baseline: unverified; target: 4/4 match).
- **SC-005**: Each skill degrades gracefully with reason codes when CLI/MCP is unavailable (baseline: unverified; target: 4/4 verified).

## Assumptions

- The `image-generate/skill.py` template pattern is appropriate for all 4 skill domains (editing, background removal, upscaling, mesh generation).
- `discover_cli_commands` + keyword matching will find the appropriate command for each skill in the `photocraft-cli` command registry.
- Skill-specific parameters (e.g., `mask` for image-edit, `scale` for image-upscale, `format` for mesh-generate) can be added to each skill's input schema without breaking the template pattern.
- The 4 `SKILL.md` files' declared inputs and outputs are accurate and stable enough to build against.
- The shared adapter (`artcraft_app_client.py`) remains stable and does not require modification for these skills to use it.

## Clarifications

### Session 2026-11-04

- **Input/output schema**: Common superset schema (`image`, `prompt`, `model`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`) plus skill-specific extras (e.g., `mask` for image-edit, `scale` for image-upscale, `format` for mesh-generate).
- **Command keywords**: Broader keyword lists covering synonyms for each skill:
  - image-edit: `edit`, `inpaint`, `outpaint`, `composite`, `modify`, `change`
  - background-remove: `background`, `remove`, `matting`, `cutout`, `isolate`
  - image-upscale: `upscale`, `enhance`, `super-resolution`, `scale`, `resize`
  - mesh-generate: `mesh`, `3d`, `mesh.generate`, `image-to-3d`, `model`
- **Shared base class**: Extract a `CreativeSkill` base class in `skills/core/` that encapsulates the discover→resolve→invoke→normalize→degrade flow parameterized by name, description, keywords, and param builder; each of the 4 skills is a thin subclass.
- **Observability / Logging**: Each skill MUST emit structured logs (JSON) for skill invocation, phase transitions, tool calls, errors, and outcomes. Use the existing `setup_logging()` in `skills/core/utils.py`. PII/secrets MUST be redacted at write time. (Research: AWS Well-Architected AGENTOPS05-BP03, OpenTelemetry GenAI semantic conventions, LangChain ADLC, Strands Agents all converge on structured logging + RED metrics for agent skills.)
- **Rate limiting**: Each skill MUST retry CLI invocations with exponential backoff + jitter on timeout or non-zero exit code (max 3 retries). Skills MUST use a semaphore-based concurrency limiter (max 3 concurrent CLI invocations per skill instance). (Research: Alibaba Cloud Model Studio rate-limiting best practices, SpillwaveSolutions subprocess patterns, SciPy Proceedings on bounded semaphore API gate.)
- **Asset uniqueness**: `asset_id` MUST be pass-through from CLI/MCP output (no server-side generation). Skills MAY optionally use content-addressing (SHA-256 of asset contents) for caching/deduplication, but MUST NOT generate asset IDs independently of CLI output. (Research: arXiv 2606.31272 per-component skill identity fingerprinting, aivitamin.org content hash cache pattern; no agentskills.io standard exists.)
- **Concurrent execution**: Each skill MUST use a semaphore-based concurrency limiter (max 3 concurrent CLI invocations per skill instance) to prevent resource exhaustion. Local worker parallelism is separate from hosted API concurrency. (Research: SpillwaveSolutions subprocess patterns, SciPy Proceedings on bounded semaphore API gate.)
