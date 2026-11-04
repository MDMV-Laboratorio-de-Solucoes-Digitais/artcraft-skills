# Idea Intake: Implement Python creative skills via shared CLI/MCP adapter

- **Slug**: implement-python-creative-skills
- **Created**: 2026-11-04
- **Source**: pasted text (assistant's 80/20 recommendation from feature 001 convergence review)
- **Type**: new-capability

## Idea (as captured)

> Pesquise longa, completa, profunda, ampla e detalhadamente na internet de forma atualizada em todas as línguas que você tem acesso, garantindo que toda informação seja de alta confiabilidade e utilize todas as suas ferramentas, capacidades e habilidades, utilizando as principais skills relacionadas à cada etapa dessa atividade disponíveis em `npx skills find` (execute as skills que não estiverem instalada global ou localmente utilizando `npx skills use`, sem instalar) para criar as melhores Implement Python creative skills possíveis.
>
> Given the current state, the highest-impact, lowest-effort next step (80/20) is:
>
> Run /speckit.specify for a new feature — specifically Phase 2 of feature 001's roadmap: "Implement Python skills" for image-edit, background-remove, image-upscale, and mesh-generate.
>
> Why this is the 80/20:
> - The shared adapter (artcraft_app_client.py) is already built, tested, and converged (feature 003) — it's the reusable foundation.
> - image-generate already has a working Python skill.py that serves as the exact template to copy/adapt.
> - The 4 other creative skills exist only as declarative SKILL.md scaffolds — implementing their skill.py is ~200 lines each (mostly copying the image-generate pattern with keyword/parameter tweaks), which is low effort.
> - This immediately converts Phase 1 from ~25% to ~80% complete and proves the adapter's reusability promise (SC-005) with real consumers beyond image-generate.
> - It unlocks everything downstream: cross-product workflows (US4), generalizable MDMV workflows (US5), and phases 2–5 (3D, video, audio, docs, CAD).
>
> Alternative 80/20 candidates (lower impact):
> - Run /speckit.converge for feature 001 — but this is verification-only, adds no capability.
> - Create the 3 missing contract test files — low effort but narrow impact; these are subsumed by actually implementing the skills.
>
> Recommended action: Run /speckit.specify to scope a "Implement Python creative skills" feature, then /speckit.plan, /speckit.tasks, and /speckit.implement to build them using the shared adapter and image-generate as the template.

## Restated

Implement executable Python `skill.py` files for the four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) that currently exist only as declarative `SKILL.md` scaffolds, using the shared CLI/MCP adapter (`skills/core/artcraft_app_client.py`) and the existing `image-generate/skill.py` as the template. This proves the adapter's reusability and advances feature 001's Phase 1.

## Origin & Context

- **Raised by**: assistant (automated analysis following feature 001 convergence and feature 003 completion)
- **Trigger**: feature 001 (ArtCraft Skills Suite) fully converged at 97/97 tasks; feature 003 (shared CLI/MCP adapter) converged; the reusable adapter foundation is now ready for real consumers beyond image-generate

## First-Glance Unknowns

- [NEEDS CLARIFICATION: exact input/output schema for each skill beyond what SKILL.md declares]
- [NEEDS CLARIFICATION: which `command_keywords` each skill should default to beyond the SKILL.md hints]
- [NEEDS CLARIFICATION: whether each skill's `_execute_cli` should pass skill-specific params (e.g. `mask` for image-edit, `scale` for image-upscale, `format` for mesh-generate)]
- [NEEDS CLARIFICATION: should a shared base class be extracted to avoid duplication across the 4 skill.py files]
- [NEEDS CLARIFICATION: are there existing tests to extend (tests/contract/test_atomic_skills.py already lists all 5 skills)]
