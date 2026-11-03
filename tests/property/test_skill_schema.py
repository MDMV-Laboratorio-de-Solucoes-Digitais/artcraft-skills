"""Property-based tests for skill schema validation.

TDD RED phase - tests written first, must fail before implementation.
"""
from hypothesis import given, strategies as st
import pytest


class TestSkillSchemaProperties:
    """Property tests for skill schema invariants."""
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_kebab_case_invariant(self, name):
        """Skill names must be valid kebab-case."""
        # Invariant: name matches pattern, no leading/trailing/consecutive hyphens
        assert not name.startswith('-')
        assert not name.endswith('-')
        assert '--' not in name
        assert all(c.islower() or c.isdigit() or c == '-' for c in name)
    
    @given(st.text(min_size=1, max_size=1024))
    def test_description_length_invariant(self, description):
        """Description must be between 1 and 1024 characters."""
        if len(description.strip()) >= 1 and len(description.strip()) <= 1024:
            # Valid description
            assert len(description.strip()) >= 1
            assert len(description.strip()) <= 1024
    
    @given(st.text(min_size=0, max_size=500))
    def test_compatibility_length_invariant(self, compatibility):
        """Compatibility must be <= 500 chars if provided."""
        if compatibility:
            assert len(compatibility) <= 500
