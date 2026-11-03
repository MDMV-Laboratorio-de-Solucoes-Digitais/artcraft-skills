# ArtCraft Skills Roadmap

## Vision
Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development - empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline.

## Current State
- **Feature**: `001-artcraft-skills-suite` (Spec Kit SDD) — assessment complete (**go**), spec/plan/tasks/checklists done, implementation in progress
- **Constitution**: Established (`.specify/memory/constitution.md` v2.0.0)
- **Foundation**: Skill schema/validation/loader/registration implemented and integrated with Spec Kit
- **Core abstractions**: Credentials, ArtCraft API adapters, provider router, asset/media handler, job orchestrator, cost estimator, composition utilities implemented
- **Skills created**: `skills/core/template/`, `skills/core/example-skill/`, `skills/creative/image-generate/`, `skills/workflow/orchestrator/`, `skills/workflow/policy-redaction/`
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md` present

## Progress Summary
**Overall**: ~40-50% complete (Foundation + core abstractions + initial skills done; majority of atomic/integration/workflow skills and verification remaining)

**Completed (✓)**: Phase 0 core items largely done (schema, loader, registration, core utilities/abstractions, templates/docs). US1 mostly done, US2 mostly done, US3 partial, US4 partial.
**In Progress**: Additional atomic creative skills (image edit/inpaint, bg removal, upscale, 3D mesh), cross-product integration workflows, testing.
**Not Started**: US5 remaining workflows (structured-packager, dag-orchestrator details, evidence-audit), full Phase 8 verification suite.

## Roadmap Phases

### Phase 0: Foundation (Q4 2026) — **~85% Complete**
**Goal**: Establish core infrastructure and patterns

- [x] **Skill Schema & Structure** - agentskills.io-compliant schema (`contracts/skill-schema.json`), validation (`scripts/validate_skill.py`), template/example skills
- [x] **Core Utilities** - Shared abstractions in `skills/core/` (credentials, artcraft_client, provider_router, asset_handler, job_orchestrator, cost_estimator, composer, base_skill, utils)
- [x] **Documentation Framework** - `docs/skill-authoring.md`, `docs/core-abstractions.md`, skill README/templates
- [x] **Testing Infrastructure** - Test structure (`tests/unit/`, `tests/integration/`, `tests/property/`) established; property/contract/integration tests scaffolded (some pending)

### Phase 1: Image & 2D Creative Skills (Q1 2027) — **~20% Complete**
**Goal**: Cover fundamental 2D creative workflows

- [x] **Image Generation** - `skills/creative/image-generate/SKILL.md` (atomic skill using core abstractions)
- [ ] **Image Editing & Compositing** - Inpainting, outpainting, compositing, layers (`skills/creative/image-edit/` pending)
- [ ] **Background Removal & Matting** - Precise subject isolation (pending)
- [ ] **Vector & Illustration** - Vector path manipulation, illustration assistance (pending)
- [ ] **Style Transfer & Consistency** - Character/style consistency across generations (pending)
- [ ] **Upscaling & Enhancement** - Image enhancement and upscaling workflows (pending)

### Phase 2: 3D, Spatial & Environment (Q1-Q2 2027) — **~0% Complete**
**Goal**: Enable 3D-aware creative workflows

- [ ] **3D Scene Composition** - Scene blocking, camera control, object placement (pending)
- [ ] **Image to 3D** - Convert 2D images to 3D meshes/objects (pending)
- [ ] **3D Asset Manipulation** - Mesh editing, kitbashing, asset integration (pending)
- [ ] **Environment Generation** - World/scene generation and Gaussian splat workflows (pending)
- [ ] **Texture Creation** - PBR texture generation and 3D painting assistance (pending)
- [ ] **Character Posing** - Rigging-aware posing and character workflow tools (pending)

### Phase 3: Video, Motion & Animation (Q2 2027) — **~0% Complete**
**Goal**: Extend to temporal media

- [ ] **Image-to-Video** - Animation from still images with camera control (pending)
- [ ] **Video Generation** - Text/image-to-video with creative controls (pending)
- [ ] **Video Editing** - Cutting, compositing, and post-production assistance (pending)
- [ ] **Motion Graphics** - Animated graphics and transitions (pending)
- [ ] **Storyboarding** - Shot planning and sequence composition (pending)

### Phase 4: Audio, Documents & Presentations (Q2-Q3 2027) — **~0% Complete**
**Goal**: Cover communication and audio workflows

- [ ] **Audio Generation** - Music, SFX, and sound design (pending)
- [ ] **Voice & Dialogue** - Voice synthesis and dialogue workflows (pending)
- [ ] **Presentation Design** - Slide creation and deck composition (pending)
- [ ] **Document Layout** - Document design and formatting assistance (pending)
- [ ] **Technical Illustration** - Diagrams, schematics, and technical art (pending)

### Phase 5: CAD, Precision & Technical Design (Q3 2027) — **~0% Complete**
**Goal**: Support precision design workflows

- [ ] **CAD Assistance** - Drafting, dimensioning, and technical drawing support (pending)
- [ ] **Technical Documentation** - Precision illustration and documentation (pending)
- [ ] **Parametric Design** - Parametric modeling assistance (pending)
- [ ] **BOM & Specification** - Technical specification and documentation workflows (pending)
- [ ] **Manufacturing Prep** - Export preparation for technical workflows (pending)

### Phase 6: Workflow Orchestration & Integration (Q3-Q4 2027) — **~30% Complete**
**Goal**: Tie everything together

- [x] **Multi-Asset Pipelines** - Orchestrator framework (`skills/workflow/orchestrator/`, `skills/core/composer.py`) started; full pipeline patterns in progress
- [ ] **ArtCraft App Integration** - Deep integration with ArtCraft suite (abstractions ready, app-specific integrations pending)
- [ ] **Batch Processing** - Efficient batch operations and automation (pending)
- [ ] **Project Templates** - Reusable project templates and presets (pending)
- [x] **Skill Composition Tools** - Composition utilities and orchestrator DAG engine implemented (`skills/workflow/orchestrator.py` exists)
- [x] **Generalizable Workflows (MDMV-derived)** - `skills/workflow/policy-redaction/` added; `structured-packager`, `dag-orchestrator`, `evidence-audit` pending

## What Remains
**High Priority (Blocking/Next):**
- Complete remaining atomic skills (US3): image-edit/inpaint, background-remove, image-upscale, mesh-generate
- Complete cross-product integration (US4): 2d-to-3d-workflow, scene-composition, shared asset/context/style layer
- Implement generalizable MDMV workflows (US5): structured-packager, dag-orchestrator, evidence-audit (policy-redaction done)
- Add/complete tests for US1-US4 (many test tasks pending) and run full verification (Phase 8)

**Medium/Lower Priority:**
- Expand to Phases 1-5 skill coverage beyond image generation
- Complete ArtCraft app deep integrations, batch processing, project templates
- Community docs/examples and final validation against all success criteria

## Success Metrics
- **Coverage**: Support for major creative asset types across the full pipeline *(In progress - foundation + 1 atomic skill so far)*
- **Adoption**: Active usage by creative professionals and AI coding agent users *(Pending release/usage)*
- **Interoperability**: Seamless integration across models, providers, and tools *(Core abstractions in place for ArtCraft; multi-provider routing ready)*
- **Quality**: Skills that meaningfully enhance creative control and output quality *(Guided by constitution; validation in progress)*
- **Community**: Growing open-source community contributing skills and improvements *(Repo initialized, ready for contributions)*

## Principles in Execution
This roadmap is guided by the ArtCraft Skills Constitution - prioritizing artist-centric design, composability, performance, and open source values in every phase.
