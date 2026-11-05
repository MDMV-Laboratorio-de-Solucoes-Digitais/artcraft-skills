# Research: MCP stdio functional integration (minimum scope)

**Feature**: 006-mcp-stdio-functional-integration  
**Date**: 2026-11-05  
**Status**: Complete (Phase 0) — resolves planning unknowns carried forward from `/speckit.clarify`

## Summary

006 adds a minimal, standards-compliant MCP stdio tools integration to the existing ArtCraft skills adapter layer. The implementation target is a **generic MCP `tools/list` + `tools/call` contract** with deterministic mock/fake stdio subprocess acceptance; **PhotoCraft headless MCP** is the reference target for documentation/optional validation. Public schemas and `SkillResult` remain unchanged; default `auto` selection remains back-compatible (CLI available → MCP available/configured → fallback/degradation). End-to-end acceptance is proven through the shared `CreativeSkill` path with `image-edit` as the primary example.

## Decisions

### D1 — Transport/client implementation: minimal sync JSON-RPC stdio client in-repo (no mandatory `mcp` SDK dependency for 006)

**Decision**: Implement a **minimal synchronous JSON-RPC-over-stdio client** in the core adapter layer (or a small internal helper module) sufficient for 006: launch subprocess, enforce newline-delimited JSON-RPC framing, initialize/capability handshake as required by negotiated MCP behavior, perform `tools/list` and one `tools/call`, capture stderr separately, enforce bounded timeouts, and terminate/clean up the subprocess safely. Do **not** require the official Python MCP SDK (`mcp`) as a new mandatory dependency in 006.

