# Implementation Plan: MCP stdio functional integration (minimum scope)

**Branch**: `006-mcp-stdio-functional-integration` | **Date**: 2026-11-05 | **Spec**: [`spec.md`](./spec.md)  
**Input**: Feature specification from `/specs/006-mcp-stdio-functional-integration/spec.md`

## Summary

Enable minimal functional MCP integration for ArtCraft creative skills over local stdio: a generic, standards-compliant MCP tools contract (`tools/list` discovery + one `tools/call` invocation) implemented in the existing adapter/skill layer with deterministic mock/fake subprocess tests. PhotoCraft headless MCP is the **reference target** for documentation/optional validation; default CI acceptance is mock-first (no real binaries/credentials/network). The design preserves `SkillResult`, public skill schemas, CLI/fallback behavior, and back-compatible default `auto` selection (CLI available → MCP available/configured → fallback/degradation). **Clarify (2026-11-05, Q4–Q8/A):** explicit `mode=mcp` never silently reroutes to CLI/fallback; FR-006 requires additive minimum failure metadata (`error`+hint, `mode`, stable `reason`, `interface`/`tool`, `error_stage`, safe context); FR-007 specifies behavioral subprocess-session invariants (JSON-RPC `id` correlation, stdout protocol/stderr diagnostics, cleanup/objective completion, session invalid after partial-startup/transport failure, no blind non-idempotent retries) while exact numeric control values remain bounded/deferred; fallback/schema/selection/recovery/ambiguous-input bounds and a spec-level verification contract are defined in `spec.md`. Primary end-to-end example: `image-edit` via the shared `CreativeSkill` path.

## Technical Context

**Language/Version**: Python 3 (repo skill/runtime code; `pytest.ini` uses `--import-mode=importlib`)  
**Primary Dependencies**: Python standard library + existing `skills/core/*` modules (`base_skill`, `artcraft_app_client`, `creative_skill`). No new mandatory third-party dependency planned for 006; Python MCP SDK (`mcp`, async/anyio) evaluated and **deferred** for this minimum sync slice (see `research.md` D1).  
**Storage**: N/A (runtime/subprocess communication only; no persistence added).  
**Testing**: `pytest` (unit/contract/property/integration-characterization patterns as applicable), `hypothesis` for property tests; deterministic fake stdio MCP subprocess/server fixtures; optional `@pytest.mark.integration` for real PhotoCraft validation (opt-in, skipped by default). Baseline: 373 passed, 12/12 skills valid (2026-11-05).  
**Target Platform**: Local development/agent environments where Python skills run (Linux/macOS/Windows-compatible Python subprocess behavior where feasible); MCP server is launched as local subprocess per `mcp_config`.  
**Project Type**: Python skills library/adapter (single repo, `skills/core` + `skills/creative` + `tests`).  
**Performance Goals**: MCP path adds bounded, predictable overhead only when selected; no regression to existing CLI path latency characteristics beyond explicit timeout bounds. Discovery+single invocation should complete within configured timeout for mock scenarios; no throughput target beyond existing skill behavior.  
**Constraints**: Preserve public schemas and `SkillResult` (FR-003 scope clarified); no stdout protocol pollution (MCP stdio stdout JSON-RPC only, stderr diagnostics); bounded startup/call timeouts with safe subprocess cleanup and objective completion; explicit `mode=mcp` no silent reroute (FR-005 Q4:A); FR-006 minimum additive failure metadata; FR-007 behavioral session invariants (exact numeric values deferred per spec Assumptions); graceful degradation per bounded existing rules; mock-first determinism and spec verification contract; no mandatory credentials/network/real binaries in default CI; follow Constitution v2.0.0 and AGENTS.md.
**Scale/Scope**: 1 reference target (PhotoCraft, docs/optional validation), 1 primary skill example (`image-edit`), 1 supported invocation after `tools/list` discovery in acceptance; generic adapter contract reusable by other `CreativeSkill` subclasses without schema changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status | Notes |
|---|---|---|---|
| I. Crafting Over Generating | MCP integration supports app/tool workflows without imposing one-shot generation semantics | PASS | Additive transport/orchestration layer. |
| II. Artist-Centric Design | Clear errors/reasons; explicit mode control; no hidden behavior changes by default | PASS | FR-005 explicit mode wins; back-compatible `auto`. |
| III. Open Source, Vendor-Neutral, Interoperable | Generic MCP tools contract; PhotoCraft reference-only; CLI/MCP/fallback preserved | PASS | No provider lock-in; target-specific mapping documented separately. |
| IV. Composability and Modularity | Reuse `artcraft_app_client` + `CreativeSkill` hooks; deterministic contracts | PASS | Minimal surface, mockable hooks, `SkillResult` unchanged. |
| V. Performance and Native Execution | Bounded timeouts, subprocess cleanup, no unnecessary overhead on non-MCP paths | PASS | CLI-first default preserved. |
| VI. Quality Through Intentional Craft | Structured failures, deterministic tests, documented limits | PASS | SC-001..SC-005 evidence-oriented. |
| VII. Transparency, Reproducibility, Cost Awareness | Reason codes/metadata, mock-first reproducibility, optional real validation clearly separated | PASS | No hidden external dependency for default tests. |
| VIII. Extensibility Without Unnecessary Complexity | Minimal stdio client slice; SDK deferred; follow existing patterns | PASS | No new mandatory dependency; narrow `tools/list`+`tools/call`. |

