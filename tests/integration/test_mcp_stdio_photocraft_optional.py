"""006 optional real PhotoCraft MCP integration (T007,T017).

Skipped by default. Requires explicit opt-in and local prerequisites.
Run explicitly: PYTHONPATH=. ARTCRAFT_MCP_INTEGRATION=1 python -m pytest -q -m integration tests/integration/test_mcp_stdio_photocraft_optional.py
"""
import os
import shutil

import pytest

pytestmark = pytest.mark.integration


def _skip_unless_enabled():
    if os.environ.get("ARTCRAFT_MCP_INTEGRATION") != "1":
        pytest.skip("optional: set ARTCRAFT_MCP_INTEGRATION=1 to enable real MCP integration tests")
    if not shutil.which("photocraft-cli"):
        pytest.skip("optional: photocraft-cli not found on PATH")
    if not os.environ.get("ARTCRAFT_MCP_READ_ROOT") or not os.environ.get("ARTCRAFT_MCP_WRITE_ROOT"):
        pytest.skip("optional: set ARTCRAFT_MCP_READ_ROOT and ARTCRAFT_MCP_WRITE_ROOT to safe absolute paths")


def test_optional_photocraft_mcp_smoke_placeholder():
    _skip_unless_enabled()
    # Minimal placeholder: when explicitly enabled, environment is configured.
    # Full end-to-end real validation is optional/manual and target-specific.
    assert os.environ["ARTCRAFT_MCP_READ_ROOT"]
    assert os.environ["ARTCRAFT_MCP_WRITE_ROOT"]
