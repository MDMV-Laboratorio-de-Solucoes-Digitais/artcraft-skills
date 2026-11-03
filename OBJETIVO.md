# Objetivo do Projeto

## Visão Geral

ArtCraft Skills Suite tem como objetivo construir um ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O projeto visa capacitar artistas, designers e criadores a transformar prompts em *crafting* intencional, proporcionando controle preciso e fluxos compostos em vez de geração *one-shot*.

## Objetivos Principais

### Objetivo Geral
Criar um framework completo e extensível de habilidades para agentes de IA que permita a criação, manipulação e composição de assets criativos através de workflows intencionais e componíveis, seguindo os princípios de "crafting over generating".

### Objetivos Específicos

1. **Padronização e Interoperabilidade** - Seguir rigorosamente o padrão agentskills.io para garantir compatibilidade com Claude Code, Cursor, Codex, Gemini, OpenCode e outros agentes compatíveis.
2. **Composição e Orquestração** - Fornecer abstrações (`BaseSkill`, `SkillComposer`, `DAGOrchestrator`) que permitam compor skills simples em workflows complexos.
3. **Cobertura Criativa Abrangente** - Suportar fluxos para 2D/raster, vetorial, 3D/espacial, vídeo/motion, áudio, documentos/apresentações e CAD/técnico.
4. **Abstração de Provedores** - Manter design vendor-neutral com roteamento multi-provedor (60+ modelos), suportando ambas modalidades de auth da API ArtCraft.
5. **Transparência e Consciência de Custos** - Fornecer estimativa de custos, orquestração assíncrona com polling/webhooks, e tratamento transparente de recursos.
6. **Qualidade e Governança** - Seguir a Constituição v2.0.0 com princípios de controle artístico, composabilidade, performance e extensibilidade sem complexidade desnecessária.
7. **Extensibilidade Comunitária** - Facilitar contribuições através de documentação clara, templates, validação rigorosa e integração com Spec Kit.

## Estado Atual vs Objetivos

### Caminho Percorrido
- **Fundação Completa (100%)**: Schema agentskills.io, validação, descoberta/carregamento, registro no Spec Kit, abstrações core implementadas e testadas.
- **Skills Implementadas**: 12 skills validadas em `core/`, `creative/`, `workflow/` e `integration/`.
- **Composição e Orquestração**: `SkillComposer` e `DAGOrchestrator` funcionais com testes abrangentes (174 testes passando).
- **Workflows Generalizáveis**: Padrões derivados e abstraídos sem branding específico.
- **Governança**: Constituição estabelecida, fluxo Spec Kit executado até convergência.

### O Que Ainda Falta
- **Convergência da Feature**: Finalizar verificação T058-T067 para fechar completamente `001-artcraft-skills-suite`.
- **Expansão de Mídias**: Implementar fases 3-5 (vídeo/motion, áudio/documentos/apresentações, CAD/precisão).
- **Integrações Profundas**: Processamento em lote, templates de projeto e wiring completo com app ArtCraft.
- **Execução Real**: Validação end-to-end com provedores reais e hardening de job orchestration.
- **Implementações Concretas**: Muitos skills ainda são principalmente scaffolds/contratos; necessidade de implementações executáveis completas.

## Métricas de Sucesso

- ✅ **Validação**: 12/12 skills passando (all_valid=True)
- ✅ **Testes**: 174/174 testes passando (unit/integration/contract/property)
- ✅ **Padrão**: Compatível com agentskills.io em múltiplos agentes
- 🔄 **Convergência**: Feature em andamento (48/96 tarefas, ~75% completo)
- ⏳ **Cobertura Completa**: Expansão para todas as mídias criativas planejadas

## Diretrizes de Desenvolvimento

- **Composição Primeiro**: Sempre preferir composição de skills simples sobre soluções monolíticas
- **Controle Artístico**: Manter controle preciso do artista em todo o fluxo
- **Vendor-Neutral**: Abstrair provedores, evitar lock-in
- **Transparente**: Expor custos, modelos e parâmetros claramente
- **Testado**: Seguir TDD quando aplicável, com testes property-based
- **Documentado**: Todo skill deve ter documentação completa
- **Open Source**: Licenças MIT/Apache-2.0, sem branding específico em skills/constituição
