# Idea Intake: MCP stateful session (007 Option B)

- **Slug**: 009-mcp-stateful-session
- **Created**: 2026-11-06
- **Source**: plano MDMV 2026-11-06 (próximo 80/20 após 008), ROADMAP/OBJETIVO/007 deferment
- **Type**: improvement (assessment + spec; docs-only neste slice)

## Idea (as captured)

Especificar uma sessão MCP **stateful** (007 Option B) para permitir ciclo determinístico cross-call em **uma sessão retida** (ex.: `doc_new → command → doc_export`/artefato) quando o servidor alvo suportar, preservando 006/007/008: mock-first, opt-in real, segurança (roots/binário/timeout/cleanup), sem claim de geração IA, sem CI/default real smoke, sem quebrar contratos públicos (`SkillResult`, schemas, FR-005/FR-006, CLI/fallback).

## Restated

Projetar e especificar (assessment GO/no-go + spec Speckit) um helper/sessão MCP stateful de escopo estreito, compatível com o adapter 006, considerando MCP 2026-07-28 (sem assumir sessão server-side no caminho 2026; preferência por estado retido no cliente / multi-round-trip quando aplicável), para viabilizar fluxos de artefato determinísticos opt-in sem regressões.

## Origin & Context

- **007 Option A** concluída: smoke stateless opt-in provou `tools/list` + `command_list` (SC-001 exercido sob autorização, engine/editor only). Limitação explícita: adapter 006 stateless por chamada (`mcp_tools_list`/`mcp_tools_call` abrem sessão stdio própria); não há ciclo cross-call.
- **008** mapeou capacidades PhotoCraft defensivamente (docs-only) e reforçou deferral de stateful/IA/bridge.
- **Evidência observada**: `doc_inspect` mostrou sessão não-persistente entre chamadas separadas do adapter (OBJETIVO/008 research).

## First-Glance Unknowns

- [NEEDS CLARIFICATION: API de sessão stateful: context manager/test harness/helper interno vs extensão do adapter público — como preservar compatibilidade e evitar vazamento de processo?]
- [NEEDS CLARIFICATION: política de retry/timeout/cancelamento dentro de uma sessão retida sem violar FR-006/segurança?]
- [NEEDS CLARIFICATION: como tratar servidores que não mantêm estado de documento mesmo em uma sessão (capability gating/evidência)?]
- [NEEDS CLARIFICATION: escopo mínimo de ferramentas para prova: `tools/list` + `doc_new` + `command_run`/`command_list` + `doc_export` em write-root temporária, ou subconjunto mais seguro?]
- [NEEDS CLARIFICATION: impacto de MCP 2026-07-28 (server/discover, sem handshake/sessão server-side no caminho 2026) no design do helper?]
