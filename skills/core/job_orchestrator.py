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
    
    def _check_idempotency(self, token: str) -> bool:
        return any(j.idempotency_token == token for j in self.jobs.values())
    
    def _get_by_idempotency(self, token: str) -> Optional[Job]:
        for j in self.jobs.values():
            if j.idempotency_token == token:
                return j
        return None
