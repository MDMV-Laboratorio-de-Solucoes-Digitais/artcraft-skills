# Data Model: MCP stateful session (009)

**Date**: 2026-11-06 | **Scope**: conceptual (docs-only)

## Entities

### MCPStatefulSession

| Field | Type | Description |
|---|---|---|
| `config` | MCPStdioConfig-like | command/args/env/cwd, normalized; no mutation of caller input |
| `roots` | SafeAccessBoundary | absolute read/write roots; temp default for real harness |
| `process` | subprocess handle (future) | retained stdio MCP server process |
| `request_id` | int/monotonic | JSON-RPC correlation per call |
| `timeouts` | object | startup/call/total bounded |
| `state` | enum | `new|starting|ready|busy|closing|closed|failed` |
| `evidence` | EvidenceRecord (optional) | opt-in real runs only |

### SessionStepResult

| Field | Type | Description |
|---|---|---|
| `ok` | bool | normalized success |
| `tool_name` | string | invoked tool |
| `data` | any | normalized/sanitized payload summary |
| `error` | object? | FR-006-aligned reason/stage/message (actionable) |
| `meta` | object | timing, step index; no secrets/PII |

### Validation Rules

- `start` requires valid config and (for real) explicit opt-in + authorized binary + absolute safe roots.
- Each `call` only in `ready` state; transitions to `busy`→`ready` or `failed/closing`.
- `close`/cleanup MUST run on all exit paths; bounded kill/terminate escalation.
- No exact tool catalog assumptions; capability gating required before cycle.

## State Transitions

`new` → `starting` → `ready` ↔ `busy` → `closing` → `closed`; any step → `failed` → `closing` → `closed`.