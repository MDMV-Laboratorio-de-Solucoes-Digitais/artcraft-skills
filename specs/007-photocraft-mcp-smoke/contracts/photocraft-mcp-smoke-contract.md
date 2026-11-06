# Contract: PhotoCraft MCP Verified Local Smoke (007, minimum scope)

**Feature**: 007-photocraft-mcp-smoke  
**Status**: Design/behavioral contract (Phase 1)  
**Type**: Behavioral/test contract for optional local verification — **no public schema, CLI, fallback, FR-005, or FR-006 contract changes**.

**Primary implementation/test surfaces** (planned): optional local verification harness/test under `tests/integration/` (or equivalent opt-in path, excluded from default CI/`pytest -q`), reusing `skills/core/artcraft_app_client.py` (`mcp_tools_list`, `mcp_tools_call`, FR-006 helpers/reasons) and/or equivalent 006 MCP/skill paths; evidence/runbook at `specs/007-photocraft-mcp-smoke/quickstart.md`.

## 1. Scope and limits

This contract defines the minimum verifiable real-local behavior for a **stateless** PhotoCraft MCP smoke path:

- Prove one real MCP stdio session can perform **`tools/list`** discovery and **one safe deterministic `tools/call`** invocation via the existing 006 adapter path.
- Primary safe invocation: **`command_list`** (engine/editor command discovery). This is **not** prompt-based AI generation.
- **Stateless adapter boundary**: each adapter call (`mcp_tools_list` / `mcp_tools_call`) performs a full stdio session per call. There is **no session reuse** and **no stateful artifact-producing cycle** (`create document -> command -> export`) in this slice.
- **Local PhotoCraft MCP** = engine/editor automation. AI generation, providers, models, and cloud credentials are **out of scope** unless separately evidenced.
- Default validation remains **mock-first**; this path is **optional and explicitly opt-in** and **excluded from default CI / `pytest -q`**.

**PhotoCraft reference command** (headless, normative reference for local opt-in runs; follow target docs for version details):

```bash
photocraft-cli mcp --automation-read-root <ABSOLUTE_SAFE_READ_ROOT> --automation-write-root <ABSOLUTE_SAFE_WRITE_ROOT>
```

Notes: root flags/mode semantics differ in bridge mode; optional real validation must follow PhotoCraft target docs. Use absolute, least-privilege roots.

## 2. Public compatibility (must preserve)

| Surface | Contract |
|---|---|
| Public skill schemas / inputs | Unchanged. No new required public fields. |
| `SkillResult` (`success`, `data`, `error`, `metadata`) | Meaning/compatibility unchanged. |
| CLI behavior, fallback behavior | Unchanged. |
| FR-005 selection | Unchanged, including explicit `mode=mcp` not silently rerouting to CLI/fallback and `auto` back-compat (CLI-first) behavior. |
| FR-006 MCP failure contracts | Preserved: existing reasons remain valid; 007 consumes/records them without breaking taxonomy or metadata semantics. |
| Default test behavior | Mock-first/default tests unchanged; optional real smoke excluded by default marker/opt-in. |

## 3. Opt-in harness preconditions, inputs, and skip/fail semantics

### 3.1 Explicit opt-in and safety controls (FR-001, FR-004)

The verification path MUST enforce all applicable controls before attempting a real MCP session:

1. **Explicit opt-in**: a dedicated opt-in signal is required (e.g., environment flag such as `ARTCRAFT_MCP_INTEGRATION=1` or an equivalent documented harness flag). Absence means the real verification MUST NOT run as part of normal/default execution.
2. **Authorized local server selection**:
   - **Binary override env preferred**: if a documented override env var names an absolute/local executable path (or explicit command), the harness uses it after safe validation (exists/executable as applicable).
   - **PATH fallback only in opt-in mode**: when opt-in is enabled and no override is provided, resolve `photocraft-cli` (or documented target name) from PATH and launch the **resolved absolute executable** path; record the resolved path.
   - Never auto-discover/run a real server outside explicit opt-in mode.
3. **Safe read/write boundaries**:
   - **Default**: harness auto-creates **isolated temporary read/write roots** (separate or clearly bounded paths) and **cleans them up** after the run, including on bounded failure paths where safe.
   - **Explicit absolute override roots**: allowed only as an **authorized maintainer opt-in** (e.g., dedicated env/config inputs). Overrides MUST be treated as maintainer-managed; harness MUST NOT delete or mutate user-managed override roots beyond what the invoked safe operation requires, and MUST record that cleanup is maintainer-managed for overrides.
