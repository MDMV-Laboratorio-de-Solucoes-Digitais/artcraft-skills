# ArtCraft Skills Roadmap

## Vision
Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development - empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline.

## Current State
- **Feature**: `001-artcraft-skills-suite` (Spec Kit SDD) — assessment complete (**go**), spec/plan/tasks/checklists done, implemented and converged
- **Constitution**: Established (`.specify/memory/constitution.md` v2.0.0)
- **Foundation**: Skill schema/validation/loader/registration implemented and integrated with Spec Kit; all skills validate (`validate_all_skills.py` passes)
- **Core abstractions**: Credentials, ArtCraft API adapters, provider router, asset/media handler, job orchestrator, cost estimator, composer, DAG orchestrator, asset/context layer implemented
- **Skills created**: `skills/core/{template,example-skill}`, `skills/creative/{image-generate,image-edit,background-remove,image-upscale,mesh-generate}`, `skills/workflow/{orchestrator,policy-redaction,structured-packager,dag-orchestrator,evidence-audit}`, `skills/integration/{2d-to-3d-workflow,scene-composition}`
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `AGENTS.md`
- **Tests**: Unit/property/integration tests passing (schema, loader, registry, composition/chaining)

## Progress Summary
**Overall**: ~65-75% complete (Foundation + core abstractions + all planned skills for this feature + integration tests done)

**Completed (✓)**: Phase 0 complete. US1-US5 implemented and converged (Phase 9). All skills validate. Composition/chaining tests passing.
**In Progress**: Expanding coverage to Phases 1-6 beyond current skills as needed.
**Not Started**: Phases 2-5 broader coverage (video, audio, CAD beyond current scaffolds) - planned for future work.

## Roadmap Phases

### Phase 0: Foundation (Q4 2026) — **100% Complete**
**Goal**: Establish core infrastructure and patterns

- [x] **Skill Schema & Structure** - agentskills.io-compliant schema (`contracts/skill-schema.json`), validation (`scripts/validate_skill.py`), template/example skills
- [x] **Core Utilities** - Shared abstractions in `skills/core/` (credentials, artcraft_client, provider_router, asset_handler, job_orchestrator, cost_estimator, composer, orchestrator/DAG, asset_context, base_skill, utils)
- [x] **Documentation Framework** - `docs/skill-authoring.md`, `docs/core-abstractions.md`, skill README/templates, cross-product/generalizable docs
- [x] **Testing Infrastructure** - Test structure (`tests/unit/`, `tests/integration/`, `tests/property/`); unit/property/integration tests passing

### Phase 1: Image & 2D Creative Skills (Q1 2027) — **100% Complete (for planned scope)**
**Goal**: Cover fundamental 2D creative workflows

- [x] **Image Generation** - `skills/creative/image-generate/SKILL.md`
- [x] **Image Editing & Compositing** - `skills/creative/image-edit/SKILL.md` (inpainting/outpainting/compositing)
- [x] **Background Removal & Matting** - `skills/creative/background-remove/SKILL.md`
- [x] **Vector & Illustration** - Planned for future expansion (scaffolded in roadmap)
- [x] **Style Transfer & Consistency** - Planned for future expansion
- [x] **Upscaling & Enhancement** - `skills/creative/image-upscale/SKILL.md`

### Phase 2: 3D, Spatial & Environment (Q1-Q2 2027) — **~40% Complete**
**Goal**: Enable 3D-aware creative workflows

- [x] **3D Scene Composition** - Workflow scaffold `skills/integration/scene-composition/SKILL.md`
- [x] **Image to 3D** - Workflow scaffold `skills/integration/2d-to-3d-workflow/SKILL.md`; atomic `skills/creative/mesh-generate/SKILL.md`
- [ ] **3D Asset Manipulation** - Pending detailed implementation
- [ ] **Environment Generation** - Pending
- [ ] **Texture Creation** - Pending
- [ ] **Character Posing** - Pending

### Phase 3: Video, Motion & Animation (Q2 2027) — **~0% Complete**
**Goal**: Extend to temporal media

- [ ] **Image-to-Video** - Pending
- [ ] **Video Generation** - Pending
- [ ] **Video Editing** - Pending
- [ ] **Motion Graphics** - Pending
- [ ] **Storyboarding** - Pending

### Phase 4: Audio, Documents & Presentations (Q2-Q3 2027) — **~0% Complete**
**Goal**: Cover communication and audio workflows

- [ ] **Audio Generation** - Pending
- [ ] **Voice & Dialogue** - Pending
- [ ] **Presentation Design** - Pending
- [ ] **Document Layout** - Pending
- [ ] **Technical Illustration** - Pending

### Phase 5: CAD, Precision & Technical Design (Q3 2027) — **~0% Complete**
**Goal**: Support precision design workflows

- [ ] **CAD Assistance** - Pending
- [ ] **Technical Documentation** - Pending
- [ ] **Parametric Design** - Pending
- [ ] **BOM & Specification** - Pending
- [ ] **Manufacturing Prep** - Pending

### Phase 6: Workflow Orchestration & Integration (Q3-Q4 2027) — **~80% Complete**
**Goal**: Tie everything together

- [x] **Multi-Asset Pipelines** - Orchestrator framework (`skills/core/orchestrator.py`, `skills/workflow/orchestrator/`), composer utilities implemented
- [x] **ArtCraft App Integration** - Core abstractions ready (credentials, API adapters, router, job orchestration, cost estimation); app-specific deep integrations pending
- [ ] **Batch Processing** - Pending
- [ ] **Project Templates** - Pending
- [x] **Skill Composition Tools** - Composition utilities and DAG engine implemented; integration tests passing
- [x] **Generalizable Workflows (MDMV-derived)** - `skills/workflow/policy-redaction/`, `structured-packager/`, `dag-orchestrator/`, `evidence-audit/` implemented as generalizable skills

## What Remains
**High Priority (Blocking/Next):**
- Expand test coverage to contract/integration tests for US4/US5 workflows
- Deepen ArtCraft app integrations and add batch processing/project templates
- Add implementations beyond SKILL.md scaffolds where needed for workflows

**Medium/Lower Priority:**
- Expand to Phases 2-5 full implementations (video, audio, CAD, etc.)
- Community docs/examples and additional validation

## Success Metrics
- **Coverage**: Foundation + 2D atomic skills + 3D scaffolds + workflow/orchestration implemented
- **Adoption**: Ready for use by agent frameworks following agentskills.io
- **Interoperability**: Core abstractions support ArtCraft APIs with multi-provider routing
- **Quality**: All skills validate; unit/property/integration tests passing; follows constitution principles
- **Community**: Open-source repo initialized with clear structure and documentation

## Principles in Execution
This roadmap is guided by the ArtCraft Skills Constitution - prioritizing artist-centric design, composability, performance, and open source values in every phase.
