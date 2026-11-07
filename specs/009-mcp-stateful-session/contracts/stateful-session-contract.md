# Contract: MCP Stateful Session (009, additive)

**Status**: Implemented additive runtime (2026-11-06, authorized TDD/mock-first slice). Preserves 006 stateless APIs.

## Intent

Additive session helper retaining one MCP stdio subprocess for multiple correlated calls (007 Option B). **Must not** replace or change behavior of 006 `mcp_tools_list`/`mcp_tools_call`.

## Conceptual API (future)

```python
from skills.core.artcraft_app_client import mcp_stateful_session, MCPStatefulSession

# 009 additive, retained stdio session (same subprocess for multiple calls)
with mcp_stateful_session(config, timeout=30) as session:
    tools = session.list_tools()                 # or tools/list normalized
    res = session.call_tool("tool.name", {"k": "v"})  # tools/call, same retained process
    session.close()  # idempotent; __exit__ closes bounded
```

`kwargs` (e.g. future `roots`/`opt_in_real` hints) accepted for forward/back compat; enforcement of 007 real-run safety controls remains harness/caller responsibility unless a future slice adds it in-contract.

## Lifecycle Rules

1. **Open/start**: validate config; resolve authorized binary (007 policy) for real; create/validate absolute roots; spawn subprocess with bounded startup timeout.
2. **Initialize**: perform required MCP handshake/initialize for supported path; treat protocol evolution (2026-07-28) defensively.
3. **Operate**: sequential calls with monotonic JSON-RPC ids; defensive parsing; normalize errors to FR-006-aligned metadata.
4. **Close**: bounded shutdown, terminate/kill escalation if needed, close pipes, cleanup harness-managed temp roots; never leak process.

## Safety & Exclusions

- Opt-in real only; never CI/default. Explicit authorization for evidence runs.
- Absolute safe roots; temp auto-cleaned by harness; explicit overrides maintainer-managed.
- **No** prompt-based AI generation/provider/model claim.
- **No** bridge/UI headless scope.
- **No** silent reroute to CLI/fallback when explicit MCP path fails.

## Deterministic Cycle (reference, capability-gated)

`tools/list` (+ `command_list` if present) → `doc_new` (if present) → deterministic engine command via `command_run`/gated equivalent → `doc_inspect`/`doc_export` to temp write-root (if present/safe). Any missing capability/unsupported state → structured skip/failure with evidence.

## Compatibility

Preserve `SkillResult`, skill schemas, FR-005, FR-006. MCP 2026-07-28: client-retained process state; do not assume server-side session ID. SDK v2 migration separate.