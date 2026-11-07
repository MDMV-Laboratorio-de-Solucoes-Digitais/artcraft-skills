# Concept: MCP stateful session helper (007 Option B)

- **Slug**: 009-mcp-stateful-session
- **Date**: 2026-11-06
- **Verdict direction**: GO (scoped, spec/docs-only nesta rodada)

## Proposed Approach (80/20)

Especificar um **helper de sessão MCP stateful** (aditivo) que:

1. Inicia um subprocesso MCP stdio **retido** para N chamadas correlacionadas (JSON-RPC ids), com handshake/initialize conforme necessário para o caminho suportado, timeouts bounded e cleanup garantido (context manager/try-finally no design futuro).
2. Expõe operações mínimas: discovery (`tools/list` ou equivalente) + chamadas de tool sequenciais na mesma sessão (ex.: `doc_new` → `command_run`/engine command → `doc_export`/`doc_inspect`/`render_preview` conforme capability gating).
3. Mantém **006 stateless APIs intactas**; FR-005/FR-006 preservados; `SkillResult`/schemas públicos inalterados.
4. Exige capability gating defensivo (008) e limites: engine/editor only, sem IA, sem bridge/UI, sem CI/default real.
5. Trata MCP 2026-07-28 com cautela: **reter estado no cliente/processo vivo**; não assumir sessão server-side; documentar `server/discover`/negociação como follow-up compatível.

## In Scope (spec)

- Contrato do helper/sessão, lifecycle, erros/cleanup, safety controls, mock-first test requirements (para implementação futura), opt-in real validation pattern.
- Mapeamento do ciclo determinístico mínimo (PhotoCraft engine/editor) como evidência alvo, condicionado a capability/ambiente.

## Out of Scope

- Implementação de runtime neste slice (docs-only assessment+spec).
- Geração IA/provider/model.
- Mudanças em `skills/`, `tests/`, `scripts/` (neste slice).
- Bridge/UI, default CI real smoke.
- Suporte universal a todos os servidores MCP.

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Vazamento de processo/temp | Cleanup obrigatório, bounded timeouts, context lifecycle no contrato |
| Regressão 006/007 | APIs aditivas; stateless preservado; FR-005/FR-006 mapping |
| Incompatibilidade MCP 2026-07-28 | Client-retained process state; não assumir server session ID |
| Overclaim IA/artefato | Exclusões explícitas; capability gating; opt-in evidence only |