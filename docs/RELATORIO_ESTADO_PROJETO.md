# Relatório de Estado do Projeto — ArtCraft Skills

- **Data**: 2026-11-06
- **Repositório**: `/home/luis/development/artcraft-skills` (branch `dev`)
- **Fonte**: verificação direta do código/artefatos nesta sessão + `OBJETIVO.md`/`ROADMAP.md` (estado verificado 2026-11-06)
- **Escopo**: resposta às perguntas do fluxo MDMV (`/queue` estado do projeto). Não altera contratos de código; factual e ancorado em evidência.

---

## 1. O que é esse projeto

Ecossistema open-source de **skills composíveis** para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io), com o objetivo de transformar *prompting* em *crafting* intencional (construir antes de gerar, controle composável).

É a **camada skill/agente** sobre superfícies reais dos apps ArtCraft (organização `storytold`: PhotoCraft, PdfCraft e outros “Crafting Apps”) via **CLI** e **MCP server**, além do AI studio da ArtCraft. **Não** reimplementa motores/provedores de geração, **não** tem backend próprio e **não** substitui os apps ArtCraft.

## 2. O que ele faz, na prática

Lista funcional concreta (símbolos exatos, verificados no código):

- **Descoberta de CLI**: `discover_cli` em `skills/core/artcraft_app_client.py` (adapter `__version__ 0.3.0`).
- **Invocação CLI**: `run_cli`, `run_cli_generation`, `discover_cli_commands`, `discover_generation_command`.
- **Fallback de geração por edição**: `generate_via_editing_commands` (usa comandos de edição como `paint.bucket`/`edit.fill`/`paint.stroke` para pixel art simples quando aplicável).
- **MCP stdio mínimo viável (006)**: `mcp_tools_list` (`tools/list`) e `mcp_tools_call` (`tools/call`) em `skills/core/artcraft_app_client.py`; JSON-RPC newline-delimited no stdout, diagnósticos no stderr, bounded timeout, request-id correlation, safe subprocess cleanup.
- **Normalização para contrato `SkillResult`** (`success`, `data`, `error`, `metadata`) — sem alterar schemas públicos (`skills/core/base_skill.py`).
- **Seleção de modo (FR-005)**: `select_mode(requested_mode, cli_available, mcp_available)`; modo explícito vence; `mode=mcp` **não** rerouteia silenciosamente para CLI/fallback; `auto` preserva **CLI-first/back-compat** quando CLI disponível.
- **Reason codes aditivos (FR-006)**: `REASON_CLI_NOT_FOUND`, `REASON_MCP_UNAVAILABLE`, `REASON_MCP_MISCONFIGURED`, `REASON_MCP_STARTUP_TIMEOUT`, `REASON_MCP_CALL_TIMEOUT`, `REASON_MCP_INVALID_RESPONSE`, `REASON_MCP_MISSING_CAPABILITY`, `REASON_MCP_TOOL_ERROR`, `REASON_NEITHER_AVAILABLE`, `REASON_IS_ERROR`.
- **`CreativeSkill`** (`skills/core/creative_skill.py`): fluxo discover → resolve → invoke → normalize → degrade; retry máximo 3 + exponential backoff + jitter; `threading.BoundedSemaphore(3)`.
- **Composição e orquestração**: `SkillComposer` (`compose` sequencial, `compose_parallel`) em `skills/core/composer.py`; `DAGOrchestrator` (DAG com detecção de ciclo e execução por ondas) em `skills/core/orchestrator.py`.
- **Validação de skills (agentskills.io)**: `scripts/validate_skill.py`, `scripts/validate_all_skills.py`.
- **Manifests `SKILL.md` localizados** (glob `skills/**/SKILL.md`, nesta sessão): **14** manifests — 5 creative (`mesh-generate`, `background-remove`, `image-edit`, `image-upscale`, `image-generate`), 5 workflow (`dag-orchestrator`, `orchestrator`, `structured-packager`, `policy-redaction`, `evidence-audit`), 2 integration (`scene-composition`, `2d-to-3d-workflow`), 2 core (`example-skill`, `template`). A contagem **validada** reportada pelo validador/gates é **12/12** (ver seção 4); qualquer divergência entre contagem de manifests e validação deve ser conferida na execução via `python scripts/validate_all_skills.py`.

