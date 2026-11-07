# Feature Specification: PhotoCraft MCP capability mapping (engine/editor)

**Feature Branch**: `[008-photocraft-capability-mapping]` *(proposed; branch may be created separately)*

**Created**: 2026-11-06

**Status**: Draft

**Input**: Plano MDMV `local://mdmv-fluxo-artcraft-skills-plan.md` (P7 80/20): “especificar mapeamento de capacidades reais do PhotoCraft via MCP (ferramentas `command_*`/`doc_*`/preview, raízes de leitura/escrita com autoridade de filesystem, progresso via `_meta.progressToken`, cancelamento via `notifications/cancelled`, semântica de erro, limitações de formato) como novo assessment + spec, sem implementar código de runtime ainda (mock-first; validação real opt-in posterior).”

**Assessment handoff**: GO (scoped, docs-only) from `.specify/assessments/008-photocraft-capability-mapping/decision.md`. Builds on 006 (MCP stdio mínimo viável, FR-005/FR-006) and 007 (stateless smoke opt-in, SC-001 exercised locally under explicit authorization for `tools/list`+`command_list`, engine/editor only). 007 Option B (stateful cross-call artifact cycle) remains deferred.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consumir um mapa de capacidades defensivo (Priority: P1)

Um mantenedor/agente que planeja uma skill PhotoCraft consulta o mapeamento para saber quais ferramentas MCP existem, quais são P1 para automação determinística engine/editor, quais constraints aplicam (roots, overwrite, stateless adapter, timeout), e como detectar capacidades de forma defensiva sem assumir catálogo fixo.

**Why this priority**: habilita skills futuras com baixo risco de overclaim/acoplamento frágil, sem tocar runtime.

**Independent Test**: revisão do spec + contratos de mapeamento permite responder: “posso usar `command_run` para `edit.fill`?” → somente após `tools/list`/`command_list` confirmar presença/parâmetros; “posso afirmar geração IA?” → não.

**Acceptance Scenarios**:

1. **Given** o spec 008 e contratos, **When** um revisor avalia uma proposta de skill de edição determinística, **Then** encontra tier P1/P2/P3, gating defensivo, limites de roots/progress/cancel/erros e exclusão explícita de IA/stateful.
2. **Given** evidência de versão observada (0.20.1, 26 tools) e docs públicas, **When** o mapeamento é consultado, **Then** trata contagens/catálogos como evidência, não como contrato rígido, e exige capability detection.

---

### User Story 2 - Preservar contratos e limites de segurança (Priority: P1)

Um revisor de segurança/governança verifica que 008 não introduz mudanças de runtime, não enfraquece opt-in de smoke real, não altera schemas públicos/FR-005/FR-006, e não abre caminho para bridge/UI/IA por ambiguidade documental.

**Why this priority**: evita regressão de segurança/contratos enquanto expande documentação.

**Independent Test**: diff do slice mostra apenas docs/specs; gates default permanecem verdes; linguagem de limites é explícita.

**Acceptance Scenarios**:

1. **Given** o slice 008, **When** executados os gates default, **Then** `PYTHONPATH=. python -m pytest -q` e `python scripts/validate_all_skills.py` permanecem inalterados (docs-only).
2. **Given** qualquer menção a validação real, **When** revisada, **Then** exige opt-in explícito, binário/root/timeout/cleanup seguros (padrões 007), nunca CI/default.

---

### User Story 3 - Planejar evolução futura sem confundir escopo (Priority: P2)

Um mantenedor planeja 007 Option B ou uma skill real e usa 008 para separar: o que o adapter atual suporta (stateless 006), o que 007 provou, o que 008 mapeia como capability reference, e o que permanece fora (stateful cross-call, IA, bridge).

**Why this priority**: reduz retrabalho e decisões duplicadas.

**Independent Test**: quickstart/data-model/plan de 008 apontam dependências e deferrals corretos.

**Acceptance Scenarios**:

1. **Given** necessidade de ciclo `doc_new → command → doc_export` cross-call, **When** consultado 008, **Then** o item é marcado fora de escopo/deferido a 007 Option B (considerando MCP 2026-07-28: sem assumir sessão server-side).
2. **Given** necessidade de prompt de geração IA, **When** consultada 008, **Then** o item é explicitamente recusado neste mapeamento (engine/editor automation only).

---

### Edge Cases

