# Repository Guidelines

## Project Overview

ArtCraft Skills Suite is an open-source, composable AI agent skills ecosystem for creative asset creation, manipulation, and development. Following the [agentskills.io](https://agentskills.io) standard, skills provide intentional "build before generating" workflows across 2D/raster, vector/illustration, 3D/spatial, video/motion, audio, documents/presentations, and CAD/technical design.

Governed by `.specify/memory/constitution.md` (v2.0.0), core principles include: crafting over generating, artist-centric design, vendor-neutrality/interoperability, composability/modularity, performance/native execution, quality through intentional craft, transparency/reproducibility/cost awareness, and extensibility without unnecessary complexity.

## Architecture & Data Flow

- **Skill System**: Skills are self-contained packages under `skills/{category}/{skill-name}/` with categories `core/`, `creative/`, `integration/`, `workflow/`. Each requires `SKILL.md` with YAML frontmatter + Markdown body. Skills may include `scripts/`, `references/`, and `assets/`.
- **Discovery/Loading**: `scripts/skill_loader.py` (`SkillLoader`) recursively finds all `SKILL.md` files via `rglob("SKILL.md")`, parses YAML frontmatter via `parse_skill_frontmatter()` (requires `---` delimiters), and loads metadata/content plus flags for presence of `scripts/`, `references/`, `assets/`.
- **Validation**: `scripts/validate_skill.py` enforces agentskills.io rules (kebab-case name `^[a-z0-9]+(-[a-z0-9]+)*$`, 1-64 chars, must match directory; description 1-1024 chars; optional `compatibility` ≤500 chars). `scripts/validate_all_skills.py` validates all skills except those under `template/` or `example-skill/`.
- **Registration**: `scripts/register_skills.py` collects skills via `SkillLoader` and updates `.specify/extensions/.registry` with `registered_skills` entries (`name`, `path`, `description`).
- **Core Abstractions** (`skills/core/`):
  - **`BaseSkill`/`SkillResult`** (`base_skill.py`): `SkillResult` dataclass (`success`, `data`, `error`, `metadata` auto-initialized). `BaseSkill` (ABC) requires `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`; provides `validate_inputs()` (basic dict check) and `get_metadata()`.
  - **`SkillComposer`** (`composer.py`): Registry + sequential/parallel composition. `compose()` threads outputs (dict preserved or wrapped as `{'result': ...}`), short-circuits on failure; `compose_parallel()` executes skills independently.
  - **`DAGOrchestrator`** (`orchestrator.py`): DAG with `DAGNode`/`NodeStatus` (PENDING/RUNNING/COMPLETED/FAILED/SKIPPED), DFS cycle detection, readiness by completed deps, wave execution.
  - **Infrastructure**: `JobOrchestrator` (idempotency/polling/wait), `CredentialManager` (env/in-memory), `OmniApiClient`/`OmniGenClient` (dual auth), `ProviderRouter` (60+ models), `AssetHandler`/`AssetContext`, `CostEstimator`, `utils` (errors/logging/config).
- **Workflow/Specs**: Features tracked under `specs/{NNN}-{name}/` using Spec Kit. Extensions/commands/workflows in `.specify/` and `.omp/`. Current feature: `001-artcraft-skills-suite`. Cross-product/generalizable workflows implemented without project-specific branding.

**Data flow**: Author creates `skills/category/name/SKILL.md` → validated by `validate_skill.py` → discovered/loaded by `SkillLoader` → registered in `.specify/extensions/.registry` → consumed by agents/composers following agentskills.io patterns.

## Key Directories

- `skills/` - Skill packages by category. `core/` contains base abstractions (`base_skill.py`, `composer.py`, `orchestrator.py`, `utils.py`, `asset_context.py`, etc.), `template/`, `example-skill/`. Each skill requires `SKILL.md`.
- `scripts/` - Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py` (stdlib + PyYAML).
- `tests/` - `unit/` (loader/extensions), `integration/` (composition/DAG/workflows/cross-product/generalizable), `contract/` (BaseSkill/interfaces/adapters), `property/` (Hypothesis invariants). No root `conftest.py`.
- `specs/` - Feature specs/plans/tasks/contracts/checklists (Spec Kit). `specs/001-artcraft-skills-suite/` includes contracts, data model, quickstart, research.
- `docs/` - Guides: `skill-authoring.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`.
- `.specify/` - Spec Kit templates, memory (`constitution.md` v2.0.0), workflows, extensions (`.registry`, `extensions.yml`), scripts (`scripts/bash/*.sh`).
- `.omp/` - OMP command definitions/plans/assessments/workflows mirroring Spec Kit structure.
- `ROADMAP.md`, `OBJETIVO.md`, `AGENTS.md` - Project goals and guidelines.

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
pytest tests/unit/test_skill_loader.py -v
pytest -v -x  # verbose, stop on first failure
```

## Code Conventions & Common Patterns

- **Skill Format (agentskills.io)**: `SKILL.md` starts with `---` YAML frontmatter containing `name` (kebab-case matching dir, 1-64, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1-1024). Optional: `license`, `compatibility` (≤500), `metadata` (string map), `allowed-tools`. Body Markdown after frontmatter. Extended schema allows `inputs`/`outputs`, `capabilities`, `dependencies`, `type` (`atomic`/`orchestrator`, default `atomic`).
- **Naming**: Skill names/directories use kebab-case; Python modules use snake_case. Test files `test_*.py`, classes `Test*`, methods `test_*`.
- **Validation-first**: Strict naming/description/compatibility; name must match directory. `validate_all_skills.py` skips `template/` and `example-skill/`. Frontmatter requires exactly 3 parts separated by `---`.
- **BaseSkill Interface**: Inherit from `BaseSkill(name, description)`, implement `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`. `SkillResult` defaults `metadata={}`.
- **Composition**: `SkillComposer` for sequential (`compose`) or parallel (`compose_parallel`). Sequential threads data (dict passthrough or wrapped as `{'result': ...}`), short-circuits on failures.
- **DAG Orchestration**: `DAGOrchestrator` manages nodes/dependencies with DFS cycle detection, ready-node resolution, wave execution.
- **Job/Provider/Assets**: Use `JobOrchestrator` (idempotency/polling), `CredentialManager`, `OmniApiClient`/`OmniGenClient`, `ProviderRouter`, `AssetHandler`/`AssetContext`, `CostEstimator`.
- **Python Style**: Stdlib + PyYAML; simple classes/functions, explicit validation. Add `scripts/` to `sys.path` as needed. Follow existing patterns.
- **Spec Kit Workflow**: Features under `specs/`, extensions/commands/workflows in `.specify/` and `.omp/`.

## Important Files

- `.specify/memory/constitution.md` - Governance/principles (v2.0.0)
- `docs/skill-authoring.md`, `docs/core-abstractions.md`, `docs/cross-product.md`, `docs/generalizable-workflows.md` - Guides
- `scripts/validate_skill.py`, `scripts/skill_loader.py`, `scripts/register_skills.py`, `scripts/validate_all_skills.py` - Core tooling
- `skills/core/base_skill.py`, `composer.py`, `orchestrator.py`, `utils.py`, `asset_context.py`, `job_orchestrator.py`, `credentials.py`, `artcraft_client.py`, `provider_router.py`, `asset_handler.py`, `cost_estimator.py` - Core abstractions
- `skills/core/example-skill/SKILL.md`, `skills/core/template/SKILL.md` - References
- `specs/001-artcraft-skills-suite/contracts/skill-schema.json` - Schema
- `.specify/extensions/.registry`, `.specify/extensions.yml` - Registry/config
- `ROADMAP.md`, `OBJETIVO.md` - Goals/planning

## Runtime/Tooling Preferences

- **Runtime**: Python 3. Scripts use only stdlib + PyYAML.
- **Dependencies**: PyYAML required for frontmatter parsing. No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json`, or other language package manifests at root.
- **Testing**: `pytest` required; `hypothesis` for property-based tests. Tests assume running from repo root.
- **Tooling**: Spec Kit (bash scripts under `.specify/scripts/bash/`, templates/workflows in `.specify/` and `.omp/`), extensions framework.
- **Constraints**: Skills must be composable and self-contained. Follow agentskills.io strictly. Validate with `scripts/validate_all_skills.py` before committing. No root build/package system.

## Testing & QA

- **Test Layout**: `tests/unit/` (loader/extensions), `tests/integration/` (composition/DAG/workflows/cross-product/generalizable), `tests/contract/` (BaseSkill/interfaces/adapters/contracts), `tests/property/` (Hypothesis invariants/schema/US1-5). No `conftest.py`.
- **Frameworks**: `pytest` (class/function based), `hypothesis` for property tests.
- **Running Tests**: `pytest` from repo root. Filter by layer/path/name. Some tests manipulate `sys.path`. Validations: `python scripts/validate_all_skills.py`, `python scripts/validate_skill.py <skill>`.
- **Patterns**: Contract tests enforce `BaseSkill` interface; integration tests use mocks/helpers for composition/DAG/workflows; property tests verify schema/invariants (kebab-case, description 1-1024, compatibility ≤500). TDD-style tests may exist alongside implementation-aligned tests.
- **Quality Gates** (Constitution): Functionality, documentation, compatibility, composability, performance, security, transparency, error handling. Skills must be independently testable with clear contracts.
- **Current State**: 12 skills validated; test suite covers US1-US5 across all layers (follow existing patterns and ensure validation/tests pass).