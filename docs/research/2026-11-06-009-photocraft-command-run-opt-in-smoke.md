# 009 PhotoCraft MCP stateful opt-in smoke — `command_run` broaden (Option A, authorized)

- **Date (UTC)**: 2026-11-07T01:44:21Z
- **Authorization**: explicit user request “A” (broaden Option A / `command_run`) — 2026-11-06
- **Opt-in**: manual ad-hoc, **never CI/default**
- **Binary**: `/usr/bin/photocraft-cli 0.20.1 (327c4cc82, 2026-11-03)` (absolute)
- **Roots**: temp auto-created, absolute, harness-managed, **cleaned** (`read_removed=true`, `write_removed=true`)
- **Timeout**: 30s bounded
- **Adapter**: `skills.core.artcraft_app_client` **v0.4.0** `mcp_stateful_session` (009, retained subprocess; 006 stateless preserved)
- **Scope**: **engine/editor only**, capability-gated (008). **No** AI generation/provider/model/prompt. **No** bridge/UI. **No** CI/default. **No** secrets/PII.

## Discovery (sanitized, version-tolerant)
`command_run` present (`inputSchema`: `id`, `params`, `wait`; headless engine command execution; long commands may return job when `wait` false — not exercised). `command_list` returned 954 commands (JSON list in content text); sample includes `layer.new.layer`, `layer.new.group`, `select.deselect`, `file.new` etc. Enabled/needsDocument flags vary; execution used retained-session document context (`doc_new` first).

## Observed steps (one retained 009 session)
| Step | id/args (sanitized) | Result |
|---|---|---:|
| `doc_new` | 64×64 `009-cmdrun-A` | ok |
| `command_run` | `layer.new.layer` `{}` | ok |
| `command_run` | `layer.new.group` `{}` | ok |
| `command_run` | `select.deselect` `{}` | **tool error** (precondition) — sanitized: `mcp_tool_error` / “command `select.deselect` is not available right now: no selection” |
| `doc_inspect` | — | ok (cross-call) |
| `doc_export` | temp write root, `format=png` | ok (`file_exists=true`, `593` bytes) |

**Summary**: engine/editor cross-call cycle with deterministic `command_run` operations **partially exercised**: `doc_new` + 2 successful `command_run` mutations + `doc_inspect` + `doc_export` ok; `select.deselect` correctly returned a structured tool error due to missing selection precondition (honest, FR-006-aligned). **Not** a claim of universal command success or AI generation.

## Conclusion
Authorized opt-in evidence shows 009 retained session can **capability-gate and execute deterministic engine/editor `command_run` commands** (`layer.new.layer`, `layer.new.group`) in the same cross-call document context and export a real PNG artifact to a cleaned temp write root. `select.deselect` failure is precondition-specific and was reported as a structured `mcp_tool_error`; future runs should gate/prepare selection state before selection-dependent commands.
