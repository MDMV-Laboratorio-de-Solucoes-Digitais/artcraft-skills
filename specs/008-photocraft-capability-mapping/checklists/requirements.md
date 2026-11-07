# Requirements Checklist: 008 PhotoCraft MCP capability mapping

**Purpose**: Reviewer-owned requirements-quality checklist (docs-only slice).
**Created**: 2026-11-06
**Feature**: `specs/008-photocraft-capability-mapping/spec.md`

## Scope & Contracts

- [x] CHK001 Spec states slice is **docs-only** (no `skills/`, `tests/`, `scripts/` changes). [FR-006, plan]
- [x] CHK002 Public contracts preserved: `SkillResult`, skill schemas, CLI/fallback, FR-005, FR-006 taxonomy additive. [FR-006]
- [x] CHK003 Real MCP smoke remains **opt-in only**, never CI/default; 007 safety controls referenced. [FR-005, FR-009, quickstart]

## Capability Mapping Quality

- [x] CHK004 Capability tiers P1/P2/P3 defined with purpose and evidence posture. [FR-001, data-model]
- [x] CHK005 Defensive gating required (`tools/list`, `command_list`/metadata as applicable); **no exact tool counts/catalog equality**. [FR-002, contract]
- [x] CHK006 Roots, progress (`_meta.progressToken`), cancellation (`notifications/cancelled`), overwrite/format limits, preview limits documented with evidence status/caveats. [FR-003]
- [x] CHK007 Error semantics aligned to FR-006 reason/metadata (no secrets/PII). [FR-004]

## Exclusions (must be explicit)

- [x] CHK008 **No** prompt-based AI generation/provider/model/prompt routing claimed. [FR-005, SC-005]
- [x] CHK009 **No** stateful MCP cross-call artifact cycle in current adapter; 007 Option B deferred (MCP 2026-07-28 limits noted). [FR-005, research]
- [x] CHK010 **No** bridge/UI/desktop control token scope in headless mapping. [FR-005, edge cases]

## Evidence & Traceability

- [x] CHK011 Evidence statuses used (`observed`/`documented`/`unverified`) with source/date/scope. [FR-007, data-model]
- [x] CHK012 MCP 2025-11-25/2026-07-28 alignment/limits recorded; SDK v2 migration noted as backlog (not implemented). [FR-008]
- [x] CHK014 Default gates verificados (docs-only, 2026-11-06): `PYTHONPATH=. python -m pytest -q` → **412 passed, 23 deselected**; `python scripts/validate_all_skills.py` → **12/12, `all_valid=True`**. [SC-003]

## Gates

- [x] CHK014 Default gates expected green after docs-only slice: `PYTHONPATH=. python -m pytest -q` (baseline 412/23), `python scripts/validate_all_skills.py` (12/12). [SC-003] — verify in P9/final.