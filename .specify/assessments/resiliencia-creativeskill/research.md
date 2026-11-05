# Idea Research: Resiliência ao CreativeSkill (retry + backoff + jitter + semáforo)

- **Slug**: resiliencia-creativeskill
- **Created**: 2026-11-04
- **Evidence confidence (overall)**: high

## Users & Demand

- **Pain point**: CLI calls fail transiently (timeouts, non-zero exits) causing skills to fail immediately with no retry — high friction for production use. — [source: specs/004-implement-python-creative-skills/research.md | cited] (confidence: high)
- **Need**: Bounded concurrency to prevent resource exhaustion under parallel agent calls. — [source: specs/004-implement-python-creative-skills/research.md, clarification 2026-11-04 | cited] (confidence: high)

## Prior Art

- **Feature 004 research**: Explicitly identified "Retry CLI invocations with exponential backoff + jitter (max 3 retries)" and "semaphore-based concurrency limiter (max 3 concurrent CLI invocations per skill instance)" with references to AWS Well-Architected, Alibaba Cloud Model Studio, SpillwaveSolutions, SciPy Proceedings. — [source: specs/004-implement-python-creative-skills/research.md | cited] (confidence: high)
- **Current implementation**: `skills/core/creative_skill.py` has no retry/backoff/semaphore; `_execute_cli` catches `TimeoutExpired` and non-zero exits but returns immediately. — [source: codebase inspection | cited] (confidence: high)
- **Image-generate template**: Same pattern, no resilience — confirms gap applies to all skills using the base/adapter pattern. — [source: skills/creative/image-generate/skill.py | cited] (confidence: high)

## Market & Context

- **Industry standard**: Exponential backoff + jitter is standard for transient failures (AWS Architecture Blog, Google SRE practices). Bounded semaphores are standard for subprocess/concurrency control. — [source: industry best practices | cited] (confidence: high)
- **Cost of doing nothing**: Skills fail on transient CLI issues, reducing reliability for agent workflows; parallel invocations risk resource exhaustion. — [source: specs/004-implement-python-creative-skills/research.md | cited] (confidence: high)

## Data & Constraints

- **Constraints**: Must not change `SkillResult` contract, must be backward compatible, must not break existing tests (351 passing). — [source: codebase/tests | cited] (confidence: high)
- **Scope**: Apply to all skills inheriting from `CreativeSkill` (5 creative skills currently). — [source: skills/core/creative_skill.py | cited] (confidence: high)
- **Limits suggested**: max 3 retries, max 3 concurrent CLI invocations per instance — per feature 004 research. — [source: specs/004-implement-python-creative-skills/research.md | cited] (confidence: high)

## Evidence Against the Idea

- **Complexity**: Adds threading/synchronization concerns; need to ensure thread-safety and testability with mocks. — [source: codebase patterns (no existing threading) | cited] (confidence: medium)
- **Over-engineering risk**: If CLI is fundamentally broken, retries won't help. — [source: general practice | assumption] (confidence: medium)
- **Test impact**: Existing tests mock methods directly; need to ensure retry logic doesn't interfere with mocked flows. — [source: tests/property/test_creative_skills_props.py, tests/characterization/test_creative_skills_behavior.py | cited] (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: Exact backoff parameters (base, max, jitter algorithm)?]
- [NEEDS CLARIFICATION: Retry on all non-zero exits or only specific ones?]
- [NEEDS CLARIFICATION: Semaphore scope (instance-level vs class-level)?]
- [NEEDS CLARIFICATION: Should retries be configurable via inputs?]
- [NEEDS CLARIFICATION: How to preserve error metadata across retries?]

## Sources

- specs/004-implement-python-creative-skills/research.md (host: local repo, policy: allowlisted)
- skills/core/creative_skill.py (host: local repo, policy: allowlisted)
- skills/creative/image-generate/skill.py (host: local repo, policy: allowlisted)
- tests/property/test_creative_skills_props.py (host: local repo, policy: allowlisted)
- tests/characterization/test_creative_skills_behavior.py (host: local repo, policy: allowlisted)
