"""Contract tests for generalizable workflow contracts (US5)."""

import os
import sys

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.base_skill import BaseSkill, SkillResult


class GeneralizableWorkflowSkill(BaseSkill):
    """Base contract for generalizable workflow skills."""

    def get_input_schema(self):
        raise NotImplementedError

    def get_output_schema(self):
        raise NotImplementedError

    def execute(self, inputs):
        raise NotImplementedError


class DummyGeneralizableSkill(GeneralizableWorkflowSkill):
    def __init__(self, name="generalizable-skill", description="Generalizable workflow"):
        super().__init__(name, description)

    def get_input_schema(self):
        return {"type": "object", "properties": {}, "additionalProperties": True}

    def get_output_schema(self):
        return {"type": "object", "properties": {}, "additionalProperties": True}

    def execute(self, inputs):
        return SkillResult(success=True, data={"processed": True, **inputs})


def test_generalizable_workflow_skill_interface():
    """Generalizable workflow skills must follow BaseSkill contract."""
    skill = DummyGeneralizableSkill("policy-redaction", "Policy redaction")
    assert skill.name == "policy-redaction"
    assert hasattr(skill, 'execute')
    assert hasattr(skill, 'get_input_schema')
    assert hasattr(skill, 'get_output_schema')
    result = skill.execute({"content": "test"})
    assert isinstance(result, SkillResult)
    assert result.success is True


def test_generalizable_workflow_no_project_branding():
    """Generalizable workflow contracts must not require project-specific branding."""
    skill = DummyGeneralizableSkill()
    # Contract should be generic - no hardcoded project names required
    assert skill.name  # name is required but should be configurable
    schema = skill.get_input_schema()
    assert isinstance(schema, dict)
    assert schema.get("type") == "object"


def test_generalizable_workflow_composable():
    """Generalizable workflows must be composable (support middleware pattern)."""
    skill = DummyGeneralizableSkill("structured-packager")
    # Should accept arbitrary inputs for composability
    result = skill.execute({"data": "test", "metadata": {}})
    assert result.success is True
    assert result.data["processed"] is True


def test_generalizable_workflow_dag_compatible():
    """Generalizable workflows must be compatible with DAG orchestration."""
    skill = DummyGeneralizableSkill("evidence-audit")
    # Skills should be stateless and take dict inputs/return SkillResult
    result = skill.execute({})
    assert isinstance(result, SkillResult)
    assert hasattr(result, 'success')
    assert hasattr(result, 'data')
    assert hasattr(result, 'error')


def test_generalizable_workflow_middleware_contract():
    """Generalizable workflows must support middleware/preprocessing pattern."""
    skill = DummyGeneralizableSkill("policy-redaction")

    # Middleware should be able to pass through modified inputs
    inputs = {"content": "sensitive data"}
    result = skill.execute(inputs)
    assert result.success
    assert isinstance(result.data, dict)
    # Should preserve composability
    assert "content" in result.data
