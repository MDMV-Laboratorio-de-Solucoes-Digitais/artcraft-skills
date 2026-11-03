"""Integration tests for job orchestration (US2)."""

import time

import pytest
from hypothesis import given, strategies as st

from skills.core.job_orchestrator import Job, JobOrchestrator, JobStatus


class TestJobOrchestrator:
    """Test job orchestration functionality."""

    def test_orchestrator_initialization(self):
        """Orchestrator should initialize correctly."""
        orch = JobOrchestrator()
        assert orch is not None
        assert hasattr(orch, "submit")
        assert hasattr(orch, "poll")
        assert hasattr(orch, "wait_for_completion")
        assert isinstance(orch.jobs, dict)

    def test_job_initialization(self):
        """Job should initialize correctly."""
        job_token = "test-token-123"
        job = Job(job_token, "test_skill")
        assert job.job_token == job_token
        assert job.skill_name == "test_skill"
        assert job.status == JobStatus.PENDING
        assert isinstance(job.all_tokens, list)
        assert job_token in job.all_tokens
        assert isinstance(job.idempotency_token, str)
        assert isinstance(job.created_at, float)
        assert isinstance(job.results, list)

    def test_submit_job(self):
        """Submitting a job should create and store it."""
        orch = JobOrchestrator()
        inputs = {"prompt": "test prompt", "count": 5}
        job = orch.submit("image_gen", inputs)
        assert isinstance(job, Job)
        assert job.skill_name == "image_gen"
        assert job.status == JobStatus.PENDING
        assert job.job_token in orch.jobs
        assert orch.jobs[job.job_token] == job

    def test_submit_multiple_jobs(self):
        """Should be able to submit multiple jobs."""
        orch = JobOrchestrator()
        job1 = orch.submit("skill_a", {"x": 1})
        job2 = orch.submit("skill_b", {"y": 2})
        job3 = orch.submit("skill_c", {"z": 3})
        assert len(orch.jobs) == 3
        assert job1.job_token != job2.job_token
        assert job1.job_token != job3.job_token
        assert job2.job_token != job3.job_token

    def test_poll_job(self):
        """Polling a job should update status."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {"data": "test"})
        polled_job = orch.poll(job.job_token)
        assert polled_job == job
        assert polled_job.status == JobStatus.COMPLETED

    def test_wait_for_completion(self):
        """Waiting for completion should return completed job."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {"data": "test"})
        completed_job = orch.wait_for_completion(job.job_token)
        assert completed_job == job
        assert completed_job.status == JobStatus.COMPLETED

    def test_poll_nonexistent_job_raises_error(self):
        """Polling non-existent job should raise ValueError."""
        orch = JobOrchestrator()
        with pytest.raises(ValueError, match="Job .* not found"):
            orch.poll("nonexistent-token")

    def test_wait_for_nonexistent_job_raises_error(self):
        """Waiting for non-existent job should raise ValueError."""
        orch = JobOrchestrator()
        with pytest.raises(ValueError, match="Job .* not found"):
            orch.wait_for_completion("nonexistent-token")

    def test_idempotency_with_token(self):
        """Submitting with same idempotency token should return existing job."""
        orch = JobOrchestrator()
        idempotency_token = "idem-12345"
        job1 = orch.submit("test_skill", {"x": 1}, idempotency_token=idempotency_token)
        job2 = orch.submit("test_skill", {"x": 2}, idempotency_token=idempotency_token)
        assert job1.job_token == job2.job_token
        assert len(orch.jobs) == 1

    def test_idempotency_without_conflict(self):
        """Different idempotency tokens should create different jobs."""
        orch = JobOrchestrator()
        job1 = orch.submit("test_skill", {"x": 1}, idempotency_token="idem-1")
        job2 = orch.submit("test_skill", {"x": 2}, idempotency_token="idem-2")
        assert job1.job_token != job2.job_token
        assert len(orch.jobs) == 2

    def test_idempotency_preserves_original_job(self):
        """Idempotent submission should return original job unchanged."""
        orch = JobOrchestrator()
        idempotency_token = "idem-abc"
        inputs1 = {"prompt": "original"}
        job1 = orch.submit("image_gen", inputs1, idempotency_token=idempotency_token)
        original_token = job1.job_token
        job2 = orch.submit("image_gen", {"prompt": "different"}, idempotency_token=idempotency_token)
        assert job2.job_token == original_token
        assert job2.skill_name == "image_gen"

    def test_submit_with_custom_idempotency_token_stored(self):
        """Custom idempotency token should be stored on job."""
        orch = JobOrchestrator()
        idempotency_token = "custom-idem-token"
        job = orch.submit("test_skill", {"x": 1}, idempotency_token=idempotency_token)
        assert job.idempotency_token == idempotency_token

    def test_job_status_transitions(self):
        """Job status should transition correctly."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {})
        assert job.status == JobStatus.PENDING
        orch.poll(job.job_token)
        assert job.status == JobStatus.COMPLETED

    def test_poll_with_timeout_parameter(self):
        """Poll should accept timeout parameter."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {})
        polled_job = orch.poll(job.job_token, timeout=60)
        assert polled_job.status == JobStatus.COMPLETED

    def test_wait_for_completion_with_timeout_parameter(self):
        """wait_for_completion should accept timeout parameter."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {})
        completed_job = orch.wait_for_completion(job.job_token, timeout=120)
        assert completed_job.status == JobStatus.COMPLETED

    def test_job_all_tokens_contains_job_token(self):
        """all_tokens should contain the job token."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", {})
        assert job.job_token in job.all_tokens
        assert len(job.all_tokens) >= 1

    def test_orchestrator_tracks_all_jobs(self):
        """Orchestrator should track all submitted jobs."""
        orch = JobOrchestrator()
        jobs = []
        for i in range(5):
            job = orch.submit(f"skill_{i}", {"index": i})
            jobs.append(job)
        assert len(orch.jobs) == 5
        for job in jobs:
            assert job.job_token in orch.jobs

    @given(st.text(min_size=1, max_size=50))
    def test_submit_various_skill_names(self, skill_name):
        """Should handle various skill names."""
        orch = JobOrchestrator()
        job = orch.submit(skill_name, {"test": True})
        assert job.skill_name == skill_name
        assert job.status == JobStatus.PENDING

    @given(st.dictionaries(st.text(min_size=1), st.integers()))
    def test_submit_various_inputs(self, inputs):
        """Should handle various input dictionaries."""
        orch = JobOrchestrator()
        job = orch.submit("test_skill", inputs)
        assert job.job_token in orch.jobs

    @given(st.text(min_size=1, max_size=100))
    def test_idempotency_with_various_tokens(self, idempotency_token):
        """Idempotency should work with various token strings."""
        orch = JobOrchestrator()
        job1 = orch.submit("test_skill", {"a": 1}, idempotency_token=idempotency_token)
        job2 = orch.submit("test_skill", {"a": 2}, idempotency_token=idempotency_token)
        assert job1.job_token == job2.job_token

    def test_job_results_list_initialized_empty(self):
        """Job results should be initialized as empty list."""
        job = Job("token123", "skill_name")
        assert isinstance(job.results, list)
        assert len(job.results) == 0

    def test_job_status_enum_values(self):
        """JobStatus enum should have expected values."""
        assert JobStatus.PENDING.value == "pending"
        assert JobStatus.PROCESSING.value == "processing"
        assert JobStatus.COMPLETED.value == "completed"
        assert JobStatus.FAILED.value == "failed"
        assert JobStatus.CANCELLED.value == "cancelled"

    def test_integration_full_job_lifecycle(self):
        """Test full job lifecycle from submission to completion."""
        orch = JobOrchestrator()
        inputs = {"prompt": "generate image", "style": "anime"}
        job = orch.submit("image_generator", inputs)
        assert job.status == JobStatus.PENDING
        assert job.skill_name == "image_generator"
        completed = orch.wait_for_completion(job.job_token, timeout=300)
        assert completed.status == JobStatus.COMPLETED
        assert completed.job_token == job.job_token
        assert completed in orch.jobs.values()
