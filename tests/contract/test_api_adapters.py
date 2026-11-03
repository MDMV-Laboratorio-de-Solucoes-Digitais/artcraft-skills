"""Contract tests for API adapters.

Tests verify that API adapters follow expected contracts:
- OmniApiClient for /v1/omni_api/* (API key auth)
- OmniGenClient for /v1/omni_gen/* (session auth)
"""
import os
import sys

# Ensure repo root in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from skills.core.artcraft_client import OmniApiClient, OmniGenClient
from skills.core.credentials import CredentialManager, Credentials


def test_omni_api_client_has_required_methods():
    """OmniApiClient must implement required API methods."""
    client = OmniApiClient()
    assert hasattr(client, 'generate_image')
    assert hasattr(client, 'get_job_status')
    assert callable(client.generate_image)
    assert callable(client.get_job_status)


def test_omni_gen_client_has_required_methods():
    """OmniGenClient must implement required API methods."""
    client = OmniGenClient()
    assert hasattr(client, 'generate_image')
    assert hasattr(client, 'get_job_status')
    assert callable(client.generate_image)
    assert callable(client.get_job_status)


def test_omni_api_client_accepts_credentials():
    """OmniApiClient should accept credentials."""
    creds = Credentials(auth_mode="api_key", value="test-key", provider_id="artcraft")
    client = OmniApiClient(credentials=creds)
    assert client.credentials is not None
    assert client.credentials.auth_mode == "api_key"


def test_omni_gen_client_accepts_credentials():
    """OmniGenClient should accept credentials."""
    creds = Credentials(auth_mode="session", value="test-session", provider_id="artcraft")
    client = OmniGenClient(credentials=creds)
    assert client.credentials is not None
    assert client.credentials.auth_mode == "session"


def test_omni_api_client_generate_image_returns_dict():
    """OmniApiClient.generate_image must return a dict with job info."""
    client = OmniApiClient(credentials=Credentials(auth_mode="api_key", value="test"))
    result = client.generate_image({"prompt": "test"})
    assert isinstance(result, dict)
    assert "job_token" in result or "status" in result


def test_omni_gen_client_generate_image_returns_dict():
    """OmniGenClient.generate_image must return a dict with job info."""
    client = OmniGenClient(credentials=Credentials(auth_mode="session", value="test"))
    result = client.generate_image({"prompt": "test"})
    assert isinstance(result, dict)
    assert "job_token" in result or "status" in result


def test_omni_api_client_get_job_status_returns_dict():
    """OmniApiClient.get_job_status must return status information."""
    client = OmniApiClient(credentials=Credentials(auth_mode="api_key", value="test"))
    status = client.get_job_status("test-token")
    assert isinstance(status, dict)
    assert "status" in status


def test_omni_gen_client_get_job_status_returns_dict():
    """OmniGenClient.get_job_status must return status information."""
    client = OmniGenClient(credentials=Credentials(auth_mode="session", value="test"))
    status = client.get_job_status("test-token")
    assert isinstance(status, dict)
    assert "status" in status


def test_adapters_support_both_auth_modes():
    """Both adapters must support their respective auth modes."""
    api_client = OmniApiClient(credentials=Credentials(auth_mode="api_key", value="key"))
    gen_client = OmniGenClient(credentials=Credentials(auth_mode="session", value="sess"))
    assert api_client.credentials.auth_mode == "api_key"
    assert gen_client.credentials.auth_mode == "session"
