# Quickstart Validation Guide: PhotoCraft MCP Verified Local Smoke (007)

**Feature**: 007-photocraft-mcp-smoke — PhotoCraft MCP Verified Local Smoke  
**Purpose**: Runnable validation/runbook for the **optional, explicitly opted-in** local verification path that proves the existing MCP stdio integration works against a real local PhotoCraft server for a **stateless, deterministic** smoke (capability discovery + one safe `command_list` invocation). This is a validation/planning execution guide, not implementation code and not a default CI gate.

## Guardrails (must preserve)

- **Optional, explicit opt-in only**. Real PhotoCraft smoke is excluded from default CI/`pytest -q`. Mock-first 006 behavior remains preserved.
- **No public schema/CLI/fallback/FR-005/FR-006 contract changes**. Reuse `skills/core/artcraft_app_client.py` + `skills/core/creative_skill.py` and existing FR-006 reasons/metadata patterns.
- **Stateless adapter boundary**. Each `mcp_tools_list`/`mcp_tools_call` performs a full stdio session per call (no session reuse). No stateful artifact-producing cycle (`create document -> command -> export`) in this slice.
- **No AI-generation claim**. Local PhotoCraft MCP in this slice is **engine/editor automation**. AI generation/providers/models are out of scope unless separately evidenced.
- **Minimal, version-tolerant assertions**. No exact tool count, no full catalog equality, no brittle version-pinned payload equality.

## References (007 planning artifacts)

- Spec (source of truth, clarifications C1–C4): [`spec.md`](./spec.md)
- 006 gate/evidence style: [`../006-mcp-stdio-functional-integration/quickstart.md`](../006-mcp-stdio-functional-integration/quickstart.md)
- 006 model/patterns: [`../006-mcp-stdio-functional-integration/data-model.md`](../006-mcp-stdio-functional-integration/data-model.md)
- 006 adapter contract: [`../006-mcp-stdio-functional-integration/contracts/mcp-stdio-adapter-contract.md`](../006-mcp-stdio-functional-integration/contracts/mcp-stdio-adapter-contract.md)
- 007 data model: [`./data-model.md`](./data-model.md) *(peer artifact; consult when present)*
- 007 contracts: [`./contracts/`](./contracts/) *(peer artifact; consult when present)*

## Prerequisites

- Repo root: `/home/luis/development/artcraft-skills`
- Python 3 with `pytest` available (same environment used for repo tests).
- Baseline gates must remain green in default runs (007 must not regress them):
  - `PYTHONPATH=. python -m pytest -q` → default run excludes real smoke (`-m "not integration"` via `pytest.ini`); baseline at 007 planning time: **399 passed, 1 deselected**.
  - `python scripts/validate_all_skills.py` → **12/12 valid**.
- For the **optional real smoke only**: a compatible local PhotoCraft binary/command-line server. No AI/cloud credentials, no network access required for the scoped smoke.

## Safety Preconditions

All preconditions are required before running real local verification:

1. **Explicit opt-in**: set `ARTCRAFT_MCP_INTEGRATION=1`. Without opt-in, real verification is skipped/excluded.
2. **Authorized local server selection** (opt-in mode only):
   - **Binary override env preferred** (per 007 data-model/contracts): use the configured override variable when provided.
   - **Else PATH resolution only in opt-in mode**: resolve `photocraft-cli` (or configured command) and launch the **resolved absolute executable**. Record resolved path/version when available.
   - Never make the real server path part of default CI.
3. **Safe read/write boundaries**:
   - **Default**: auto-create **isolated temporary read/write roots** for the run and **clean them up** after completion/failure.
   - **Explicit authorized override** (opt-in only, maintainer-managed): absolute read/write root paths may be supplied only as an authorized local override; maintainer is responsible for their safety/content. Prefer temp roots.
4. **Bounded execution time**: startup/call timeouts must be bounded. A timeout produces a structured, diagnosable outcome (FR-006 aligned) and must not hang or leak process state.
5. **No unsafe state leakage**: subprocesses, temp roots (when harness-managed), and partial state must be cleaned up on success, skip, or failure.

Verified local PhotoCraft MCP command shape (reference):

```bash
photocraft-cli mcp --automation-read-root <abs-path> --automation-write-root <abs-path>
```

Use absolute paths for roots. The adapter/verification harness must supply roots consistent with the selected root policy.

## Opt-in Environment

| Variable / input | Required for real smoke | Behavior |
|---|---:|---|
| `ARTCRAFT_MCP_INTEGRATION` | yes | Must be `1` to enable optional real integration tests/verification. Any other value/unset → skipped/excluded. |
| Binary override env (per 007 data-model/contracts) | no (preferred when set) | Authorized local server selection override in opt-in mode. |
| `ARTCRAFT_MCP_READ_ROOT` / `ARTCRAFT_MCP_WRITE_ROOT` | only for explicit authorized override; **not required** for 007 default temp-root flow | Absolute maintainer-managed roots. The 007 harness target auto-creates temp roots by default with cleanup. Existing placeholder tests may still require these env vars until implementation aligns; treat that as pre-007 placeholder behavior. |

