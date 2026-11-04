# Decision: Shared CLI/MCP adapter for ArtCraft apps

- **Slug**: shared-cli-mcp-adapter
- **Created**: 2026-11-04
- **Decision**: GO
- **Decided by**: assessment pipeline

## Summary

GO to proceed with Option A: extract CLI/MCP integration logic from `skills/creative/image-generate/skill.py` into `skills/core/artcraft_app_client.py` and refactor image-generate to use it. This is the 80/20 move that unlocks the entire creative skill family with low effort and low risk.

## Rationale

- **Problem validated**: CLI/MCP logic is coupled to image-generate; future skills need same patterns (Constitution v2.1.0 requires CLI/MCP-only)
- **Evidence strong**: Working implementation exists, tests pass (23/23), patterns match core utilities approach
- **Best option**: Option A maximizes impact/minimizes effort vs duplicating or doing nothing
- **Low risk**: Pure refactor with existing test coverage

## Conditions / Next Steps

- Proceed to `/speckit.specify` or direct implementation following the plan
- Keep API simple and flexible, driven by proven patterns
- Validate with all tests after refactor
- Ensure module lives in `skills/core/` as infrastructure (not a BaseSkill)

## Risks Accepted

- Minor API design choices now that may need adjustment for future skills (acceptable - can evolve)
- Refactor could introduce subtle bugs (mitigated by comprehensive tests)
