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
3. **Given** a supported MCP entrypoint returns an operation-level failure, **When** the skill executes the operation, **Then** the system returns a structured failure with actionable error information and does **not** silently reroute to CLI/fallback when `mode=mcp` was explicitly requested (explicit mode wins; FR-005). Graceful fallback/degradation applies only where the documented selection policy allows it (for example, `auto` selecting another path per FR-005).

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
  - The system returns a structured `mcp_invalid_response`/mapping failure (FR-006 minimum reason taxonomy), performs safe cleanup, and leaves no unsafe/ambiguous state.
- What happens when MCP is explicitly requested but unavailable, versus when automatic selection is used?
  - Explicit `mode=mcp` returns a structured MCP failure (no silent CLI reroute). `auto` follows FR-005 back-compatible selection (CLI available → MCP available/configured → fallback/degradation).
- What happens when the same operation is attempted after a prior MCP failure—does the system avoid unsafe state leakage and follow the documented selection/fallback policy?
  - Prior failure must not leak process/session state. Subsequent attempts re-evaluate selection from current state (FR-005). After partial startup or transport/protocol failure, the MCP stdio subprocess session is invalid and must be cleaned up before any retry (FR-007).
- Stdio protocol/message edge cases (MCP 2026-07-28 stdio/cancellation guidance, bounded for 006): JSON-RPC responses are correlated by `id`; unmatched/duplicate/late/unsolicited responses are handled as structured protocol failures (or safely handled per documented rule) and never corrupt normalized results. EOF/exit-mid-transmission, invalid framing/JSON, or partial unusable response → structured protocol/transport failure + safe cleanup. Spawn/command-not-found/permission/OS launch failures → structured unavailable/misconfigured/launch failure with actionable guidance. Diagnostic output on stderr never replaces or pollutes stdout protocol messages.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support a minimum functional MCP integration over the local standard-input/standard-output transport using a generic, standards-compliant MCP tools contract (capability discovery and operation invocation). PhotoCraft headless MCP is the confirmed **reference target** for documentation and optional/manual validation; default automated acceptance remains deterministic mock/fake MCP verification, not a mandatory real PhotoCraft binary or blanket default support for every environment.
- **FR-002**: The system MUST provide MCP capability discovery and one supported operation invocation (discovery + invocation path) that demonstrates end-to-end value for at least one existing creative-skill path. For 006 acceptance, “end-to-end value” means: a deterministic mock MCP path performs discovery plus invocation for one supported operation mapped to the `image-edit` creative-skill path (primary example) and returns a normalized success or structured failure in the existing skill result contract. Target-specific tool naming (for example, PhotoCraft engine-oriented tool mappings) MUST be documented as reference mapping, not hard-coded as the universal contract.
- **FR-003**: The system MUST normalize MCP success and failure outcomes into the existing skill result contract without changing public skill schemas or breaking backward-compatible inputs/outputs. **“Public skill schemas unchanged” (006 scope)** means: existing skill input fields, enums, and default semantics remain valid (`mode` `cli|mcp|auto`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`, `timeout`, and skill-specific inputs); `skills.core.base_skill.SkillResult` fields/meaning (`success`, `data`, `error`, `metadata`) remain backward-compatible; metadata additions are additive and optional for existing consumers.
- **FR-004**: The system MUST preserve existing non-MCP behavior: current CLI and fallback paths remain available, and MCP integration MUST NOT remove or regress them.
- **FR-005**: The system MUST apply a documented selection policy when multiple execution paths are possible (explicit MCP request, explicit non-MCP request, and automatic selection). **Explicit mode always wins**. **Explicit `mode=mcp` MUST NOT silently reroute to CLI or fallback on MCP unavailability, timeout, invalid response, missing capability, or operation failure;** it MUST return a structured MCP failure with selection/MCP context. The **default automatic-selection behavior MUST remain back-compatible**: prefer CLI when CLI is available, then MCP when MCP is available/configured, then fallback/degradation according to existing documented rules. **For 006, “existing documented rules” are bounded to current `CreativeSkill`/adapter behavior and this feature’s contract (`contracts/mcp-stdio-adapter-contract.md` §2/§6); 006 adds the MCP path only and does not redefine unrelated legacy fallback semantics.** Any MCP-preferred automatic behavior is out of minimum-scope default behavior and, if introduced later, MUST be explicitly opted into and documented without breaking public schemas. **Ambiguous inputs** (for example `cli_path` present but unusable, `mcp_config` present, or conflicting non-explicit hints) are resolved by explicit mode when present; otherwise by the back-compatible `auto` order using current availability/preflight. **Recovery**: a failed attempt returns a structured failure, leaves no unsafe state, and subsequent attempts re-evaluate selection from current state (no sticky corrupted session).
- **FR-006**: The system MUST handle MCP unavailability, startup/communication timeout, invalid protocol/response data, missing capability, and operation failure as structured, diagnosable outcomes with clear reasons. **Minimum failure metadata (additive, no secret/PII leakage)**: `SkillResult.error` is a human-actionable message with remediation hint where safe; `metadata.mode` records requested/effective mode context; `metadata.reason` is a stable, documented, compatibly-extensible reason code (006 minimum set: `mcp_unavailable`, `mcp_misconfigured`, `mcp_startup_timeout`, `mcp_call_timeout`, `mcp_invalid_response`, `mcp_missing_capability`, `mcp_tool_error`, `cli_not_found`, `neither_available`); `metadata.interface`/`tool` identifies the MCP path/tool when attempted; `metadata.error_stage` (or equivalent, e.g., `launch`/`initialize`/`discovery`/`invocation`/`normalization`/`cleanup`) is included where available; timeout/protocol/cleanup context may be included when safe and bounded.
- **FR-007**: The system MUST isolate subprocess communication safely: protocol communication MUST remain usable even when diagnostic output is present, and failures MUST not leave the skill in an unsafe or ambiguous state. **MCP stdio subprocess-session invariants (006 behavioral minimum; exact numeric control values remain bounded/deferred by Assumptions line 114):** stdout carries only newline-delimited JSON-RPC MCP protocol messages; stderr is diagnostic-only. Requests and responses are correlated by JSON-RPC `id`; unmatched, duplicate, late, or unsolicited protocol messages MUST NOT corrupt normalized results and MUST produce a structured protocol failure or be safely handled per documented rule. On startup/communication timeout, invalid framing/JSON, EOF/exit-mid-transmission, partial unusable response, or caller abort, the adapter performs safe cleanup (close stdin, bounded wait, terminate/kill fallback as needed). A session is invalid after partial startup failure or transport/protocol failure and MUST be cleaned up before retry. Cleanup is objectively complete when no MCP subprocess is left running for that session and protocol streams are closed; spawn/command-not-found/permission/OS launch failures are classified as structured unavailable/misconfigured/launch failures with actionable guidance. No blind retries of non-idempotent tool calls.
- **FR-008**: The system MUST support deterministic automated verification for the minimum MCP scope using mock/fake MCP servers or subprocesses; standard repository verification MUST NOT require real credentials, paid services, network access, or mandatory real ArtCraft binaries.
- **FR-009**: The system MUST document the initial supported target, supported operations, selection policy, known limitations, and any optional path for real-environment validation.
- **FR-010**: The system SHOULD provide an optional, clearly separated path for maintainers to validate against a real MCP-capable ArtCraft environment when available, without making that path mandatory for standard CI.

### Key Entities *(include if feature involves data)*

- **MCP Entrypoint Configuration**: The user- or environment-provided information needed to locate and run a supported MCP-capable application entrypoint, including any required access boundaries for that target.
- **Capability Discovery Result**: The set of capabilities/operations reported by the target MCP entrypoint that can be evaluated for support.
- **Operation Invocation**: A request to execute one supported capability with mapped inputs and contextual metadata, producing a structured outcome.
- **Normalized Skill Result**: The existing skill-facing success/failure result, including human-actionable reason/error information and relevant metadata. Minimum additive failure metadata follows FR-006; success metadata may include `mode`, `interface`, and tool/capability context without breaking existing consumers.
- **Selection Policy Decision**: The outcome of choosing MCP, CLI, fallback, or no-available-path based on explicit request, configuration, and availability.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In deterministic automated tests, 100% of defined minimum-scope scenarios demonstrate successful capability discovery and successful invocation for each in-scope supported operation through the MCP path, with results normalized to the existing skill result contract.
- **SC-002**: In deterministic automated tests, 100% of defined failure scenarios (unavailable entrypoint, timeout, invalid response, missing capability, operation failure) produce structured, diagnosable failures without breaking the existing result contract.
- **SC-003**: Existing repository quality gates remain green after integration: at least 373 automated tests pass and 12/12 skills remain valid, with no regressions attributable to MCP integration.
- **SC-004**: Standard automated verification for this feature completes without real credentials, paid services, network access, or mandatory real ArtCraft binaries in 100% of CI/local default runs.
- **SC-005**: Maintainers and integrators can identify, from project documentation, the supported initial target, supported operations, selection policy, and out-of-scope boundaries in under 5 minutes during review/onboarding.

## Clarifications

### Session 2026-11-05

- Q: Initial MCP target/entrypoint — default support or reference-only validation? → A: Generic stdio MCP tools contract as 006 deliverable; PhotoCraft headless MCP confirmed as reference target for documentation/optional validation; default CI acceptance uses deterministic mock/fake MCP (Q1:B).
- Q: Which 1–2 MCP operations and end-to-end acceptance mapping? → A: Protocol-level capability discovery plus one operation invocation; end-to-end value = deterministic mock MCP path mapped to the `image-edit` creative-skill path returns normalized `SkillResult` success/structured failure; target-specific tool naming documented as reference mapping (Q2:A).
- Q: Automatic-selection order/precedence? → A: Explicit mode always wins; default `auto` remains back-compatible = CLI available → MCP available/configured → fallback/degradation; no MCP-preferred default in 006 (Q3:C, default A).
- Q: Must explicit `mode=mcp` ever fall back to CLI/fallback on MCP failure? → A: No. Explicit `mode=mcp` never silently reroutes; return structured MCP failure with selection/MCP context. “Fallback behavior where applicable” applies only to non-explicit/`auto` policy paths (Q4:A; resolves US1 Scenario 3 tension with FR-005).
- Q: What minimum failure metadata is required for FR-006/SC-002 diagnosability? → A: Additive minimum fields: human `error` + remediation hint (safe), `metadata.mode`, stable `metadata.reason` (006 set), `metadata.interface`/`tool` when attempted, `metadata.error_stage` where available, safe bounded context; no secret/PII leakage (Q5:A).
- Q: Which subprocess/MCP behavioral invariants must be specified now vs. numeric defaults deferred? → A: Specify JSON-RPC `id` correlation/disorder handling, stdout-protocol/stderr-diagnostic isolation, EOF/exit-mid-transmission/invalid-framing classification, spawn/launch-failure classification, partial-startup/session-invalid + cleanup-before-retry, objective cleanup completion, no blind non-idempotent retries; exact timeout/signal durations remain bounded/deferred (Q6:A).
- Q: How are fallback rules, schema scope, selection coverage, recovery, and ambiguous inputs bounded? → A: Bound fallback rules to existing `CreativeSkill`/adapter behavior + `contracts/mcp-stdio-adapter-contract.md` §2/§6; scope schema stability to existing inputs/enums/defaults + `SkillResult` shape/meaning + additive metadata; require explicit CLI/CLI-first-auto/MCP-unavailable selection coverage; re-evaluate selection after failure with no sticky corrupted session; resolve ambiguous non-explicit inputs by back-compatible `auto` order (Q7:A).
- Q: What verification contract is required at spec level? → A: Mandate minimum deterministic mock stdio MCP behavior (handshake as required, `tools/list`, one `tools/call` success/missing-capability/tool-error/invalid-response/timeout-hang classes), SC-005-style ambiguous-failure evidence protocol for the supported stdio path (recorded run conditions, FR-006 reason/stage classification, zero reproducible ambiguous transport failures in validation runs), parity bounded to equivalent `SkillResult` semantics/normalized outputs for operations supported by both paths, regression set = existing `SkillResult`/schema/`CreativeSkill` selection tests + 12/12 skill validation baseline, minimum supported environment = Linux + Python/pytest with packaged/test entrypoint or mock subprocess (SC-004). Exact fixture code/marker names remain implementation details (Q8:A).
- Q: What explicit-mode observability/correlation fields are required beyond minimum metadata? → A: Keep FR-006 minimum fields required; add optional additive correlation fields when available/safe (`metadata.request_id`/JSON-RPC `id`, `metadata.operation_id`/session token, bounded trace context). Explicit requested mode must remain observable. No new correlation IDs required for existing consumers (Q9:A).
- Q: What repeatability/coverage protocol is required for deterministic outcomes? → A: Each defined mock scenario class passes in the default deterministic suite with stable expected `reason`/`error_stage` for failure cases (same scenario conditions → same classification) in the 006 mock scope; nondeterministic classification is a defect. No fixed rerun count mandated unless flake is observed (Q10:A).
- Q: Must verification evidence include explicit FR/SC traceability? → A: Yes, lightweight mapping required: 006 acceptance evidence (test names, quickstart notes, or review report) must map each covered scenario class to FR/SC IDs (table or inline tags); no specific tool format mandated (Q11:A).
- Q: What is the canonical conformance baseline? → A: Repository `SkillResult`/public schema contracts + existing `CreativeSkill`/adapter CLI/selection behavior as exercised by the pre-006 green test/validation baseline on the integration branch; implementation PR records commit/SHA or test summary (Q12:A).


### Verification Contract (006 minimum)

- **Mock/fake stdio MCP (default CI/local)**: Deterministic subprocess/server MUST speak newline-delimited JSON-RPC on stdout and diagnostics on stderr only. Minimum scenario classes: successful discovery (`tools/list`) + one successful `tools/call` mapped to `image-edit` (SC-001), missing capability, tool-level error/`isError`, invalid JSON/protocol/framing or unusable response, timeout/hang/no usable response, unavailable/misconfigured/launch failure. No real credentials, paid services, network access, or mandatory real ArtCraft binaries (FR-008, SC-004). **Repeatability/classification stability (Q10:A)**: each scenario class passes in the default deterministic suite with stable expected FR-006 `reason`/`error_stage` for failure cases under the same scenario conditions; nondeterministic classification is a defect for the 006 mock scope. No fixed rerun count is mandated unless flake is observed.
- **Selection/back-compat evidence**: Explicit `mode=cli` and `mode=mcp` behavior, default `auto` CLI-first when CLI is available (including MCP configured but not selected by `auto`), CLI unavailable + MCP available/configured, and no-interface/degradation outcomes MUST be covered by deterministic tests or documented scenario evidence. Existing regression set includes `SkillResult`/schema/selection contract tests and repository baseline gates (SC-003). **Conformance baseline (Q12:A)** is the repository `SkillResult`/public schema contracts plus existing `CreativeSkill`/adapter CLI/selection behavior as exercised by the pre-006 green test/validation baseline on the integration branch; the implementation PR records commit/SHA or test summary.
- **Parity boundary**: For operations supported by both CLI and MCP paths, parity is required for `SkillResult` success/failure semantics and normalized output fields; transport-specific metadata may differ and MUST remain additive/non-breaking.
- **Ambiguous-failure evidence**: Validation runs for the supported stdio path MUST record run conditions and classify failures by FR-006 `reason`/`error_stage`; “ambiguous transport failure” means an MCP stdio-path failure that cannot be attributed to a defined stage/reason. Target for 006 supported mock scope is zero reproducible ambiguous transport failures.
- **Traceability (Q11:A)**: 006 acceptance evidence (test names, quickstart notes, or review report) MUST map each covered scenario class to FR/SC IDs (lightweight table or inline tags); no specific tool format is mandated.
- **Support matrix (minimum)**: Linux + Python/pytest environment with a test/packaged entrypoint or mock subprocess is the minimum supported/default verification environment (SC-004). Other environments are best-effort unless separately validated; optional real PhotoCraft validation is non-default (FR-010). Exact fixture code, test names, marker mechanics, and optional correlation field names are implementation details.
## Assumptions

- The first implementation targets the smallest valuable slice (Option A): one confirmed reference target (PhotoCraft headless MCP) and one invoked operation after discovery, proven via deterministic mock/fake MCP, not broad multi-app/multi-domain coverage.
- PhotoCraft is the reference validation candidate because public project documentation describes a local MCP entrypoint; exact reference command/roots and any target-specific mapping are finalized during planning and documented before implementation is considered complete.
- Existing public skill input/output schemas and the `SkillResult` contract remain stable; MCP support is additive.
- Deterministic mock/fake MCP subprocess coverage is sufficient for standard CI confidence; real-environment validation is optional and environment-dependent.
- Safe operational defaults (bounded waiting, clear failure reasons, isolation of diagnostic output from protocol handling) are required; exact control values and any optional advanced controls are selected during planning within the minimum-scope goal.
- Selection-policy behavior is treated as user-visible: default automatic behavior preserves current expectations for existing CLI/fallback users unless an explicit MCP choice is made.
- Roadmap/objective hygiene (001/005/006 state, 373 tests, next focus MCP) is already handled and not part of this feature’s deliverable.

## Dependencies

- Availability of assessment artifacts for this slug (`intake`, `research`, `problem`, `concept`, `decision`) as product context.
- Existence of current creative-skill execution paths (CLI and fallback) that must remain compatible.
- Access to accurate MCP target documentation/behavior for the confirmed reference entrypoint (PhotoCraft) before final reference mapping documentation is locked.
