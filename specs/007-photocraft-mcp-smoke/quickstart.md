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
- **007 implemented harness behavior** (`tests/integration/test_mcp_stdio_photocraft_optional.py`): opt-in gate preserved (`ARTCRAFT_MCP_INTEGRATION=1`); binary override env `ARTCRAFT_MCP_PHOTOCRAFT_BIN` preferred (absolute existing path required), else opt-in-only PATH fallback resolving absolute `photocraft-cli` with path/version capture when available; default temp auto-created absolute read/write roots with harness cleanup; explicit authorized absolute root overrides accepted only as maintainer-managed (`ARTCRAFT_MCP_READ_ROOT`/`ARTCRAFT_MCP_WRITE_ROOT` or harness args) and **never auto-deleted**; bounded timeout passed to existing 006 adapter calls; stateless sequence `artcraft_app_client.mcp_tools_list` then `mcp_tools_call(..., "command_list", {})` (full session per call, no reuse/artifact cycle); version-tolerant capability presence (`command_list`) and defensive/non-error parseable-normalizable result parsing; no AI-generation claim.
- Current implementation uses fake/monkeypatched seams for deterministic 007 tests; a real local PhotoCraft server is exercised only when a caller supplies an authorized real `mcp_config`/binary context in an explicitly opted-in environment. Do not run real smoke in default CI.

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

## 007 Implementation & Focused Regression Evidence (T009-T014, 2026-11-06)

**Implemented (test-only harness, no public contract changes)**:
- `tests/integration/test_mcp_stdio_photocraft_optional.py`: explicit opt-in (`ARTCRAFT_MCP_INTEGRATION=1`) preserved; binary override `ARTCRAFT_MCP_PHOTOCRAFT_BIN` preferred, opt-in-only PATH fallback resolves absolute `photocraft-cli` and captures path/version context when available; temp auto-created isolated absolute read/write roots cleaned on completion/failure; explicit authorized absolute root overrides maintainer-managed and never auto-deleted; bounded timeout; stateless `mcp_tools_list` then `mcp_tools_call(..., "command_list", {})` via 006 adapter; defensive/version-tolerant parsing and capability presence (`command_list`, no exact count/catalog/order); FR-006-aligned skip/failure classifier (`mcp_unavailable|mcp_misconfigured|mcp_startup_timeout|mcp_call_timeout|mcp_invalid_response|mcp_missing_capability|mcp_tool_error`), no silent MCP→CLI reroute, no session reuse/artifact cycle, no AI-generation claim.
- `skills/core/artcraft_app_client.py` and `skills/core/creative_skill.py`: **no changes** (contracts preserved).

**Focused regression matrix (T014)**:
```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q tests/contract/test_mcp_stdio_contract.py tests/unit/test_creative_skill_mcp_selection.py tests/unit/test_creative_skill_mcp_stdio.py tests/property/test_mcp_stdio_props.py tests/property/test_photocraft_mcp_smoke_props.py tests/integration/test_mcp_stdio_photocraft_optional.py
```
**Summary**: `32 passed, 23 deselected in 3.53s` (007 integration deselected by default marker; 006 MCP contract/unit/property preserved; 007 property tests green).

**Integration-selected deterministic 007 tests**:
```bash
PYTHONPATH=. python -m pytest -q -m integration tests/integration/test_mcp_stdio_photocraft_optional.py
```
**Summary**: `22 passed, 1 skipped in 0.35s` (opt-in coherence skip path exercised as expected under harness semantics; all deterministic fake/monkeypatched US1/US2 cases passed). No real PhotoCraft server required.

**Commits (007 slice)**: `5408f57` harness US1/US2 implementation, `c1d1468` cleanup-state fix, `d4b538b` tasks T012-T014 status.


## 007 Verification Attestation Evidence (T018–T021, 2026-11-06) — ONLY ATTESTATION

**Attestation scope**: Per 007 workflow, **only Phase 6 verification tasks (T018–T021) attest success/completeness**. This section records executed gates and explicit limits. No public schema/CLI/fallback/FR-005/FR-006 contract changes were made in `skills/core/*`.

### T018 — Default regression gates (mock-first preserved, independent of real PhotoCraft)
Commands:
```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. python -m pytest -q
python scripts/validate_all_skills.py
```
Results:
- `412 passed, 23 deselected in 22.40s` (default `pytest.ini -m "not integration"` excludes optional integration; 007 adds 13 executed default tests across 007 property coverage and 22 deselected integration cases by marker selection context reported above — baseline quality gates remain green; no unrelated regressions observed).
- `Validated 12 skills, all_valid=True`.

### T019 — Targeted 007/006 MCP matrix
Command:
```bash
PYTHONPATH=. python -m pytest -q \
  tests/property/test_photocraft_mcp_smoke_props.py \
  tests/property/test_mcp_stdio_props.py \
  tests/contract/test_mcp_stdio_contract.py \
  tests/unit/test_creative_skill_mcp_selection.py \
  tests/unit/test_creative_skill_mcp_stdio.py \
  tests/unit/test_mcp_stdio_transport.py \
  tests/integration/test_mcp_stdio_photocraft_optional.py
```
Result: `39 passed, 23 deselected in 5.48s`. Confirms 006 MCP contract/unit/property/selection behavior preserved, FR-005/FR-006 compatibility preserved, 007 property invariants satisfied, and 007 optional integration remains excluded by default marker.

