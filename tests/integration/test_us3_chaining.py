"""Integration tests for skill chaining (US3)."""

import pytest
from hypothesis import given, strategies as st

from skills.core.composer import SkillComposer
from skills.core.base_skill import BaseSkill, SkillResult


class MockAtomicSkill(BaseSkill):
    """Mock atomic skill for testing."""
    
    def __init__(self, name, description, fn=None):
        super().__init__(name, description)
        self.fn = fn or (lambda x: x)
    
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


class TestSkillChaining:
    """Test chaining of atomic creative skills."""
    
    def test_chain_generate_remove_bg_upscale(self):
        """Test chaining generate -> background-remove -> upscale as in US3."""
        composer = SkillComposer()
        
        def generate(inputs):
            return {"image_id": "img_001", "prompt": inputs.get("prompt", "test"), "status": "generated"}
        
        def remove_bg(inputs):
            assert "image_id" in inputs
            return {**inputs, "image_id": f"{inputs['image_id']}_nobg", "has_bg": False, "status": "bg_removed"}
        
        def upscale(inputs):
            assert "image_id" in inputs
            return {**inputs, "image_id": f"{inputs['image_id']}_2x", "scale": 2, "status": "upscaled"}
        
        composer.register(MockAtomicSkill("generate", "Generate image", generate))
        composer.register(MockAtomicSkill("remove_bg", "Remove background", remove_bg))
        composer.register(MockAtomicSkill("upscale", "Upscale image", upscale))
        
        result = composer.compose(["generate", "remove_bg", "upscale"], {"prompt": "cat on beach"})
        assert result.success
        assert result.data["image_id"] == "img_001_nobg_2x"
        assert result.data["has_bg"] is False
        assert result.data["scale"] == 2
        assert result.data["prompt"] == "cat on beach"
    
    def test_chain_preserves_all_intermediate_data(self):
        """All data from previous steps should be available to later steps."""
        composer = SkillComposer()
        
        composer.register(MockAtomicSkill("s1", "Step 1", lambda x: {**x, "a": 1, "meta1": "data1"}))
        composer.register(MockAtomicSkill("s2", "Step 2", lambda x: {**x, "b": x["a"] * 2, "meta2": "data2"}))
        composer.register(MockAtomicSkill("s3", "Step 3", lambda x: {**x, "c": x["b"] + 1, "meta3": "data3"}))
        
        result = composer.compose(["s1", "s2", "s3"], {"initial": 100})
        assert result.success
        assert result.data["initial"] == 100
        assert result.data["a"] == 1
        assert result.data["b"] == 2
        assert result.data["c"] == 3
        assert result.data["meta1"] == "data1"
        assert result.data["meta2"] == "data2"
        assert result.data["meta3"] == "data3"
    
    def test_chain_with_single_skill(self):
        """Chaining with single skill should work."""
        composer = SkillComposer()
        composer.register(MockAtomicSkill("single", "Single skill", lambda x: {**x, "done": True}))
        
        result = composer.compose(["single"], {"input": "test"})
        assert result.success
        assert result.data["input"] == "test"
        assert result.data["done"] is True
    
    def test_chain_fails_if_intermediate_skill_fails(self):
        """If any skill in chain fails, composition should fail and return error."""
        composer = SkillComposer()
        
        composer.register(MockAtomicSkill("ok1", "OK", lambda x: {**x, "step1": True}))
        composer.register(MockAtomicSkill("bad", "Bad", lambda x: (_ for _ in ()).throw(ValueError("failed"))))
        composer.register(MockAtomicSkill("ok2", "OK", lambda x: {**x, "step3": True}))
        
        result = composer.compose(["ok1", "bad", "ok2"], {})
        assert not result.success
        assert "failed" in result.error.lower()
    
    def test_chain_fails_if_skill_not_found(self):
        """Chaining with missing skill should fail gracefully."""
        composer = SkillComposer()
        composer.register(MockAtomicSkill("exists", "Exists", lambda x: x))
        
        result = composer.compose(["exists", "missing"], {})
        assert not result.success
        assert "not found" in result.error.lower()
    
    def test_chain_fails_if_invalid_inputs(self):
        """Chaining should validate inputs for each skill."""
        composer = SkillComposer()
        
        class StrictSkill(BaseSkill):
            def __init__(self):
                super().__init__("strict", "Strict skill")
            
            def get_input_schema(self):
                return {"required": ["required_key"]}
            
            def get_output_schema(self):
                return {}
            
            def execute(self, inputs):
                return SkillResult(success=True, data={**inputs, "processed": True})
            
            def validate_inputs(self, inputs):
                return "required_key" in inputs
        
        composer.register(StrictSkill())
        result = composer.compose(["strict"], {"wrong_key": "value"})
        assert not result.success
        assert "invalid inputs" in result.error.lower()
    
    def test_chain_image_edit_workflow(self):
        """Test image-edit in a chain."""
        composer = SkillComposer()
        
        composer.register(MockAtomicSkill("generate", "Gen", lambda x: {"image": "raw.png", "prompt": x["prompt"]}))
        composer.register(MockAtomicSkill("image_edit", "Edit", lambda x: {**x, "image": "edited.png", "edited": True}))
        composer.register(MockAtomicSkill("upscale", "Upscale", lambda x: {**x, "image": "edited_4x.png", "scale": 4}))
        
        result = composer.compose(["generate", "image_edit", "upscale"], {"prompt": "landscape"})
        assert result.success
        assert result.data["image"] == "edited_4x.png"
        assert result.data["edited"] is True
        assert result.data["scale"] == 4
    
    def test_chain_3d_workflow(self):
        """Test mesh generation in a chain."""
        composer = SkillComposer()
        
        composer.register(MockAtomicSkill("image_generate", "Gen", lambda x: {"image": "concept.png"}))
        composer.register(MockAtomicSkill("mesh_generate", "Mesh", lambda x: {**x, "mesh": "model.obj", "format": "obj"}))
        
        result = composer.compose(["image_generate", "mesh_generate"], {"prompt": "chair"})
        assert result.success
        assert result.data["mesh"] == "model.obj"
        assert result.data["image"] == "concept.png"
    
    @given(st.lists(st.integers(), min_size=1, max_size=10))
    def test_chain_accumulates_values(self, values):
        """Property: chaining additions should accumulate correctly."""
        composer = SkillComposer()
        
        def add_step(n):
            def step(x):
                return {**x, f"step{n}": x.get("total", 0) + n}
            return step
        
        # Build chain dynamically
        skill_names = []
        for i, v in enumerate(values):
            name = f"add{i}"
            skill_names.append(name)
            def make_fn(val):
                return lambda x: {**x, "total": x.get("total", 0) + val}
            composer.register(MockAtomicSkill(name, f"Add {v}", make_fn(v)))
        
        result = composer.compose(skill_names, {})
        assert result.success
        expected = sum(values)
        assert result.data["total"] == expected
    
    def test_composition_with_empty_initial_data(self):
        """Composition should work with empty initial inputs."""
        composer = SkillComposer()
        composer.register(MockAtomicSkill("a", "A", lambda x: {"result": "from_a"}))
        composer.register(MockAtomicSkill("b", "B", lambda x: {"result": f"{x['result']}_then_b"}))
        
        result = composer.compose(["a", "b"], {})
        assert result.success
        assert result.data["result"] == "from_a_then_b"
    
    def test_chaining_output_becomes_next_input(self):
        """Explicit test that output flows as input (US3 acceptance scenario 2)."""
        composer = SkillComposer()
        call_order = []
        
        def skill1(x):
            call_order.append(1)
            assert isinstance(x, dict)
            return {"data": "processed_by_1", "value": 42}
        
        def skill2(x):
            call_order.append(2)
            assert x["data"] == "processed_by_1"
            assert x["value"] == 42
            return {"data": x["data"] + "_processed_by_2", "value": x["value"] * 2}
        
        def skill3(x):
            call_order.append(3)
            assert x["data"] == "processed_by_1_processed_by_2"
            assert x["value"] == 84
            return {"final": x["data"], "result_value": x["value"]}
        
        composer.register(MockAtomicSkill("skill1", "S1", skill1))
        composer.register(MockAtomicSkill("skill2", "S2", skill2))
        composer.register(MockAtomicSkill("skill3", "S3", skill3))
        
        result = composer.compose(["skill1", "skill2", "skill3"], {"initial": True})
        assert result.success
        assert call_order == [1, 2, 3]
        assert result.data["result_value"] == 84
