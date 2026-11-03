import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
#!/usr/bin/env python3
"""Register skills with Spec Kit extension system."""

import json
from pathlib import Path
from skill_loader import SkillLoader


def get_skill_registrations():
    """Get skill registrations for extension registry."""
    loader = SkillLoader()
    skills = loader.discover()
    
    registrations = []
    for skill_path in skills:
        skill = loader.load(skill_path)
        if skill and skill['frontmatter']:
            fm = skill['frontmatter']
            registrations.append({
                'name': fm.get('name'),
                'path': f'skills/{skill_path}/SKILL.md',
                'description': fm.get('description', '')
            })
    
    return registrations


def register_skills():
    """Register skills in .specify/extensions/.registry."""
    registry_path = Path('.specify/extensions/.registry')
    
    if not registry_path.exists():
        print(f"Registry not found at {registry_path}")
        return False
    
    with open(registry_path) as f:
        registry = json.load(f)
    
    registrations = get_skill_registrations()
    
    # Add registered_skills to registry
    if isinstance(registry, dict):
        if 'extensions' in registry:
            # Add to each extension or create skills entry
            for ext_id, ext in registry['extensions'].items():
                ext['registered_skills'] = registrations
        else:
            registry['registered_skills'] = registrations
    
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"Registered {len(registrations)} skills")
    return True


if __name__ == '__main__':
    register_skills()
