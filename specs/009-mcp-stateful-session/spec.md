# Feature Specification: MCP stateful session helper (007 Option B)

**Feature Branch**: `[009-mcp-stateful-session]`

**Created**: 2026-11-06

**Status**: Implemented (additive runtime + mock-first tests, 2026-11-06); preserves 006 stateless APIs/FR-005/FR-006/schemas

**Input**: Próximo 80/20 (MDMV 2026-11-06, após 008): especificar 007 Option B — sessão MCP stateful para ciclo determinístico `doc_new → command → doc_export`/artefato em **uma sessão retida**, mock-first para implementação futura, validação real opt-in posterior, preservando 006/007/008 e contratos públicos. Sem implementação de runtime neste slice.

**Assessment handoff**: GO (scoped, docs-only nesta rodada) from `.specify/assessments/009-mcp-stateful-session/decision.md`. Referências: 006 (MCP stdio mínimo, stateless, FR-005/FR-006), 007 (Option A smoke stateless; Option B deferida), 008 (capability map, defensive gating).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Contrato de sessão stateful aditivo (Priority: P1)

Um mantenedor precisa de um contrato claro para uma sessão MCP stateful que retenha um subprocesso stdio para múltiplas chamadas correlacionadas, sem substituir as APIs stateless 006.

**Why this priority**: desbloqueia implementação futura segura de ciclos cross-call.

**Independent Test**: spec define lifecycle (open/init/list/call*/close), cleanup, timeouts, erros FR-006-aligned e preservação de `mcp_tools_list`/`mcp_tools_call`.

**Acceptance Scenarios**:

1. **Given** o spec 009, **When** um implementador projeta o helper, **Then** encontra requisitos para processo retido, correlação de JSON-RPC ids, cleanup em sucesso/falha/timeout, e não modificação das APIs stateless 006.
2. **Given** falha no meio da sessão, **When** especificada, **Then** exige encerramento bounded do subprocesso, cleanup de recursos harness-managed e resultado estruturado acionável (FR-006 aligned).

---

### User Story 2 - Ciclo determinístico engine/editor com safety (Priority: P1)

Um revisor valida que o ciclo alvo (ex.: discovery → `doc_new` → engine command → export/inspect) é **engine/editor only**, capability-gated, opt-in real, com roots/temp/cleanup/timeout.

**Why this priority**: evita claims inseguros e mantém alinhamento com 007/008.

**Independent Test**: spec inclui acceptance para ciclo mínimo condicionado a capabilities; exclui IA e default CI.

**Acceptance Scenarios**:

1. **Given** ambiente opt-in autorizado com capabilities presentes, **When** validação real futura for executada, **Then** o ciclo usa roots absolutos seguros, timeout bounded, cleanup e evidencia stateless-boundary anterior vs sessão retida, sem claim de IA.
2. **Given** capability ausente ou servidor sem estado cross-call útil, **When** avaliado, **Then** resultado é skip/falha estruturada (`mcp_missing_capability`/tool error) com evidência, sem fallback silencioso indevido.

---

### User Story 3 - Compatibilidade de protocolo e contratos (Priority: P2)

Um mantenedor confirma compatibilidade documental com MCP 2025-11-25 stdio e consciência de MCP 2026-07-28 (sem assumir sessão server-side no caminho 2026), preservando FR-005/FR-006/schemas.

**Why this priority**: reduz retrabalho na evolução do protocolo.

**Independent Test**: spec/plan registram limites e não afirmam features não implementadas.

**Acceptance Scenarios**:

1. **Given** MCP 2026-07-28, **When** consultado, **Then** o design prefere estado retido no cliente/processo vivo e documenta `server/discover`/negociação como follow-up; não assume `_Mcp-Session-Id` server-side.
2. **Given** implementação futura, **When** adicionada, **Then** deve ser mock-first com fake stdio server determinístico cobrindo sessão retida, ids correlacionados, erros e cleanup.

### Edge Cases

