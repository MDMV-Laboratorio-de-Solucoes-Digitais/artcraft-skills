# Requirements Checklist: 009 MCP stateful session (007 Option B)

**Purpose**: Reviewer-owned requirements-quality checklist (docs-only).
**Created**: 2026-11-06
**Feature**: `specs/009-mcp-stateful-session/spec.md`

## Scope & Contracts

- [x] CHK001 Docs-only slice; no `skills/`, `tests/`, `scripts/` changes. [FR-009, plan]
- [x] CHK002 Helper is **additive**; 006 `mcp_tools_list`/`mcp_tools_call` stateless APIs preserved. [FR-001, FR-006]
- [x] CHK003 `SkillResult`, public schemas, FR-005, FR-006 additive taxonomy preserved. [FR-006]
- [x] CHK004 Real validation future-only: opt-in, autorização explícita, 007 controls; never CI/default. [FR-003, FR-005]

## Session Lifecycle & Safety

- [x] CHK005 Lifecycle covers start/init/correlated calls/shutdown with bounded cleanup on all paths. [FR-002, data-model, contract]
- [x] CHK006 Timeouts/errors mapped to actionable FR-006-aligned outcomes; no hang/process leak by contract. [FR-002, FR-006]
- [x] CHK007 Safe roots (absolute, temp default/cleanup), binário autorizado, no secrets/PII. [FR-005]

## Deterministic Cycle & Gating

- [x] CHK008 Minimum engine/editor cycle specified as capability-gated and conditional (no success claim when unsupported). [FR-004, FR-007]
- [x] CHK009 Defensive gating required (`tools/list`/`command_list`); no exact counts/catalogs. [FR-007, 008]

## Exclusions & Protocol

- [x] CHK010 **No** prompt-based AI generation/provider/model claim. [FR-004, FR-005]
- [x] CHK011 **No** bridge/UI headless scope. [edge cases]
- [x] CHK012 MCP 2026-07-28 limits documented; client-retained process state; no server-side session assumption. [FR-008]
- [x] CHK013 Mock-first deterministic session tests required for future implementation. [FR-003]

## Gates

- [x] CHK014 Default gates expected green (docs-only): pytest 412/23 baseline, 12/12 skills. Verify at P4/final.