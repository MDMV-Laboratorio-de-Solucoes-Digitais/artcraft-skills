"""Tests for skill discovery/loading mechanism.

TDD RED phase - tests written first.
"""
import pytest
from pathlib import Path


class TestSkillLoader:
    """Tests for skill loader/discovery."""
    
    def test_discover_skills_in_directory(self):
        """Should discover skills in skills/ directory."""
        # This will fail until implemented
        from scripts.skill_loader import SkillLoader
        loader = SkillLoader('skills/')
        skills = loader.discover()
        assert isinstance(skills, list)
    
    def test_load_skill_from_directory(self):
        """Should load a skill from its directory."""
        from scripts.skill_loader import SkillLoader
        loader = SkillLoader('skills/')
        # Will fail until implemented
        skill = loader.load('core/example-skill')
        assert skill is not None
    
    def test_parse_skill_frontmatter(self):
        """Should parse SKILL.md frontmatter."""
        from scripts.skill_loader import parse_skill_frontmatter
        # Will fail until implemented
        content = "---\nname: test\ndescription: test\n---\n# Test"
        result = parse_skill_frontmatter(content)
        assert result['name'] == 'test'
