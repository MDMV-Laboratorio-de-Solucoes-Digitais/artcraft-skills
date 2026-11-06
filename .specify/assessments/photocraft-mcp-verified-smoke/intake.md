# Idea Intake: PhotoCraft MCP verified local smoke and one deterministic headless capability mapping

- **Slug**: photocraft-mcp-verified-smoke
- **Created**: 2026-11-05
- **Source**: pasted text (user-provided 80/20 proposal, captured in-session)
- **Type**: improvement

## Idea (as captured)

> “PhotoCraft MCP verified local smoke + one deterministic headless capability mapping” (pequeno, mock-first preservado).
>
> Por quê é 80/20:
> - Reaproveita tudo já pronto (adapter/FR-005/FR-006/testes). O transporte já funciona contra photocraft-cli 0.20.1.
> - Transforma “MCP funciona em mock” em “MCP comprovado com servidor real local + 1 fluxo real útil/determinístico”, com baixo risco e sem depender de modelos/credenciais cloud.
> - Evita o erro caro: tentar “geração por prompt via PhotoCraft MCP” sem evidência de tool/capability de IA no motor local (PhotoCraft expõe engine commands; geração IA é outra superfície/produto).
>
> Escopo mínimo do 80/20 (a especificar):
> 1. Smoke real opcional, determinístico e seguro (não padrão CI): usar/ajustar tests/integration/test_mcp_stdio_photocraft_optional.py para tools/list + command_list (e opcionalmente um ciclo doc_new→comando simples→doc_export/artefato em write-root temporária) com ARTCRAFT_MCP_INTEGRATION=1, roots temporários, cleanup, timeout; exigir binário explícito. Registrar evidência em specs/.../quickstart.md ou docs/.
> 2. Mapear 1 capability local concreta (ex.: export/conversão simples ou edição determinística raster suportada por command_run) no caminho MCP do CreativeSkill/skill existente, com normalização SkillResult, sem quebrar schemas/CLI/fallback. Não fingir geração IA.
> 3. Documentar limites: MCP local = motor PhotoCraft; geração IA/modelos/provider = fora desse slice salvo evidência. Atualizar README.md/quickstart com comando real verificado:
>
> ```bash
> photocraft-cli mcp --automation-read-root /tmp/pc-r --automation-write-root /tmp/pc-w
> ```
> 4. Higiene rápida (opcional no mesmo PR pequeno): desambiguar referência 006-*, fechar notas documentais Speckit residuais.
>
> Se quiser começar já (sem código novo de produto): rodar o smoke manual reproduzível e registrar evidência (maior confiança, ~baixo esforço). Eu já validei tools/list/command_list via adapter; falta apenas um ciclo com artefato em write-root temporária + evidência formal no doc de integração.

Context captured alongside intake (factual, session-observed): prior 006 MCP stdio work added mock-first `tools/list`+`tools/call` with FR-005/FR-006 and preserved contracts; a local `/usr/bin/photocraft-cli 0.20.1` was observed returning 26 MCP tools and `command_list` results via `skills.core.artcraft_app_client` with temporary read/write roots. This is context, not an intake verdict.

## Restated

Proposed work would add an optional, deterministic, safe local verification path for the existing MCP stdio integration against a real PhotoCraft MCP server, and map one concrete deterministic headless capability (not AI prompt generation) through the existing skill/MCP path with normalized `SkillResult`, while preserving mock-first tests, existing schemas, CLI, and fallback behavior.

## Origin & Context

- **Raised by**: user request in current session (following repo-status/roadmap analysis and 80/20 recommendation).
- **Trigger**: need to convert mock-verified MCP stdio integration into locally verified real-server behavior with minimal risk/effort; avoid assuming prompt-based AI generation is available through PhotoCraft’s local engine-oriented MCP tools without evidence. Current repo state: 006 MCP stdio implemented (mock-first), 399 passed/1 deselected default, 12/12 skills validated.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: Which single deterministic headless capability provides clear end-to-end value and is reliably supported by `photocraft-cli` MCP in target environments (e.g., `doc_new` + simple command + `doc_export`, raster edit, or conversion/export)?]
- [NEEDS CLARIFICATION: Which existing skill should own the mapping (`image-edit`, `image-generate` fallback path, or a narrow new/adapter-level capability), without misrepresenting AI generation?]
- [NEEDS CLARIFICATION: Exact acceptance evidence for the optional real smoke (required artifacts, command transcript shape, roots/cleanup policy, binary discovery/override, timeout bounds)?]
- [NEEDS CLARIFICATION: Should the cycle be limited to `tools/list`+`command_list`, or include file-producing `doc_export` in a temporary write root by default when the optional integration is explicitly enabled?]
- [NEEDS CLARIFICATION: How to document and resolve the existing `006-integracao-geracao-assets` vs `006-mcp-stdio-functional-integration` numbering ambiguity in specs/assessments?]
- [NEEDS CLARIFICATION: What minimum PhotoCraft/`photocraft-cli` version/capability assumptions are acceptable for the optional smoke, given local 0.20.1 was observed?]
- [NEEDS CLARIFICATION: CI policy — keep real PhotoCraft smoke strictly local/opt-in, or allow a dedicated non-default job when a trusted binary is provisioned?]