- Servidor encerra stdout/exit mid-session → erro estruturado, cleanup, sem hang.
- Timeout em uma chamada dentro da sessão → política explícita (abort call/session), cleanup bounded, FR-006 reason.
- `isError`/tool error em passo intermediário → parar ciclo, reportar passo/ferramenta, cleanup.
- Export overwrite/format constraints (PhotoCraft docs/008) → respeitar; preferir write-root temporária isolada.
- Drift de tool names/params → capability gating via `tools/list`/`command_list` (008), sem contagens exatas.
- Bridge/UI tools → fora do escopo headless.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O spec DEVE definir um **helper/sessão MCP stateful aditivo** (nome/API final a decidir na implementação, contrato fixado aqui) que retém um subprocesso MCP stdio para múltiplas chamadas em sequência, com correlação JSON-RPC `id`, sem substituir `mcp_tools_list`/`mcp_tools_call` stateless.
- **FR-002**: O lifecycle DEVE incluir: validação de config/binário/roots (opt-in para real), start subprocess, initialize/handshake conforme caminho suportado, N chamadas `tools/call`/`tools/list` na mesma sessão, shutdown/cleanup bounded em todos os caminhos (sucesso, erro, timeout, exceção).
- **FR-003**: O spec DEVE exigir **mock-first** para implementação futura: testes determinísticos com fake stdio server cobrindo sessão retida, múltiplas chamadas, correlação de ids, timeout, invalid response, tool error, missing capability e cleanup. Real validation permanece opt-in, autorização explícita, controles 007.
- **FR-004**: O ciclo determinístico alvo MÍNIMO (referência PhotoCraft engine/editor, condicionado a capabilities) DEVE ser especificado como: discovery → operação de criação/contexto de documento (ex. `doc_new` se disponível) → comando engine determinístico (via `command_run`/equivalente gated) → verificação/export seguro em write-root temporária (ex. `doc_export`/`doc_inspect`/artefato conforme suportado). **Sem** geração IA. Se capability/estado não suportado, resultado estruturado (skip/falha), não claim de sucesso.
- **FR-005**: Safety: opt-in explícito para real; binário absoluto explícito preferido; roots absolutos (temp auto-cleaned por padrão em harness futuro); bounded timeouts; sem segredos/PII em logs/evidência; cleanup de processo e temp; **nunca** CI/default.
- **FR-006**: Preservar contratos: `SkillResult`/schemas públicos inalterados; FR-005 seleção; FR-006 reason taxonomy/metadados aditivos; sem reroute silencioso MCP→CLI em modo explícito MCP. Session helper é aditivo.
- **FR-007**: Gating defensivo (008): `tools/list`/`command_list` antes de invocar; não assumir contagens/catálogos/versões fixas; documentar evidência observed/documented/unverified.
- **FR-008**: Protocolo: suportar framing JSON-RPC newline-delimited stdio (006). Documentar limites MCP 2026-07-28 (server/discover, sem assumir sessão server-side no caminho 2026; client-retained process state). SDK v2 migration backlog.
- **FR-009 (updated 2026-11-06)**: Assessment + spec/plan/tasks/checklist/contracts/quickstart/research/data-model criados. **Runtime implementado em slice separado autorizado**: helper aditivo em `skills/core/artcraft_app_client.py` (`mcp_stateful_session`/`MCPStatefulSession`, `__version__ 0.4.0`) + testes determinísticos mock-first (`tests/unit/test_mcp_stateful_session_009.py`, cenários fake stdio estendidos). **Preservadas** APIs stateless 006, `SkillResult`/schemas públicos, FR-005/FR-006, CLI/fallback. Sem geração IA, sem bridge/UI, sem CI/default real, sem sessão server-side MCP 2026-07-28 assumida.

### Key Entities

- **MCPStatefulSession** (conceitual): subprocesso retido + config + roots + timeout policy + next request id.
- **SessionStepResult**: resultado normalizado por chamada (sucesso/falha FR-006-aligned).
- **DeterministicArtifactCycle**: sequência mínima document-scoped com evidência/limites.
- **SafeSessionBoundary**: opt-in, binário, roots, cleanup, timeout.

## Success Criteria *(mandatory)*

- **SC-001**: Artefatos 009 completos e coerentes (assessment GO + spec/plan/tasks/checklist/contracts/quickstart/research/data-model), rastreáveis a 006/007/008.
- **SC-002**: Contrato especifica lifecycle/cleanup/timeout/FR-006/errors e ciclo determinístico mínimo sem IA.
- **SC-003 (updated)**: Exclusões explícitas preservadas: sem geração IA, sem bridge/UI headless, sem CI/default real. Runtime aditivo permitido por slice autorizado com TDD/mock-first e preservação de contratos; sem mudança em skills públicas existentes além do adapter aditivo documentado/contratado.
- **SC-004 (verified 2026-11-06)**: Gates default verdes após runtime aditivo 009 (mock-first): pytest default **421 passed, 23 deselected** (baseline 412+23; +9 testes 009), **12/12 skills válidas**.
- **SC-005**: Revisão confirma: APIs 006 stateless preservadas; stateful aditivo; MCP 2026-07-28 limits documentados.

## Assumptions

- PhotoCraft (ou servidor compatível) pode manter estado de documento em processo vivo; comprovação real é opt-in futura.
- 006 framing/normalização são base reutilizável; refatoração interna futura deve preservar contratos.

## Clarifications

### Session 2026-11-06

- Q: Implementar código agora? → A: **Não**. Docs-only spec/assessment; runtime em slice futuro com TDD/mock-first.
- Q: Substituir APIs stateless? → A: **Não**. Helper aditivo.
- Q: IA/stateful server-side assumido? → A: **Não** (IA excluída; MCP 2026-07-28 → client-retained process state).