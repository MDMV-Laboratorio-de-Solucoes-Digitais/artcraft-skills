# Feature Specification: ArtCraft Skills Suite

**Feature Branch**: `001-artcraft-skills-suite`  
**Created**: 2026-11-03  
**Status**: Draft  
**Input**: User description from assessment (go verdict) - extensive suite of composable agent skills for creative asset creation/editing/manipulation/development across ArtCraft products with cross-product integration, initially to serve MDMV needs while remaining general-purpose and open-source

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Foundation & Schema (Priority: P1)

As an AI agent user (Claude Code, Cursor, Codex, Gemini, OpenCode), I need a well-defined, composable skill system following agentskills.io standards so I can discover and use ArtCraft creative capabilities in my agent workflows.

**Why this priority**: Foundation is required before any skills can be built. Must follow ArtCraft Skills Constitution and be compatible across agents.

**Independent Test**: Can define a skill schema, create a template, validate skill structure, and load/discover skills in a compatible agent environment.

**Acceptance Scenarios**:

1. **Given** the skill system is initialized, **When** an agent looks for available skills, **Then** skills are discoverable with proper metadata (name, description, capabilities)
2. **Given** a skill follows the schema, **When** validated, **Then** it passes schema validation
3. **Given** multiple agents, **When** using the same skills, **Then** they work across Claude Code, Cursor, Codex, Gemini, OpenCode

---

### User Story 2 - Core Abstractions & ArtCraft Integration (Priority: P1)

As a skill developer, I need core abstractions (model/provider routing, ArtCraft API adapters, asset handling, job orchestration) so I can build skills that work with ArtCraft's ecosystem without reimplementing common patterns.

**Why this priority**: Enables all skills to integrate properly with ArtCraft's 60+ models, async job system, and credential management.

**Independent Test**: Can create a skill using core abstractions that authenticates, estimates costs, submits a job to ArtCraft API, polls for completion, and retrieves results.

**Acceptance Scenarios**:

1. **Given** ArtCraft credentials configured, **When** a skill uses the provider abstraction, **Then** it can route requests to appropriate providers
2. **Given** a generation request, **When** using job orchestration, **Then** async jobs are properly submitted, polled, and results retrieved
3. **Given** cost estimation needed, **When** using cost abstraction, **Then** costs are estimated before execution with transparency

---

### User Story 3 - Atomic Creative Skills (Priority: P1)

As an artist/creator using an AI agent, I need atomic skills for core creative operations (image generation/editing, background removal, upscaling, 3D operations) that I can compose into workflows.

**Why this priority**: Provides immediate value and demonstrates composability pattern.

**Independent Test**: Can use individual atomic skills independently and compose them together (e.g., generate image → remove background → upscale).

**Acceptance Scenarios**:

1. **Given** an atomic skill, **When** invoked with valid inputs, **Then** it performs the single operation correctly
2. **Given** multiple atomic skills, **When** composed in sequence, **Then** outputs flow correctly between skills
3. **Given** a skill operation, **When** executed, **Then** it follows "build before generating" philosophy where applicable

---

### User Story 4 - Cross-Product Integration Skills (Priority: P2)

As a creator working across multiple ArtCraft apps, I need skills that orchestrate workflows across different asset types and products (e.g., 2D design → 3D texturing → scene composition).

**Why this priority**: Differentiates from single-purpose tools and enables the unified workflow vision.

**Independent Test**: Can execute a cross-product workflow using orchestrator skills that coordinate multiple atomic skills across different domains.

**Acceptance Scenarios**:

1. **Given** assets from different domains, **When** using cross-product skills, **Then** assets flow seamlessly between operations
2. **Given** a multi-step creative workflow, **When** orchestrated by a workflow skill, **Then** all steps execute in proper sequence with state management
3. **Given** ArtCraft apps ecosystem, **When** using integration skills, **Then** they leverage shared asset/context/style layers

---

### User Story 5 - Generalizable MDMV Workflows (Priority: P2)

As a MDMV team member, I need generalizable skills derived from our project needs (evidence packaging, documentation/diagrams, asset workflows) that can be used across projects.

**Why this priority**: Validates the architecture against real needs while keeping skills general-purpose (MDMV guides ROADMAP/OBJETIVOS, not constitution).

**Independent Test**: Can use skills derived from MDMV patterns in non-MDMV contexts, demonstrating generalizability.

**Acceptance Scenarios**:

1. **Given** a generalizable workflow skill, **When** applied to different projects, **Then** it works without MDMV-specific assumptions
2. **Given** MDMV use case needs, **When** designing skills, **Then** they are abstracted to be reusable
3. **Given** documentation/asset needs, **When** using workflow skills, **Then** they produce professional outputs

---

### Edge Cases

