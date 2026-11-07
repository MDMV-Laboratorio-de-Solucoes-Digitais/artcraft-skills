# Contract: PhotoCraft MCP Capability Map (008)

**Status**: Draft (docs-only). **No runtime API changes.**

## Purpose

Define a estrutura mínima para entradas de mapeamento de capacidades PhotoCraft MCP consumidas por specs/skills futuras, preservando 006/007 e a constitution.

## Entry Schema (conceptual)

```yaml
capability_id: photocraft.<area>.<name>      # required, repo-local stable id
tool_name: command_run                        # MCP tool name, when applicable
command_id: edit.fill                         # engine command id, when applicable
tier: P1                                      # P1|P2|P3
transport: mcp-stdio                          # 006
discovery:
  tools_list_required: true
  command_list_required: false                # true for engine command ids
  defensive_checks:
    - "confirm tool presence via tools/list"
    - "do not assert exact tool count/catalog"
input_constraints:
  roots_required: true                        # for filesystem-affecting ops
  known_params: {}
  limits: {}
  unknowns: []
output_shape:
  skillresult_normalizable: true
  mcp_shapes: ["content", "structured", "isError"]
safety_notes:
  - "engine/editor automation only; no AI generation claim"
  - "opt-in real validation only; never CI/default"
  - "respect read/write roots and overwrite/format constraints"
evidence_status: documented                   # observed|documented|unverified
protocol_limits:
  mcp_revisions: ["2025-11-25-compatible-scope", "2026-07-28-aware-limits"]
  adapter_stateless: true                     # 006
  stateful_cross_call: deferred-option-b
  progress_cancel_adapter_support: not-implemented-in-008
```

## Required Rules

1. **Defensive gating**: every runtime-consumer spec MUST require `tools/list` (and `command_list` for engine IDs) presence checks before invocation. MUST NOT rely on exact tool counts or full static catalogs.
2. **No AI claim**: entries MUST NOT describe prompt-based AI generation/provider/model routing as supported.
3. **No stateful assumption**: entries affecting cross-call artifacts MUST document adapter 006 statelessness and 007 Option B deferral.
4. **Safety**: filesystem operations MUST note root authority and overwrite/format constraints; real validation MUST follow 007 opt-in controls.
5. **Evidence honesty**: `observed` entries MUST include scope/date/source limits; public docs do not override local safety constraints.
6. **Compatibility**: mapping entries are additive references; they MUST NOT change `SkillResult`, public skill schemas, FR-005, FR-006, CLI, or fallback.

## Non-Goals

- No OpenAPI/runtime endpoint. No code generation. No test harness added by 008. No bridge/UI contract.