## 3. Estado atual do repositório

- **Branch**: `dev` (checkout local). `main` local existe. Remotos: `origin/dev`, `origin/main`, `origin/HEAD -> origin/dev`.
- **HEAD (apurado nesta sessão)**: `44b9667 docs(specs): reconcile 006-integracao task markers and disambiguate 006 numbering`.
- **Histórico recente** (5): `44b9667`, `c26adf3 docs(readme): add root onboarding README with verified status and limits`, `d592d17 docs(roadmap): update 2026-11-06 roadmap with verified progress and next steps`, `d940717 docs(objetivo): update verified 2026-11-06 status and scoped gaps`, `d62e5e0 chore(merge): integrate 007 PhotoCraft MCP smoke PR stack (#131-#135) into dev`.
- **PRs abertos**: nenhum esperado (apenas `dev`/`main`, sem branches feature). `gh` disponível em `/usr/bin/gh` — verificar com `gh pr list --state open` na execução. **Higiene de branches**: conforme (apenas `dev` e `main`).
- **Working tree (apurado nesta sessão)**: 4 arquivos modificados (`OBJETIVO.md`, `ROADMAP.md`, `specs/006-mcp-stdio-functional-integration/quickstart.md`, `specs/007-photocraft-mcp-smoke/quickstart.md`) e 1 não rastreado (`docs/research/2026-11-06-ecosystem-research-update.md`). *Revisar individualmente antes de qualquer commit (P6 do plano).*
- **`.gitignore`**: cobre `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.hypothesis/`, `.codegraph/`, `.archify/`, `.omp/plans/` (sem adições necessárias nesta verificação).
- **Ferramentas MDMV/auxiliares**: `codegraph` CLI encontrado em `/home/luis/.local/bin/codegraph` e `gh` em `/usr/bin/gh`; `/init`/`/archify` do fluxo MDMV não têm equivalente direto de reindexação/diagramas neste repositório. Estado mapeado por leitura direta.

## 4. O que exatamente FUNCIONA (verificado)

- **Testes default**: **412 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`, integração opt-in excluída por padrão via `pytest.ini: -m "not integration"`). [Fonte: `OBJETIVO.md`/`ROADMAP.md` verificados 2026-11-06; re-executar na execução se qualquer código em `skills/` for modificado.]
- **Validação de skills (agentskills.io)**: **12/12, `all_valid=True`** (`python scripts/validate_all_skills.py`). [Fonte: gates verificados 2026-11-06.]
- **Adapter 006 (MCP stdio mínimo viável)**: transporte `tools/list`/`tools/call`, normalização para `SkillResult`, reason codes/taxonomia FR-006 aditiva, seleção FR-005 preservada. `photocraft-cli 0.20.1` observado localmente retornando **26 MCP tools** via `tools/list`; `command_list` com engine command metadata (`file.new`, `edit.fill`, `paint.stroke`, `file.export.quickExport`, `layer.exportAs`, `doc.export`). [Fonte: `OBJETIVO.md`, evidência 007 quickstart.]
- **007 Option A (stateless, opt-in, test-only)**: evidência local autorizada de `tools/list` + `tools/call name=command_list` — capability presente, resultado não-erro/normalizável; **stateless, sem reuso de sessão, sem ciclo de artefato cross-call**. Smoke MCP real **nunca em CI/default**. Repositório público `storytold/photocraft` e docs MCP existem (ver P5); operação real continua dependente de binário/ambiente local autorizado e escopo verificado. [Fonte: `specs/007-photocraft-mcp-smoke/quickstart.md`, pesquisa P5.]
- **Resiliência**: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)` em `CreativeSkill`.
- **Specs convergidos (escopo definido)**: 001, 003, 004, 005 (evidência de resiliência), 006-MCP stdio funcional, 007 PhotoCraft MCP smoke Option A (T001–T023).

