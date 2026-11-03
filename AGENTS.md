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
  - **`BaseSkill`/`SkillResult`** (`base_skill.py`): `SkillResult` is a dataclass (`success`, `data`, `error`, `metadata` auto-initialized). `BaseSkill` (ABC) requires `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`; provides `validate_inputs()` (basic dict check) and `get_metadata()`.
  - **`SkillComposer`** (`composer.py`): Registers skills by name; `compose()` runs sequentially with input validation, output threading (dict passed through or wrapped as `{'result': ...}`), and short-circuit on failure; `compose_parallel()` executes each registered skill independently.
  - **`DAGOrchestrator`** (`orchestrator.py`): DAG execution with `DAGNode`/`NodeStatus` (PENDING/RUNNING/COMPLETED/FAILED/SKIPPED), dependency tracking, DFS cycle detection, `get_ready_nodes()` for dependency resolution, `execute()` runs ready-node waves.
  - **Utilities** (`utils.py`): `SkillError`/`SkillValidationError`/`SkillExecutionError`, `setup_logging()`, `get_config(key, default)` (reads `ARTCRAFT_SKILLS_{KEY.upper()}`), `ensure_dir()`.
- **Workflow/Specs**: Features tracked under `specs/{NNN}-{name}/` using Spec Kit. Extensions/commands/workflows in `.specify/` and `.omp/` (registry in `.specify/extensions/.registry`). Current feature: `001-artcraft-skills-suite` (converging). Cross-product workflows use shared `AssetContext`; generalizable workflows (Structured Packager, Policy Redaction, DAG Orchestrator, Evidence Audit) are abstracted without project-specific branding.

**Data flow**: Author creates `skills/category/name/SKILL.md` → validated by `validate_skill.py` → discovered/loaded by `SkillLoader` → registered via `register_skills.py` into `.specify/extensions/.registry` → consumed by agents/composers following agentskills.io patterns.

## Key Directories

