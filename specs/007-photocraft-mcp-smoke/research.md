# Research: PhotoCraft MCP Verified Local Smoke (007)

**Feature**: `specs/007-photocraft-mcp-smoke/spec.md`  
**Date**: 2026-11-05  
**Status**: Complete — no `NEEDS CLARIFICATION` remains for Phase 1 design.  
**Scope**: Option A (stateless verified smoke, mock-first preserved). Stateful session-capable artifact cycle is **out of scope** (Option B, separate spec).

## Guardrails (non-negotiable)
- Optional, explicit opt-in local verification only; excluded from default CI/`pytest -q`. Mock-first 006 behavior preserved.
- No public schema, CLI, fallback, or FR-005/FR-006 contract changes. Reuse existing adapter/skill surfaces.
- Stateless adapter boundary: each MCP call performs a full stdio session per invocation (no session reuse). No multi-call artifact-producing cycle in this slice.
- Deterministic engine/editor automation only. **No prompt-based AI generation/provider/model behavior** via local PhotoCraft MCP.
- Safety: explicit opt-in, bounded timeout, least-privilege read/write roots, cleanup, no unsafe state/resource leakage, no secrets in evidence.

## C1 — Binary selection policy (resolved)

**Decision**: Explicit opt-in required. Support a binary override (explicit env/config selected by implementation; prefer explicit absolute path). If no override is provided, resolve `photocraft-cli` on `PATH` **only when the smoke is explicitly opted in**, launch the **resolved absolute executable**, and record resolved path/version identity when available. Default/CI runs never launch a real PhotoCraft binary.

**Rationale**:
- Matches current optional-test pattern (`tests/integration/test_mcp_stdio_photocraft_optional.py:14-18` uses `ARTCRAFT_MCP_INTEGRATION=1` + `shutil.which("photocraft-cli")`) while hardening evidence and path trust.
- MCP stdio transport launches the server as a subprocess with command/args (`skills/core/artcraft_app_client.py:245-283`, `_mcp_stdio_call` uses `subprocess.Popen([command]+args)`); the client controls executable selection.
- PATH-only discovery is convenient but has trust ambiguity (untrusted search path / PATH hijack class, CWE-426/427). Opt-in-only resolution + launching the resolved absolute path + recording identity gives a proportional 80/20 control without breaking local ergonomics.
- Preserves 007 guardrails: optional/not default CI, no schema/contract changes.

**Alternatives considered**:
- **Explicit absolute path only**: strongest safety/determinism; stricter than current local ergonomics and 006-era placeholder behavior.
- **Bare ambient PATH / no resolved-path recording**: weakest reproducibility/auditability; rejected.
- **Allowlist/hash/signature verification**: strong supply-chain control, but operationally heavy for local opt-in smoke; out of 80/20 scope.

**Primary sources**: MCP stdio transport (client launches subprocess) — https://modelcontextprotocol.io/specification/2025-11-25/basic/transports ; Python `subprocess` direct-exec guidance — https://docs.python.org/3/library/subprocess.html ; `shutil.which` resolution behavior — https://docs.python.org/3/library/shutil.html ; CWE-426/CWE-427 (path trust context) — https://cwe.mitre.org/data/definitions/426.html , https://cwe.mitre.org/data/definitions/427.html .

## C2 — Safe read/write root provisioning and cleanup (resolved)

**Decision**: Auto-create isolated temporary read/write roots by default for opted-in smoke runs, pass them as explicit absolute `--automation-read-root`/`--automation-write-root` values, and clean up temporary roots/resources on completion (bounded). Allow explicit authorized absolute root overrides only under opt-in for maintainer-controlled environments; explicit override roots are **maintainer-managed** (not auto-deleted) unless implementation explicitly creates them as temp. Reject/skip/fail with actionable reason when roots are missing, non-absolute (for explicit overrides), or unsafe to use.

