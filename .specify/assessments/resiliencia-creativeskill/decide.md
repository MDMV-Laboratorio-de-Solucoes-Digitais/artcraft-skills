# Decision: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

- **Slug**: resiliencia-creativeskill
- **Created**: 2026-11-04
- **Decision**: GO — implementar Option A

## Decision Rationale

Baseado em pesquisa da feature 004, implementação centralizada em `CreativeSkill` oferece maior confiabilidade com menor esforço, mantendo contratos backward-compatible e beneficiando todos os 5 skills criativos.

## Chosen Option

**Option A** — Resiliência centralizada no CreativeSkill base class
- Retry com exponential backoff + jitter (máx. 3 tentativas)
- Semáforo de concorrência (máx. 3 por instância)
- Aplicado em `_execute_cli` com preservação de metadados

## Conditions / Risks Accepted

- Adicionar threading/sincronização — mitigado por implementação simples e testes
- Possível impacto em mocks — será verificado com testes existentes
- Valores padrão baseados em pesquisa, podem ser ajustados se necessário

## Next Step

Recomendado prosseguir para `/speckit.specify` com escopo: adicionar resiliência ao `skills/core/creative_skill.py` sem alterar contratos `SkillResult` ou schemas.
