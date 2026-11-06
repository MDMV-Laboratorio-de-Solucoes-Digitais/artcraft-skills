# Implementation Plan: PhotoCraft MCP Verified Local Smoke

**Branch**: `007-photocraft-mcp-smoke` | **Date**: 2026-11-05 | **Spec**: `specs/007-photocraft-mcp-smoke/spec.md`  
**Input**: Feature specification from `specs/007-photocraft-mcp-smoke/spec.md`

## Summary

Deliver a small, safe, **optional** local verification slice that proves the existing mock-first MCP stdio integration (006) works against a **real local PhotoCraft MCP server** for one deterministic, stateless, engine/editor-oriented capability: **`tools/list` discovery + `tools/call` name=`command_list`**. Reuse `skills.core.artcraft_app_client.mcp_tools_list`/`mcp_tools_call` and preserve all public schemas, CLI/fallback behavior, and FR-005/FR-006 contracts. Evidence is recorded in `specs/007-photocraft-mcp-smoke/quickstart.md`; default CI/`pytest -q` remains mock-first and independent of a real PhotoCraft binary.

## Technical Context

**Language/Version**: Python 3 (repo standard; scripts/core use stdlib-first patterns).  
**Primary Dependencies**: stdlib (`json`, `os`, `shutil`, `subprocess`, `tempfile`/`pathlib` patterns, `pytest` fixtures); existing `skills.core.artcraft_app_client`, `skills.core.creative_skill`, `skills.core.base_skill.SkillResult`; optional local `photocraft-cli` binary (opt-in only, never required by default). No new runtime dependencies.  
**Storage**: N/A for product state. Temporary filesystem read/write automation roots for opted-in smoke (auto-created by harness by default, cleaned up); explicit authorized absolute roots allowed only as opt-in override and maintainer-managed. Markdown evidence/runbook in `specs/007-photocraft-mcp-smoke/quickstart.md`.  
**Testing**: `pytest` with default marker exclusion `-m "not integration"` (`pytest.ini`); `scripts/validate_all_skills.py`. Mock-first deterministic tests remain source of truth for CI. Optional real smoke: explicitly enabled, `@pytest.mark.integration` (or equivalent existing marker), bounded timeout, structured skip/fail.  
**Target Platform**: Local maintainer environments (Linux/macOS/Windows where compatible `photocraft-cli` is available) for opt-in runs; repository CI/default validation remains platform-independent of real PhotoCraft.  
**Project Type**: Python skill-suite/library + Spec Kit feature slice (verification harness + contracts/docs; minimal/no production API changes).  
**Performance Goals**: N/A for throughput. Verification must complete within bounded timeout and clean up safely; no long-lived default test impact.  
**Constraints**: Opt-in only; excluded from default CI; explicit binary selection/identity recording (override preferred; opt-in PATH resolution launches resolved absolute executable); safe absolute temp roots by default + cleanup; stateless adapter per call (no session reuse/artifact cycle); minimal version-tolerant assertions; no exact tool count/catalog equality; defensive MCP `content`/result parsing; no secrets/PII in logs/evidence; no AI-generation claim; no public schema/CLI/fallback/FR-005/FR-006 changes.  
**Scale/Scope**: 1 optional integration verification path, 1 safe deterministic invocation (`command_list`) after `tools/list`, Phase 1 design artifacts (`research.md`, `data-model.md`, `contracts/`, `quickstart.md`) complete.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|---|---|---|
| I. Crafting Over Generating | PASS | Proof targets deterministic engine/editor capability discovery (`command_list`), not one-shot AI generation. |
| II. Artist-Centric Design | PASS | Gives maintainers trustworthy, transparent verification and explicit limits; no false capability claims. |
| III. Open Source, Vendor-Neutral, Interoperable | PASS | Uses standard MCP stdio JSON-RPC contract via existing adapter; PhotoCraft is reference/verified target, not a locked vendor API. |
| IV. Composability and Modularity | PASS | Reuses existing adapter/skill contracts; no monolithic/session API added; optional harness is a narrow verification slice. |
| V. Performance and Native Execution | PASS | Bounded timeouts, opt-in only, no default CI cost, cleanup of temp/process resources. |
| VI. Quality Through Intentional Craft | PASS | Minimal, stable assertions prove real behavior without brittle overfitting; explicit non-AI limits preserve integrity. |
| VII. Transparency, Reproducibility, Cost Awareness | PASS | Records command shape, safety preconditions, resolved binary/version when available, roots policy, observed proof, stateless boundary, and limits. No cloud/paid credentials. |
| VIII. Extensibility Without Unnecessary Complexity | PASS | Defers stateful session helper/artifact cycle (Option B) to separate spec; keeps 006 adapter API unchanged. |

