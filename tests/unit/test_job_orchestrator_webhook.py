"""Unit tests for job orchestrator webhook support (T105)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from skills.core.job_orchestrator import JobOrchestrator, JobStatus


def test_register_webhook():
    orch = JobOrchestrator()
    job = orch.submit("test-skill", {"x": 1})
    ok = orch.register_webhook(job.job_token, "https://example.com/hook")
    assert ok is True
    hooks = orch.get_webhooks(job.job_token)
    assert "https://example.com/hook" in hooks


def test_handle_webhook_callback_updates_status():
    orch = JobOrchestrator()
    job = orch.submit("test-skill", {"x": 1})
    orch.register_webhook(job.job_token, "https://example.com/hook")
    result = orch.handle_webhook_callback(job.job_token, {"status": "completed", "result": {"ok": True}})
    assert result is not None
    assert result.status == JobStatus.COMPLETED


def test_webhook_callback_rejects_unknown_job():
    orch = JobOrchestrator()
    result = orch.handle_webhook_callback("nope", {"status": "completed"})
    assert result is None
