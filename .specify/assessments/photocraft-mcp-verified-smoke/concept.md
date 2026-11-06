# Concept: PhotoCraft MCP verified local smoke and one deterministic headless capability mapping

- **Slug**: photocraft-mcp-verified-smoke
- **Created**: 2026-11-05
- **Recommended option**: Option A (stateless verified smoke + explicit capability-limits proof), followed by a narrowly scoped Option B only if session/artifact proof is required

## Options

### Option A — Stateless verified smoke, mock-first preserved
- **Sketch**: Strengthen the optional PhotoCraft integration so a maintainer can explicitly opt in (env gate + available `photocraft-cli`) and prove the real MCP stdio path works for stateless discovery/invocation checks: `tools/list` shows expected tools (`command_list`/`command_run` at minimum), and at least one safe MCP tool call (e.g., `command_list` filter or `doc_new` result-shape check acknowledging non-persistent session) returns a non-error, parseable structure through the existing adapter. Record reproducible evidence (binary path/version, args, temp roots policy, observed tool names/count, result shape, limits) in a quickstart/doc note. Do not claim AI generation; document PhotoCraft MCP as engine/editor automation.
- **Appetite**: small (days)
- **Trade-offs**: Wins: lowest risk, reuses adapter/FR-005/FR-006/tests, preserves default CI, proves real transport/handshake/tool discovery immediately, avoids schema breakage and session API design. Sacrifices: does not prove a multi-step artifact-producing cycle because the adapter is currently stateless per call; “one deterministic capability mapping” may be limited to verified discovery/invocation evidence rather than a file artifact in write root.
- **Rabbit holes**: asserting exact PhotoCraft tool sets/command ids across versions; trying to force `doc_new`→`doc_export` across separate adapter subprocesses (known session boundary); over-parsing `content[].text` JSON payloads in brittle ways; accidentally making real integration non-optional.

### Option B — Small session-capable MCP helper + artifact-producing smoke
- **Sketch**: Add a narrow internal/session helper that keeps one MCP stdio subprocess alive for a bounded sequence (`initialize`/`notifications/initialized` → `tools/list` → `doc_new` → `command_run` simple deterministic command → `doc_export` into an auto-created temp write root → close/cleanup), exposed only where needed (test/helper or adapter-internal API). Map that deterministic local workflow to a clearly named, non-AI capability/result path with normalized `SkillResult` metadata and evidence including produced file presence/hash and cleanup.
- **Appetite**: medium (weeks, if kept narrow; can balloon)
- **Trade-offs**: Wins: proves real stateful headless MCP behavior and produces an artifact, giving higher confidence for future mappings. Sacrifices: larger API/safety/testing surface (session lifecycle, request ids, timeouts, cleanup on failure, concurrent use), more risk to existing adapter simplicity/contracts; still does not prove AI generation.
- **Rabbit holes**: designing a general-purpose persistent MCP session API prematurely; command id/params instability across PhotoCraft versions; export semantics/overwrite safety; cleaning up partial artifacts/processes on timeout; accidentally coupling CreativeSkill public behavior to PhotoCraft-specific engine commands.

### Option C — Do nothing now / manual evidence only
- **Sketch**: Keep mock-first 006 as-is and rely on occasional manual probes against a local `photocraft-cli`. Optionally store a dated manual note, but do not change the optional integration test or map a capability.
- **Appetite**: small
- **Trade-offs**: Wins: zero implementation risk now. Sacrifices: no repeatable verified gate; confidence decays as PhotoCraft/protocol behavior changes; future MCP work continues on partially assumed ground.
- **Rabbit holes**: stale manual notes mistaken for current proof; undocumented local assumptions.

## Recommendation

Recommend **Option A** now, tied to goals/metrics: it delivers the 80/20 proof that the existing MCP adapter works against real `photocraft-cli 0.20.1`-class servers for safe, stateless discovery/invocation, preserves mock-first defaults and contracts, and documents the critical session boundary discovered in research. **Option B** is justified only as a follow-up if the project explicitly needs artifact-producing/stateful proof; it should be specified as a separate small session-scope slice after Option A establishes stable real smoke assertions.

Not recommended: claiming AI prompt generation through local PhotoCraft MCP, or expanding to broad capability mapping before real smoke and session semantics are settled.

## Out of Scope (for the recommended option)

- Multi-step artifact-producing cycle across one MCP session (deferred to Option B/spec follow-up).
- Prompt-based AI generation, provider/model routing, or AI studio behavior through PhotoCraft MCP.
- Default CI dependency on `photocraft-cli`/PhotoCraft app/credentials/network.
- Public schema changes, CLI/fallback behavior changes, or FR-005/FR-006 regressions.
- Bridge mode, UI tools, progress/cancellation coverage, broad PhotoCraft command mapping, and deep Speckit renumbering beyond small clarifying notes.

## Assumptions to Validate

- `tools/list` and `command_list` (and selected tool names) are stable enough across supported PhotoCraft versions for minimal assertions; otherwise tests must use capability checks/skip conditions.
- Running `photocraft-cli mcp` with explicit temp read/write roots in opt-in tests is safe and deterministic enough for local maintainer verification.
- PhotoCraft MCP `tools/call` result `content[].text` payloads can be parsed defensively without making the test brittle (or assertions can remain at adapter-normalized/non-error shape).
- The repository accepts “verified stateless smoke + documented session limit” as satisfying the first 80/20 confidence increment; artifact production is a separate increment.
