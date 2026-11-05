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

## Estado Atual (Verificado — 2026-11-04)

**Branch**: `dev` (commit `14530b2`). Apenas `dev` e `main` remotos/locais restantes. Todos os PRs abertos mergeados.

- **Feature 001** (`001-artcraft-skills-suite`): Ciclo Spec Kit executado até implement; **68/98 tarefas (~69%)** completas. Verificação/convergência pendentes.
- **Feature 003** (`003-shared-cli-mcp-adapter`): **Convergida**. Adapter compartilhado `skills/core/artcraft_app_client.py` (9 funções, reason codes, `__version__=0.2.0`), `image-generate` refatorado com equivalência verificada.
- **Feature 004** (`004-implement-python-creative-skills`): **Completa e convergida**. Adicionado `skills/core/creative_skill.py` e skills Python executáveis para `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`. Schemas `SKILL.md` ↔ `skill.py` alinhados. Testes property-based e characterization adicionados (47 novos testes).
- **Constituição**: `.specify/memory/constitution.md` v2.0.0 em vigor.
- **Skills**: **12/12 validadas** (`python scripts/validate_all_skills.py` → `all_valid=True`). **5 skills criativos** com implementações Python executáveis via adapter compartilhado.
- **Testes**: **351 passando** (`python -m pytest -q` → `351 passed`), sem regressões.
- **Documentação**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `docs/architecture.md`, `AGENTS.md`.
- **Ferramentas**: CodeGraph sincronizado, Archify atualizado.

## Caminho Percorrido
- **Fundação Completa (100%)**: Schema agentskills.io, validação, descoberta/carregamento, registro no Spec Kit, abstrações core implementadas e testadas.
- **Adapter Compartilhado (100%)**: `artcraft_app_client.py` com degradação graciosa, reason codes e integração CLI/MCP.
- **Skills Criativos Python (100%)**: Todos os 4 skills da feature 004 implementados com `CreativeSkill` base class, testes dedicados adicionados.
- **Composição e Orquestração**: `SkillComposer` e `DAGOrchestrator` funcionais com testes abrangentes.
- **Workflows Generalizáveis**: Padrões derivados e abstraídos sem branding específico.
- **Governança**: Constituição v2.0.0 estabelecida, fluxo Spec Kit executado até convergência (003, 004).

## O Que Ainda Falta
- **Feature 001 (artcraft-skills-suite)**: 68/98 tarefas (~69%) concluídas; faltam ~30 tarefas. Analyze/converge não executados. Alguns testes originais de `image-generate` perdidos durante merge (cobertura substituída por golden/differential/property).
- **Expansão de Mídias**: Fases 3-5 (vídeo/motion, áudio/documentos/apresentações, CAD/precisão) — majoritariamente não iniciadas.
- **Processamento em lote e templates** (Phase 6): Pendente.
- **Hardening de orquestração**: Validação end-to-end com provedores reais, melhorias em polling/webhook/retry/idempotency.
- **Integração MCP funcional**: Atualmente apenas stubs; conexão real, descoberta de tools e execução via MCP pendentes.
- **Resiliência**: Retry com exponential backoff + jitter, rate limiting e concurrency limiter por instância.
- **Observabilidade**: Logging estruturado e métricas RED efetivamente integrados aos skills.

## Métricas de Sucesso

- ✅ **Validação**: 12/12 skills passando (all_valid=True)
- ✅ **Testes**: 351/351 testes passando (unit/contract/integration/property/characterization)
- ✅ **Padrão**: Compatível com agentskills.io em múltiplos agentes
- ✅ **Feature 003**: Convergida
- ✅ **Feature 004**: Completa e convergida com cobertura de testes
- 🔄 **Feature 001**: 68/98 tarefas (~69% completo)
- ⏳ **Cobertura Completa**: Expansão para todas as mídias criativas planejadas

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
