# Research: Shared CLI/MCP Adapter

## Decisions

**Decision 1: API Style**
- Chosen: Function-based module (module with functions)
- Rationale: Stateless utilities, composable, Pythonic, matches current implementation. Class-based not needed for current use cases.
- Alternatives: Class-based `ArtcraftAppClient`, hybrid approach

**Decision 2: Module Location**
- Chosen: `skills/core/artcraft_app_client.py`
- Rationale: Core utilities live in `skills/core/`, infrastructure not a skill itself
- Alternatives: In image-generate, in separate package

**Decision 3: Extraction Scope**
- Chosen: Extract CLI discovery, command discovery/filtering, CLI invocation, MCP normalization/config helpers, output normalization, error patterns
- Rationale: These are shared patterns used by all creative skills
- Alternatives: Extract everything including MCP method stubs (MCP has app-specific details, keep stubs in skill for now)

## Findings

- Existing patterns in core are mixed (some classes, some functions) - function-based is fine
- All tests pass with function-based approach
- No new dependencies needed
