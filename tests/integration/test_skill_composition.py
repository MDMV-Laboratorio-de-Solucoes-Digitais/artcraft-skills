"""Integration tests for skill composition and chaining (US3)."""

import pytest
from hypothesis import given, strategies as st

from skills.core.composer import SkillComposer
from skills.core.base_skill import BaseSkill, SkillResult


class MockSkill(BaseSkill):
    def __init__(self, name, fn):
        super().__init__(name, f"Mock {name}")
        self.fn = fn
    
    def execute(self, inputs):
        try:
            result = self.fn(inputs)
            return SkillResult(success=True, data=result)
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    def validate_inputs(self, inputs):
        return True


class TestSkillComposition:
    """Test skill composition and chaining."""
    
    def test_composer_initialization(self):
        """Composer should initialize correctly."""
        composer = SkillComposer()
        assert composer is not None
        assert hasattr(composer, 'compose')
    
    def test_sequential_chaining_two_skills(self):
        """Test chaining two skills sequentially."""
        composer = SkillComposer()
        
        def skill_a(x):
            return {"value": x["value"] * 2, "from": "a"}
        
        def skill_b(x):
            return {"value": x["value"] + 10, "from": "b"}
        
        composer.register(MockSkill("a", skill_a))
        composer.register(MockSkill("b", skill_b))
        
        result = composer.compose(["a", "b"], {"value": 5})
        assert result.success
        assert result.data["value"] == 20
        assert result.data["from"] == "b"
    
    def test_sequential_chaining_three_skills(self):
        """Test chaining three atomic skills like generate -> bg-remove -> upscale."""
        composer = SkillComposer()
        
        def generate(x):
            return {"image": "img_123", "status": "generated"}
        
        def remove_bg(x):
            assert x["image"] == "img_123"
            return {"image": "img_123_nobg", "status": "bg_removed"}
        
        def upscale(x):
            assert x["image"] == "img_123_nobg"
            return {"image": "img_123_nobg_2x", "status": "upscaled"}
        
        composer.register(MockSkill("generate", generate))
        composer.register(MockSkill("remove_bg", remove_bg))
        composer.register(MockSkill("upscale", upscale))
        
        result = composer.compose(["generate", "remove_bg", "upscale"], {})
        assert result.success
        assert result.data["image"] == "img_123_nobg_2x"
        assert result.data["status"] == "upscaled"
    
    def test_output_flows_to_input(self):
        """Outputs must flow correctly as inputs between skills."""
        composer = SkillComposer()
        
        composer.register(MockSkill("s1", lambda x: {**x, "step1": True}))
        composer.register(MockSkill("s2", lambda x: {**x, "step2": x.get("step1", False)}))
        composer.register(MockSkill("s3", lambda x: {**x, "step3": x.get("step2", False)}))
        
        result = composer.compose(["s1", "s2", "s3"], {"initial": True})
        assert result.success
        assert result.data["step1"] is True
        assert result.data["step2"] is True
        assert result.data["step3"] is True
    
    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.integers()))
    def test_composition_preserves_initial_data(self, initial_data):
        """Composition should preserve data flow invariants."""
        composer = SkillComposer()
        composer.register(MockSkill("passthrough", lambda x: {**x, "processed": True}))
        
        result = composer.compose(["passthrough"], initial_data)
        assert result.success
        for k, v in initial_data.items():
            assert result.data[k] == v
        assert result.data["processed"] is True