- `skills/` - Skill packages by category. `core/` contains base abstractions (`base_skill.py`, `composer.py`, `orchestrator.py`, `utils.py`), `template/`, and `example-skill/`. Each skill requires `SKILL.md` (may have `scripts/`, `references/`, `assets/`).
- `scripts/` - Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py`.
- `tests/` - Test suites: `unit/` (loader/extensions), `integration/` (composition/DAG/workflows/cross-product/generalizable), `contract/` (BaseSkill/interface/contracts), `property/` (Hypothesis schema/invariant tests). No `conftest.py` at root; some tests manipulate `sys.path`.
- `specs/` - Feature specs/plans/tasks/contracts/checklists (Spec Kit). `specs/001-artcraft-skills-suite/` includes contracts, data model, quickstart, research.
- `docs/` - Guides: `skill-authoring.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`.
- `.specify/` - Spec Kit templates, memory (`constitution.md` v2.0.0), workflows, extensions (`.registry`, `extensions.yml`), scripts (`scripts/bash/*.sh`).
- `.omp/` - OMP command definitions/plans/assessments/workflows mirroring Spec Kit structure.
- `ROADMAP.md` - Project phases and goals.

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

- **Skill Format (agentskills.io)**: `SKILL.md` must start with `---` YAML frontmatter containing `name` (kebab-case matching dir, 1-64, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1-1024). Optional: `license`, `compatibility` (≤500), `metadata` (string map), `allowed-tools`. Body is Markdown after frontmatter. Extended schema allows `inputs`/`outputs` (JSON Schema refs), `capabilities`, `dependencies`, `type` (`atomic`/`orchestrator`, default `atomic`).
- **Naming**: Skill names/directories use kebab-case; Python modules follow snake_case. Test files `test_*.py`, classes `Test*`, methods `test_*`.
- **Validation-first**: Name/description/compatibility enforced strictly; name must match directory. `validate_all_skills.py` skips `template/` and `example-skill/`. Frontmatter parsing requires exactly 3 parts separated by `---` (see `scripts/skill_loader.py`).
- **BaseSkill Interface**: All skills inherit from `BaseSkill(name, description)`, implement `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`. `SkillResult` dataclass defaults `metadata={}`.
- **Composition**: Use `SkillComposer` for sequential (`compose(skill_sequence, inputs)`) or parallel (`compose_parallel(skill_names, inputs)`) execution. Sequential passes data forward (dict preserved or wrapped as `{'result': ...}`), short-circuiting on failures.
- **DAG Orchestration**: `DAGOrchestrator` manages `DAGNode` objects with dependencies and status enum; validates for cycles (DFS), executes ready nodes in waves.
- **Core Utilities**: `skills/core/utils.py` provides errors, `setup_logging()`, `get_config()` via `ARTCRAFT_SKILLS_*` env vars, `ensure_dir()`.
- **Composability**: Skills are self-contained and independently testable. Use core abstractions for shared concerns (credentials, adapters, routing, job orchestration, cost estimation, asset/context) rather than calling APIs directly.
- **Python Style**: Stdlib + PyYAML; simple classes/functions, explicit validation with clear messages. Add `scripts/`/repo root to `sys.path` as needed. Follow existing patterns.
- **Spec Kit Workflow**: Features under `specs/`, extensions/commands/workflows in `.specify/` and `.omp/`, registry in `.specify/extensions/.registry`.

## Important Files

- `.specify/memory/constitution.md` - Project governance/principles (v2.0.0)
- `docs/skill-authoring.md` - Skill structure/requirements/validation guide
- `docs/core-abstractions.md` - Core abstractions and usage patterns
- `docs/cross-product.md` - Cross-product composition patterns
- `docs/generalizable-workflows.md` - Generalizable workflow patterns
- `scripts/validate_skill.py` - Canonical skill validation rules
- `scripts/skill_loader.py` - Skill discovery/loading logic
- `scripts/register_skills.py` - Registry registration logic
- `skills/core/base_skill.py` - Base skill interface and `SkillResult`
- `skills/core/composer.py` - Skill composition utilities (sequential/parallel)
- `skills/core/orchestrator.py` - DAG orchestration engine
- `skills/core/utils.py` - Common utilities, errors, logging, config
- `skills/core/asset_context.py` - Shared asset/context layer
- `skills/core/example-skill/SKILL.md` - Reference skill format
- `skills/core/template/SKILL.md` - Skill template
- `specs/001-artcraft-skills-suite/contracts/skill-schema.json` - Extended skill schema
- `.specify/extensions/.registry` - Registered skills/extensions
- `.specify/extensions.yml` - Extensions/hooks configuration
- `ROADMAP.md` - Project phases and goals

## Runtime/Tooling Preferences

- **Runtime**: Python 3. Scripts use only stdlib + PyYAML.
- **Dependencies**: PyYAML required for frontmatter parsing. No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json`, or other language package manifests at root.
- **Testing**: `pytest` required; `hypothesis` used for property-based tests. Tests assume running from repo root.
- **Tooling**: Spec Kit for planning/workflows (bash scripts under `.specify/scripts/bash/`, templates/workflows under `.specify/` and `.omp/`). Extensions framework with hooks in `.specify/extensions.yml`.
- **Constraints**: Skills must be composable and self-contained. Follow agentskills.io format strictly. Validate with `scripts/validate_all_skills.py` before committing. No build system/package manager at root - project is script/skills/spec-driven.

## Testing & QA

- **Test Layout**: `tests/unit/` (loader/extensions), `tests/integration/` (composition/DAG/workflows/cross-product/generalizable/US1-5), `tests/contract/` (BaseSkill/interfaces/adapters/contracts), `tests/property/` (Hypothesis invariants/schema/US1-5). No `conftest.py` present.
- **Frameworks**: `pytest` (class/function based), `hypothesis` for property-based tests.
- **Running Tests**: `pytest` from repo root. Filter by layer/path/name as needed. Some tests manipulate `sys.path`. Related validations: `python scripts/validate_all_skills.py`, `python scripts/validate_skill.py <skill>`.
- **Patterns**: Contract tests enforce `BaseSkill` interface; integration tests use mocks/helpers to test composition/DAG/workflows; property tests verify schema/invariants (kebab-case names, description length 1-1024, compatibility ≤500). TDD-style tests exist (some marked RED-phase) alongside implementation-aligned tests.
- **Quality Gates** (from Constitution): Functionality, documentation, compatibility, composability, performance, security, transparency, error handling. Skills should be independently testable with clear contracts.
- **Current State**: 12 skills total (validation status per latest checks may vary); tests cover US1-US5 across all layers. Follow existing patterns and ensure changes pass validation/tests.