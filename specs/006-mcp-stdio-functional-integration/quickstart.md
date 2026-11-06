# Quickstart Validation Guide: MCP stdio functional integration (006)

**Feature**: 006-mcp-stdio-functional-integration  
**Purpose**: Runnable validation scenarios to prove the minimum MCP stdio integration works end-to-end (mock-first) without real credentials, network access, or mandatory ArtCraft binaries. This is a validation/run guide, not an implementation plan.

## Prerequisites

- Repo root: `/home/luis/development/artcraft-skills`
- Python 3 with `pytest` (and `hypothesis` for property tests) available in the environment used by the repo.
- Baseline before changes: `373 passed`, `12/12` skills validated (2026-11-05).
- No real MCP server, no PhotoCraft binary, no paid API keys required for default scenarios.

## Contracts / Model References

- Spec: `specs/006-mcp-stdio-functional-integration/spec.md`
- Research: `specs/006-mcp-stdio-functional-integration/research.md`
- Data model: `specs/006-mcp-stdio-functional-integration/data-model.md`
- Adapter contract: `specs/006-mcp-stdio-functional-integration/contracts/mcp-stdio-adapter-contract.md`
- MCP message reference shapes: `specs/006-mcp-stdio-functional-integration/contracts/mcp-messages.schema.json`

## Validation Scenarios

### Scenario 1 — Baseline compatibility (must stay green)

**Goal**: confirm no regressions to existing skill/test/validation baseline.

**Commands**:
```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q
python scripts/validate_all_skills.py
```

**Expected outcome**:
- Pytest reports all existing tests passing (baseline >= 373; may increase with 006 tests).
- Skill validation reports `12/12` valid / `all_valid=True`.
- No public schema breaks.

### Scenario 2 — MCP `tools/list` + `tools/call` success via deterministic fake stdio server (FR-001/002/003)

**Goal**: prove minimum functional MCP path end-to-end with normalized `SkillResult`.

**Setup**: use the 006 deterministic fake stdio MCP subprocess/server fixture/helper (planned under tests). The fake server speaks newline-delimited JSON-RPC over stdin/stdout and returns a valid `tools/list` response and a valid `tools/call` result for the supported operation mapped to the `image-edit` primary example.

**Exercise** (conceptual; exact test names finalized in implementation):
- Configure `mcp_config` with fake server `command`/`args` (and bounded timeout).
- Invoke the primary example path with `mode=mcp` (or `auto` where MCP is selected by the documented back-compatible policy and fake MCP is available/configured).

**Expected outcome**:
- Discovery (`tools/list`) is performed before/for invocation as specified.
- Invocation (`tools/call`) returns a normalized success: `SkillResult.success == True`, `SkillResult.error is None`, normalized output fields present per contract, metadata identifies MCP/interface/tool and mode without leaking secrets.
- Stderr/diagnostic output from the fake server does not corrupt protocol handling.

### Scenario 3 — Structured failure cases (FR-006/FR-007)

**Goal**: prove graceful, diagnosable failures without unsafe state.

**Cases** (deterministic fake server/process fixtures):
- MCP unavailable/misconfigured launch (`command` missing/invalid) → structured failure with MCP-unavailable/misconfigured reason.
- Startup/communication timeout (fake server delays or blocks) → structured timeout failure; subprocess cleaned up.
- Invalid protocol/JSON response on stdout → structured invalid-response failure.
- `tools/list` succeeds but supported capability missing → structured missing-capability failure.
- `tools/call` returns tool error / `isError` → structured operation failure with actionable metadata.

**Expected outcome**:
- Every case returns a `SkillResult` failure (no uncaught exception across skill boundary).
- `error`/`metadata.reason` are actionable and compatible with existing reason patterns.
- No stdout protocol pollution; no leaked subprocess.

### Scenario 4 — Back-compatible selection policy (FR-004/FR-005)

**Goal**: preserve existing behavior while enabling MCP.

**Cases**:
- `mode=cli`: unchanged; missing CLI yields existing `cli_not_found` behavior.
- `mode=mcp`: attempts MCP only; failure is returned as structured MCP failure (no silent CLI reroute).
- `mode=auto` default, CLI available: CLI path selected/executed as today (CLI-first preserved) even if MCP config is present but not selected by default policy.
- `mode=auto` default, CLI unavailable and MCP available/configured (fake server): MCP path may be selected and executed; normalized result returned.
- No CLI and no usable MCP: structured no-interface/degradation failure (`neither_available`/compatible behavior).

**Expected outcome**:
- Existing CLI/fallback expectations remain intact.
- MCP-preferred automatic behavior is **not** introduced by default in 006.

### Scenario 5 — Contract/property invariants (FR-003/FR-008)

**Goal**: protect schemas and deterministic behavior.

**Checks**:
- `mcp_config` passed by caller is not mutated.
- Public skill input/output schemas unchanged; `SkillResult` contract preserved.
- Property tests (where applicable) cover normalization/selection invariants for MCP outcomes without flakiness.

**Expected outcome**:
- Targeted unit/contract/property tests pass deterministically in default runs.

### Scenario 6 — Optional real PhotoCraft validation (FR-010, non-default)

**Goal**: manual confidence against the reference target when available.

**Prerequisites (all optional)**:
- `photocraft-cli` installed and accessible.
- Safe automation roots configured (dedicated folders recommended).
- Local command (reference): `photocraft-cli mcp --automation-read-root <abs-path> --automation-write-root <abs-path>` or equivalent environment-specific setup.

**Run** (planned): `PYTHONPATH=. python -m pytest -q -m integration` (or the repo’s chosen marker/invocation), only when explicitly enabled.

**Expected outcome**:
- Optional integration checks pass or are skipped with a clear reason when prerequisites are absent.
- Default CI/local `pytest -q` does **not** require this path.

## Evidence to Capture (implementation/PR)

- Pytest summary (default run) showing >= 373 passed and 006 tests green.
- `scripts/validate_all_skills.py` summary showing `12/12` valid.
- Notes confirming: mock-first determinism, no public schema breaks, PhotoCraft treated as reference/optional validation, default `auto` remains CLI-first.

## 006 RED Gate Evidence (T018, 2026-11-05)
Command:
`cd /home/luis/development/artcraft-skills && PYTHONPATH=. python -m pytest -q tests/unit/test_mcp_stdio_transport.py tests/unit/test_creative_skill_mcp_stdio.py tests/unit/test_creative_skill_mcp_selection.py tests/contract/test_mcp_stdio_contract.py tests/property/test_mcp_stdio_props.py tests/integration/test_mcp_stdio_photocraft_optional.py`

Result summary: **14 failed, 12 passed, 1 deselected** in 4.65s.
- RED failures are for missing 006 MCP stdio behavior (e.g. `artcraft_app_client.mcp_tools_list/mcp_tools_call` missing; `CreativeSkill` MCP path returns `mcp_unavailable` instead of discovery+invocation/FR-006 scenario-specific reasons like `mcp_missing_capability`, `mcp_tool_error`, `mcp_invalid_response`).
- Passing tests are back-compatible selection/property cases already satisfied by current behavior; integration test deselected by default marker (`-m "not integration"`).
- Baseline before edits remained green in this session context: 373 passed, 12/12 skills valid (`bg_59` / `scripts/validate_all_skills.py`).
