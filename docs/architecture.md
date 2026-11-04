# Architecture

High-level structure of the ArtCraft Skills Suite.

## System Overview

```mermaid
flowchart TB
    subgraph Skills["skills/"]
        Core["core/<br/>BaseSkill, SkillResult<br/>SkillComposer, DAGOrchestrator<br/>artcraft_app_client (adapter)<br/>job/credentials/provider routing"]
        Creative["creative/<br/>image-generate (refactored)<br/>image-edit, image-upscale<br/>background-remove, mesh-generate"]
        Integration["integration/<br/>2d-to-3d-workflow<br/>scene-composition"]
        Workflow["workflow/<br/>dag-orchestrator<br/>evidence-audit, orchestrator<br/>policy-redaction, structured-packager"]
    end

    subgraph Scripts["scripts/"]
        V["validate_skill.py<br/>validate_all_skills.py"]
        L["skill_loader.py"]
        R["register_skills.py"]
    end

    subgraph Tests["tests/"]
        U["unit/"]
        I["integration/"]
        C["contract/"]
        P["property/"]
        Ch["characterization/"]
    end

    Core --> Creative
    Core --> Integration
    Core --> Workflow
    Scripts --> Skills
    Tests --> Skills
```

## Adapter Data Flow (003)

```mermaid
flowchart LR
    Skill["Skill (image-generate)<br/>schemas, validation,<br/>param assembly, SkillResult"]
    Adapter["artcraft_app_client<br/>(stateless functions)"]
    CLI["photocraft-cli<br/>(subprocess)"]
    MCP["MCP config/output<br/>(skill-level transport)"]

    Skill -->|"discover_cli<br/>discover_generation_command<br/>run_cli / run_cli_generation<br/>select_mode<br/>standardize_error<br/>normalize_output<br/>normalize_mcp_config"| Adapter
    Adapter --> CLI
    Skill -. "MCP discovery/invocation<br/>(skill-level)" .-> MCP
    Adapter -->|"normalize_mcp_config<br/>normalize_output"| MCP
```

## Skill Execution Lifecycle

```mermaid
sequenceDiagram
    participant Agent
    participant Loader as SkillLoader
    participant Validator as validate_skill
    participant Skill as BaseSkill.execute
    participant Adapter as artcraft_app_client

    Agent->>Loader: discover SKILL.md
    Loader->>Validator: validate (name, desc, compat)
    Validator-->>Loader: ok
    Agent->>Skill: execute(inputs)
    Skill->>Adapter: discover_cli / select_mode / run_cli
    Adapter-->>Skill: result / None
    Skill-->>Agent: SkillResult(success, data, error, metadata)
```

## Key Conventions

- Skills are `SKILL.md` (YAML frontmatter + body) under `skills/{category}/{name}/`.
- Python skills subclass `BaseSkill` and return `SkillResult`.
- Composition via `SkillComposer` (sequential/parallel) and `DAGOrchestrator`.
- Adapter is function-based, stateless; no `ArtcraftAppClient` class.
