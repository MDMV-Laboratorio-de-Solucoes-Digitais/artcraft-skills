# Research: MCP stateful session (009 / 007 Option B)

- **Slug**: 009-mcp-stateful-session
- **Date**: 2026-11-06
- **Method**: evidência local 006/007/008 + specs MCP; sem execução real adicional.

## Findings

1. **006 adapter**: `artcraft_app_client._mcp_stdio_call` (nome/forma conforme 006) executa sessão por chamada; `mcp_tools_list`/`mcp_tools_call` são stateless. Preservar API pública; qualquer stateful deve ser **aditivo e opt-in** (helper/contexto separado) ou claramente isolado.
2. **007**: Option A provou stateless; Option B adiada por boundary. Harness 007 usou opt-in, temp roots, timeout, cleanup, binário explícito — padrões obrigatórios para 009.
3. **008**: `doc_*`/`command_run`/`render_preview` mapeados com evidência limitada; cross-call requer stateful; exclusões: IA, bridge/UI, CI/default real.
4. **MCP 2025-11-25**: stdio JSON-RPC; ciclo request/response por conexão suportado pelo subprocesso retido.
5. **MCP 2026-07-28** (pesquisa 2026-11-06): `server/discover`; evolução de _meta/negociação; caminho 2026 sem handshake/sessão server-side tradicional — **não depender de sessão server-side**; helper pode reter subprocesso stdio + estado client-side (processo vivo) para múltiplas chamadas correlacionadas por `id`.
6. **Segurança**: manter roots absolutos, least privilege, cleanup de processo/temp, bounded timeouts por chamada e/ou total, sem segredos/PII, FR-006 reasons.

## Design constraints (input to concept)

- API stateful **não** substitui `mcp_tools_list`/`mcp_tools_call` stateless existentes.
- Mock-first: fake stdio server determinístico para testes de sessão retida (futuro, fora do slice docs-only se necessário; spec deve exigir).
- Real validation: opt-in + autorização explícita + controles 007.
- Engine/editor only; sem geração IA; sem bridge/UI headless fora de escopo.