# Avaliação de Andamento — Speckit (assessments, specs, bugs)

- **Data**: 2026-11-06
- **Fonte**: leitura direta de `.specify/assessments/`, `specs/`, `.specify/` e artefatos 008 criados nesta rodada (plano `local://mdmv-fluxo-artcraft-skills-plan.md`, P8/P9).
- **Gates (verificados nesta rodada, docs-only)**: `PYTHONPATH=. python -m pytest -q` → **412 passed, 23 deselected**; `python scripts/validate_all_skills.py` → **12/12, `all_valid=True`**.

## Assessments (`.specify/assessments/`, 8 diretórios)

| Assessment | Artefatos | Status (evidência) |
|---|---|---|
| `artcraft-skills-suite-intake` | intake/problem/research/concept/decision | Decisão tomada; base do programa 001 |
| `shared-cli-mcp-adapter` | intake/problem/research/concept/decision | Decisão tomada; implementado/convergido em 003 |
| `implement-python-creative-skills` | intake/problem/research/concept/decision | Decisão tomada; convergido em 004 |
| `resiliencia-creativeskill` | intake/problem/research/concept/decide | Decisão tomada; convergido em 005 (evidência de resiliência; checkboxes residuais de higiene documental possíveis) |
| `mcp-stdio-functional-integration` | intake/problem/research/concept/decision | Decisão tomada; convergido em 006-mcp-stdio-functional-integration |
| `integracao-geracao-assets` | intake/problem/research/concept/decision | Decisão tomada; spec `006-integracao-geracao-assets` reconciliada como doc hygiene/ambiguidade histórica de numeração `006-*` (não confundir com 006-mcp-stdio) |
| `photocraft-mcp-verified-smoke` | intake/problem/research/concept/decision | Decisão GO (Option A stateless); convergido em 007 Option A; Option B deferida |
| `008-photocraft-capability-mapping` | intake/problem/research/concept/decision | **GO (scoped, docs-only)** — spec 008 criada nesta rodada; sem alteração de runtime; validação real futura apenas opt-in/007 |

## Specs (`specs/`, 8 diretórios)

| Spec | Estado | Observações |
|---|---|---|
| `001-artcraft-skills-suite` | Convergido (escopo definido) | Fundação do programa |
| `003-shared-cli-mcp-adapter` | Convergido | Adapter compartilhado CLI/MCP |
| `004-implement-python-creative-skills` | Convergido | Skills criativas Python (escopo atual) |
| `005-resiliencia-creativeskill` | Convergido (evidência) | Retry/backoff/jitter/semáforo; reconciliar checkboxes residuais se necessário (doc hygiene) |
| `006-mcp-stdio-functional-integration` | Convergido | MCP stdio mínimo viável, FR-005/FR-006, mock-first |
| `006-integracao-geracao-assets` | Reconciliada (doc hygiene) | Ambiguidade histórica de numeração com 006-mcp-stdio; não reescrever histórico |
| `007-photocraft-mcp-smoke` | Convergido (Option A stateless) | SC-001 exercido localmente sob autorização explícita (escopo limitado, engine/editor); **Option B stateful deferida** |
| `008-photocraft-capability-mapping` | **Draft/spec criado (docs-only, GO)** | Mapeamento de capacidades PhotoCraft MCP (defensive gating, roots/progress/cancel/errors, exclusões IA/stateful/bridge). Sem código; mock-first; real opt-in futuro |

## Bugs (`.specify/bugs/`)

- Diretório **`.specify/bugs/` não existe** no repositório (fato verificado nesta sessão). Existe `.specify/extensions/bug/` (infra de extensão). Bugs/problemas devem ser rastreados via issues do GitHub remoto quando aplicável (verificar com `gh issue list` se necessário).

## Resumo

- **Convergidos (escopo definido)**: 001, 003, 004, 005 (evidência), 006-mcp-stdio, 007 Option A.
- **Reconciliado/higiene**: 006-integracao-geracao-assets (numeração ambígua).
- **Novo 80/20 (esta rodada)**: 008-photocraft-capability-mapping — assessment GO + spec/docs completos, docs-only, sem alteração de runtime.
- **Pendentes**: 007 Option B (stateful, spec separada), decisão MCP SDK v2, mapeamento/capabilities implementation follow-ups, job CI real opcional, Phases 3–5, matriz de compatibilidade.