**Quality gates alignment**: functionality tested (planned), docs/contracts produced, agent/skills compatibility preserved, composability maintained, security (no secrets/PII in logs, safe subprocess, roots guidance for reference target), graceful error handling.

## Project Structure

### Documentation (this feature)

```text
specs/006-mcp-stdio-functional-integration/
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── mcp-stdio-adapter-contract.md
│   └── mcp-messages.schema.json
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/speckit.tasks - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
skills/
├── core/
│   ├── base_skill.py              # existing SkillResult/BaseSkill contract (unchanged)
│   ├── artcraft_app_client.py     # extend: stdio MCP helpers/protocol mapping/error reasons as needed
│   └── creative_skill.py          # extend: functional MCP hooks, availability/config checks, execute flow
└── creative/
    ├── image-edit/
    │   └── skill.py               # primary 006 acceptance example path (CreativeSkill-based)
    ├── image-generate/
    │   └── skill.py               # BaseSkill outlier; alignment follow-up unless zero-risk reuse
    └── */                         # other CreativeSkill subclasses benefit via shared base (verify back-compat)

tests/
├── unit/                          # MCP transport/config/normalization units (planned)
├── contract/                      # adapter/skill contract tests (planned)
├── property/                      # selection/normalization/mcp_config invariants (planned/extended)
├── integration/                   # optional real PhotoCraft @integration (planned, skipped by default)
└── characterization/             # only if needed for behavior lock-in (planned as needed)
```

**Structure Decision**: Reuse existing single-repo Python skill suite layout. Implement the minimal transport/protocol in core adapter/`CreativeSkill` hooks; validate through deterministic fake stdio subprocess tests; document PhotoCraft as reference mapping only.

## Phase 0: Research Output

See [`research.md`](./research.md). Key decisions:
- D1: minimal sync JSON-RPC stdio client in-repo for 006; defer `mcp` SDK dependency.
- D2: preserve `mcp_config` schema; define minimal launch/timeout config shape; PhotoCraft headless as reference mapping (roots, `command_list`/`command_run` engine-oriented tools).
- D3: explicit mode wins; default `auto` back-compatible (CLI→MCP→fallback); no new CLI→MCP failthrough; define “MCP available/configured”.
- D4: bounded timeouts, stderr diagnostics only, safe subprocess cleanup; no blind tool retries; extend reason metadata compatibly.
- D5: mock-first deterministic fake stdio acceptance; `image-edit` primary example; optional `@integration` real target; `image-generate` alignment follow-up.
- D6: acceptance owner = maintainers/governance unless specified.

## Phase 1: Design & Contracts Output

- [`data-model.md`](./data-model.md): `MCPStdioConfig`, transport session state, capability/invocation/outcome entities, `SkillResult` invariants.
- [`contracts/mcp-stdio-adapter-contract.md`](./contracts/mcp-stdio-adapter-contract.md): compatibility, MCP hook behavior, stdio framing/cleanup, `tools/list`+`tools/call` normalization, FR-005 selection/degradation, reference mapping notes, test contract.
- [`contracts/mcp-messages.schema.json`](./contracts/mcp-messages.schema.json): reference JSON shapes for deterministic fake MCP message tests.
- [`quickstart.md`](./quickstart.md): runnable validation scenarios (baseline, mock success, structured failures, selection policy, invariants, optional real integration).

