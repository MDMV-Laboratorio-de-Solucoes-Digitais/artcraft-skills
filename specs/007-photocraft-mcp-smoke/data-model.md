# Data Model: PhotoCraft MCP Verified Local Smoke (007)

**Feature**: 007-photocraft-mcp-smoke  
**Date**: 2026-11-05  
**Spec**: `specs/007-photocraft-mcp-smoke/spec.md` (Draft, clarified C1–C4; scoped go Option A — stateless verified smoke, mock-first preserved)  
**Phase 0/1 context**: planning artifact for optional, explicit opt-in local verification. **Not a public API/schema change**; conceptual/runtime entities map to opt-in test/harness behavior reusing existing MCP adapter and skill contracts.

## Scope

Defines runtime/conceptual entities for the optional real-PhotoCraft MCP verification path: opt-in enablement, binary/root/timeout safety controls, stateless verification sequence (`tools/list` → `tools/call name=command_list`), evidence capture, normalized outcome mapping, and safe-access boundaries.

This feature does **not** add persistent storage, does **not** change public skill schemas/CLI/fallback/FR-005/FR-006 contracts, does **not** make default CI depend on a real PhotoCraft binary/server, and does **not** implement a stateful multi-call artifact-producing cycle (deferred Option B).

## Reused codebase surfaces (citations)

| Surface | Location | Role in 007 |
|---|---|---|
| CLI discovery | `skills/core/artcraft_app_client.py` → `discover_cli(cli_path=None)` | Reused for authorized local server/binary resolution context; 007 opt-in mode may prefer explicit binary override env, else PATH resolution only in opt-in mode launching a resolved absolute executable. No change to default discovery semantics. |
| MCP config normalization | `skills/core/artcraft_app_client.py` → `normalize_mcp_config(cfg)` | Reused to normalize harness-built `mcp_config` (transport/command/args/env/cwd/timeouts) without mutating inputs. |
| MCP stdio operations (stateless per call) | `skills/core/artcraft_app_client.py` → `mcp_tools_list(cfg, timeout=None)`, `mcp_tools_call(cfg, tool_name, arguments=None, timeout=None)` | Core invocation surface. Each call performs a full stdio session per call (no session reuse) — 007 relies on this boundary (FR-002, spec session-boundary note). |
| FR-006 failure reasons/helpers | `skills/core/artcraft_app_client.py` → `REASON_MCP_UNAVAILABLE`, `REASON_MCP_MISCONFIGURED`, `REASON_MCP_STARTUP_TIMEOUT`, `REASON_MCP_CALL_TIMEOUT`, `REASON_MCP_INVALID_RESPONSE`, `REASON_MCP_MISSING_CAPABILITY`, `REASON_MCP_TOOL_ERROR`, `_MCP_TIMEOUT_REASONS`, adapter structured error payloads/metadata | 007 outcomes/skip/failure reasons align to existing FR-006 taxonomy; no new public reason contract. |
| FR-005/selection hooks | `skills/core/creative_skill.py` → `execute()` mode validation (`cli|mcp|auto`), `_mcp_available`, `_mcp_command_list`, `_mcp_command_run`, explicit-MCP-no-reroute behavior | Preserved unchanged (FR-005). 007 verification may exercise adapter calls and, where useful, skill-facing normalization context; it MUST NOT alter selection/fallback. |
| Normalized skill result | `skills/core/base_skill.py` → `SkillResult(success, data, error, metadata)` (006/007 contract, unchanged) | Evidence/skill-facing normalization context maps to existing result shape; no schema change. |
| Existing optional placeholder | `tests/integration/test_mcp_stdio_photocraft_optional.py` (006 T007,T017; `@pytest.mark.integration`, deselected by default) | Current baseline: requires `ARTCRAFT_MCP_INTEGRATION=1`, `photocraft-cli` on PATH, `ARTCRAFT_MCP_READ_ROOT/WRITE_ROOT`; placeholder only. 007 planning supersedes behavior in-slice via new/updated opt-in harness/test + `quickstart.md`, while keeping opt-in/default-CI exclusion. |
| 006 patterns | `specs/006-mcp-stdio-functional-integration/{data-model,quickstart,research}.md`, `contracts/mcp-stdio-adapter-contract.md` | Entity/result/timeout/diagnostic-safe patterns reused; PhotoCraft is reference/verified target, not a new public contract. |

## Entities

### 1. `OptInVerificationRun` (runtime/orchestration)

