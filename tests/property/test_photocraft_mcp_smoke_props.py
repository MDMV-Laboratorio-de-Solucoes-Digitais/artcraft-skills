"""007 RED/property invariants: PhotoCraft MCP verified local smoke (T004,T005).

Deterministic, no sleeps, no real PhotoCraft server/binary in default CI.
Covers 007 invariants:
- explicit opt-in required; excluded from default CI
- stateless smoke target is tools/list + tools/call name=command_list only
- no prompt-based AI generation/provider/model claim
- safe roots: temp auto-created absolute roots cleaned by harness; explicit
  authorized absolute overrides are maintainer-managed (never auto-deleted)
- minimal, version-tolerant assertions (no exact tool count/catalog equality)
- FR-006-aligned actionable outcomes; public schemas/CLI/fallback/FR-005 unchanged
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest  # noqa: E402
from hypothesis import given, settings, strategies as st  # noqa: E402

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")
