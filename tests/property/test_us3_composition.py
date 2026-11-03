"""Property-based tests for skill composition invariants (US3).

TDD RED phase - tests written first, must fail before implementation.
"""
from hypothesis import given, strategies as st
import pytest

from skills.core.composer import SkillComposer
from skills.core.base_skill import BaseSkill, SkillResult


class PassthroughSkill(BaseSkill):
    """Skill that passes data through unchanged."""
    
    def __init__(self, name="passthrough"):
        super().__init__(name, f"Passthrough {name}")
    
    def get_input_schema(self):
        return {}
    
    def get_output_schema(self):
        return {}
    
    def execute(self, inputs):
        return SkillResult(success=True, data=dict(inputs) if isinstance(inputs, dict) else inputs)
    
    def validate_inputs(self, inputs):
        return True


class AddFieldSkill(BaseSkill):
    """Skill that adds a field."""
    
    def __init__(self, name, field_name, value=None):
        super().__init__(name, f"Add {field_name}")
        self.field_name = field_name
        self.value = value
    
    def get_input_schema(self):
        return {}
    
    def get_output_schema(self):
        return {}
    
    def execute(self, inputs):
        if not isinstance(inputs, dict):
            inputs = {"result": inputs}
        result = dict(inputs)
        result[self.field_name] = self.value if self.value is not None else True
        return SkillResult(success=True, data=result)
    
    def validate_inputs(self, inputs):
        return True


class TransformSkill(BaseSkill):
    """Skill that transforms data."""
    
    def __init__(self, name, transform_fn):
        super().__init__(name, f"Transform {name}")
        self.transform_fn = transform_fn
    
    def get_input_schema(self):
        return {}
    
    def get_output_schema(self):
        return {}
    
    def execute(self, inputs):
        try:
            result = self.transform_fn(inputs)
            return SkillResult(success=True, data=result)
        except Exception as e:
            return SkillResult(success=False, error=str(e))
    
    def validate_inputs(self, inputs):
        return True


