# Quickstart: MCP stateful session (009)

**Purpose**: review 007 Option B spec + verify implemented additive mock-first runtime (2026-11-06). **No real MCP execution by default.**

## 1) Review / default gates

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

## 3) Authorized opt-in real smoke (executed, scoped — 2026-11-06)

**Evidence**: `docs/research/2026-11-06-009-photocraft-stateful-opt-in-smoke.md`

- Authorization: explicit user request (Option A), 2026-11-06. **Never CI/default.**
- Binary: `/usr/bin/photocraft-cli 0.20.1` (absolute), temp absolute roots harness-managed/cleaned, timeout 30s bounded.
- Scope: engine/editor, capability-gated (008). **No** AI generation/provider/model/prompt, **no** bridge/UI, **no** secrets/PII.
- Observed (sanitized): `tools/list` ok (26 tools, version-tolerant), `command_list` ok, **cross-call** `doc_new` → `doc_inspect` → `doc_export` (png, temp write root, 593 bytes, file exists) → `doc_save` (pcraft exists) — all ok in **one retained 009 session**. Cleanup ok.
- Parameter note (evidence-backed): `doc_export` rejected `overwrite` arg in this env; `format=png` succeeded. Keep parameter handling version-tolerant.

## 4) Future real validation (additional cases)

Only with explicit authorization + opt-in + 007 controls (absolute binário/roots, bounded timeout, temp cleanup, no secrets/PII, no CI/default). Capability-gate via `tools/list`/`command_list`; treat tool params/catalog as version-tolerant. Add deterministic engine commands (`command_run`) only when gated and safe.

## 5) Limits

- No AI generation claim. No bridge/UI. No server-side session assumption on MCP 2026-07-28 path (client-retained process state). No CI/default real smoke. Real evidence is **environment-specific** (`photocraft-cli 0.20.1`), not universal parity.