## Constitution Check (Post-Design)

Re-evaluated after Phase 1 artifacts:

| Check | Result | Evidence |
|---|---|---|
| No schema/contract breaks | PASS | FR-003/FR-004/FR-005 in spec; contracts preserve `SkillResult`/inputs; quickstart Scenario 1/4/5. |
| Vendor-neutral / reference-target bounded | PASS | Generic tools contract; PhotoCraft only reference/optional validation (D2, contract §7). |
| Graceful degradation + transparency | PASS | Structured failures/reasons (FR-006/FR-007, contract §8), mock failure scenarios. |
| Deterministic testability | PASS | Fake stdio subprocess default; no creds/network/mandatory binaries (FR-008, SC-004). |
| Simplicity/extensibility | PASS | Minimal scope, no new mandatory dep, reuse existing hooks/patterns (D1, D5). |
| Security/safety | PASS | stdout protocol-only, stderr diagnostics, bounded timeouts, cleanup, root/PII guidance in research. |

**Gate result**: PASS — no unjustified violations. Proceed to `/speckit.tasks` when ready.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | — | — |

## Clarify Decisions (2026-11-05, applied to spec/contracts)

- **Q4/A — Explicit MCP no silent fallback**: `mode=mcp` returns structured MCP failure on any MCP-path failure; no CLI/fallback reroute. Resolves `spec.md` US1 Scenario 3 tension.
- **Q5/A — Minimum failure metadata**: additive `error`+remediation hint, `metadata.mode`, stable `metadata.reason` (006 set), `metadata.interface`/`metadata.tool` when attempted, `metadata.error_stage` where available, bounded safe context; no secrets/PII.
- **Q6/A — Subprocess-session invariants**: JSON-RPC `id` correlation; unmatched/duplicate/late/unsolicited messages do not corrupt results; EOF/exit-mid-transmission/invalid framing/partial unusable response classified + cleaned up; spawn/launch failures classified with guidance; session invalid after partial startup/transport failure; cleanup objective completion; no blind non-idempotent retries. Exact timeout/signal durations deferred.
- **Q7/A — Bounded fallback/schema/selection/recovery**: fallback rules bounded to current `CreativeSkill`/adapter + contract §2/§6; schema stability scoped to existing inputs/enums/defaults + `SkillResult` + additive metadata; explicit selection/recovery/ambiguous-input rules clarified in spec FR-005.
- **Q8/A — Verification contract**: minimum deterministic mock stdio scenario classes, selection/back-compat evidence, parity boundary, ambiguous-failure evidence protocol, regression set, minimum supported environment (Linux+Python/pytest+mock/test entrypoint).
- **Q9/A — Optional correlation metadata**: FR-006 minimum fields remain required; additive optional correlation/trace fields may be included when safe (`request_id`/JSON-RPC id, `operation_id`/session token); explicit mode remains observable.
- **Q10/A — Repeatability/classification stability**: deterministic mock scenario classes require stable FR-006 `reason`/`error_stage` under same conditions; nondeterministic classification is a defect for 006 mock scope.
- **Q11/A — Evidence traceability**: acceptance evidence maps covered scenario classes to FR/SC IDs (lightweight table/inline tags).
- **Q12/A — Conformance baseline**: pre-006 green `SkillResult`/schema + existing `CreativeSkill`/adapter CLI/selection behavior on integration branch; record commit/SHA or test summary in implementation PR.

## Planning Notes / Risks (tracked)

- **Sync vs async MCP SDK**: 006 uses minimal sync client to fit existing skill execution model; if scope expands, revisit SDK behind adapter boundary.
- **PhotoCraft tool mapping**: engine-oriented (`command_list`/`command_run`) vs capability-specific tools; reference mapping must not leak into generic contract.
- **`image-generate` outlier**: extends `BaseSkill` with duplicated MCP/CLI flow; verify no regressions and schedule alignment follow-up if needed.
- **Failthrough semantics**: explicit `mode=mcp` never silently reroutes (Q4/A); default `auto` remains CLI-first with no new CLI→MCP failthrough (D3).
- **Numeric control values deferred**: timeout/signal escalation durations, exact fixture/marker names/mechanics remain implementation choices within bounded behavioral invariants (spec Assumptions/FR-007).
