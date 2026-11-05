# Feature Specification: Integração de geração de assets com ArtCraft

**Feature Branch**: `006-integracao-geracao-assets`  
**Created**: 2026-11-05  
**Status**: Draft  
**Input**: User description from assessment (go verdict)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descobrir comandos de geração reais (Priority: P1)

Como agente de IA usando as skills criativas do ArtCraft, quero que as skills descubram e utilizem comandos de geração reais quando disponíveis via CLI ou MCP para gerar assets corretamente.

**Why this priority**: Essencial para usar as superfícies reais dos apps ArtCraft conforme projetado.

**Independent Test**: Com comandos de geração disponíveis, a skill usa o comando correto e gera o asset.

**Acceptance Scenarios**:

1. **Given** photocraft-cli expõe comandos de geração, **When** skill é invocada com prompt, **Then** descobre e usa o comando correto
2. **Given** MCP server expõe ferramenta de geração, **When** configurado, **Then** usa via MCP

### User Story 2 - Fallback para comandos de edição (Priority: P1)

Como usuário em ambiente sem comandos de geração, quero que as skills consigam gerar pixel art simples usando comandos de edição disponíveis (paint.bucket, edit.fill, paint.stroke) para não ficar completamente bloqueado.

**Why this priority**: Permite uso prático das skills mesmo sem interface de geração completa.

**Independent Test**: Sem comandos de geração, skill gera pixel art simples baseado em prompt.

**Acceptance Scenarios**:

1. **Given** sem comandos de geração disponíveis, **When** skill chamada com prompt simples de pixel art, **Then** cria imagem usando comandos de edição
2. **Given** fallback usado, **When** sucesso, **Then** retorna SkillResult com imagem gerada

## Requirements

### Functional Requirements

- **FR-001**: Sistema DEVE tentar descobrir comandos de geração reais primeiro (CLI e MCP)
- **FR-002**: Sistema DEVE permitir configurar `generation_command` ou `command_keywords` via inputs
- **FR-003**: Quando não houver comandos de geração, sistema DEVE oferecer fallback usando comandos de edição (`paint.bucket`, `edit.fill`, `paint.stroke`) para pixel art simples
- **FR-004**: Fallback DEVE respeitar dimensões solicitadas e criar arquivo PNG válido
- **FR-005**: Comportamento DEVE manter compatibilidade com contratos `SkillResult` existentes
- **FR-006**: Sistema DEVE falhar graciosamente se nem geração nem edição forem possíveis

### Success Criteria

- **SC-001**: Comandos de geração reais são descobertos e utilizados quando disponíveis
- **SC-002**: Pixel art simples é gerado via fallback quando não há geração disponível
- **SC-003**: Todos os 357 testes existentes continuam passando
- **SC-004**: Contratos `SkillResult` permanecem inalterados
- **SC-005**: Assets gerados são arquivos PNG válidos nas dimensões solicitadas

## Assumptions

- Comandos de edição do photocraft-cli são suficientes para pixel art básico
- Prompts simples podem ser mapeados para operações de pintura básicas
