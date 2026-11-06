# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development — empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility and embody ArtCraft’s philosophy of “turning prompting into crafting”.

Skills are consumed by agents that drive real ArtCraft creative apps (PhotoCraft, PdfCraft, and other Rust “Crafting Apps” in the `storytold` org) through **CLI** and **MCP server** surfaces, plus ArtCraft’s AI studio. This repo is the skill/agent layer on top of those surfaces (no separate generation backend).

## Current State (Verificado — 2026-11-06)

- **Branch:** `dev` @ `d62e5e0` (synced with `origin/dev`), PR stack 007 #131–#135 integrated; only `dev`/`main` local+remote; **no open PRs**.
- **Quality gates (default):** **412 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`); **12/12 skills validated** (`python scripts/validate_all_skills.py`). Integration tests are opt-in (`-m "not integration"` excluded by default).
- **Converged specs (defined scope):** `001`, `003`, `004`, `005-resiliencia-creativeskill` (evidence recorded), `006-mcp-stdio-functional-integration`, `007-photocraft-mcp-smoke` (Option A stateless, T001–T023 complete; SC-001 exercised locally under explicit authorization — engine/editor only, no AI/provider/model claim).
- **Core:** schema/validation/loader/registry, `BaseSkill/SkillResult`, `CreativeSkill`, shared `artcraft_app_client` (CLI + MCP stdio minimum viable, FR-005/FR-006 preserved), resilience (retry 3 + exponential backoff + jitter + `BoundedSemaphore(3)`), `SkillComposer`, `DAGOrchestrator`.
- **Creative skills (Python, current scope):** `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`; `scene-composition` executable; generalizable workflows present.
- **Research (primary-source based):** `docs/research/2026-11-06-ecosystem-roadmap-status.md` (agentskills.io spec; MCP stdio 2025-11-25; `storytold/photocraft` MCP docs; local evidence/gaps). Prior: `docs/research/2026-11-05-ecosystem-and-status.md`.

## Progress Summary

**Overall:** **~95% of foundational scope + minimum viable MCP stdio integration + authorized local real-path smoke (PhotoCraft, stateless)**. Not 100% of product: multi-app/environment operational validation, stateful MCP (Option B), deep per-app capability mapping, domain expansion (Phases 3–5), and product adoption docs remain.

**Completed (✓):**
- **Phase 0 Foundation**: schema/validation/loader/registry, core abstractions, composer/DAG, docs, deterministic test infrastructure.
- **006 MCP stdio (minimum viable, mock-first):** `tools/list`/`tools/call` transport path in adapter, `SkillResult` normalization, FR-005 selection/back-compat (explicit `mcp` no silent CLI reroute; `auto` CLI-first preserved), FR-006 additive reason/metadata taxonomy, deterministic tests.
- **007 PhotoCraft MCP smoke (Option A, stateless, opt-in):** test-only harness reusing 006 adapter; safe temp roots/cleanup, bounded timeout, explicit authorization; real local evidence recorded for `tools/list` + `command_list` (**engine/editor automation only; no AI/provider/model/artifact-cycle/default-CI claim**).
- **Resilience + fallback:** retry/backoff/jitter/semaphore; `generate_via_editing_commands` graceful degradation.
- **Creative skills/workflows (current scope):** 5 creative Python skills + scene-composition + generalizable workflows; **12/12 skills validated**.

**Backlog / caveats:**
- `specs/005-resiliencia-creativeskill/tasks.md`: implementation checkboxes partially marked while convergence evidence exists — **reconcile checkboxes/evidence** (doc hygiene).
- `specs/006-integracao-geracao-assets` (0/11) vs `006-mcp-stdio-functional-integration` — **historical `006-*` numbering ambiguity**; normalize future references without rewriting history.
- `README.md` (root) not present — adoption/onboarding gap.

## Roadmap Phases

### Phase 0: Foundation — **100% Complete**
- [x] agentskills.io schema/validation/discovery/loading/registry
- [x] Core abstractions, shared adapter, resilience, composition/DAG
- [x] Docs and deterministic test infrastructure (**412 passed / 23 deselected**, **12/12 valid**)

### Phase 1: Image & 2D Creative Skills — **100% (current scope)**
- [x] `image-generate`, `image-edit`, `background-remove`, `image-upscale`
- [ ] Vector & Illustration (future)
- [ ] Style Transfer & Consistency (future)

### Phase 2: 3D, Spatial & Environment — **~60%**
- [x] Scene composition + `mesh-generate`
- [ ] 3D asset manipulation, environment generation, texture creation, character posing

### Phase 3: Video, Motion & Animation — **0%**
- [ ] Image-to-video, video generation/editing, motion graphics, storyboarding

### Phase 4: Audio, Documents & Presentations — **0%**
- [ ] Audio/voice/dialogue, presentation design, document layout, technical illustration

### Phase 5: CAD, Precision & Technical Design — **0%**
- [ ] CAD assistance, technical documentation, parametric design, BOM/specification, manufacturing prep

### Phase 6: Workflow Orchestration & Integration — **~96% (foundation)**
- [x] Multi-asset pipelines, skill composition, DAG/generalizable workflows
- [x] ArtCraft app integration foundation (CLI + MCP stdio minimum viable, fallback, resilience)
- [x] Optional authorized real PhotoCraft MCP stateless smoke (007, test-only)
- [ ] **007 Option B (separate spec):** stateful MCP session helper for `doc_new → command → doc_export` in one retained session (mock-first + opt-in real validation)
- [ ] Per-capability MCP mapping for Crafting Apps (tools/roots/progress/cancel/format constraints)
- [ ] Controlled optional CI/manual job for real MCP smoke (never default), secure evidence handling
- [ ] Batch processing, project templates, deep app integrations

## Immediate Next Steps (prioritized)
1. **Reconcile Speckit doc hygiene** (low risk): 005 checkbox/evidence alignment; clarify `006-*` numbering in docs; keep history intact.
2. **Spec/decide 007 Option B** (stateful MCP session, narrow) if stateful artifact workflows become priority; preserve public contracts and mock-first defaults.
3. **Deepen real capability mapping** (PhotoCraft first): engine-oriented `command_*`/`doc_*`/preview/resource tools, roots/progress/cancellation/error semantics; no AI-generation overclaim.
4. **MCP dependency decision (only if needed):** evaluate official Python SDK (`modelcontextprotocol/python-sdk`, observed v2.x line) vs current minimal client for advanced lifecycle/auth/Streamable HTTP; maintain deterministic tests/back-compat.
5. **Product adoption:** add root `README.md`, onboarding, and compatibility matrix (Crafting Apps/MCP/protocol versions). Expand Phases 3–5 after stable mappings.

## What this project does NOT do
- No model/provider/backend reimplementation; no replacement of ArtCraft apps.
- No real MCP smoke in default CI; opt-in + explicit authorization + safety controls only.
- No AI generation/provider/model/prompt claim via local PhotoCraft MCP smoke path (007 = engine/editor stateless).
- No stateful MCP artifact cycle in current adapter (Option B deferred).
- No guaranteed operation without external binaries/apps/credentials/environments.

## Success Metrics (verified 2026-11-06)
- **Skills validated:** 12/12 (100%)
- **Default tests:** 412 passed, 23 deselected (integration opt-in)
- **Converged (defined scope):** 001, 003, 004, 005, 006-MCP, 007 ✓
- **MCP minimum viable (stdio, mock-first):** ✓
- **Authorized local real MCP smoke (PhotoCraft, stateless, scoped):** ✓
- **Stateful MCP artifact cycle (Option B):** pending
