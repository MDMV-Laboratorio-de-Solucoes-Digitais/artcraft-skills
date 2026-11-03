# Repository Guidelines

## Project Overview

ArtCraft Skills Suite is an open-source ecosystem of composable AI agent skills for creative asset creation, manipulation, and development. Following the [agentskills.io](https://agentskills.io) standard, skills provide intentional "build before generating" workflows across 2D/raster, vector, 3D/spatial, video/motion, audio, documents/presentations, and CAD/technical design. The project uses Spec Kit (`.specify/`) for structured development workflows and governance via `.specify/memory/constitution.md` (v2.0.0). Core principles: crafting over generating, artist-centric design, vendor-neutrality/interoperability, composability/modularity, performance, quality through intentional craft, transparency/reproducibility/cost awareness, and extensibility without unnecessary complexity.

## Architecture & Data Flow

- **Skill System**: Skills are self-contained directories under `skills/{category}/{skill-name}/` with a required `SKILL.md` containing YAML frontmatter + Markdown content. Categories include `core/`, `creative/`, `integration/`, `workflow/`.
- **Discovery/Loading**: `scripts/skill_loader.py` (`SkillLoader`) recursively finds all `SKILL.md` files via `rglob("SKILL.md")`, parses YAML frontmatter (`parse_skill_frontmatter()` accepts content starting with `---`, loads middle as YAML), and loads skill metadata/content plus flags for presence of `scripts/`, `references/`, `assets/`.
- **Validation**: `scripts/validate_skill.py` enforces agentskills.io-style rules (kebab-case name `^[a-z0-9]+(-[a-z0-9]+)*$`, 1-64 chars, must match directory; description 1-1024 chars; optional `compatibility` ≤500 chars). `scripts/validate_all_skills.py` validates all skills except paths containing `template/` or `example-skill`.
- **Registration**: `scripts/register_skills.py` collects skills via `SkillLoader` and updates `.specify/extensions/.registry` with `registered_skills` entries (`name`, `path`, `description`).
- **Core Abstractions**: `skills/core/base_skill.py` defines `BaseSkill` (abstract `get_input_schema()`, `get_output_schema()`, `execute()`, `SkillResult`), `skills/core/composer.py` provides `SkillComposer` for sequential/parallel composition. Shared infrastructure includes credentials, API adapters (ArtCraft/Omni), provider router, asset handler, job orchestrator, cost estimator, DAG orchestrator, etc.
- **Specifications/Workflow**: Features/specs live under `specs/{NNN}-{name}/`. Spec Kit templates/workflows/extensions/commands live in `.specify/` and `.omp/` (extensions registered in `.registry`, commands under `*/commands/`, workflows in `workflows/workflow-registry.json`). Assessments/bugs tracked under `.specify/extensions/` and `.omp/assessments/`.

**Data flow**: Skill author creates `skills/category/name/SKILL.md` → validated by `validate_skill.py` → discovered/loaded by `SkillLoader` → registered via `register_skills.py` into Spec Kit registry (`.specify/extensions/.registry`) → consumed by agents following agentskills.io patterns.

## Key Directories

- `skills/` - Skill packages by category (`core/`, `creative/`, `integration/`, `workflow/`). Each requires `SKILL.md`; may have `scripts/`, `references/`, `assets/`. `core/` includes base abstractions and `example-skill/`/`template/`.
- `scripts/` - Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py`.
- `tests/` - Test suites split into `unit/`, `integration/`, `property/` (pytest; Hypothesis used in property/integration tests).
- `specs/` - Feature specs/plans/tasks/contracts/checklists (Spec Kit artifacts). Current feature `001-artcraft-skills-suite/`.
- `docs/` - Guides like `skill-authoring.md`, `core-abstractions.md`.
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
pytest tests/property/

# Run specific test
pytest tests/unit/test_skill_loader.py -v
```

*(No package manager/build system files at root; tooling is Python scripts + Spec Kit.)*

## Code Conventions & Common Patterns

- **Skill format (agentskills.io)**: `SKILL.md` must start with `---` YAML frontmatter containing `name` (kebab-case, matches dir, 1-64, `^[a-z0-9]+(-[a-z0-9]+)*$`), `description` (1-1024). Optional `license`, `compatibility` (≤500), `metadata` (e.g., `author`, `version`). Body is Markdown after frontmatter.
- **Naming**: Skill names/directories use kebab-case; Python modules follow snake_case. Test files `test_*.py`, classes `Test*`, methods `test_*`.
- **Validation-first**: Name/description/compatibility enforced strictly; name must match directory name. `validate_all_skills.py` skips `template/` and `example-skill/`.
- **Composability**: Skills are self-contained, independently testable building blocks designed to compose into pipelines (per Constitution). Use `BaseSkill`/`SkillResult` and `SkillComposer` for composition; leverage core abstractions for shared concerns.
- **Spec Kit workflow**: Features follow specify/plan/tasks/checklists under `specs/`; extensions/commands/workflows in `.specify/` and `.omp/`.
- **Python style**: Scripts use stdlib + PyYAML; simple classes/functions, explicit validation with clear error messages. Add `scripts/` to `sys.path` as needed. Property-based tests use Hypothesis.

## Important Files

- `.specify/memory/constitution.md` - Project governance/principles (v2.0.0; crafting over generating, composability, vendor-neutrality, quality gates).
- `docs/skill-authoring.md` - Skill structure/requirements/validation guide.
- `docs/core-abstractions.md` - Core abstractions and usage patterns.
- `scripts/validate_skill.py` - Canonical skill validation rules.
- `scripts/skill_loader.py` - Skill discovery/loading logic.
- `scripts/register_skills.py` - Registry registration logic.
- `skills/core/base_skill.py` - Base skill interface and `SkillResult`.
- `skills/core/composer.py` - Skill composition utilities.
- `skills/core/example-skill/SKILL.md` - Reference skill format.
- `skills/core/template/SKILL.md` - Skill template.
- `.specify/extensions/.registry` - Registered skills/extensions.
- `ROADMAP.md` - Project phases and goals.

## Runtime/Tooling Preferences

- **Runtime**: Python 3 for utility scripts. PyYAML required. No Node/Bun/Rust toolchain files at root.
- **Frameworks/Tools**: pytest (with Hypothesis for property tests). Spec Kit for planning/workflows.
- **Standards**: Follow agentskills.io skill format; Spec Kit for structured development. Open source (MIT/Apache-2.0 dual-licensed), vendor-neutral where possible.
- **Constraints**: Skills must be composable and self-contained. No build system/package manager at root.

## Testing & QA

- **Test layout**: `tests/unit/`, `tests/integration/`, `tests/property/` (pytest cache present).
- **Framework**: pytest; property-based testing via Hypothesis. No `conftest.py`/`pytest.ini`/`pyproject.toml` at root (default discovery).
- **Running tests**: `pytest` from repo root; filter by layer/path/name as needed.
- **Validation**: Run `python scripts/validate_all_skills.py` to check skill compliance. Individual skills validated via `python scripts/validate_skill.py`.
- **Quality gates** (from Constitution): functionality, documentation, compatibility, composability, performance, security, transparency, error handling.
- **Expectations**: Skills should be independently testable with clear contracts; follow existing patterns and include comprehensive documentation. Tests may cover not-yet-implemented modules during TDD.
