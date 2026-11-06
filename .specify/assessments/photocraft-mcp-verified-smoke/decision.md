# Decision: PhotoCraft MCP verified local smoke and one deterministic headless capability mapping

- **Slug**: photocraft-mcp-verified-smoke
- **Decided**: 2026-11-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | 006 MCP stdio is mock-verified but lacks routine opt-in proof against a real PhotoCraft server; research found a real session-boundary constraint (stateless-per-call adapter) that can mislead future mapping work. |
| Evidence strength | adequate | Primary sources (agentskills.io spec, MCP 2025-11-25 stdio/lifecycle/tools, PhotoCraft MCP/control docs) and local repo/test evidence support the scoped problem; local probe against `photocraft-cli 0.20.1` with temp roots confirmed `tools/list` (26 tools) and `command_list`/`doc_new` behavior plus session non-persistence. Evidence is adequate for a small stateless verified-smoke slice, not for AI-generation claims or full stateful coverage. |
| Value vs. inaction | strong | Converts “mock green” into reproducible real-server confidence with low effort and prevents costly incorrect assumptions (tool shapes, session semantics, capability boundaries) before broader MCP mapping. |
| Feasibility / appetite | strong | Option A reuses existing adapter/FR-005/FR-006/tests/optional integration test pattern; real `photocraft-cli 0.20.1` already observed locally; default CI remains mock-first. Artifact-producing stateful cycle is correctly deferred due to adapter session boundary. |
| Strategic fit | strong | Aligns with constitution/repo goals (CLI/MCP-first, composable skills, deterministic tests, graceful degradation, no backend/model reimplementation) and with the roadmap gap of moving MCP from mock-first to verified operational confidence. |
| Risk posture | adequate | Key risks are understood and can be mitigated by keeping smoke opt-in, using explicit env/binary/roots, temp dirs, bounded timeouts, cleanup, minimal stable assertions, and explicit non-AI scope. Residual risk: PhotoCraft version/tool-shape drift and over-claiming beyond stateless smoke. |

## Verdict & Rationale

**Go (scoped).** The problem is real and the evidence is sufficient to specify a small, defensible slice: an optional, deterministic, safe local verification path that proves the existing MCP stdio adapter works against a real PhotoCraft MCP server for stateless discovery/invocation checks, plus explicit evidence/limits documentation. The go is intentionally narrow—mock-first defaults, public schemas, FR-005/FR-006, CLI, and fallback remain unchanged; AI prompt generation via local PhotoCraft MCP is explicitly out of scope; a stateful artifact-producing cycle is deferred to a follow-up because the current adapter is stateless per call.

## If needs-clarification

- **Blocking questions**: N/A for Option A. Clarifications to resolve during `/speckit.specify`: stable assertions across PhotoCraft versions, binary/roots discovery policy for opt-in runs, where evidence is recorded, and whether any adapter-normalized `content[].text` parsing assertion is worth the brittleness.
- **Revisit stage**: N/A (use specify clarifications; revisit `shape` only if scope expands to Option B session/artifact proof).

## If go — Handoff to `/speckit.specify`

- **Problem**: Mock-verified MCP stdio integration lacks a repeatable, opt-in proof against a real local PhotoCraft MCP server; maintainers need confidence in real transport/tool behavior and explicit capability/session limits without risking default CI determinism or implying AI generation.
- **Chosen approach**: Option A — stateless verified smoke, mock-first preserved. Adjust the optional integration path (or equivalent opt-in harness) to run `tools/list` and at least one safe MCP invocation such as `command_list` (and, if justified by stable assertions, a non-persistent `doc_new` result-shape check) against `photocraft-cli mcp` with explicit enablement, explicit binary selection policy, safe temporary/explicit absolute roots, timeout, and cleanup. Record reproducible evidence and limits; do not add AI-generation mapping.
- **In scope / out of scope**:
  - In scope: opt-in local smoke, deterministic/stable assertions, safe roots/cleanup/timeouts, failure-path clarity, evidence in `specs/.../quickstart.md` or `docs/`, documentation that local PhotoCraft MCP is engine/editor automation; small hygiene notes only where directly related.
  - Out of scope: default CI real-binary dependency, stateful multi-call artifact cycle in current adapter, prompt-based AI generation/provider routing, public schema/CLI/fallback/FR-005/FR-006 behavior changes, bridge/UI/progress/cancellation broad coverage, deep `006-*` renumbering.
- **Success metrics**: default suite still `399 passed, 1 deselected` and `12/12` skills validate; an explicitly enabled local smoke proves `tools/list` and one safe tool invocation against real `photocraft-cli` MCP with recorded version/binary/roots/limits; failures are structured/actionable; docs do not claim AI generation.
- **Carried-forward open questions**:
  - [NEEDS CLARIFICATION: Minimal stable assertions for PhotoCraft 0.20.x (and skip behavior for missing/older capabilities)?]
  - [NEEDS CLARIFICATION: Binary selection: explicit env override required, or PATH fallback allowed when opt-in is enabled?]
  - [NEEDS CLARIFICATION: Roots: auto-create temp dirs in the test harness vs require `ARTCRAFT_MCP_READ_ROOT`/`ARTCRAFT_MCP_WRITE_ROOT`?]
  - [NEEDS CLARIFICATION: Evidence location/format (006 quickstart, new spec slice quickstart, and/or dated `docs/` runbook entry)?]
  - [NEEDS CLARIFICATION: Should assertions inspect MCP `content[].text` payload JSON defensively or only adapter-normalized/non-error structure?]
  - [NEEDS CLARIFICATION: Is Option B (session-capable helper + artifact-producing cycle) a required follow-up for this feature family?]
