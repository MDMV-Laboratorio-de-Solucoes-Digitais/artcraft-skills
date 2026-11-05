# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development — empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode, and others) and embody ArtCraft's philosophy of "turning prompting into crafting" — build before generating, with precise control and composition-first workflows.

Skills are consumed by agents that drive the real ArtCraft creative apps (PhotoCraft, PdfCraft, and the rest of the 13–16 Rust "Crafting Apps" in the `storytold` org) through their **CLI** (`photocraft-cli`, 500+ commands) and **MCP server** surfaces, plus ArtCraft's AI studio (60+ models across image/video/audio/3D/worlds). There is no separate generation backend in this repo — it is the skill/agent layer on top of those surfaces.

## Current State (Verificado — 2026-11-05)

- **Branch**: `dev`. Local/remote branches cleaned to only `dev` and `main`.
- **Feature 001** (`001-artcraft-skills-suite`): **Convergida (escopo clarificado)**. `/speckit.analyze` + `/speckit.converge` executados; T098–T109 fechados com evidência (`3e0d28e`). Inclui `scene-composition` executável, webhook handling surface no `JobOrchestrator`, clarificações FR-004/FR-005/FR-006/SC-002 e calibração de custo para subconjunto suportado.
- **Feature 003** (`003-shared-cli-mcp-adapter`): **Convergida**. Shared adapter `skills/core/artcraft_app_client.py` com `generate_via_editing_commands()`, reason codes, `__version__=0.2.0`.
- **Feature 004** (`004-implement-python-creative-skills`): **Convergida**. `skills/core/creative_skill.py` + implementações Python para `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`.
- **Feature 005** (`005-resiliencia-creativeskill`): **Convergida**. Retry máx. 3 com exponential backoff + jitter e `BoundedSemaphore(3)` em `CreativeSkill._execute_cli`; FR-001..FR-005/SC-001..SC-005 satisfeitos (`7962298`).
- **Feature 006** (`006-integracao-geracao-assets`): **Convergida**. Discovery-first com fallback para comandos de edição (degradação graciosa), PR #109 mergeado.
- **Constitution**: `.specify/memory/constitution.md` v2.0.0 em vigor.
- **Skills**: **12/12 validated** (`python scripts/validate_all_skills.py` → `all_valid=True`). **5 creative skills** com implementações Python executáveis.
- **Tests**: **373 passing** (`python -m pytest -q` → `373 passed`), sem regressões.
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `docs/architecture.md`, `AGENTS.md`, `OBJETIVO.md`, `ROADMAP.md`.

## Progress Summary

**Overall**: **~90% complete** (Foundation + core abstractions + shared adapter + fallback + resiliência + 5 creative skills + composição/DAG + workflows generalizáveis; 373 tests passing, 12/12 skills validated; features 001/003/004/005/006 convergidas no escopo definido).

**Completed (✓)**:
- **Phase 0 Foundation**: 100% (schema, validation, loader, registry, core abstractions, docs, test infrastructure)
- **Features 001, 003, 004, 005, 006**: Convergidas com evidência
- **Shared adapter**: CLI/MCP discovery hooks, reason codes, graceful degradation, fallback de edição
- **Resiliência**: retry + backoff + jitter + semáforo no `CreativeSkill`
- **Python creative skills**: `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`
- **Composition/orchestration**: `SkillComposer`, `DAGOrchestrator`, `AssetContext`, workflows generalizáveis
- **Repository hygiene**: `dev`/`main`, PRs mergeados, testes/validação verdes

**Gap principal restante**:
- **Integração MCP funcional (real transport)**: hoje majoritariamente stubs/contratos e descoberta parcial; CLI + fallback já funcionam. Próximo foco: **MCP stdio mínimo viável** (discovery `tools/list` + `tools/call` para operações suportadas, mock-first, back-compat).

## Roadmap Phases

### Phase 0: Foundation — **100% Complete**
- [x] Skill Schema & Structure (agentskills.io compliant)
- [x] Core Utilities (credentials, adapters, router, assets, jobs, costs, composer, DAG, context, base skill, shared adapter)
- [x] Documentation Framework
- [x] Testing Infrastructure (373 tests passing)

### Phase 1: Image & 2D Creative Skills — **100% Complete (escopo atual)**
- [x] Image Generation (`image-generate/skill.py`) with fallback
- [x] Image Editing & Compositing (`image-edit/skill.py`)
- [x] Background Removal & Matting (`background-remove/skill.py`)
- [x] Upscaling & Enhancement (`image-upscale/skill.py`)
- [ ] Vector & Illustration (future)
- [ ] Style Transfer & Consistency (future)

### Phase 2: 3D, Spatial & Environment — **~60% Complete**
- [x] 3D Scene Composition (workflow scaffold + `scene-composition` executável)
- [x] Image to 3D (`mesh-generate/skill.py`)
- [ ] 3D Asset Manipulation
- [ ] Environment Generation
- [ ] Texture Creation
- [ ] Character Posing

### Phase 3: Video, Motion & Animation — **0% Complete**
- [ ] Image-to-Video, Video Generation, Video Editing, Motion Graphics, Storyboarding

### Phase 4: Audio, Documents & Presentations — **0% Complete**
- [ ] Audio Generation, Voice & Dialogue, Presentation Design, Document Layout, Technical Illustration

### Phase 5: CAD, Precision & Technical Design — **0% Complete**
- [ ] CAD Assistance, Technical Documentation, Parametric Design, BOM & Specification, Manufacturing Prep

### Phase 6: Workflow Orchestration & Integration — **~92% Complete**
- [x] Multi-Asset Pipelines (orchestrator, DAG, composer)
- [x] Skill Composition Tools
- [x] Generalizable Workflows
- [x] ArtCraft App Integration Foundation (shared adapter with fallback + resilience)
- [ ] **Functional MCP stdio integration (minimal viable)** — próximo 80/20
- [ ] Batch Processing, Project Templates, Deep App Integrations

## Immediate Next Steps
1. **Assess/Specify MCP stdio funcional (mínimo viável)** — intake → research/define/shape/decide → specify: transport stdio, `tools/list` + `tools/call`, normalização para `SkillResult`, testes mock-first, preservação de CLI/fallback/back-compat.
2. **Implementar MCP stdio mínimo** com cobertura determinística (unit/contract/property/characterization conforme aplicável).
3. **Atualizar documentação/contratos** do adapter para refletir MCP real vs stubs.
4. Expandir domínios criativos (fases 3–5) somente após integração MCP estável.

## Success Metrics
- **Skills Validated**: 12/12 (100%)
- **Tests Passing**: 373/373 (100%)
- **Features 001/003/004/005/006**: Convergidas ✓
- **Creative Skills Python**: 5/5 implementados ✓
- **MCP funcional (stdio, mínimo)**: Pendente (próximo foco)
