# Checklist: Schema & Agent Compatibility Requirements Quality

**Purpose**: Unit tests for requirements writing - validate quality of schema and agent compatibility requirements  
**Created**: 2026-11-03  
**Feature**: [ArtCraft Skills Suite](../spec.md)

**Note**: This checklist tests the REQUIREMENTS THEMSELVES, not the implementation.

## Requirement Completeness
- [ ] CHK001 - Are all required agentskills.io frontmatter fields (name, description) explicitly specified? [Completeness, Spec §Clarifications]
- [ ] CHK002 - Are optional frontmatter fields (license, compatibility, metadata, allowed-tools) documented with usage guidance? [Gap]
- [ ] CHK003 - Is the skill directory structure (SKILL.md, scripts/, references/, assets/) explicitly defined? [Completeness, Spec §Clarifications]
- [ ] CHK004 - Are progressive disclosure requirements specified (metadata at startup, instructions on activation, resources on demand)? [Gap]
- [ ] CHK005 - Is skill discovery/loading mechanism specified for this repo's integration with Spec Kit? [Completeness, Spec §Clarifications]

## Requirement Clarity
- [ ] CHK006 - Is "kebab-case" naming convention quantified with pattern constraints? [Clarity, Spec §Data Model]
- [ ] CHK007 - Is description length constraint specified (1-1024 chars)? [Clarity, Spec §Clarifications]
- [ ] CHK008 - Is "composable" defined with measurable criteria for skill design? [Ambiguity, Spec §Constitution]
- [ ] CHK009 - Are agent compatibility requirements specific about which agents and what compatibility means? [Clarity, Spec §FR-002]

## Requirement Consistency
- [ ] CHK010 - Do schema requirements align between contracts/skill-schema.json and spec requirements? [Consistency]
- [ ] CHK011 - Are naming conventions consistent across all skill types (atomic/orchestrator)? [Consistency]
- [ ] CHK012 - Do registration requirements align with existing Spec Kit extension patterns? [Consistency]

## Acceptance Criteria Quality
- [ ] CHK013 - Is SC-001 ("discoverable and usable by at least 3 major agent frameworks") measurable and testable? [Measurability, Spec §Success Criteria]
- [ ] CHK014 - Is SC-008 (schema and loader mechanism documented and extensible) testable without implementation details? [Measurability]

## Coverage
- [ ] CHK015 - Are requirements defined for skill validation against schema? [Gap]
- [ ] CHK016 - Are requirements defined for both agent-loaded and repo-integrated patterns? [Coverage, Spec §Clarifications]
- [ ] CHK017 - Are extension system integration requirements specified (.specify/extensions/.registry updates)? [Coverage]

## Notes
- Items marked `[Gap]` indicate requirements that may need to be added for completeness
