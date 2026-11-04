# Idea Research: Implement Python creative skills via shared CLI/MCP adapter

- **Slug**: implement-python-creative-skills
- **Created**: 2026-11-04
- **Evidence confidence (overall)**: medium

## Users & Demand

- Skill directory marketplaces (skillsdirectory.com, openagentskill.com) list image-edit and image-remove-background skills with ratings, copies, and view counts — evidence of user demand for agent-consumable creative skills — [source: skillsdirectory.com/skills/twuijri-image-edit, skillsdirectory.com/skills/scenario-labs-scenario-image-editing, openagentskill.com/skills/godot-fun-image-remove-background] (confidence: medium)
- PhotoCraft (ArtCraft) `photocraft-cli` exposes 500+ commands via CLI and MCP server, including `layer.removeBackground` for background removal — demand exists for agent-driven creative tooling over these surfaces — [source: photocraft.im/guides/mcp-cli, photocraft.im/guides/remove-background, artcraftai.org/tutorials/photocraft-cli-mcp] (confidence: high)
- agentskills.io is the de-facto open standard for agent skills (SKILL.md format), with growing ecosystem (agentskills-core PyPI package, Microsoft Agent Framework Python skills, MCP Python SDK skills) — [source: agentskills.io/specification, pypi.org/project/agentskills-core, github.com/microsoft/agent-framework] (confidence: high)

## Prior Art

- veniceai/skills publishes `venice-image-edit/SKILL.md` covering POST /image/edit and /image/upscale — external precedent for image-edit agent skills — [source: github.com/veniceai/skills/blob/main/skills/venice-image-edit/SKILL.md] (confidence: high)
- OpenClip-App/agent-skills provides agent skills for image editing, background removal, thumbnails via CLI and MCP — external precedent combining editing + background removal — [source: github.com/OpenClip-App/agent-skills] (confidence: high)
- awesome-genmedia/skills publishes `image-editing/SKILL.md` for natural-language image editing (inpaint, outpaint, retouch) — external precedent — [source: github.com/awesome-genmedia/skills/blob/main/.agents/skills/image-editing/SKILL.md] (confidence: high)
- openagentskill.com indexes `image-remove-background` using rembg (U2Net / BiRefNet) — external precedent for background removal as a standalone agent skill — [source: openagentskill.com/skills/godot-fun-image-remove-background] (confidence: high)
- Internally, `skills/creative/image-generate/skill.py` already exists as a working Python implementation using the shared adapter — direct in-repo precedent for the exact pattern proposed — [source: skills/creative/image-generate/skill.py] (confidence: high)
- Internally, `skills/creative/{image-edit,background-remove,image-upscale,mesh-generate}/SKILL.md` exist as declarative scaffolds only — no `skill.py` — [source: skills/creative/*/SKILL.md] (confidence: high)

## Market & Context

- agentskills.io specification defines skill directory structure: `SKILL.md` (required) + optional `scripts/`, `references/`, `assets/` — skills can bundle executable code in `scripts/` — [source: agentskills.io/specification, agentskills.io/skill-creation/using-scripts] (confidence: high)
- Multiple agent frameworks (Claude Code, Cursor, Codex, Gemini, OpenCode, VS Code) consume agentskills.io-compatible skills — market for portable, vendor-neutral skills — [source: agentskills.io/home, agentskills.io/client-implementation/adding-skills-support] (confidence: high)
- Cost of doing nothing: the 4 creative skills remain declarative-only; the adapter's reusability promise (SC-005) remains unproven with real consumers; Phase 1 stays at ~25% Python implementation — [assumption] (confidence: medium)

## Data & Constraints

- `photocraft-cli` commands include: `convert`, `info`, `run`, `batch`, `droplet`, `commands`, `mcp`; command IDs like `layer.removeBackground` exist — adapter's `discover_cli_commands` can enumerate them — [source: photocraft.im/guides/mcp-cli, photocraft.im/guides/remove-background] (confidence: high)
- `photocraft-cli` v0.16.0 generates man pages and shell completions — CLI surface is documented and stable enough to build against — [source: photocraft.im/guides/mcp-cli] (confidence: medium)
- PhotoCraft is early alpha (Windows/macOS/Linux/Web self-hosted) — platform limitations exist but CLI/MCP surfaces are the integration contract — [source: artcraftwiki.com/apps/photocraft/] (confidence: medium)
- FR-005 (decision from feature 003): MCP discovery/invocation remain skill-level; adapter provides config/output normalization plus injectable helpers only — constraint on scope — [source: specs/003-shared-cli-mcp-adapter/spec.md FR-005] (confidence: high)

## Evidence Against the Idea

- The 4 skills already function as declarative `SKILL.md` — agents that consume SKILL.md directly may not need Python `skill.py` at all; implementing `skill.py` could be duplicated effort if the skill schema alone is sufficient for agent consumption — [assumption] (confidence: medium)
- `photocraft-cli` is early alpha; commands and behavior may change, requiring skill.py updates — maintenance burden — [source: artcraftwiki.com/apps/photocraft/] (confidence: medium)
- Implementing 4 `skill.py` files (~200 lines each) duplicates the image-generate pattern; without a shared base class, this creates maintenance surface — [assumption] (confidence: medium)
- Alternative 80/20 candidates exist: `/speckit.converge` for feature 001 (verification-only, adds no capability), or creating the 3 missing contract test files (narrow impact) — [source: prior analysis in this session] (confidence: high)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: exact input/output schema for each skill beyond what SKILL.md declares]
- [NEEDS CLARIFICATION: default `command_keywords` for each skill]
- [NEEDS CLARIFICATION: skill-specific params (mask for image-edit, scale for image-upscale, format for mesh-generate)]
- [NEEDS CLARIFICATION: whether to extract a shared base class to avoid duplication]
- [NEEDS CLARIFICATION: whether tests/contract/test_atomic_skills.py should be extended to cover the 4 new skills]

## Sources

- https://agentskills.io/specification (host: agentskills.io, policy: allowlisted)
- https://agentskills.io/skill-creation/best-practices (host: agentskills.io, policy: allowlisted)
- https://agentskills.io/skill-creation/using-scripts (host: agentskills.io, policy: allowlisted)
- https://photocraft.im/guides/mcp-cli (host: photocraft.im, policy: allowlisted)
- https://photocraft.im/guides/remove-background (host: photocraft.im, policy: allowlisted)
- https://artcraftai.org/tutorials/photocraft-cli-mcp (host: artcraftai.org, policy: allowlisted)
- https://github.com/veniceai/skills/blob/main/skills/venice-image-edit/SKILL.md (host: github.com, policy: allowlisted)
- https://github.com/OpenClip-App/agent-skills (host: github.com, policy: allowlisted)
- https://github.com/awesome-genmedia/skills/blob/main/.agents/skills/image-editing/SKILL.md (host: github.com, policy: allowlisted)
- https://openagentskill.com/skills/godot-fun-image-remove-background (host: openagentskill.com, policy: unrecognized — auto-refused: host not on safe list)
- https://www.skillsdirectory.com/skills/twuijri-image-edit (host: skillsdirectory.com, policy: unrecognized — auto-refused: host not on safe list)
- https://pypi.org/project/agentskills-core (host: pypi.org, policy: unrecognized — auto-refused: host not on safe list)
- https://github.com/microsoft/agent-framework (host: github.com, policy: allowlisted)
- specs/003-shared-cli-mcp-adapter/spec.md FR-005 (host: local repo, policy: N/A — local file)
- skills/creative/image-generate/skill.py (host: local repo, policy: N/A — local file)
