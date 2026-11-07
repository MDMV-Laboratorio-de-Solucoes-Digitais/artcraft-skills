# Decision note: MCP Python SDK v2 vs minimal client (artcraft-skills)

- **Date**: 2026-11-06
- **Context**: 006 implemented a minimal synchronous stdio JSON-RPC client (mock-first, deterministic, FR-005/FR-006, back-compatible). 009 added an additive retained-session helper reusing the same framing/normalization. `modelcontextprotocol/python-sdk` v2.3.0 (2026-10-02) targets MCP 2026-07-28 and serves 2025-11-25/2026-07-28 (per SDK docs/releases, ecosystem research 2026-11-06).
- **Decision (current)**: **Keep minimal client + additive 009 helper for now (no migration in this slice).** Re-evaluate SDK v2 when a concrete need exceeds minimal scope.
- **Why keep minimal now**:
  - **Determinism/mock-first**: fake stdio servers and bounded behavior are simple and stable; default gates (421/23, 12/12) and 006/009 coverage are green.
  - **Contract stability**: preserves public schemas, `SkillResult`, FR-005/FR-006, CLI/fallback, additive exports; low regression risk.
  - **Scope fit**: verified needs (006 stateless `tools/list`/`tools/call`, 009 retained multi-call, opt-in PhotoCraft engine/editor smoke) are satisfied without SDK lifecycle/auth/remote/Streamable HTTP features.
  - **MCP 2026-07-28 awareness**: 009 uses client-retained process state and does not assume server-side session IDs; protocol evolution handled defensively/documented.
- **When to migrate/adopt SDK v2** (trigger-based):
  1. Need Streamable HTTP/remote MCP/auth/OAuth or advanced session lifecycle beyond local stdio.
  2. Need `server/discover`/negotiation/features not practical in minimal client.
  3. Need broader multi-server interoperability where SDK maintenance cost < custom maintenance.
  4. Security/compatibility fixes in SDK that outweigh migration/test churn.
- **Migration constraints (if triggered)**:
  - TDD/mock-first first; preserve 006/009 public behavior and reason taxonomy where applicable (additive mapping allowed).
  - Keep opt-in real smokes explicit (never CI/default); maintain capability-gating (008) and version-tolerant assertions.
  - No AI-generation/provider/model claims introduced by migration.
  - Separate spec/slice with characterization tests around `artcraft_app_client`/CreativeSkill MCP boundaries.
- **Status**: backlog/decision recorded; **not implemented**. Revisit after B (version-tolerant params) or when a trigger appears.
