# Idea Intake: Shared CLI/MCP adapter for ArtCraft apps

- **Slug**: shared-cli-mcp-adapter
- **Created**: 2026-11-04
- **Source**: pasted text
- **Type**: improvement

## Idea (as captured)

> Criar um adaptador CLI/MCP compartilhado em skills/core/ (artcraft_app_client.py) e refatorar o image-generate para utilizá-lo.         
> Este é, disparadamente, o maior avanço com menor esforço (80/20) dado que agora seguimos a regra de apenas CLI/MCP.

## Restated

Extract the CLI/MCP discovery, invocation, and normalization logic currently embedded in `skills/creative/image-generate/skill.py` into a shared `skills/core/artcraft_app_client.py`, then refactor `image-generate` to use it. This creates a reusable integration layer for all creative skills following the project's CLI/MCP-only approach (per Constitution v2.1.0).

## Origin & Context

- **Raised by**: user
- **Trigger**: Post-constitution update enforcing CLI/MCP-only integration (no online API). Need to avoid duplicating integration logic across upcoming creative skills.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: What is the exact interface contract for the shared client (class name, method signatures, return types) that will be stable for all creative skills?]
- [NEEDS CLARIFICATION: Should the shared client live in `skills/core/` as a plain module or follow `BaseSkill` patterns?]
- [NEEDS CLARIFICATION: Are there any MCP transport details specific to ArtCraft apps that need to be abstracted vs passed through?]
- [NEEDS CLARIFICATION: Will we need to support both sync/async patterns for future skills, or match current synchronous implementation?]
