# Create AGENTS.md Plan

## Context
The user wants Repository Guidelines (AGENTS.md) created at project root. Requirements specify structure, content focus (AI-assistant-relevant), must explicitly call out architecture and code patterns, use required headings.

## Approach
1. **Discover codebase structure** - Use parallel scouts/task to understand core src, tests, configs/build, scripts/docs. Look at files we already saw (.specify, skills/, scripts/, tests/, docs/, ROADMAP, constitution).
2. **Extract architecture** - Identify key modules (skills system, validation scripts, registry/loader if present), data flow (skill discovery/loading/validation).
3. **Document patterns** - Extract conventions from existing code (Python scripts, skill structure per agentskills.io, validation rules).
4. **Write AGENTS.md** - Create at /home/luis/development/artcraft-skills/AGENTS.md following exact structure with title "Repository Guidelines".

Key findings to document:
- This is ArtCraft Skills Suite - skills ecosystem following agentskills.io standard
- Skills in skills/{category}/{name}/SKILL.md with YAML frontmatter
- Python scripts for validation/registration/loading
- Tests in tests/{unit,integration,property}
- Specs/docs in specs/, docs/
- Uses .specify framework, has constitution

## Critical files & anchors
- skills/core/example-skill/SKILL.md - skill format example
- scripts/validate_skill.py - validation logic
- scripts/skill_loader.py, register_skills.py - loading/registration
- .specify/memory/constitution.md - project principles
- docs/skill-authoring.md - authoring guide

## Verification
- AGENTS.md exists at repo root
- Title is "Repository Guidelines"
- All required sections present
- Content is concise and AI-assistant relevant
- Architecture and code patterns explicitly called out

## Assumptions & contingencies
- Assume Python-based tooling for validation scripts (based on .py files). If different runtime needed, note it.
- Follow existing patterns from constitution/docs.
