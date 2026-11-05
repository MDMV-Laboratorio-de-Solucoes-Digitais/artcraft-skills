# Problem Definition: Integração MCP funcional (stdio, escopo mínimo)

- **Slug**: mcp-stdio-functional-integration
- **Created**: 2026-11-05
- **Inputs used**: intake.md | research.md | user input

## Problem Statement

Desenvolvedores e agentes que consomem o ArtCraft Skills Suite não conseguem, de forma confiável e verificável, descobrir e invocar capacidades reais expostas por servidores MCP dos apps ArtCraft (além do caminho CLI e do fallback de edição). Como resultado, o principal gap arquitetural restante do roadmap impede interoperabilidade plena com o ecossistema MCP, mantém parte da integração em stubs/contratos parciais e aumenta o risco de divergência entre capacidades declaradas e capacidades executáveis.

## Affected Users & Stakeholders

- **Users**: Mantenedores/contribuidores do ArtCraft Skills Suite — precisam implementar, testar e evoluir skills com comportamento previsível entre CLI/MCP/fallback sem quebrar contratos existentes.
- **Users**: Operadores de agentes de IA (Claude Code, Cursor, Codex, Gemini, OpenCode e compatíveis agentskills.io) — precisam que skills criativas usem superfícies reais disponíveis, com degradação graciosa e erros acionáveis quando MCP não estiver disponível.
- **Users**: Integradores dos apps ArtCraft (PhotoCraft/PdfCraft/outros Craft apps) — [NEEDS CLARIFICATION: quais apps/entrypoints são alvo inicial?] — precisam de um mapeamento claro entre ferramentas MCP expostas e operações suportadas pelas skills.
- **Stakeholders**: Mantenedores do roadmap/projeto ArtCraft Skills — decidem prioridade, escopo e critérios de aceite; interessados em fechar o gap MCP com menor esforço e risco.
- **Stakeholders**: Ecossistema ArtCraft/storytold — interessado em que agentes consumam capacidades reais dos apps sem reimplementar backends. [NEEDS CLARIFICATION: ownership/prioridade formal do lado dos apps].

## Goals

- Permitir, no escopo mínimo, descoberta e invocação funcional de ferramentas MCP reais via transporte stdio para operações suportadas, com normalização para `SkillResult`.
- Preservar contratos públicos (`SkillResult`, schemas/inputs existentes) e back-compat com CLI + fallback de edição.
- Garantir degradação graciosa e reason codes/mensagens claras quando MCP não estiver disponível, falhar, ou a ferramenta não existir.
- Viabilizar validação determinística em CI/local sem credenciais reais nem binários MCP reais obrigatórios (mock-first), com caminho opcional para integração real quando disponível.
- Reduzir incerteza arquitetural: tornar explícita a política de seleção/ordem CLI↔MCP↔fallback e o mapeamento mínimo de ferramentas MCP suportadas.

## Non-Goals

- Cobrir todos os domínios criativos (vídeo, áudio, CAD, apresentações, etc.) ou todas as tools MCP de todos os apps ArtCraft nesta etapa.
- Reimplementar modelos/provedores de geração ou criar backend novo; apenas orquestrar superfícies existentes.
- Exigir credenciais reais, serviços externos pagos, ou binários MCP reais em testes padrão do repositório.
- Suportar todos os transportes MCP (ex.: Streamable HTTP completo, recursos avançados) no escopo mínimo; foco em stdio.
- Alterar schemas públicos das skills ou remover o caminho CLI/fallback existente.
- Resolver hardening amplo fora do escopo mínimo (ex.: observabilidade RED completa, batching/templates, todos os casos de segurança de produção) além do necessário para operação segura básica do subprocesso MCP.

## Success Metrics

- **MCP mínimo funcional:** pelo menos 1 app/entrypoint MCP alvo e 1–2 operações suportadas executam `tools/list` + `tools/call` via stdio em testes determinísticos mockados, com saída normalizada para `SkillResult`. (baseline: hooks MCP stubados; execução MCP real ausente)
- **Back-compat:** suíte de testes existente permanece verde e skills validadas (`>=373 passed`, `12/12 validated` ou maior, sem regressões). (baseline: 373/12 em 2026-11-05)
- **Degradação graciosa:** cenários de MCP indisponível, timeout, resposta inválida, ferramenta ausente e erro de ferramenta retornam falha estruturada/razão adequada sem quebrar fluxo CLI/fallback quando aplicável. (baseline: cobertura parcial/stub)
- **Determinismo CI:** testes MCP mínimos rodam sem rede/credenciais/binários reais obrigatórios. (baseline: integração MCP real não verificável deterministicamente)
- **Clareza operacional:** documentação/contrato registram alvo inicial, ferramentas mínimas, ordem de seleção e limitações. (baseline: [NEEDS CLARIFICATION: documentação MCP funcional insuficiente])

## Cost of Inaction

O repositório continuará com o principal gap arquitetural aberto: MCP permanecerá majoritariamente stub/descoberta parcial, limitando a validação real da estratégia CLI/MCP dos apps ArtCraft e a interoperabilidade com o ecossistema MCP. Novas features criativas (fases 3–5) terão maior risco e custo por dependerem de uma base de integração instável/incompleta. Decisões de seleção CLI↔MCP↔fallback permanecerão implícitas, aumentando divergência entre comportamento esperado e executável.

## Open Questions

- [NEEDS CLARIFICATION: Qual app/entrypoint MCP é o alvo inicial (ex.: PhotoCraft `photocraft-cli mcp` headless)?]
- [NEEDS CLARIFICATION: Quais 1–2 ferramentas/operações MCP mínimas devem ser suportadas primeiro e qual critério define “valor end-to-end”?]
- [NEEDS CLARIFICATION: Adotar SDK Python MCP oficial (`mcp`) como dependência ou implementar cliente JSON-RPC stdio mínimo?]
- [NEEDS CLARIFICATION: Qual a ordem de seleção em modo `auto` (CLI→MCP→fallback, MCP→CLI→fallback, ou configurável)?]
- [NEEDS CLARIFICATION: Quais controles mínimos de segurança/operabilidade são obrigatórios (timeouts, cancelamento, stderr capture, roots allowlist, reason codes)?]
- [NEEDS CLARIFICATION: Haverá suíte opcional de integração contra servidor/binário MCP real, e em que ambiente?]
- [NEEDS CLARIFICATION: Quem é o owner/stakeholder formal para priorização e aceite desta integração?]
