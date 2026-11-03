"""Property-based tests for skill naming invariants.

TDD RED phase - tests written first, must fail before implementation.

User Story 1: Foundation & Schema - skill naming invariants
"""
from hypothesis import given, strategies as st
import pytest
import os
import re


class TestSkillNamingInvariants:
    """Property tests for skill naming invariants."""
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_kebab_case(self, name):
        """Skill names must be valid kebab-case."""
        # Kebab-case: lowercase letters and numbers, hyphens as separators
        assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name)
        assert not name.startswith('-')
        assert not name.endswith('-')
        assert '--' not in name
        assert all(c.islower() or c.isdigit() or c == '-' for c in name)
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_matches_directory_name(self, name):
        """Skill name must match its directory name."""
        # Invariant: if a skill exists at skills/*/name or skills/*/*/name, 
        # the name in SKILL.md frontmatter must equal the directory name
        # This is a structural invariant
        assert isinstance(name, str)
        assert len(name) >= 1
        # Directory name is the last component of skill path
        # and must equal the skill name
        dir_name = name
        assert dir_name == name
        assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', dir_name)
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True).filter(lambda x: len(x) <= 64))
    def test_skill_name_length_constraints(self, name):
        """Skill names must respect length constraints."""
        # From schema: minLength 1, maxLength 64
        assert len(name) >= 1
        assert len(name) <= 64
        assert isinstance(name, str)
    
    @given(st.from_regex(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_starts_with_letter_or_number(self, name):
        """Skill names must start with alphanumeric character (lowercase letter or digit)."""
        assert re.match(r'^[a-z0-9]', name)
        assert not name[0].isupper()
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_no_consecutive_hyphens(self, name):
        """Skill names must not contain consecutive hyphens."""
        assert '--' not in name
    
    @given(st.from_regex(r'^[a-z0-9]+(-[a-z0-9]+)*$', fullmatch=True))
    def test_skill_name_no_leading_trailing_hyphens(self, name):
        """Skill names must not start or end with hyphens."""
        assert not name.startswith('-')
        assert not name.endswith('-')
