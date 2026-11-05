# Repository Guidelines

## Project Overview

ArtCraft Skills Suite: an open-source, composable AI agent skills ecosystem following the [agentskills.io](https://agentskills.io) standard. It provides "build before generating" workflows across creative domains (raster, vector, 3D/spatial, video/motion, audio, documents/presentations, CAD/technical design). 

- **Implementation tiers**: Declarative `SKILL.md` skills (YAML frontmatter + Markdown) for most workflow/integration skills; Python `BaseSkill` subclasses for executable skills (e.g., image generation/adapters).
- **Governance**: Guided by `.specify/memory/constitution.md` (v2.0.0). Feature specs/plans/tasks live under `specs/`.
- **Status**: 12 skills validated; no root package/build system.

## Architecture & Data Flow

### Core Abstractions (`skills/core/`)
- **`base_skill.py`**: `SkillResult` (dataclass: `success`, `data`, `error`, `metadata`), `BaseSkill` (ABC) with `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`, `validate_inputs()`, `get_metadata()`.
- **`creative_skill.py`**: `CreativeSkill(BaseSkill)` template for ArtCraft app integration. Implements discover → resolve → invoke → normalize → degrade for CLI/MCP with mode selection (`cli`/`mcp`/`auto`), `threading.BoundedSemaphore(3)`, retry with exponential backoff + jitter (max 3 attempts). Most creative skills inherit from it; `ImageGenerateSkill` is an outlier extending `BaseSkill` directly.
- **`artcraft_app_client.py`**: Stateless CLI/MCP adapter (discovery, command resolution, normalization, mode selection, error standardization). Shared by `CreativeSkill`. Reason codes: `REASON_CLI_NOT_FOUND`, `REASON_MCP_UNAVAILABLE`, `REASON_NEITHER_AVAILABLE`.
- **`composer.py`**: `SkillComposer` for sequential (`compose`) and parallel (`compose_parallel`) chaining. Sequential passes `result.data` forward, wrapping non-dict data as `{'result': ...}` and short-circuiting on failure.
- **`orchestrator.py`**: `DAGOrchestrator` with `DAGNode`/`NodeStatus`, cycle detection (DFS), ready-node resolution, wave execution.
- **Utilities**: `utils.py` (`SkillError`, logging/env/config helpers), `credentials.py` (`CredentialManager`), `artcraft_client.py` (API stubs like `OmniApiClient`/`OmniGenClient`), `provider_router.py`, `asset_handler.py`, `cost_estimator.py`, `job_orchestrator.py`.

### Data Flow
1. Author `skills/{category}/{name}/SKILL.md` (YAML frontmatter) or Python skill in `skill.py`.
2. Validate via `scripts/validate_skill.py` / `scripts/validate_all_skills.py` (agentskills.io rules).
3. Discover/load via `scripts/skill_loader.py` (`SkillLoader`).
4. Register via `scripts/register_skills.py` → `.specify/extensions/.registry`.
5. Execute via `BaseSkill.execute()`; creative skills go through `CreativeSkill` → `artcraft_app_client` (CLI/MCP) with normalization to `SkillResult`.

### Inheritance Patterns
- **Template method**: `CreativeSkill` provides orchestration; subclasses override `get_input_schema()`, `get_output_schema()`, `validate_inputs()`, set `command_keywords`, optionally override MCP hooks/param building.
- **Two styles**: Most creative skills extend `CreativeSkill` (thin). `skills/creative/image-generate/skill.py` extends `BaseSkill` directly with its own flow.
- **Composition/DAG**: `SkillComposer` and `DAGOrchestrator` enable multi-skill workflows.

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `skills/` | Skill packages by category (`core/`, `creative/`, `integration/`, `workflow/`). Each skill may have `SKILL.md`, `skill.py`, `scripts/`, `references/`, `assets/`. |
| `skills/core/` | Base abstractions, orchestrators, composers, adapters, utilities. |
| `skills/creative/` | Creative skills inheriting from `CreativeSkill` or `BaseSkill` (e.g., `image-generate/`, `image-edit/`, `background-remove/`, `image-upscale/`, `mesh-generate/`). |
| `scripts/` | Tooling: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py`, `check_vendor_neutrality.py`. Stdlib + PyYAML. |
| `tests/` | Layered tests: `unit/`, `integration/`, `contract/`, `property/`, `characterization/`, `_helpers/`, `reference/`, `golden/`. No root `conftest.py` (only `tests/characterization/conftest.py`). |
| `specs/` | Feature specs/plans/tasks/contracts/checklists (Spec Kit). |
| `docs/` | Guides: `skill-authoring.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`, `architecture.md`. |
| `.specify/` | Spec Kit templates, `memory/constitution.md` (v2.0.0), workflows, extensions, scripts. |
| `.omp/` | OMP command definitions mirroring Spec Kit. |

## Development Commands

```bash
# Validate skills (agentskills.io)
python scripts/validate_skill.py skills/category/skill-name
python scripts/validate_all_skills.py

# Discover/load/register
python scripts/skill_loader.py
python scripts/register_skills.py

# Run tests (from repo root)
pytest
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/
pytest tests/property/
pytest tests/characterization/
pytest -v -x
pytest tests/unit/test_image_generate.py -v
```

**Notes**: Run from repo root. No build/package manager/lint/format tools configured. Dependencies assumed installed (`PyYAML`, `pytest`, `hypothesis`). Tests use `--import-mode=importlib` and often set `sys.path` manually.

## Code Conventions & Common Patterns

### Naming & Style
- **Skills**: Directories/names kebab-case matching `SKILL.md` `name` (`^[a-z0-9]+(-[a-z0-9]+)*$`), 1–64 chars. Description 1–1024 chars, optional `compatibility` ≤500.
- **Python**: Modules/files snake_case, classes PascalCase (`BaseSkill`, `SkillResult`, `CreativeSkill`), functions/variables snake_case, constants UPPER_SNAKE.
- **Tests**: `test_*.py`, classes `Test*`, methods `test_*`.

### Skill Structure
- **SKILL.md** frontmatter: `---` delimited YAML with required `name`, `description`. Optional: `license`, `compatibility`, `metadata`, `allowed-tools`, `inputs`/`outputs`, `capabilities`, `dependencies`, `type` (`atomic`/`orchestrator`, default `atomic`).
- **Python skills**: Inherit from `BaseSkill` or `CreativeSkill`. Implement `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`. Return `SkillResult` (never raise for expected failures); catch exceptions and stringify.

### Patterns
- **Result objects**: All operations return `SkillResult(success=bool, data=Any, error=str|None, metadata=dict)`. Metadata often includes `mode`, `interface`, `command`, `exit_code`, `timeout_s`, `reason`, `is_error`.
- **Adapter pattern**: `artcraft_app_client` centralizes transport; `CreativeSkill` delegates discovery/normalization/mode selection there. Skills remain thin.
- **Keyword-driven discovery**: CLI/MCP commands resolved via keywords/overrides passed through `artcraft_app_client`.
- **Composition**: `SkillComposer.compose()` threads dict data (non-dict wrapped as `{'result': ...}`), short-circuits on failure. `compose_parallel()` runs independent skills.
- **DAG orchestration**: `DAGOrchestrator` manages dependencies with cycle detection and wave execution.
- **Validation-first**: Strict agentskills.io validation; input validation returns structured errors.
- **Resilience**: `CreativeSkill` uses `BoundedSemaphore(3)`, retries up to 3 times with exponential backoff + jitter on transient failures (timeouts/non-zero exits), preserving metadata on final failure.
- **Error standardization**: Reason codes and consistent `SkillResult` shapes across CLI/MCP paths.
- **No async/await**: Synchronous execution throughout core.

### Dependency Injection / State
- Skills instantiated directly; configuration via inputs/env helpers (`utils.get_config`). Credentials via `CredentialManager`. No global DI container; dependencies passed explicitly.

## Important Files

| File | Purpose |
|------|---------|
| `skills/core/base_skill.py` | `SkillResult` and `BaseSkill` contract. |
| `skills/core/creative_skill.py` | Shared CreativeSkill base with CLI/MCP orchestration, retries, semaphore. |
| `skills/core/artcraft_app_client.py` | Shared CLI/MCP adapter (discovery/normalization/mode selection). |
| `skills/core/composer.py` | `SkillComposer` for sequential/parallel chaining. |
| `skills/core/orchestrator.py` | `DAGOrchestrator` for dependency-aware workflows. |
| `skills/creative/image-generate/skill.py` | Reference Python skill (extends `BaseSkill` directly). |
| `scripts/validate_skill.py`, `scripts/validate_all_skills.py` | Skill validation against agentskills.io rules. |
| `scripts/skill_loader.py`, `scripts/register_skills.py` | Discovery/loading/registration. |
| `pytest.ini` | Pytest config (`--import-mode=importlib`, `testpaths=tests`). |
| `.specify/memory/constitution.md` | Governance (v2.0.0). |
| `specs/001-artcraft-skills-suite/contracts/skill-schema.json` | Skill schema contract. |

## Runtime/Tooling Preferences

- **Runtime**: Python 3 (scripts use stdlib only where possible).
- **Dependencies**: `PyYAML` required for frontmatter parsing. `pytest` and `hypothesis` for testing. No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json` at root.
- **Package manager**: None configured.
- **Build/Lint/Format**: No build step, no lint/format tooling configured (no ruff/black/isort/pre-commit).
- **Tooling**: Spec Kit (`.specify/`, `.omp/`), agentskills.io validation enforced.

## Testing & QA

### Structure
- `tests/unit/` - Isolated unit tests (adapters, utilities, core primitives). Heavy mocking of `subprocess`, `shutil`, filesystem.
- `tests/integration/` - Cross-component workflows (composition, DAG/orchestration, cross-product). Tests `SkillComposer`/orchestrators with mock skills.
- `tests/contract/` - Interface/schema contracts (`BaseSkill`, `SkillResult`, adapters, workflows).
- `tests/property/` - Hypothesis property tests enforcing invariants (determinism, immutability of inputs, mode validation, composition behavior).
- `tests/characterization/` - Golden-master/differential tests. Uses `tests/golden/*` fixtures and `tests/_helpers/canonicalize.py` to strip non-determinism; supports `--update-golden` via `tests/characterization/conftest.py`.
- `tests/_helpers/`, `tests/reference/` - Shared utilities and reference implementations for differential testing.

### Running Tests
```bash
pytest                    # All tests
pytest -v                 # Verbose
pytest -x                 # Stop on first failure
pytest tests/unit/        # By layer
pytest tests/property/    # Property tests
pytest tests/characterization/  # Golden tests
pytest --update-golden    # Regenerate golden masters (if needed)
```

### Patterns & Expectations
- **Canonicalization**: Use `tests/_helpers/canonicalize.canonicalize_skill_result()` to normalize volatile metadata (`duration_ms`, `timeout_s`) for stable comparisons.
- **Mock-first**: CLI/MCP paths faked via monkeypatch (`subprocess.run`, discovery functions) for deterministic tests.
- **TDD-friendly**: Some tests marked RED-phase; resilience/composition features have dedicated property + characterization tests.
- **Traceability**: Tests often map to specs/US1-5.
- **Quality gates** (per constitution): Functionality, documentation, compatibility, composability, performance, security, transparency, error handling. Skills must be independently testable with clear contracts.
- **Current state**: All tests pass (357 passed as of recent runs). Validate with `python scripts/validate_all_skills.py` before committing.
