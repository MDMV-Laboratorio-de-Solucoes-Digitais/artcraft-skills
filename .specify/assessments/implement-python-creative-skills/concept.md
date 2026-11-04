# Concept: Executable Python creative skills via shared adapter

- **Slug**: implement-python-creative-skills
- **Created**: 2026-11-04
- **Recommended option**: Option A

## Options

### Option A — Implement 4 skill.py files directly (copy/adapt image-generate template)
- **Sketch**: Each of the 4 creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) gets a Python `skill.py` that follows the `image-generate/skill.py` template: imports `artcraft_app_client`, defines a `BaseSkill` subclass with `get_input_schema`, `get_output_schema`, `validate_inputs`, `_execute_cli`, `_execute_mcp`, `execute`, and `__all__`. Each skill resolves its generation command via keyword matching, invokes the CLI with a timeout, normalizes output, and degrades gracefully when CLI/MCP is unavailable using reason codes.
- **Appetite**: small (days)
- **Trade-offs**: Wins — lowest effort, proven pattern (image-generate already works), immediate reusability proof (SC-005), Phase 1 advances ~25%→~80%. Sacrifices — code duplication across 4 files (~200 lines each), no shared base class means future changes must be mirrored. Risks — SKILL.md-declared schemas may drift from skill.py schemas; command keywords are guesses unless validated against photocraft-cli output.
- **Rabbit holes**: Extracting a shared base class (scope creep), adding skill-specific params beyond what SKILL.md declares, trying to match photocraft-cli's 500+ commands exactly.

### Option B — Extract a shared base class first, then implement 4 skills on top
- **Sketch**: Create a `CreativeSkill` base class in `skills/core/` that encapsulates the discover→resolve→invoke→normalize→degrade flow parameterized by name, description, keywords, and param builder. Then each of the 4 skills is a thin ~30-line subclass.
- **Appetite**: medium (1–2 weeks)
- **Trade-offs**: Wins — no duplication, single point of change for the adapter flow, cleaner for future skills. Sacrifices — higher upfront effort, base class design decisions (what's parameterized vs. hardcoded) risk over-engineering, delays the 4 executable skills. Risks — base class may not fit all 4 skills equally well, requiring refactoring mid-implementation.
- **Rabbit holes**: Designing the base class API (what methods are overridable, what's concrete), supporting MCP differences across skills, handling skill-specific param schemas in the base class.

### Option C — Do nothing / defer (buy instead of build)
- **Sketch**: Keep the 4 skills as declarative `SKILL.md` only. Agents consume them via the skill schema without executable code. Revisit `skill.py` implementation when a real consumer needs it.
- **Appetite**: small (days — zero implementation effort)
- **Trade-offs**: Wins — zero implementation cost, no duplication, no maintenance surface. Sacrifices — adapter reusability (SC-005) stays unproven with only one consumer, agents can't invoke 4/5 creative skills, Phase 1 stays at ~25%, downstream capabilities (US4, US5, Phases 2–5) remain blocked.
- **Rabbit holes**: None (no implementation).

## Recommendation

**Option A** — Implement the 4 `skill.py` files directly by copying/adapting the `image-generate` template.

Rationale: It directly addresses all goals in the problem definition (4 executable skills, adapter reuse, graceful degradation, Phase 1 advancement, SC-005 proof) with the lowest effort. Option B's base class adds upfront design risk and delays delivery without clear evidence that 4 skills need shared behavior beyond what the adapter already provides. Option C leaves the problem unsolved. Option A's code duplication is acceptable as a first step; a base class can be extracted later if a 5th+ skill needs the same pattern.

## Out of Scope (for the recommended option)

- Implementing MCP transport inside the adapter (FR-005: MCP discovery/invocation stay skill-level)
- Creating new skill categories (video, audio, 3D beyond mesh-generate, CAD, documents — Phases 3–5)
- Building provider backends or reimplementing ArtCraft APIs
- Refactoring `image-generate/skill.py` (already works, must remain unchanged)
- Extracting a shared base class (deferred; can be revisited after 4 skills exist)

## Assumptions to Validate

- The `image-generate/skill.py` template pattern is appropriate for all 4 skills (each skill's domain differs — editing vs. background removal vs. upscaling vs. mesh generation)
- `discover_cli_commands` + keyword matching will find the right command for each skill in photocraft-cli's 500+ command registry
- Skill-specific params (mask, scale, format) can be added without breaking the template pattern
- The 4 SKILL.md files' declared inputs/outputs are accurate and stable enough to build against