### T020 — Opt-in local real PhotoCraft smoke (authorized local only)
**Prior record (preserved, honest):** `photocraft-cli` was found on PATH (`/usr/bin/photocraft-cli`) earlier, but **no explicit user authorization** was provided in that conversation to execute the real local MCP server smoke; that run was **not executed** and SC-001 was not exercised.

**T022 authorized execution (2026-11-06, explicit user authorization provided in this conversation):** opt-in local PhotoCraft MCP stateless smoke executed via the 007 harness (`tests/integration/test_mcp_stdio_photocraft_optional.py::run_photocraft_mcp_smoke`) with safe temp roots and bounded timeout. Evidence recorded from observed run only (no secrets/PII/raw sensitive payload dumps).

| Field | Observed value |
|---|---|
| Date (UTC) | `2026-11-06T04:51:37.034304+00:00` |
| Commit (repo state at run) | `0d597dc` |
| Opt-in | `ARTCRAFT_MCP_INTEGRATION=1` (explicit opt-in; excluded from default CI) |
| Authorization | Explicit user authorization provided in conversation to run opt-in local PhotoCraft MCP smoke (T022) with safe temp roots and bounded timeout |
| Binary override env | `ARTCRAFT_MCP_PHOTOCRAFT_BIN=/usr/bin/photocraft-cli` (preferred absolute override) |
| Resolved executable / source | `/usr/bin/photocraft-cli` (`override_env`, available/actionable) |
| Version context | `photocraft-cli 0.20.1 (327c4cc82, 2026-11-03)` |
| Command shape (roots passed) | `photocraft-cli mcp --automation-read-root <abs-temp-read> --automation-write-root <abs-temp-write>` (normalized via adapter config; exact temp paths created by harness) |
| Timeout | `30` seconds (bounded) |
| Roots policy | `mode=temp_auto`, isolated absolute temp roots created, `cleanup_owner=harness`, `auto_deleted_override=null` |
| Post-run cleanup | Temp roots removed after run: `read=true`, `write=true` (`roots.cleaned=true`, `roots.temp_paths_removed=true`) |
| Stateless boundary | `stateless=true`, `session_reuse=false`, `artifact_cycle=false`; adapter reuse only (`artcraft_app_client.mcp_tools_list` then `mcp_tools_call`) |
| MCP attempted | `true` |
| `tools/list` capability presence | `supports_command_list=true`, `required_capability_present=true`, observed sample `["command_list"]`, `version_tolerant=true` (minimal presence check; no exact count/full catalog/order asserted) |
| `tools/call command_list` result-shape summary | `ok=true`, `is_error=false`, `normalizable=true`, parsed type `list` (defensive non-error/normalizable evidence; large catalog content not dumped) |
| Reason / error_stage | `null` / not applicable (passed) |
| Limits (explicit) | Engine/editor automation only (headless PhotoCraft MCP command discovery). **No prompt-based AI image/video/audio/3D generation claim. No provider/model routing claim. No stateful multi-call artifact cycle. No default CI dependence.** |

**Status (honest, observed)**: `opt-in run executed with explicit authorization; safe temp roots cleaned; bounded timeout; stateless tools/list + command_list passed with version-tolerant capability presence and non-error normalizable result-shape evidence` — **SC-001 exercised for this local environment (evidence-backed, scoped to stateless engine/editor smoke only)**.

Full runbook/template/limits remain documented above and in `contracts/photocraft-mcp-smoke-contract.md`. Safe execution pattern:
```bash
cd /home/luis/development/artcraft-skills
PYTHONPATH=. ARTCRAFT_MCP_INTEGRATION=1 ARTCRAFT_MCP_PHOTOCRAFT_BIN=/absolute/path/to/photocraft-cli \
  python -m pytest -q -m integration tests/integration/test_mcp_stdio_photocraft_optional.py
```
Optional explicit authorized roots: absolute `ARTCRAFT_MCP_READ_ROOT`/`ARTCRAFT_MCP_WRITE_ROOT` are maintainer-managed and never auto-deleted.