An explicitly enabled maintainer action that exercises the real MCP path under bounded safety controls and records an outcome (spec Key Entity: Optional Local Verification Run; FR-001, FR-004, FR-006, FR-007).

| Field | Type | Required | Description / Validation |
|---|---:|---:|---|
| `enabled` | `bool` | yes | Derived from explicit opt-in (e.g. `ARTCRAFT_MCP_INTEGRATION=1`-style gate; exact name is implementation detail, but opt-in MUST be explicit). When false, run is skipped/excluded; default CI never enables (FR-001, FR-005, SC-002). |
| `binary_selection` | `object` | when enabled | `{override_env?, path_resolution_allowed: bool, resolved_executable: abs path|None, version_context?: string|object|None}`. Preferred: explicit binary override env. Else PATH resolution allowed **only** in opt-in mode, launching the resolved absolute executable. Must record path/version context when available; never log secrets. Unavailable/unresolvable binary → structured skip/failure (FR-004, FR-006). |
| `roots_policy` | `object` | when enabled | `{mode: "temp_auto"|"explicit_override", read_root, write_root, authorized: bool, cleanup_owner: "harness"|"maintainer"}`. Default auto-creates isolated temporary read/write roots with cleanup. Explicit absolute override roots allowed only as authorized opt-in and are maintainer-managed (not auto-deleted by harness). Missing/misconfigured/unauthorized boundaries → structured failure/skip (FR-004, FR-006, edge cases). |
| `timeout_policy` | `object` | yes (bounded default) | `{startup_timeout_s?, call_timeout_s?, overall_bound_s?}` positive when provided. Bounded execution required (FR-004). Maps to adapter timeout handling / FR-006 `mcp_startup_timeout`/`mcp_call_timeout`. |
| `mcp_config` | `object` (normalized) | when executing | Harness-built config passed to `normalize_mcp_config`/adapter calls: stdio transport, resolved command/args for PhotoCraft MCP headless mode, env/cwd as needed, automation read/write roots, bounded timeouts. Caller/harness input not mutated. |
| `cleanup_state` | `enum` | runtime | `not_needed` \| `pending` \| `completed` \| `failed` \| `maintainer_managed`. Temporary roots/process resources tracked for cleanup (FR-004, SC-003). |
| `outcome` | `NormalizedOutcome` | terminal | Final recorded result: skipped, passed, or failed with actionable reason/evidence context (FR-006, FR-007). |

**Validation rules**:
- Not explicitly enabled → terminal `skipped` outcome; MUST NOT launch real server; MUST NOT affect default mock-first runs.
- Enabled but binary unavailable/misconfigured or roots unsafe/misconfigured → terminal structured `skipped`/`failed` (FR-006-aligned reason), no unsafe launch/state leakage.
- Timeouts MUST be positive/bounded; unbounded waits are invalid.
- Binary/roots/env diagnostics recorded MUST be secret-safe (no tokens/credentials).

### 2. `MCPVerificationSequence` (runtime, stateless)

The minimal real-server proof sequence (FR-002, FR-003, FR-009): capability discovery plus one safe deterministic invocation. **Stateless by design**: each adapter call is a full stdio session per call; no retained session, no stateful artifact cycle.

| Step | Adapter call | Required | Expected evidence |
|---|---|---:|---|
| 1. Discovery | `mcp_tools_list(mcp_config, timeout?)` | yes | Non-error tools/capabilities payload or structured error. Minimal check: required discovery/invocation capabilities present for this smoke (primary target includes `command_list` invocable path); do **not** assert exact tool count or full catalog equality. |
| 2. Safe deterministic invocation | `mcp_tools_call(mcp_config, "command_list", arguments={}, timeout?)` | yes (primary proof) | Non-error, parseable/normalizable structured result sufficient for skill-facing normalization context. `command_list` is the primary safe deterministic target (engine discovery). No AI generation, no destructive effect required. |

| Field | Type | Description |
|---|---|---|
| `session_model` | constant `stateless_per_call` | Invariant: uses existing per-call adapter behavior; never assumes cross-call state. |
| `discovery_result` | `object` | Raw/normalized `tools/list` outcome + minimal capability presence summary. |
| `invocation_target` | `object` | `{name: "command_list", arguments: {...minimal/version-tolerant...}}` (primary). |
| `invocation_result` | `object` | Raw/normalized `tools/call` outcome. Defensive parsing of MCP `content`/text/structured payloads (edge case). |
| `capability_gap` | `object|None` | If required capability missing/differs across versions, records observed tool context and structured `mcp_missing_capability`/actionable skip-failure (edge case). |

