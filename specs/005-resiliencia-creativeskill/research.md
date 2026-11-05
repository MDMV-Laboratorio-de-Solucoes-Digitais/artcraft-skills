# Research: Resiliência ao CreativeSkill

## Decision
Adicionar retry com exponential backoff + jitter e semáforo de concorrência em `skills/core/creative_skill.py`.

## Rationale
- Segue recomendações da feature 004 (research.md itens 2 e 4)
- Padrão industry-standard (AWS, Google SRE)
- Mudança centralizada afeta todos os skills criativos
- Baixo risco, alto impacto

## Alternatives Considered
1. Retry por skill individual - mais trabalho, duplicação
2. Retry no adapter - menos granular, afeta outros usos
3. Não fazer - mantém fragilidade

## Implementation Notes
- Usar `threading` (stdlib, já disponível)
- Jitter com `random.uniform`
- Backoff base recomendado: 0.5s ou 1s com fator 2
- Retry em TimeoutExpired e possivelmente em falhas temporárias
