"""Contract tests for FR-004 auth adapter abstractions (T107)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core import artcraft_client


def test_omni_api_client_contract():
    c = artcraft_client.OmniApiClient(api_key="test-key")
    assert c.api_key == "test-key"
    assert hasattr(c, "submit_job")
    assert hasattr(c, "get_job_status")


def test_omni_gen_client_contract():
    c = artcraft_client.OmniGenClient(session_id="sess", api_base="https://example.invalid")
    assert c.session_id == "sess"
    assert hasattr(c, "submit_job")
    assert hasattr(c, "get_job_status")
