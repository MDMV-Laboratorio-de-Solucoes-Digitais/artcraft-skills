# Feature Specification: MCP stdio functional integration (minimum scope)

**Feature Branch**: `006-mcp-stdio-functional-integration`  
**Created**: 2026-11-05  
**Status**: Draft  
**Input**: User description: "Use `.specify/assessments/mcp-stdio-functional-integration/` (GO handoff, Option A) to specify minimal functional MCP stdio integration: discovery + tool invocation for 1 target/1–2 operations, `SkillResult` normalization, preserve CLI+fallback and public contracts, graceful degradation, deterministic mock-first tests; no public schema breaks."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Execute a supported creative operation through a real MCP path (Priority: P1)

A maintainer or agent operator configures a supported ArtCraft application entrypoint that exposes MCP over the local standard-input/standard-output channel. When a creative skill requests a supported operation and the MCP path is selected or available, the system discovers the application’s exposed capabilities and invokes the chosen supported operation, returning a normalized success or failure result in the same result contract used by existing skills.

**Why this priority**: This closes the primary architectural gap (MCP remains mostly stubbed today) and proves end-to-end value for the minimum viable MCP integration.

**Independent Test**: Can be fully tested with a deterministic fake MCP server/subprocess that responds to capability discovery and a supported operation invocation; delivers a verifiable normalized result without real credentials, network access, or a real ArtCraft binary.

**Acceptance Scenarios**:

1. **Given** a supported MCP entrypoint is available and configured for a supported operation, **When** the skill executes that operation through the MCP path, **Then** the system discovers available capabilities, invokes the supported operation, and returns a successful normalized result consistent with the existing skill result contract.
2. **Given** a supported MCP entrypoint is available, **When** capability discovery returns no matching supported operation, **Then** the system returns a structured failure that identifies the missing capability and does not corrupt the existing result contract.
3. **Given** a supported MCP entrypoint returns an operation-level failure, **When** the skill executes the operation, **Then** the system returns a structured failure with actionable error information and preserves graceful fallback behavior where applicable.

---

### User Story 2 - Preserve existing behavior and degrade gracefully (Priority: P2)

An agent operator uses existing creative skills in environments where MCP is unavailable, misconfigured, slow, or returns invalid responses. The system continues to honor existing CLI and fallback behavior according to the defined selection policy, and failures are reported with clear reasons rather than silent breakage.

**Why this priority**: Backward compatibility and graceful degradation protect current users while MCP support is introduced incrementally.

**Independent Test**: Can be fully tested by simulating unavailable/misconfigured/failing MCP conditions alongside existing CLI/fallback paths; delivers confidence that existing flows remain functional or fail with structured, diagnosable outcomes.

**Acceptance Scenarios**:

1. **Given** MCP is unavailable or not configured, **When** a skill is executed under the applicable selection policy, **Then** the system uses the existing non-MCP path (CLI or fallback) when available, or returns a structured “no available interface/capability” failure.
2. **Given** MCP communication exceeds the allowed time or returns an invalid/unexpected response, **When** the skill executes, **Then** the system stops safely, reports a clear failure reason, and does not require external services or manual cleanup to continue subsequent operations.
3. **Given** the current repository test suite and skill validation baseline, **When** this feature is integrated, **Then** existing behavior remains compatible (no public schema breaks; baseline quality gates remain green).

---

### User Story 3 - Verify MCP integration deterministically and document limits (Priority: P3)

A maintainer runs automated checks locally or in continuous integration. The MCP minimum scope is verifiable without real credentials, paid services, network access, or mandatory real ArtCraft binaries. The supported target, supported operations, selection policy, and known limitations are documented.

**Why this priority**: Deterministic verification and clear limits make the integration safe to evolve and prevent overclaiming capability.

**Independent Test**: Can be fully tested by running the deterministic MCP mock/fake-subprocess test coverage and documentation checks; delivers repeatable evidence of the minimum supported MCP contract.

**Acceptance Scenarios**:

1. **Given** a continuous integration or local test environment without real MCP binaries or credentials, **When** automated tests for this feature run, **Then** the MCP minimum-scope scenarios pass deterministically.
2. **Given** maintainers and integrators need to understand support boundaries, **When** they read the feature documentation/contract notes, **Then** they can identify the initial target, supported operations, selection policy, failure reasons, and explicit out-of-scope areas.

---

### Edge Cases