**Validation rules**:
- `tools/list` success alone is insufficient; step 2 required for SC-001 proof.
- Assertions are minimal and version-tolerant: presence/non-error/normalizable shape, not exact counts/catalogs/AI claims.
- A tool-level error from a real server is a valid observed outcome → normalized/recorded as `mcp_tool_error` (or aligned reason), not treated as harness crash.
- Multi-step `create document -> command -> export artifact` across separate calls is **out of scope** and must be documented as session-boundary limit (FR-008, spec edge case).

### 3. `VerifiedCapabilityEvidence` (recorded evidence)

Observed proof for maintainers/reviewers (spec Key Entity; FR-007, FR-008, SC-001, SC-004).

| Field | Type | Description |
|---|---|---|
| `command_shape` | `object/string` | Verified invocation shape (discovery + `tools/call command_list`) and relevant MCP config shape, redacted/safe. |
| `preconditions` | `object` | Explicit opt-in, binary selection mode, root policy, timeout bounds. |
| `binary_identity` | `object` | Resolved absolute path and version/context when available; absence recorded explicitly. |
| `discovery_summary` | `object` | Minimal observed capability facts (e.g., required capabilities present; relevant tool names/context) — no full catalog dump required. |
| `invocation_summary` | `object` | Non-error/normalizable result summary for `command_list`; defensive parse notes if applicable. |
| `limits` | `array[string]` | MUST include: stateless per-call session boundary; stateful artifact cycle out of scope; local PhotoCraft MCP = engine/editor automation; AI generation/providers/models out of scope unless separately evidenced (FR-008). |
| `observed_at` / `environment_note` | `string/object` | Local/maintainer context as safe metadata (no secrets). |

### 4. `NormalizedOutcome` / `SkillResult` mapping context (conceptual)

Maps real MCP/verification outcomes to actionable records and, where applicable, existing skill-facing result semantics (spec Key Entity: Skill-Facing Result Normalization Context; FR-005, FR-006, FR-009). **No `SkillResult` schema change**.

| Outcome class | Typical FR-006-aligned reason/metadata | Terminal run state | Notes |
|---|---|---|---|
| Not opted in / excluded | documented skip (harness reason, e.g. `opt_in_required`/test skip) | `skipped` | Default CI path; mock-first preserved (FR-001, SC-002). |
| Prerequisite/binary missing | `mcp_unavailable` / `cli_not_found`-adjacent context as applicable | `skipped` or `failed` (actionable) | Explicit, non-hanging. |
| Roots/boundary misconfigured or unauthorized | `mcp_misconfigured` or actionable validation failure | `failed`/`skipped` | No unsafe filesystem access (FR-004). |
| Startup/call timeout | `mcp_startup_timeout` / `mcp_call_timeout` | `failed` | Bounded stop + cleanup (FR-004, FR-006). |
| Invalid/unexpected response or parse issue | `mcp_invalid_response` | `failed` | Defensive MCP payload parsing. |
| Missing required capability | `mcp_missing_capability` | `failed`/`skipped` (actionable, version-tolerant) | Record observed tool context. |
| Tool-level error (`isError`/tool failure) | `mcp_tool_error` (+ protocol/tool metadata where safe) | `failed` | Real server behavior recorded, not masked. |
| Verified success | success metadata (`mode`/interface/tool context as applicable) | `passed` | Discovery + `command_list` invocation non-error and normalizable (FR-002, FR-009, SC-001). |

**Mapping rules**:
- Reuse existing FR-006 reason taxonomy and metadata keys/patterns from `artcraft_app_client.py` / 006 contract where the condition matches; add only harness-local, non-public skip reasons if needed (documented, not a skill-schema change).
- `SkillResult` remains `{success, data, error, metadata}` compatible when skill-facing normalization is exercised; 007 primarily records verification evidence.
- Explicit MCP/verification failures MUST NOT silently reroute to CLI/fallback (preserve FR-005 contract).

### 5. `SafeAccessBoundary` (policy/resource)

Bounded read/write location policy for the verification run (spec Key Entity; FR-004, SC-003).

| Mode | Behavior | Cleanup | Validation |
|---|---|---|---|
| `temp_auto` (default) | Auto-create isolated temporary read/write roots for the run | Harness cleans created temp resources on success/failure/timeout paths where feasible | Roots must be absolute/resolved, contained to created temp area, not user-secret locations. |
| `explicit_override` (authorized opt-in only) | Maintainer supplies explicit absolute read/write roots | **Maintainer-managed**; harness MUST NOT delete override roots | Must be explicit opt-in, absolute, authorized/bounded for the local run; misconfiguration is actionable failure/skip. |