class TestCompositionInvariants:
    """Property tests for skill composition invariants."""
    
    @given(st.dictionaries(st.text(min_size=1, max_size=20), st.integers()))
    def test_empty_composition_preserves_input(self, initial_data):
        """Composing with empty sequence should preserve inputs."""
        composer = SkillComposer()
        result = composer.compose([], initial_data)
        # Invariant: empty composition returns inputs unchanged
        assert result.success
        assert result.data == initial_data
    
    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.one_of(st.integers(), st.text(max_size=20))))
    def test_single_skill_passthrough_composition(self, initial_data):
        """Single skill composition should apply skill once."""
        composer = SkillComposer()
        composer.register(PassthroughSkill("p1"))
        result = composer.compose(["p1"], initial_data)
        assert result.success
        # Passthrough preserves all original data
        for k, v in initial_data.items():
            assert result.data[k] == v
    
    @given(st.integers(min_value=0, max_value=10))
    def test_composition_is_associative_in_effect(self, n):
        """Composition order matters - sequential application is deterministic."""
        composer = SkillComposer()
        
        # Each skill multiplies by 2 then adds 1
        def make_skill(mult, add):
            def fn(x):
                if isinstance(x, dict) and "value" in x:
                    return {"value": x["value"] * mult + add}
                elif isinstance(x, (int, float)):
                    return x * mult + add
                else:
                    return x
            return TransformSkill(f"s{mult}_{add}", fn)
        
        # Different order gives different results - this tests order dependence
        s1 = make_skill(2, 1)  # (*2)+1
        s2 = make_skill(3, 0)  # (*3)
        composer.register(s1)
        composer.register(s2)
        
        result1 = composer.compose([s1.name, s2.name], {"value": n})
        # Reset composer state conceptually - create new one
        composer2 = SkillComposer()
        composer2.register(s1)
        composer2.register(s2)
        result2 = composer2.compose([s2.name, s1.name], {"value": n})
        
        assert result1.success
        assert result2.success
        # Order matters: (n*2+1)*3 = 3n+3 vs (n*3)*2+1 = 6n+1 (different for n>0)
        assert result1.data["value"] != result2.data["value"] or n == 0
    
    @given(st.dictionaries(st.text(min_size=1, max_size=15), st.integers(min_value=-100, max_value=100)), st.integers(min_value=1, max_value=5))
    def test_composition_data_flow_is_monotonic(self, initial_data, depth):
        """Each skill in composition can only transform/add data, flow is forward."""
        composer = SkillComposer()
        
        for i in range(depth):
            composer.register(AddFieldSkill(f"add_{i}", f"field_{i}", i))
        
        skill_names = [f"add_{i}" for i in range(depth)]
        result = composer.compose(skill_names, dict(initial_data))
        
        assert result.success
        # All initial data must be preserved
        for k, v in initial_data.items():
            assert result.data[k] == v
        # All added fields must be present
        for i in range(depth):
            assert f"field_{i}" in result.data
            assert result.data[f"field_{i}"] == i
    
    @given(st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=4).filter(lambda x: len(set(x)) == len(x)))
    def test_missing_skill_fails_composition(self, skill_names):
        """Composition fails if any skill in sequence is not registered."""
        composer = SkillComposer()
        # Register only first skill if exists
        if skill_names:
            composer.register(PassthroughSkill(skill_names[0]))
        result = composer.compose(skill_names, {"test": 1})
        if len(skill_names) == 1 and skill_names[0] in composer.skills:
            assert result.success
        else:
            # Should fail if any skill missing
            assert not result.success
            assert "not found" in result.error.lower()
    
    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.text(max_size=30)))
    def test_composition_maintains_dict_structure(self, initial_data):
        """Composition maintains data flow as dictionaries through the chain."""
        composer = SkillComposer()
        composer.register(TransformSkill("t1", lambda x: {**x, "t1": True}))
        composer.register(TransformSkill("t2", lambda x: {**x, "t2": True}))
        
        result = composer.compose(["t1", "t2"], initial_data)
        assert result.success
        assert isinstance(result.data, dict)
        # Original keys preserved
        for k in initial_data:
            assert k in result.data
    
    @given(st.integers(min_value=1, max_value=10))
    def test_composition_length_invariant(self, chain_length):
        """Composition applies exactly as many skills as in the sequence."""
        composer = SkillComposer()
        call_count = []
        
        for i in range(chain_length):
            def make_counter(idx):
                def counter(x):
                    call_count.append(idx)
                    if isinstance(x, dict):
                        return {**x, f"c{idx}": True}
                    return x
                return counter
            composer.register(TransformSkill(f"s{i}", make_counter(i)))
        
        skill_names = [f"s{i}" for i in range(chain_length)]
        result = composer.compose(skill_names, {"init": True})
        
        assert result.success
        # Each skill in sequence should be called exactly once
        assert len(call_count) == chain_length
        assert call_count == list(range(chain_length))
    
    @given(st.dictionaries(st.text(min_size=1, max_size=5), st.booleans()))
    def test_composition_idempotence_property(self, initial_data):
        """Applying composition is deterministic."""
        composer = SkillComposer()
        composer.register(TransformSkill("t1", lambda x: {**dict(x), "x": 1}))
        composer.register(TransformSkill("t2", lambda x: {**dict(x), "y": 2}))
        
        result1 = composer.compose(["t1", "t2"], dict(initial_data))
        result2 = composer.compose(["t1", "t2"], dict(initial_data))
        
        assert result1.success
        assert result2.success
        assert result1.data == result2.data
    
    @given(st.one_of(st.integers(), st.text(), st.lists(st.integers())))
    def test_composition_handles_non_dict_inputs(self, non_dict_input):
        """Composition should handle non-dict inputs by wrapping them."""
        composer = SkillComposer()
        composer.register(TransformSkill("t1", lambda x: x))  # pass through
        result = composer.compose(["t1"], non_dict_input)
        # Based on composer implementation, non-dict outputs get wrapped
        assert result.success
    
    def test_composition_failure_short_circuits(self):
        """If a skill fails, composition should short-circuit and return failure."""
        composer = SkillComposer()
        
        def failing_skill(x):
            raise ValueError("Skill failed")
        
        def should_not_run(x):
            assert False, "Should not be called"
        
        composer.register(TransformSkill("fail", failing_skill))
        composer.register(TransformSkill("never", should_not_run))
        
        result = composer.compose(["fail", "never"], {"test": True})
        assert not result.success
        assert "failed" in result.error.lower()
    
    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.integers()))
    def test_composition_output_becomes_next_input(self, initial_data):
        """Invariant: output of skill i becomes input to skill i+1."""
        composer = SkillComposer()
        received_inputs = []
        
        def track_skill1(x):
            received_inputs.append(('s1', dict(x)))
            return {**x, "from_s1": True}
        
        def track_skill2(x):
            received_inputs.append(('s2', dict(x)))
            return {**x, "from_s2": True}
        
        composer.register(TransformSkill("s1", track_skill1))
        composer.register(TransformSkill("s2", track_skill2))
        
        result = composer.compose(["s1", "s2"], dict(initial_data))
        
        assert result.success
        # s1 receives original input
        assert received_inputs[0][0] == 's1'
        for k, v in initial_data.items():
            assert received_inputs[0][1][k] == v
        # s2 receives output from s1 (must contain from_s1)
        assert received_inputs[1][0] == 's2'
        assert received_inputs[1][1].get("from_s1") is True
        for k, v in initial_data.items():
            assert received_inputs[1][1][k] == v
