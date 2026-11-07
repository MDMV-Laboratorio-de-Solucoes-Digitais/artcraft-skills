# 009 PhotoCraft MCP stateful opt-in smoke (Option A execution, authorized)

- **Date (UTC)**: 2026-11-07T00:54:38Z (execution 2026-11-06 local request)
- **Authorization**: explicit user message (“Opção A”, maior valor se autorizado) — 2026-11-06
- **Opt-in**: manual ad-hoc, **never CI/default** (`ARTCRAFT_MCP_INTEGRATION` not required for this harness script; run was explicitly authorized and isolated)
- **Binary**: `/usr/bin/photocraft-cli` (absolute)
- **Version**: `photocraft-cli 0.20.1 (327c4cc82, 2026-11-03)`
- **Roots**: temp auto-created, absolute, harness-managed, **cleaned** after run (`read_removed=true`, `write_removed=true`); no maintainer-managed override roots
- **Timeout**: 30s bounded (adapter session timeout)
- **Adapter**: `skills.core.artcraft_app_client` **v0.4.0** — `mcp_stateful_session`/`MCPStatefulSession` (009, additive, retained MCP stdio subprocess; 006 stateless APIs preserved)
- **Command shape**: `photocraft-cli mcp --automation-read-root <abs-temp> --automation-write-root <abs-temp>`

## Scope / limits (explicit)
- **Engine/editor automation only**, capability-gated (008 defensive gating pattern). **No** prompt-based AI generation, **no** provider/model/prompt routing/claim.
- **No** bridge/UI headless scope. **No** CI/default real smoke. **No** secrets/PII recorded; no raw sensitive payload/catalog dumps.
- MCP 2026-07-28 aware: **client-retained process state** (009); no server-side session assumption.
- 007 stateless boundary remains proven separately; this run exercises **009 retained session** for cross-call steps.

## Observed evidence (sanitized)
| Step | Result | Notes |
|---|---:|---|
| `tools/list` | ok | 26 tools reported (version-tolerant discovery only; sample includes `command_list, doc_new, doc_inspect, doc_export, doc_save, command_run`, etc.) |
| `command_list` | ok | engine/editor discovery, catalog not dumped |
| `doc_new` (64×64, name `009-smoke`) | ok | context created in retained session |
| `doc_inspect` | ok | **cross-call** after `doc_new` in same retained session |
| `doc_export` (`path=<temp-write>/009-smoke.png`, `format=png`) | ok | `file_exists=true`, `file_size_bytes=593` (temp write root) |
| `doc_save` (`<temp-write>/009-smoke.pcraft`) | ok | `file_exists=true` |

**Cycle summary**: all steps ok (`command_list, doc_new, doc_inspect, doc_export, doc_save`).

## Notable parameter behavior (evidence-backed)
- `doc_export` with `overwrite=false` returned `mcp_tool_error` / `unknown argument \`overwrite\` for doc_export` in this environment (sanitized). Retrying with `path` + `format=png` (no `overwrite`) succeeded. *Capability/parameter handling remains version-tolerant; do not assume exact schema across versions.*

## Contracts preserved
006 stateless `mcp_tools_list`/`mcp_tools_call` unchanged; 009 additive only. FR-005/FR-006, public schemas, CLI/fallback preserved (repo gates: 421/23, 12/12 at verification time).

## Conclusion
**Opt-in real smoke exercised (authorized, scoped, engine/editor, capability-gated):** 009 retained MCP stdio session successfully performed discovery + cross-call document operations and produced artifacts in a harness-managed temp write root, with cleanup. Evidence is **environment/binary-specific** (`photocraft-cli 0.20.1`) and **not** a claim of AI generation, bridge/UI support, universal PhotoCraft capability parity, or CI/default execution.
