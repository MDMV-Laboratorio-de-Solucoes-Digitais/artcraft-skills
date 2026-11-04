# Problem Definition: Shared CLI/MCP adapter for ArtCraft apps

- **Slug**: shared-cli-mcp-adapter
- **Created**: 2026-11-04
- **Inputs used**: intake.md | research.md | user input only

## Problem Statement

Developers building creative skills for ArtCraft apps (image-edit, background-remove, image-upscale, mesh-generate, etc.) need to integrate via CLI/MCP following Constitution v2.1.0, but the working CLI/MCP discovery, invocation, and normalization logic is currently embedded in `skills/creative/image-generate/skill.py`. This duplication will create maintenance burden and inconsistent behavior as the skill family grows.

## Affected Users & Stakeholders

- **Users**: Skill developers/contributors building new creative skills — need to integrate with ArtCraft CLI/MCP without reimplementing discovery/invocation/normalization.
- **Stakeholders**: Project maintainers — need consistent patterns, easier maintenance, and faster skill development; ArtCraft ecosystem users benefit from more skills.

## Goals

- Extract CLI/MCP integration logic into a reusable shared module in `skills/core/`
- Refactor `image-generate` to use the shared module without changing behavior
- Enable future creative skills to reuse the same integration patterns
- Maintain all existing tests passing and validation passing

## Non-Goals

- Changing the CLI/MCP behavior or adding new features
- Implementing API integration (explicitly forbidden by Constitution v2.1.0)
- Creating a BaseSkill implementation (this is infrastructure)
- Modifying MCP transport protocols beyond what's needed to extract current working code

## Success Metrics

- All existing image-generate tests pass (23/23) — baseline: passing
- `python scripts/validate_skill.py skills/creative/image-generate` returns Valid — baseline: Valid
- `python scripts/validate_all_skills.py` shows all skills valid — baseline: 14/14 valid
- Shared module created and used by image-generate with no behavior changes — baseline: unknown, target: achieved

## Cost of Inaction

Without a shared adapter, each new creative skill will duplicate CLI/MCP discovery, command filtering, mode selection (auto/cli/mcp), invocation, error handling, and output normalization. This leads to code duplication, inconsistent behavior, higher maintenance costs, and slower development of the skill family as mandated by the CLI/MCP-only approach.

## Open Questions

- [NEEDS CLARIFICATION: Exact public API surface (class/module name, method signatures) for the shared client]
- [NEEDS CLARIFICATION: Should it be a class or module of functions?]
- [NEEDS CLARIFICATION: How to structure for reuse across different ArtCraft apps with potentially different CLI/MCP interfaces]
