# Feature Specification: PhotoCraft MCP Verified Local Smoke

**Feature Branch**: `[007-photocraft-mcp-smoke]` *(proposed; branch may be created separately)*

**Created**: 2026-11-05

**Status**: Draft

**Input**: User description: "PhotoCraft MCP verified local smoke + one deterministic headless capability mapping (small, mock-first preserved). Reuse existing MCP adapter/FR-005/FR-006/tests; prove MCP against a real local PhotoCraft server for a useful deterministic flow without AI/cloud credentials; avoid claiming prompt-based AI generation via local PhotoCraft MCP. Minimum 80/20: optional deterministic safe local smoke (not default CI) for capability discovery + command discovery/invocation (optional artifact cycle in temporary write root only if safely supported), with explicit opt-in, explicit binary, temporary read/write roots, cleanup, timeout, and recorded evidence; map one concrete deterministic headless capability through the existing MCP/skill path with normalized skill results without breaking schemas/CLI/fallback; document limits (local PhotoCraft MCP = engine/editor automation; AI generation/providers out of scope) and verified runbook command; optional hygiene to disambiguate 006 spec references."

**Assessment handoff**: Scoped go (Option A) from `.specify/assessments/photocraft-mcp-verified-smoke/decision.md` — stateless verified smoke, mock-first preserved. Stateful artifact-producing cycle in one MCP session is deferred (Option B) due to current adapter session boundary.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Verify real local PhotoCraft MCP stateless smoke (Priority: P1)

A maintainer who has a compatible local PhotoCraft command-line server can explicitly opt in to a safe local verification flow. The flow proves that the existing MCP integration can start a real MCP session, discover exposed capabilities, and perform at least one safe deterministic tool invocation, returning a structured non-error result that can be normalized for the skill result contract.

**Why this priority**: This converts mock-only confidence into reproducible real-server evidence with minimal risk, reusing existing adapter behavior and protecting default automation from environment dependence.

**Independent Test**: Can be fully tested in an opted-in local environment with a real PhotoCraft binary by running the documented verification path; it delivers evidence of real capability discovery and one safe deterministic invocation without requiring AI credentials, cloud access, or default CI execution.

**Acceptance Scenarios**:

1. **Given** a maintainer has explicitly enabled the optional local verification, a compatible local PhotoCraft server is available, and safe temporary read/write boundaries are configured, **When** they run the verification, **Then** the system performs MCP capability discovery and confirms the presence of the minimal expected discovery/invocation capabilities needed for the smoke.
2. **Given** the same opted-in safe environment, **When** the maintainer runs the safe deterministic invocation step, **Then** the system completes the invocation and reports a structured, non-error result with enough information to normalize it as a skill-facing success and to record evidence (binary identity/version context where available, capability/result shape, and limits).
3. **Given** the maintainer has not explicitly enabled optional local verification, **When** default automated validation runs, **Then** the real PhotoCraft verification is skipped or excluded and mock-first/default validation behavior remains unchanged.

---

### User Story 2 - Preserve contracts and report safe failures (Priority: P2)

An integrator uses the existing MCP/CLI/fallback skill paths in environments where the real PhotoCraft server is absent, misconfigured, slow, or returns an unsupported/error response. The system preserves existing selection and fallback contracts, avoids unsafe cleanup/state leakage, and reports actionable failures.

**Why this priority**: Real-server verification must not reduce the safety or determinism of the existing mock-first integration; maintainers need clear failures, not ambiguous hangs or silent behavior changes.

**Independent Test**: Can be tested by exercising missing-binary, missing opt-in, misconfigured roots, timeout, and tool-error conditions in the optional verification path and by running default mock-first regression checks; it delivers confidence that failures are structured and existing contracts remain intact.

**Acceptance Scenarios**:

1. **Given** the optional verification is enabled but the local PhotoCraft server is unavailable, misconfigured, or not permitted to use the required access boundaries, **When** the verification runs, **Then** the system returns or records a structured, actionable failure/skip reason and does not change existing CLI/fallback behavior for unrelated default runs.
2. **Given** the optional verification encounters a timeout, invalid response, or tool-level error, **When** the verification runs, **Then** the system stops within bounded limits, cleans up temporary verification resources, and reports a diagnosable outcome without leaking unsafe process or file state.
3. **Given** existing mock-first MCP, skill validation, and public skill contracts, **When** this feature is delivered, **Then** default mock-first tests remain green, skill validation remains green, and existing public schemas, CLI behavior, fallback behavior, and MCP selection/failure contracts (including explicit MCP mode not silently rerouting) remain preserved.

---

### User Story 3 - Record evidence and capability limits (Priority: P3)

A maintainer or reviewer needs durable evidence that the real MCP path was proven locally and needs clear boundaries for what that proof means.

**Why this priority**: Without recorded evidence and explicit limits, teams may either distrust the integration or overclaim unsupported AI-generation capabilities.

**Independent Test**: Can be tested by reviewing the recorded runbook/evidence notes after an opted-in verification run; it delivers a reproducible command, observed result summary, and explicit scope limits.

**Acceptance Scenarios**:

1. **Given** an opted-in real local verification has been executed, **When** a maintainer reviews the feature evidence, **Then** they can find the verified command shape, opt-in/safety preconditions, observed capability/invocation result summary, and any session or environment limits.
2. **Given** the evidence and runbook documentation, **When** a maintainer evaluates local PhotoCraft MCP capabilities, **Then** the documentation states that local PhotoCraft MCP is engine/editor automation and that prompt-based AI generation/provider/model behavior is out of scope for this slice unless separately evidenced.

---

### Edge Cases

- What happens when the local PhotoCraft binary is present but its exposed tool set differs across versions (for example, missing `command_list`, `command_run`, or expected command identifiers)? The verification uses minimal capability checks and records a structured skip/failure reason rather than brittle exact-count assertions.
- What happens when `tools/list` succeeds but the selected safe invocation capability is unavailable or returns a tool-level error? The verification reports a structured missing-capability or operation-failure outcome with the observed tool context.
- How does the system handle PhotoCraft returning MCP tool results as structured content payloads whose text contains serialized data? The verification treats payload parsing defensively and accepts a non-error, parseable/normalizable structure as evidence.
- What happens when a maintainer expects a multi-step document cycle (`create document -> command -> export artifact`) across separate adapter calls? The verification and documentation state the current session boundary: stateless smoke is in scope; a stateful artifact-producing cycle requires a separately scoped session-capable follow-up.
- How does the system prevent unsafe filesystem access? The verification requires explicit opt-in and uses safe, bounded read/write boundaries (temporary or explicitly authorized absolute locations), cleans temporary resources, and never makes the real server path part of default CI.
- What happens when a local server reports engine-oriented export/conversion commands but no prompt-based AI generation capability? The slice records deterministic engine capability evidence only and does not present AI generation as supported.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an optional, explicitly enabled local verification path for the existing MCP stdio integration against a real PhotoCraft server; this path MUST be excluded from default automated validation.
- **FR-002**: The verification path MUST perform real MCP capability discovery and at least one safe deterministic MCP tool invocation using the existing MCP integration behavior, producing evidence that the real local path is operable for stateless interactions.
- **FR-003**: The verified invocation MUST be limited to deterministic engine/editor-oriented behavior with a non-destructive or safely contained effect; it MUST NOT claim, simulate, or require prompt-based AI image/video/audio/3D generation through local PhotoCraft MCP.
- **FR-004**: The verification path MUST enforce safety controls: explicit opt-in, an authorized local server selection, bounded execution time, safe read/write boundaries (temporary by default or explicitly authorized), and cleanup of temporary verification resources.
- **FR-005**: The system MUST preserve mock-first default behavior and existing contracts: public skill schemas unchanged, existing CLI behavior unchanged, existing fallback behavior unchanged, and existing MCP selection/failure contracts unchanged (including explicit MCP mode not silently rerouting to CLI/fallback).
- **FR-006**: The system MUST report actionable outcomes for supported success and failure conditions in the optional path, including unavailable server, missing opt-in/prerequisites, misconfigured access boundaries, timeout, invalid/unexpected response, missing capability, and tool-level failure.
- **FR-007**: The system MUST record reproducible verification evidence for maintainers, including the verified command shape, required safety preconditions, observed capability/invocation summary, relevant version/binary identity context when available, and known limits.
- **FR-008**: Documentation MUST state that local PhotoCraft MCP in this slice represents engine/editor automation, that the current adapter session boundary makes a stateful multi-call artifact-producing cycle out of scope for this slice, and that AI generation/providers/models are out of scope unless separately evidenced.
- **FR-009**: The slice MUST deliver the scoped “one deterministic headless capability mapping” as verified, normalized evidence of one safe deterministic MCP invocation path (discovery plus invocation, with skill-facing result normalization context) rather than introducing a new AI-generation capability or a stateful cross-call artifact workflow.