## Binary Resolution Behavior (opt-in mode)

1. If a binary override is provided (per 007 contract), use it as the authorized server selection.
2. Else resolve from `PATH` **only because opt-in is enabled**; obtain the resolved absolute executable path.
3. Record the resolved binary path and version/identity context when available.
4. If no authorized/available binary can be resolved, produce a structured **skip/failure** (`mcp_unavailable`/misconfigured reason, FR-006 aligned) — never silently fall back to CLI or change default behavior.

## Root Policy and Cleanup

- **Temp auto-created roots (default, recommended)**: create isolated temp directories for read and write boundaries before the smoke; pass absolute paths to PhotoCraft; remove harness-managed temp roots after the run (success or failure). Record that temp roots were used and cleaned up.
- **Explicit authorized absolute roots (opt-in override)**: allowed only when maintainer explicitly supplies absolute paths and accepts responsibility. The harness must not delete maintainer-managed override roots unless the contract explicitly states otherwise; record override policy.
- **Cleanup requirement**: bounded shutdown, no leaked subprocess, no unsafe leftover temp state from harness-managed roots.

## Bounded Timeout

- Startup and invocation timeouts are **bounded** (configured per 007 data-model/contracts; never unbounded).
- On timeout: stop the session/process within limits, clean up harness-managed resources, and report a structured timeout outcome (FR-006 `startup_timeout`/`call_timeout` or equivalent actionable reason/`error_stage`).

## Exact Pytest Command (Optional Integration Test)

Run only when explicitly opted in and prerequisites/safety controls are satisfied:

```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. ARTCRAFT_MCP_INTEGRATION=1 python -m pytest -q -m integration tests/integration/test_mcp_stdio_photocraft_optional.py
```

Notes:
- `pytest.ini` sets default `addopts = ... -m "not integration"`; the `-m integration` override is required to select this path.
- The existing file is currently a placeholder/minimal environment check (006-era); 007 implementation may expand it into real stateless smoke while preserving opt-in/exclusion. If implementation changes command shape/test name, keep the opt-in and exclusion contract identical and update this guide in the same change.
- Current placeholder also requires `ARTCRAFT_MCP_READ_ROOT`/`ARTCRAFT_MCP_WRITE_ROOT` and `photocraft-cli` on PATH; 007 target behavior prefers temp auto-roots and explicit binary resolution — verify actual harness behavior before recording evidence.

## Manual Adapter Smoke Shape (Stateless)

This describes the **logical** verification sequence using existing MCP adapter behavior (each call is a full stdio session; no session reuse):

1. **Preconditions**: opt-in enabled, authorized binary resolved, safe absolute roots selected, bounded timeout configured.
2. **`tools/list`**: start MCP stdio session → initialize/handshake as required by existing adapter → request capability discovery → capture capability presence summary (version-tolerant). Stop/cleanup session per adapter boundary.
3. **Safe deterministic invocation — `tools/call` `name=command_list` (primary)**: start new MCP stdio session → `tools/list`/readiness as adapter requires → `tools/call` with `name="command_list"` (arguments per 007 contract; keep minimal/deterministic) → capture normalized/result-shape summary. Stop/cleanup session.
4. **Normalization/evidence**: record structured outcome using FR-006-aligned reason/metadata patterns and the evidence template below. Accept non-error, parseable/normalizable structured MCP content; parse defensively (MCP results may be structured content payloads).

Verified PhotoCraft MCP launch shape (per call/session as invoked by adapter):

```bash
photocraft-cli mcp --automation-read-root <abs-path> --automation-write-root <abs-path>
```

Minimal assertion guidance:
- Capability discovery succeeds and indicates required discovery/invocation capability presence (at minimum, enough to support `command_list` as the safe deterministic smoke target) — **do not** assert exact tool count.
- `command_list` returns a structured, non-error, normalizable result/shape summary — **do not** assert full catalog equality.
- Record limits: stateless per-call sessions, no artifact export cycle, no AI generation.

## Expected Outcomes

| Scenario | Expected outcome |
|---|---|
| Opt-in set, compatible server, safe roots, bounded timeout | `tools/list` succeeds; `command_list` returns structured non-error/normalizable result; evidence recorded; harness-managed temp roots cleaned up. |
| Opt-in not set | Real smoke skipped/excluded; default tests unaffected. |
| Server unavailable / binary not resolved | Structured skip/failure, FR-006 aligned (`mcp_unavailable`/misconfigured); no silent CLI fallback. |
| Misconfigured access boundaries (invalid/missing required roots where override policy requires them) | Structured actionable failure/skip; no unsafe filesystem access. |
| Startup/call timeout | Bounded stop, cleanup, structured timeout reason (`startup_timeout`/`call_timeout` or equivalent). |
| Invalid/unexpected MCP/protocol response | Structured `invalid_response`/actionable failure; protocol output handled defensively. |
| Required capability missing (e.g., `command_list` not exposed/usable) | Structured `missing_capability` (or equivalent) with observed context. |
| Tool-level error / `isError` | Structured `tool_error`/operation failure with actionable metadata; no unsafe state leakage. |

