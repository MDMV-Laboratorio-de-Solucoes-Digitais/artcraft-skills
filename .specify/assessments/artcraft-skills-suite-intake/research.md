# Idea Research: ArtCraft Skills Suite - Extensive Creative Asset Skills

- **Slug**: artcraft-skills-suite-intake
- **Created**: 2026-11-03
- **Updated**: 2026-11-03
- **Evidence confidence (overall)**: high

## Users & Demand

- **Artists/creators want control, not just generation** — ArtCraft's philosophy is "IDE for artists" with "build before generating", composition-first workflows (2D/3D compositing, scene blocking, kitbashing). Users want precise control over composition, character identity, camera placement. [source: https://getartcraft.com/, https://raw.githubusercontent.com/storytold/artcraft/main/README.md | cited] (confidence: high)
- **Multi-modal creative workflows are complex** — Artists mix images, 3D models, cutouts, environments, audio/video. Current tools fragmented across apps. Need for unified workflows. [source: https://getartcraft.com/apps, README.md | cited] (confidence: high)
- **Agent/AI assistant users want composable creative capabilities** — Growing demand for skills that work with Claude Code, Cursor, Codex, Gemini, OpenCode etc. for creative tasks. [source: skills ecosystem patterns, ArtCraft Skills constitution | cited] (confidence: high)
- **MDMV needs** — Multiple projects (tirateima_fc, crsdd-fabro, MDMV-AI-Stack, casv-rust) have concrete workflows needing asset/automation capabilities. tirateima_fc needs evidence packaging/WhatsApp delivery; crsdd-fabro needs deterministic workflows; cross-project needs for branding, diagrams, asset pipelines. [source: internal codebase analysis | cited] (confidence: high)

## Prior Art

- **ArtCraft monorepo (storytold/artcraft)** — Tauri desktop app (Rust + TS), supports images, video, 3D meshes, Gaussian splats/worlds, multiple providers (ArtCraft, Grok, Midjourney, Sora). Has comprehensive model catalog (62+ models). [source: https://github.com/storytold/artcraft | cited] (confidence: high)
- **ArtCraft Services (storytold/artcraft-services)** — Backend API, workers, provider routing (`artcraft_router`), billing/credits. Well-architected with clear patterns (session auth `/v1/omni_gen/*`, API key auth `/v1/omni_api/*`, async jobs via webhooks/polling). [source: https://github.com/storytold/artcraft-services | cited] (confidence: high)
- **Crafting Apps Suite** — 15 open-source Rust apps (PhotoCraft, VectorCraft, FilmCraft, TextureCraft, CADCraft, DeckCraft, SoundCraft, etc.), all native + WASM, local-first, agent-ready (CLI/JSON/MCP). [source: https://getartcraft.com/apps | cited] (confidence: high)
- **Skills ecosystems** — Anthropic Agent Skills (agentskills.io standard), skills.sh ecosystem, Claude Code skills, Codex skills. Many ad/marketing focused skills exist; fewer comprehensive creative asset suites. Scenario Labs has good patterns (expert teams, orchestrators, evals). [source: external research, agentskills.io | cited] (confidence: high)
- **Creative tool ecosystems** — Blender (open source 3D), Krita, Godot have strong plugin ecosystems. Blender MCP, ComfyUI MCP show good integration patterns. [source: external research | cited] (confidence: high)
- **MDMV internal patterns** — Existing skills in MDMV-AI-Stack (`mdmv-mode`, `tdd`, `verify-loop`, `unslop`, `unstick`) show agent skill patterns in use. Spec Kit extensions/commands show dual commands/skills packaging. [source: internal codebase | cited] (confidence: high)

## Market & Context

- **AI creative tools landscape** — Rapid evolution with many models/providers. Users want choice and control, not lock-in. ArtCraft positions as "IDE for artists" vs model aggregation sites. [source: https://getartcraft.com/, README | cited] (confidence: high)
- **Fragmentation problem** — Artists use multiple tools for different asset types. Need for unified workflows and cross-app integration. [source: ArtCraft philosophy, apps page | cited] (confidence: high)
- **Skills/agent extensibility gap** — Few comprehensive, composable skill suites for full creative pipeline. Most skills are narrow/single-purpose. Opportunity for well-architected suite following agentskills.io standard. [source: skills.sh search results, external research | cited] (confidence: high)
- **Cost of doing nothing** — Continued tool fragmentation, manual asset pipeline orchestration, lack of agent-assisted creative workflows. [source: inferred from ArtCraft philosophy | ASSUMPTION] (confidence: medium)

## Data & Constraints

- **ArtCraft supports 60+ models** across images (16), video (25), audio/music (5), 3D meshes (11), worlds/splats (5). Wide provider coverage via ArtCraft router. [source: README model catalog | cited] (confidence: high)
- **Tech stack** — Rust (performance), Tauri, TypeScript/React, Nx. Skills need to be compatible with agent environments. [source: artcraft AGENTS.md, README | cited] (confidence: high)
- **Open source licensing** — MIT/Apache-2.0 dual license. Must respect licenses. [source: README, constitution | cited] (confidence: high)
- **Constitution exists** — ArtCraft Skills has v2.0.0 constitution emphasizing crafting over generating, composability, interoperability, transparency/cost awareness. Skills must comply. [source: .specify/memory/constitution.md | cited] (confidence: high)
- **Agent compatibility required** — Must support Claude Code, Cursor, Codex, Gemini, OpenCode, and others per constitution. agentskills.io standard provides common ground. [source: constitution, external research | cited] (confidence: high)
- **MDMV projects exist locally** — Multiple projects under ~/development/MDMV/projetos/ with concrete needs. Must guide ROADMAP/OBJETIVOS but not appear in constitution. [source: filesystem, internal analysis | cited] (confidence: high)
- **Skill format undefined** — No SKILL.md files exist yet in repo. Commands use frontmatter+markdown; skills mode packages differently (per github extension). Need to define canonical schema in Phase 0. [source: internal analysis | cited] (confidence: high)

## Evidence Against the Idea

- **Scope is very large** — Covering all asset types, all ArtCraft products, cross-product integration is a massive undertaking. Risk of scope creep. [source: inferred from README/apps scope | ASSUMPTION] (confidence: high)
- **Maintenance burden** — Skills need updating as models/providers change rapidly. Need clear architecture and governance. [source: general ecosystem observation | ASSUMPTION] (confidence: medium)
- **Fragmentation of skills systems** — Different agents may expect different skill formats. Need framework-agnostic approach or broad compatibility following agentskills.io. [source: external research | ASSUMPTION] (confidence: medium)
- **MDDMV-specific needs may conflict with generality** — Need to balance serving initial use cases without making suite MDMV-specific. Constitution says MDMV must guide ROADMAP/OBJETIVOS but not appear in constitution. [source: user request | cited] (confidence: high)
- **Existing skills may overlap** — Some functionality might already exist in skills ecosystem. Need to check for duplication vs differentiation. [source: skills.sh search | cited] (confidence: medium)
- **Integration complexity** — ArtCraft has complex async job-based API, multiple auth modes, credential management. Skills need to handle this properly. [source: artcraft-services analysis | cited] (confidence: high)

## Gaps & Open Questions

**RESOLVED by research:**
- Skill format follows agentskills.io standard (SKILL.md with YAML frontmatter: name, description required; optional license, compatibility, metadata, allowed-tools). Directory structure with scripts/references/assets. Progressive disclosure model.
- Agent compatibility: must support Claude Code, Cursor, Codex, Gemini, OpenCode etc. Follow agentskills.io for portability.
- Integration patterns: MCP-first where available (Blender, ComfyUI), API wrappers for ArtCraft services, handle async jobs/polling, cost awareness, credential management.
- Granularity: atomic skills by default, orchestrator/workflow skills on top for composition. Cross-product via shared asset/context/style layers and capability composition.
- ArtCraft ecosystem: 15 crafting apps, 60+ models, Tauri desktop + web + services APIs.

**STILL NEEDS CLARIFICATION:**
- [NEEDS CLARIFICATION: What skill format/structure does this specific repo expect? Commands use different packaging; need to define canonical schema for artcraft-skills repo specifically]
- [NEEDS CLARIFICATION: Should skills integrate directly with ArtCraft APIs/services (artcraft-services) or be tool-agnostic abstractions? Or both with adapters?]
- [NEEDS CLARIFICATION: What are the concrete MDMV workflows to prioritize initially? tirateima_fc (evidence/WhatsApp), crsdd-fabro patterns, others - need specific prioritization]
- [NEEDS CLARIFICATION: Which ArtCraft products/apps are highest priority for initial skill coverage?]
- [NEEDS CLARIFICATION: Granularity boundaries - where does atomic skill end and orchestrator begin for specific use cases?]
- [NEEDS CLARIFICATION: How to structure cross-product integration skills concretely?]
- [NEEDS CLARIFICATION: What is the loading mechanism in this repo? How does it differ from commands mode?]
- [NEEDS CLARIFICATION: Testing strategy for creative skills (especially non-deterministic generation)?]

## Sources

- https://getartcraft.com/ (host: getartcraft.com, policy: allowlisted) - cited
- https://getartcraft.com/apps (host: getartcraft.com, policy: allowlisted) - cited
- https://getartcraft.com/tutorials (host: getartcraft.com, policy: allowlisted) - cited
- https://github.com/storytold/artcraft (host: github.com, policy: allowlisted) - cited
- https://github.com/storytold/artcraft-services (host: github.com, policy: allowlisted) - cited
- https://raw.githubusercontent.com/storytold/artcraft/main/README.md (host: raw.githubusercontent.com, policy: allowlisted) - cited
- https://raw.githubusercontent.com/storytold/artcraft/main/AGENTS.md (host: raw.githubusercontent.com, policy: allowlisted) - cited
- https://agentskills.io/ (host: agentskills.io, policy: allowlisted) - cited
- https://github.com/anthropics/skills (host: github.com, policy: allowlisted) - cited
- https://github.com/scenario-labs/skills (host: github.com, policy: allowlisted) - cited
- https://github.com/sandraschi/blender-mcp (host: github.com, policy: allowlisted) - cited
- https://docs.comfy.org/agent-tools/mcp (host: comfy.org, policy: allowlisted) - cited
- skills.sh search results (local command) - cited
- /home/luis/development/artcraft-skills/.specify/memory/constitution.md (local) - cited
- /home/luis/development/MDMV/ and /home/luis/development/MDMV/projetos/ (local filesystem) - cited
- Agent research results (internal scouts) - cited
