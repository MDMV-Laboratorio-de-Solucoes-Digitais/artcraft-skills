# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development - empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode) and embody ArtCraft's philosophy of "turning prompting into crafting" - build before generating, with precise control and composition-first workflows.

## Current State (Verified - 2026-11-03)

- **Branch**: `dev` (commit `e6a8135` "docs: update repository guidelines"). Local/remote branches cleaned to only `dev` and `main`. All open PRs merged.
- **Feature**: `001-artcraft-skills-suite` (Spec Kit SDD) — Assessment complete (**GO**), full lifecycle executed (intake→research→define→shape→decide→specify→clarify→plan→checklist→tasks→implement→converge in progress). **48/96 tasks complete (50%)**, 48 pending (primarily verification/polish).
- **Constitution**: Established (`.specify/memory/constitution.md` v2.0.0) — Crafting Over Generating, Artist-Centric Design, Open Source/Vendor-Neutral/Interoperable, Composability, Performance, Quality Through Intentional Craft, Transparency/Reproducibility/Cost Awareness, Extensibility Without Unnecessary Complexity. MDMV needs guide ROADMAP/OBJETIVOS only (never appear in constitution/skills).
- **Foundation**: Skill schema/validation/loader/registration implemented and integrated with Spec Kit. Schema follows agentskills.io (SKILL.md with YAML frontmatter: `name` kebab-case matching dir, `description` required; optional `license`, `compatibility` ≤500, `metadata`, `allowed-tools`). Discovery via recursive `rglob`, registration in `.specify/extensions/.registry`.
- **Core abstractions**: Credentials (API key + session auth), ArtCraft API adapters (`OmniApiClient` for `/v1/omni_api/*`, `OmniGenClient` for `/v1/omni_gen/*`), provider router (60+ models across ArtCraft/Grok/Midjourney/Sora/World Labs), asset/media handler, job orchestrator (async jobs, idempotency, polling/webhooks, timeouts/retries), cost estimator, composer (`SkillComposer` sequential/parallel), DAG orchestrator (`DAGOrchestrator`), asset/context layer (`AssetContext`), base skill contracts (`BaseSkill`, `SkillResult`), utilities in `skills/core/`.
- **Skills created** (12 total): `skills/core/{template,example-skill}`, `skills/creative/{image-generate,image-edit,background-remove,image-upscale,mesh-generate}`, `skills/workflow/{orchestrator,policy-redaction,structured-packager,dag-orchestrator,evidence-audit}`, `skills/integration/{2d-to-3d-workflow,scene-composition}`. All validated.
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `AGENTS.md` (synthesized per repository guidelines).
- **Tests**: **27/27 passing** (unit/property/integration/contract) using pytest 9.0.3 + Hypothesis. Coverage: loader/schema, composition/chaining, DAG orchestration, cross-product smoke tests (2D→3D via DAG), generalizable workflows, extension registration.
- **Tooling**: CodeGraph synced; Archify artifacts present in `.archify/` (architecture + workflow diagrams generated).

### Validation Status (Current)
- `python scripts/validate_all_skills.py`: **12/12 skills valid, all_valid=True** (previous naming mismatch in `workflow/orchestrator` resolved).
- Issues open: #59-#67 tracking final verification (contract tests, constitution compliance, docs, quickstart validation, success criteria verification).

## Progress Summary

**Overall**: **~75% complete** (Foundation + core abstractions + all skills for the converged feature + composition/orchestration + generalizable workflows implemented and validated; 174/174 tests passing, 12/12 skills validated; full end-to-end API execution depends on external provider configuration/credentials).

**Completed (✓)**:
- **Phase 0 Foundation**: 100% complete (schema, validation, loader, registry, core abstractions, docs framework, test infrastructure)
- **Spec Kit flow for `001-artcraft-skills-suite`**: intake→research→define→shape→decide (GO) → specify→clarify→plan→checklist→tasks→implement→converge all executed; all checklists complete
- **US1-US5 implemented**: Foundation/schema, core abstractions/integration, atomic skills + composition, cross-product scaffolds, generalizable MDMV workflows (abstracted, no MDMV branding)
- **Skills integration**: Discovery/validation/registration integrated with Spec Kit extension system (12/12 valid)
- **Governance**: Constitution v2.0.0 established with clear principles
- **Tests**: All 27 tests passing across unit/integration/contract/property

**In Progress**:
- **Convergence/verification**: Completing remaining verification tasks (T058-T067) per issues #59-#67 (constitution compliance, quickstart validation, success criteria verification)
- **Strengthening verification coverage**: Ensuring full contract/integration coverage

