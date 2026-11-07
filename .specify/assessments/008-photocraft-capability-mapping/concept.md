# Concept: PhotoCraft MCP capability mapping (spec-only)

- **Slug**: 008-photocraft-capability-mapping
- **Date**: 2026-11-06
- **Verdict direction**: GO (scoped, docs-only)

## Proposed Approach (80/20)

Entregar um **mapa de capacidades PhotoCraft MCP** como artefato Speckit (assessment + spec + plan + tasks + checklist + contratos de mapeamento + quickstart + data-model + research) que:

1. Cataloga capacidades em tiers (P1/P2/P3) com **gating defensivo** (`tools/list`/`command_list` presence), sem hardcode de contagens/catálogos completos.
2. Documenta semântica operacional relevante: **roots** (read/write, autoridade de filesystem), **progresso** (`_meta.progressToken`), **cancelamento** (`notifications/cancelled`), **erros/FR-006 mapping**, **restrições de overwrite/formato/export**, **statelessness do adapter 006**.
3. Separa explicitamente: **engine/editor automation (in scope)** vs **prompt-based AI generation/provider/model routing (out of scope)** vs **stateful cross-call artifact cycle (Option B, out of scope)** vs **bridge/UI mode (out of scope)**.
4. Define como skills futuras devem consumir o mapa (contrato de capability reference) sem alterar `skills/core/*` neste slice.
5. Mantém política de validação real: **mock-first**; qualquer evidência real futura apenas opt-in, binário/root/timeout/cleanup explícitos (reutilizar padrões 007), nunca CI/default.

## In Scope

- Documentação/mapeamento: `command_list`, `command_run`, `command_batch`, `doc_*` relevantes (new/open/save/export/inspect/place/select conforme evidência), `render_preview`, jobs/session como referência limitada; roots; progress/cancel; erros; limites de protocolo/versão.
- Contratos de dados de mapeamento (schema/MD) em `specs/008-.../contracts/`.
- Critérios de aceitação verificáveis por revisão + gates existentes (pytest/validação de skills) sem tocar runtime.

## Out of Scope

- Qualquer mudança em `skills/core/artcraft_app_client.py`, `skills/core/creative_skill.py`, `skills/creative/*`, `scripts/*`, `tests/*` (exceto se um gate futuro exigir — não previsto; este slice é docs-only).
- Implementação de sessão stateful MCP / ciclo `doc_new → command → doc_export` cross-call (007 Option B).
- Geração IA via PhotoCraft MCP local, seleção de provider/modelo/prompt, ou claims equivalentes.
- Execução de smoke MCP real neste slice (a menos que explicitamente autorizado depois; não requerido para convergência de spec docs).
- Suporte a bridge mode/UI tools/desktop control token.

## Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Drift de versão do `photocraft-cli` | Gating defensivo por `tools/list`/`command_list`; assertions de presença/shape, nunca contagens exatas; registrar versão observada como evidência, não contrato rígido. |
| Overclaim de IA | Seções/FRs explícitos de exclusão; linguagem "engine/editor automation only" em todos os artefatos. |
| Confusão com 007 Option B | Repetir stateless boundary do adapter 006 e apontar Option B como spec separada/deferida. |
| Escopo creep para código | P8 implement = docs; verificação final confirma nenhum arquivo em `skills/`/`tests/` alterado. |
| Protocolo MCP em evolução (2026-07-28) | Documentar limites e não afirmar server-initiated requests/deprecated features. |

## Success (for spec slice)

- Assessment completo com decisão **go**.
- Spec 008 com FR/SC/acceptance testáveis por revisão.
- Plan/tasks decision-complete, sem dependência de mudanças de runtime.
- Gates do repo permanecem verdes (docs-only).