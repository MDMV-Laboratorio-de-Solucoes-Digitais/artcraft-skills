# Tasks: ArtCraft Skills Suite

[This is a placeholder - keeping existing tasks, will append convergence if needed]



## Phase 10: Convergence

**Purpose**: Formal closure via analyze/converge process

- [ ] T098 [P] Run `/speckit.analyze` validation and review findings - verify spec/plan/tasks alignment with implementation
- [ ] T099 Run `/speckit.converge` to identify and append remaining tasks if any gaps found
- [ ] T100 Verify all requirements (FR-001 through FR-015) have implementation coverage
- [ ] T101 Verify all success criteria (SC-001 through SC-008) are met
- [ ] T102 Document convergence completion in feature tracking

## Phase 11: Convergence (Analysis Findings 2026-11-05)

**Purpose**: Address gaps identified by `/speckit.analyze` for formal closure.

- [ ] T103 [CRITICAL] Implement executable `scene-composition` orchestrator skill in `skills/integration/scene-composition/skill.py` with schema-compatible inputs/outputs and `SkillResult` contract, per SC-003 and FR-010 (missing implementation).
- [ ] T104 [CRITICAL] Add/extend tests for `scene-composition` (unit/contract/integration) verifying cross-product composition and end-to-end workflow execution, per SC-003 and SC-004 (missing verification).
- [ ] T105 [HIGH] Add webhook support surface to `skills/core/job_orchestrator.py` (registration/callback handling contract, validation, and tests), or explicitly document scope reduction in spec/plan with traceability, per FR-005 (partial implementation).
- [ ] T106 [HIGH] Add cost-estimation calibration evidence and tests demonstrating ±20% accuracy for supported providers/subset, or scope FR-006 to supported providers with documented evidence, per FR-006 and SC-005 (underspecified evidence).
- [ ] T107 [MEDIUM] Clarify FR-004/SC-005 integration status (stub vs real API behavior) in spec/plan and add contract tests for supported auth modes where feasible, per FR-004 and SC-005 (ambiguity).
- [ ] T108 [MEDIUM] Enumerate supported “major asset types” for feature 001 scope in spec/plan to make SC-002 measurable, per SC-002 (ambiguity).
- [ ] T109 [LOW] After remediation, re-run `/speckit.analyze` and mark T098-T102 complete with evidence; confirm 357+ tests pass and 12/12 skills validate, per FR-001–FR-015 and SC-001–SC-008 (closure verification).
