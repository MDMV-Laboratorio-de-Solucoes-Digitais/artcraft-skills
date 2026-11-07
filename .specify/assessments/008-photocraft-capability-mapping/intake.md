# Idea Intake: PhotoCraft MCP capability mapping (engine/editor)

- **Slug**: 008-photocraft-capability-mapping
- **Created**: 2026-11-06
- **Source**: plano MDMV `local://mdmv-fluxo-artcraft-skills-plan.md` (P7 80/20), ROADMAP.md/OBJETIVO.md 2026-11-06
- **Type**: improvement (specification/mapping; docs-only)

## Idea (as captured)

Mapear capacidades reais do PhotoCraft expostas via MCP (`tools/list`/`tools/call`) — ferramentas `command_*`/`doc_*`/preview/resources, raízes de leitura/escrita com autoridade de filesystem, progresso via `_meta.progressToken` (0–1, ≤10/s), cancelamento via `notifications/cancelled`, semântica de erro e limites de formato/versão/protocolo — como **especificação de capacidade** para habilitar skills futuras. Sem implementar código de runtime neste slice; mock-first; validação real opt-in posterior.

## Restated

Produzir um artefato de mapeamento verificável (assessment + spec Speckit) que documenta, com limites explícitos, as capacidades MCP do PhotoCraft observadas/documentadas e como elas se alinham ao adapter 006/007, sem afirmar geração IA, sem sessão stateful, sem alterar contratos públicos.

## Origin & Context

- **Raised by**: fluxo MDMV 2026-11-06 (80/20).
- **Trigger**: 006 (MCP stdio mínimo viável) e 007 (stateless smoke opt-in, SC-001 exercido localmente com autorização) já provaram transporte/discovery real limitado; falta mapeamento profundo e estável por capacidade para guiar skills futuras sem overclaim.
- **Baseline verificada (2026-11-06)**: 412 passed, 23 deselected; 12/12 skills validadas; adapter `skills/core/artcraft_app_client.py` v0.3.0; `photocraft-cli 0.20.1` observado retornando 26 MCP tools via `tools/list`; `command_list` com engine command metadata (`file.new`, `edit.fill`, `paint.stroke`, `file.export.quickExport`, `layer.exportAs`, `doc.export`).

## First-Glance Unknowns

- [NEEDS CLARIFICATION: quais ferramentas PhotoCraft MCP são estáveis entre versões e quais exigem detecção defensiva/capability gating?]
- [NEEDS CLARIFICATION: qual subconjunto mínimo de capabilities (ex.: `command_list`/`command_run`/`doc_*`/`render_preview`) deve ser mapeado como P1 para habilitar skills de edição determinística?]
- [NEEDS CLARIFICATION: como representar roots/progresso/cancelamento no contrato de mapeamento sem exigir mudanças no adapter atual?]
- [NEEDS CLARIFICATION: onde registrar evidência de validação real opt-in futura (007 quickstart/runbook vs 008 quickstart) sem duplicar política de segurança?]
- [NEEDS CLARIFICATION: como tratar divergências entre MCP 2025-11-25, 2026-07-28 e comportamento observado do `photocraft-cli`?]
