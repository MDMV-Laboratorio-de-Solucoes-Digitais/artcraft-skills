# Decision: MCP stateful session (007 Option B)

- **Slug**: 009-mcp-stateful-session
- **Decided**: 2026-11-06
- **Verdict**: go
- **Artifacts reviewed**: intake/problem/research/concept; 006/007/008 specs; OBJETIVO/ROADMAP; MCP 2026-07-28/SDK notes (2026-11-06)

## Scorecard

| Criterion | Rating | Justification |
|---|---|---|
| Problem validity | strong | Adapter 006 stateless bloqueia composição cross-call; 007/008 documentam deferment. |
| Evidence strength | adequate | Limitação stateless comprovada; MCP stdio suporta subprocesso retido; detalhes de stateful dependem de servidor/implementação futura (exigir mock-first + opt-in). |
| Value vs. inaction | strong | Habilita próximo passo para ciclos engine/editor determinísticos (doc→command→export) com segurança. |
| Feasibility / appetite | adequate | Design estreito possível como helper aditivo; implementação real tem risco moderado (process lifecycle) — spec deve conter controles. |
| Strategic fit | strong | Alinha com roadmap Phase 6/007 Option B, 008 capability map, constitution (segurança, transparência, sem IA). |
| Risk posture | adequate | Mitigável por opt-in, cleanup, bounded timeouts, defensive gating, docs-only agora. |

## Verdict & Rationale

**GO (scoped, spec/docs-only nesta rodada).** Produzir assessment + spec 009 para sessão MCP stateful (007 Option B): helper aditivo, subprocesso retido/client state, ciclo determinístico engine/editor opt-in, mock-first para implementação futura, sem alterações de runtime em `skills/`/`tests/`/`scripts/` neste slice. Preservar 006 stateless, FR-005/FR-006, schemas públicos. **Exclusões**: geração IA, bridge/UI, CI/default real smoke.

## Handoff to `/speckit.specify`

- **Problem**: stateless 006 impede cross-call; precisa contrato seguro para sessão retida.
- **Chosen approach**: 009 spec com lifecycle/contrato/FR/SC/checklist/tasks; implementação futura separada.
- **Success metrics**: artefatos 009 completos; gates verdes; nenhum claim IA/stateful server-side indevido.
- **Carried-forward open questions**: API final (módulo/helper), subconjunto mínimo de tools para prova, suporte progress/cancel em sessão retida, alinhamento `server/discover` 2026-07-28.