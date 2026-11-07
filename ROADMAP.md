# ArtCraft Skills Roadmap

## Vision

Build a comprehensive, open-source ecosystem of AI agent skills for creative asset creation, manipulation, and development — empowering artists and creators with tools that enhance intentional crafting across the entire creative pipeline. Skills follow the [agentskills.io](https://agentskills.io) standard for broad agent compatibility and embody ArtCraft’s philosophy of “turning prompting into crafting”.

Skills are consumed by agents that drive real ArtCraft creative apps (PhotoCraft, PdfCraft, and other Rust “Crafting Apps” in the `storytold` org) through **CLI** and **MCP server** surfaces, plus ArtCraft’s AI studio. This repo is the skill/agent layer on top of those surfaces (no separate generation backend).

## Current State (Verificado — 2026-11-06)

- **Branch:** `dev` (local clean; 2026-11-06: 10 commits ahead of `origin/dev` published in this execution upon explicit authorization). PR stack 007 #131–#135 previously integrated; only `dev`/`main` local+remote. Working tree reviewed for docs consolidation (MDMV flow 2026-11-06).
- **Quality gates (default):** **424 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`); **12/12 skills validated** (`python scripts/validate_all_skills.py`). Integration tests are opt-in (`-m "not integration"` excluded by default).
- **Converged specs (defined scope):** `001`, `003`, `004`, `005-resiliencia-creativeskill` (evidence recorded), `006-mcp-stdio-functional-integration`, `007-photocraft-mcp-smoke` (Option A stateless, T001–T023 complete; SC-001 exercised locally under explicit authorization — engine/editor only, no AI/provider/model claim).
- **Core:** schema/validation/loader/registry, `BaseSkill/SkillResult`, `CreativeSkill`, shared `artcraft_app_client` (CLI + MCP stdio minimum viable, FR-005/FR-006 preserved), resilience (retry 3 + exponential backoff + jitter + `BoundedSemaphore(3)`), `SkillComposer`, `DAGOrchestrator`.
- **Creative skills (Python, current scope):** `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`; `scene-composition` executable; generalizable workflows present.
- Conformidade agentskills.io: 12/12 skills validadas (`SKILL.md` YAML frontmatter, name kebab-case, description 1–1024 chars, progressive disclosure).
- MCP stdio mínimo viável (006) implementado e alinhado com MCP 2025-11-25 e revisão 2026-07-28 (_meta obrigatório, server/discover, sem handshake/sessão na nova revisão, tools/list com paginação/caching, tools/call com input_required).
- MCP Python SDK v2.3.0 (`modelcontextprotocol/python-sdk`) avaliado como candidato; cliente mínimo atual preservado por back-compat/mock-first.
- PhotoCraft `photocraft-cli 0.20.1` (2026-11-03) observado localmente: 26 MCP tools via `tools/list`, `command_list` com engine command metadata, `doc_inspect` com sessão não-persistente entre chamadas separadas do adapter.
## Progress Summary

**Overall:** **~95% of foundational scope + minimum viable MCP stdio integration + authorized local real-path smoke (PhotoCraft, stateless)**. Conformity with agentskills.io (12/12 skills validated) and alignment with MCP 2026-07-28 (_meta, server/discover, stateless-by-design). Not 100% of product: multi-app/environment operational validation, stateful MCP (Option B), deep per-app capability mapping, domain expansion (Phases 3–5), and product adoption docs remain.

**Completed (✓):**
- **Phase 0 Foundation**: schema/validation/loader/registry, core abstractions, composer/DAG, docs, deterministic test infrastructure.
- **006 MCP stdio (minimum viable, mock-first):** `tools/list`/`tools/call` transport path in adapter, `SkillResult` normalization, FR-005 selection/back-compat (explicit `mcp` no silent CLI reroute; `auto` CLI-first preserved), FR-006 additive reason/metadata taxonomy, deterministic tests.
- **007 PhotoCraft MCP smoke (Option A, stateless, opt-in):** test-only harness reusing 006 adapter; safe temp roots/cleanup, bounded timeout, explicit authorization; real local evidence recorded for `tools/list` + `command_list` (**engine/editor automation only; no AI/provider/model/artifact-cycle/default-CI claim**).
- **Resilience + fallback:** retry/backoff/jitter/semaphore; `generate_via_editing_commands` graceful degradation.
- **Creative skills/workflows (current scope):** 5 creative Python skills + scene-composition + generalizable workflows; **12/12 skills validated**.

**Backlog / caveats:**
- `specs/005-resiliencia-creativeskill/tasks.md`: implementation checkboxes partially marked while convergence evidence exists — **reconcile checkboxes/evidence** (doc hygiene).
- `specs/006-integracao-geracao-assets` (0/11) vs `006-mcp-stdio-functional-integration` — **historical `006-*` numbering ambiguity**; normalize references in specs 006/007 and quickstarts to avoid numbering confusion, without rewriting history.
- `README.md` (root) not present — adoption/onboarding gap.

## Roadmap Phases

### Phase 0: Foundation — **100% Complete**
- [x] agentskills.io schema/validation/discovery/loading/registry
- [x] Core abstractions, shared adapter, resilience, composition/DAG
- [x] Docs and deterministic test infrastructure (**424 passed / 23 deselected**, **12/12 valid**)

### Phase 1: Image & 2D Creative Skills — **100% (current scope)**
- [x] `image-generate`, `image-edit`, `background-remove`, `image-upscale`
- [ ] Vector & Illustration (future)
- [ ] Style Transfer & Consistency (future)
- [ ] Avaliar decisão de dependência MCP SDK v2 vs cliente mínimo (manter mock-first/back-compat).

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
- [x] **009 / 007 Option B (spec + additive runtime mock-first, 2026-11-06):** `mcp_stateful_session`/`MCPStatefulSession` em `skills.core.artcraft_app_client` (subprocesso stdio retido, ids correlacionados, cleanup bounded, FR-006); testes determinísticos `tests/unit/test_mcp_stateful_session_009.py`. Preserva 006 stateless/FR-005/FR-006/schemas. Validação real futura permanece opt-in/007. **Sem IA/bridge/UI/CI-default real.**
- [ ] Per-capability MCP mapping for Crafting Apps (tools/roots/progress/cancel/format constraints)
- [ ] Controlled optional CI/manual job for real MCP smoke (never default), secure evidence handling
- [ ] Batch processing, project templates, deep app integrations
- [ ] Alinhar adapter com revisão MCP 2026-07-28 (_meta, server/discover, sem handshake na nova revisão).

1. **009 (concluído, 2026-11-06):** runtime aditivo stateful MCP (`mcp_stateful_session`/`MCPStatefulSession`), TDD/mock-first, preservando contratos 006/FR-005/FR-006/schemas; gates default verificados **424 passed, 23 deselected**, **12/12**. Validação real artefato continua opt-in (007/008).
2. **80/20 anterior (MDMV 2026-11-06): spec `008-photocraft-capability-mapping`** — PhotoCraft MCP capability mapping (tools `command_*`/`doc_*`/preview/resources, roots, progress `_meta.progressToken`, cancellation `notifications/cancelled`, error semantics, protocol/version limits). Spec/docs only in this slice; **no runtime code, no AI-generation claim, no stateful session** (007 Option B deferred). Mock-first; optional real validation opt-in. Contingency: if maintainer prioritizes stateful MCP, replace with 007 Option B spec/decide.
3. **Reconcile Speckit doc hygiene** (low risk): 005 checkbox/evidence alignment; clarify `006-*` numbering in docs; keep history intact.
4. **(feito em 009 spec/runtime aditivo mock-first) Spec/decide 007 Option B** (stateful MCP session, narrow) if stateful artifact workflows become priority; preserve public contracts and mock-first defaults; consider MCP 2026-07-28 (no handshake/session server-side; multi-round-trip client-side).
5. **Deepen real capability mapping implementation follow-ups** (PhotoCraft first, post-008): engine-oriented `command_*`/`doc_*`/preview/resource tools, roots/progress/cancellation/error semantics; no AI-generation overclaim.
6. **MCP dependency decision (only if needed):** evaluate official Python SDK (`modelcontextprotocol/python-sdk` v2.3.0) vs current minimal client for advanced lifecycle/auth/Streamable HTTP; maintain deterministic tests/back-compat.
7. **Product adoption:** compatibility matrix (Crafting Apps/MCP/protocol versions), examples/onboarding; expand Phases 3–5 after stable mappings.


## What this project does NOT do
- No model/provider/backend reimplementation; no replacement of ArtCraft apps.
- No real MCP smoke in default CI; opt-in + explicit authorization + safety controls only.
- No AI generation/provider/model/prompt claim via local PhotoCraft MCP smoke path (007 = engine/editor stateless).
- No stateful MCP artifact cycle in current adapter (Option B deferred).
- No guaranteed operation without external binaries/apps/credentials/environments.

## Success Metrics (verified 2026-11-06)
- **Skills validated:** 12/12 (100%)
- **Default tests:** 424 passed, 23 deselected (integration opt-in)
- **Converged (defined scope):** 001, 003, 004, 005, 006-MCP, 007 ✓
- **MCP minimum viable (stdio, mock-first):** ✓
- **Authorized local real MCP smoke (PhotoCraft, stateless, scoped):** ✓
- **Stateful MCP session helper (009, additive, mock-first):** ✓ (runtime + deterministic tests); real artifact cycle opt-in pending
- ✅ Conformidade agentskills.io: 12/12 skills validadas
- ✅ MCP stdio mínimo viável alinhado com MCP 2025-11-25 e 2026-07-28
- ⏳ Avaliação MCP SDK v2 — pendente
- ⏳ 007 Option B stateful — pendente
