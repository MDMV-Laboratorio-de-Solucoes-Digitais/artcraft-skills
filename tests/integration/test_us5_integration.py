"""Integration tests for generalizable MDMV workflows (US5)."""

import pytest
from pathlib import Path

from skills.core.composer import SkillComposer
from skills.core.base_skill import BaseSkill, SkillResult
from skills.core.orchestrator import DAGOrchestrator, DAGNode


class MockSkill(BaseSkill):
    def __init__(self, name, fn):
        super().__init__(name, f"Mock {name}")
        self.fn = fn
    
    def get_input_schema(self):
        return {"type": "object"}
    
    def get_output_schema(self):
        return {"type": "object"}
    
    def execute(self, inputs):
        try:
            result = self.fn(inputs)
            return SkillResult(success=True, data=result)
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    def validate_inputs(self, inputs):
        return isinstance(inputs, dict)


class TestUS5Integration:
    """Integration tests for US5 generalizable workflows."""
    
    def test_no_mdmv_branding_in_workflow_skills(self):
        """Verify no MDMV branding in generalizable workflow skills (FR-015)."""
        workflow_skills = [
            "skills/workflow/policy-redaction/SKILL.md",
            "skills/workflow/structured-packager/SKILL.md",
            "skills/workflow/dag-orchestrator/SKILL.md",
            "skills/workflow/evidence-audit/SKILL.md",
        ]
        mdmv_terms = ["mdmv", "tirateima", "crsdd", "fabro"]
        for skill_path in workflow_skills:
            path = Path(skill_path)
            assert path.exists(), f"{skill_path} should exist"
            content = path.read_text().lower()
            for term in mdmv_terms:
                assert term not in content, f"{skill_path} should not contain MDMV-specific term '{term}'"
    
    def test_composition_with_generalizable_workflows(self):
        """Test composing generalizable workflow skills."""
        composer = SkillComposer()
        
        composer.register(MockSkill("policy-redaction", lambda x: {**x, "redacted": True}))
        composer.register(MockSkill("structured-packager", lambda x: {**x, "packaged": True}))
        
        result = composer.compose(["policy-redaction", "structured-packager"], {"data": "test"})
        assert result.success
        assert result.data["redacted"] is True
        assert result.data["packaged"] is True
    
    def test_dag_orchestration_with_workflow_skills(self):
        """Test DAG orchestration with generalizable workflow skills."""
        orch = DAGOrchestrator()
        orch.add_node(DAGNode(id="redact", skill="policy-redaction", inputs={}))
        orch.add_node(DAGNode(id="package", skill="structured-packager", inputs={}, dependencies=["redact"]))
        orch.add_node(DAGNode(id="audit", skill="evidence-audit", inputs={}, dependencies=["package"]))
        
        assert orch.validate_dag() is True
        results = orch.execute({})
        assert len(results) == 3
        assert all(orch.nodes[n].status.name == "COMPLETED" for n in ["redact", "package", "audit"])
    
    def test_all_generalizable_workflows_exist(self):
        """Verify all required generalizable workflows exist."""
        required = [
            "skills/workflow/policy-redaction/SKILL.md",
            "skills/workflow/structured-packager/SKILL.md",
            "skills/workflow/dag-orchestrator/SKILL.md",
            "skills/workflow/evidence-audit/SKILL.md",
        ]
        for path in required:
            assert Path(path).exists(), f"{path} must exist"
    
    def test_generalizable_workflow_chaining(self):
        """Test chaining multiple generalizable workflows end-to-end."""
        composer = SkillComposer()
        
        composer.register(MockSkill("policy-redaction", lambda x: {**x, "redacted": True, "policy_checked": True}))
        composer.register(MockSkill("structured-packager", lambda x: {**x, "packaged": True, "structure": "standard"}))
        composer.register(MockSkill("evidence-audit", lambda x: {**x, "audited": True, "evidence_hash": "abc123"}))
        
        result = composer.compose(
            ["policy-redaction", "structured-packager", "evidence-audit"],
            {"raw_data": "test_input"}
        )
        assert result.success
        assert result.data["redacted"] is True
        assert result.data["packaged"] is True
        assert result.data["audited"] is True
        assert "evidence_hash" in result.data
    
    def test_workflow_skills_are_domain_agnostic(self):
        """Verify workflow skills can be applied to different domains."""
        composer = SkillComposer()
        
        # Apply same workflow pattern to different domain data
        composer.register(MockSkill("policy-redaction", lambda x: {**x, "redacted": True}))
        composer.register(MockSkill("structured-packager", lambda x: {**x, "packaged": True}))
        
        # Finance domain
        result_finance = composer.compose(["policy-redaction", "structured-packager"], 
                                          {"transactions": [{"amount": 100}], "domain": "finance"})
        assert result_finance.success
        
        # Healthcare domain
        result_healthcare = composer.compose(["policy-redaction", "structured-packager"], 
                                            {"records": [{"patient_id": "123"}], "domain": "healthcare"})
        assert result_healthcare.success
        
        # Legal domain
        result_legal = composer.compose(["policy-redaction", "structured-packager"], 
                                       {"documents": [{"case_id": "456"}], "domain": "legal"})
        assert result_legal.success
