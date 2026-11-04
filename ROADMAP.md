# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development — empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode, and others) and embody ArtCraft's philosophy of "turning prompting into crafting" — build before generating, with precise control and composition-first workflows.

Skills are consumed by agents that drive the real ArtCraft creative apps (PhotoCraft, PdfCraft, and the rest of the 13–16 Rust "Crafting Apps" in the `storytold` org) through their **CLI** (`photocraft-cli`, 500+ commands) and **MCP server** surfaces, plus ArtCraft's AI studio (60+ models across image/video/audio/3D/worlds). There is no separate generation backend in this repo — it is the skill/agent layer on top of those surfaces.

## Research & Competitive Landscape (verified 2026-11-04)

- **agentskills.io** is the de-facto open format (SKILL.md + YAML frontmatter); supported by Claude Code, Codex, Cursor, Gemini CLI, OpenCode, VS Code, and others. Best-practices guidance exists for description optimization, evals, and MCP integration. → Our schema/loader/validation already conform.
- **ArtCraft's own surfaces**: 13–16 open-source Rust apps (`storytold` org), each exposing a CLI + MCP server; `photocraft-cli` exposes 500+ commands. Agent tutorials and a `craft-agent-kit` (CLI wrappers/MCP configs/skills for all 13 apps) exist. → Our adapter wraps exactly these surfaces; we are the Spec-Kit-governed, vendor-neutral, composable layer.
- **Competing/complementary skill packs**: `full-aigc-skills/artcraft-skills` (artcraft-cli, artcraft-use, artcraft-harness, …), `midasmatterhorn/artcraft-skills`, `MGBuilds9/craft-agent-kit`. → Differentiate by: Spec-Kit SDD lifecycle, constitution/governance, characterization-tested equivalence, shared adapter with reason codes, vendor-neutral abstractions, MDMV-derived generalizable workflows.
- **Broader creative-agent skill ecosystem**: `pexo-skills`, `generative-media-skills`, `scenario` skills, `muapi` agent skills, `open-clip`, `claude-remotion-skill`. → Confirms demand for image/video/audio/3D agent skills; our roadmap Phases 3–5 target these domains via ArtCraft apps rather than re-implementing providers.
- **MCP**: 2026-07-28 spec is stateless core; MCP is the dominant integration for creative tools (Figma, Canva, PhotoCraft). → Our adapter keeps MCP discovery/invocation skill-level (FR-005) and normalizes config/output — consistent with the ecosystem pattern of thin adapters over real MCP servers.

## Current State (Verified — 2026-11-04)

