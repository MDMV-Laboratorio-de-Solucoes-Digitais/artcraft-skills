# Research: MCP stateful session (009)

**Date**: 2026-11-06

## Sources

| Source | Type | Notes |
|---|---|---|
| `skills/core/artcraft_app_client.py` (006) | local | Stateless per-call stdio sessions; FR-005/FR-006 |
| `specs/006-mcp-stdio-functional-integration/*` | local | Transport/normalization baseline |
| `specs/007-photocraft-mcp-smoke/*` | local | Option A stateless SC-001 (authorized, limited); Option B deferred |
| `specs/008-photocraft-capability-mapping/*` | local | Capability tiers, gating, cross-call limits |
| MCP 2025-11-25 stdio/tools/lifecycle | primary web (prior) | JSON-RPC over stdio; subprocess model |
| MCP 2026-07-28 changelog/server/discover (2026-11-06) | primary web | No server-side session assumption on 2026 path; negotiation changes |
| MCP Python SDK v2.3.0 notes (2026-11-06) | primary web | Future migration candidate; backlog |

## Key Findings

- **Stateless boundary (006/007)**: cross-call document state not preserved. Option B requires retained subprocess/session on client side.
- **Minimum safe cycle**: gated discovery + document-scoped operations + export/inspect in temp write-root; only if server supports; engine/editor only.
- **Cleanup risk**: orphan processes/file handles on timeout/error — contract must mandate bounded shutdown and finalizers.
- **Protocol evolution**: design must not encode deprecated session semantics; prefer explicit request/response correlation over retained connection.

## Decisions

| Decision | Rationale | Alternative |
|---|---|---|
| Additive helper, not replace stateless | Back-compat, low risk | Refactor 006 APIs (risky) |
| Docs-only now | 80/20 spec/decide; runtime needs TDD | Implement now (larger, unplanned) |
| Client-retained process state | MCP 2026-07-28 awareness; stdio reality | Assume server session ID (fragile) |
| Mock-first future + opt-in real | Determinism + safety | Real-only tests (non-deterministic/unsafe) |