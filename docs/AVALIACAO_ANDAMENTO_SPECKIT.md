# Avaliação de Andamento — Speckit (assessments, specs, bugs)

- **Data**: 2026-11-06
- **Fonte**: leitura direta de `.specify/assessments/`, `specs/`, `.specify/`; 008 (docs-only) + 009 (007 Option B) especificado e runtime aditivo implementado em slice autorizado TDD/mock-first (2026-11-06).
- **Gates (verificados 2026-11-06, pós-009 runtime aditivo mock-first)**: `PYTHONPATH=. python -m pytest -q` → **424 passed, 23 deselected**; `python scripts/validate_all_skills.py` → **12/12, `all_valid=True`**.

## Assessments (`.specify/assessments/`, 9 diretórios)

| Assessment | Artefatos | Status (evidência) |
|---|---|---|
| `artcraft-skills-suite-intake` | intake/problem/research/concept/decision | Decisão tomada; base do programa 001 |
| `shared-cli-mcp-adapter` | intake/problem/research/concept/decision | Decisão tomada; implementado/convergido em 003 |
| `implement-python-creative-skills` | intake/problem/research/concept/decision | Decisão tomada; convergido em 004 |
| `resiliencia-creativeskill` | intake/problem/research/concept/decide | Decisão tomada; convergido em 005 (evidência de resiliência; checkboxes residuais de higiene documental possíveis) |
| `mcp-stdio-functional-integration` | intake/problem/research/concept/decision | Decisão tomada; convergido em 006-mcp-stdio-functional-integration |
| `integracao-geracao-assets` | intake/problem/research/concept/decision | Decisão tomada; spec `006-integracao-geracao-assets` reconciliada como doc hygiene/ambiguidade histórica de numeração `006-*` (não confundir com 006-mcp-stdio) |
| `photocraft-mcp-verified-smoke` | intake/problem/research/concept/decision | Decisão GO (Option A stateless); convergido em 007 Option A; Option B especificada/implementada aditivamente em 009 (mock-first) |
| `009-mcp-stateful-session` | intake/problem/research/concept/decision | **GO** — 007 Option B: sessão MCP stateful aditiva, runtime mock-first + testes determinísticos (2026-11-06); preserva 006 stateless/FR-005/FR-006; real opt-in futuro (007) |
| `008-photocraft-capability-mapping` | intake/problem/research/concept/decision | **GO (scoped, docs-only)** — spec 008 criada nesta rodada; sem alteração de runtime; validação real futura apenas opt-in/007 |

## Specs (`specs/`, 9 diretórios)

| Spec | Estado | Observações |
|---|---|---|
| `001-artcraft-skills-suite` | Convergido (escopo definido) | Fundação do programa |
| `003-shared-cli-mcp-adapter` | Convergido | Adapter compartilhado CLI/MCP |
| `004-implement-python-creative-skills` | Convergido | Skills criativas Python (escopo atual) |
| `005-resiliencia-creativeskill` | Convergido (evidência) | Retry/backoff/jitter/semáforo; reconciliar checkboxes residuais se necessário (doc hygiene) |
| `006-mcp-stdio-functional-integration` | Convergido | MCP stdio mínimo viável, FR-005/FR-006, mock-first |
| `006-integracao-geracao-assets` | Reconciliada (doc hygiene) | Ambiguidade histórica de numeração com 006-mcp-stdio; não reescrever histórico |
| `007-photocraft-mcp-smoke` | Convergido (Option A stateless) | SC-001 exercido localmente sob autorização explícita (escopo limitado, engine/editor); Option B coberta por 009 (aditivo, mock-first) |
| `009-mcp-stateful-session` | **Spec + runtime aditivo implementado (mock-first, 2026-11-06)** | `mcp_stateful_session`/`MCPStatefulSession` (subprocesso retido, ids correlacionados, cleanup bounded, FR-006); +9 testes; preserva 006/FR-005/FR-006/schemas; sem IA/bridge/UI/CI-default real |
| `008-photocraft-capability-mapping` | **Draft/spec criado (docs-only, GO)** | Mapeamento de capacidades PhotoCraft MCP (defensive gating, roots/progress/cancel/errors, exclusões IA/stateful/bridge). Sem código; mock-first; real opt-in futuro |

## Bugs (`.specify/bugs/`)

- Diretório **`.specify/bugs/` não existe** no repositório (fato verificado nesta sessão). Existe `.specify/extensions/bug/` (infra de extensão). Bugs/problemas devem ser rastreados via issues do GitHub remoto quando aplicável (verificar com `gh issue list` se necessário).

## Resumo

- **Convergidos (escopo definido)**: 001, 003, 004, 005 (evidência), 006-mcp-stdio, 007 Option A.
- **Reconciliado/higiene**: 006-integracao-geracao-assets (numeração ambígua).
- **80/20 008 (anterior)**: 008-photocraft-capability-mapping — assessment GO + spec/docs completos, docs-only.
- **80/20 009 (2026-11-06, concluído)**: 007 Option B — assessment GO + spec + runtime aditivo `mcp_stateful_session`/`MCPStatefulSession` (TDD/mock-first), preservando contratos; real artifact cycle ainda opt-in.
- **Pendentes**: ciclo real de artefato stateful opt-in (009 helper pronto, capability/ambiente 007/008), decisão MCP SDK v2, follow-ups de capability mapping, job CI real opcional, Phases 3–5, matriz de compatibilidade.