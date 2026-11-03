# Quickstart: ArtCraft Skills Suite

**Feature**: 001-artcraft-skills-suite  
**Date**: 2026-11-03

## Prerequisites

- ArtCraft Skills repository cloned
- Agent environment that supports skills (Claude Code, Cursor, Codex, Gemini, OpenCode)
- ArtCraft API credentials (API key for Omni API or session auth) - optional for basic testing
- Understanding of agentskills.io standard

## Setup

### 1. Understand the Structure
Skills follow agentskills.io structure:
```
skills/
├── core/           # Core abstractions
├── creative/       # Creative asset skills
├── workflow/       # Orchestrators
└── integration/    # Cross-product skills
```

Each skill is a directory with `SKILL.md` containing YAML frontmatter and instructions.

### 2. Review Constitution
Read `.specify/memory/constitution.md` to understand principles (crafting over generating, composability, etc.)

### 3. Explore Existing Patterns
Review assessment artifacts in `.specify/assessments/artcraft-skills-suite-intake/` for context.

## Creating Your First Skill

### 1. Create Skill Directory
```bash
mkdir -p skills/creative/my-skill
```

### 2. Create SKILL.md
```markdown
---
name: my-skill
description: Brief description of what this skill does and when to use it
license: Apache-2.0
metadata:
  author: your-name
  version: "1.0"
---

# My Skill

## Purpose
[Describe the skill's purpose]

## When to Use
[When to use this skill]

## Inputs
[Describe inputs]

## Outputs
[Describe outputs]

## Usage
[Usage examples]

## Limitations
[Known limitations]
```

### 3. Validate Skill
Skills must follow the schema in `contracts/skill-schema.json` and agentskills.io requirements.

### 4. Test Composition
Try composing your skill with others to verify composability.

## Using Core Abstractions

### Credential Management
```python
# Pseudo-code
creds = CredentialManager.get_credentials(provider="artcraft", auth_mode="api_key")
```

### Job Orchestration
```python
# Pseudo-code
job = await job_orchestrator.submit(skill="image-generate", inputs={...})
result = await job_orchestrator.wait_for_completion(job.id)
```

### Cost Estimation
```python
# Pseudo-code
cost = await cost_estimator.estimate(skill="video-generate", inputs={...})
# Show cost to user before execution
```

## Validation Scenarios

### Scenario 1: Skill Discovery
1. Agent scans for skills
2. Discovers skills with proper metadata
3. Can list and understand capabilities

### Scenario 2: Atomic Skill Execution
1. Invoke atomic skill with valid inputs
2. Skill uses core abstractions appropriately
3. Returns results in expected format

### Scenario 3: Skill Composition
1. Compose multiple atomic skills
2. Data flows correctly between skills
3. Orchestrator manages state and errors

### Scenario 4: ArtCraft API Integration
1. Configure credentials
2. Use skill that calls ArtCraft API
3. Job orchestration handles async flow
4. Cost estimation shown before execution

## Testing

- **Schema validation**: Validate all SKILL.md files against schema
- **Contract tests**: Test skill interfaces
- **Integration tests**: Test with mocked providers
- **Composition tests**: Test skill chaining
- **Cross-agent tests**: Verify compatibility with different agents

## Next Steps

1. Define skill schema and loader (Phase 0)
2. Implement core abstractions
3. Create first atomic skills
4. Build orchestrators
5. Add cross-product integration skills
6. Validate with generalizable MDMV workflows

## Resources

- [agentskills.io Specification](https://agentskills.io/specification)
- [ArtCraft Skills Constitution](../../.specify/memory/constitution.md)
- [ArtCraft API Documentation](https://storyteller-docs.netlify.app/)
- [Feature Specification](spec.md)
