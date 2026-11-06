# Objetivo do Projeto

## Visão Geral

ArtCraft Skills Suite tem como objetivo construir um ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O projeto capacita artistas, designers e criadores a transformar prompts em *crafting* intencional, com controle preciso e fluxos compostos em vez de geração *one-shot*.

As skills não reimplementam motores de geração: expõem, de forma composável e governada, capacidades reais dos apps ArtCraft (PhotoCraft, PdfCraft e demais “Crafting Apps” Rust da organização `storytold`) via superfícies de **CLI** (`photocraft-cli`, 500+ comandos) e **MCP server**, além do AI studio da ArtCraft. O repositório é a *camada de skill/agente* sobre essas superfícies.

## Estado Atual (Verificado — 2026-11-06)

- **Branch:** `dev` (sincronizado com `origin/dev`, merge `d62e5e0` integrando stack 007 #131–#135). Remoto/local: apenas `dev` e `main`. Sem PRs abertos.
- **Gates padrão (verificados):** **412 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`); **12/12 skills validadas** (`python scripts/validate_all_skills.py`). Testes `@pytest.mark.integration` ficam excluídos por padrão (`pytest.ini: -m "not integration"`).
- **Convergência Speckit (escopo definido):** 001, 003, 004, 005 (resiliência) e 006-MCP stdio funcional convergidos com evidência em `specs/*`. **007 PhotoCraft MCP Verified Local Smoke (Option A, stateless)** concluído/convergido (T001–T023): harness *test-only* opt-in, mock-first preservado, **SC-001 exercido sob autorização explícita** no ambiente local (escopo limitado, engine/editor; sem IA/provider/model), com evidência em `specs/007-photocraft-mcp-smoke/quickstart.md`.
- **Pesquisa/documentação:** `docs/research/2026-11-06-ecosystem-roadmap-status.md` (fontes primárias: agentskills.io, MCP 2025-11-25 stdio, docs `storytold/photocraft` MCP; evidência local + gaps).

## O que funciona (verificado)

- Schema/validação/descoberta/carregamento agentskills.io, core abstractions, composição (`SkillComposer`) e DAG (`DAGOrchestrator`).
- Adapter compartilhado `skills/core/artcraft_app_client.py`: discovery/invocação CLI, transport MCP stdio mínimo (`tools/list`/`tools/call`) com normalização para `SkillResult`, reason codes/taxonomia FR-006 aditiva, seleção FR-005 (explícito `mcp` sem reroute silencioso; `auto` preserva CLI-first/back-compat), fallback de edição (`generate_via_editing_commands`).
- `CreativeSkill` resiliente: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)`.
- 5 skills criativas Python executáveis: `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`; `scene-composition` executável; workflows generalizáveis.
- **007 (escopo limitado, verificado com autorização explícita):** smoke real local stateless `tools/list` + `tools/call name=command_list` contra `photocraft-cli 0.20.1` (`/usr/bin/photocraft-cli`), temp roots limpas, timeout 30s, capability presente, resultado ok/não-erro/normalizável; `stateless/session_reuse=false/artifact_cycle=false`. **Automação engine/editor apenas.**

## O que falta

1. **Operacionalização opcional controlada:** job/manual para smoke MCP real em ambiente autorizado (nunca default), com gestão segura de binário/evidência.
2. **007 Option B (spec separada):** sessão MCP stateful para ciclo determinístico `doc_new → command → doc_export` em sessão retida; mock-first + validação opt-in real.
3. **Mapeamento MCP por capacidade real** (PhotoCraft/outros Crafting Apps): tools/roots/progresso/cancelamento/formatos/erros, sem reivindicar geração IA indevida.
4. **Decisão de dependência MCP (quando necessário):** avaliar SDK Python oficial (`modelcontextprotocol/python-sdk`, linha v2.x observada) vs cliente mínimo atual para lifecycle/auth remota/Streamable HTTP/compatibilidade ampliada; manter mock-first/back-compat.
5. **Backlog Speckit:** `specs/005-resiliencia-creativeskill` tem checkboxes de implementação parcialmente marcados (evidência de convergência existe — reconciliar); `specs/006-integracao-geracao-assets` (0/11) permanece backlog/numeração ambígua com `006-mcp-stdio-functional-integration` — normalizar referências sem reescrever histórico.
6. **Expansão de domínios (Phases 3–5):** vídeo/motion/animação; áudio/voz/docs/apresentações; CAD/precisão/técnico.
7. **Produto/adoção:** `README.md` raiz, exemplos reais, onboarding CLI/MCP, matriz de compatibilidade (Crafting Apps/MCP).

## O que este projeto NÃO faz

- Não reimplementa modelos/provedores de geração nem backend próprio; orquestra superfícies reais ArtCraft.
- Não substitui os apps ArtCraft.
- **Não executa smoke MCP real em CI/default**; exige opt-in + autorização explícita + controles de segurança.
- **Não prova/implementa geração IA** via PhotoCraft MCP local (007 = automação engine/editor stateless), nem roteamento provider/modelo/prompt nesse caminho.
- **Não implementa** sessão MCP stateful/ciclo de artefato cross-call (Option B adiada).
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos.
- Não fabrica evidência (ausência de execução autorizada = não exercido/não atestado).

## Métricas (verificadas)

- ✅ **412/412** testes default passando, **23** deselected (integração opcional)
- ✅ **12/12** skills validadas
- ✅ 001/003/004/005/006-MCP convergidos (escopo definido)
- ✅ 007 convergido (Option A stateless); SC-001 exercido localmente sob autorização (escopo limitado)
- ⏳ Option B (MCP stateful) — próxima decisão/spec quando priorizado
