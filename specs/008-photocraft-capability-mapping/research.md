# Research: PhotoCraft MCP capability mapping (008)

**Date**: 2026-11-06 | **Branch**: `008-photocraft-capability-mapping`

## Sources

| Source | Type | Access | Notes |
|---|---|---|---|
| `skills/core/artcraft_app_client.py` v0.3.0 | local code (reference) | 2026-11-06 | `mcp_tools_list`, `mcp_tools_call`, FR-005/FR-006, stateless per call |
| `specs/006-mcp-stdio-functional-integration/*` | local spec | 2026-11-06 | MCP stdio mínimo viável, mock-first, selection/normalization |
| `specs/007-photocraft-mcp-smoke/*` | local spec/evidence | 2026-11-06 | Option A stateless; SC-001 exercido localmente sob autorização; `tools/list`+`command_list`; no AI claim |
| `OBJETIVO.md`/`ROADMAP.md` | local docs | 2026-11-06 | Baseline 412/23, 12/12; 26 MCP tools observadas (0.20.1) |
| https://agentskills.io/specification | primary web | 2026-11-06 | Skill format/validation alignment |
| https://modelcontextprotocol.io/specification/2026-07-28/changelog, /server/discover | primary web | 2026-11-06 | 2026-07-28 changes (server/discover, _meta, sessão/handshake) |
| https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0, docs v2 | primary web | 2026-11-06 | SDK v2.3.0, 2025-11-25 + 2026-07-28 support |
| https://github.com/storytold/photocraft (docs/mcp.md, book automation) | primary web | 2026-11-06 | Public MCP docs; roots, tools, progress/cancel, overwrite constraints |

## Decisions

| Decision | Rationale | Alternatives considered |
|---|---|---|
| Docs-only slice, no runtime changes | 80/20 baixo risco; habilita skills futuras sem regressão | Implementar skill/mapping em código agora (maior risco, escopo maior) |
| Defensive gating obrigatório | Versões/params variam; 0.20.1 é evidência limitada | Hardcode tool count/catalog (frágil) |
| Tiers P1/P2/P3 com evidence status | Separa determinístico/alto valor de referência/incerto | Lista plana sem prioridade/evidência |
| Excluir IA, stateful cross-call, bridge | Consistente com 006/007, constitution, evidência | Incluir geração IA/Option B (sem evidência/fora do adapter) |
| Reutilizar 007 safety pattern para validação real futura | Evita duplicar política opt-in/roots/cleanup | Novo runbook independente (drift) |
| SDK v2 permanece backlog | Cliente mínimo 006 suficiente para mapping; migração tem custo | Migrar agora (fora do 80/20 docs-only) |

## Capability Surface (evidence-tiered summary)

| Capability area | Examples (observed/documented) | Tier candidate | Evidence | Notes |
|---|---|---|---|---|
| Discovery | `tools/list`, `command_list` | P1 | observed + documented | Ponto de entrada obrigatório; `command_list` dá engine metadata |
| Engine invocation | `command_run`, `command_batch` | P1/P2 | documented (+ command_list observed) | `command_batch` não atomic; `stop_on_error` default true (docs) |
| Document lifecycle | `doc_new/open/save/export`, `doc_inspect`, `doc_place/select` | P2 (headless constraints) | observed limited + documented | Cross-call state limitado pelo adapter stateless 006 |
| Preview | `render_preview` | P2 | documented | `index`, `max_side` default 1024 máx 2048 |
| Jobs/session | `jobs_*`, `session_list` | P3/reference | observed name presence | Semântica não aprofundada neste slice |
| UI/bridge | `ui_*`, bridge mode | P3/out of headless scope | documented | Requer desktop/control token |
| Progress/cancel | `_meta.progressToken`, `notifications/cancelled` | P2/reference | documented | Suporte adapter não implementado em 008 |
| Export constraints | overwrite rules, multi-file no overwrite | P1 safety note | documented | Deve ser respeitado por skills futuras |

## Open Items (deferred)

- 007 Option B: stateful session helper / multi-round-trip client-side para ciclo cross-call (MCP 2026-07-28).
- Adapter support para progress/cancel observável.
- MCP SDK v2 migration decision.
- Capability-specific real opt-in evidence per tool (only when authorized).