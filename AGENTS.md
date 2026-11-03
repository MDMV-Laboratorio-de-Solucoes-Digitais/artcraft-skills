# Repository Guidelines

## Project Overview

ArtCraft Skills Suite is an open-source, composable AI agent skills ecosystem for creative asset creation, manipulation, and development. Following the [agentskills.io](https://agentskills.io) standard, skills provide intentional "build before generating" workflows across 2D/raster, vector/illustration, 3D/spatial, video/motion, audio, documents/presentations, and CAD/technical design. 

Governed by `.specify/memory/constitution.md` (v2.0.0), core principles include: crafting over generating, artist-centric design, vendor-neutrality/interoperability, composability/modularity, performance/native execution, quality through intentional craft, transparency/reproducibility/cost awareness, and extensibility without unnecessary complexity.

## Architecture & Data Flow

- **Skill System**: Skills are self-contained packages under `skills/{category}/{skill-name}/` with categories `core/`, `creative/`, `integration/`, `workflow/`. Each requires `SKILL.md` with YAML frontmatter + Markdown body. Skills may include `scripts/`, `references/`, and `assets/`.
- **Discovery/Loading**: `scripts/skill_loader.py` (`SkillLoader`) recursively finds all `SKILL.md` files via `rglob("SKILL.md")`, parses YAML frontmatter via `parse_skill_frontmatter()` (requires `---` delimiters), and loads metadata/content plus flags for presence of `scripts/`, `references/`, `assets/`.
- **Validation**: `scripts/validate_skill.py` enforces agentskills.io rules (kebab-case name `^[a-z0-9]+(-[a-z0-9]+)*$`, 1-64 chars, must match directory; description 1-1024 chars; optional `compatibility` ≤500 chars). `scripts/validate_all_skills.py` validates all skills except those under `template/` or `example-skill/`.
- **Registration**: `scripts/register_skills.py` collects skills via `SkillLoader` and updates `.specify/extensions/.registry` with `registered_skills` entries (`name`, `path`, `description`).
- **Core Abstractions** (`skills/core/`): `BaseSkill`/`SkillResult` define the skill interface, `SkillComposer` enables sequential/parallel composition, `DAGOrchestrator` executes dependency graphs. Shared infrastructure includes credentials, API adapters (`OmniApiClient` for `/v1/omni_api/*` with API key auth, `OmniGenClient` for `/v1/omni_gen/*` with session auth), provider router (60+ models), asset/media handler, job orchestrator (idempotency/polling/webhooks/retries/timeouts), cost estimator, and asset/context layer.
- **Workflow/Specs**: Features tracked under `specs/{NNN}-{name}/` using Spec Kit. Extensions/commands/workflows live in `.specify/` and `.omp/` (registry in `.specify/extensions/.registry`). Current feature: `001-artcraft-skills-suite`.

**Data flow**: Author creates `skills/category/name/SKILL.md` → validated by `validate_skill.py` → discovered/loaded by `SkillLoader` → registered via `register_skills.py` into `.specify/extensions/.registry` → consumed by agents following agentskills.io patterns.

## Key Directories

- `skills/` - Skill packages by category. `core/` contains base abstractions (`base_skill.py`, `composer.py`, `orchestrator.py`, `utils.py`), `template/`, and `example-skill/`. Each skill requires `SKILL.md`.
- `scripts/` - Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py`.
- `tests/` - Test suites split into `unit/` (skill loader, extensions), `integration/` (composition, DAG orchestration, workflows), `contract/` (BaseSkill interface), `property/` (Hypothesis-based schema invariants).
- `specs/` - Feature specs/plans/tasks/contracts/checklists (Spec Kit artifacts). `specs/001-artcraft-skills-suite/` contains contracts including `contracts/skill-schema.json`.
- `docs/` - Guides: `skill-authoring.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`.
- `.specify/` - Spec Kit templates, memory (constitution), workflows, extensions (registry/assess/bug/github), integrations, scripts.
- `.omp/` - OMP command definitions/plans/assessments/workflows/integrations mirroring Spec Kit structure.
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
```

## Code Conventions & Common Patterns

- **Skill Format (agentskills.io)**: `SKILL.md` must start with `---` YAML frontmatter containing `name` (kebab-case matching dir, 1-64, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1-1024). Optional: `license`, `compatibility` (≤500), `metadata` (string map), `allowed-tools`. Body is Markdown after frontmatter. Extended schema allows `inputs`/`outputs` (JSON Schema refs), `capabilities`, `dependencies`, `type` (`atomic`/`orchestrator`, default `atomic`).
- **Naming**: Skill names/directories use kebab-case; Python modules follow snake_case. Test files `test_*.py`, classes `Test*`, methods `test_*`.
- **Validation-first**: Name/description/compatibility enforced strictly; name must match directory. `validate_all_skills.py` skips `template/` and `example-skill/`. Frontmatter parsing requires exactly 3 parts separated by `---`.
- **BaseSkill Interface** (`skills/core/base_skill.py`): All skills inherit from `BaseSkill(name, description)`, implement `get_input_schema()`, `get_output_schema()`, `execute(inputs) -> SkillResult`. `SkillResult` is a dataclass with `success`, `data`, `error`, `metadata` (defaults to `{}`).
- **Composition**: Use `SkillComposer` for sequential (`compose(skill_sequence, inputs)`) or parallel (`compose_parallel(skill_names, inputs)`) execution. Sequential composition passes data through (`result.data` becomes next inputs if dict, else wrapped as `{'result': ...}`), short-circuiting on failures.
- **DAG Orchestration**: `DAGOrchestrator` manages `DAGNode` objects (with dependencies, status enum PENDING/RUNNING/COMPLETED/FAILED/SKIPPED), validates for cycles, executes ready nodes in loops.
- **Core Utilities**: `skills/core/utils.py` provides `SkillError`/`SkillValidationError`/`SkillExecutionError`, `setup_logging()`, `get_config(key, default)` (reads `ARTCRAFT_SKILLS_{KEY.upper()}` env vars), `ensure_dir()`.
- **Composability**: Skills are self-contained, independently testable building blocks. Use core abstractions for shared concerns (credentials, adapters, routing, job orchestration, cost estimation) rather than calling APIs directly.
- **Python Style**: Stdlib + PyYAML; simple classes/functions, explicit validation with clear error messages. Add `scripts/` to `sys.path` as needed. Follow existing patterns from tests and implementations.
- **Spec Kit Workflow**: Features follow specify/plan/tasks/checklists under `specs/`; extensions/commands/workflows in `.specify/` and `.omp/`.

## Important Files

- `.specify/memory/constitution.md` - Project governance/principles (v2.0.0)
- `docs/skill-authoring.md` - Skill structure/requirements/validation guide
- `docs/core-abstractions.md` - Core abstractions and usage patterns
- `scripts/validate_skill.py` - Canonical skill validation rules
- `scripts/skill_loader.py` - Skill discovery/loading logic
- `scripts/register_skills.py` - Registry registration logic
- `skills/core/base_skill.py` - Base skill interface and `SkillResult`
- `skills/core/composer.py` - Skill composition utilities (sequential/parallel)
- `skills/core/orchestrator.py` - DAG orchestration engine
- `skills/core/utils.py` - Common utilities, errors, logging, config
- `skills/core/example-skill/SKILL.md` - Reference skill format
- `skills/core/template/SKILL.md` - Skill template
- `specs/001-artcraft-skills-suite/contracts/skill-schema.json` - Extended skill schema
- `.specify/extensions/.registry` - Registered skills/extensions
- `ROADMAP.md` - Project phases and goals

## Runtime/Tooling Preferences

- **Runtime**: Python 3. Scripts use only stdlib + PyYAML.
- **Dependencies**: PyYAML required for frontmatter parsing. No `requirements.txt`, `pyproject.toml`, `setup.py`, `setup.cfg` at root.
- **Testing**: `pytest` required. Property-based tests use `Hypothesis`. Tests assume running from repo root.
- **Tooling**: Spec Kit for planning/workflows. No Node/Bun/Rust/build/package manager files at root - project is script-driven.
- **Constraints**: Skills must be composable and self-contained. Follow agentskills.io format strictly. Validate with `scripts/validate_all_skills.py` before committing.

## Testing & QA

- **Test Layout**: `tests/unit/`, `tests/integration/`, `tests/contract/`, `tests/property/` (pytest cache present).
- **Frameworks**: `pytest` (standard assertions, class-based tests). `Hypothesis` for property-based testing in `tests/property/`.
- **Running Tests**: `pytest` from repo root. Filter by layer/path/name as needed (e.g., `pytest tests/unit/ -v`). Some tests manipulate `sys.path` and assume repo root execution.
- **Patterns**: Contract tests enforce `BaseSkill` interface; integration tests use mock skills/classes to test composition/DAG/workflows; property tests verify schema invariants (kebab-case names, description length 1-1024, compatibility ≤500). TDD-style tests may exist for not-yet-implemented modules.
- **Validation**: Run `python scripts/validate_all_skills.py` to check skill compliance. Individual skills: `python scripts/validate_skill.py skills/category/skill-name`.
- **Quality Gates** (from Constitution): Functionality, documentation, compatibility, composability, performance, security, transparency, error handling. Skills should be independently testable with clear contracts and comprehensive documentation.
- **Current State**: 12 skills total (11/12 valid; `workflow/orchestrator` has name/dir mismatch blocking full validation). Feature implementation ~72% complete per ROADMAP.