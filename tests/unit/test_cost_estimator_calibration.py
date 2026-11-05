"""Calibration/property tests for cost estimator (T106, FR-006)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.cost_estimator import CostEstimator


SUPPORTED_CALIBRATION = {
    # (category, model, reference_credits) - documented baseline for supported subset
    ("image", "nano-banana"): 0.01,
    ("image", "flux"): 0.003,
    ("3d", "tripo"): 0.05,
}


def test_estimate_includes_required_fields():
    est = CostEstimator()
    r = est.estimate("image-generate", {}, provider="artcraft", model="nano-banana")
    assert r.provider
    assert r.model
    assert r.estimated_credits is not None
    assert r.estimated_usd is not None


def test_calibration_within_20_percent_for_supported_subset():
    est = CostEstimator()
    for (category, model), reference in SUPPORTED_CALIBRATION.items():
        skill = "mesh-generate" if category == "3d" else "image-generate"
        r = est.estimate(skill, {}, provider="artcraft", model=model)
        assert abs(r.estimated_credits - reference) / max(reference, 1e-9) <= 0.20, (
            f"{category}/{model}: {r.estimated_credits} vs {reference}"
        )
