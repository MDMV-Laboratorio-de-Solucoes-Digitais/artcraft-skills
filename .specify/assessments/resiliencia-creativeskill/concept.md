# Concept: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

- **Slug**: resiliencia-creativeskill
- **Created**: 2026-11-04
- **Recommended option**: Option A — Resiliência centralizada no CreativeSkill base class

## Options

### Option A — Resiliência centralizada no CreativeSkill base class
- **Sketch**: Adicionar retry com exponential backoff + jitter (máx. 3 tentativas) e semáforo de concorrência (máx. 3 por instância) diretamente em `skills/core/creative_skill.py`. Todos os skills criativos herdam e se beneficiam automaticamente sem alterar seus contratos.
- **Appetite**: small (1-2 horas)
- **Trade-offs**: 
  - Wins: Mudança centralizada, backward-compatible, afeta todos os 5 skills, segue pesquisa da feature 004
  - Sacrifices: Adiciona threading/sincronização, precisa testar com mocks
- **Rabbit holes**: Comportamento em testes com mocks, thread-safety, preservação de metadados em retries

### Option B — Resiliência por skill
- **Sketch**: Implementar lógica de retry/semaphore em cada skill individual.
- **Appetite**: medium (3-6 horas)
- **Trade-offs**:
  - Wins: Mais granular
  - Sacrifices: Duplicação de código, risco de inconsistência, maior manutenção
- **Rabbit holes**: Sincronização entre skills, difícil garantir comportamento uniforme

### Option C — Do nothing
- **Sketch**: Manter comportamento atual (falha imediata).
- **Appetite**: small
- **Trade-offs**:
  - Wins: Zero esforço
  - Sacrifices: Skills permanecem frágeis em produção, falhas transitórias não são tratadas
- **Rabbit holes**: Nenhum técnico, mas bloqueia uso confiável em produção

## Recommendation

**Option A** — Alinhado aos objetivos (confiabilidade, prevenção de exaustão), segue exatamente o que foi pesquisado na feature 004, mudança centralizada e de baixo risco. Mantém contratos existentes e não quebra testes.

## Out of Scope (for the recommended option)

- Integração MCP funcional
- Observabilidade completa (logging estruturado/métricas)
- Nova feature ou skill
- Mudanças em contratos `SkillResult`

## Assumptions to Validate

- Os valores padrão (3 retries, backoff+jitter, semáforo 3) são suficientes
- Retry deve cobrir timeouts e possivelmente alguns exit codes
- Semáforo por instância é apropriado vs compartilhado
