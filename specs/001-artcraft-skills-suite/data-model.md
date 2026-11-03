# Data Model: ArtCraft Skills Suite

**Feature**: 001-artcraft-skills-suite  
**Date**: 2026-11-03

## Core Entities

### Skill
Represents a composable capability following agentskills.io standard.

**Fields**:
- `name` (string, required): Kebab-case identifier, matches directory name
- `description` (string, required): What it does and when to use it (1-1024 chars)
- `license` (string, optional): License identifier or file reference
- `compatibility` (string, optional): Environment requirements (1-500 chars)
- `metadata` (map[string]string, optional): Additional metadata
- `allowed_tools` (string[], optional): Pre-approved tools
- `inputs` (Schema, required): Input schema (JSON Schema)
- `outputs` (Schema, required): Output schema (JSON Schema)
- `capabilities` (string[], optional): Capability tags
- `dependencies` (string[], optional): Other skills this depends on
- `implementation_path` (path, required): Path to SKILL.md or implementation
- `type` (enum: atomic|orchestrator, required): Skill type

**Relationships**:
- Has many: SkillInputs, SkillOutputs
- May depend on: Skill[]
- Used by: SkillOrchestrator

### SkillOrchestrator
Coordinates execution of multiple skills.

**Fields**:
- `name` (string, required): Orchestrator identifier
- `workflow` (WorkflowDefinition, required): DAG or sequence definition
- `state_manager` (StateManager, required): State handling
- `error_handler` (ErrorHandler, required): Error handling strategy

**Relationships**:
- Composes: Skill[]
- Manages: WorkflowExecution

### ModelProvider
Abstraction for AI model providers.

**Fields**:
- `id` (string, required): Provider identifier
- `name` (string, required): Display name
- `base_url` (string, required): API base URL
- `auth_type` (enum: api_key|session|oauth, required): Authentication type
- `models` (Model[], required): Available models
- `capabilities` (string[], required): Supported capabilities
- `rate_limits` (RateLimit, optional): Rate limiting info
- `cost_info` (CostInfo, optional): Pricing information

**Relationships**:
- Provides: Model[]
- Used by: JobOrchestrator

### Model
Individual AI model.

**Fields**:
- `id` (string, required): Model identifier
- `provider_id` (string, required): Parent provider
- `name` (string, required): Display name
- `capabilities` (string[], required): Supported operations (image, video, 3D, audio, etc.)
- `cost_per_unit` (CostPerUnit, optional): Pricing
- `limits` (ModelLimits, optional): Usage limits

### Asset
Creative asset with metadata.

**Fields**:
- `id` (string, required): Asset identifier
- `type` (enum: image|video|3d_mesh|3d_splat|audio|document|other, required): Asset type
- `format` (string, required): File format
- `url` (string, optional): CDN/storage URL
- `media_token` (string, optional): ArtCraft media token
- `metadata` (map, required): Asset metadata
- `created_at` (timestamp, required): Creation time
- `source_skill` (string, optional): Skill that created it

**Relationships**:
- Used by: Skill inputs/outputs
- Referenced by: Job

### Job
Async generation job.

**Fields**:
- `id` (string, required): Job identifier
- `token` (string, required): Inference job token
- `all_tokens` (string[], optional): Batch job tokens
- `status` (enum: pending|processing|completed|failed|cancelled, required): Job status
- `provider_id` (string, required): Provider used
- `model_id` (string, required): Model used
- `skill_name` (string, required): Skill that created job
- `inputs` (map, required): Job inputs
- `outputs` (Asset[], optional): Result assets
- `cost` (Cost, optional): Actual cost
- `error` (Error, optional): Error details
- `created_at` (timestamp, required): Creation time
- `updated_at` (timestamp, required): Last update
- `idempotency_token` (string, required): Idempotency key

**Relationships**:
- Belongs to: Skill
- Produces: Asset[]
- Uses: ModelProvider, Model

### Credential
Authentication credentials.

**Fields**:
- `id` (string, required): Credential identifier
- `type` (enum: api_key|session, required): Credential type
- `provider_id` (string, optional): Specific provider or "artcraft"
- `auth_mode` (enum: api_key|session, required): Auth mode for ArtCraft
- `encrypted_value` (string, required): Encrypted credential
- `expires_at` (timestamp, optional): Expiration
- `scopes` (string[], optional): Permission scopes

**Validation**:
- Never logged or exposed in plaintext
- Encrypted at rest
- Rotatable

## State Transitions

### Job Status
```
pending -> processing -> completed
                      -> failed
pending -> cancelled
processing -> cancelled
```

## Validation Rules
- Skill name must match agentskills.io pattern (kebab-case)
- Description required and 1-1024 chars
- Job must have idempotency_token
- Credentials must never be in logs
- Assets must have valid type and format
- Cost estimates required before paid operations