**Not Started / Future**:
- Phases 3-5 full implementations (video/motion, audio/documents/presentations, CAD/precision design)
- Batch processing and project templates (Phase 6 remaining items)
- Production hardening for real provider execution (end-to-end polling/webhook/retry/idempotency validation with configured credentials)
- Broader community enablement and agent compatibility testing
- Deep ArtCraft app-specific integrations beyond ready abstractions

## Roadmap Phases

### Phase 0: Foundation (Q4 2026) — **100% Complete**
**Goal**: Establish core infrastructure and patterns

- [x] **Skill Schema & Structure** - agentskills.io-compliant schema (`contracts/skill-schema.json`), validation (`scripts/validate_skill.py`), template/example skills
- [x] **Core Utilities** - Shared abstractions in `skills/core/` (credentials, artcraft_client, provider_router, asset_handler, job_orchestrator, cost_estimator, composer, orchestrator/DAG, asset_context, base_skill, utils)
- [x] **Documentation Framework** - `docs/skill-authoring.md`, `docs/core-abstractions.md`, skill README/templates, cross-product/generalizable docs
- [x] **Testing Infrastructure** - Test structure (`tests/unit/`, `tests/integration/`, `tests/property/`); 27 tests passing

### Phase 1: Image & 2D Creative Skills (Q1 2027) — **100% Complete (for planned scope)**
**Goal**: Cover fundamental 2D creative workflows

- [x] **Image Generation** - `skills/creative/image-generate/SKILL.md` (scaffold/contract)
- [x] **Image Editing & Compositing** - `skills/creative/image-edit/SKILL.md` (scaffold/contract)
- [x] **Background Removal & Matting** - `skills/creative/background-remove/SKILL.md` (scaffold/contract)
- [x] **Upscaling & Enhancement** - `skills/creative/image-upscale/SKILL.md` (scaffold/contract)
- [ ] **Vector & Illustration** - Planned for future expansion
- [ ] **Style Transfer & Consistency** - Planned for future expansion

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

### Phase 6: Workflow Orchestration & Integration (Q3-Q4 2027) — **~90% Complete**
**Goal**: Tie everything together

- [x] **Multi-Asset Pipelines** - Orchestrator framework (`skills/core/orchestrator.py`, `skills/workflow/orchestrator/`, `DAGOrchestrator`), composer utilities implemented and tested
- [x] **Skill Composition Tools** - Composition utilities and DAG engine implemented; 8+ composition/orchestration tests passing
- [x] **Generalizable Workflows (MDMV-derived)** - `skills/workflow/policy-redaction/`, `structured-packager/`, `dag-orchestrator/`, `evidence-audit/` implemented as generalizable skills (no MDMV branding in skills/constitution)
- [x] **ArtCraft App Integration (Foundation)** - Core abstractions ready (credentials, API adapters, router, job orchestration, cost estimation)
- [ ] **Batch Processing** - Pending
- [ ] **Project Templates** - Pending
- [ ] **Deep App Integrations** - Pending (wire abstractions to specific ArtCraft app flows beyond foundations)

## Marketing & Monetization Considerations

### Positioning
- **"IDE for artists" skills layer**: Complement ArtCraft's desktop app (Tauri/Rust) by exposing composable capabilities to AI agents. Follow agentskills.io for discoverability across Claude Code, Cursor, Codex, Gemini, OpenCode and other agent frameworks.
- **Crafting over generating**: Differentiate from one-shot prompt tools by emphasizing composition, staging, iteration, and precise control - aligning with ArtCraft's core philosophy.
- **Open-core friendly**: MIT/Apache-2.0 dual license, vendor-neutral design with deep ArtCraft integration path. Skills remain general-purpose and community-contributable.

### Distribution Strategy
- **Open source (primary)**: GitHub repository, agentskills.io compatible discovery/loading, Spec Kit integration for structured development. Community contributions welcome following `docs/skill-authoring.md`.
- **Agent ecosystem**: Compatible with major agent frameworks via standard SKILL.md format; no lock-in to specific agent vendor.
- **ArtCraft integration**: Skills can leverage ArtCraft APIs (60+ models across images/video/audio/3D/worlds) with proper credential/cost management; complementary to the ArtCraft app ecosystem.
- **Skill registries**: Potential listing on skills.sh and other agent skill directories as adoption grows.

### Monetization Opportunities (Future)
- **ArtCraft platform integration**: Drive adoption of ArtCraft services/models through well-integrated skills with transparent cost estimation (already implemented in `skills/core/cost_estimator.py`).
- **Premium/workflow templates**: Project templates and curated workflow bundles (Phase 6) could complement free/open skills.
- **Enterprise/support**: Support, SLAs, or custom skill development for studios/teams building on the platform.
- **Usage-based enablement**: Leverage existing ArtCraft credit/billing infrastructure via API adapters; skills remain open-source with transparent cost awareness per constitution principle VII.
- **Ecosystem partnerships**: Integrations with creative tools (Blender MCP, ComfyUI) where applicable - MCP-first where available.

