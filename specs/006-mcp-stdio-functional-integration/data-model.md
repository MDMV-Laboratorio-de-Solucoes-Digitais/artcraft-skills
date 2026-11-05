# Data Model: MCP stdio functional integration (minimum scope)

**Feature**: 006-mcp-stdio-functional-integration  
**Date**: 2026-11-05

## Scope

Conceptual/runtime entities for the minimal MCP stdio tools integration. This feature does **not** add persistent storage or change public skill schemas. Entities map to adapter/runtime structures and normalized results.

## Entities

### MCPStdioConfig (normalized input/config shape)

Configuration consumed by MCP adapter/hooks. Source: `inputs["mcp_config"]` (existing public schema field) after normalization. Unknown fields are ignored unless documented.

| Field | Type | Required | Description / Validation |
|---|---|---:|---|
| `transport` | `string` | no (normalized) | Must resolve to `stdio` for 006 execution path; existing normalization may default/ensure transport metadata. |
| `command` | `string` | yes for launch | Executable/entrypoint used to start MCP server subprocess (reference: `photocraft-cli`). Must be non-empty when MCP path is attempted. |
| `args` | `array[string]` | no | Subprocess arguments. Reference PhotoCraft headless: `["mcp","--automation-read-root",...,"--automation-write-root",...]` (documented as reference mapping). |
| `env` | `object<string,string>` | no | Optional environment overrides/additions. Sensitive values must not be logged. |
| `cwd` | `string` | no | Optional working directory for subprocess launch. |
| `timeout` / `call_timeout` | `number` (seconds) | no | Bounded operation timeout override. Must be positive when provided. |
| `startup_timeout` | `number` (seconds) | no | Optional bounded startup/handshake timeout override. |
| `tool_name` / operation mapping hint | `string/object` | no | Optional reference mapping hint for selecting the invoked MCP capability; 006 core contract remains generic `tools/list` + `tools/call`. |

**Validation rules**: treat missing/invalid launch config as unavailable/misconfigured MCP path → structured failure (`mcp_unavailable` or equivalent reason), not an exception escaping to callers. Do not mutate caller-provided config.

### MCPStdioTransportSession (runtime)

Ephemeral subprocess/session state for one MCP interaction (minimum scope may be per-request; planning may optimize later without contract change).

| Field | Type | Description |
|---|---|---|
| `process` | subprocess handle | Running MCP server process with stdin/stdout/stderr pipes. |
| `stdin/stdout` | stream | Protocol channel only (newline-delimited JSON-RPC). |
| `stderr` | stream/buffer | Diagnostic capture only; never protocol. |
| `deadline/timeouts` | runtime | Bounded startup/call deadlines. |
| `state` | enum | `starting` → `ready` → `busy` → `closing`/`closed`/`failed`. |

**State transitions**:
- `starting` → `ready`: subprocess launched and minimal MCP readiness/handshake satisfied for tools operations.
- `starting|ready|busy` → `failed`: timeout, spawn error, protocol/JSON parse error, invalid response, or unexpected termination → safe cleanup + structured failure.
- `ready` → `busy` → `ready/closed`: `tools/list`/`tools/call` completed or session closed.
- any → `closed`: stdin closed, bounded wait, terminate/kill fallback as needed; no leaked process.

### MCPCapability (discovery result)

Represents one tool/capability reported by `tools/list`.

| Field | Type | Required | Description |
|---|---|---:|---|
| `name` | `string` | yes | MCP tool identifier used in `tools/call`. |
| `description` | `string` | no | Human-readable description. |
| `inputSchema` | `object` | no | JSON-schema-like input contract (if provided). |
| `raw` | `object` | no | Original tool descriptor for diagnostics/mapping (careful with size/sensitivity). |

### MCPOperationInvocation (request)

| Field | Type | Required | Description |
|---|---|---:|---|
| `method` | `string` | yes | `tools/list` or `tools/call`. |
| `tool_name` | `string` | for `tools/call` | Capability to invoke. |
| `arguments` | `object` | for `tools/call` | Mapped inputs; 006 primary example maps `image-edit` path inputs to the selected operation. |
| `request_id` | string/int | yes | JSON-RPC correlation id. |
| `timeout` | number | no | Bounded call timeout. |

### MCPNormalizedOutcome (internal)

Adapter-level intermediate before `SkillResult`.

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | Protocol/operation success after normalization rules. |
| `data` | `object` | Normalized output fields (`image_url`, `image_path`, `asset_id`, `format`, `width`, `height`, `metadata`) where applicable. |
| `error` | `string|null` | Actionable message. |
| `metadata` | `object` | `mode`, `interface`=`mcp` (or equivalent), `tool`/capability id, `reason`, `is_error`/protocol flags, timeout/diagnostic-safe details. |

### Normalized Skill Result (`SkillResult`, existing contract)

Defined by `skills/core/base_skill.py` — **unchanged**.

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | Execution outcome. |
| `data` | `Any` | Normalized output on success. |
| `error` | `str|None` | Failure reason/message. |
| `metadata` | `dict` | Selection/transport/diagnostic metadata. |

## Relationships

- `MCPStdioConfig` → launches → `MCPStdioTransportSession`.
- `MCPStdioTransportSession` → performs → `MCPOperationInvocation` (`tools/list`, `tools/call`).
- `tools/list` → returns → `MCPCapability[]`.
- `MCPOperationInvocation`/tool result → normalized to → `MCPNormalizedOutcome` → returned as `SkillResult`.
- `CreativeSkill.execute()` / MCP hooks (`_mcp_available`, `_mcp_command_list`, `_mcp_command_run`) consume config and produce/propagate `SkillResult` without schema changes.

## Invariants

- Stdout is protocol-only for MCP stdio messages; stderr is diagnostic-only.
- Public skill schemas (`mode`, `mcp_config`, skill-specific fields) are unchanged.
- `SkillResult` shape remains backward-compatible.
- Default `auto` selection remains CLI-first when CLI is available (FR-005).
- Deterministic mock/fake subprocess tests require no real credentials/network/binaries.