- What happens when the MCP subprocess starts but produces no usable protocol response within the allowed time?
- What happens when the subprocess writes diagnostic output separately from protocol communication (diagnostics must not corrupt protocol handling or normalized results)?
- What happens when capability discovery succeeds but the selected tool/capability name is absent, renamed, or ambiguous?
- What happens when the MCP entrypoint requires environment-specific access boundaries (such as allowed read/write roots) and they are missing or invalid?
- What happens when an operation returns partial/invalid structured data that cannot be mapped to the existing result contract?
- What happens when MCP is explicitly requested but unavailable, versus when automatic selection is used?
- What happens when the same operation is attempted after a prior MCP failure—does the system avoid unsafe state leakage and follow the documented selection/fallback policy?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support a minimum functional MCP integration over the local standard-input/standard-output transport for at least one confirmed initial ArtCraft application entrypoint. [NEEDS CLARIFICATION: Which initial MCP target/entrypoint is confirmed for this feature (e.g., PhotoCraft headless MCP entrypoint with required access roots), and is that target in scope for default support or reference-only validation?]
- **FR-002**: The system MUST provide MCP capability discovery and invocation for 1–2 supported operations that demonstrate end-to-end value for at least one existing creative skill. [NEEDS CLARIFICATION: Which 1–2 MCP capabilities/operations are in scope, how do they map to an existing skill operation, and what constitutes “end-to-end value” for acceptance?]
- **FR-003**: The system MUST normalize MCP success and failure outcomes into the existing skill result contract without changing public skill schemas or breaking backward-compatible inputs/outputs.
- **FR-004**: The system MUST preserve existing non-MCP behavior: current CLI and fallback paths remain available, and MCP integration MUST NOT remove or regress them.
- **FR-005**: The system MUST apply a documented selection policy when multiple execution paths are possible (explicit MCP request, explicit non-MCP request, and automatic selection). [NEEDS CLARIFICATION: What is the automatic-selection order and precedence among CLI, MCP, and fallback to preserve current behavior while enabling MCP value?]
- **FR-006**: The system MUST handle MCP unavailability, startup/communication timeout, invalid protocol/response data, missing capability, and operation failure as structured, diagnosable outcomes with clear reasons.
- **FR-007**: The system MUST isolate subprocess communication safely: protocol communication MUST remain usable even when diagnostic output is present, and failures MUST not leave the skill in an unsafe or ambiguous state.
- **FR-008**: The system MUST support deterministic automated verification for the minimum MCP scope using mock/fake MCP servers or subprocesses; standard repository verification MUST NOT require real credentials, paid services, network access, or mandatory real ArtCraft binaries.
- **FR-009**: The system MUST document the initial supported target, supported operations, selection policy, known limitations, and any optional path for real-environment validation.
- **FR-010**: The system SHOULD provide an optional, clearly separated path for maintainers to validate against a real MCP-capable ArtCraft environment when available, without making that path mandatory for standard CI.

### Key Entities *(include if feature involves data)*

- **MCP Entrypoint Configuration**: The user- or environment-provided information needed to locate and run a supported MCP-capable application entrypoint, including any required access boundaries for that target.
- **Capability Discovery Result**: The set of capabilities/operations reported by the target MCP entrypoint that can be evaluated for support.
- **Operation Invocation**: A request to execute one supported capability with mapped inputs and contextual metadata, producing a structured outcome.
- **Normalized Skill Result**: The existing skill-facing success/failure result, including human-actionable reason/error information and relevant metadata.
- **Selection Policy Decision**: The outcome of choosing MCP, CLI, fallback, or no-available-path based on explicit request, configuration, and availability.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In deterministic automated tests, 100% of defined minimum-scope scenarios demonstrate successful capability discovery and successful invocation for each in-scope supported operation through the MCP path, with results normalized to the existing skill result contract.
- **SC-002**: In deterministic automated tests, 100% of defined failure scenarios (unavailable entrypoint, timeout, invalid response, missing capability, operation failure) produce structured, diagnosable failures without breaking the existing result contract.
- **SC-003**: Existing repository quality gates remain green after integration: at least 373 automated tests pass and 12/12 skills remain valid, with no regressions attributable to MCP integration.
- **SC-004**: Standard automated verification for this feature completes without real credentials, paid services, network access, or mandatory real ArtCraft binaries in 100% of CI/local default runs.
- **SC-005**: Maintainers and integrators can identify, from project documentation, the supported initial target, supported operations, selection policy, and out-of-scope boundaries in under 5 minutes during review/onboarding.

## Assumptions

- The first implementation targets the smallest valuable slice (Option A): one confirmed MCP entrypoint and 1–2 operations, not broad multi-app/multi-domain coverage.
- PhotoCraft is a reference candidate because public project documentation describes a local MCP entrypoint; final in-scope target and required access boundaries are confirmed during clarification/planning and documented before implementation is considered complete.
- Existing public skill input/output schemas and the `SkillResult` contract remain stable; MCP support is additive.
- Deterministic mock/fake MCP subprocess coverage is sufficient for standard CI confidence; real-environment validation is optional and environment-dependent.
- Safe operational defaults (bounded waiting, clear failure reasons, isolation of diagnostic output from protocol handling) are required; exact control values and any optional advanced controls are selected during planning within the minimum-scope goal.
- Selection-policy behavior is treated as user-visible: it must preserve current expectations for existing CLI/fallback users unless an explicit, documented MCP choice is made.
- Roadmap/objective hygiene (001/005/006 state, 373 tests, next focus MCP) is already handled and not part of this feature’s deliverable.

## Dependencies

- Availability of assessment artifacts for this slug (`intake`, `research`, `problem`, `concept`, `decision`) as product context.
- Existence of current creative-skill execution paths (CLI and fallback) that must remain compatible.
- Access to accurate MCP target documentation/behavior for the confirmed initial entrypoint (PhotoCraft or equivalent) before final operation mapping is locked.
