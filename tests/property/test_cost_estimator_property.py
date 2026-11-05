"""Property-based tests for cost estimator (T106)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from hypothesis import given, strategies as st
from skills.core.cost_estimator import CostEstimator


@given(st.sampled_from(["image-generate", "image-edit", "mesh-generate", "video-gen"]))
def test_cost_estimate_has_fields(skill_name):
    est = CostEstimator()
    r = est.estimate(skill_name, {}, provider="artcraft", model="nano-banana")
    assert r.provider == "artcraft"
    assert r.model
    assert r.estimated_credits >= 0
    assert r.estimated_usd >= 0