**Quality gates alignment**: functionality proven by opt-in real smoke + preserved mock-first gates; documentation/runbook added; compatibility preserved (schemas/CLI/fallback/FR-005/FR-006); composability preserved; performance bounded; security via explicit opt-in, least-privilege temp roots, cleanup, no secrets; transparency via explicit limits; graceful, actionable failures/skips.

**Gate result (pre-Phase 0 / post-Phase 1)**: **PASS** — no violations. Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/007-photocraft-mcp-smoke/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── photocraft-mcp-smoke-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md                  # created later by /speckit.tasks, not by /speckit.plan
```

### Source Code (repository root)

```text
skills/
└── core/
    ├── artcraft_app_client.py    # reuse: normalize_mcp_config, mcp_tools_list/call, FR-006 reasons
    ├── creative_skill.py         # preserve: FR-005 selection/hooks; no changes expected
    └── base_skill.py             # preserve: SkillResult contract

tests/
├── _helpers/
│   └── fake_mcp_stdio_server.py  # existing 006 deterministic MCP server; reuse for mock-first regressions
├── contract/
│   └── test_mcp_stdio_contract.py
├── integration/
│   └── test_mcp_stdio_photocraft_optional.py  # 007 target: evolve from placeholder to safe opt-in stateless smoke
├── property/
│   └── test_mcp_stdio_props.py
└── unit/
    ├── test_mcp_stdio_transport.py
    ├── test_creative_skill_mcp_stdio.py
    └── test_creative_skill_mcp_selection.py

specs/
├── 006-mcp-stdio-functional-integration/  # reference patterns/FR-006 baseline
└── 007-photocraft-mcp-smoke/              # this feature
```

**Structure Decision**: Single-project Python skill suite. 007 is a verification/documentation slice centered on the existing optional MCP integration test path plus spec artifacts. Prefer evolving `tests/integration/test_mcp_stdio_photocraft_optional.py` and reusing existing adapter/helpers over adding new production modules or public APIs. If implementation discovers a small shared test helper is needed, keep it test-local/opt-in and contract-preserving.

## Phase 0: Research Output

- `specs/007-photocraft-mcp-smoke/research.md` — **complete**. Resolves C1–C4: binary selection, root provisioning/cleanup, deterministic stateless invocation (`tools/list` + `command_list`) with minimal version-tolerant/defensive assertions, and evidence/runbook location/format. All `NEEDS CLARIFICATION` resolved.

## Phase 1: Design & Contracts Output

- `specs/007-photocraft-mcp-smoke/data-model.md` — runtime/conceptual entities (`OptInVerificationRun`, `MCPVerificationSequence`, `VerifiedCapabilityEvidence`, `NormalizedOutcome`/`SkillResult` mapping context, `SafeAccessBoundary`), validation, state transitions, invariants.
- `specs/007-photocraft-mcp-smoke/contracts/photocraft-mcp-smoke-contract.md` — opt-in harness preconditions, MCP interaction contract (`tools/list` + `tools/call command_list`), adapter reuse/FR-006 preservation, minimal assertion contract, evidence fields, reference PhotoCraft command, stateless/non-AI limits.
- `specs/007-photocraft-mcp-smoke/quickstart.md` — runnable validation/runbook guide and evidence record template (no implementation bodies).

## Post-Design Constitution Check

Re-evaluated after Phase 1 artifacts: **PASS**. Design remains within 006/constitution boundaries: CLI/MCP-first, composable reuse, deterministic/mock-first default, graceful structured failures, bounded resources, transparent evidence, and no unnecessary session/adapter complexity.

## Implementation Notes for `/speckit.tasks` (non-binding)

- Evolve optional integration test from placeholder to real stateless smoke only when explicitly opted in; keep `@pytest.mark.integration` excluded by default.
- Implement C2 temp-root default with cleanup in the opt-in harness/test path (do not break safety if explicit authorized roots are used; do not auto-delete maintainer-managed explicit roots).
- Reuse `mcp_tools_list`/`mcp_tools_call` directly where practical to prove the 006 adapter path; normalize evidence via existing FR-006 metadata patterns.
- Assert capability presence + non-error parseable `command_list` result shape defensively; record observed tool count as evidence, not pass criteria.
- Record run evidence in `quickstart.md` only for actual opted-in runs; do not add CI jobs or artifact pipelines.
- Verify regressions: default `pytest -q` and `scripts/validate_all_skills.py` remain green; no public schema/CLI/fallback/FR-005/FR-006 changes.
