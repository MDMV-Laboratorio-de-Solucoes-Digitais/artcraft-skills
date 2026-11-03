# Decision: ArtCraft Skills Suite - Extensive Creative Asset Skills

- **Slug**: artcraft-skills-suite-intake
- **Decided**: 2026-11-03
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | Clear problem: fragmented creative tooling across asset types/apps, need for composable AI-assisted workflows. Aligns with ArtCraft's "IDE for artists" philosophy. MDMV needs provide validation. |
| Evidence strength | strong | Extensive research from ArtCraft ecosystem (repos, apps, APIs), agentskills.io standard, external implementations (Scenario, Blender MCP, ComfyUI MCP), internal MDMV analysis. Well-documented patterns exist. |
| Value vs. inaction | strong | Doing nothing means continued fragmentation; unified skills suite would enable cross-product workflows, agent compatibility, serve both community and MDMV needs. |
| Feasibility / appetite | adequate | Option A (foundation-first) is reasonable. Roadmap exists. Main unknowns are repo-specific (skill loader/schema) but patterns are clear from agentskills.io and existing codebase. |
| Strategic fit | strong | Perfectly aligned with ArtCraft Skills Constitution v2.0.0 (composability, interoperability, artist-centric, crafting over generating). Follows established standards. |
| Risk posture | adequate | Risks identified and mitigable (foundation-first approach, atomic+orchestrator pattern, generalizable design). Some unknowns remain but can be resolved during specification. |

## Verdict & Rationale

**go** - The idea is strong and well-aligned with ArtCraft's philosophy and constitution. Extensive research shows clear patterns (agentskills.io standard, ArtCraft APIs, composable architecture). Foundation-first approach with atomic skills + orchestrators is sound. MDMV needs provide concrete validation while keeping skills general-purpose. Remaining clarifications can be resolved during `/speckit.specify` phase.

## If go — Handoff to `/speckit.specify`

- **Problem**: Artists, creators, and agent users need unified, composable AI skills for creative asset workflows across fragmented tools/apps. MDMV projects need reusable generalizable capabilities.
- **Chosen approach**: Option A - Foundation First (Composability-Focused Core). Define skill schema following agentskills.io, build core abstractions (metadata/loading/composition/model-provider abstraction/ArtCraft API adapters), create atomic skills with orchestrators on top.
- **In scope**: Skill schema/structure/loading mechanism, core utilities, model/provider abstraction, ArtCraft API integration patterns, atomic skills for key asset types, cross-product composition patterns, agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode), MDMV-validated generalizable workflows
- **Out of scope**: Full coverage of all 15 apps initially, MDMV-specific skills, full orchestration UI, supporting every agent framework at once, duplicating entire apps as skills
- **Success metrics**: Composable skills following agentskills.io, cross-agent compatible, integrate with ArtCraft ecosystem, serve generalizable MDMV needs, follow constitution principles
- **Carried-forward open questions**: 
  - [NEEDS CLARIFICATION: Canonical skill schema/loader for this repo vs agentskills.io - how to adapt to Spec Kit/commands infrastructure?]
  - [NEEDS CLARIFICATION: Integration approach - direct ArtCraft APIs vs tool-agnostic abstractions with adapters?]
  - [NEEDS CLARIFICATION: Which generalizable MDMV workflows to prioritize?]
  - [NEEDS CLARIFICATION: Priority order for ArtCraft products/asset types?]
  - [NEEDS CLARIFICATION: Authentication/credentials across contexts?]
  - [NEEDS CLARIFICATION: Testing strategy for non-deterministic operations?]
  - [NEEDS CLARIFICATION: Distribution model - part of repo consumed by external agents?]
