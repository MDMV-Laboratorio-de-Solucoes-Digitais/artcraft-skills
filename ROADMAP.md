# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development — empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode, and others) and embody ArtCraft's philosophy of "turning prompting into crafting" — build before generating, with precise control and composition-first workflows.

Skills are consumed by agents that drive the real ArtCraft creative apps (PhotoCraft, PdfCraft, and the rest of the 13–16 Rust "Crafting Apps" in the `storytold` org) through their **CLI** (`photocraft-cli`, 500+ commands) and **MCP server** surfaces, plus ArtCraft's AI studio (60+ models across image/video/audio/3D/worlds). There is no separate generation backend in this repo — it is the skill/agent layer on top of those surfaces.

## Current State (Verified — 2026-11-04)

- **Branch**: `dev` (commit `14530b2`). Local/remote branches cleaned to only `dev` and `main`. All PRs merged.
- **Feature 001** (`001-artcraft-skills-suite`): Assessment complete (**GO**), full lifecycle executed through implement. **68/98 tasks complete (~69%)**; analyze/converge pending.
- **Feature 003** (`003-shared-cli-mcp-adapter`): **Converged**. Shared adapter `skills/core/artcraft_app_client.py` (9 functions, reason codes, `__version__=0.2.0`), image-generate refactored with equivalence verified.
- **Feature 004** (`004-implement-python-creative-skills`): **Complete and converged**. Added `skills/core/creative_skill.py` and Python implementations for `image-edit`, `background-remove`, `image-upscale`, `mesh-generate` with full test coverage (47 new tests).
- **Constitution**: `.specify/memory/constitution.md` v2.0.0 in effect.
- **Skills**: **12/12 validated** (`python scripts/validate_all_skills.py` → `all_valid=True`). **5 creative skills** have executable Python implementations.
- **Tests**: **351 passing** (`python -m pytest -q` → `351 passed`), no regressions.
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `docs/architecture.md`, `AGENTS.md`.
- **Tooling**: CodeGraph synced; Archify artifacts updated.

## Progress Summary

**Overall**: **~82% complete** (Foundation + core abstractions + shared adapter + all 4 creative skills implemented with tests + composition/orchestration + generalizable workflows; 351 tests passing, 12/12 skills validated; features 003 and 004 converged; feature 001 at ~69%).

**Completed (✓)**:
- **Phase 0 Foundation**: 100% complete (schema, validation, loader, registry, core abstractions, docs framework, test infrastructure)
- **Feature 003**: Full lifecycle complete and **converged**
- **Feature 004**: Full lifecycle complete and **converged** with tests
- **US1-US5 foundation (001)**: Core abstractions, composition/DAG, generalizable workflows implemented
- **Shared adapter (003)**: Complete with CLI/MCP support, reason codes, graceful degradation
- **Python creative skills (004)**: All 4 skills implemented with `CreativeSkill` base class and comprehensive tests
- **Governance**: Constitution v2.0.0 established
- **Repository hygiene**: Clean branch structure (dev/main only), all PRs merged

**In Progress**:
- **Feature 001 convergence/verification**: Completing remaining tasks and preparing for analyze/converge

## Roadmap Phases

### Phase 0: Foundation (Q4 2026) — **100% Complete**
- [x] Skill Schema & Structure (agentskills.io compliant)
- [x] Core Utilities (credentials, adapters, router, assets, jobs, costs, composer, DAG, context, base skill, shared adapter)
- [x] Documentation Framework
- [x] Testing Infrastructure (351 tests passing)

### Phase 1: Image & 2D Creative Skills (Q1 2027) — **100% Complete**
- [x] Image Generation (`image-generate/skill.py`)
- [x] Image Editing & Compositing (`image-edit/skill.py`)
- [x] Background Removal & Matting (`background-remove/skill.py`)
- [x] Upscaling & Enhancement (`image-upscale/skill.py`)
- [ ] Vector & Illustration (future)
- [ ] Style Transfer & Consistency (future)

### Phase 2: 3D, Spatial & Environment (Q1-Q2 2027) — **~50% Complete**
- [x] 3D Scene Composition (workflow scaffold)
- [x] Image to 3D (workflow scaffold + `mesh-generate/skill.py`)
- [ ] 3D Asset Manipulation
- [ ] Environment Generation
- [ ] Texture Creation
- [ ] Character Posing

### Phase 3: Video, Motion & Animation (Q2 2027) — **0% Complete**
- [ ] Image-to-Video, Video Generation, Video Editing, Motion Graphics, Storyboarding

### Phase 4: Audio, Documents & Presentations (Q2-Q3 2027) — **0% Complete**
- [ ] Audio Generation, Voice & Dialogue, Presentation Design, Document Layout, Technical Illustration

### Phase 5: CAD, Precision & Technical Design (Q3 2027) — **0% Complete**
- [ ] CAD Assistance, Technical Documentation, Parametric Design, BOM & Specification, Manufacturing Prep

### Phase 6: Workflow Orchestration & Integration (Q3-Q4 2027) — **~90% Complete**
- [x] Multi-Asset Pipelines (orchestrator, DAG, composer)
- [x] Skill Composition Tools
- [x] Generalizable Workflows (policy-redaction, structured-packager, dag-orchestrator, evidence-audit)
- [x] ArtCraft App Integration Foundation (shared adapter)
- [ ] Batch Processing, Project Templates, Deep App Integrations

## Immediate Next Steps
1. **Complete Feature 001 convergence** - Run analyze/converge, address remaining verification tasks
2. **Harden resilience** - Add retry with backoff+jitter, rate limiting, concurrency control
3. **Functional MCP integration** - Replace stubs with real MCP transport where needed
4. **Expand coverage** - Add missing tests, complete remaining 001 tasks

## Success Metrics
- **Skills Validated**: 12/12 (100%)
- **Tests Passing**: 351/351 (100%)
- **Feature 003**: Converged ✓
- **Feature 004**: Converged ✓
- **Feature 001**: ~69% complete
- **Creative Skills Python**: 5/5 implemented ✓
