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
| Creative skill inputs | Existing fields remain valid: `mode` (`cli|mcp|auto`), `cli_path`, `mcp_config`, `command_keywords`, `generation_command`, `timeout`, skill-specific inputs. No new required fields. Existing enum values/default semantics remain valid; metadata additions are additive and optional for existing consumers (spec FR-003). |
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
  - Tool-level error (`isError`/error payload) → structured failure with actionable message and FR-006 minimum reason metadata.
  - Protocol/transport errors (spawn/launch, timeout, invalid JSON/shape/framing, EOF/exit-mid-transmission, missing capability, unusable/mapping failure) → structured failure; **explicit `mode=mcp` does not silently reroute to CLI/fallback** (spec FR-005 Q4:A).

## 6. Selection/Degradation Contract (FR-005)

| Input `mode` | Behavior |
|---|---|
| `cli` | Existing CLI behavior: discover/execute CLI; missing CLI → existing `cli_not_found` failure shape. |
| `mcp` | Attempt MCP path; return normalized MCP success/failure. **No silent CLI/fallback reroute** on MCP failure (FR-005). |
| `auto` (default) | **Back-compatible default**: CLI available → execute CLI; else MCP available/configured → execute MCP; else structured no-interface/fallback/degradation per existing rules bounded by this contract §2/§6 and current `CreativeSkill`/adapter behavior (FR-005 Q7:A). No MCP-preferred default in 006. After failure, no unsafe state; subsequent attempts re-evaluate selection from current state. |

## 7. Reference Mapping (non-normative target note)

PhotoCraft headless MCP (`photocraft-cli mcp --automation-read-root ... --automation-write-root ...`) may expose engine-oriented tools such as `command_list`/`command_run`. 006 may document a reference mapping from the primary `image-edit` example to PhotoCraft tool invocation, but the core adapter contract remains generic MCP tools. Bridge mode/root semantics differ; optional real validation must follow target docs.

## 8. Error/Metadata Contract (minimum, additive; FR-006 Q5:A)

Failures MUST include, where available and safe (no secrets/PII):
- `error`: human-actionable message with remediation hint (safe)
- `metadata.mode`: requested/effective mode context
- `metadata.reason`: stable, documented, compatibly-extensible reason code (006 minimum set: `mcp_unavailable`, `mcp_misconfigured`, `mcp_startup_timeout`, `mcp_call_timeout`, `mcp_invalid_response`, `mcp_missing_capability`, `mcp_tool_error`, `cli_not_found`, `neither_available`)
- `metadata.interface`/`metadata.tool`: MCP path/tool id when attempted
- `metadata.error_stage` (or equivalent): `launch`/`initialize`/`discovery`/`invocation`/`normalization`/`cleanup` when available
- timeout/protocol/cleanup context: bounded, non-sensitive
- optional additive correlation/observability when available and safe (Q9:A, not required): `metadata.request_id`/JSON-RPC `id`, `metadata.operation_id`/session token, bounded trace context; explicit requested mode remains observable

## 9. Subprocess Session Invariants (FR-007 Q6:A)

- Stdout is protocol-only (newline-delimited JSON-RPC MCP). Stderr is diagnostic-only.
- Correlate JSON-RPC responses by `id`; unmatched/duplicate/late/unsolicited protocol messages MUST NOT corrupt normalized results and MUST produce structured protocol failure or be safely handled per documented rule.
- On timeout, invalid framing/JSON, EOF/exit-mid-transmission, partial unusable response, or caller abort: close stdin, bounded wait, terminate/kill fallback as needed; leave no running subprocess for the session.
- Session is invalid after partial startup failure or transport/protocol failure; cleanup before retry. No blind retries of non-idempotent tool calls.

## 10. Test/Verification Contract (Q8:A)

Default CI/local tests are deterministic and require no real credentials/network/mandatory binaries. Minimum coverage:
- `tools/list` + `tools/call` success → normalized `SkillResult` for `image-edit` primary example path.
- missing capability, tool error/`isError`, invalid JSON/protocol/framing/unusable response, unavailable/misconfigured/launch failure, timeout/hang/startup failure.
- back-compat: existing tests remain green; `mcp_config` non-mutation; explicit mode behavior (`cli`, `mcp` no silent reroute, `auto` CLI-first preserved including MCP configured but not selected); selection/failure metadata includes FR-006 minimum fields where applicable.
- mock stdio server behavior: newline-delimited JSON-RPC on stdout, diagnostics on stderr only, deterministic responses for the 006 scenario classes above. **Repeatability/classification stability (Q10/A)**: same scenario conditions → stable expected FR-006 `reason`/`error_stage`; no fixed rerun count mandated unless flake observed.

Parity (operations supported by both paths): equivalent `SkillResult` success/failure semantics and normalized output fields; transport-specific metadata may differ and must remain additive/non-breaking. Regression set includes existing `SkillResult`/schema/`CreativeSkill` selection tests and repository baseline gates (SC-003). **Conformance baseline (Q12/A)**: pre-006 green `SkillResult`/public schema + existing `CreativeSkill`/adapter CLI/selection behavior on integration branch (record commit/SHA or test summary in PR). **Traceability (Q11:A)**: acceptance evidence maps each covered scenario class to FR/SC IDs (lightweight). Minimum supported/default verification environment: Linux + Python/pytest with test/packaged entrypoint or mock subprocess (SC-004).

Optional real PhotoCraft integration is `@pytest.mark.integration` (or equivalent), opt-in and skipped by default.

## 11. 006 Implementation Limits / Reference Mapping Notes (T030)

- **Generic contract**: 006 implements minimal generic MCP stdio tools contract (`initialize` handshake best-effort, `tools/list`, one `tools/call`) in `skills/core/artcraft_app_client.py` (`mcp_tools_list`, `mcp_tools_call`) and `skills/core/creative_skill.py` hooks. PhotoCraft tool names are **not** hard-coded.
- **Primary e2e example**: `skills/creative/image-edit/skill.py` via shared `CreativeSkill` path (T022: no public schema change required).
- **Selection policy implemented**: explicit `cli`/`mcp` win; `mode=mcp` returns structured MCP failure with no silent CLI/fallback reroute; default `auto` remains CLI-first when CLI is available, then MCP when CLI unavailable and MCP is configured/available, else `neither_available` degradation.
- **FR-006 metadata**: additive structured failures include actionable `error`, `metadata.mode`, stable `metadata.reason` (006 taxonomy + compatibility reasons), `metadata.interface`/`metadata.tool` when attempted, `metadata.error_stage` where available; no secrets/PII intended.
- **Out of scope (006)**: full MCP SDK adoption, async transport, broad multi-tool orchestration, blanket support for every MCP target/environment, mandatory real binaries/credentials/network in default CI, `skills/creative/image-generate/skill.py` (BaseSkill outlier) behavior changes beyond back-compat verification evidence (T036).
- **Optional real PhotoCraft validation**: non-default `@pytest.mark.integration`; requires explicit env/prereqs (`ARTCRAFT_MCP_INTEGRATION=1`, `photocraft-cli`, safe roots). Root paths must be user-controlled/safe; do not run against sensitive directories.
