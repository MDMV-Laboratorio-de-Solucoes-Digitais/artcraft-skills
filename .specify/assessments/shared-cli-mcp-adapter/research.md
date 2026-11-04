# Idea Research: Shared CLI/MCP adapter for ArtCraft apps

- **Slug**: shared-cli-mcp-adapter
- **Created**: 2026-11-04
- **Evidence confidence (overall)**: high

## Users & Demand

- **Internal team need**: Constitution v2.1.0 mandates CLI/MCP-only integration with ArtCraft apps (no online API). Current image-generate works via CLI/MCP but logic is coupled; upcoming skills (image-edit, background-remove, image-upscale, mesh-generate) will need same patterns. — [source: .specify/memory/constitution.md v2.1.0 | cited] (confidence: high)
- **Avoid duplication**: Duplicating CLI discovery/invocation/MCP calling logic across multiple skills creates maintenance burden and inconsistency. — [source: existing codebase analysis | cited] (confidence: high)

## Prior Art

- **Existing implementation**: `skills/creative/image-generate/skill.py` contains proven patterns - CLI discovery via `shutil.which('photocraft-cli')`, dynamic command discovery via `--help` parsing, mode selection (auto/cli/mcp), MCP tool discovery/calling, output normalization, error handling. All working (23/23 tests passing). — [source: skills/creative/image-generate/skill.py | cited] (confidence: high)
- **Core abstractions pattern**: Project follows shared utilities in `skills/core/` (e.g., `credentials.py`, `asset_handler.py`, `utils.py`) for cross-cutting concerns, not as BaseSkill implementations. — [source: skills/core/ structure, AGENTS.md | cited] (confidence: high)
- **agentskills.io pattern**: Skills are composable building blocks; shared infrastructure belongs in core utilities. — [source: agentskills.io, project constitution | cited] (confidence: high)

## Market & Context

- **CLI/MCP-first trend**: MCP (Model Context Protocol) and CLI interfaces are becoming standard for local/app integrations, allowing agents to control desktop applications directly. This aligns with local-first, privacy-preserving approaches. — [source: MCP specification, industry trend | ASSUMPTION] (confidence: medium)
- **ArtCraft app ecosystem**: Integration with PhotoCraft and other ArtCraft open-source clones via CLI/MCP fits the "blind artist" model where any model can direct apps. — [source: constitution v2.1.0 | cited] (confidence: high)

## Data & Constraints

- **No new dependencies**: Must use stdlib only (subprocess, json, shutil, etc.) consistent with project constraints. — [source: AGENTS.md Runtime/Tooling Preferences | cited] (confidence: high)
- **Backward compatibility required**: Refactoring must not break existing image-generate tests (23/23 passing). — [source: tests/ | cited] (confidence: high)
- **Synchronous patterns**: Current implementation is synchronous; need to match for now. — [source: skills/creative/image-generate/skill.py | cited] (confidence: high)
- **Validation required**: Must pass `validate_skill.py` and `validate_all_skills.py`. — [source: project validation scripts | cited] (confidence: high)

## Evidence Against the Idea

- **Over-abstraction risk**: Extracting too early could create rigid API that doesn't fit future skills' needs. Need to keep interface flexible and driven by actual use cases. — [source: software engineering best practice | ASSUMPTION] (confidence: medium)
- **MCP transport complexity**: MCP integration details might vary between apps; over-abstracting could hide important differences. — [source: MCP spec complexity | ASSUMPTION] (confidence: medium)
- **YAGNI concerns**: Only image-generate uses it now; could wait until second skill needs it. But with constitution mandating CLI/MCP-only and multiple skills planned, extracting now is efficient. — [source: project roadmap/plans | cited] (confidence: high)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: Exact public API surface of the shared client - class name (e.g., `ArtcraftAppClient`), method names/signatures, what gets returned]
- [NEEDS CLARIFICATION: Should it be a class or module of functions? Follow existing core patterns (e.g., modules with functions/classes as appropriate)]
- [NEEDS CLARIFICATION: How to handle MCP transport - current implementation details need to be preserved]
- [NEEDS CLARIFICATION: Configuration/paths discovery strategy for different ArtCraft apps]

## Sources

- .specify/memory/constitution.md (host: local, policy: allowlisted)
- skills/creative/image-generate/skill.py (host: local, policy: allowlisted)
- skills/core/ directory structure (host: local, policy: allowlisted)
- AGENTS.md (host: local, policy: allowlisted)
- tests/unit/test_image_generate*.py, tests/contract/test_image_generate.py, tests/integration/test_image_generate_composition.py (host: local, policy: allowlisted)