4. **Bounded execution time**: startup/call/overall verification time MUST be bounded by documented defaults and/or explicit timeout inputs; no unbounded hang.
5. **No unsafe state leakage**: on timeout/invalid response/tool error/caller abort, harness/adapter paths MUST follow safe cleanup invariants (006 §9) and leave no leaked subprocess/session state attributable to the verification run.

### 3.2 Inputs (behavioral; names may be finalized in implementation but semantics are fixed)

| Input class | Semantics |
|---|---|
| Opt-in enablement | Required explicit signal; gates all real-server execution. |
| Server binary/command override | Optional; preferred over PATH resolution. Must resolve to an authorized local executable/command in opt-in mode. |
| Read root / write root overrides | Optional, absolute, maintainer-authorized only. If omitted, harness provisions isolated temp roots with cleanup. |
| Timeout(s) | Bounded startup/call/verification limits; safe defaults required. |
| Evidence/output destination (if any) | Additive; must not affect public skill schemas. May be console/structured report/runbook-recorded evidence. |

### 3.3 Skip vs fail semantics (FR-006, SC-003)

Outcomes MUST be actionable and structured/documented. Classification:

| Condition | Opt-in absent | Opt-in present |
|---|---|---|
| Missing opt-in | **Skip/excluded** (default runs never execute real smoke). | n/a |
| Missing local prerequisite not safely satisfiable in opted-in run (e.g., binary not found/resolvable, required env/config absent when harness cannot safely provision) | n/a | **Skip or structured prerequisite failure** with explicit reason; default CI behavior unchanged. Prefer `pytest.skip`/equivalent when invoked as optional test; prefer structured actionable outcome when invoked as explicit verification harness path. |
| Misconfigured access boundaries (unsafe/invalid/unusable roots, override not absolute/authorized as required) | n/a | **Structured failure** (actionable). Do not silently fall back to unsafe defaults when an explicit override is invalid. |
| Server unavailable/startup failure/timeout | n/a | **Structured failure** with FR-006-aligned reason/metadata (e.g., `mcp_unavailable`, `mcp_startup_timeout`). |
| Invalid/unexpected response, missing capability, tool-level error | n/a | **Structured failure** with FR-006-aligned reason/metadata (e.g., `mcp_invalid_response`, `mcp_missing_capability`, `mcp_tool_error`). |
| Success | n/a | **Structured/recorded success** with evidence fields (§6). |

**No silent reroute**: the optional verification path MUST NOT silently reroute an explicit MCP verification attempt to CLI/fallback. FR-005/FR-006 semantics remain observable.

## 4. MCP interaction contract (stateless smoke)

All real MCP protocol interactions for this smoke MUST go through the existing 006 adapter behavior (`artcraft_app_client.mcp_tools_list` / `mcp_tools_call`) or an equivalent path that preserves the same framing, timeout/cleanup, and FR-006 normalization semantics. The harness MUST NOT introduce a parallel ad hoc MCP client with divergent behavior.

### 4.1 Discovery: `tools/list`

- Invoke MCP discovery equivalent to `tools/list` for the configured local PhotoCraft stdio server.
- **Expectation (version-tolerant)**: the returned capability/tool listing contains a tool/capability named **`command_list`** (presence check). Do **not** assert exact tool count, full catalog equality, ordering, or undocumented extra fields.
- Accept discovery payload shapes defensively (direct tools list/result object/adapter-normalized success shape) consistent with 006 adapter behavior.

### 4.2 Invocation: `tools/call` `command_list`

- Invoke exactly one safe deterministic MCP tool call: `name=command_list` (or equivalent normalized tool identifier for the target).
- **Arguments**: minimal and safe (empty object `{}` / no risky parameters) unless target version requires a documented safe no-op form; do not pass document-mutating/export paths, user data, or generation prompts.
- **No AI generation claim**: do not invoke prompt-based image/video/audio/3D generation tools; do not interpret `command_list`/engine discovery as AI provider/model support.

### 4.3 Defensive MCP result acceptance

The verification/harness normalization MUST accept MCP/adapter outcomes defensively:

- Success may arrive as an adapter-normalized success dict, a JSON-RPC `result`, or MCP tool `content` payloads (including text/serialized content that is parseable/normalizable).
- Tool-level/protocol failure may arrive as `isError`/`is_error`, error payloads, adapter structured failures, or missing/invalid result shapes.
- A **non-error, parseable/normalizable structure** from the safe `command_list` invocation is sufficient evidence of stateless invocation operability; brittle deep schema equality is forbidden.
- Redact/avoid secrets, PII, and sensitive filesystem details in recorded evidence beyond what is necessary and safe (e.g., do not dump raw sensitive stderr/config; prefer resolved path/version context and bounded summaries).

