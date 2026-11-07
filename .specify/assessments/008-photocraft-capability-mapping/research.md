# Research: PhotoCraft MCP capability mapping

- **Slug**: 008-photocraft-capability-mapping
- **Date**: 2026-11-06
- **Method**: evidência local do repositório (006/007, adapter, OBJETIVO/ROADMAP, quickstarts) + pesquisa web (agentskills.io, MCP spec/SDK, `storytold/photocraft` docs públicos). Sem execução de MCP real adicional nesta rodada.

## Findings

### 1. Baseline do adapter (006)

- `skills/core/artcraft_app_client.py` (v0.3.0) expõe transporte stdio mínimo: `mcp_tools_list(cfg, timeout)`, `mcp_tools_call(cfg, tool_name, arguments, timeout)`.
- FR-005: `select_mode`; explícito vence; `mode=mcp` sem reroute silencioso; `auto` CLI-first/back-compat.
- FR-006: reason codes aditivos (`mcp_unavailable`, `mcp_misconfigured`, `mcp_startup_timeout`, `mcp_call_timeout`, `mcp_invalid_response`, `mcp_missing_capability`, `mcp_tool_error`, etc.), metadados aditivos, sem secrets/PII.
- **Limite atual**: adapter stateless por chamada (006) — cada list/call executa sessão stdio própria; sem reuso de sessão/ciclo cross-call.

### 2. Evidência 007 (real, opt-in, escopo limitado)

- Smoke local autorizado (2026-11-06) provou `tools/list` + `tools/call name=command_list` contra `photocraft-cli 0.20.1` com temp roots, timeout, cleanup. Resultado: capability presente, não-erro/normalizável; `stateless/session_reuse=false/artifact_cycle=false`. **Sem claim de geração IA.**

### 3. Superfície PhotoCraft MCP (observada/documentada)

- **Observado localmente (0.20.1, evidência 007/OBJETIVO)**: 26 MCP tools; `command_list` retorna engine command metadata; exemplos observados: `file.new`, `edit.fill`, `paint.stroke`; export: `file.export.quickExport`, `layer.exportAs`, `doc.export`. `doc_inspect` mostrou sessão não-persistente entre chamadas separadas do adapter.
- **Documentação pública `storytold/photocraft` (acesso 2026-11-06)**:
  - `docs/mcp.md` / `book/src/automation/mcp.md`: `photocraft-cli mcp --automation-read-root <abs> --automation-write-root <abs>` (headless); roots concedem autoridade de filesystem.
  - Ferramentas típicas: `command_list` (filter, enabled_only), `command_run` (id, params, wait), `command_batch` (steps, stop_on_error; não atomic transaction), `doc_inspect`, `render_preview` (index, max_side default 1024, máx 2048), `ui_inspect`/`ui_screenshot` (bridge), `doc_new/open/save/export/place/select` etc.; exports multi-file recusam overwrite; `doc_save/export` têm restrições de overwrite/formato.
  - Progresso via `_meta.progressToken` (0–1, throttled ≤10/s, inclui `total`); cancelamento via `notifications/cancelled`.
  - Bridge mode (`--bridge`, control token, roots no app desktop) — **fora do escopo stateless headless 006/007/008**.
- **Risco**: nomes/params podem variar por versão; mapeamento deve ser defensivo (capability gating via `tools/list`/`command_list`, sem hardcode frágil).

### 4. Protocolo MCP

- MCP 2025-11-25: stdio JSON-RPC framing usado pelo adapter 006.
- MCP 2026-07-28 (pesquisa 2026-11-06): `server/discover`, _meta/negociação evoluídos; caminho 2026 sem handshake/sessão server-side; server-initiated requests (roots/sampling/logging/ping) alterados/deprecados conforme revisão. **007 Option B** deve considerar multi-round-trip client-side / estado retido no cliente, não sessão server-side.
- **Implicação 008**: documentar alinhamento/limites por revisão; não afirmar suporte a features não implementadas.

### 5. MCP Python SDK

- `modelcontextprotocol/python-sdk` v2.3.0 fala 2026-07-28 e serve 2025-11-25/2026-07-28 (pesquisa 2026-11-06). Migração do cliente mínimo 006 → SDK v2 permanece **backlog** (mock-first/back-compat).

## Gaps / Open Questions carried to concept/decision

- Subconjunto P1 de capabilities para skills determinísticas (sem IA): discovery + engine commands + doc/export? preview?
- Como normalizar progress/cancel/roots no mapeamento sem mudar adapter.
- Política de validação real opt-in futura: reutilizar runbook 007 (SC-001/segurança) e adicionar apenas capability-specific evidence em 008.
- Tratamento de drift de versão: assertions mínimas/presença, nunca contagens exatas.
