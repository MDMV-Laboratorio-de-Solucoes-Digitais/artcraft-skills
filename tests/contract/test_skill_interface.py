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


def test_base_skill_constructor_contract():
    """BaseSkill must accept name and description."""
    skill = DummySkill("example-skill", "Example description")
    assert skill.name == "example-skill"
    assert skill.description == "Example description"


def test_get_input_schema_returns_dict():
    """get_input_schema must return a dict schema."""
    skill = DummySkill("test-skill", "Test")
    schema = skill.get_input_schema()
    assert isinstance(schema, dict)


def test_get_output_schema_returns_dict():
    """get_output_schema must return a dict schema."""
    skill = DummySkill("test-skill", "Test")
    schema = skill.get_output_schema()
    assert isinstance(schema, dict)


def test_execute_returns_skill_result():
    """execute must return a SkillResult instance."""
    skill = DummySkill("test-skill", "Test")
    result = skill.execute({})
    assert isinstance(result, SkillResult)


def test_skill_result_defaults():
    """SkillResult has proper defaults."""
    result = SkillResult(success=True)
    assert result.success is True
    assert result.data is None
    assert result.error is None
    assert result.metadata == {}


def test_skill_result_with_error():
    """SkillResult can represent failures."""
    result = SkillResult(success=False, error="Something went wrong")
    assert result.success is False
    assert result.error == "Something went wrong"


def test_validate_inputs_exists():
    """BaseSkill must have validate_inputs method."""
    skill = DummySkill("test-skill", "Test")
    assert hasattr(skill, 'validate_inputs')
    assert callable(skill.validate_inputs)


def test_validate_inputs_accepts_dict():
    """validate_inputs should handle dict inputs."""
    skill = DummySkill("test-skill", "Test")
    result = skill.validate_inputs({})
    assert isinstance(result, bool)


def test_get_metadata_exists():
    """BaseSkill must have get_metadata method."""
    skill = DummySkill("test-skill", "Test")
    assert hasattr(skill, 'get_metadata')
    assert callable(skill.get_metadata)


def test_get_metadata_structure():
    """get_metadata returns expected structure."""
    skill = DummySkill("test-skill", "Test description")
    metadata = skill.get_metadata()
    assert isinstance(metadata, dict)
    assert metadata['name'] == "test-skill"
    assert metadata['description'] == "Test description"
    assert 'type' in metadata


def test_base_skill_is_abstract():
    """BaseSkill cannot be instantiated directly."""
    try:
        BaseSkill("test", "desc")
        assert False, "BaseSkill should be abstract"
    except TypeError:
        pass


def test_execute_abstract():
    """execute is abstract and must be implemented."""
    class IncompleteSkill(BaseSkill):
        def get_input_schema(self):
            return {}
        def get_output_schema(self):
            return {}
        # Missing execute
    
    try:
        IncompleteSkill("test", "desc")
        assert False, "Should fail without execute"
    except TypeError:
        pass


def test_get_input_schema_abstract():
    """get_input_schema is abstract."""
    class IncompleteSkill(BaseSkill):
        def get_output_schema(self):
            return {}
        def execute(self, inputs):
            return SkillResult(success=True)
        # Missing get_input_schema
    
    try:
        IncompleteSkill("test", "desc")
        assert False, "Should fail without get_input_schema"
    except TypeError:
        pass


def test_get_output_schema_abstract():
    """get_output_schema is abstract."""
    class IncompleteSkill(BaseSkill):
        def get_input_schema(self):
            return {}
        def execute(self, inputs):
            return SkillResult(success=True)
        # Missing get_output_schema
    
    try:
        IncompleteSkill("test", "desc")
        assert False, "Should fail without get_output_schema"
    except TypeError:
        pass
