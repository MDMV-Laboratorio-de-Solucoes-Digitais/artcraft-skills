# ArtCraft Skills Constitution

**Version**: 2.0.0 | **Ratified**: 2026-11-03 | **Last Amended**: 2026-11-03

## Preamble

ArtCraft Skills is an open-source ecosystem of composable AI agent skills for creative asset creation, manipulation, development, and elaboration. We exist to empower artists, designers, filmmakers, and creators by providing tools that enhance intentional crafting rather than replacing artistic judgment. Our mission is to turn prompting into crafting - enabling precise, repeatable, and expressive creative control across the entire asset pipeline.

This Constitution establishes the principles, standards, and governance that guide all development within the ArtCraft Skills project.

## Core Principles

### I. Crafting Over Generating
All skills MUST be designed with the philosophy of "build before generating". We prioritize composition, staging, and intentional construction over one-shot generation. Skills MUST provide artists with control over placement, structure, relationships, and context before invoking generative models. The goal is to mold and direct like clay, not merely describe.

### II. Artist-Centric Design
All skills MUST be designed from the perspective of working artists. Tools MUST prioritize creative control, precision, flexibility, and expressiveness over blind automation. Skills SHOULD feel like natural extensions of an artist's workflow, respecting established creative practices while augmenting them with AI capabilities. Artistic judgment MUST remain in the artist's hands.

### III. Open Source, Vendor-Neutral, and Interoperable
ArtCraft Skills MUST remain open source under a permissive license (MIT or Apache-2.0, dual-licensed). Skills MUST be vendor-neutral where possible, working across diverse AI models, providers, and creative tools. We embrace interoperability with the broader creative ecosystem while maintaining seamless integration with the ArtCraft suite of applications. Users MUST retain freedom of choice in models, providers, and workflows.

### IV. Composability and Modularity
Every skill MUST be self-contained, independently testable, and composable with others. Skills MUST follow clear contracts with well-defined inputs, outputs, and capabilities. Complex creative workflows MUST be built by composing simple, focused skills rather than creating monolithic solutions. Skills SHOULD be designed to work together in pipelines, chains, and orchestration patterns.

### V. Performance and Native Execution
Skills MUST respect the creative workflow's need for responsiveness and control. Leveraging efficient processing, skills SHOULD minimize unnecessary latency and work well in both local and cloud environments. Resource-intensive operations MUST provide clear feedback, respect system constraints, and offer users control over quality/speed/cost tradeoffs. Where applicable, skills SHOULD favor efficient implementations that align with native, performant creative tooling.

### VI. Quality Through Intentional Craft
We MUST maintain high standards for creative output quality. Skills MUST preserve artistic intent, support iteration, and enable precise control at every stage. Generations MUST be guided, editable, refinable, and composable. Artists MUST be able to adjust, mix assets, iterate progressively, and achieve repeatable results. Quality comes from control and intentionality, not just model capability.

### VII. Transparency, Reproducibility, and Cost Awareness
Skills MUST be transparent in their behavior. When using AI models, skills SHOULD make model choices, parameters, operations, and costs clear to users. Workflows MUST support reproducibility where feasible, enabling artists to reliably iterate on their creations. Skills SHOULD provide visibility into resource usage, credit consumption, and provider selection, empowering informed decision-making.

### VIII. Extensibility Without Unnecessary Complexity
The skill system MUST remain simple to understand, discover, and extend. New skills SHOULD follow established patterns without requiring deep knowledge of the entire system. We prioritize clarity, discoverability, and good documentation over premature abstraction. Simplicity and architectural coherence MUST be balanced thoughtfully.

## Creative Asset Standards

### Asset Type Coverage
ArtCraft Skills MUST support comprehensive creative asset workflows across all major media types:

- **2D & Raster**: Image generation, editing, compositing, inpainting, outpainting, upscaling, enhancement, background removal/matting, and manipulation
- **Vector & Illustration**: Vector creation, path manipulation, typography, scalable graphics, and illustration assistance
- **3D & Spatial**: 3D modeling, texturing (PBR), scene composition, camera control, object placement, kitbashing, image-to-3D, and spatial workflows
- **Video & Motion**: Video generation (text/image-to-video), animation, editing, motion graphics, storyboarding, and temporal composition
- **Audio**: Music generation, sound design, SFX, voice/dialogue synthesis, and audio manipulation
- **Documents & Presentations**: Layout design, slides, documents, technical illustration, diagrams, and communication-focused design
- **CAD & Technical Design**: Precision drafting, dimensioning, technical drawing, parametric design assistance, BOM/specification workflows, and manufacturing preparation

### Creative Control Principles

- **Composition First**: Skills MUST enable scene composition and spatial control before generation where applicable. Building the structure, relationships, and layout is fundamental to the crafting workflow.
- **Multi-Modal Workflows**: Skills MUST support mixing different asset types (images, 3D models, cutouts, layers, audio, video) in unified, composable workflows.
- **Iterative Refinement**: Every creative operation MUST support progressive iteration. Skills SHOULD enable refinement over multiple passes rather than forcing one-shot perfection.
- **Asset Reusability**: Skills SHOULD promote reusable assets, components, styles, templates, and presets that can be composed across projects and workflows.
- **Non-Destructive Operations**: Where technically feasible, skills MUST preserve original assets and support non-destructive editing. Artists MUST be able to experiment without fear of losing their work.
- **Mixed Asset Crafting**: Skills SHOULD facilitate combining disparate elements (2D cutouts, 3D meshes, environments, characters) into cohesive compositions with proper depth, lighting, and spatial coherence.

### Quality Assurance
- **Format Fidelity**: Skills MUST respect and preserve asset quality, resolution, color space, and format-appropriate characteristics.
- **Artistic Integrity**: Skills MUST not impose unwanted styles, biases, or aesthetic homogenization. They should serve the artist's creative vision and adapt to diverse artistic preferences.
- **Precise Control**: Skills MUST provide granular control over relevant parameters (composition, camera, pose, lighting, style, etc.) appropriate to the creative task.
- **Graceful Handling**: Skills MUST handle edge cases, failures, and limitations transparently with actionable guidance.

## Skill Architecture

### Skill Structure
Every skill MUST follow a consistent, predictable structure:

- **Clear Purpose**: Each skill MUST have a well-defined, singular purpose documented in its metadata. Skills should solve focused problems that can be composed into larger workflows.
- **Standardized Interface**: Skills MUST use consistent input/output schemas, follow established naming conventions, and provide predictable behavior.
- **Comprehensive Documentation**: Every skill MUST include thorough documentation covering purpose, usage, parameters, inputs/outputs, examples, limitations, and guidance on when to use (and when not to use) the skill.
- **Discoverability**: Skills MUST be properly categorized, tagged, and described for easy discovery through skill browsing, search, and composition tools.
- **Self-Contained Testing**: Skills MUST be independently testable with clear contracts and minimal external dependencies where possible.

### Model and Provider Abstraction
- **Provider Agnostic**: Skills MUST abstract over AI model providers where appropriate, allowing users to choose models that fit their needs, budget, quality requirements, and preferences.
- **Model Catalog Awareness**: Skills SHOULD be aware of and compatible with the diverse ecosystem of models, understanding their capabilities, strengths, limitations, and appropriate use cases.
- **Graceful Degradation**: Skills MUST handle provider failures, rate limits, API changes, and unavailable models gracefully with clear, actionable error messages.
- **Cost Transparency**: When dealing with paid APIs or metered services, skills SHOULD provide transparency about resource usage, estimated costs, and credit consumption where feasible.
- **Multi-Provider Support**: Skills SHOULD enable switching between providers/models without requiring workflow rewrites, supporting user choice and resilience.

### Integration Standards
- **Ecosystem Integration**: Skills SHOULD integrate seamlessly with ArtCraft applications and shared data formats, enabling fluid workflows across the ArtCraft suite (ArtCraft, DrawCraft, TextureCraft, CADCraft, DeckCraft, and related tools).
- **Agent Compatibility**: Skills MUST be compatible with AI coding assistants and agents that support the skills system (Claude Code, Cursor, Codex, Gemini, OpenCode, and others), following established skills ecosystem patterns.
- **Standards Compliance**: Skills MUST follow established patterns from the skills ecosystem while appropriately extending them for creative workflows.
- **Data Format Interoperability**: Skills SHOULD work with common creative asset formats and be mindful of interoperability with industry-standard tools where practical.
- **Tool Orchestration**: Skills MUST be designed to work within orchestration systems, supporting composition, chaining, conditional execution, and pipeline workflows.

