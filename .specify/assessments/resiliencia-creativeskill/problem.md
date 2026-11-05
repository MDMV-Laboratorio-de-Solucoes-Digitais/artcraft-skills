# Problem Definition: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

- **Slug**: resiliencia-creativeskill
- **Created**: 2026-11-04
- **Inputs used**: intake.md, research.md

## Problem Statement

Skills criativos que herdam de `CreativeSkill` falham imediatamente em falhas transientes do CLI (timeouts, códigos de saída não-zero) e não possuem limitação de concorrência, tornando fluxos compostos por agentes instáveis e propensos à exaustão de recursos em ambientes de produção.

## Affected Users & Stakeholders

- **Users**: Desenvolvedores/agentes usando skills criativos do ArtCraft Skills Suite — experiência instável em chamadas concorrentes ou sob falhas transientes.
- **Stakeholders**: Mantenedores do repositório — precisam de maior confiabilidade sem aumentar complexidade por skill; usuários de agentes — precisam de execução previsível.

## Goals

- Eliminar falhas desnecessárias por erros transientes do CLI
- Prevenir exaustão de recursos com chamadas concorrentes limitadas
- Manter comportamento backward-compatible e contratos existentes

## Non-Goals

- Implementar integração MCP funcional
- Adicionar observabilidade completa neste escopo
- Criar nova feature ou skill

## Success Metrics

- Redução de falhas transitórias em cenários com timeouts/retries simulados
- Respeito ao limite de concorrência (máx. 3 chamadas simultâneas)
- 351/351 testes existentes permanecem passando
- Todos os 5 skills criativos se beneficiam sem alteração de contrato

## Cost of Inaction

Skills permanecem frágeis em produção, com falhas imediatas em condições transitórias e risco de sobrecarga em execuções paralelas por agentes.

## Open Questions

- [NEEDS CLARIFICATION: Parâmetros exatos de backoff/jitter]
- [NEEDS CLARIFICATION: Escopo de retry (apenas TimeoutExpired ou também exit codes específicos)]
- [NEEDS CLARIFICATION: Semáforo por instância ou compartilhado]
- [NEEDS CLARIFICATION: Configurabilidade via inputs]
