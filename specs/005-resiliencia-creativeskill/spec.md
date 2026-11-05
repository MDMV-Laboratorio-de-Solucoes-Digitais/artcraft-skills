# Feature Specification: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

**Feature Branch**: `005-resiliencia-creativeskill`  
**Created**: 2026-11-04  
**Status**: Draft  
**Input**: Adicionar resiliência ao CreativeSkill base class (retry com exponential backoff + jitter e semáforo de concorrência)

## User Scenarios & Testing

### User Story 1 - Skills resilientes a falhas transientes (Priority: P1)
Como agente de IA usando skills criativos, quero que falhas transientes do CLI (timeouts) sejam automaticamente tentadas novamente com backoff para que execuções intermitentemente falhas não quebrem fluxos compostos.

**Independent Test**: Simular timeout no CLI e verificar que o skill tenta novamente com backoff e eventualmente falha após tentativas ou sucede em retry.

**Acceptance Scenarios**:
1. **Given** CLI retorna timeout na primeira tentativa, **When** skill executa, **Then** faz retry com exponential backoff + jitter e retorna resultado ou falha após máx. 3 tentativas
2. **Given** múltiplas chamadas concorrentes, **When** executadas em paralelo, **Then** são limitadas por semáforo (máx. 3 simultâneas)

### User Story 2 - Backward compatibility (Priority: P1)
Como mantenedor, quero que a resiliência seja aditiva sem alterar contratos existentes para não quebrar skills ou testes atuais.

**Acceptance Scenarios**:
1. **Given** skills existentes, **When** usados, **Then** continuam retornando `SkillResult` com mesma estrutura
2. **Given** testes existentes com mocks, **When** executados, **Then** continuam passando

## Requirements

### Functional Requirements
- **FR-001**: Sistema DEVE adicionar retry com exponential backoff + jitter (máx. 3 tentativas) em `CreativeSkill._execute_cli`
- **FR-002**: Sistema DEVE adicionar semáforo de concorrência (máx. 3 chamadas CLI simultâneas por instância)
- **FR-003**: Retry DEVE aplicar-se a falhas transientes (ex. TimeoutExpired) e opcionalmente a falhas apropriadas
- **FR-004**: Comportamento DEVE ser aditivo, não alterando contratos `SkillResult` ou schemas
- **FR-005**: Todos os 5 skills criativos (image-generate, image-edit, background-remove, image-upscale, mesh-generate) DEVEM se beneficiar automaticamente

### Key Entities
- **CreativeSkill**: Classe base com lógica de resiliência centralizada
- **RetryConfig**: Parâmetros de retry (tentativas, backoff, jitter)
- **ConcurrencyLimiter**: Semáforo por instância

## Success Criteria
- **SC-001**: Skills lidam com timeouts transitórios via retry sem alterar API pública
- **SC-002**: Chamadas concorrentes são limitadas a máx. 3 por instância
- **SC-003**: Todos os 351 testes existentes continuam passando
- **SC-004**: Contratos `SkillResult` permanecem inalterados
- **SC-005**: Implementação centralizada afeta todos os skills herdeiros automaticamente

## Assumptions
- Baseado em pesquisa da feature 004 (itens 2 e 4)
- Valores padrão: 3 tentativas, exponential backoff com jitter, semáforo de 3
- Aplicado em nível de base class para máxima reutilização
