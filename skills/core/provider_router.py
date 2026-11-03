"""Model/Provider Router supporting ArtCraft's 60+ model ecosystem."""

from typing import Dict, Any, List, Optional


class ModelProvider:
    """Provider abstraction."""
    
    def __init__(self, provider_id: str, name: str, models: List[str]):
        self.provider_id = provider_id
        self.name = name
        self.models = models


class ProviderRouter:
    """Route requests to appropriate providers."""
    
    def __init__(self):
        self.providers = {
            "artcraft": ModelProvider("artcraft", "ArtCraft", 
                                     ["nano-banana", "gpt-image", "flux", "seedream", 
                                      "seedance", "kling", "veo", "sora"]),
            "grok": ModelProvider("grok", "Grok", ["grok-imagine", "grok-video"]),
            "midjourney": ModelProvider("midjourney", "Midjourney", ["midjourney"]),
            "sora": ModelProvider("sora", "Sora", ["sora-1", "sora-2"]),
            "worldlabs": ModelProvider("worldlabs", "World Labs", ["marble"]),
        }
    
    def route(self, capability: str, model_preference: Optional[str] = None) -> ModelProvider:
        """Route request based on capability."""
        if model_preference and model_preference in self.providers:
            return self.providers[model_preference]
        # Default to ArtCraft
        return self.providers["artcraft"]
    
    def get_models_for_capability(self, capability: str) -> List[str]:
        """Get all models supporting capability."""
        models = []
        for provider in self.providers.values():
            models.extend(provider.models)
        return models
