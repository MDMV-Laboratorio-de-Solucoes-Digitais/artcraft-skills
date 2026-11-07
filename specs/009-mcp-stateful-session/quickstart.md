# Quickstart: MCP stateful session (009)

**Purpose**: review 007 Option B spec + verify implemented additive mock-first runtime (2026-11-06). **No real MCP execution by default.**

## 1) Review (default)

```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q
python scripts/validate_all_skills.py
```

Read: `specs/009-mcp-stateful-session/spec.md`, `contracts/stateful-session-contract.md`, `checklists/requirements.md`, assessment `decision.md`.

## 2) Implemented (2026-11-06, additive, mock-first)

- `skills.core.artcraft_app_client.mcp_stateful_session` / `MCPStatefulSession` (v0.4.0): retained MCP stdio subprocess, correlated JSON-RPC ids, `list_tools()`/`call_tool()`, bounded/idempotent cleanup, FR-006-aligned errors. Preserves 006 stateless `mcp_tools_list`/`mcp_tools_call`, FR-005/FR-006, schemas.
- Deterministic tests: `tests/unit/test_mcp_stateful_session_009.py` (9) + extended `tests/_helpers/fake_mcp_stdio_server.py` scenarios (006 scenarios intact).

```bash
PYTHONPATH=. python -m pytest -q tests/unit/test_mcp_stateful_session_009.py
```

## 3) Future real validation (NOT default)

Only with explicit authorization + opt-in + 007 controls (absolute binário/roots, bounded timeout, temp cleanup, no secrets/PII, no CI/default). Evidence must state engine/editor only, no AI, session retained scope, capability gating (008). Cycle target (capability-gated): `tools/list` → `doc_new` → deterministic engine command → inspect/export to temp write-root.

## 4) Limits

- No AI generation claim. No bridge/UI. No server-side session assumption on MCP 2026-07-28 path (client-retained process state). No CI/default real smoke. Real PhotoCraft artifact cycle **not exercised** unless explicitly authorized/opt-in.