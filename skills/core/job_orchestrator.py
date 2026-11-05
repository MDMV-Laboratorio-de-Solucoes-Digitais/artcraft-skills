"""Job Orchestrator for async generation jobs."""

import uuid
import time
from typing import Dict, Any, Optional, List
from enum import Enum


class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Job:
    def __init__(self, job_token: str, skill_name: str):
        self.job_token = job_token
        self.all_tokens = [job_token]
        self.skill_name = skill_name
        self.status = JobStatus.PENDING
        self.idempotency_token = str(uuid.uuid4())
        self.created_at = time.time()
        self.results = []
        self.webhooks: List[str] = []
        self.payload: Dict[str, Any] = {}


class JobOrchestrator:
    """Orchestrate async jobs with idempotency, polling, webhooks."""

    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def submit(self, skill_name: str, inputs: Dict[str, Any],
               idempotency_token: Optional[str] = None) -> Job:
        """Submit a job."""
        if idempotency_token and self._check_idempotency(idempotency_token):
            return self._get_by_idempotency(idempotency_token)

        job_token = str(uuid.uuid4())
        job = Job(job_token, skill_name)
        if idempotency_token:
            job.idempotency_token = idempotency_token
        self.jobs[job_token] = job
        return job

    def poll(self, job_token: str, timeout: int = 300) -> Job:
        """Poll job status."""
        job = self.jobs.get(job_token)
        if not job:
            raise ValueError(f"Job {job_token} not found")
        # Stub - in real implementation would poll API
        job.status = JobStatus.COMPLETED
        return job

    def wait_for_completion(self, job_token: str, timeout: int = 300) -> Job:
        """Wait for job to complete."""
        return self.poll(job_token, timeout)

    def register_webhook(self, job_token: str, url: str) -> bool:
        """Register a webhook URL for job status callbacks (FR-005)."""
        job = self.jobs.get(job_token)
        if not job or not url:
            return False
        if url not in job.webhooks:
            job.webhooks.append(url)
        return True

    def get_webhooks(self, job_token: str) -> List[str]:
        """Return registered webhook URLs for a job."""
        job = self.jobs.get(job_token)
        return list(job.webhooks) if job else []

    def handle_webhook_callback(self, job_token: str, payload: Dict[str, Any]) -> Optional[Job]:
        """Handle an inbound webhook callback payload (FR-005).

        Expected payload keys (contract): status, result?, error?.
        Unknown jobs return None. This provides the webhook handling surface;
        transport/auth verification is adapter-specific.
        """
        job = self.jobs.get(job_token)
        if not job or not isinstance(payload, dict):
            return None
        status = (payload.get("status") or "").lower()
        status_map = {
            "pending": JobStatus.PENDING,
            "processing": JobStatus.PROCESSING,
            "completed": JobStatus.COMPLETED,
            "failed": JobStatus.FAILED,
            "cancelled": JobStatus.CANCELLED,
        }
        if status in status_map:
            job.status = status_map[status]
        if "result" in payload:
            job.results.append(payload["result"])
        if "error" in payload:
            job.payload["error"] = payload["error"]
        job.payload["last_webhook"] = payload
        return job

    def _check_idempotency(self, token: str) -> bool:
        return any(j.idempotency_token == token for j in self.jobs.values())

    def _get_by_idempotency(self, token: str) -> Optional[Job]:
        for j in self.jobs.values():
            if j.idempotency_token == token:
                return j
        return None