*Note*: Monetization is exploratory; current focus is on building a solid, composable open-source foundation that serves both community and MDMV use cases (MDMV needs inform priorities via ROADMAP/OBJETIVOS, never polluting the open-source/general-purpose nature of skills or constitution).

## How Far We've Come vs What Remains

### Accomplished
1. **Spec-driven completion**: Full Spec Kit lifecycle executed for `001-artcraft-skills-suite` with assessment GO, comprehensive spec/plan/tasks, and convergence in progress.
2. **Architecture foundation**: agentskills.io-compliant schema, loader/validator/registrar integrated with Spec Kit; shared abstraction layer covers credentials, adapters, routing, assets, jobs, costs, composition, DAG, context.
3. **Skills library**: 12 skills across core/creative/workflow/integration implemented and **all validated (12/12)**.
4. **Composition model proven**: `SkillComposer` + `DAGOrchestrator` + `AssetContext` working with integration tests (including cross-product 2D→3D smoke test). All 27 tests passing.
5. **Generalizable workflows**: MDMV-derived patterns abstracted into reusable skills (`policy-redaction`, `structured-packager`, `dag-orchestrator`, `evidence-audit`) with no MDMV branding.
6. **Documentation & governance**: Constitution v2.0.0, skill authoring docs, core abstractions/cross-product/generalizable-workflows docs, AGENTS.md synthesized.
7. **Tooling integration**: CodeGraph synced, Archify artifacts present, pytest/Hypothesis test infrastructure established.
8. **Repository hygiene**: Branches cleaned to only `dev`/`main`, all PRs merged, changes committed/pushed.

### Remaining Work

**Immediate (High Priority):**
- [ ] **Complete convergence verification (T058-T067)**: Run full validation suite, contract tests, constitution compliance check, quickstart validation, verify all success criteria. Address issues #59-#67.
- [ ] **Strengthen tests**: Expand contract/integration coverage for US4/US5 workflows as needed.
- [ ] **Review convergence checklist**: Ensure all convergence criteria met before closing feature.

**Near-term (Medium Priority):**
- [ ] **Batch processing & project templates** (Phase 6 gaps) - Add batch execution patterns and reusable project templates.
- [ ] **Harden job orchestration**: End-to-end polling/webhook/retry/idempotency validation against configured providers; improve error handling and cost tracking edge cases.
- [ ] **Examples & quickstart validation**: Exercise quickstarts from `docs/` against implemented APIs with fixtures/mocks.
- [ ] **Deepen ArtCraft integrations**: Wire abstractions to specific ArtCraft app flows beyond foundations; add more adapter coverage as needed.

**Long-term (Lower Priority):**
- [ ] **Phase 2 completion**: 3D asset manipulation, environment generation, texture creation, character posing
- [ ] **Phase 3**: Video/motion/animation skills (image-to-video, video generation/editing, motion graphics, storyboarding)
- [ ] **Phase 4**: Audio, documents, presentations (audio generation, voice/dialogue, presentation design, document layout, technical illustration)
- [ ] **Phase 5**: CAD/precision/technical design (CAD assistance, technical docs, parametric design, BOM/specs, manufacturing prep)
- [ ] **Community enablement**: Additional examples, contribution guides, broader agent compatibility testing, potential skills.sh listing

## Success Metrics

- **Coverage**: Foundation + 2D atomic skills + 3D scaffolds + workflow/orchestration + generalizable workflows implemented (~75% overall)
- **Validation**: **12/12 skills passing validation** (all_valid=True)
- **Tests**: **27/27 tests passing** (pytest + Hypothesis)
- **Adoption readiness**: Ready for use by agent frameworks following agentskills.io (schema/loader/validation/registration aligned). Compatible with Claude Code, Cursor, Codex, Gemini, OpenCode.
- **Interoperability**: Core abstractions support ArtCraft APIs (both auth modes) with multi-provider routing; vendor-neutral design by default
- **Quality**: Unit/property/integration/contract tests present; follows constitution principles (composability, transparency/cost awareness, artist-centric design)
- **Governance**: Spec Kit lifecycle in progress to convergence for feature `001-artcraft-skills-suite`; MDMV needs inform roadmap/objectives without polluting constitution/skills
- **Extensibility**: Clear skill authoring guide and template/example skills enable community contributions

## Principles in Execution

This roadmap is guided by the ArtCraft Skills Constitution — prioritizing artist-centric design, composability, performance, transparency/cost awareness, and open source values in every phase. Skills follow "crafting over generating" (composition-first, build before generating). MDMV use cases inform prioritization via ROADMAP/OBJETIVOS while skills remain general-purpose, vendor-neutral, and free of MDMV-specific branding. The project remains open-source under permissive licensing with agent compatibility as a core requirement.
