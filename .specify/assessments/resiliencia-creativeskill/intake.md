# Idea Intake: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

- **Slug**: resiliencia-creativeskill
- **Created**: 2026-11-04
- **Source**: pasted text
- **Type**: improvement

## Idea (as captured)

> "Adicionar resiliência ao CreativeSkill base class (retry com exponential backoff + jitter e semáforo de concorrência) ao invés de iniciar uma nova feature."
> 
> Torna os skills production-ready, lida com falhas transientes de CLI, previne exaustão de recursos com chamadas concorrentes e segue o que foi pesquisado nas clarificações da feature 004 (research.md itens 2 e 4). Os skills falham imediatamente em timeouts ou códigos de saída não-zero sem resiliência.

## Restated

Adicionar resiliência ao `CreativeSkill` base class com retry (exponential backoff + jitter, máx. 3 tentativas) e semáforo de concorrência (máx. 3 chamadas CLI simultâneas por instância), aplicando-se a todos os skills criativos que herdam dele.

## Origin & Context

- **Raised by**: [NEEDS CLARIFICATION: autor não especificado]
- **Trigger**: Análise do estado do repositório após convergência das features 001/003/004; gaps identificados na pesquisa da feature 004 nunca implementados.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: Valores exatos de backoff/jitter além de "exponential backoff + jitter"?]
- [NEEDS CLARIFICATION: Retry aplica-se apenas a TimeoutExpired ou também a falhas por exit code não-zero / erros específicos?]
- [NEEDS CLARIFICATION: O semáforo deve ser por instância ou compartilhado?]
- [NEEDS CLARIFICATION: Há necessidade de tornar configurável via inputs/params?]
- [NEEDS CLARIFICATION: Impacto em testes existentes que fazem mock precisa de ajustes?]