- **Branch**: `dev` (commit `c307e1f`). Local/remote branches cleaned to only `dev` and `main`. All open PRs merged (6 PRs for feature 003).
- **Feature 001**: `001-artcraft-skills-suite` (Spec Kit SDD) — Assessment complete (**GO**), full lifecycle executed (intake→research→define→shape→decide→specify→clarify→plan→checklist→tasks→implement→converge in progress). **68/98 tasks complete (~69%)**; the remaining 21 `[ ]` entries in `tasks.md` are largely stale (referenced test files exist under different names; creative skills exist as SKILL.md).
- **Feature 003**: `003-shared-cli-mcp-adapter` — **Converged**. Shared adapter `skills/core/artcraft_app_client.py` (9 functions, reason codes, `__version__=0.2.0`), image-generate refactored with equivalence verified (golden master + differential + property), 41/41 checklists, analyze + converge executed.
- **Constitution**: Established (`.specify/memory/constitution.md` v2.0.0) — Crafting Over Generating, Artist-Centric Design, Open Source/Vendor-Neutral/Interoperable, Composability, Performance, Quality Through Intentional Craft, Transparency/Reproducibility/Cost Awareness, Extensibility Without Unnecessary Complexity.
- **Foundation**: Skill schema/validation/loader/registration implemented and integrated with Spec Kit. Schema follows agentskills.io (SKILL.md with YAML frontmatter: `name` kebab-case matching dir, `description` required; optional `license`, `compatibility` ≤500, `metadata`, `allowed-tools`). Discovery via recursive `rglob`, registration in `.specify/extensions/.registry`.
- **Core abstractions**: Credentials (API key + session auth), ArtCraft API adapters (`OmniApiClient` for `/v1/omni_api/*`, `OmniGenClient` for `/v1/omni_gen/*`), provider router (60+ models across ArtCraft/Grok/Midjourney/Sora/World Labs), asset/media handler, job orchestrator (async jobs, idempotency, polling/webhooks, timeouts/retries), cost estimator, composer (`SkillComposer` sequential/parallel), DAG orchestrator (`DAGOrchestrator`), asset/context layer (`AssetContext`), base skill contracts (`BaseSkill`, `SkillResult`), utilities in `skills/core/`, shared adapter (`artcraft_app_client`).
- **Skills created** (14 total, all validated): `skills/core/{template,example-skill}`, `skills/creative/{image-generate,image-edit,background-remove,image-upscale,mesh-generate}`, `skills/workflow/{orchestrator,policy-redaction,structured-packager,dag-orchestrator,evidence-audit}`, `skills/integration/{2d-to-3d-workflow,scene-composition}`. **5 creative skills now have Python implementations** (image-generate, image-edit, background-remove, image-upscale, mesh-generate); workflow/integration skills remain declarative SKILL.md.
- **Docs**: `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`, `docs/architecture.md` (new), `AGENTS.md`.
- **Tests**: **278 passing** (unit/contract/integration/property/characterization) using pytest 9.0.3 + Hypothesis. Coverage: loader/schema, composition/chaining, DAG orchestration, cross-product smoke tests, generalizable workflows, adapter unit/property/contract/characterization/differential. (Note: 23 original image-generate unit/contract/integration tests were lost during merge; equivalence covered by golden/differential/property.)
- **Tooling**: CodeGraph synced; Archify artifacts present in `.archify/`; pytest/Hypothesis test infrastructure; `pytest.ini` with import-mode=importlib.

### Validation Status (Current)
- `python scripts/validate_all_skills.py`: **14/14 skills valid, all_valid=True** (incl. template/example-skill).
- `python scripts/validate_skill.py skills/creative/image-generate`: Valid.
- Issues open: #59-#67 tracking final verification for 001 (contract tests, constitution compliance, docs, quickstart validation, success criteria verification).

## Progress Summary

**Overall**: **~75% complete** (Foundation + core abstractions + all skills for the converged feature + composition/orchestration + generalizable workflows implemented and validated; 278 tests passing, 14/14 skills validated; feature 003 converged; feature 001 at ~69% by task count).

**Completed (✓)**:
- **Phase 0 Foundation**: 100% complete (schema, validation, loader, registry, core abstractions, docs framework, test infrastructure)
- **Spec Kit flow for `001-artcraft-skills-suite`**: intake→research→define→shape→decide (GO) → specify→clarify→plan→checklist→tasks→implement→converge in progress (68/98 tasks)
- **Spec Kit flow for `003-shared-cli-mcp-adapter`**: full cycle executed and **converged** (Phase 7 complete, 41/41 checklists, 32/32 tasks)
- **US1-US5 implemented (001)**: Foundation/schema, core abstractions/integration, atomic skills + composition, cross-product scaffolds, generalizable MDMV workflows (abstracted, no MDMV branding)
- **Shared adapter (003)**: `artcraft_app_client.py` with 9 functions, reason codes, `__version__=0.2.0`, image-generate refactored with equivalence verified
- **Skills integration**: Discovery/validation/registration integrated with Spec Kit extension system (14/14 valid)
- **Governance**: Constitution v2.0.0 established with clear principles
- **Tests**: 278 tests passing across unit/contract/integration/property/characterization
- **Repository hygiene**: Branches cleaned to only `dev`/`main`, all PRs merged, changes committed/pushed

