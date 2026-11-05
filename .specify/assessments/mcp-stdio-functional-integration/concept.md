# Concept: Integração MCP funcional (stdio, escopo mínimo)

- **Slug**: mcp-stdio-functional-integration
- **Created**: 2026-11-05
- **Recommended option**: Option A

## Options

### Option A — Cliente MCP stdio mínimo (mock-first) para 1 app + 1–2 operações
- **Sketch**: Um operador/agente usa uma skill criativa como hoje; quando MCP real estiver configurado/disponível, a skill consegue descobrir capacidades expostas pelo app alvo e executar uma ou duas operações suportadas por esse canal, recebendo resultado no mesmo formato de sucesso/erro já esperado. Quando MCP não estiver disponível ou falhar, o comportamento volta ao caminho já funcional (CLI/fallback/degradação), com motivo claro. O valor é provar interoperabilidade MCP fim-a-fim no menor recorte útil, sem mudar a experiência pública das skills.
- **Appetite**: small (dias, se escopo estritamente limitado a 1 alvo + 1–2 operações + testes determinísticos)
- **Trade-offs**: **Ganha** fechamento do gap arquitetural central com risco controlado; valida contrato MCP real em CI sem dependências externas; preserva back-compat e degradação. **Sacrifica** cobertura ampla (apenas um alvo/recorte), recursos MCP avançados e generalização imediata para todos os Craft apps. **Riscos/incertezas**: ferramenta MCP mínima pode não mapear limpo para uma operação “end-to-end” de skill; escolha SDK vs cliente mínimo afeta manutenção/modelo de execução; ordem `auto` pode mudar comportamento observado.
- **Rabbit holes**: generalizar para múltiplos apps/ferramentas antes de provar 1 caso; implementar transporte HTTP/resources/prompts/cancelamento completo; acoplar testes a binários/rede reais; alterar schemas públicos para acomodar MCP.

### Option B — Integração MCP ampla (stdio + mapeamento multi-app/multi-tool)
- **Sketch**: O ecossistema de skills passa a tratar MCP como superfície principal para várias operações criativas em múltiplos apps, com descoberta e execução cobrindo a maior parte das capacidades expostas. Usuários/agentes teriam acesso consistente às tools MCP reais onde disponíveis, reduzindo dependência de heurísticas CLI por operação.
- **Appetite**: large (meses, dado mapeamento por app/tool, testes, compatibilidade e operação)
- **Trade-offs**: **Ganha** interoperabilidade e cobertura MCP muito maiores; alinha melhor com ecossistema MCP maduro. **Sacrifica** velocidade, simplicidade e foco no 80/20; aumenta superfície de bugs/regressão. **Riscos**: diferenças de contrato entre apps (`command_run` engine-oriented vs tools específicas), dependências/ambientes, manutenção alta.
- **Rabbit holes**: catálogo completo de tools por app; normalização semântica universal de resultados; suporte a todos os transportes/capacidades MCP; migração forçada de CLI/fallback.

### Option C — Não construir integração MCP real agora (manter CLI + fallback 006)
- **Sketch**: Nenhuma execução MCP real é adicionada. Skills continuam usando CLI e fallback de edição existentes; MCP permanece documentado como gap/stub.
- **Appetite**: small (dias, apenas higiene documental/expectativas)
- **Trade-offs**: **Ganha** zero risco técnico imediato; evita complexidade de subprocesso/protocolo. **Sacrifica** fechamento do principal gap arquitetural (ROADMAP), validação real da estratégia MCP, e interoperabilidade com agentes/ecossistema MCP. **Riscos**: dívida cresce; futuras integrações podem exigir retrabalho maior; percepção de capacidade MCP pode divergir da realidade.
- **Rabbit holes**: “temporário” que vira permanente sem critério de saída.

## Recommendation

**Option A** — Cliente MCP stdio mínimo (mock-first) para 1 app + 1–2 operações. Ela atende diretamente os goals do problema (descoberta+invocação MCP real no menor recorte, `SkillResult` preservado, back-compat, degradação graciosa, testes determinísticos) com o menor apetite compatível com o 80/20 identificado em intake/research/problem. Option B excede a necessidade atual e concentra riscos de mapeamento entre apps; Option C deixa o gap arquitetural aberto.

Racional ligado a métricas: Option A permite provar `tools/list`+`tools/call` mockados, manter `373/12` verdes, exercitar falhas estruturadas e documentar política/limites — sem exigir rede/credenciais/binários reais.

## Out of Scope (for the recommended option)

- Todos os domínios/apps/tools além do alvo inicial e 1–2 operações mínimas.
- Transportes MCP além de stdio no recorte mínimo; recursos/prompts/HTTP avançado salvo necessidade comprovada.
- Alterações em schemas públicos, remoção de CLI/fallback, ou backend/provedor novo.
- Integração e2e obrigatória contra binário MCP real em CI padrão.
- Hardening amplo não essencial ao recorte (observabilidade completa, generalização multi-app total).

## Assumptions to Validate

- Existe pelo menos um app/entrypoint MCP alvo (candidato: PhotoCraft `photocraft-cli mcp`) com ferramentas estáveis suficientes para 1–2 operações de valor end-to-end.
- As 1–2 operações mínimas podem ser mapeadas para inputs/outputs compatíveis com `SkillResult` sem quebrar schemas públicos.
- A abordagem de dependência (SDK Python MCP oficial ou cliente JSON-RPC mínimo) cabe no modelo atual do repositório e permanece testável de forma determinística.
- A política `auto` (ordem CLI↔MCP↔fallback) pode ser definida sem regressão perceptível para fluxos que hoje dependem de CLI/fallback.
- Timeouts, captura de stderr, tratamento de respostas inválidas e reason codes mínimos são suficientes para operação segura básica do subprocesso MCP no escopo mínimo.
- Mock subprocess/fake MCP server cobre os riscos críticos de protocolo para CI; integração real opcional é viável localmente quando ambiente/binário existir.