### T021 — FR/SC traceability (lightweight, updated from observed T022 evidence)
| ID | Attestation / evidence |
|---|---|
| FR-001 | Opt-in gate preserved (`ARTCRAFT_MCP_INTEGRATION=1`); default `-m "not integration"` excludes optional integration (T018/T019). Real smoke executed only under explicit authorization (T022). |
| FR-002 | Harness performed stateless `artcraft_app_client.mcp_tools_list` then `mcp_tools_call(...,"command_list",...)` with bounded timeout (30s). **Observed authorized real local run passed** (T022): MCP attempted, `command_list` capability present, `command_list` invocation non-error/normalizable. Deterministic integration-selected tests pass (22 passed, 1 skipped). |
| FR-003 | `command_list` is a safe deterministic engine/editor discovery target; minimal args `{}`; no AI-generation/provider/model claim asserted by harness/tests/docs/run evidence. |
| FR-004 | Binary override preferred + opt-in-only PATH resolved absolute; temp auto roots cleaned (`temp_roots_removed_after_run read/write true`), explicit absolute overrides maintainer-managed; bounded timeout; no unsafe state leakage indicated by observed cleanup and harness tests. |
| FR-005 | No silent MCP→CLI reroute; 006 selection/explicit-MCP behavior preserved by T019 targeted matrix and no `skills/core/*` production changes. |
| FR-006 | Classifier/skip/failure paths map to `mcp_unavailable|mcp_misconfigured|mcp_startup_timeout|mcp_call_timeout|mcp_invalid_response|mcp_missing_capability|mcp_tool_error` with actionable `error_stage` where applicable; taxonomy preserved/additive-compatible. Authorized T022 run reported no error reason. |
| FR-007 | Runbook + evidence template in this quickstart; T008/T014/T018–T023 evidence recorded, including observed T022 real-server summary. |
| FR-008 | Stateless per-call adapter boundary documented/enforced and observed (`stateless=true`, `session_reuse=false`, `artifact_cycle=false`); no cross-call artifact cycle; limits explicit. |
| FR-009 | No new public AI capability/workflow/stateful session API; adapter reuse only. |
| SC-001 | **Exercised in this local environment under explicit authorization (T022, 2026-11-06)**: real MCP capability discovery plus one safe deterministic `command_list` invocation passed with version-tolerant presence and non-error normalizable result-shape evidence, temp roots cleaned, bounded timeout, stateless non-AI scope only. |
| SC-002 | Default mock-first gates green: `412 passed, 23 deselected`, `12/12 all_valid=True` (T018). |
| SC-003 | FR-006-aligned actionable outcomes + bounded timeout/cleanup covered by deterministic tests/matrix; T022 observed safe cleanup. |
| SC-004 | Quickstart/runbook/evidence records command shape, safety controls, observed proof, stateless boundary, and explicit non-AI-generation limits. |
| SC-005 | 006 MCP contract/unit/property/selection suites preserved (T019); no public schema/CLI/fallback/FR-005/FR-006 contract changes. |

**Checklists (reviewer-owned, coverage awareness only; markers not toggled)**:
- `specs/007-photocraft-mcp-smoke/checklists/requirements.md` (PASS)
- `specs/007-photocraft-mcp-smoke/checklists/contracts-fr006-normalization.md` (reviewed `[x]`, PASS; commit f24bbf0)
- `specs/007-photocraft-mcp-smoke/checklists/mcp-protocol-capability.md` (reviewed `[x]`, PASS; commit 593d3a3)
- `specs/007-photocraft-mcp-smoke/checklists/safety-opt-in-isolation.md` (reviewed `[x]`, PASS; commits 593d3a3,fca9305)

**Honest status (T023 attestation update)**: implementation/harness/tests/docs and default/targeted regression gates remain green. **SC-001 was exercised in this local environment under explicit user authorization (T022)** with safe temp roots, bounded timeout, stateless `tools/list` + `command_list` discovery/invocation evidence, and temp-root cleanup observed. Evidence is **scoped only** to deterministic engine/editor MCP smoke against `photocraft-cli 0.20.1`; **no prompt-based AI generation/provider/model behavior is claimed or supported by this slice**. Phase 6/Phase 7 verification tasks attest completeness only from recorded evidence.

## Referências e versões de protocolo

- MCP specification: revisão 2026-07-28 (latest); transporte stdio implementado compatível com 2025-11-25 e alinhado com 2026-07-28 (_meta obrigatório, server/discover, sem handshake/sessão na nova revisão). Fontes: https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports.md.
- MCP Python SDK: `modelcontextprotocol/python-sdk` v2.3.0 (v2.0.0 estável desde 2026-07-28); cliente mínimo atual preservado por back-compat/mock-first. Fonte: https://py.sdk.modelcontextprotocol.io/v2/whats-new/.
- PhotoCraft MCP: `docs/mcp.md` (main branch, storytold/photocraft) — `command_list`, `command_run`, `command_batch`, `doc_inspect`, `render_preview`, raízes de automação, progresso via `_meta.progressToken`. Fonte: https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md.

## Nota sobre sessão stateless (adapter 006)

O adapter atual é stateless por chamada (006): cada `mcp_tools_list`/`mcp_tools_call` executa uma sessão stdio completa por chamada, sem reuso de sessão. Não há ciclo stateful de artefato (`doc_new → command → doc_export`) neste slice.

MCP 2026-07-28 remove handshake e sessão server-side; uma sessão stateful (007 Option B) deve reter estado client-side ou usar multi-round-trip (InputRequiredResult), não depender de sessão server-side.
