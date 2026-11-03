# Problem Definition: ArtCraft Skills Suite - Extensive Creative Asset Skills

- **Slug**: artcraft-skills-suite-intake
- **Created**: 2026-11-03
- **Updated**: 2026-11-03
- **Inputs used**: intake.md | research.md | user input only

## Problem Statement

Artists, creators, and AI agent users working with creative asset pipelines struggle with fragmented tooling across different asset types and applications - there is no unified, composable way to leverage AI capabilities for creation, editing, manipulation, and development of assets across the full creative workflow (2D, 3D, video, audio, CAD, documents/presentations). This fragmentation prevents seamless cross-application workflows and makes it difficult to build end-to-end creative pipelines with AI assistance. MDMV projects face similar challenges with asset workflows and need reusable, composable AI capabilities.

## Affected Users & Stakeholders

- **Users**: Digital artists, illustrators, 3D artists, filmmakers/motion designers, game developers, product designers, technical illustrators — need unified creative workflows across asset types without switching between disconnected tools
- **Users**: AI coding agent users (Claude Code, Cursor, Codex, Gemini, OpenCode, and others) — need composable creative capabilities integrated into their agent workflows following agentskills.io patterns
- **Users**: MDMV team members working on projects (tirateima_fc, crsdd-fabro, MDMV-AI-Stack, etc.) — need reusable AI-assisted asset/documentation workflows (evidence packaging, branding assets, diagrams, technical docs). [NEEDS CLARIFICATION: specific prioritized MDMV workflows]
- **Stakeholders**: ArtCraft project maintainers — need to extend ArtCraft ecosystem with extensible skill capabilities following the established philosophy
- **Stakeholders**: Open source community — benefit from vendor-neutral, composable creative skills compatible with multiple agents

## Goals

- Enable composable, agent-accessible skills for creative asset workflows across all major asset types (2D/raster/vector, 3D/spatial, video/motion, audio, documents/presentations, CAD/technical)
- Provide seamless integration across ArtCraft products (15 crafting apps) and enable cross-product workflows
- Support the "build before generating" / composition-first philosophy with precise creative control
- Maintain vendor-neutral, model-agnostic approach supporting ArtCraft's 60+ model ecosystem and beyond
- Follow agentskills.io standard for maximum cross-agent compatibility
- Create a foundation that can serve MDMV's initial needs while remaining general-purpose for the broader community
- Follow ArtCraft Skills constitution principles (composability, interoperability, artist-centric design, transparency, cost awareness)
- Handle async job-based generation properly with cost estimation and credential management

## Non-Goals

- Building a monolithic creative application (ArtCraft apps already exist)
- Creating proprietary, vendor-locked skills
- Replacing existing ArtCraft functionality
- Building MDMV-specific skills that cannot be generalized (MDMV needs guide ROADMAP/OBJETIVOS, not constitution)
- Creating skills for non-creative/asset workflows outside the defined scope
- Duplicating entire applications as skills
- Supporting only a single agent framework

## Success Metrics

- **Coverage**: Skills exist for major asset types across ArtCraft product categories (baseline: 0 comprehensive skills suite; target: [NEEDS CLARIFICATION: specific coverage goals])
- **Composability**: Skills can be chained/composed into cross-product workflows following atomic+orchestrator pattern (baseline: unknown; target: [NEEDS CLARIFICATION])
- **Agent Compatibility**: Works across Claude Code, Cursor, Codex, Gemini, OpenCode and follows agentskills.io (baseline: 0; target: broad compatibility)
- **Interoperability**: Integrates with ArtCraft APIs/services where appropriate while remaining usable standalone (baseline: unknown; target: [NEEDS CLARIFICATION])
- **Adoption**: Usage by agent users and integration into workflows (baseline: 0; target: [NEEDS CLARIFICATION])
- **MDMV Utility**: Successfully supports identified generalizable MDMV project needs (baseline: unknown; target: [NEEDS CLARIFICATION])

## Cost of Inaction

Without a unified skills suite, artists and agent users continue to face fragmented workflows across different tools and asset types. Manual orchestration of creative pipelines remains necessary, preventing efficient AI-assisted creative work. MDMV projects lack standardized, reusable AI capabilities for asset creation and documentation workflows. The opportunity to create a composable, open-source creative skill ecosystem aligned with ArtCraft's philosophy and compatible with the broader agent ecosystem is missed.

## Open Questions

- [NEEDS CLARIFICATION: What skill format/structure does this repo expect specifically? Commands use frontmatter+markdown with different packaging; need to define canonical schema/loader for artcraft-skills repo]
- [NEEDS CLARIFICATION: Should skills integrate directly with ArtCraft APIs/services (artcraft-services) or be tool-agnostic abstractions? Or both with adapters?]
- [NEEDS CLARIFICATION: What are the concrete MDMV workflows to prioritize initially (tirateima_fc evidence packaging, crsdd-fabro patterns, etc.) while keeping skills generalizable?]
- [NEEDS CLARIFICATION: Which ArtCraft products/apps are highest priority for initial skill coverage?]
- [NEEDS CLARIFICATION: Granularity boundaries - where does atomic skill end and orchestrator begin? How to structure cross-product integration skills?]
- [NEEDS CLARIFICATION: What is the loading mechanism in this repo and how does it differ from commands mode?]
- [NEEDS CLARIFICATION: Testing strategy for creative skills (especially non-deterministic generation, async jobs)?]
- [NEEDS CLARIFICATION: How to handle authentication/credentials across different contexts (local agents, ArtCraft app integration)?]
- [NEEDS CLARIFICATION: Priority order for asset types to implement first?]
- [NEEDS CLARIFICATION: Should skills be distributed as part of this repo or consumed by external agents? Both?]
