# Concept: Shared CLI/MCP adapter for ArtCraft apps

- **Slug**: shared-cli-mcp-adapter
- **Created**: 2026-11-04
- **Recommended option**: Option A — Extract shared module and refactor image-generate

## Options

### Option A — Extract shared module and refactor image-generate (Recommended)
- **Sketch**: Create `skills/core/artcraft_app_client.py` extracting CLI discovery, command filtering, mode selection (auto/cli/mcp), invocation, MCP helpers, output normalization, and error handling from `skills/creative/image-generate/skill.py`. Refactor image-generate to use the shared module while preserving exact behavior and API.
- **Appetite**: small (days)
- **Trade-offs**: Wins - eliminates duplication, enables future skills, standardizes patterns, low risk. Sacrifices - small upfront refactor time, need to design flexible API.
- **Rabbit holes**: Over-engineering the API to be "perfect" for all future skills; need to keep it simple and driven by current proven patterns.

### Option B — Duplicate for now, extract later
- **Sketch**: Create image-edit (and others) by copying image-generate's CLI/MCP logic with minimal changes. Extract to shared module only when we have 2-3 implementations to see common patterns.
- **Appetite**: small now, larger later
- **Trade-offs**: Wins - no upfront refactor risk, faster to add first new skill. Sacrifices - code duplication, inconsistent patterns, harder maintenance, technical debt, more total effort.
- **Rabbit holes**: "Extract later" often never happens or happens with poor design; harder to refactor once multiple copies exist.

### Option C — Do nothing
- **Sketch**: Keep CLI/MCP logic coupled in image-generate. Each new skill reimplements or copies as needed.
- **Appetite**: none
- **Trade-offs**: Wins - no work now. Sacrifices - violates DRY, contradicts goal of efficient skill development, will slow down all future creative skills.
- **Rabbit holes**: N/A

## Recommendation

**Option A** is strongly recommended. It has maximum impact with minimum effort (80/20) - we already have a proven working implementation to extract from, tests exist to validate behavior, and Constitution v2.1.0 mandates CLI/MCP-only integration making this critical infrastructure. The refactor is low-risk and unlocks the entire creative skill family.

## Out of Scope (for the recommended option)

- API integration (forbidden by Constitution v2.1.0)
- Creating BaseSkill wrapper for the client (it's infrastructure)
- Supporting async patterns (keep synchronous to match current implementation)
- Building for hypothetical future apps beyond extracting what's needed for ArtCraft CLI/MCP patterns

## Assumptions to Validate

- The extracted API will be flexible enough for image-edit, background-remove, image-upscale without major changes
- MCP transport details are sufficiently similar across ArtCraft apps to abstract cleanly
- Refactoring won't break any tests (mitigated by existing test suite)
