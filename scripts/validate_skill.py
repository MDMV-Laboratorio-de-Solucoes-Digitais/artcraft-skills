#!/usr/bin/env python3
"""Skill schema validation following agentskills.io standard."""

import json
import yaml
from pathlib import Path
import re


def validate_skill_name(name):
    """Validate skill name follows kebab-case pattern."""
    if not name:
        return False, "Name is required"
    if len(name) < 1 or len(name) > 64:
        return False, "Name must be 1-64 characters"
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
        return False, "Name must be kebab-case (lowercase letters, numbers, hyphens)"
    if name.startswith('-') or name.endswith('-') or '--' in name:
        return False, "Name cannot start/end with hyphen or have consecutive hyphens"
    return True, None


def validate_description(description):
    """Validate description."""
    if not description:
        return False, "Description is required"
    if len(description) < 1 or len(description) > 1024:
        return False, "Description must be 1-1024 characters"
    return True, None


def validate_compatibility(compatibility):
    """Validate compatibility if provided."""
    if compatibility and len(compatibility) > 500:
        return False, "Compatibility must be <= 500 characters"
    return True, None


def validate_skill(skill_dir):
    """Validate a skill directory."""
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "SKILL.md must have YAML frontmatter"
    
    # Parse frontmatter
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid frontmatter format"
        frontmatter = yaml.safe_load(parts[1])
    except Exception as e:
        return False, f"Failed to parse frontmatter: {e}"
    
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a dictionary"
    
    # Validate required fields
    valid, err = validate_skill_name(frontmatter.get('name'))
    if not valid:
        return False, err
    
    valid, err = validate_description(frontmatter.get('description'))
    if not valid:
        return False, err
    
    # Validate optional fields
    if 'compatibility' in frontmatter:
        valid, err = validate_compatibility(frontmatter['compatibility'])
        if not valid:
            return False, err
    
    # Check name matches directory
    if frontmatter['name'] != skill_dir.name:
        return False, f"Skill name '{frontmatter['name']}' must match directory name '{skill_dir.name}'"
    
    return True, None


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: validate_skill.py <skill_dir>")
        sys.exit(1)
    valid, err = validate_skill(sys.argv[1])
    if valid:
        print("Valid")
        sys.exit(0)
    else:
        print(f"Invalid: {err}")
        sys.exit(1)