## 5. Adapter reuse and FR-006 preservation

1. **Reuse required**: use existing `artcraft_app_client.mcp_tools_list` and/or `artcraft_app_client.mcp_tools_call` (or the same 006 skill/adapter path they serve) for real MCP discovery/invocation.
2. **Config normalization**: use/align with `normalize_mcp_config` / existing adapter config handling; do not mutate caller-owned config.
3. **FR-006 reason taxonomy preserved** (additive-compatible consumption only): `mcp_unavailable`, `mcp_misconfigured`, `mcp_startup_timeout`, `mcp_call_timeout`, `mcp_invalid_response`, `mcp_missing_capability`, `mcp_tool_error`, plus compatibility reasons where surfaced (`cli_not_found`, `neither_available`, `is_error`) — meanings must remain compatible with 006.
4. **Metadata preserved where applicable/safe**: `error` (actionable), `metadata.reason`, `metadata.mode`/interface/tool context, `metadata.error_stage`, timeout/protocol/cleanup context; no secrets/PII.
5. **Session invariants (006 §9)**: stdout protocol-only, stderr diagnostic-only, bounded cleanup, no blind retries of non-idempotent tool calls. `command_list` is treated as a safe discovery/read-oriented invocation in this smoke; retries, if any, must be bounded and explicitly justified (default: no blind retries).

## 6. Assertions contract (minimal, stable)

Assertions MUST be version-tolerant and evidence-oriented:

| Area | Required minimal assertion | Forbidden brittle assertion |
|---|---|---|
| Discovery | `tools/list` (or equivalent) completes without transport/protocol failure for the opted-in target; capability/tool set indicates presence of `command_list`. | Exact tool count, full tool catalog equality, exact ordering, exact undocumented schema. |
| Invocation | `tools/call command_list` returns a non-error, parseable/normalizable structured result (or adapter-normalized success) sufficient to map to skill-facing success context. | Exact command catalog contents/count across versions, exact payload byte/string equality, AI output fields. |
| Failure paths (when exercised by slice/tests) | Actionable structured outcome/skip reason; FR-006-aligned reason when MCP path is attempted; bounded cleanup/no unsafe leakage. | Raw stack traces as the only user-facing outcome; silent success/fallback. |
| Scope claims | Evidence states stateless smoke only; no stateful artifact cycle; no AI generation claim. | Claiming prompt-based generation, provider/model routing, or cross-call session state. |

## 7. Evidence contract (FR-007, SC-004)

For an opted-in real local verification run, recorded evidence MUST make the following discoverable in under 5 minutes (runbook/quickstart or recorded run output):

| Evidence field | Description |
|---|---|
| Verified command shape | Exact/representative local command used (e.g., `photocraft-cli mcp --automation-read-root ... --automation-write-root ...`) and the MCP interactions performed (`tools/list`, `tools/call name=command_list`). |
| Required safety preconditions | Explicit opt-in, authorized server selection (override env preferred, resolved absolute path when PATH used in opt-in mode), temp/override root policy, bounded timeout, cleanup expectations. |
| Observed capability/invocation summary | Whether `command_list` capability was present (version-tolerant), invocation non-error/normalizable outcome summary, and relevant result shape notes (defensive parsing). |
| Binary/version identity context | Resolved executable path and PhotoCraft/app version or MCP/server identity when available; otherwise record “unavailable/unknown” explicitly. |
| Known limits | Stateless per-call session boundary (no session reuse, no stateful artifact cycle in this slice); local PhotoCraft MCP is engine/editor automation; AI generation/providers/models out of scope; optional local verification excluded from default CI; mock-first preserved. |
| Outcome classification | Success, skip (with reason), or structured failure (FR-006-aligned reason/`error_stage`/actionable message context) as applicable. |

## 8. Out of scope (reinforced)

- Default CI dependence on a real PhotoCraft binary/server.
- Stateful session-capable adapter API or multi-step `create -> command -> export` artifact cycle across one retained MCP session.
- Prompt-based AI generation/provider/model routing or cloud credentials.
- Public schema changes; CLI/fallback/selection/FR-006 contract changes.
- Exact tool-count/catalog assertions and brittle payload snapshots.
- Bridge mode, UI tools, progress/cancellation broad coverage, and deep spec renumbering.
