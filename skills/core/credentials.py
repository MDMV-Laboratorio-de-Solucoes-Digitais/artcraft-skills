"""Credential Manager for ArtCraft Skills.

Supports both API key (Omni API) and session auth (Omni Gen).
Secure storage, no logging of secrets.
"""

import os
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class Credentials:
    """Credential container."""
    auth_mode: str  # 'api_key' or 'session'
    value: str
    provider_id: Optional[str] = None


class CredentialManager:
    """Manage credentials securely across agent environments."""
    
    def __init__(self):
        self._cache: Dict[str, Credentials] = {}
    
    def get_credentials(self, provider_id: str = "artcraft", 
                       auth_mode: str = "api_key") -> Optional[Credentials]:
        """Get credentials for provider."""
        cache_key = f"{provider_id}:{auth_mode}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Try environment variables
        if auth_mode == "api_key":
            api_key = os.environ.get(f"ARTCRAFT_API_KEY") or os.environ.get(f"{provider_id.upper()}_API_KEY")
            if api_key:
                creds = Credentials(auth_mode="api_key", value=api_key, provider_id=provider_id)
                self._cache[cache_key] = creds
                return creds
        elif auth_mode == "session":
            session = os.environ.get(f"ARTCRAFT_SESSION") or os.environ.get(f"{provider_id.upper()}_SESSION")
            if session:
                creds = Credentials(auth_mode="session", value=session, provider_id=provider_id)
                self._cache[cache_key] = creds
                return creds
        
        return None
    
    def set_credentials(self, credentials: Credentials) -> None:
        """Set credentials (in memory only)."""
        cache_key = f"{credentials.provider_id}:{credentials.auth_mode}"
        self._cache[cache_key] = credentials
    
    def clear_credentials(self, provider_id: str = "artcraft") -> None:
        """Clear credentials for provider."""
        keys_to_remove = [k for k in self._cache if k.startswith(provider_id)]
        for k in keys_to_remove:
            del self._cache[k]