- **Drift de versão**: `photocraft-cli` expõe ferramentas/params diferentes de 0.20.1 → mapa exige `tools/list`/`command_list` gating; não usa contagens exatas.
- **Ferramenta ausente**: skill futura encontra `mcp_missing_capability` → comportamento deve ser falha estruturada/degradação conforme FR-006/contratos, não tentativa cega.
- **Roots inválidos/inseguros**: operação fora de read/write roots → tratado como erro operacional/constraint de filesystem; validação real opt-in deve usar roots absolutos seguros.
- **Progresso/cancelamento**: servidor emite `_meta.progressToken` / recebe `notifications/cancelled` → 008 documenta semântica; suporte no adapter é **não implementado neste slice** (referência para evolução).
- **Stateless adapter**: `doc_new` em uma chamada e `doc_export` em outra podem não compartilhar estado → 008 marca cross-call artifact cycle como fora de escopo (007 Option B).
- **Bridge/UI**: ferramentas `ui_*`/bridge exigem desktop/control token → fora do escopo headless 008.
- **Overwrite/formatos**: `doc_save/export` e exports multi-file têm restrições (conforme docs PhotoCraft) → mapeamento registra constraints defensivas.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O spec DEVE definir um **mapa de capacidades PhotoCraft MCP** em tiers (P1/P2/P3) cobrindo, no mínimo: discovery (`tools/list`, `command_list`), invocação engine (`command_run`, `command_batch` como referência), inspeção/preview (`doc_inspect`, `render_preview`), operações de documento/export (`doc_*` relevantes observadas/documentadas) e referência limitada a jobs/session/UI/bridge como fora de escopo headless quando aplicável.
- **FR-002**: O mapeamento DEVE exigir **gating defensivo** (presença/capacidade via `tools/list` e/ou `command_list`; parâmetros via metadata quando disponível). NÃO DEVE usar contagens exatas de tools, catálogos completos fixos ou igualdade de versão como critério de correção.
- **FR-003**: O spec DEVE documentar constraints operacionais: **roots** de leitura/escrita com autoridade de filesystem; **progresso** `_meta.progressToken` (0–1, ≤10/s, `total` quando presente); **cancelamento** `notifications/cancelled`; restrições de overwrite/formato/export (incl. exports multi-file); limites de `render_preview` (`index`, `max_side` default 1024, máx 2048 — conforme docs; validar defensivamente).
- **FR-004**: O spec DEVE documentar semântica de erro e alinhamento com FR-006 do adapter 006 (reason codes/metadados aditivos, sem secrets/PII) para falhas de capability ausente, timeout, resposta inválida, erro de tool e misconfiguração.
- **FR-005**: O spec DEVE declarar limites explícitos: **engine/editor automation only**; **sem** prompt-based AI generation/provider/model routing; **sem** sessão MCP stateful/ciclo cross-call no adapter atual (007 Option B deferida); **sem** bridge/UI/desktop control token no escopo headless; **sem** smoke MCP real em CI/default.
- **FR-006**: O spec DEVE preservar compatibilidade documental com 006/007: sem alterar `SkillResult`, schemas públicos de skills, FR-005 (seleção de modo), FR-006 (reason taxonomy aditiva), CLI/fallback, ou política opt-in de validação real. Este slice é **docs-only** (nenhum arquivo em `skills/`, `tests/`, `scripts/` modificado).
- **FR-007**: O spec DEVE definir contratos de dados de mapeamento (artefatos em `specs/008-photocraft-capability-mapping/contracts/`) descrevendo campos mínimos: `capability_id`, `tool_name`/`command_id`, `tier`, `transport` (mcp stdio), `discovery`, `input_constraints`, `output_shape` (alto nível), `safety_notes`, `evidence_status` (observed/documented/unverified), `protocol_limits`.
- **FR-008**: O spec DEVE registrar alinhamento/limites com MCP 2025-11-25 e revisão 2026-07-28 (server/discover, _meta, ausência de handshake/sessão server-side no caminho 2026; não assumir server-initiated requests deprecadas/removidas). Decisão MCP SDK v2 permanece backlog.
- **FR-009**: O spec DEVE fornecer runbook/quickstart de **validação documental** (revisão) e instruções para **validação real opt-in futura** reutilizando controles 007 (nunca executada por default; evidência apenas quando autorizada).

### Key Entities *(data/documentation)*

- **Capability Map Entry**: registro de uma capacidade MCP PhotoCraft (tool/command), tier, descoberta, constraints, evidência e limites.
- **Capability Tier**: P1 (determinístico, alto valor, defensável), P2 (útil com constraints adicionais), P3 (referência/fora do escopo headless inicial).
- **Safety Boundary**: roots, overwrite/format constraints, opt-in real, no secrets/PII, no IA claim.
- **Evidence Record**: observed (local autorizado), documented (fonte pública/oficial), unverified (requer validação futura).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Artefatos Speckit 008 completos: assessment (`intake/problem/research/concept/decision`) + spec (`spec.md`, `plan.md`, `tasks.md`, `checklists/requirements.md`, `contracts/`, `quickstart.md`, `research.md`, `data-model.md`), todos coerentes com FR-001–FR-009.
- **SC-002**: Revisão documental confirma: gating defensivo obrigatório; exclusões explícitas (IA, stateful cross-call, bridge, CI/default real smoke); nenhuma alteração em `skills/`, `tests/`, `scripts/`.
- **SC-003**: Gates default permanecem verdes após o slice: `PYTHONPATH=. python -m pytest -q` → 412 passed, 23 deselected (ou baseline equivalente documentado se alterado por trabalho não relacionado — não esperado); `python scripts/validate_all_skills.py` → 12/12.
- **SC-004**: Um mantenedor consegue, em <10 minutos, identificar para uma capability candidata: tier, pré-condições de discovery, constraints de safety, status de evidência e se está fora de escopo (IA/stateful/bridge).
- **SC-005**: Nenhum claim de geração IA/provider/model/prompt via PhotoCraft MCP local aparece como suportado; 007 Option B permanece claramente deferida.

## Assumptions

- Evidência local 007 (0.20.1, `tools/list`+`command_list`, 26 tools observadas) é válida como **observed (limited)**, não como contrato universal.
- Docs públicas `storytold/photocraft` MCP são úteis mas podem divergir da versão/binário local; validar defensivamente.
- MCP 2026-07-28 informa limites de design (especialmente stateful/Option B); adapter 006 permanece cliente mínimo compatível no escopo implementado.

## Clarifications

### Session 2026-11-06

- Q: Este slice implementa código? → A: **Não**. Docs/spec apenas; nenhum arquivo em `skills/`, `tests/`, `scripts/` modificado. (FR-006)
- Q: Inclui geração IA? → A: **Não**. Engine/editor automation only. (FR-005, SC-005)
- Q: Inclui stateful cross-call? → A: **Não**. Adapter 006 stateless; 007 Option B deferida. (FR-005)
- Q: Validação real agora? → A: **Não requerida**. Mock-first; opt-in futuro sob padrões 007, somente com autorização explícita. (FR-009)