## Development Workflow

### Skill Development Process
1. **Research First**: Before creating a skill, developers MUST research existing solutions, user needs, creative workflows, and relevant patterns in the ArtCraft ecosystem.
2. **Design for Composition**: Skills MUST be designed as composable building blocks that solve general problems, not just narrow, one-off use cases.
3. **Follow the Crafting Philosophy**: Skills SHOULD enable composition and control before generation, supporting the "build before generating" approach.
4. **Test with Real Workflows**: Skills SHOULD be validated against authentic creative workflows and tested with artist use cases.
5. **Document Thoroughly**: Every skill MUST include usage examples, parameter documentation, integration guidance, limitations, and clear guidance on appropriate usage.
6. **Consider the Full Pipeline**: Skills SHOULD be designed with awareness of upstream and downstream workflows, enabling smooth integration into larger creative pipelines.

### Quality Gates
All skills MUST meet the following quality gates before acceptance:
- **Functionality**: Core functionality MUST be tested and working as specified
- **Documentation**: Complete, accurate, and clear documentation MUST be provided
- **Compatibility**: Skills MUST work with supported skill loading mechanisms and agent environments
- **Composability**: Skills MUST follow interface contracts and integrate cleanly with other skills
- **Performance**: Skills MUST not introduce unnecessary overhead to creative workflows
- **Security**: Skills MUST handle user data, API keys, credentials, and assets securely with appropriate safeguards
- **Transparency**: Skills MUST be clear about their behavior, model usage, and any external dependencies
- **Error Handling**: Skills MUST provide graceful error handling with actionable messages

### Contribution Guidelines
- **Follow Conventions**: All contributions MUST follow established patterns, naming conventions, and architectural principles
- **Respect Licenses**: Contributions MUST be compatible with the project's open source license (MIT or Apache-2.0, dual-licensed)
- **Atomic Changes**: Changes SHOULD be focused and atomic, making review, testing, and integration straightforward
- **Community Collaboration**: We value constructive feedback, knowledge sharing, mentorship, and collaborative improvement
- **Artist Feedback**: Contributors SHOULD seek input from working artists to ensure skills meet real creative needs
- **Backwards Compatibility**: Breaking changes MUST be carefully considered, documented, and justified with migration paths

## Governance

### Constitution Authority
This Constitution supersedes all other practices, conventions, and guidelines within the ArtCraft Skills project. All skills, contributions, architectural decisions, and development activities MUST comply with these principles.

### Amendment Process
Amendments to this Constitution require:
1. **Documentation**: All proposed amendments MUST be clearly documented with rationale, impact analysis, and examples
2. **Community Review**: Significant changes SHOULD be discussed openly with the community, allowing for feedback and iteration
3. **Versioning**: Constitution version MUST follow semantic versioning (MAJOR for incompatible governance changes, MINOR for additions/expansions, PATCH for clarifications and corrections)
4. **Migration Plan**: MAJOR changes MUST include a migration plan for existing skills, workflows, and documentation
5. **Ratification**: Amendments take effect upon documented ratification following the review process

### Compliance and Evolution
- **Review Requirement**: All skill submissions and major changes MUST be reviewed for constitutional compliance
- **Justification Required**: Any deviation from these principles MUST be explicitly justified, documented, and reviewed for necessity
- **Living Document**: This Constitution SHOULD evolve with the creative tools landscape, AI capabilities, and community needs while maintaining its core commitment to artists, intentional crafting, openness, and interoperability
- **Principled Pragmatism**: We balance idealism with practicality - principles guide decisions, but we remain pragmatic about implementation realities

**Version**: 2.0.0 | **Ratified**: 2026-11-03 | **Last Amended**: 2026-11-03
