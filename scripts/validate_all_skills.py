#!/usr/bin/env python3
"""Validate all skills in the skills directory."""

from pathlib import Path
from validate_skill import validate_skill


def validate_all():
    """Validate all skills."""
    skills_dir = Path('skills')
    if not skills_dir.exists():
        print("No skills directory found")
        return False
    
    all_valid = True
    count = 0
    
    for skill_md in skills_dir.rglob('SKILL.md'):
        skill_dir = skill_md.parent
        # Skip if it's in core/template or example
        if 'template' in str(skill_dir) or skill_dir.name == 'example-skill':
            continue
        valid, err = validate_skill(skill_dir)
        count += 1
        if valid:
            print(f"✓ {skill_dir.relative_to(skills_dir)}")
        else:
            print(f"✗ {skill_dir.relative_to(skills_dir)}: {err}")
            all_valid = False
    
    print(f"\nValidated {count} skills, all_valid={all_valid}")
    return all_valid


if __name__ == '__main__':
    import sys
    sys.exit(0 if validate_all() else 1)
