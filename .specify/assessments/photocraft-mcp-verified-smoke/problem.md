# Problem Definition: PhotoCraft MCP verified local smoke and one deterministic headless capability mapping

- **Slug**: photocraft-mcp-verified-smoke
- **Created**: 2026-11-05
- **Inputs used**: intake.md | research.md | user input

## Problem Statement

Maintainers of the ArtCraft Skills Suite have a mock-verified MCP stdio integration (006) and a locally available PhotoCraft MCP server, but they lack a routine, safe, opt-in way to prove that the real MCP path works end to end for at least one concrete deterministic headless capability. Without that evidence, future MCP mapping work risks building on unverified assumptions about real tool shapes, session behavior, and safety boundaries, while teams may also overstate local PhotoCraft MCP as AI prompt-generation capability without evidence.

## Affected Users & Stakeholders

- **Users — skill maintainers/contributors**: need reproducible confidence that `artcraft_app_client`/`CreativeSkill` MCP behavior works against a real PhotoCraft server, not only deterministic fakes; affected by hidden protocol/shape/session mismatches.
- **Users — agent/skill integrators**: need honest, normalized results and clear limits (engine/editor MCP vs AI generation) so workflows do not depend on unsupported claims.
- **Stakeholders — repo maintainers/reviewers**: decide whether MCP integration is trustworthy enough to extend; need evidence that preserves default CI determinism (`399 passed, 1 deselected`, mock-first) and contract safety.
- **Stakeholders — downstream ArtCraft/Crafting Apps operators** [NEEDS CLARIFICATION: owner/team for PhotoCraft compatibility expectations]: affected by how skills map to engine-oriented tools, roots, and file-write behavior.

## Goals

- Establish an optional, deterministic, safe, local verification path that proves the existing MCP stdio transport works against a real PhotoCraft MCP server for a minimal supported interaction.
- Produce at least one concrete deterministic headless capability mapping (or an equally concrete verified smoke artifact, if mapping is deferred by design) that yields an actionable normalized `SkillResult` and does not misrepresent AI generation.
- Preserve mock-first default CI behavior, public schemas, CLI/fallback behavior, and FR-005/FR-006 contract expectations.
- Record reproducible evidence and explicit limits (MCP local motor/editor scope, roots/timeouts/opt-in, version assumptions).

## Non-Goals

- Implementing or claiming prompt-based AI image/video/audio/3D generation through local PhotoCraft MCP without evidence.
- Making real PhotoCraft integration mandatory for default `pytest`/CI runs.
- Broad MCP capability coverage across PhotoCraft tools, bridge mode, UI tools, progress/cancellation, or multiple apps.
- Adding new public skill schemas or breaking CLI/fallback/selection behavior.
- Solving all Speckit hygiene issues beyond small, directly related documentation/spec reference clarifications.

## Success Metrics

- A documented opt-in local command/test path can execute a real PhotoCraft MCP smoke using explicit enablement and safe temporary/explicit roots; baseline default suite remains green (`399 passed, 1 deselected`) and `12/12` skills validate. (baseline: real MCP smoke not exercised in default workflow; prior session observed ad hoc `tools/list`/`command_list` success only)
- The verified slice produces evidence for at least `tools/list` and one MCP tool invocation path with a structured result (`SkillResult` normalization where mapped), and records version/binary/roots/limits. (baseline: mock-only for routine validation)
- Failure modes in the optional real path are structured/actionable (timeout, missing binary, misconfigured roots, tool error/unsupported capability) without leaking unsafe process state. (baseline: unknown for full optional workflow; adapter has FR-006 patterns) [NEEDS CLARIFICATION: exact minimum failure assertions for the optional test]
- Documentation clearly states: local PhotoCraft MCP = engine/editor automation; AI generation/providers/models are out of scope for this slice. (baseline: limits documented partially in research/roadmap, not as verified-slice runbook)

## Cost of Inaction

The repo keeps green mock tests while accumulating risk that real PhotoCraft MCP behavior differs in tool result shape, session semantics, root handling, or capability availability. Contributors may spend more effort later debugging broader MCP mappings, and users may be given ambiguous capability claims that blur deterministic engine automation with unavailable AI generation.

## Open Questions

- [NEEDS CLARIFICATION: Should the slice be stateless smoke-only (adapter unchanged) or include a small session-capable MCP helper to prove an artifact-producing cycle in one subprocess/session?]
- [NEEDS CLARIFICATION: Which single deterministic capability is the best first mapping (and in which skill/path) without implying AI generation?]
- [NEEDS CLARIFICATION: What exact evidence must be recorded (test output, transcript, exported artifact hash/path, `photocraft-cli --version`, roots) and where?]
- [NEEDS CLARIFICATION: What PhotoCraft version/tool availability assumptions and skip conditions are acceptable for the optional integration?]
- [NEEDS CLARIFICATION: Should temp roots be auto-created by the test harness or supplied via env vars, given current optional test behavior?]
- [NEEDS CLARIFICATION: Is binary selection explicit env/config only, PATH fallback allowed, or both for opt-in runs?]
