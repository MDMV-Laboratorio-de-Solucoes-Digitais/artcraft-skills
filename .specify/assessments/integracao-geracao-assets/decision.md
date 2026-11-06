# Decision: Integração de geração de assets com ArtCraft

- **Slug**: integracao-geracao-assets
- **Decided**: 2026-11-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | Usuários reais precisam gerar assets via skills, comprovado por briefings e tentativas práticas |
| Evidence strength | adequate | Código analisado, CLI verificado, mas comandos exatos de geração desconhecidos |
| Value vs. inaction | strong | Bloqueia automação de assets, solução pragmática viável |
| Feasibility / appetite | adequate | Pequeno ajuste no adapter/skills, fallback viável |
| Strategic fit | strong | Alinha com constituição (orquestrar superfícies reais) e objetivos do projeto |
| Risk posture | adequate | Riscos mitigados com abordagem discovery-first + fallback gracioso |

## Verdict & Rationale

**GO** - Problema real e bem definido. Abordagem discovery-first (usar comandos reais quando existirem) + fallback para edição é pragmática, segue constituição, mantém compatibilidade. Evidência suficiente para prosseguir com especificação.

## If go — Handoff to `/speckit.specify`

- **Problem**: Usuários de agentes IA usando skills criativas do ArtCraft não conseguem gerar assets quando não há comandos de geração explícitos disponíveis via CLI/MCP
- **Chosen approach**: Option A — Descobrir e configurar geração existente + fallback para edição
- **In scope / out of scope**: 
  - In scope: Descobrir comandos de geração (CLI/MCP), configurar keywords/override, adicionar caminho alternativo com comandos de edição para pixel art simples, manter contratos
  - Out of scope: Reimplementar motores, geração complexa via edição, mudar comportamento quando geração já funciona
- **Success metrics**: Skills geram assets pixel-art simples via edição quando não há geração; usa geração real quando disponível; 357/357 testes passam
- **Carried-forward open questions**: Comandos exatos de geração disponíveis, MCP tools, configuração necessária
