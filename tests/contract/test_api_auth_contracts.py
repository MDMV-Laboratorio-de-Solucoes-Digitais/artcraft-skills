"""Contract tests for FR-004 auth adapter abstractions (T107)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_client
from skills.core.credentials import Credentials


def test_omni_api_client_contract():
    c = artcraft_client.OmniApiClient(credentials=Credentials(auth_mode="api_key", value="test-key", provider_id="artcraft"))
    assert c.credentials.value == "test-key"
    assert hasattr(c, "generate_image")
    assert hasattr(c, "get_job_status")


def test_omni_gen_client_contract():
    c = artcraft_client.OmniGenClient(credentials=Credentials(auth_mode="session", value="sess", provider_id="artcraft"))
    assert c.credentials.value == "sess"
    assert hasattr(c, "generate_image")
    assert hasattr(c, "get_job_status")