## Skip/Failure Cases (FR-006 Aligned)

Use existing MCP/skill failure reason patterns where applicable; record `error_stage`/reason in evidence:

- `mcp_unavailable` / misconfigured launch or missing authorized binary
- `startup_timeout`
- `call_timeout`
- `invalid_response`
- `missing_capability`
- `tool_error`
- Access-boundary/prerequisite skip (actionable, explicit reason)

Failures must be diagnosable, bounded, and free of unsafe process/file-state leakage. Explicit MCP verification/selection paths must not silently reroute to CLI/fallback.

## Evidence Record Template

Copy and fill after an opted-in run (store in PR notes, local verification notes, or the location designated by 007 follow-up process; do not commit secrets):

```markdown
## 007 PhotoCraft MCP Verified Local Smoke Evidence

- Date (UTC/local):
- Operator / environment:
- Repo commit:
- Opt-in: `ARTCRAFT_MCP_INTEGRATION=1` (confirmed)
- Resolved binary: <absolute path>
- Binary/version identity (if available):
- Root policy: temp auto-created (cleaned up: yes/no) | explicit authorized absolute override (maintainer-managed)
- Read root: <absolute path or "temp">
- Write root: <absolute path or "temp">
- Cleanup result: <subprocess stopped, temp roots removed / override retained as expected>
- Command shape: `photocraft-cli mcp --automation-read-root <abs> --automation-write-root <abs>`
- Bounded timeout(s): startup=<...>, call=<...>
- Pytest/manual command executed:
- Capability presence summary (`tools/list`): <version-tolerant summary; required capabilities observed>
- `command_list` invocation: `tools/call name=command_list`
- `command_list` normalized/result-shape summary: <non-error, parseable/normalizable summary; no full catalog dump>
- Reason / `error_stage` (if skip/failure): <FR-006-aligned reason>
- Stateless boundary: confirmed (full stdio session per call; no session reuse)
- AI-generation limit: confirmed out of scope (engine/editor automation only; no AI/provider/model claim)
- Notes / observed limits:
```

## Default Gate Confirmation (007 must not regress)

Default `pytest -q` excludes real smoke and baseline gates remain green:

```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q
python scripts/validate_all_skills.py
```

Expected: default tests pass with integration deselected by `pytest.ini` (`-m "not integration"`); skill validation reports `12/12` valid. Any 007 test additions for the optional path must follow the same opt-in/exclusion pattern.

## 007 RED Gate Evidence (T008, 2026-11-06)

**Status**: RED gate satisfied for implementation start (T004–T007 written; failures are for missing 007 implementation behavior, not collection/import errors unrelated to intent).

**Command**:
```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q tests/property/test_photocraft_mcp_smoke_props.py tests/integration/test_mcp_stdio_photocraft_optional.py
```

**Summary**:
- `1 failed, 12 passed, 10 deselected in 1.18s`
- **Marker/deselection**: 10 integration tests in `tests/integration/test_mcp_stdio_photocraft_optional.py` were **deselected** by default `pytest.ini` addopts (`-m "not integration"`), preserving mock-first/default-CI exclusion. RED property/invariant tests in `tests/property/test_photocraft_mcp_smoke_props.py` collected and executed.
- **Failure (intentional RED, missing 007 harness behavior)**:
  - `tests/property/test_photocraft_mcp_smoke_props.py::TestT005PhotoCraftMCPFailureContractInvariants::test_007_harness_missing_capability_and_error_paths_are_red`
  - `Failed: 007 harness not implemented (RED): missing capability must preserve FR-006 reason.` (classifier hook exists as incomplete RED stub in integration module but does not yet provide FR-006-aligned `reason`/`error_stage` mapping).

**Why failures are expected**:
- T004–T007 added collectible RED tests/stubs for 007 stateless opt-in smoke (`tools/list` + `tools/call name=command_list`), safe temp/explicit root policy, FR-006-aligned outcomes, no session reuse/artifact cycle, and no AI-generation claim.
- Harness/classifier behavior is intentionally unimplemented (RED stubs in `tests/integration/test_mcp_stdio_photocraft_optional.py`: `run_photocraft_mcp_smoke`/binary/root/parse stubs raise `NotImplementedError`; `classify_photocraft_mcp_smoke_outcome` returns incomplete mapping). No collection/import errors; default integration deselection preserved.
- **Commits**: T004–T005 RED property invariants `e8ec422` (+ helper stabilization `954f7ce`); T006–T007 RED integration tests/stubs `34442de` (+ US2 classifier stub shape `433d9ec`).

**Implementation gate**: Phases 3–5 may proceed (T008 satisfied). Verification-only attestation remains T018–T021.