### Scope Boundaries & Dependencies *(include if relevant)*

- **In scope**: Optional local real-server smoke for stateless MCP discovery/invocation; deterministic minimal assertions; safety controls; evidence and runbook documentation; small directly related documentation clarifications.
- **Out of scope**: Default CI dependence on a real PhotoCraft binary/server; stateful session-capable adapter API; multi-step `create -> command -> export` artifact cycle across one retained MCP session; prompt-based AI generation/provider/model routing; public schema changes; CLI/fallback/selection contract changes; bridge mode, UI tools, progress/cancellation broad coverage, and deep spec renumbering.
- **Dependencies**: Existing MCP stdio adapter and mock-first tests (006), existing skill result normalization contracts, local availability of a compatible PhotoCraft server for opted-in runs, and maintainer access to safe local filesystem boundaries.

### Key Entities *(include if feature involves data)*

- **Optional Local Verification Run**: An explicitly enabled maintainer action that exercises the real MCP path under bounded safety controls and records an outcome.
- **Verified MCP Capability Evidence**: The observed capability-discovery and deterministic invocation results used to prove real local MCP behavior, including limits and environment context.
- **Safe Access Boundary**: A bounded read/write location policy for the verification run, temporary by default or explicitly authorized, with cleanup expectations.
- **Skill-Facing Result Normalization Context**: The structured success/failure information needed to map a real MCP outcome to the existing skill result contract without changing public schemas.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In an explicitly opted-in local environment with a compatible PhotoCraft server and safe access boundaries, maintainers can complete the documented verification path and obtain evidence of successful real MCP capability discovery plus one safe deterministic invocation in a single run.
- **SC-002**: Default automated validation remains independent of a real PhotoCraft server: 100% of default runs continue to execute mock-first behavior, with the existing baseline quality gates remaining green (`399` tests passed, `1` deselected integration test excluded by default, and `12/12` skills valid at the time of this slice’s baseline).
- **SC-003**: 100% of defined optional-path failure conditions covered by the slice (missing opt-in/prerequisite, unavailable/misconfigured server, timeout, invalid response, missing capability, tool-level failure) produce actionable, structured outcomes or documented skip/failure evidence without unsafe resource leakage.
- **SC-004**: Maintainers and reviewers can identify from the recorded documentation, in under 5 minutes, the verified command shape, required safety controls, observed proof, session boundary, and explicit non-AI-generation limits.
- **SC-005**: No public skill schema, existing CLI behavior, existing fallback behavior, or existing MCP selection/failure contract is regressed by the feature, as demonstrated by preserved mock-first/contract validation.

## Assumptions

- A compatible local PhotoCraft server is available only for maintainers who explicitly opt in; default contributors and CI environments are not expected to have it.
- Minimal capability assertions (presence of required discovery/invocation capabilities and non-error/normalizable result structure) are more stable than exact tool counts or full command catalogs across PhotoCraft versions.
- The current MCP adapter’s stateless per-call session boundary is a known constraint; proving that boundary and documenting it satisfies the scoped 80/20 goal. A stateful artifact-producing cycle is valuable but intentionally deferred to a separate follow-up decision/spec.
- Temporary access boundaries created for verification can be cleaned up automatically after the run; explicitly supplied boundaries remain the maintainer’s responsibility.
- Primary sources for capability limits and protocol behavior are the assessment research citations (MCP 2025-11-25 specs, PhotoCraft MCP/control docs, and local observed probe dated 2026-11-05). Web/community guides are supplementary and not normative.