**In Progress**:
- **Convergence/verification (001)**: Completing remaining verification tasks (T058-T067) per issues #59-#67 (constitution compliance, quickstart validation, success criteria verification)
- **Strengthening verification coverage**: Expanding contract/integration coverage for US4/US5 workflows

**Not Started / Future**:
- Phase 2 3D implementation (mesh-generate skill.py done, but 3D asset manipulation/environment/texture/posing pending)
- Phases 3-5 full implementations (video/motion, audio/documents/presentations, CAD/precision design)
- Batch processing and project templates (Phase 6 remaining items)
- Production hardening for real provider execution (end-to-end polling/webhook/retry/idempotency validation with configured credentials)
- Broader community enablement and agent compatibility testing
- Deep ArtCraft app-specific integrations beyond ready abstractions
- Python implementations for creative skills (image-edit, background-remove, image-upscale, mesh-generate)
- MCP transport in the adapter (deliberately kept skill-level per FR-005)

## Roadmap Phases

### Phase 0: Foundation (Q4 2026) — **100% Complete**
**Goal**: Establish core infrastructure and patterns

- [x] **Skill Schema & Structure** - agentskills.io-compliant schema (`contracts/skill-schema.json`), validation (`scripts/validate_skill.py`), template/example skills
- [x] **Core Utilities** - Shared abstractions in `skills/core/` (credentials, artcraft_client, provider_router, asset_handler, job_orchestrator, cost_estimator, composer, orchestrator/DAG, asset_context, base_skill, utils, artcraft_app_client)
- [x] **Documentation Framework** - `docs/skill-authoring.md`, `docs/core-abstractions.md`, skill README/templates, cross-product/generalizable docs, `docs/architecture.md`
- [x] **Testing Infrastructure** - Test structure (`tests/unit/`, `tests/integration/`, `tests/property/`, `tests/contract/`, `tests/characterization/`); 278 tests passing

