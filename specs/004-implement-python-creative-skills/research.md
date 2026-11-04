# Research: Implement Python Creative Skills

**Slug**: implement-python-creative-skills
**Date**: 2026-11-04

## Summary

This feature implements executable Python `skill.py` files for four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) that currently exist only as declarative `SKILL.md` scaffolds. Each skill uses the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) and follows the `image-generate/skill.py` template pattern.

## Research Findings

### Source: /speckit.clarify (Session 2026-11-04)

All four clarification questions were resolved autonomously based on research evidence from codebase deep-dives and online research:

1. **Observability / Logging** → Add structured JSON logging via existing `setup_logging()` in `skills/core/utils.py`. PII/secrets MUST be redacted at write time.
   - Evidence: AWS Well-Architected AGENTOPS05-BP03, OpenTelemetry GenAI semantic conventions, LangChain ADLC, Strands Agents all converge on structured logging + RED metrics for agent skills.
   - Codebase: Only `logging` import exists in `skills/core/utils.py` (line 2), `setup_logging()` defined but never called — dead code ready to be activated.

2. **Rate limiting** → Retry CLI invocations with exponential backoff + jitter (max 3 retries). Skills MUST use semaphore-based concurrency limiter (max 3 concurrent CLI invocations per skill instance).
   - Evidence: Alibaba Cloud Model Studio rate-limiting best practices, SpillwaveSolutions subprocess patterns, SciPy Proceedings on bounded semaphore API gate (~5x throughput improvement with bounded semaphore).
   - Codebase: NO rate limiting infrastructure exists anywhere in `skills/core/` or `skills/creative/` (confirmed by full repo grep).

3. **Asset uniqueness** → `asset_id` MUST be pass-through from CLI/MCP output (no server-side generation). Skills MAY optionally use content-addressing (SHA-256) for caching/deduplication but MUST NOT generate asset IDs independently.
   - Evidence: arXiv:2606.31272 per-component skill identity fingerprinting; aivitamin.org content hash cache pattern; no agentskills.io standard exists for asset uniqueness.
   - Codebase: No `import uuid`, `hashlib`, or content-addressing infrastructure exists in `skills/core/`.

4. **Concurrent execution** → Semaphore-based concurrency limiter (max 3 concurrent CLI invocations per skill instance).
   - Evidence: SpillwaveSolutions subprocess patterns, SciPy Proceedings on bounded semaphore API gate (~5x throughput improvement).
   - Codebase: `JobOrchestrator` uses synchronous dict operations, no threading/asyncio/multiprocessing anywhere in `skills/`.

### Source: /speckit.specify (Session 2026-11-04)

- Q1 Answer B: Common superset schema (`image`, `prompt`, `model`, `mode`, `cli_path`, `mcp_config`, `command_keywords`, `generation_command`) plus skill-specific extras.
- Q2 Answer B: Broader keyword lists covering synonyms for each skill.
- Q3 Answer B: Extract a `CreativeSkill` base class in `skills/core/`.

### Source: codebase deep-dives (10 agents)

- **`skills/core/base_skill.py`**: `SkillResult` dataclass with `success`, `data`, `error`, `metadata` fields. `BaseSkill` ABC with abstract `get_input_schema()`, `get_output_schema()`, `execute()` methods.
- **`skills/core/artcraft_app_client.py`**: 9 public functions (`discover_cli`, `discover_generation_command`, `normalize_output`, `normalize_mcp_config`, `run_cli`, `discover_cli_commands`, `run_cli_generation`, `select_mode`, `standardize_error`) + `__version__ = "0.2.0"` + `__all__` + reason codes.
- **`skills/creative/image-generate/skill.py`**: Complete working template implementing `ImageGenerateSkill(BaseSkill)` with all adapter integration patterns.
- **No logging infrastructure**: Only `import logging` + unused `setup_logging()` in `skills/core/utils.py`.
- **No rate limiting infrastructure**: Confirmed by full `skills/` grep for `ratelimit`, `retry`, `sleep`, `backoff`, `Semaphore`, `bucket`.
- **No asset uniqueness infrastructure**: `asset_id` is pass-through from CLI/MCP output only.

## Decisions

| Decision | Rationale |
|----------|-----------|
| Extract `CreativeSkill` base class | Encapsulates discover→resolve→invoke→normalize→degrade flow; each skill becomes thin subclass; single point of change |
| Use superset schema + skill-specific extras | Matches `image-generate` pattern while allowing per-skill customization (e.g., `mask` for image-edit, `scale` for image-upscale, `format` for mesh-generate) |
| Broader keyword lists | Increases command match probability across `photocraft-cli` 500+ command registry |
| Structured logging via `setup_logging()` | Existing infrastructure, just needs activation; follows AWS Well-Architected + OpenTelemetry GenAI conventions |
| Retry with backoff + jitter (max 3) | Handles transient CLI failures without over-engineering |
| Semaphore concurrency (max 3) | Prevents resource exhaustion from concurrent CLI invocations |
| `asset_id` pass-through only | No agentskills.io standard for asset uniqueness; avoids over-engineering |

## Files to Create

- `skills/core/creative_skill.py` — `CreativeSkill` base class
- `skills/creative/image-edit/skill.py` — Image edit skill
- `skills/creative/background-remove/skill.py` — Background remove skill
- `skills/creative/image-upscale/skill.py` — Image upscale skill
- `skills/creative/mesh-generate/skill.py` — Mesh generate skill

## Files to Update

- `skills/core/utils.py` — Activate `setup_logging()` calls in skill modules (optional, skills call it)

## Contracts

No new `contracts/` directory needed — this feature uses the existing `skills/core/artcraft_app_client.py` adapter contract and `skills/core/base_skill.py` base class contract, both already existing in the codebase.
