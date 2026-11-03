# Skill Authoring Guide

## Overview
This guide explains how to create skills for the ArtCraft Skills Suite following the agentskills.io standard.

## Skill Structure
Each skill is a directory containing a `SKILL.md` file:

```
skills/category/skill-name/
├── SKILL.md          # Required: metadata and instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates/resources
```

## SKILL.md Format
```markdown
---
name: skill-name
description: What the skill does and when to use it
license: Apache-2.0
metadata:
  author: your-name
  version: "1.0"
---

# Skill Name

## Purpose
...

## Usage
...
```

## Requirements
- Name: kebab-case, 1-64 chars, must match directory name
- Description: 1-1024 chars
- Follow composability principles
- Be vendor-neutral where possible
- Include comprehensive documentation

## Validation
Use `scripts/validate_skill.py` or `scripts/validate_all_skills.py` to validate skills.
