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

**Evidence**: `docs/research/2026-11-06-009-photocraft-stateful-opt-in-smoke.md`, `docs/research/2026-11-06-009-photocraft-command-run-opt-in-smoke.md`

- Authorization: explicit user requests (Option A), 2026-11-06. **Never CI/default.**
- Binary: `/usr/bin/photocraft-cli 0.20.1` (absolute), temp absolute roots harness-managed/cleaned, timeout 30s bounded.
- Scope: engine/editor, capability-gated (008). **No** AI generation/provider/model/prompt, **no** bridge/UI, **no** secrets/PII.
- Run 1 (sanitized): `tools/list` + `command_list` + `doc_new` → `doc_inspect` (cross-call) → `doc_export` png (593B, temp write root) → `doc_save` — all ok in **one retained 009 session**.
- Run 2 broaden `command_run` (sanitized): `doc_new` → `command_run layer.new.layer` ok → `command_run layer.new.group` ok → `command_run select.deselect` **structured `mcp_tool_error`** (precondition: no selection, honest) → `doc_inspect` ok → `doc_export` png ok (593B). Demonstrates deterministic engine command execution in retained session; selection-dependent command correctly failed with FR-006-aligned error.
- Parameter notes (version-tolerant): `doc_export` rejected `overwrite` in this env; `format=png` ok. Do not assume exact command catalog/params/enabled state across versions.


## 4) Future real validation (additional cases)

Only with explicit authorization + opt-in + 007 controls (absolute binário/roots, bounded timeout, temp cleanup, no secrets/PII, no CI/default). Capability-gate via `tools/list`/`command_list`; treat tool params/catalog as version-tolerant. Add deterministic engine commands (`command_run`) only when gated and safe.

## 5) Limits

- No AI generation claim. No bridge/UI. No server-side session assumption on MCP 2026-07-28 path (client-retained process state). No CI/default real smoke. Real evidence is **environment-specific** (`photocraft-cli 0.20.1`), not universal parity.

## 6) 009/B param normalization (additive, opt-in)
- `skills.core.artcraft_app_client.normalize_mcp_tool_arguments(tool_name, arguments)` — pure, returns copy, **no mutation**. Default `mcp_tools_call`/`call_tool` unchanged unless callers opt in.
- Observed (PhotoCraft 0.20.1 opt-in): `doc_export` rejected `overwrite`; normalizer drops `overwrite` for `doc_export` compatibility while preserving other args. Keep usage **capability-gated** and version-tolerant (008).
