# Checklist: Composability & Workflow Requirements Quality

**Purpose**: Unit tests for requirements writing - validate quality of composability and workflow requirements  
**Created**: 2026-11-03  
**Feature**: [ArtCraft Skills Suite](../spec.md)

**Note**: This checklist tests the REQUIREMENTS THEMSELVES, not the implementation.

## Requirement Completeness
- [ ] CHK036 - Are atomic skill requirements specified with clear input/output contracts? [Completeness, Spec §FR-007]
- [ ] CHK037 - Are orchestrator/workflow skill requirements specified? [Completeness, Spec §FR-008]
- [ ] CHK038 - Are cross-product integration requirements specified? [Completeness, Spec §FR-010]
- [ ] CHK039 - Are composition patterns (chaining, parallel execution, state management) documented? [Gap]
- [ ] CHK040 - Are MDMV generalizable workflow requirements specified (structured-packager, policy-redaction, orchestrator, evidence-audit)? [Completeness, Spec §Clarifications]

## Requirement Clarity
- [ ] CHK041 - Is "atomic skill" (single responsibility) clearly defined? [Clarity]
- [ ] CHK042 - Is "orchestrator" vs "atomic skill" distinction unambiguous? [Clarity]
- [ ] CHK043 - Is "build before generating" philosophy translated into specific requirements? [Clarity, Spec §FR-009]
- [ ] CHK044 - Are cross-product integration boundaries clearly defined? [Ambiguity]

## Requirement Consistency
- [ ] CHK045 - Do atomic and orchestrator requirements align with composability principle? [Consistency, Spec §Constitution IV]
- [ ] CHK046 - Are MDMV workflow requirements generalizable (no MDMV branding) as specified? [Consistency, Spec §FR-015]
- [ ] CHK047 - Do workflow requirements align with ArtCraft philosophy? [Consistency]

## Acceptance Criteria Quality
- [ ] CHK048 - Is SC-003 (at least 5 atomic skills and 2 orchestrator skills) measurable? [Measurability]
- [ ] CHK049 - Is SC-004 (cross-product workflow executable) testable? [Measurability]
- [ ] CHK050 - Is SC-007 (generalizable MDMV workflow implemented and validated as non-MDMV-specific) measurable? [Measurability]

## Coverage
- [ ] CHK051 - Are requirements defined for skill composition error handling? [Gap]
- [ ] CHK052 - Are requirements defined for state management in orchestrators? [Gap]
- [ ] CHK053 - Are requirements defined for parallel vs sequential execution? [Gap]
- [ ] CHK054 - Are requirements defined for skill dependency resolution? [Gap]

## Notes
- Ensure all workflows remain general-purpose per constitution
