# Contract: MCP stdio adapter (006 minimum scope)

**Feature**: 006-mcp-stdio-functional-integration  
**Status**: Design contract (Phase 1)  
**Primary implementation surfaces** (planned): `skills/core/artcraft_app_client.py` (transport/helpers/reason mapping as needed), `skills/core/creative_skill.py` (MCP hooks + selection/execute behavior), tests under `tests/unit|contract|property|integration` (deterministic mock-first).

## 1. Scope

Define the minimal internal/behavioral contract for functional MCP stdio integration:

- Generic MCP tools contract over stdio: **`tools/list`** discovery + **one `tools/call`** invocation.
- Deterministic mock/fake stdio subprocess acceptance for CI/default tests.
- PhotoCraft headless MCP as **reference target** for documentation/optional validation only.
- No public schema breaks; preserve `SkillResult` and existing CLI/fallback behavior.

## 2. Public Compatibility (must preserve)

| Surface | Contract |
|---|---|
| `skills.core.base_skill.SkillResult` | Fields `success`, `data`, `error`, `metadata` unchanged in meaning/compatibility. |
| Creative skill inputs | Existing fields remain valid: `mode` (`cli|mcp|auto`), `cli_path`, `mcp_config`, `command_keywords`, `generation_command`, `timeout`, skill-specific inputs. No new required fields. |
| `CreativeSkill.execute()` | Explicit `mode` honored. `mode=cli`/CLI-unavailable behavior preserved. Default `auto` remains back-compatible (CLI available → MCP available/configured → fallback/degradation per existing rules). |
| Reason codes | Existing `artcraft_app_client` reasons (`cli_not_found`, `mcp_unavailable`, `neither_available`, `is_error`) remain valid; 006 may add compatible, documented reasons/metadata without breaking existing consumers. |

## 3. MCP Hooks Contract (`CreativeSkill`)

Current stubs become functional (or delegate to adapter helpers) with compatible signatures:

```python
def _mcp_available(self, cfg: Dict[str, Any]) -> bool: ...
def _mcp_command_list(self, cfg: Dict[str, Any]) -> list|Any: ...  # discovery result
def _mcp_command_run(self, cfg: Dict[str, Any], tool_id: str, params: Dict[str, Any], timeout: int) -> dict|Any: ...
```

Behavioral requirements:
- `_mcp_available` returns `True` only when normalized config is sufficient for stdio launch and minimal preflight passes; otherwise `False`.
- `_mcp_command_list` performs/represents `tools/list` discovery (or equivalent capability listing) and returns structured data; on failure returns a structured error shape that `_execute_mcp` can normalize (never raises uncaught transport exceptions across the skill boundary).
- `_mcp_command_run` performs `tools/call` for `tool_id` with `params`; returns tool result payload or structured error (`is_error`/error info).
- `_execute_mcp` maps hook outcomes to `SkillResult` with `metadata.mode`, `metadata.interface="mcp"` (or equivalent), and actionable error/reason metadata on failure.

## 4. Stdio Transport Contract

Implementation MUST follow MCP stdio framing rules:
- Launch MCP server as subprocess using configured `command`/`args`/`env`/`cwd`.
- Write only valid JSON-RPC MCP messages to server stdin.
- Read only JSON-RPC MCP messages from server stdout (newline-delimited; no embedded newlines).
- Capture stderr for diagnostics; do not treat stderr as protocol content or as sole error signal.
- Enforce bounded startup/call timeouts.
- On failure/timeout/caller abort path, perform safe cleanup: close stdin, wait bounded, terminate/kill fallback if needed; no leaked process.

## 5. MCP Tools Contract (minimum)

- **Discovery**: issue `tools/list` and obtain available tools/capabilities (handle empty/missing expected capability as structured failure).
- **Invocation**: issue `tools/call` with selected `name` and mapped `arguments` for one supported operation.
- **Normalization**:
  - Success tool result → `SkillResult(success=True, data=<normalized output>, metadata={mode, interface, tool,...})`.
  - Tool-level error (`isError`/error payload) → structured failure with actionable message and reason metadata.
  - Protocol/transport errors (spawn, timeout, invalid JSON/shape, missing capability) → structured failure; explicit `mode=mcp` does not silently reroute to CLI.

## 6. Selection/Degradation Contract (FR-005)

| Input `mode` | Behavior |
|---|---|
| `cli` | Existing CLI behavior: discover/execute CLI; missing CLI → existing `cli_not_found` failure shape. |
| `mcp` | Attempt MCP path; return normalized MCP success/failure. No silent CLI fallback. |
| `auto` (default) | **Back-compatible default**: CLI available → execute CLI; else MCP available/configured → execute MCP; else structured no-interface/fallback/degradation per existing rules. No MCP-preferred default in 006. |

## 7. Reference Mapping (non-normative target note)

PhotoCraft headless MCP (`photocraft-cli mcp --automation-read-root ... --automation-write-root ...`) may expose engine-oriented tools such as `command_list`/`command_run`. 006 may document a reference mapping from the primary `image-edit` example to PhotoCraft tool invocation, but the core adapter contract remains generic MCP tools. Bridge mode/root semantics differ; optional real validation must follow target docs.

## 8. Error/Metadata Contract (minimum)

Failures should include, where available and safe:
- `error`: human-actionable message
- `metadata.mode`
- `metadata.reason` (compatible reason code)
- `metadata.interface`/tool id when MCP path was attempted
- timeout/protocol context without leaking secrets/PII

## 9. Test Contract

Default CI/local tests are deterministic and require no real credentials/network/mandatory binaries. Minimum coverage:
- `tools/list` + `tools/call` success → normalized `SkillResult` for `image-edit` primary example path.
- missing capability, tool error/`isError`, invalid JSON/protocol response, unavailable/misconfigured entrypoint, timeout/startup failure.
- back-compat: existing tests remain green; `mcp_config` non-mutation; explicit mode behavior; default `auto` CLI-first preserved.

Optional real PhotoCraft integration is `@pytest.mark.integration` (or equivalent), opt-in and skipped by default.
