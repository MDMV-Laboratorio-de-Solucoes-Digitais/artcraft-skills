# 009 PhotoCraft MCP stateful opt-in smoke — `command_run` broaden #2 (Option A, authorized)

- **Date (UTC)**: 2026-11-07T01:53:45Z
- **Authorization**: explicit user “A+B+c” (A broaden, authorized) — 2026-11-06
- **Opt-in**: manual ad-hoc, **never CI/default**
- **Binary**: `/usr/bin/photocraft-cli 0.20.1 (327c4cc82, 2026-11-03)` (absolute)
- **Roots**: temp auto-created, absolute, harness-managed, **cleaned** (`read_removed=true`, `write_removed=true`)
- **Timeout**: 30s bounded
- **Adapter**: `skills.core.artcraft_app_client` **v0.4.0** `mcp_stateful_session` (009, retained; 006 preserved)
- **Scope**: **engine/editor only**, capability-gated. **No** AI generation/provider/model/prompt, **no** bridge/UI, **no** CI, **no** secrets/PII.

## Observed steps (one retained 009 session)
| Step | id/args (sanitized) | Result |
|---|---|---:|
| `doc_new` | 64×64 `009-A2` | ok |
| `command_run` | `layer.new.layer` `{}` | ok |
| `command_run` | `layer.new.group` `{}` | ok |
| `command_run` | `view.zoom.fitOnScreen` `{}` | **tool error** — `mcp_tool_error` / “unknown command `view.zoom.fitOnScreen`” (catalog/id/version mismatch; honest) |
| `command_run` | `image.flatten` `{}` | **tool error** — `mcp_tool_error` / “unknown command `image.flatten`” (catalog/id/version mismatch; honest) |
| `command_run` | `select.all` `{}` | ok |
| `command_run` | `select.deselect` `{}` | ok (precondition satisfied by prior `select.all` in same retained session) |
| `doc_inspect` | — | ok (cross-call) |
| `doc_export` | temp write root, `format=png` | ok (`file_exists=true`, `593` bytes) |

**Summary**: retained-session cross-call cycle exercised additional deterministic engine commands: layer creation, selection precondition (`select.all`→`select.deselect`), inspect, export. Two guessed ids (`view.zoom.fitOnScreen`, `image.flatten`) failed with structured `mcp_tool_error` (“unknown command”) — **honest FR-006-aligned**; reinforces 008/009 guidance: **do not assume command ids/enabled state; capability-gate via `command_list` and treat catalog as version-tolerant**. No AI/bridge/UI claim.
