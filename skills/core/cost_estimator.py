"""Cost Estimator for transparency before execution."""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CostEstimate:
    """Cost estimate for a skill execution."""
    estimated_credits: float
    estimated_usd: float
    provider: str
    model: str
    breakdown: Dict[str, float]


class CostEstimator:
    """Estimate costs before executing paid operations."""
    
    # Rough pricing (example values)
    PRICING = {
        "image": {"nano-banana": 0.01, "gpt-image": 0.04, "flux": 0.003},
        "video": {"seedance": 0.10, "kling": 0.15, "veo": 0.20},
        "3d": {"tripo": 0.05, "rodin": 0.08, "meshy": 0.10},
    }
    
    def estimate(self, skill_name: str, inputs: Dict[str, Any],
                 provider: str = "artcraft", model: str = "nano-banana") -> CostEstimate:
        """Estimate cost for skill execution."""
        # Determine category from skill name
        category = "image"
        if "video" in skill_name:
            category = "video"
        elif "mesh" in skill_name or "3d" in skill_name:
            category = "3d"
        
        credits = self.PRICING.get(category, {}).get(model, 0.01)
        usd = credits * 0.01  # Example conversion
        
        return CostEstimate(
            estimated_credits=credits,
            estimated_usd=usd,
            provider=provider,
            model=model,
            breakdown={skill_name: credits}
        )
    
    def show_estimate(self, estimate: CostEstimate) -> str:
        """Format cost estimate for display."""
        return f"Estimated cost: {estimate.estimated_credits} credits (${estimate.estimated_usd:.4f}) via {estimate.provider}/{estimate.model}"
