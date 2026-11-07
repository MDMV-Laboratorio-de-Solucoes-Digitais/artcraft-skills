# Decision: PhotoCraft MCP capability mapping

- **Slug**: 008-photocraft-capability-mapping
- **Decided**: 2026-11-06
- **Verdict**: go
- **Artifacts reviewed**: intake.md | problem.md | research.md | concept.md | `specs/006-*`/`007-*` (006 stdio, 007 stateless smoke) | `OBJETIVO.md`/`ROADMAP.md` (2026-11-06) | pesquisa externa 2026-11-06

## Scorecard

| Criterion | Rating | Justification |
|---|---|---|
| Problem validity | strong | Falta mapeamento consolidado de capabilities MCP reais; 006/007 provaram transporte/smoke limitado mas não cobrem mapeamento por capacidade/constraints. |
| Evidence strength | adequate | Evidência local limitada + autorizada (007: `tools/list`+`command_list`, 26 tools observadas em 0.20.1) + docs públicas `storytold/photocraft` + specs MCP/SDK. Suficiente para spec de mapeamento defensivo; insuficiente para claims de IA/stateful/cobertura universal. |
| Value vs. inaction | strong | Desbloqueia planejamento seguro de skills futuras com baixo esforço (docs-only), reduz risco de overclaim e retrabalho. |
| Feasibility / appetite | strong | Nenhuma mudança de runtime; reutiliza padrões 006/007 e templates Speckit; mock-first preservado. |
| Strategic fit | strong | Alinhado à constitution (CLI/MCP-first, transparência, graceful degradation, crafting>generating, sem reimplementar backend) e ao roadmap (Phase 6 capability mapping). |
| Risk posture | adequate | Riscos controlados por escopo estrito: engine/editor only, stateless, opt-in real, gating defensivo, no AI claim. |

## Verdict & Rationale

**GO (scoped, docs-only).** Especificar e documentar o mapeamento de capacidades PhotoCraft MCP (ferramentas, roots, progress, cancelamento, erros, limites de protocolo/versão/formato) com gating defensivo e limites explícitos. **Não** implementar código de runtime, **não** adicionar sessão stateful, **não** afirmar geração IA/provider/model. Validação real futura permanece opt-in (padrões 007).

## If go — Handoff to `/speckit.specify`

- **Problem**: ausência de mapa consolidado de capabilities MCP PhotoCraft com limites operacionais, gerando risco de overclaim e acoplamento frágil.
- **Chosen approach**: spec 008 (assessment + spec/plan/tasks/checklist/contracts/quickstart/data-model/research), docs-only, mock-first; capability tiers P1/P2/P3; gating defensivo; FRs explícitos de exclusão (IA/stateful/bridge).
- **In scope / out of scope**: ver `concept.md` e `specs/008-photocraft-capability-mapping/spec.md`.
- **Success metrics**: artefatos Speckit completos; FR/SC/acceptance verificáveis por revisão; gates do repo verdes (412/23, 12/12) sem alteração de runtime.
- **Carried-forward open questions**:
  - Subconjunto P1 mínimo definitivo para skills determinísticas (confirmar em clarify): `command_list`+`command_run`+`doc_inspect`+`render_preview`? `doc_new/open/save/export`? (evidência de statelessness do adapter limita cross-call).
  - Como capturar progress/cancel em evidência futura sem mudar adapter 006.
  - Nomenclatura/estabilidade de engine commands por versão (`command_list` metadata é fonte de verdade).
- **Option B contingency** (decisão do usuário, fora desta decisão): se mantainer priorizar stateful MCP, substituir execução por 007 Option B spec/decide.