**Rationale**:
- PhotoCraft headless MCP requires read/write automation roots and grants filesystem authority below them. Official docs require roots for headless file authority, recommend absolute roots in client configs, warn that a client has full rights below granted roots, and recommend a dedicated output folder over a whole project (`photocraft-cli mcp --automation-read-root <dir> --automation-write-root <dir>`).
- Current placeholder test only checks `ARTCRAFT_MCP_READ_ROOT/WRITE_ROOT` env presence (`tests/integration/test_mcp_stdio_photocraft_optional.py:19-28`); it does not provision/cleanup or perform real MCP calls. 007 FR-004 requires “temporary by default or explicitly authorized” + cleanup of temporary resources.
- pytest `tmp_path`/tempfile patterns provide isolated, managed temp locations for tests (`tests/property/test_artcraft_app_client_props.py` and unit tests already use `tmp_path`).
- Least privilege: dedicated empty temp roots minimize blast radius; explicit overrides remain possible but audited/recorded.

**Alternatives considered**:
- **Require env roots only** (current placeholder style): simple but brittle and shifts safety/cleanup burden to users; weaker reproducibility.
- **Auto-temp only, no override**: safest but blocks legitimate controlled local setups.
- **Workspace/repo-root roots**: rejected as unsafe by PhotoCraft/MCP least-privilege guidance.

**Primary sources**: PhotoCraft MCP docs (roots, authority, absolute paths, dedicated output folder) — https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md , https://photocraft.im/guides/mcp-cli ; pytest temporary directories — https://docs.pytest.org/en/stable/how-to/tmp_path.html ; 006 references — `specs/006-mcp-stdio-functional-integration/quickstart.md:103-107`, `contracts/mcp-stdio-adapter-contract.md:70,109`, `data-model.md:19-20`.

## C3 — Deterministic invocation, assertions, and payload parsing (resolved)

**Decision**: The “one deterministic headless capability mapping” for 007 is **verified stateless evidence** of `tools/list` discovery plus one safe deterministic `tools/call` to **`command_list`** (engine command discovery), using the existing 006 MCP adapter path (`artcraft_app_client.mcp_tools_list/mcp_tools_call` or equivalent 006 hooks) with bounded timeout and temp roots. Assertions must be **minimal, version-tolerant, and defensive**:
- `tools/list` completes without transport/protocol failure and indicates required capability presence (at least `command_list`; `command_run` may be observed but not required for pass if `command_list` smoke is sufficient and version-tolerant policy allows — implementation should prefer presence checks over exact sets).
- `command_list` invocation returns a non-error, parseable/normalizable structured result (adapter-normalized `SkillResult` success context or MCP result/content shape accepted defensively).
- Accept MCP `tools/call` result envelopes including `result.content` text payloads containing serialized JSON and/or `structuredContent`; treat JSON-RPC protocol errors and tool `isError`/error payloads as failures with FR-006-aligned reasons.
- **Do not** assert exact tool count, full tool catalog, exact command list contents/order, version strings, timestamps, or AI output fields.
- **Do not** require `doc_new→command→doc_export` artifact cycle or any cross-call state. Optional `doc_new` result-shape probing is not required; if ever added, it must respect stateless per-call boundary and not imply persistence.

**Rationale**:
- Codebase fact: current adapter is stateless per call (`skills/core/artcraft_app_client.py` creates/tears down stdio session per `_mcp_stdio_call` invocation; local probe showed `doc_new` then separate `doc_inspect` had no shared document). This makes multi-step artifact cycles infeasible without a session-capable helper (Option B).
- Local verified probe (2026-11-05, `photocraft-cli 0.20.1`, temp roots): `tools/list` returned 26 tools including `command_list`/`command_run`/`command_batch`/`doc_*`; `command_list` returned parseable engine command metadata; `doc_new` returned non-error content with document id. This confirms `command_list` is a safe read-oriented engine-discovery capability.
- MCP Tools spec: `tools/call` returns `content` (unstructured, may include text), may include `structuredContent` and `isError`; protocol errors differ from tool execution errors. PhotoCraft MCP returns engine-oriented results; `command_list` is documented as returning command metadata array.
- Robust integration/contract tests should prefer stable envelopes and presence/shape checks over brittle snapshots (reduces flakiness/version coupling).

**Alternatives considered**:
- **`tools/list` only**: lower confidence (no invocation of a PhotoCraft tool payload path).
- **`doc_new` result-shape check**: useful but creates side effects/state assumptions and can mislead under stateless adapter; not required for 80/20.
- **Artifact-producing cycle**: highest confidence but requires session-capable transport/composite flow; deferred (Option B).
- **Deep/full payload equality**: brittle across PhotoCraft versions/locales/configs.

