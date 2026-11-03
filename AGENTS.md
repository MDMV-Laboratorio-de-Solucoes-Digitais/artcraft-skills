# Repository Guidelines

## Project Overview
ArtCraft Skills Suite is an open-source ecosystem of composable AI agent skills for creative asset creation, manipulation, and development. Following the [agentskills.io](https://agentskills.io) standard, skills provide intentional "build before generating" workflows across 2D/raster, vector, 3D/spatial, video/motion, audio, documents/presentations, and CAD/technical design. The project uses Spec Kit (`.specify/`) for structured development workflows and governance via `.specify/memory/constitution.md` (v2.0.0).

## Architecture & Data Flow
- **Skill System**: Skills are self-contained directories under `skills/{category}/{skill-name}/` with a required `SKILL.md` containing YAML frontmatter + Markdown content. Categories include `core/`, `creative/`, `workflow/` (see existing skills).
- **Discovery/Loading**: `scripts/skill_loader.py` (`SkillLoader`) recursively finds all `SKILL.md` files via `rglob("SKILL.md")`, parses YAML frontmatter, and loads skill metadata/content plus optional subdirs (`scripts/`, `references/`, `assets/`).
- **Validation**: `scripts/validate_skill.py` enforces agentskills.io-style rules (kebab-case name 1-64 chars matching directory, description 1-1024 chars, optional compatibility ≤500 chars). `scripts/validate_all_skills.py` validates all non-template/example skills.
- **Registration**: `scripts/register_skills.py` collects skills via `SkillLoader` and updates `.specify/extensions/.registry` with `registered_skills` entries (name, path, description).
- **Specifications/Workflow**: Features/specs live under `specs/{NNN}-{name}/` (spec, plan, research, data-model, contracts, checklists, tasks). Spec Kit commands/templates/extensions in `.specify/` and `.omp/commands/`. Assessments/bugs tracked under `.specify/assessments/`, `.specify/extensions/`.

**Data flow**: Skill author creates `skills/category/name/SKILL.md` → validated by `validate_skill.py` → discovered/loaded by `SkillLoader` → registered via `register_skills.py` into Spec Kit registry → consumed by agents following agentskills.io patterns.

## Key Directories
- `skills/` - Skill packages by category (`core/`, `creative/`, `workflow/`). Each requires `SKILL.md`; may have `scripts/`, `references/`, `assets/`.
- `scripts/` - Python utilities: `validate_skill.py`, `validate_all_skills.py`, `skill_loader.py`, `register_skills.py`.
- `tests/` - Test suites split into `unit/`, `integration/`, `property/`.
- `specs/` - Feature specs/plans/tasks/contracts/checklists (Spec Kit artifacts).
- `docs/` - Guides like `skill-authoring.md`, `core-abstractions.md`.
- `.specify/` - Spec Kit templates, memory (constitution), workflows, extensions, integrations, registry.
- `.omp/` - OMP command definitions for Speckit workflows.

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
```
*(No package manager/build system files like package.json/pyproject.toml/Cargo.toml visible at root; tooling is Python scripts + Spec Kit.)*

## Code Conventions & Common Patterns
- **Skill format (agentskills.io)**: `SKILL.md` must start with `---` YAML frontmatter containing `name` (kebab-case, matches dir, 1-64), `description` (1-1024). Optional `license`, `compatibility` (≤500), `metadata` (e.g. `author`, `version`). Body is Markdown with Purpose/Usage/Inputs/Outputs etc.
- **Naming**: Skill names/directories use kebab-case (`example-skill`, `image-generate`); Python modules follow snake_case.
- **Validation-first**: Name/description/compatibility enforced strictly; name must match directory name.
- **Composability**: Skills are self-contained, independently testable building blocks designed to compose into pipelines (per Constitution).
- **Spec Kit workflow**: Features follow specify/plan/tasks/checklists under `specs/`; extensions and assessments under `.specify/`.
- **Python style**: Scripts use stdlib + PyYAML; simple classes/functions, explicit validation with error messages.

## Important Files
- `.specify/memory/constitution.md` - Project governance/principles (crafting over generating, composability, vendor-neutrality).
- `docs/skill-authoring.md` - Skill structure/requirements/validation guide.
- `scripts/validate_skill.py` - Canonical skill validation rules.
- `scripts/skill_loader.py` - Skill discovery/loading logic.
- `skills/core/example-skill/SKILL.md` - Reference skill format.
- `skills/core/template/SKILL.md` - Skill template.
- `ROADMAP.md` - Project phases and goals.

## Runtime/Tooling Preferences
- **Runtime**: Python 3 for utility scripts (PyYAML required). No Node/Bun/Rust toolchain files at root.
- **Standards**: Follow agentskills.io skill format; Spec Kit for planning/workflows.
- **Constraints**: Vendor-neutral where possible; skills must be composable and self-contained.

## Testing & QA
- **Test layout**: `tests/unit/`, `tests/integration/`, `tests/property/` (pytest cache present).
- **Validation**: Run `validate_all_skills.py` to check skill compliance. Individual skills validated via `validate_skill.py`.
- **Quality gates** (from Constitution): functionality, documentation, compatibility, composability, performance, security, transparency, error handling.
- **Expectations**: Skills should be independently testable with clear contracts; follow existing patterns and include comprehensive documentation.
