# Idea Research: Integração de geração de assets com ArtCraft

- **Slug**: integracao-geracao-assets
- **Created**: 2026-11-05
- **Evidence confidence (overall)**: high

## Users & Demand

- **Artistas/criadores usando agentes IA precisam gerar assets** diretamente via skills sem sair do fluxo do agente. [source: OBJETIVO.md | cited] (confidence: high)
- **Projetos MDMV precisam de assets pixel-art** (compost, bins, etc.) gerados de forma automatizada via skills. [source: Briefings em stardew-raizes-vivas/specs/*/briefings | cited] (confidence: high)
- **Skills criativas já existem mas falham ao tentar gerar** - tentativas com `image-generate` skill retornam "No image-generation capability found". [source: Teste prático no ambiente | cited] (confidence: high)

## Prior Art

- **Skills criativas implementadas** em `skills/creative/` (image-generate, image-edit, background-remove, image-upscale, mesh-generate) com `CreativeSkill` base class. [source: Repositório artcraft-skills | cited] (confidence: high)
- **Adapter compartilhado** `skills/core/artcraft_app_client.py` com descoberta CLI, resolução de comandos, seleção de modo CLI/MCP. [source: Repositório artcraft-skills | cited] (confidence: high)
- **photocraft-cli instalado** (v0.20.1) com comandos de edição (`paint.bucket`, `edit.fill`, `paint.stroke`) mas sem comandos de geração de IA. [source: Verificação no ambiente | cited] (confidence: high)
- **MCP server disponível** via `photocraft-cli mcp` - potencial interface para geração. [source: photocraft-cli help | cited] (confidence: high)

## Market & Context

- **Padrão agentskills.io** adotado - skills devem ser interoperáveis entre agentes. [source: OBJETIVO.md, constitution v2.0.0 | cited] (confidence: high)
- **ArtCraft apps** (PhotoCraft, etc.) têm superfícies CLI/MCP reais. Skills devem orquestrar essas superfícies, não reimplementar geração. [source: OBJETIVO.md | cited] (confidence: high)
- **Geração via IA** pode estar disponível através de comandos específicos ou via MCP server - precisa ser descoberto. [source: ASSUMPTION] (confidence: medium)

## Data & Constraints

- **photocraft-cli v0.20.1** no ambiente tem apenas comandos de documento/edição, sem `generate`/`ai`/`image.generate`. [source: `photocraft-cli commands` | cited] (confidence: high)
- **Adapter já implementa lógica correta** - falha graciosamente quando não encontra comandos de geração. [source: artcraft_app_client.py, creative_skill.py | cited] (confidence: high)
- **Skills seguem princípios constitucionais** - não devem inventar capacidades, devem orquestrar superfícies reais. [source: Constitution v2.0.0 | cited] (confidence: high)
- **Necessário manter compatibilidade** com contratos existentes (`SkillResult`). [source: BaseSkill | cited] (confidence: high)

## Evidence Against the Idea

- **Pode não haver interface de geração disponível** neste ambiente específico - o Photocraft instalado pode não ter geração habilitada ou configurada. [source: Teste prático | cited] (confidence: high)
- **Estender para usar comandos de edição** muda o propósito da skill - `image-generate` deveria gerar, não desenhar pixel por pixel. [source: ASSUMPTION] (confidence: medium)
- **photocraft-cli MCP** pode não expor ferramentas de geração - precisa verificação. [source: ASSUMPTION] (confidence: medium)
- **Complexidade vs valor** - gerar pixel art simples com `paint.bucket`/`paint.stroke` é possível mas trabalhoso e limitado comparado a geração real. [source: ASSUMPTION] (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: Quais comandos de geração existem no Photocraft/ArtCraft apps instalados?]
- [NEEDS CLARIFICATION: O `photocraft-cli mcp` expõe ferramentas de geração? Quais?]
- [NEEDS CLARIFICATION: Há configuração/API keys para geração habilitada?]
- [NEEDS CLARIFICATION: Devemos modificar `CreativeSkill` base class para suportar caminho alternativo de edição, ou apenas as skills específicas?]
- [NEEDS CLARIFICATION: Qual o comportamento esperado quando não há geração disponível - falhar graciosamente (atual) ou tentar via edição?]

## Sources

- `skills/creative/*/skill.py` (host: local, policy: allowlisted)
- `skills/core/artcraft_app_client.py`, `skills/core/creative_skill.py` (host: local, policy: allowlisted)
- `.specify/memory/constitution.md` (host: local, policy: allowlisted)
- `OBJETIVO.md`, `ROADMAP.md` (host: local, policy: allowlisted)
- `photocraft-cli commands` (host: local, policy: allowlisted)
- Briefings em `/home/luis/development/stardew-raizes-vivas/specs/*/briefings/` (host: local, policy: allowlisted)