## 5. O que deveria, mas não funciona / gaps (não exercido ou pendente)

- **007 Option B (stateful MCP)**: ciclo `doc_new → command → doc_export` em sessão retida — **adiada, spec separada** (não implementada no adapter atual).
- **Decisão MCP SDK v2** (`modelcontextprotocol/python-sdk` v2.3.0, fala revisão 2026-07-28) vs cliente mínimo atual — **pendente** (manter mock-first/back-compat).
- **Mapeamento profundo de capacidades PhotoCraft** (ferramentas, raízes, progresso, cancelamento, semântica de erro) — **pendente** (candidato 80/20, P7–P8).
- **Job CI/manual opcional** para smoke MCP real — **não implementado** (nunca default).
- **Domínios Phases 3–5** (vídeo/motion, áudio/voz/docs, CAD/precisão) — **não iniciados**.
- **Higiene Speckit residual**: `005-resiliencia-creativeskill` checkboxes parcialmente marcados vs evidência de convergência (reconciliar); ambiguidade de numeração `006-integracao-geracao-assets` vs `006-mcp-stdio-functional-integration` (doc hygiene parcial já aplicada).
- **Produto/adoção**: matriz de compatibilidade (Crafting Apps × MCP × versões) pendente.

## 6. O que ainda não está implementado

- Phases 3–5 do `ROADMAP.md` (vídeo/motion/animação; áudio/voz; documentos/apresentações; CAD/precisão/técnico).
- Sessão MCP stateful / ciclo de artefato cross-call (007 Option B).
- Job CI seguro, **nunca default**, para smoke MCP real com gestão segura de binário/evidência.
- Matriz de compatibilidade (Crafting Apps/MCP/versões de protocolo).
- Diagramas Archify de arquitetura (backlog separado `codegraph-archify-diagrams`).
- Root `README.md` e onboarding — **já adicionados** (commit `c26adf3`); verificar completude na execução.

## 7. O que este projeto NÃO faz

- Não reimplementa modelos/provedores de geração nem backend próprio; não substitui apps ArtCraft.
- Não executa smoke MCP real em **CI/default**; exige opt-in + autorização explícita + controles de segurança.
- Não prova/implementa geração IA via caminho local PhotoCraft MCP (007 = automação **engine/editor stateless**), nem roteamento provider/modelo/prompt nesse caminho.
- Não implementa sessão MCP stateful/ciclo determinístico de artefato cross-call (Option B adiada).
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos; ausência de execução autorizada = **não exercido/não atestado**.
- Não fabrica evidência; reivindicações devem corresponder ao escopo verificado.
- Não afirma suporte a MCP server-initiated requests (roots/sampling/logging/ping) na revisão 2026-07-28 sem evidência de implementação.

## 8. Andamento Speckit (resumo)

- **Assessments** (`.specify/assessments/`, 7): `artcraft-skills-suite-intake`, `shared-cli-mcp-adapter`, `implement-python-creative-skills`, `resiliencia-creativeskill`, `mcp-stdio-functional-integration`, `integracao-geracao-assets`, `photocraft-mcp-verified-smoke` — todos com intake/problem/research/concept/decision (ou decide).
- **Specs** (`specs/`, 7): 001/003/004/005/006-mcp-stdio/006-integracao/007 — escopo definido/convergido conforme descrito; 007 Option B pendente.
- **`.specify/bugs`**: **não existe** como diretório (fato verificado; existe `.specify/extensions/bug/`). Bugs via GitHub issues (remoto) — verificar na execução se necessário.

---

*Relatório gerado no contexto do plano `local://mdmv-fluxo-artcraft-skills-plan.md` (P4). Atualizar `OBJETIVO.md`/`ROADMAP.md` em P6 com base em P5 (pesquisa externa).*
