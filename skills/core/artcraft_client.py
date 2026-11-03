"""ArtCraft API adapters for both auth modes."""

from typing import Dict, Any, Optional
from .credentials import CredentialManager, Credentials


class OmniApiClient:
    """Client for /v1/omni_api/* (API key auth)."""
    
    def __init__(self, base_url: str = "https://api.storyteller.ai", 
                 credentials: Optional[Credentials] = None):
        self.base_url = base_url
        self.credentials = credentials or CredentialManager().get_credentials(auth_mode="api_key")
    
    def generate_image(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image via Omni API."""
        # Stub implementation
        return {"job_token": "stub", "status": "pending"}
    
    def get_job_status(self, job_token: str) -> Dict[str, Any]:
        """Get job status."""
        return {"status": "completed", "results": []}


class OmniGenClient:
    """Client for /v1/omni_gen/* (session auth)."""
    
    def __init__(self, base_url: str = "https://api.storyteller.ai",
                 credentials: Optional[Credentials] = None):
        self.base_url = base_url
        self.credentials = credentials or CredentialManager().get_credentials(auth_mode="session")
    
    def generate_image(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image via Omni Gen API."""
        return {"job_token": "stub", "status": "pending"}
    
    def get_job_status(self, job_token: str) -> Dict[str, Any]:
        """Get job status."""
        return {"status": "completed", "results": []}