**Invariants**: no unsafe filesystem access; no default-CI dependence; no silent widening of access; cleanup never targets explicit override roots.

## State transitions

### `OptInVerificationRun` lifecycle

```text
[default / not opted in]
  -> skipped_excluded                      (terminal; no launch, no cleanup side effects)

[explicit opt-in]
  -> evaluating_prerequisites
      -> skipped_unavailable               (binary/prereq missing; FR-006-aligned)
      -> failed_misconfigured              (roots/config/binary selection invalid; FR-006-aligned)
      -> preparing_boundaries
          -> failed_misconfigured          (cannot create/authorize safe roots)
          -> running_discovery             (MCPVerificationSequence step 1)
              -> failed_{startup_timeout|call_timeout|invalid_response|unavailable|misconfigured}
              -> failed_missing_capability (required smoke capability absent)
              -> running_invocation        (step 2: tools/call command_list)
                  -> failed_{startup_timeout|call_timeout|invalid_response|tool_error|missing_capability}
                  -> passed_verified        (discovery + invocation non-error/normalizable)
  -> cleaning_temp_resources               (temp_auto only; best-effort, bounded)
      -> cleanup_completed | cleanup_failed (cleanup failure recorded; does not fabricate verification success)
  -> terminal outcome recorded             (EvidenceRecord persisted in docs/test output context as applicable)
```

### `SafeAccessBoundary` / cleanup

```text
temp_auto:      planned -> created -> in_use -> cleanup_pending -> cleaned | cleanup_error
explicit_override: declared -> authorized -> in_use -> maintainer_managed (no harness delete)
```

## Invariants

- **Default safety (FR-001, FR-005, SC-002)**: Real PhotoCraft verification is optional and explicitly enabled only; excluded from default CI/`pytest -q` mock-first runs. Baseline mock-first/selection contracts remain preserved.
- **No contract drift (FR-005, FR-009, SC-005)**: No public schema/CLI/fallback/FR-005/FR-006 contract changes. `SkillResult` shape remains backward-compatible. Explicit MCP-mode behavior is not silently rerouted.
- **Stateless adapter boundary (FR-002, FR-008)**: Each `mcp_tools_list`/`mcp_tools_call` is a full stdio session per call; 007 MUST NOT assume session reuse or implement stateful artifact cycles.
- **Deterministic safe proof (FR-002, FR-003, FR-009)**: Proof = `tools/list` + one safe deterministic `tools/call` (`command_list` primary). Minimal, version-tolerant assertions; defensive MCP `content`/result parsing. No exact tool count, no full catalog equality, no AI generation/provider/model claim.
- **Safety controls (FR-004, SC-003)**: Explicit opt-in; authorized binary selection (override env preferred, else PATH only in opt-in mode with resolved absolute executable); bounded timeouts; safe read/write boundaries; temp roots cleaned; explicit override roots never deleted by harness; no unsafe process/file state leakage; no secret logging.
- **Actionable outcomes (FR-006, SC-003)**: Supported/expected conditions (missing opt-in/prereq, unavailable/misconfigured server, timeout, invalid response, missing capability, tool-level failure) produce structured/actionable skip or failure outcomes aligned to FR-006 taxonomy where applicable.
- **Evidence (FR-007, FR-008, SC-001, SC-004)**: Records command shape, safety preconditions, binary/path-version context when available, capability/invocation summary, and explicit limits (stateless boundary, no stateful artifact cycle, engine/editor automation only, AI out of scope).

## FR traceability

| FR | Entity coverage |
|---|---|
| FR-001 | `OptInVerificationRun.enabled`, skipped/excluded transitions |
| FR-002 | `MCPVerificationSequence` steps 1–2, stateless per call |
| FR-003 | `invocation_target=command_list`, deterministic/safe/non-AI invariants |
| FR-004 | `OptInVerificationRun` binary/roots/timeout/cleanup, `SafeAccessBoundary` |
| FR-005 | Reused FR-005 hooks/contracts preserved; no reroute; no schema changes |
| FR-006 | `NormalizedOutcome` mapping aligned to FR-006 reasons |
| FR-007 | `VerifiedCapabilityEvidence` / evidence record fields |
| FR-008 | `limits` and invariants documenting session boundary and non-AI scope |
| FR-009 | Discovery + invocation + skill-facing normalization context as verified evidence (no new AI capability/workflow) |
