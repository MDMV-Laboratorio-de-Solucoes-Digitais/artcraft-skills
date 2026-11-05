"""Contract tests for FR-004 auth adapter abstractions (T107)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_client
from skills.core.credentials import Credentials


def test_omni_api_client_contract():
    c = artcraft_client.OmniApiClient(credentials=Credentials(auth_mode="api_key", api_key="test-key"))
    assert c.credentials.api_key == "test-key"
    assert hasattr(c, "generate_image")
    assert hasattr(c, "get_job_status")


def test_omni_gen_client_contract():
    c = artcraft_client.OmniGenClient(credentials=Credentials(auth_mode="session", session_token="sess"))
    assert c.credentials.session_token == "sess"
    assert hasattr(c, "generate_image")
    assert hasattr(c, "get_job_status")