**Primary sources**: MCP tools/lifecycle/transports — https://modelcontextprotocol.io/specification/2025-11-25/server/tools , https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle , https://modelcontextprotocol.io/specification/2025-11-25/basic/transports ; PhotoCraft MCP/control docs — https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md , https://raw.githubusercontent.com/storytold/photocraft/main/docs/control-protocol.md , https://photocraft.im/guides/mcp-cli ; local repo evidence — `skills/core/artcraft_app_client.py:244-438`, `tests/_helpers/fake_mcp_stdio_server.py`, `tests/contract/test_mcp_stdio_contract.py`, `specs/006-mcp-stdio-functional-integration/contracts/mcp-stdio-adapter-contract.md`, `.specify/assessments/photocraft-mcp-verified-smoke/research.md`.

## C4 — Evidence location and format (resolved)

**Decision**: Primary runbook + evidence template/record lives in **`specs/007-photocraft-mcp-smoke/quickstart.md`** (this slice). Record real-smoke evidence only when an opted-in run is executed; default CI evidence remains the normal mock-first suite/skill-validation summaries. Keep format minimal and reviewable (markdown), with no secrets/raw sensitive paths/content.

**Minimum evidence fields** (FR-007/SC-004): date/time + environment label (optional), repo ref/commit when captured, explicit opt-in, resolved binary path and version identity when available, root policy (temp auto-created/cleaned or explicit authorized maintainer-managed) with sanitized absolute paths as appropriate, exact command(s), bounded timeout, `tools/list` capability-presence summary (observed count allowed but not pass criterion), `command_list` invocation/result-shape summary (defensive parsing), skip/failure reason + FR-006 `error_stage`/reason when applicable, cleanup outcome, stateless session boundary, and explicit non-AI-generation limit. Optional: short sanitized excerpt or digest; no artifact pipeline required.

**Rationale**:
- Matches 006 convention (`specs/006-mcp-stdio-functional-integration/quickstart.md` contains runbook scenarios and dated evidence/attestation sections).
- Satisfies SC-004 discoverability (<5 min) in one spec-local location without creating `docs/runbooks/*` or CI artifact infrastructure.
- Preserves 007 guardrails: optional evidence is separate from default mock-first gates.

**Alternatives considered**:
- **006 quickstart only**: cross-slice coupling/ambiguity.
- **Dated `docs/` runbook system**: durable but process-heavy for one 80/20 slice.
- **CI artifact store/mandatory reports**: conflicts with optional-local/non-default-CI scope.

**Primary sources**: 006 quickstart evidence pattern — `specs/006-mcp-stdio-functional-integration/quickstart.md`; GitHub Actions artifacts/retention/digest concepts (future portability, not required now) — https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts , https://docs.github.com/en/actions/tutorials/store-and-share-data ; FAIR4RS provenance/transparency principle (applied narrowly) — https://doi.org/10.15497/RDA00068 ; NIST SSDF v1.1 (reviewable development/testing evidence context) — https://doi.org/10.6028/NIST.SP.800-218 .

## Resolution summary

| Topic | Status | Decision |
|---|---|---|
| C1 Binary selection | Resolved | Explicit opt-in; override preferred; opt-in PATH resolution launches resolved absolute executable; record identity/version. |
| C2 Roots/cleanup | Resolved | Temp auto-created isolated absolute roots by default with cleanup; explicit authorized absolute overrides allowed, maintainer-managed. |
| C3 Invocation/assertions | Resolved | Stateless `tools/list` + safe `command_list` invocation via existing 006 adapter; minimal version-tolerant assertions; defensive `content`/result parsing; no artifact cycle/AI claim. |
| C4 Evidence | Resolved | `specs/007-photocraft-mcp-smoke/quickstart.md` runbook + minimal dated evidence fields; record only when opted-in run occurs. |

All Phase 0 unknowns are resolved. Phase 1 artifacts may proceed: `data-model.md`, `contracts/`, `quickstart.md`, and constitution-aligned `plan.md`.
