# Repository Guidelines

## Project Overview

ArtCraft Skills Suite: open-source, composable AI agent skills ecosystem following the [agentskills.io](https://agentskills.io) standard. Skills provide "build before generating" workflows across 2D/raster, vector, 3D/spatial, video/motion, audio, documents/presentations, and CAD/technical design. Two implementation tiers: declarative `SKILL.md` skills (most creative/integration/workflow) and Python `BaseSkill` subclasses (image-generate and shared adapter). Governed by `.specify/memory/constitution.md` (v2.0.0).

## Architecture & Data Flow

- **Skill System**: Each skill is `skills/{category}/{name}/` with `SKILL.md` (YAML frontmatter + Markdown body). Categories: `core/`, `creative/`, `integration/`, `workflow/`.
- **Discovery/Loading**: `scripts/skill_loader.py` (`SkillLoader`) recursively finds `SKILL.md`, parses frontmatter (requires `---` delimiters), loads metadata/content, flags `scripts/`, `references/`, `assets/`.
- **Validation**: `scripts/validate_skill.py` enforces agentskills.io rules (kebab-case name matching dir, description 1–1024 chars, optional compatibility ≤500). `validate_all_skills.py` skips `template/` and `example-skill/`.
- **Registration**: `scripts/register_skills.py` updates `.specify/extensions/.registry`.
- **Core abstractions** (`skills/core/`): `BaseSkill`/`SkillResult` contract; `SkillComposer` (sequential/parallel composition, short-circuits on failure); `DAGOrchestrator` (cycle detection, readiness, wave execution); plus job orchestration, credentials, provider routing, asset handling, cost estimation.
- **Shared adapter** (`skills/core/artcraft_app_client.py`): stateless CLI/MCP infrastructure (discovery, invocation, normalization, mode selection, error standardization) extracted from image-generate; reason-code constants; `__version__`.
- **Data flow**: Author `SKILL.md` → validate → load → register → consume by agents/composers. Python skills execute synchronously returning `SkillResult`.
- **Python skills** (e.g. `creative/image-generate/skill.py`) delegate to the shared adapter and keep schemas/validation/orchestration/`SkillResult` construction.

## Key Directories

- `skills/` — skill packages by category. `core/` holds base abstractions and utilities.
- `scripts/` — Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py` (stdlib + PyYAML).
- `tests/` — `unit/`, `integration/`, `contract/`, `property/`, `characterization/`, `_helpers/`, `reference/`, `golden/`. No root `conftest.py`.
- `specs/` — feature specs/plans/tasks/contracts/checklists (Spec Kit).
- `docs/` — guides: skill-authoring, core-abstractions, cross-product, generalizable-workflows.
- `.specify/` — Spec Kit templates, memory (constitution v2.0.0), workflows, extensions, scripts.
- `.omp/` — OMP command definitions mirroring Spec Kit.

## Development Commands

```bash
# Validate a single skill
python scripts/validate_skill.py skills/category/skill-name

# Validate all non-template/example skills
python scripts/validate_all_skills.py

# Discover and print skills
python scripts/skill_loader.py

# Register skills into Spec Kit registry
python scripts/register_skills.py

# Run all tests
pytest

# Run tests by layer
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
pytest tests/property/

# Run specific test
pytest tests/unit/test_image_generate.py -v
pytest -v -x
```

No build step and no package manager: dependencies (PyYAML, pytest, hypothesis) are assumed installed. Tests run from repo root.

## Code Conventions & Common Patterns

- **Skill format (agentskills.io)**: `SKILL.md` starts with `---` YAML frontmatter: `name` (kebab-case matching dir, 1–64, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1–1024). Optional: `license`, `compatibility` (≤500), `metadata`, `allowed-tools`, `inputs`/`outputs`, `capabilities`, `dependencies`, `type` (`atomic`/`orchestrator`, default `atomic`).
- **Naming**: skill names/dirs kebab-case; Python modules snake_case; tests `test_*.py`, classes `Test*`, methods `test_*`. Classes PascalCase; functions/vars snake_case; constants UPPER_SNAKE.
- **Adapter pattern**: function-based stateless module in `skills/core/`; thin skill classes wrap adapter calls (`_discover_cli`, etc.). Inputs use `Mapping`/`Sequence`; returns concrete `dict`/`str | None`. Metadata dicts carry `mode`, `interface`, `command`, `exit_code`, `timeout_s`, `reason`, `is_error`.
- **Reason codes**: shared constants `REASON_CLI_NOT_FOUND`, `REASON_MCP_UNAVAILABLE`, `REASON_NEITHER_AVAILABLE`, `REASON_IS_ERROR`.
- **Error handling**: skills return `SkillResult(success=False, error=...)` rather than raising; exceptions caught and stringified. Adapter discovery returns `None`/`[]`; invocation propagates OS/timeout. `standardize_error` builds transport-neutral shape with retryable flag.
- **Async/state**: no async/await anywhere; execution is synchronous. Async jobs simulated via `JobOrchestrator` with polling/wait and idempotency (in-memory). State held in instance dicts; no persistence layer.
- **BaseSkill interface**: inherit `BaseSkill(name, description)`, implement `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`. `SkillResult` defaults `metadata={}`.
- **Composition**: `SkillComposer` sequential (`compose`) or parallel (`compose_parallel`). Sequential threads data (dict passthrough or wrapped as `{'result': ...}`), short-circuits on failure.
- **DAG**: `DAGOrchestrator` manages nodes/dependencies with DFS cycle detection, ready-node resolution, wave execution.
- **Validation-first**: strict naming/description/compatibility; name must match directory.

## Important Files

- `.specify/memory/constitution.md` — governance/principles (v2.0.0)
- `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md`
- `scripts/validate_skill.py`, `scripts/skill_loader.py`, `scripts/register_skills.py`, `scripts/validate_all_skills.py`
- `skills/core/base_skill.py`, `composer.py`, `orchestrator.py`, `utils.py`, `asset_context.py`, `job_orchestrator.py`, `credentials.py`, `artcraft_client.py`, `provider_router.py`, `asset_handler.py`, `cost_estimator.py`, `artcraft_app_client.py`
- `skills/creative/image-generate/skill.py` — reference Python skill
- `specs/001-artcraft-skills-suite/contracts/skill-schema.json`
- `.specify/extensions/.registry`, `.specify/extensions.yml`
- `ROADMAP.md`, `OBJETIVO.md`

## Runtime/Tooling Preferences

- **Runtime**: Python 3. Scripts use only stdlib + PyYAML.
- **Dependencies**: PyYAML required for frontmatter parsing. No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json`, or other package manifests at root.
- **Testing**: `pytest` required; `hypothesis` for property-based tests. Tests assume running from repo root. No lint/format tooling configured (no ruff/black/isort/pre-commit).
- **Tooling**: Spec Kit (bash scripts under `.specify/scripts/bash/`, templates/workflows in `.specify/` and `.omp/`), extensions framework.
- **Constraints**: Skills must be composable and self-contained; follow agentskills.io strictly; validate with `scripts/validate_all_skills.py` before committing. No root build/package system.

## Testing & QA

- **Test layout**: `tests/unit/` (loader/extensions/skills), `tests/integration/` (composition/DAG/workflows/cross-product/generalizable), `tests/contract/` (BaseSkill/interfaces/adapters/contracts), `tests/property/` (Hypothesis invariants/schema/US1-5), `tests/characterization/` (golden master), `tests/_helpers/`, `tests/reference/`, `tests/golden/`. No root `conftest.py`; only `tests/characterization/conftest.py` (adds `--update-golden`).
- **Frameworks**: `pytest` (class/function based), `hypothesis` for property tests.
- **Running**: `pytest` from repo root; filter by layer/path/name. Some tests manipulate `sys.path`. Validation: `python scripts/validate_all_skills.py`, `python scripts/validate_skill.py <skill>`.
- **Patterns**: Contract tests enforce `BaseSkill` interface; integration tests use mocks/helpers; property tests verify schema/invariants (kebab-case, description 1–1024, compatibility ≤500). Characterization/golden-master + differential tests for refactor equivalence. Mocking via `monkeypatch` (subprocess.run, shutil.which, os.path.exists), `unittest.mock`, fake `CompletedProcess`.
- **Quality gates** (Constitution): functionality, documentation, compatibility, composability, performance, security, transparency, error handling. Skills must be independently testable with clear contracts.
- **Current state**: 12 skills validated; test suite covers US1–US5 across all layers. Follow existing patterns and ensure validation/tests pass.