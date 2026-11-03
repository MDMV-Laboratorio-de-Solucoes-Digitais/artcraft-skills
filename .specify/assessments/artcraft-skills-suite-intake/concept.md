# Concept: ArtCraft Skills Suite - Extensive Creative Asset Skills

- **Slug**: artcraft-skills-suite-intake
- **Created**: 2026-11-03
- **Updated**: 2026-11-03
- **Recommended option**: Option A - Foundation First (Composability-Focused Core)

## Options

### Option A — Foundation First (Composability-Focused Core)
- **Sketch**: Define canonical skill schema following agentskills.io standard adapted for this repo's needs. Build core infrastructure (metadata, loading/discovery, composition/orchestration patterns, model/provider abstraction, ArtCraft API adapters). Create 2-3 atomic skills demonstrating cross-product composition. Focus on architecture that enables everything else.
- **Appetite**: medium
- **Trade-offs**: Wins - solid foundation, follows constitution, reusable patterns, cross-agent compatible via agentskills.io, easier to extend. Sacrifices - slower to show broad coverage, may not immediately cover all ArtCraft products.
- **Rabbit holes**: Over-abstracting schema, trying to support every agent format at once, perfecting abstractions before validating, getting stuck on loader mechanism details.

### Option B — Product-by-Product Coverage
- **Sketch**: Systematically build skills for each ArtCraft product/app in turn, starting with most-used or most-relevant. Each product gets comprehensive skills before moving to next.
- **Appetite**: large
- **Trade-offs**: Wins - broad coverage quickly, directly addresses product needs. Sacrifices - risk of duplication/inconsistency across products, harder to achieve cross-product integration, may miss composability patterns, high maintenance burden.
- **Rabbit holes**: Product silos, inconsistent interfaces, integration becomes afterthought, scope explosion across 15 apps.

### Option C — MDMV-Driven Vertical Slice
- **Sketch**: Identify specific generalizable MDMV workflows (e.g., evidence packaging for tirateima_fc, documentation/diagram generation, asset workflows) and build end-to-end skills while keeping them general-purpose. Validate architecture against real needs.
- **Appetite**: small
- **Trade-offs**: Wins - quick validation, focused scope, demonstrates value with concrete use cases. Sacrifices - risk of over-fitting if not careful, might miss broader ArtCraft ecosystem needs, limited initial coverage.
- **Rabbit holes**: Over-fitting to MDMV specifics, not discovering cross-product opportunities, abstracting too early or too late.

### Option D — Do Nothing / Buy Instead of Build
- **Sketch**: Rely on existing skills ecosystem (skills.sh) and ad-hoc agent capabilities. No dedicated ArtCraft Skills suite.
- **Appetite**: small
- **Trade-offs**: Wins - no maintenance burden. Sacrifices - no integration with ArtCraft ecosystem/apps/APIs, can't leverage composition-first philosophy, no control over skill design, won't serve ArtCraft-specific workflows (scene composition, 3D kitbashing, etc.), fragmentation remains, MDMV needs unmet in unified way.
- **Rabbit holes**: None significant - just opportunity cost.

## Recommendation

**Recommend Option A - Foundation First (Composability-Focused Core)** as the primary approach, with Option C elements for validation.

Rationale:
- Aligns perfectly with ArtCraft Skills Constitution v2.0.0 (composability, modularity, interoperability, agent compatibility)
- Leverages agentskills.io standard for broad cross-agent compatibility (Claude Code, Cursor, Codex, Gemini, OpenCode)
- Addresses core fragmentation problem through proper architecture
- Enables both broad coverage (Option B) and vertical slices (Option C) to be built on solid foundation
- Manageable appetite (medium) with clear patterns to avoid scope explosion
- Positions well for long-term success as ArtCraft ecosystem grows
- Can serve MDMV needs through generalizable skills without making them MDMV-specific

Approach: Define skill schema in Phase 0 (ROADMAP), create core abstractions, build 1-2 generalizable skills validated against MDMV patterns where applicable.

## Out of Scope (for the recommended option)

- Building skills for every ArtCraft product immediately (do iteratively on top of foundation)
- Creating MDMV-specific skills (must be general-purpose; MDMV needs inform design/prioritization only)
- Building full orchestration UI/workflow composer (focus on skill primitives and composition patterns first)
- Supporting every possible agent framework simultaneously (start with agentskills.io compatible agents, design for extensibility)
- Complete coverage of all asset types in first phase
- Deep integration into all 15 apps at once - focus on API-level integration patterns first

## Assumptions to Validate

- [NEEDS CLARIFICATION: Can we adapt agentskills.io standard to work with this repo's Spec Kit/commands infrastructure?]
- [NEEDS CLARIFICATION: What skill format/loader mechanism does this repo expect?]
- [NEEDS CLARIFICATION: How to integrate with ArtCraft APIs (artcraft-services) vs direct tool usage?]
- [NEEDS CLARIFICATION: Which generalizable patterns from MDMV projects to prioritize for validation?]
- [NEEDS CLARIFICATION: What's the priority order for initial skill development?]
- [NEEDS CLARIFICATION: How to handle authentication/credentials across agent environments?]
- [NEEDS CLARIFICATION: Testing strategy for non-deterministic creative operations?]
- [NEEDS CLARIFICATION: Should skills be self-contained or depend on ArtCraft CLI/tools?]