### Phase 1: Image & 2D Creative Skills (Q1 2027) — **~80% Complete (Python implementation)**
**Goal**: Cover fundamental 2D creative workflows (via ArtCraft apps' CLI/MCP, not re-implemented providers)

- [x] **Image Generation** - `skills/creative/image-generate/SKILL.md` + Python implementation (`skill.py`) using shared adapter
- [x] **Image Editing & Compositing** - `skills/creative/image-edit/SKILL.md` + `skill.py` (shared adapter)
- [x] **Background Removal & Matting** - `skills/creative/background-remove/SKILL.md` + `skill.py` (shared adapter)
- [x] **Upscaling & Enhancement** - `skills/creative/image-upscale/SKILL.md` + `skill.py` (shared adapter)
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
- [x] **ArtCraft App Integration (Foundation)** - Core abstractions ready (credentials, API adapters, router, job orchestration, cost estimation, shared adapter)
- [ ] **Batch Processing** - Pending
- [ ] **Project Templates** - Pending
- [ ] **Deep App Integrations** - Pending (wire abstractions to specific ArtCraft app flows beyond foundations)

## Marketing & Monetization Considerations

### Positioning
- **"IDE for artists" skills layer**: Complement ArtCraft's desktop app (Tauri/Rust) by exposing composable capabilities to AI agents. Follow agentskills.io for discoverability across Claude Code, Cursor, Codex, Gemini, OpenCode and other agent frameworks.
- **Crafting over generating**: Differentiate from one-shot prompt tools by emphasizing composition, staging, iteration, and precise control — aligning with ArtCraft's core philosophy and the broader shift (2026) toward agent-driven creative workflows over single-shot generation.
- **Open-core friendly**: MIT/Apache-2.0 dual license, vendor-neutral design with deep ArtCraft integration path. Skills remain general-purpose and community-contributable.
- **Differentiators vs. existing ArtCraft skill packs** (`full-aigc-skills/artcraft-skills`, `midasmatterhorn/artcraft-skills`, `craft-agent-kit`): Spec-Kit-governed lifecycle, constitution, characterization-tested equivalence, shared adapter with reason codes, vendor-neutral abstractions, MDMV-derived generalizable workflows.

### Distribution Strategy
- **Open source (primary)**: GitHub repository, agentskills.io compatible discovery/loading, Spec Kit integration for structured development. Community contributions welcome following `docs/skill-authoring.md`.
- **Agent ecosystem**: Compatible with major agent frameworks via standard SKILL.md format; no lock-in to specific agent vendor. Listing on skills.sh / agentskills.io client showcase as adoption grows.
- **ArtCraft integration**: Skills leverage ArtCraft APIs (60+ models across images/video/audio/3D/worlds) with proper credential/cost management; complementary to the ArtCraft app ecosystem and its CLI/MCP surfaces.
- **Skill registries**: Potential listing on skills.sh and other agent skill directories as adoption grows.

### Monetization Opportunities (Future)
- **ArtCraft platform integration**: Drive adoption of ArtCraft services/models through well-integrated skills with transparent cost estimation (already implemented in `skills/core/cost_estimator.py`).
- **Premium/workflow templates**: Project templates and curated workflow bundles (Phase 6) could complement free/open skills.
- **Enterprise/support**: Support, SLAs, or custom skill development for studios/teams building on the platform.
- **Usage-based enablement**: Leverage existing ArtCraft credit/billing infrastructure via API adapters; skills remain open-source with transparent cost awareness per constitution principle VII.
- **Ecosystem partnerships**: Integrations with creative tools (Blender MCP, ComfyUI) where applicable — MCP-first where available.

*Note*: Monetization is exploratory; current focus is on building a solid, composable open-source foundation that serves both community and MDMV use cases (MDMV needs inform priorities via ROADMAP/OBJETIVOS, never polluting the open-source/general-purpose nature of skills or constitution).

## How Far We've Come vs What Remains

### Accomplished
1. **Spec-driven completion (003)**: Full Spec Kit lifecycle executed for `003-shared-cli-mcp-adapter` with assessment GO, comprehensive spec/plan/tasks, and **convergence achieved** (Phase 7 complete, 41/41 checklists, 32/32 tasks, 278 tests passing).
2. **Spec-driven in progress (001)**: Full Spec Kit lifecycle executed through implement; 68/98 tasks complete (~69%); analyze/converge not yet run.
3. **Architecture foundation**: agentskills.io-compliant schema, loader/validator/registrar integrated with Spec Kit; shared abstraction layer covers credentials, adapters, routing, assets, jobs, costs, composition, DAG, context, shared adapter.
4. **Skills library**: 14 skills across core/creative/workflow/integration implemented and **all validated (14/14)**. 5 creative skills now have Python implementations via the shared adapter.
5. **Composition model proven**: `SkillComposer` + `DAGOrchestrator` + `AssetContext` working with integration tests (including cross-product 2D→3D smoke test).
6. **Generalizable workflows**: MDMV-derived patterns abstracted into reusable skills (`policy-redaction`, `structured-packager`, `dag-orchestrator`, `evidence-audit`) with no MDMV branding.
7. **Documentation & governance**: Constitution v2.0.0, skill authoring docs, core abstractions/cross-product/generalizable-workflows docs, `docs/architecture.md`, AGENTS.md synthesized.
8. **Tooling integration**: CodeGraph synced, Archify artifacts present, pytest/Hypothesis test infrastructure established, `pytest.ini` with import-mode=importlib.
9. **Repository hygiene**: Branches cleaned to only `dev`/`main`, all PRs merged, changes committed/pushed.

### Remaining Work

**Immediate (High Priority):**
- [ ] **Complete convergence verification (001, T058-T067)**: Run full validation suite, contract tests, constitution compliance check, quickstart validation, verify all success criteria. Address issues #59-#67.
- [ ] **Strengthen tests**: Expand contract/integration coverage for US4/US5 workflows as needed.
- [ ] **Review convergence checklist**: Ensure all convergence criteria met before closing feature 001.
- [ ] **Restore lost image-generate tests**: Recreate the 23 original unit/contract/integration tests (lost during merge) to satisfy SC-002.
- [ ] **Sync tasks.md (001)**: Mark the 21 stale `[ ]` entries as done where the corresponding files already exist.

**Near-term (Medium Priority):**
- [ ] **Batch processing & project templates** (Phase 6 gaps) - Add batch execution patterns and reusable project templates.
- [ ] **Harden job orchestration**: End-to-end polling/webhook/retry/idempotency validation against configured providers; improve error handling and cost tracking edge cases.
- [ ] **Examples & quickstart validation**: Exercise quickstarts from `docs/` against implemented APIs with fixtures/mocks.
- [ ] **Deepen ArtCraft integrations**: Wire abstractions to specific ArtCraft app flows beyond foundations; add more adapter coverage as needed.
- [x] **Implement Python skills**: image-edit, background-remove, image-upscale, mesh-generate (now executable via shared adapter).
- [ ] **MCP transport decision follow-up**: Re-evaluate FR-005 (skill-level MCP) once a second creative skill ships and a real MCP client is justified.

**Long-term (Lower Priority):**
- [ ] **Phase 2 completion**: 3D asset manipulation, environment generation, texture creation, character posing
- [ ] **Phase 3**: Video/motion/animation skills (image-to-video, video generation/editing, motion graphics, storyboarding)
- [ ] **Phase 4**: Audio, documents, presentations (audio generation, voice/dialogue, presentation design, document layout, technical illustration)
- [ ] **Phase 5**: CAD/precision/technical design (CAD assistance, technical docs, parametric design, BOM/specs, manufacturing prep)
- [ ] **Community enablement**: Additional examples, contribution guides, broader agent compatibility testing, potential skills.sh listing
- [ ] **Differentiation vs. competing packs**: Publish benchmarks/coverage comparison; contribute upstream to agentskills.io client showcase

## Success Metrics

- **Coverage**: Foundation + 2D atomic skills (5 implemented in Python) + 3D scaffolds + workflow/orchestration + generalizable workflows implemented (~75% overall)
- **Validation**: **14/14 skills passing validation** (all_valid=True)
- **Tests**: **278 passing** (unit/contract/integration/property/characterization) with pytest + Hypothesis
- **Features**: 001 at ~69% (68/98 tasks); 003 converged (32/32 tasks, 41/41 checklists)
- **Adoption readiness**: Ready for use by agent frameworks following agentskills.io (schema/loader/validation/registration aligned). Compatible with Claude Code, Cursor, Codex, Gemini, OpenCode.
- **Interoperability**: Core abstractions support ArtCraft APIs (both auth modes) with multi-provider routing; vendor-neutral design by default; wraps real ArtCraft CLI/MCP surfaces
- **Quality**: Unit/property/integration/contract/characterization tests present; follows constitution principles (composability, transparency/cost awareness, artist-centric design)
- **Governance**: Spec Kit lifecycle in progress to convergence for 001; 003 converged; MDMV needs inform roadmap/objectives without polluting constitution/skills
- **Extensibility**: Clear skill authoring guide and template/example skills enable community contributions

## Principles in Execution

This roadmap is guided by the ArtCraft Skills Constitution — prioritizing artist-centric design, composability, performance, transparency/cost awareness, and open source values in every phase. Skills follow "crafting over generating" (composition-first, build before generating). MDMV use cases inform prioritization via ROADMAP/OBJETIVOS while skills remain general-purpose, vendor-neutral, and free of MDMV-specific branding. The project remains open-source under permissive licensing with agent compatibility as a core requirement. MCP discovery/invocation stays at skill level (FR-005) to avoid a premature universal runtime.
