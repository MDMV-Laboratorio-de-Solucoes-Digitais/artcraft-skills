# Research: ArtCraft Skills Suite

**Feature**: 001-artcraft-skills-suite  
**Date**: 2026-11-03

## Research Summary

All clarifications from spec have been researched and resolved. Key decisions documented below.

## Decisions

### 1. Skill Schema & Loader (agentskills.io + Spec Kit Integration)
**Decision**: Adopt agentskills.io standard (SKILL.md with YAML frontmatter) adapted to integrate with Spec Kit extension system.

**Rationale**:
- agentskills.io is widely adopted by Claude Code, Cursor, Codex, Gemini, OpenCode
- Provides clear schema (name, description required), progressive disclosure, composability
- Can be integrated with existing Spec Kit extension registration (.specify/extensions/.registry)
- No existing loader in repo - need to define and implement in Phase 0

**Alternatives considered**:
- Keep existing command-markdown format only - would limit cross-agent compatibility
- Custom schema from scratch - reinventing wheel, less compatible

### 2. Integration Approach with ArtCraft APIs
**Decision**: Abstraction-first with adapters (not direct API calls)

**Rationale**:
- ArtCraft has complex dual-auth (API key for /v1/omni_api/*, session for /v1/omni_gen/*), async job-based generation
- Need vendor-neutral design with ability to swap providers
- Core abstractions enable composability and testability
- Centralized cost tracking and credential management required by constitution

**Layers**:
- Credential Manager (secure storage, both auth modes)
- API Adapters (OmniApiClient, OmniGenClient)
- Model/Provider Router (60+ models)
- Asset/Media Handler
- Job Orchestrator (idempotency, polling/webhooks, retries/timeouts)
- Cost Estimator

**Alternatives considered**:
- Direct API calls in each skill - would create duplication, hard to maintain, poor composability
- MCP-only - not all functionality may be exposed via MCP

### 3. MDMV Workflow Prioritization
**Decision**: P0 - structured-packager (generalized from tirateima_fc); P1 - policy-redaction, workflow-orchestrator/DAG, evidence-audit (generalized from crsdd-fabro patterns)

**Rationale**:
- Validate core abstractions with real needs
- All generalizable with no MDMV branding
- Cover key capabilities: data transformation, guardrails, orchestration, reproducibility
- Align with ArtCraft philosophy of composition and control

**Alternatives considered**:
- MDMV-specific skills - violates FR-015 and constitution guidance
- Different prioritization - these exercise all core requirements

### 4. Testing Strategy
**Decision**: Layered approach separating deterministic and non-deterministic logic

**Rationale**:
- Non-deterministic generation can't be tested with exact equality
- Need contract validation, mocking, fixtures, property tests for deterministic parts
- Variance budgets and evals for generation quality

**Approach**:
- Contract/schema validation for all skills
- Mocked providers for deterministic unit/integration tests
- Fixture-based replay where possible
- Property-based tests for deterministic components (redaction, formatting, orchestration logic)
- Variance budgets for generation quality
- Trajectory/eval-based testing for workflows
- Separate deterministic logic from non-deterministic generation

### 5. Authentication/Credentials
**Decision**: Centralized Credential Manager supporting both auth modes

**Rationale**:
- ArtCraft requires both API key and session auth
- Must work across different agent environments
- Security critical (no logging of secrets)
- Constitution requires secure handling

**Features**:
- Support API key (Omni API) and session auth (Omni Gen)
- Secure storage per environment
- No secret logging
- Per-agent-environment aware
- Works with external agents and ArtCraft app contexts

## References
- ArtCraft Skills Constitution v2.0.0
- agentskills.io specification
- ArtCraft ecosystem research (storytold/artcraft, artcraft-services)
- MDMV project analysis
- Assessment artifacts (intake/research/problem/concept/decision)