- **API unavailable/rate-limited**: skills MUST return `SkillResult(success=False, error=..., metadata={"reason":"provider_unavailable"})` and MUST NOT retry beyond configured retries; callers decide fallback.
- **Non-deterministic results**: generation outputs MUST include `seed` and `model` in metadata when available; golden/characterization tests use tolerance budgets, not exact equality.
- **Missing/invalid credentials**: `CredentialManager` MUST raise `SkillValidationError` before any network call; skills MUST surface a clear error without leaking secrets.
- **Large assets**: asset handler MUST enforce configurable size limits and stream/chunk transfers; oversized inputs MUST fail fast with a clear error.
- **Cross-agent capability gaps**: skills MUST declare required capabilities in `SKILL.md` `allowed-tools`/`capabilities`; loader MUST surface missing capabilities at discovery time.
- **Job failures/timeouts**: `JobOrchestrator` MUST mark job as failed with error detail; skills MUST propagate failure as `SkillResult(success=False)` with timeout metadata.
- **Incompatible skill I/O**: composer MUST validate input/output schema compatibility before execution and fail fast with a clear error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a canonical skill schema following agentskills.io standard (SKILL.md with YAML frontmatter including name, description; optional license, compatibility, metadata, allowed-tools)
- **FR-002**: System MUST support skill discovery and loading compatible with Claude Code, Cursor, Codex, Gemini, OpenCode, and other agentskills.io compatible agents
- **FR-003**: System MUST provide core abstractions for model/provider routing supporting ArtCraft's 60+ model ecosystem
- **FR-004**: System MUST provide ArtCraft API adapters supporting both session auth (/v1/omni_gen/*) and API key auth (/v1/omni_api/*)
- **FR-005**: System MUST handle async job-based generation with submission, polling, webhook support, and result retrieval
- **FR-006**: System MUST provide cost estimation and transparency before executing paid operations; estimates MUST be within ±20% of actual billed cost for supported providers, and MUST include model, token/credit count, and currency in the estimate.
- **FR-007**: System MUST support atomic skills (single responsibility) with clear input/output contracts
- **FR-008**: System MUST support orchestrator/workflow skills for composing atomic skills
- **FR-009**: Skills MUST follow "build before generating" / composition-first philosophy where applicable
- **FR-010**: System MUST support cross-product integration across ArtCraft apps/domains
- **FR-011**: Skills MUST be vendor-neutral and work with multiple providers where appropriate
- **FR-012**: System MUST handle credentials securely across different agent environments
- **FR-013**: Skills MUST provide comprehensive documentation (purpose, usage, parameters, examples, limitations)
- **FR-014**: System MUST be open-source under MIT or Apache-2.0 license
- **FR-015**: Skills MUST be general-purpose and not contain MDMV-specific branding/code (MDMV needs guide ROADMAP/OBJETIVOS only)

### Key Entities *(include if feature involves data)*

- **Skill**: A composable capability with metadata, inputs/outputs schema, implementation, documentation
- **SkillOrchestrator**: Coordinates execution of multiple skills in sequence/parallel with state management
- **ModelProvider**: Abstraction for AI model providers (ArtCraft, Grok, Midjourney, etc.) with routing logic
- **Asset**: Creative asset (image, video, 3D model, audio, document) with metadata and lifecycle
- **Job**: Async generation job with status, progress, results, costs
- **Credential**: Secure authentication/authorization for services and providers

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Skills are discoverable and usable by at least 3 major agent frameworks (Claude Code, Cursor, OpenCode) following agentskills.io standard
- **SC-002**: Core abstractions support all major ArtCraft asset types (images, video, 3D meshes/splats, audio) with proper job orchestration
- **SC-003**: At least 5 atomic skills (image-generate, image-edit, background-remove, image-upscale, mesh-generate) and 2 orchestrator skills (dag-orchestrator, scene-composition) are implemented demonstrating composability
- **SC-004**: Cross-product workflow can be executed combining skills from different domains
- **SC-005**: Skills work with ArtCraft API (both auth modes) including cost estimation and async job handling
- **SC-006**: All skills follow constitution principles and pass quality gates (documentation, composability, security, transparency)
- **SC-007**: At least one generalizable workflow derived from MDMV patterns is implemented and validated as non-MDMV-specific
- **SC-008**: Skill schema and loader mechanism are documented and extensible for community contributions

## Assumptions

- ArtCraft APIs (artcraft-services) remain stable or changes are manageable through adapters
- agentskills.io standard continues to be widely adopted
- Users have access to appropriate model providers/credentials
- Development follows ArtCraft Skills Constitution v2.0.0
- MDMV projects provide concrete validation use cases
- Skills will be consumed by external agents and/or integrated with ArtCraft tools


## Clarifications

### Session 2026-11-03

- Q: What skill schema/loader mechanism should this repo use (adapt agentskills.io to Spec Kit/commands infrastructure)? → A: Follow agentskills.io standard (SKILL.md with YAML frontmatter: name, description required; optional license, compatibility, metadata, allowed-tools). Directory structure per skill with scripts/references/assets. Discovery/registration must integrate with Spec Kit extension system (update .specify/extensions/.registry with registered_skills). Since no loader exists currently, Phase 0 must implement schema definition and registration/discovery mechanism compatible with both agent-loaded and repo-integrated patterns.
- Q: Integration approach with ArtCraft APIs? → A: Abstraction-first with adapters (not direct calls). Core layers: Credential Manager, API Adapters (OmniApiClient for /v1/omni_api/* API key auth, OmniGenClient for /v1/omni_gen/* session auth), Model/Provider Router, Asset/Media Handler, Job Orchestrator (async jobs with idempotency_token, polling/webhooks, timeouts/retries), Cost Estimator. Vendor-neutral where possible while supporting deep ArtCraft integration.
- Q: Which generalizable MDMV workflows to prioritize for validation? → A: P0 - structured-packager (from tirateima_fc evidence/WhatsApp export, generalized to templates+redaction). P1 - policy-redaction middleware, workflow-orchestrator/DAG (from crsdd-fabro patterns), evidence-audit with content-addressing. All must be generalizable with no MDMV branding.
- Q: Testing strategy for non-deterministic operations? → A: Layered approach - contract/schema validation, mocked providers for deterministic tests, fixture-based replay, property-based tests for deterministic components (redaction/formatting), variance budgets for generation quality, trajectory/eval-based testing for workflows. Separate deterministic logic from non-deterministic generation.
- Q: Authentication/credentials across contexts? → A: Centralized Credential Manager supporting both API key (Omni API) and session auth (Omni Gen), secure storage, no logging of secrets, per-agent-environment aware, works with external agents and ArtCraft app contexts.
