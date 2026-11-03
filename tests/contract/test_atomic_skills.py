"""Contract tests for atomic skill interfaces.

Atomic skills are single-responsibility skills with clear input/output contracts
following the agentskills.io standard and composability principles.
"""
import os
import sys

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.base_skill import BaseSkill, SkillResult


class MockAtomicSkill(BaseSkill):
    """Mock atomic skill for contract testing."""
    
    def __init__(self, name="mock-atomic", description="Mock atomic skill"):
        super().__init__(name, description)
    
    def get_input_schema(self):
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            },
            "required": ["input"]
        }
    
    def get_output_schema(self):
        return {
            "type": "object",
            "properties": {
                "output": {"type": "string"}
            },
            "required": ["output"]
        }
    
    def execute(self, inputs):
        return SkillResult(success=True, data={"output": inputs.get("input", "")})


def test_atomic_skill_inherits_from_base_skill():
    """Atomic skill must inherit from BaseSkill."""
    skill = MockAtomicSkill()
    assert isinstance(skill, BaseSkill)


def test_atomic_skill_has_required_attributes():
    """Atomic skill must have name and description attributes."""
    skill = MockAtomicSkill("test-atomic", "Test atomic skill")
    assert hasattr(skill, 'name')
    assert hasattr(skill, 'description')
    assert skill.name == "test-atomic"
    assert skill.description == "Test atomic skill"


def test_atomic_skill_implements_execute():
    """Atomic skill must implement execute method."""
    skill = MockAtomicSkill()
    assert hasattr(skill, 'execute')
    assert callable(skill.execute)
    result = skill.execute({"input": "test"})
    assert isinstance(result, SkillResult)


def test_atomic_skill_implements_get_input_schema():
    """Atomic skill must implement get_input_schema method."""
    skill = MockAtomicSkill()
    assert hasattr(skill, 'get_input_schema')
    assert callable(skill.get_input_schema)
    schema = skill.get_input_schema()
    assert isinstance(schema, dict)


def test_atomic_skill_implements_get_output_schema():
    """Atomic skill must implement get_output_schema method."""
    skill = MockAtomicSkill()
    assert hasattr(skill, 'get_output_schema')
    assert callable(skill.get_output_schema)
    schema = skill.get_output_schema()
    assert isinstance(schema, dict)


def test_atomic_skill_metadata_type_is_atomic():
    """Atomic skill metadata must have type 'atomic'."""
    skill = MockAtomicSkill("image-generate", "Generate images")
    metadata = skill.get_metadata()
    assert isinstance(metadata, dict)
    assert 'type' in metadata
    assert metadata['type'] == 'atomic'
    assert metadata['name'] == "image-generate"
    assert metadata['description'] == "Generate images"


def test_atomic_skill_execute_returns_skill_result():
    """Atomic skill execute must return SkillResult instance."""
    skill = MockAtomicSkill()
    result = skill.execute({"input": "hello"})
    assert isinstance(result, SkillResult)
    assert hasattr(result, 'success')
    assert hasattr(result, 'data')
    assert hasattr(result, 'error')
    assert hasattr(result, 'metadata')


def test_atomic_skill_validate_inputs_method_exists():
    """Atomic skill must have validate_inputs method."""
    skill = MockAtomicSkill()
    assert hasattr(skill, 'validate_inputs')
    assert callable(skill.validate_inputs)
    # Should accept dict inputs
    assert skill.validate_inputs({"input": "test"}) is True


def test_atomic_skill_single_responsibility_contract():
    """Atomic skill must follow single responsibility principle with clear contracts."""
    skill = MockAtomicSkill("background-remove", "Remove background from image")
    # Must have clear input and output schemas
    input_schema = skill.get_input_schema()
    output_schema = skill.get_output_schema()
    assert isinstance(input_schema, dict)
    assert isinstance(output_schema, dict)
    # Must be composable - execute takes dict, returns SkillResult
    result = skill.execute({"input": "image.png"})
    assert isinstance(result, SkillResult)


def test_atomic_skill_error_handling_contract():
    """Atomic skill must handle errors gracefully returning SkillResult."""
    class FailingSkill(BaseSkill):
        def __init__(self):
            super().__init__("failing", "Failing skill")
        
        def get_input_schema(self):
            return {"type": "object"}
        
        def get_output_schema(self):
            return {"type": "object"}
        
        def execute(self, inputs):
            return SkillResult(success=False, error="Something went wrong")
    
    skill = FailingSkill()
    result = skill.execute({})
    assert isinstance(result, SkillResult)
    assert result.success is False
    assert result.error is not None
