# Objetivo do Projeto

## Visão Geral

ArtCraft Skills Suite tem como objetivo construir um ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O projeto visa capacitar artistas, designers e criadores a transformar prompts em *crafting* intencional, proporcionando controle preciso e fluxos compostos em vez de geração *one-shot*.

As skills não reimplementam motores de geração: elas expõem, de forma composável e governada, as capacidades reais dos apps ArtCraft (PhotoCraft, PdfCraft e os demais "Crafting Apps" Rust da organização `storytold`), via suas superfícies de **CLI** (`photocraft-cli`, 500+ comandos) e **MCP server**, além da AI studio da ArtCraft (60+ modelos de imagem/vídeo/áudio/3D/mundos). O repositório é a *camada de skill/agente* sobre essas superfícies.

## Estado Atual (Verificado — 2026-11-05)

**Branch**: `dev`. Apenas `dev` e `main` remotos/locais.  
**Convergência Spec Kit (escopo definido):** Features **001, 003, 004, 005, 006** convergidas com evidência em `specs/*/tasks.md` e commits em `dev`.  
**Qualidade verificada:** **373/373 testes passando** (`python -m pytest -q`), **12/12 skills validadas** (`python scripts/validate_all_skills.py`).

### O que funciona (verificado)
- Schema/validação/descoberta/carregamento de skills (agentskills.io), core abstractions, composição (`SkillComposer`) e DAG (`DAGOrchestrator`).
- Adapter compartilhado `skills/core/artcraft_app_client.py` com discovery/invocação CLI, reason codes e fallback de edição (`generate_via_editing_commands`) quando geração não está disponível.
- `CreativeSkill` com resiliência: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)`.
- 5 skills criativos Python executáveis: `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`; `scene-composition` executável.
- Workflows generalizáveis (policy-redaction, structured-packager, dag-orchestrator, evidence-audit).

### Gap principal restante
- **Integração MCP funcional (real transport)**: contratos/descoberta parcial existem, mas execução MCP real ainda é majoritariamente stub. CLI + fallback já funcionam. **Próximo 80/20:** MCP stdio mínimo viável (`tools/list` + `tools/call` para operações suportadas, mock-first, back-compat com CLI/fallback e contratos `SkillResult`).

## O que ainda falta
- Implementar MCP stdio funcional mínimo e testes determinísticos.
- Expandir domínios (vídeo/motion, áudio/docs/apresentações, CAD/precisão) após integração MCP estável.
- Batch processing, project templates e integrações profundas por app (Phase 6).
- Observabilidade/logging estruturado e métricas RED integradas.

## O que este projeto NÃO faz
- Não reimplementa modelos/provedores de geração; orquestra superfícies reais ArtCraft (CLI/MCP/AI studio).
- Não substitui os apps ArtCraft; é a camada de skill/agente sobre eles.
- Não gera via backend próprio; depende das capacidades expostas pelos apps.

## Métricas de Sucesso (atuais)
- ✅ 12/12 skills validadas
- ✅ 373/373 testes passando
- ✅ Features 001/003/004/005/006 convergidas
- ⏳ MCP funcional (stdio mínimo) — próximo foco