**Rationale**:
- The repo has **no root dependency manifest** and skill execution is synchronous (`BaseSkill.execute`, `CreativeSkill.execute`, CLI path uses `subprocess.run`). Python MCP SDK v2 provides `stdio_client`/`Client` patterns that are **async/anyio-oriented** (docs: https://py.sdk.modelcontextprotocol.io/v2/api/mcp/client/stdio/, https://py.sdk.modelcontextprotocol.io/v2/get-started/testing/ — accessed 2026-11-05). Introducing it now would add dependency/async-bridging complexity and risk for a one-target/one-operation slice.
- 006 needs only a narrow surface: stdio framing + `tools/list` + `tools/call` + error normalization. A minimal client keeps scope small, testable, and dependency-free, consistent with current adapter patterns (`artcraft_app_client.py`, `CreativeSkill._execute_cli`).
- SDK remains a valid future alternative if/when MCP scope expands (resources/prompts/HTTP/tasks/cancellation patterns, multi-target support). This decision is reversible behind the adapter contract.

**Alternatives considered**:
- **Adopt Python MCP SDK `mcp` v2**: strongest protocol coverage and in-memory testing model, but async integration cost and new dependency outweigh 006 value. Rejected for minimum scope.
- **Wrap SDK via background event loop/thread**: possible but increases lifecycle/shutdown/cancellation complexity and test flakiness risk. Rejected.

**Authoritative evidence**:
- MCP stdio transport (2025-11-25): subprocess; stdin/stdout JSON-RPC; newline-delimited; no embedded newlines; stdout protocol-only; stderr for logs and not an error signal by itself. https://modelcontextprotocol.io/specification/2025-11-25/basic/transports
- MCP stdio transport (2026-07-28): confirms framing/lifecycle; cancellation via `notifications/cancelled` for in-flight requests; shutdown via closing input/wait/terminate; restart guidance. https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio
- MCP Tools (2025-11-25): servers declare `tools`; `tools/list` (pagination), `tools/call` (`name`, `arguments`) returns `content` and `isError`. https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- Python MCP SDK stdio/testing docs (accessed 2026-11-05): async transport/client; in-memory `Client(mcp)` useful for SDK-based tests. https://py.sdk.modelcontextprotocol.io/v2/api/mcp/client/stdio/, https://py.sdk.modelcontextprotocol.io/v2/get-started/testing/

### D2 — MCP configuration contract (`mcp_config`) and PhotoCraft reference mapping

**Decision**: Keep public skill schemas unchanged (`mcp_config` remains an object). Define a **minimal documented config shape** consumed by the adapter hooks (no schema migration required in 006): entrypoint launch fields for stdio subprocess (`command`, optional `args`, optional `env`, optional `cwd`), optional bounded `timeout`/`startup_timeout`/`call_timeout` overrides, optional `tool_name`/operation mapping hints for the reference path, and optional `stderr_capture`/diagnostic behavior flags with safe defaults. Unknown fields are ignored by the minimal client unless explicitly documented.

**PhotoCraft reference mapping** (documentation/optional validation only): headless entrypoint `photocraft-cli mcp` with required `--automation-read-root` and `--automation-write-root` (absolute paths recommended). PhotoCraft exposes engine-oriented MCP tools including `command_list` and `command_run` (`id`, `params`, `wait`); root flags differ in `--bridge` mode (roots configured on desktop app). Reference docs must state these constraints and must not imply blanket PhotoCraft-default behavior in CI.

**Rationale**:
- `CreativeSkill`/creative schemas already accept `mcp_config` (`skills/creative/*/skill.py`, `skill.md`). A contract-level config shape enables real stdio launch without adding new required public inputs.
- PhotoCraft’s actual tool surface is target-specific (`command_list`/`command_run`) while 006’s core contract is generic `tools/list`/`tools/call`. Mapping belongs in reference documentation and optional adapter mapping hooks, not in universal protocol assumptions.

**Evidence**:
- PhotoCraft MCP docs (raw, accessed 2026-11-05): headless/bridge modes, roots, tool inventory (`command_list`, `command_run`, `command_batch`, `doc_*`, resources), strict unknown-arg `-32602` behavior, stdout protocol discipline, writes/overwrite constraints. https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md
- Repo: `artcraft_app_client.normalize_mcp_config` currently normalizes/ensures `transport` key; `CreativeSkill._mcp_available/_mcp_command_list/_mcp_command_run` are stubs to be implemented behind existing hooks.

### D3 — Availability, selection policy, and failthrough

**Decision**:
- **Explicit mode wins** (unchanged).
- **`mode=mcp`**: attempt MCP path; on MCP unavailable/misconfigured/startup/timeout/invalid-response/missing-capability/operation failure, return structured `SkillResult` failure with reason/metadata. Do **not** silently switch to CLI in explicit MCP mode.
- **`mode=cli`**: unchanged behavior.
- **`auto` default (back-compatible)**: CLI if available → MCP if available/configured → fallback/degradation per documented existing rules. 006 does **not** change `select_mode`’s CLI-first preference for the default case.
- **MCP available/configured (006 definition)**: MCP path is considered available only when `mcp_config` provides sufficient launch/connection information for the stdio transport (at minimum a resolvable `command`/entrypoint in the normalized config, or an equivalent explicit adapter-supported form) and adapter preflight checks pass. Absence of config or invalid config yields `mcp_unavailable`/structured failure, never a crash.
- **Failthrough on selected-path runtime failure**: in `auto`, if CLI is selected by current policy it executes CLI as today (no new CLI→MCP failthrough added in 006). If MCP is selected (i.e., CLI unavailable and MCP available/configured), MCP executes and returns its structured result; fallback/degradation follows existing/explicit documented behavior only where already defined. 006 avoids changing runtime fallthrough semantics except what is necessary to make MCP functional and diagnosable.

**Rationale**: Minimizes regression risk (373 tests, existing CLI behavior) while making MCP reachable when explicitly requested or when CLI is absent/unavailable. Explicit MCP failure is more diagnosable than implicit rerouting.

**Alternatives considered**:
- **MCP-preferred auto**: rejected for 006 default (regression risk).
- **CLI failure → MCP failthrough in auto**: potentially useful but behavior-changing; defer unless characterized and explicitly specified.

### D4 — Timeouts, stderr, cancellation, retries, and reason codes

**Decision**:
- **Timeouts**: bounded defaults; allow config overrides (`startup_timeout`, `call_timeout`/`timeout`) without schema breaks. On timeout, return structured failure with timeout metadata and no leaked subprocess/zombie state.
- **stderr**: capture/retain stderr for diagnostics/metadata/logging (subject to PII/secret redaction rules) but **never** treat stderr as protocol content; stdout remains the sole protocol channel (MCP spec).
- **Cancellation**: full MCP cancellation semantics are best-effort/minimal in 006. If the client-side operation times out or the caller aborts the local flow, terminate the subprocess safely (close stdin, wait bounded, kill if needed). Sending `notifications/cancelled` is optional/planning-level enhancement unless trivial in the minimal client; subprocess cleanup is mandatory.
- **Retries**: reuse existing resilience posture where appropriate; do **not** blindly retry non-idempotent MCP tool calls in 006. Discovery/list may be retried only if clearly safe and bounded (planning detail); tool invocation retries default off unless idempotency is explicit.
- **Reason codes/metadata**: extend adapter/core error mapping as needed for 006 minimum cases (`mcp_unavailable`, missing capability, timeout, invalid response/protocol, tool error, `neither_available`) using existing `SkillResult.metadata`/`standardize_error` patterns; avoid breaking existing reason consumers.

**Evidence**:
- MCP stdio stdout/stderr and framing rules (2025-11-25/2026-07-28).
- MCP cancellation (2025-11-25/2026-07-28): cancellation is notification-based for in-flight requests; stdio has no per-request stream close. https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation, https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation

### D5 — Testing strategy and real integration

**Decision**:
- **Default CI/local acceptance**: deterministic **fake stdio MCP subprocess/server** tests (mock process emitting newline-delimited JSON-RPC responses) covering `tools/list`, `tools/call` success, missing capability, tool `isError`/operation failure, invalid JSON/protocol response, timeout/startup failure, and `mcp_config` non-mutation/back-compat cases.
- **Primary e2e example**: shared `CreativeSkill` path, **`image-edit`** as primary skill example mapping to one invoked operation after discovery.
- **Optional real integration**: mark as `@pytest.mark.integration` (or equivalent repo convention if introduced) and skip by default unless explicitly enabled and PhotoCraft binary/roots are available. Never required for standard CI.
- **Outlier**: `skills/creative/image-generate/skill.py` extends `BaseSkill` and duplicates MCP flow; 006 plans/contracts target shared `CreativeSkill`/adapter behavior. Aligning `image-generate` is a **follow-up** unless planning identifies a zero-risk minimal reuse.

**Rationale**: Satisfies SC-001..SC-004 deterministically; avoids environment coupling.

### D6 — Formal owner/acceptance

**Decision**: No formal owner is encoded in repo artifacts today. **Planning/implementation acceptance owner** remains ArtCraft Skills maintainers (constitution/project governance) unless the user names a specific stakeholder; track as an operational note, not a schema/code dependency.

## Consolidated Planning Notes (formerly open questions)

| Item | Resolution for planning |
|---|---|
| SDK `mcp` vs minimal client | Minimal sync JSON-RPC stdio client in-repo for 006 (D1) |
| Exact `mcp_config` fields / PhotoCraft roots mapping | Minimal launch/timeout fields; PhotoCraft roots/mapping documented as reference (D2) |
| Runtime failthrough in `auto` | No new CLI→MCP failthrough; explicit/auto rules per D3 |
| “MCP available/configured” | Normalized config has sufficient stdio launch info + preflight passes (D3) |
| Timeout/cancel/retry/reason codes | Bounded timeouts, stderr capture, safe cleanup; no blind tool retries; extend reasons minimally (D4) |
| Optional real integration | `@pytest.mark.integration`, opt-in, non-CI (D5) |
| `image-generate` alignment | Follow-up unless zero-risk reuse identified (D5) |
| Formal owner | Maintainers/project governance; user may override (D6) |

## Best Practices / Security Notes (evidence-backed)

- **Stdout protocol purity**: never log/print non-MCP bytes to the MCP server/client protocol stream; use stderr or in-process logging for diagnostics (MCP 2025-11-25/2026-07-28 stdio).
- **Subprocess safety**: bounded waits on read/write/startup; terminate process tree/process on timeout/failure; do not assume stderr means error.
- **Roots/access boundaries**: PhotoCraft headless requires read/write roots; treat roots and paths as sensitive configuration. Document least-privilege roots for optional real validation.
- **Untrusted content**: MCP tool results and PhotoCraft document-derived text may contain prompt-injection/steering content; adapter must treat payloads as data and normalize defensively.
- **No secret leakage**: redact credentials/tokens/PII from logs, errors, and metadata (consistent with constitution/skill security gates).

