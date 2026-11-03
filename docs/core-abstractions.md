# Core Abstractions

## Overview
Core abstractions for the ArtCraft Skills Suite provide a unified, vendor-neutral interface to creative capabilities.

## Components

### Credential Manager
Secure credential management supporting API key (Omni API) and session auth (Omni Gen).
- No secret logging
- In-memory secure storage
- Per-environment aware

### API Adapters
- **OmniApiClient**: For `/v1/omni_api/*` endpoints with API key authentication
- **OmniGenClient**: For `/v1/omni_gen/*` endpoints with session authentication

### Model/Provider Router
Routes requests across ArtCraft's 60+ model ecosystem with vendor-neutral abstraction.
Defaults to ArtCraft provider with ability to select others (Grok, Midjourney, Sora, etc.).

### Asset/Media Handler
Manages assets across different formats and providers.

### Job Orchestrator
Handles async job-based generation with:
- Idempotency tokens
- Polling and webhook support
- Timeouts and retries
- Batch job tracking

### Cost Estimator
Provides cost transparency before executing paid operations with estimates in credits and USD.

## Usage
All skills should use these abstractions rather than calling APIs directly for composability and maintainability.
