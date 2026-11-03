"""Contract tests for skill interfaces following agentskills.io."""
import os
import sys

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.base_skill import BaseSkill, SkillResult


class DummySkill(BaseSkill):
    def get_input_schema(self):
        return {"type": "object"}
    
    def get_output_schema(self):
        return {"type": "object"}
    
    def execute(self, inputs):
        return SkillResult(success=True, data={})


def test_base_skill_interface():
    skill = DummySkill("test-skill", "Test skill")
    assert skill.name == "test-skill"
    assert hasattr(skill, 'execute')
    assert hasattr(skill, 'get_input_schema')
    assert hasattr(skill, 'get_output_schema')
    result = skill.execute({})
    assert isinstance(result, SkillResult)
    assert result.success is True
