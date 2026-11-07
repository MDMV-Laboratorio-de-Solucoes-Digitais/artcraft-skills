# Problem: MCP stateful session (007 Option B)

- **Slug**: 009-mcp-stateful-session
- **Date**: 2026-11-06

## Problem Statement

O adapter MCP 006 (`skills.core.artcraft_app_client.mcp_tools_list`/`mcp_tools_call`) é **stateless por chamada**: cada operação abre/fecha sua própria sessão stdio. Isso é seguro e simples, mas **impede fluxos determinísticos cross-call** que dependem de estado retido pelo servidor/processo MCP na mesma sessão (ex.: criar documento, executar comando, exportar artefato). A 007 Option A provou transporte/discovery/invocação stateless; a Option B foi explicitamente deferida.

Sem uma especificação/contrato para sessão stateful controlada, qualquer implementação futura corre risco de: quebrar FR-005/FR-006 e schemas públicos; vazar processos/arquivos temporários; assumir sessão server-side incompatível com MCP 2026-07-28; ou fazer claims de geração IA/artefato sem controles.

## Who is affected

- Mantenedores que precisam de prova opt-in de ciclo de artefato engine/editor (não IA).
- Skills futuras que dependam de operações document-scoped no PhotoCraft MCP.
- Revisores de segurança (roots, cleanup, timeout, opt-in).

## Impact of inaction

- Capacidades documentadas em 008 (doc_new/export/command_run) permanecem sem caminho seguro de composição cross-call.
- Pressão para workarounds ad-hoc fora do adapter, aumentando risco de regressão.

## Evidence

- 006: `_mcp_stdio_call` cria sessão por chamada (stateless). 007: evidência SC-001 stateless; `doc_inspect` sem estado persistente entre chamadas separadas (observado). 008: cross-call deferido a 007 Option B.
- MCP 2026-07-28: mudanças em handshake/sessão/negociação — design deve ser consciente (estado retido no cliente quando necessário; sem assumir `_Mcp-Session-Id` server-side no caminho 2026).