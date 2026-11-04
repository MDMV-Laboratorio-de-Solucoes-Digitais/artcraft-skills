# Decision: Implement Python creative skills via shared CLI/MCP adapter

- **Slug**: implement-python-creative-skills
- **Decided**: 2026-11-04
- **Verdict**: go
- **Artifacts reviewed**: intake.md? yes | research.md? yes | problem.md | concept.md?

## Scorecard

| Criterion | Rating | Justification |
|-----------|--------|---------------|
| Problem validity | strong | 4 creative skills exist only as declarative SKILL.md scaffolds with no executable Python skill.py — agents cannot invoke them. Verified in problem.md and confirmed by repo state. |
| Evidence strength | adequate | Research gathered from agentskills.io spec, PhotoCraft CLI/MCP docs, internal repo precedent (image-generate/skill.py works). Some claims marked ASSUMPTION (template fit, keyword matching, skill-specific params). |
| Value vs. cost of inaction | strong | Solving advances Phase 1 ~25%→~80%, proves adapter reusability (SC-005) with real consumers, unblocks US4/US5 and Phases 2–5. Inaction leaves adapter with 1 consumer and 4/5 creative skills unactionable. |
| Feasibility / appetite | strong | Option A (copy/adapt image-generate template) is small (days), template proven working, 4 skills × ~200 lines each. |
| Strategic fit | strong | Aligns with Constitution v2.0.0: composability (IV), crafting over generating (I), extensibility without unnecessary complexity (VIII), vendor-neutral (III). |
| Risk posture | adequate | Risks identified and credibly mitigated: template fit across skill domains (mitigated by image-generate template being generic), keyword matching in 500+ command registry (mitigated by override param), skill-specific params (mitigated by optional params). Skill-specific base class deferred to avoid scope creep. |

## Verdict & Rationale

**Verdict: go** — implement the 4 creative skills' Python `skill.py` files (Option A).

The problem is real (4 skills unactionable), evidence is adequate (template precedent + research), value clearly beats inaction (unblocks downstream capabilities), feasibility is high (small appetite, proven template), strategic fit is strong (constitution-aligned), and risks are understood with mitigations. Evidence strength is `adequate` not `strong` because some claims (template fit across all 4 domains, keyword matching success) are assumption-tagged, but `adequate` clears the bar for `go`.

## If go — Handoff to `/speckit.specify`

- **Problem**: Four creative skills (`image-edit`, `background-remove`, `image-upscale`, `mesh-generate`) exist only as declarative SKILL.md scaffolds with no executable Python implementation; the shared CLI/MCP adapter has only one consumer (`image-generate`), leaving its reusability promise unproven.
- **Chosen approach**: Option A — implement 4 `skill.py` files by copying/adapting the `image-generate/skill.py` template, each reusing the shared adapter (`discover_cli`, `discover_generation_command`, `run_cli_generation`, `normalize_output`, `normalize_mcp_config`, `select_mode`, reason codes) with keyword-based command resolution, timeout invocation, output normalization, and graceful degradation.
- **In scope**: skill.py for image-edit, background-remove, image-upscale, mesh-generate; each validates via `scripts/validate_skill.py`; graceful degradation when CLI/MCP unavailable.
- **Out of scope**: MCP transport in adapter (FR-005), new skill categories (video/audio/CAD/docs), provider backends, refactoring image-generate/skill.py, shared base class (deferred).
- **Success metrics**: 4/4 skills have executable skill.py (baseline 0/4); all 4 validate via `validate_skill.py`; full test suite (278+) continues to pass; feature 001 convergence (97/97 tasks) maintained.
- **Carried-forward open questions**: exact input/output schema per skill beyond SKILL.md; default `command_keywords` per skill; skill-specific params (mask/scale/format); whether to extract a shared base class later; whether tests/contract/test_atomic_skills.py should cover the 4 new skills.
