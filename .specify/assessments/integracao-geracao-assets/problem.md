# Problem Definition: Integração de geração de assets com ArtCraft

- **Slug**: integracao-geracao-assets
- **Created**: 2026-11-05
- **Inputs used**: intake.md | research.md | user input only

## Problem Statement

Usuários de agentes IA que usam as skills criativas do ArtCraft (artcraft-skills) não conseguem gerar assets quando o ambiente não expõe comandos de geração via CLI/MCP, mesmo que o Photocraft/ArtCraft app tenha capacidades de edição disponíveis. Isso impede a automação de criação de assets necessária para projetos como Stardew Valley Raízes Vivas.

## Affected Users & Stakeholders

- **Users**: Desenvolvedores/Artistas usando agentes IA com skills artcraft-skills para gerar assets
- **Stakeholders**: Mantenedores do projeto artcraft-skills, desenvolvedores de projetos que dependem das skills para gerar assets

## Goals

- Permitir geração de assets via skills criativas mesmo quando não há comandos de geração explícitos disponíveis
- Descobrir e utilizar comandos de geração reais quando existirem (CLI ou MCP)
- Manter compatibilidade com comportamento existente e contratos `SkillResult`
- Seguir princípios da constituição (não inventar capacidades, orquestrar superfícies reais)

## Non-Goals

- Reimplementar motores de geração de IA
- Criar interface gráfica
- Suportar todos os formatos possíveis
- Modificar o comportamento quando comandos de geração já existem e funcionam

## Success Metrics

- Skills conseguem gerar assets pixel-art simples usando comandos de edição quando não há geração disponível (baseline: atualmente falham com "No image-generation capability found")
- Quando comandos de geração existem, são utilizados corretamente (baseline: desconhecido)
- Todos os testes existentes continuam passando (baseline: 357/357)
- Assets gerados são utilizáveis pelos projetos (formato PNG correto, dimensões adequadas)

## Cost of Inaction

Projetos que precisam gerar assets automaticamente ficam bloqueados, tendo que gerar manualmente com outras ferramentas (como foi feito com ImageMagick neste caso). As skills perdem utilidade prática para geração de assets, contradizendo seu propósito declarado.

## Open Questions

- [NEEDS CLARIFICATION: Quais comandos de geração existem no Photocraft/ArtCraft apps instalados?]
- [NEEDS CLARIFICATION: O `photocraft-cli mcp` expõe ferramentas de geração? Quais?]
- [NEEDS CLARIFICATION: Devemos modificar `CreativeSkill` base class ou apenas skills específicas?]
- [NEEDS CLARIFICATION: Qual o escopo - apenas pixel art simples via edição, ou tentar outros caminhos?]
