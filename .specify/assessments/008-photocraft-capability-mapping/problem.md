# Problem: PhotoCraft MCP capability mapping

- **Slug**: 008-photocraft-capability-mapping
- **Date**: 2026-11-06

## Problem Statement

O repositório já possui transporte MCP stdio funcional (006) e smoke stateless real opt-in (007) que prova `tools/list` + `command_list` em escopo limitado. Porém, **não existe um mapeamento consolidado, verificável e com limites explícitos** das capacidades MCP reais do PhotoCraft (ferramentas, parâmetros, raízes, progresso, cancelamento, erros, restrições de formato/protocolo) que permita planejar e implementar skills futuras de forma segura e sem overclaim.

Sem esse mapeamento, implementadores tendem a: assumir capacidades de geração IA inexistentes na superfície MCP local engine/editor; acoplar skills a nomes/parâmetros instáveis sem gating defensivo; ignorar constraints de filesystem roots, overwrite e statelessness do adapter; ou duplicar decisões já tomadas em 006/007.

## Who is affected

- Mantenedores/implementadores de skills criativas que consumirão `photocraft-cli` via adapter 006.
- Revisores Speckit/segurança que precisam avaliar claims de capacidade.
- Agentes de IA que precisam de contratos claros para decidir quando usar `command_run`/`doc_*`/preview vs quando recusar/adiar.

## Impact of inaction

- Maior risco de specs/skills com claims incorretos (especialmente geração IA).
- Retrabalho ao implementar 007 Option B ou skills de edição/export sem contrato de capability.
- Fragilidade diante de drift de versão do `photocraft-cli`/protocolo MCP.

## Evidence

- `skills/core/artcraft_app_client.py` v0.3.0: `mcp_tools_list`, `mcp_tools_call`, FR-005/FR-006.
- 007 Option A: evidência local autorizada de `tools/list` + `command_list` (stateless, engine/editor only, sem IA).
- `photocraft-cli 0.20.1` observado com 26 MCP tools (incl. `command_list`, `command_run`, `command_batch`, `doc_*`, `render_preview`, jobs/session/UI/bridge) — evidência local limitada; validar defensivamente.
- Pesquisa externa 2026-11-06: docs públicas `storytold/photocraft` (`docs/mcp.md`, `book/src/automation/mcp.md`); MCP 2026-07-28 (server/discover, _meta, mudanças de sessão/handshake); MCP Python SDK v2.3.0.
- Baseline: 412 passed, 23 deselected; 12/12 skills validadas.
