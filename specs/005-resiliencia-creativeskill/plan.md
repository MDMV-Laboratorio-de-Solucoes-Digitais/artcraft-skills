# Implementation Plan: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

**Branch**: `005-resiliencia-creativeskill` | **Date**: 2026-11-04 | **Spec**: specs/005-resiliencia-creativeskill/spec.md
**Input**: Feature specification from `/specs/005-resiliencia-creativeskill/spec.md`

## Summary

Adicionar resiliência ao `CreativeSkill` base class com retry (exponential backoff + jitter, máx. 3 tentativas) e semáforo de concorrência (máx. 3 chamadas CLI simultâneas por instância). Mudança centralizada, aditiva, sem alterar contratos `SkillResult`.

## Technical Context

**Language/Version**: Python 3.x  
**Primary Dependencies**: Python standard library (`threading`, `time`, `random`)  
**Storage**: N/A  
**Testing**: pytest  
**Target Platform**: Linux  
**Project Type**: Library (skills core)  
**Constraints**: Sem alteração de API pública, manter backward compatibility, não quebrar 351 testes existentes  
**Scale/Scope**: Afeta `skills/core/creative_skill.py` e beneficia todos os skills herdeiros

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] I. Crafting Over Generating - não altera filosofia
- [x] II. Artist-Centric Design - melhora confiabilidade
- [x] III. Open Source, Vendor-Neutral, Interoperable - sem mudanças
- [x] IV. Composability and Modularity - centralizado na base class
- [x] V. Performance and Native Execution - adiciona controle de concorrência
- [x] VI. Quality Through Intentional Craft - melhora robustez
- [x] VII. Transparency, Reproducibility, Cost Awareness - mantém metadados
- [x] VIII. Extensibility Without Unnecessary Complexity - simples e aditivo

## Project Structure

### Source Code
```text
skills/
├── core/
│   └── creative_skill.py        # MODIFY: adicionar retry + semáforo
```

## Complexity Tracking
Sem violações.

## Design Decisions

1. **Retry**: Em `_execute_cli`, capturar `subprocess.TimeoutExpired` e códigos de saída não-zero, tentar até 3 vezes com `time.sleep(base * 2^attempt + jitter)`
2. **Semáforo**: `threading.BoundedSemaphore(3)` por instância, adquirido antes da chamada CLI
3. **Backward compatibility**: Comportamento padrão idêntico quando não há falhas; mocks existentes continuam funcionando
4. **Metadados**: Preservar `timeout_s`, `exit_code`, `command` em falhas finais
