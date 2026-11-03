"""Tests for Spec Kit extension registration integration.

TDD RED phase - tests written first.
"""
import pytest
import json
from pathlib import Path


class TestExtensionIntegration:
    """Tests for skill registration with Spec Kit extensions."""
    
    def test_register_skills_in_extension_registry(self):
        """Should register skills in .specify/extensions/.registry."""
        from scripts.register_skills import register_skills
        # Will fail until implemented
        result = register_skills()
        assert result is True
        
        # Check registry updated
        registry_path = Path('.specify/extensions/.registry')
        with open(registry_path) as f:
            registry = json.load(f)
        # Should have registered_skills
        assert 'registered_skills' in registry or any(
            ext.get('registered_skills') for ext in registry.get('extensions', {}).values()
        )
    
    def test_skill_registration_follows_extension_pattern(self):
        """Skills should be registered following extension patterns."""
        from scripts.register_skills import get_skill_registrations
        registrations = get_skill_registrations()
        assert isinstance(registrations, list)
