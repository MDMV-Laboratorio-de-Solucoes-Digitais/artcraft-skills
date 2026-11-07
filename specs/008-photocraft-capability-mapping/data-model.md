# Data Model: PhotoCraft MCP capability mapping (008)

**Date**: 2026-11-06 | **Scope**: documentação/mapeamento (sem persistência de runtime, sem DB)

## Entities

### CapabilityMapEntry

Representa uma capacidade MCP PhotoCraft mapeada para consumo por mantenedores/skills futuras.

| Field | Type | Required | Description |
|---|---|---|---|
| `capability_id` | string | yes | Identificador estável do mapeamento (repo-local), ex. `photocraft.command_run`. |
| `tool_name` | string | conditional | Nome MCP tool (`command_run`, `doc_inspect`) quando aplicável. |
| `command_id` | string | conditional | ID de engine command (ex. `edit.fill`) quando aplicável via `command_list`/`command_run`. |
| `tier` | enum `P1\|P2\|P3` | yes | Prioridade/defensabilidade. |
| `transport` | string | yes | `mcp-stdio` (006). |
| `discovery` | object | yes | Como detectar: `tools_list`, `command_list`, metadata keys, defensive checks. |
| `input_constraints` | object | yes | Params conhecidos, roots, formatos, limites (`max_side` etc.), unknowns. |
| `output_shape` | object | yes | Alto nível: `SkillResult`-normalizable, MCP `content`/structured, `isError`. |
| `safety_notes` | list[string] | yes | Roots, overwrite, no AI claim, no secrets/PII, opt-in real validation. |
| `evidence_status` | enum `observed\|documented\|unverified` | yes | Nível de evidência. |
| `protocol_limits` | object | yes | MCP 2025-11-25/2026-07-28, stateless adapter 006, progress/cancel support status. |

### SafetyBoundary

| Field | Type | Description |
|---|---|---|
| `read_root` | absolute path (future runtime) | Raiz de leitura autorizada (headless MCP). |
| `write_root` | absolute path (future runtime) | Raiz de escrita/export autorizada. |
| `opt_in_required` | boolean | Sempre `true` para validação real. |
| `ci_default` | boolean | Sempre `false` para smoke/validação real. |
| `cleanup` | string | Temp auto-created roots limpos; explicit roots maintainer-managed. |

### EvidenceRecord

| Field | Type | Description |
|---|---|---|
| `status` | `observed\|documented\|unverified` | Nível. |
| `source` | string | `007 quickstart`, `OBJETIVO.md`, URL pública, etc. |
| `date` | date | Data de acesso/observação. |
| `scope` | string | Limites (ex.: 0.20.1, stateless, `tools/list`+`command_list`). |

## Validation Rules

- `evidence_status=observed` requer fonte local/reproduzível com escopo explícito; não implica suporte universal.
- `tier=P1` requer gating defensivo documentado e exclusão de IA/stateful quando relevante.
- Nenhuma entrada pode declarar prompt-based AI generation como suportada neste mapeamento.
- Entradas cross-call devem marcar dependência/limite de stateless adapter 006 e deferral a 007 Option B.
- `ci_default` para execução real deve ser `false`.

## State Transitions (documentation lifecycle)

`unverified` → `documented` (fonte primária confiável) → `observed (limited)` (validação opt-in autorizada com evidência) → `mapped-stable` (múltiplas evidências/versões; futuro, fora de 008). Regressões voltam para status menor com nota.