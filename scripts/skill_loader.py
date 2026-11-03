#!/usr/bin/env python3
"""Skill discovery and loading mechanism for agentskills.io format."""

from pathlib import Path
import yaml
from typing import List, Dict, Any, Optional


class SkillLoader:
    """Load and discover skills following agentskills.io standard."""
    
    def __init__(self, skills_dir: str = "skills/"):
        self.skills_dir = Path(skills_dir)
    
    def discover(self) -> List[str]:
        """Discover all skills in skills directory."""
        skills = []
        if not self.skills_dir.exists():
            return skills
        
        # Recursively find SKILL.md files
        for skill_md in self.skills_dir.rglob("SKILL.md"):
            skill_dir = skill_md.parent
            skills.append(str(skill_dir.relative_to(self.skills_dir)))
        
        return sorted(skills)
    
    def load(self, skill_path: str) -> Optional[Dict[str, Any]]:
        """Load a skill from its path."""
        skill_dir = self.skills_dir / skill_path
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            return None
        
        content = skill_md.read_text()
        frontmatter = parse_skill_frontmatter(content)
        
        if not frontmatter:
            return None
        
        return {
            'path': str(skill_dir),
            'frontmatter': frontmatter,
            'content': content.split('---', 2)[-1].strip() if '---' in content else content,
            'has_scripts': (skill_dir / 'scripts').exists(),
            'has_references': (skill_dir / 'references').exists(),
            'has_assets': (skill_dir / 'assets').exists(),
        }


def parse_skill_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter from SKILL.md content."""
    if not content.startswith('---'):
        return None
    
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        frontmatter = yaml.safe_load(parts[1])
        return frontmatter if isinstance(frontmatter, dict) else None
    except Exception:
        return None


if __name__ == '__main__':
    loader = SkillLoader()
    print(loader.discover())
