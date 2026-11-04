# Objetivo do Projeto

## Visão Geral

ArtCraft Skills Suite tem como objetivo construir um ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O projeto visa capacitar artistas, designers e criadores a transformar prompts em *crafting* intencional, proporcionando controle preciso e fluxos compostos em vez de geração *one-shot*.

As skills não reimplementam motores de geração: elas expõem, de forma composável e governada, as capacidades reais dos apps ArtCraft (PhotoCraft, PdfCraft e os demais "Crafting Apps" Rust da organização `storytold`), via suas superfícies de **CLI** (`photocraft-cli`, 500+ comandos) e **MCP server**, além da AI studio da ArtCraft (60+ modelos de imagem/vídeo/áudio/3D/mundos). O repositório é a *camada de skill/agente* sobre essas superfícies.

## Objetivos Principais

### Objetivo Geral
Criar um framework completo e extensível de habilidades para agentes de IA que permita a criação, manipulação e composição de assets criativos através de workflows intencionais e componíveis, seguindo os princípios de "crafting over generating", sobre as superfícies CLI/MCP reais dos apps ArtCraft.

### Objetivos Específicos

1. **Padronização e Interoperabilidade** - Seguir rigorosamente o padrão agentskills.io para garantir compatibilidade com Claude Code, Cursor, Codex, Gemini, OpenCode e outros agentes compatíveis (formato SKILL.md com frontmatter YAML; descoberta/carregamento padronizados).
2. **Composição e Orquestração** - Fornecer abstrações (`BaseSkill`, `SkillComposer`, `DAGOrchestrator`, `AssetContext`) que permitam compor skills simples em workflows complexos, incluindo pipelines cross-product (ex.: 2D→3D).
3. **Cobertura Criativa Abrangente** - Suportar fluxos para 2D/raster, vetorial, 3D/espacial, vídeo/motion, áudio, documentos/apresentações e CAD/técnico, via os apps ArtCraft correspondentes.
4. **Abstração de Provedores e Apps** - Manter design vendor-neutral com roteamento multi-provedor (60+ modelos) e adapter compartilhado sobre as superfícies CLI/MCP dos apps ArtCraft (discovery, invocation, normalização, mode selection, error standardization), suportando ambas modalidades de auth da API ArtCraft.
5. **Transparência e Consciência de Custos** - Fornecer estimativa de custos, orquestração assíncrona com polling/webhooks, e tratamento transparente de recursos e erros (reason codes: `cli_not_found`, `mcp_unavailable`, `neither_available`, `is_error`).
6. **Qualidade e Governança** - Seguir a Constituição v2.0.0 com princípios de controle artístico, composabilidade, performance e extensibilidade sem complexidade desnecessária; ciclo Spec Kit (intake→research→define→shape→decide→specify→clarify→plan→checklist→tasks→implement→analyze→converge).
7. **Extensibilidade Comunitária** - Facilitar contribuições através de documentação clara, templates, validação rigorosa e integração com Spec Kit; compatibilidade com registros (skills.sh, agentskills.io client showcase).

### Pesquisa e Contexto Competitivo (verificado 2026-11-04)

- **agentskills.io** é o formato aberto de facto, com guias de best practices (descrições, evals, integração MCP/CLI) e ampla adoção por agentes. Nosso schema/loader/validação já conformam.
- **Superfícies ArtCraft**: 13–16 apps Rust open-source (`storytold`), cada um com CLI + servidor MCP; `photocraft-cli` expõe 500+ comandos. Existem tutoriais e um `craft-agent-kit` (wrappers/MCP configs/skills para os 13 apps). Nosso adapter envolve exatamente essas superfícies.
- **Packs concorrentes/complementares**: `full-aigc-skills/artcraft-skills`, `midasmatterhorn/artcraft-skills`, `MGBuilds9/craft-agent-kit`. Diferenciação: ciclo Spec Kit, constituição, equivalência testada por caracterização, adapter compartilhado com reason codes, abstrações vendor-neutral, workflows generalizáveis derivados de MDMV.
- **Ecossistema criativo de agent skills** (`pexo-skills`, `generative-media-skills`, `scenario`, `muapi`, `open-clip`, `claude-remotion-skill`) confirma demanda por skills de imagem/vídeo/áudio/3D para agentes. Fases 3–5 do roadmap visam esses domínios via apps ArtCraft, sem reimplementar provedores.
- **MCP**: spec 2026-07-28 (core stateless); MCP é o padrão dominante para ferramentas criativas. Decisão documentada: discovery/invocation MCP permanecem a nível de skill (FR-005), adapter normaliza config/output — alinhado ao padrão de adaptadores finos sobre servidores MCP reais.

