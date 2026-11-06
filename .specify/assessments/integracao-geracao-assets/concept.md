# Concept: Integração de geração de assets com ArtCraft

- **Slug**: integracao-geracao-assets
- **Created**: 2026-11-05
- **Recommended option**: Option A — Descobrir e configurar geração existente + fallback para edição

## Options

### Option A — Descobrir e configurar geração existente + fallback para edição
- **Sketch**: Primeiro tentar descobrir comandos de geração reais no CLI/MCP (configurando `generation_command`/`command_keywords`). Se encontrados e funcionais, usá-los. Se não encontrados, estender `CreativeSkill` para ter um caminho alternativo que use comandos de edição disponíveis (`paint.bucket`, `edit.fill`, `paint.stroke`) para gerar pixel art simples baseado no prompt.
- **Appetite**: small (dias)
- **Trade-offs**: 
  - Vence: Mantém compatibilidade com superfícies reais, segue constituição, resolve problema imediato
  - Sacrifica: Fallback para edição é limitado (apenas pixel art simples, não geração complexa)
- **Rabbit holes**: Descobrir comandos reais pode levar tempo; MCP pode precisar configuração; necessidade de mapear prompts simples para comandos de edição

### Option B — Apenas estender skills para usar edição
- **Sketch**: Ignorar descoberta de geração e sempre usar comandos de edição quando aplicável para pixel art.
- **Appetite**: small (dias)
- **Trade-offs**:
  - Vence: Mais simples, não depende de descobrir comandos de geração
  - Sacrifica: Não usa capacidades reais de geração se existirem; muda propósito da skill
- **Rabbit holes**: Pode conflitar com expectativa de "geração" vs "desenho"; difícil mapear prompts complexos

### Option C — Do nothing
- **Sketch**: Manter comportamento atual (falhar graciosamente quando não há geração).
- **Appetite**: none
- **Trade-offs**:
  - Vence: Zero risco, sem mudanças
  - Sacrifica: Problema persiste, usuários precisam usar ferramentas externas
- **Rabbit holes**: Nenhum

## Recommendation

**Option A** - É a mais alinhada com os objetivos: primeiro usa superfícies reais quando disponíveis (conforme constituição), e adiciona fallback pragmático apenas quando necessário. Mantém comportamento existente quando geração já funciona.

## Out of Scope (for the recommended option)

- Reimplementar motores de geração
- Suportar geração complexa via comandos de edição
- Modificar comportamento quando comandos de geração já existem e funcionam
- Criar nova skill separada (estender as existentes)

## Assumptions to Validate

- [ ] `photocraft-cli` pode ter comandos de geração em algumas configurações (precisa descoberta)
- [ ] MCP server pode expor ferramentas de geração via bridge
- [ ] É possível gerar pixel art simples e útil com `paint.bucket`/`edit.fill`/`paint.stroke`
- [ ] Extensão do `CreativeSkill` não quebra contratos existentes