### Caminho Percorrido
- **Fundação Completa (100%)**: Schema agentskills.io, validação, descoberta/carregamento, registro no Spec Kit, abstrações core implementadas e testadas.
- **Feature 003 Concluída e Convergida**: Adapter compartilhado `skills/core/artcraft_app_client.py` (9 funções, reason codes, `__version__=0.2.0`), refactor de `image-generate` com equivalência verificada (golden master + differential + property), 41/41 checklists, analyze + converge executados.
- **Skills Implementadas**: 14 skills validadas em `core/`, `creative/`, `workflow/` e `integration/`.
- **Composição e Orquestração**: `SkillComposer` e `DAGOrchestrator` funcionais com testes abrangentes.
- **Workflows Generalizáveis**: Padrões derivados e abstraídos sem branding específico.
- **Governança**: Constituição v2.0.0 estabelecida, fluxo Spec Kit executado até convergência (003) e parcialmente (001).
- **Testes**: 278 testes passando (unit/contract/integration/property/characterization) com pytest 9.0.3 + Hypothesis.
- **Documentação**: `docs/skill-authoring.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`, `architecture.md`, `AGENTS.md`.
- **Tooling**: CodeGraph sincronizado, artefatos Archify, pytest/Hypothesis.

### O Que Ainda Falta
- **Feature 001 (artcraft-skills-suite)**: 68/98 tarefas concluídas; faltam 30 tarefas (testes de propriedade/contrato/integração para US1–US5, skills criativas em Python, compositor, orquestrador, abstrações restantes). Analyze/converge não executados. `tasks.md` desatualizado (21 `[ ]` stale).
- **Implementações Concretas**: 5 skills criativos agora têm `skill.py` (image-generate, image-edit, background-remove, image-upscale, mesh-generate) via adapter compartilhado.
- **Expansão de Mídias**: Implementar fases 3-5 (vídeo/motion, áudio/documentos/apresentações, CAD/precisão).
- **Integrações Profundas**: Processamento em lote, templates de projeto e wiring completo com app ArtCraft.
- **Execução Real**: Validação end-to-end com provedores reais e hardening de job orchestration.
- **Testes Perdidos**: Os 23 testes originais de image-generate (unit/contract/integration) foram perdidos durante reset/merge; cobertura substituída por golden/differential/property.
- **Diferenciação**: Publicar benchmarks/cobertura vs. packs concorrentes; contribuir para client showcase do agentskills.io.

## Métricas de Sucesso

- ✅ **Validação**: 14/14 skills passando (all_valid=True)
- ✅ **Testes**: 278/278 testes passando (unit/contract/integration/property/characterization)
- ✅ **Padrão**: Compatível com agentskills.io em múltiplos agentes
- ✅ **Feature 003**: Convergida (adapter compartilhado + refactor image-generate)
- 🔄 **Feature 001**: 68/98 tarefas (~69% completo)
- ⏳ **Cobertura Completa**: Expansão para todas as mídias criativas planejadas
- ✅ **Implementações Python**: 5/5 skills criativos com código executável

## Diretrizes de Desenvolvimento

- **Composição Primeiro**: Sempre preferir composição de skills simples sobre soluções monolíticas
- **Controle Artístico**: Manter controle preciso do artista em todo o fluxo
- **Vendor-Neutral**: Abstrair provedores, evitar lock-in
- **Transparente**: Expor custos, modelos e parâmetros claramente
- **Testado**: Seguir TDD quando aplicável, com testes property-based
- **Documentado**: Todo skill deve ter documentação completa
- **Open Source**: Licenças MIT/Apache-2.0, sem branding específico em skills/constituição
- **CLI/MCP-first**: Consumir superfícies reais dos apps ArtCraft; não reimplementar provedores
- **MCP a nível de skill**: Discovery/invocation MCP permanecem na skill; adapter normaliza config/output (FR-005)
