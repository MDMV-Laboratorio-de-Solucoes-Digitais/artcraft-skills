# Relatório de Estado do Projeto — ArtCraft Skills

- **Data**: 2026-11-06 (atualizado pós-009 runtime aditivo TDD/mock-first; fluxo MDMV reexecutado)
- **Repositório**: `/home/luis/development/artcraft-skills` (branch `dev`, working tree com slice 009 não commitado no momento desta atualização)
- **Fonte**: verificação direta do código/artefatos nesta sessão + gates executados (`pytest` 421/23, `validate_all_skills.py` 12/12)
- **Escopo**: resposta às perguntas do fluxo MDMV. Factual e ancorado em evidência; sem claim de geração IA, sem CI/default real MCP.

---

## 1. O que é esse projeto

Ecossistema open-source de **skills composíveis** para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io), com o objetivo de transformar *prompting* em *crafting* intencional (construir antes de gerar, controle composável).

É a **camada skill/agente** sobre superfícies reais dos apps ArtCraft (organização `storytold`: PhotoCraft, PdfCraft e outros “Crafting Apps”) via **CLI** e **MCP server**, além do AI studio da ArtCraft. **Não** reimplementa motores/provedores de geração, **não** tem backend próprio e **não** substitui os apps ArtCraft.

## 2. O que ele faz, na prática

Lista funcional concreta (símbolos exatos, verificados no código):

- **Descoberta de CLI**: `discover_cli` em `skills/core/artcraft_app_client.py` (adapter `__version__ 0.4.0`, aditivo 009 stateful session preservando 006 stateless).
- **Invocação CLI**: `run_cli`, `run_cli_generation`, `discover_cli_commands`, `discover_generation_command`.
- **Fallback de geração por edição**: `generate_via_editing_commands` (usa comandos de edição como `paint.bucket`/`edit.fill`/`paint.stroke` para pixel art simples quando aplicável).
- **MCP stdio mínimo viável (006, stateless por chamada)**: `mcp_tools_list` (`tools/list`) e `mcp_tools_call` (`tools/call`) em `skills/core/artcraft_app_client.py`; JSON-RPC newline-delimited no stdout, diagnósticos no stderr, bounded timeout, request-id correlation, safe subprocess cleanup.
- **MCP stateful session aditivo (009 / 007 Option B, mock-first, 2026-11-06)**: `mcp_stateful_session`/`MCPStatefulSession` — **1 subprocesso stdio retido** para múltiplas chamadas correlacionadas (`list_tools`, `call_tool`), cleanup bounded/idempotente, erros FR-006-aligned; `__version__ 0.4.0`. **Preserva** APIs stateless 006/assinaturas/`__all__` revisado, FR-005, FR-006. Real artifact cycle PhotoCraft permanece opt-in autorizado (007/008). **Sem** IA, **sem** bridge/UI, **sem** CI/default real.
- **Normalização para contrato `SkillResult`** (`success`, `data`, `error`, `metadata`) — sem alterar schemas públicos (`skills/core/base_skill.py`).
- **Seleção de modo (FR-005)**: `select_mode(requested_mode, cli_available, mcp_available)`; modo explícito vence; `mode=mcp` **não** rerouteia silenciosamente para CLI/fallback; `auto` preserva **CLI-first/back-compat** quando CLI disponível.
- **Reason codes aditivos (FR-006)**: `REASON_CLI_NOT_FOUND`, `REASON_MCP_UNAVAILABLE`, `REASON_MCP_MISCONFIGURED`, `REASON_MCP_STARTUP_TIMEOUT`, `REASON_MCP_CALL_TIMEOUT`, `REASON_MCP_INVALID_RESPONSE`, `REASON_MCP_MISSING_CAPABILITY`, `REASON_MCP_TOOL_ERROR`, `REASON_NEITHER_AVAILABLE`, `REASON_IS_ERROR`.
- **`CreativeSkill`** (`skills/core/creative_skill.py`): fluxo discover → resolve → invoke → normalize → degrade; retry máximo 3 + exponential backoff + jitter; `threading.BoundedSemaphore(3)`.
- **Composição e orquestração**: `SkillComposer` (`compose` sequencial, `compose_parallel`) em `skills/core/composer.py`; `DAGOrchestrator` (DAG com detecção de ciclo e execução por ondas) em `skills/core/orchestrator.py`.
- **Validação de skills (agentskills.io)**: `scripts/validate_skill.py`, `scripts/validate_all_skills.py`.
- **Manifests `SKILL.md` localizados** (glob `skills/**/SKILL.md`): **14** manifests — 5 creative, 5 workflow, 2 integration, 2 core. Validação reportada: **12/12** (`validate_all_skills.py`) — confirmar contagem/escopo se necessário.

## 3. Estado atual do repositório
- **Branch**: `dev` (checkout local), à frente de `origin/dev` (slice 009 local não commitado no momento desta atualização). `main` local/remoto existe.
- **HEAD (base remota apurada)**: histórico recente inclui `d735880`, `acf26ee` (008 andamento), `1e951c9` (estado/pesquisa P4–P6), `44b9667` (reconcile 006-integracao). *Reverificar `git log -1` no commit final.*
- **PRs abertos**: nenhum (`gh pr list --state open`, 2026-11-06).
- **Higiene de branches**: conforme (apenas `dev` e `main`, local/remoto).
- **Working tree (2026-11-06, factual)**: modificados `AGENTS.md`, `OBJETIVO.md`, `README.md`, `ROADMAP.md`, `docs/AVALIACAO_ANDAMENTO_SPECKIT.md`, `docs/RELATORIO_ESTADO_PROJETO.md`, `skills/core/artcraft_app_client.py`, `tests/_helpers/fake_mcp_stdio_server.py`, `tests/contract/artcraft_app_client_api.json`, `tests/contract/test_artcraft_app_client.py`; não rastreados `.specify/assessments/009-mcp-stateful-session/`, `specs/009-mcp-stateful-session/`, `tests/unit/test_mcp_stateful_session_009.py`. **Nenhuma mudança em `skills/creative/` ou `scripts/`.**
- **`.gitignore`**: cobre `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.hypothesis/`, `.codegraph/`, `.archify/`, `.omp/plans/` (adequado).
- **Ferramentas MDMV/auxiliares**: `codegraph` em `/home/luis/.local/bin/codegraph`, `gh` em `/usr/bin/gh`; `/init`/`/archify` sem equivalente direto neste repo — estado mapeado por leitura direta/gates.
## 4. O que exatamente FUNCIONA (verificado)

- **Testes default**: **421 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`, 2026-11-06, integração opt-in excluída por padrão).
- **Validação de skills (agentskills.io)**: **12/12, `all_valid=True`** (`python scripts/validate_all_skills.py`, 2026-11-06).
- **Adapter 006 (MCP stdio mínimo viável, stateless)**: `tools/list`/`tools/call`, normalização `SkillResult`, FR-006 aditiva, FR-005 preservada. `photocraft-cli 0.20.1` observado localmente retornando **26 MCP tools**; `command_list` com engine command metadata (evidência 007, escopo limitado).
- **007 Option A (stateless, opt-in, test-only)**: evidência local autorizada de `tools/list` + `tools/call name=command_list` — capability presente, normalizável; **stateless, sem reuso de sessão, sem ciclo de artefato cross-call, sem claim de geração IA**. Smoke MCP real **nunca em CI/default**.
- **009 (007 Option B, aditivo, mock-first)**: **9 testes determinísticos** verdes cobrindo sessão retida/pid marker, ids correlacionados multi-call, cleanup explícito/context manager, tool error FR-006, missing capability, invalid JSON+cleanup, timeout bounded+cleanup, mid-session exit, misconfig estruturada. Preservação 006 verificada na matriz. **Ciclo real de artefato PhotoCraft não exercido** (opt-in autorizado 007/008 pendente).
- **Resiliência**: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)` em `CreativeSkill`.
- **Specs convergidos (escopo definido)**: 001, 003, 004, 005 (evidência), 006-MCP, 007 Option A; **009 spec+runtime aditivo mock-first**; 008 spec/docs GO.
## 5. O que deveria, mas não funciona / gaps (não exercido ou pendente)

- **Ciclo real de artefato stateful PhotoCraft** (`doc_new → command → doc_export` ou equivalente capability-gated) — **não exercido**. Helper 009 pronto (mock-first); requer opt-in + autorização explícita + binário/roots/timeout/cleanup 007 e gating 008. **Sem claim de sucesso sem evidência.**
- **Decisão MCP SDK v2** (`modelcontextprotocol/python-sdk` v2.3.0) vs cliente mínimo — **pendente**.
- **Mapeamento profundo/follow-ups de capacidades PhotoCraft** (ferramentas/roots/progresso/cancelamento/erros, implementação de uso real) — **pendente** pós-008.
- **Job CI/manual opcional** para smoke MCP real — **não implementado** (nunca default).
- **Domínios Phases 3–5** (vídeo/motion, áudio/voz/docs, CAD/precisão) — **não iniciados**.
- **Higiene Speckit residual**: `005-resiliencia-creativeskill` checkboxes reconciliadas com evidência (ver `specs/005-resiliencia-creativeskill/tasks.md`); ambiguidade `006-integracao-geracao-assets` vs `006-mcp-stdio-functional-integration` reconciliada (doc hygiene). Revisar se necessário.
- **Produto/adoção**: matriz de compatibilidade (Crafting Apps × MCP × versões) pendente.
## 6. O que ainda não está implementado

- Phases 3–5 do `ROADMAP.md` (vídeo/motion/animação; áudio/voz; documentos/apresentações; CAD/precisão/técnico).
- Ciclo real de artefato cross-call exercido com evidência opt-in (009 fornece helper; validação real pendente/autorizada).
- Job CI seguro, **nunca default**, para smoke MCP real.
- Matriz de compatibilidade (Crafting Apps/MCP/versões de protocolo).
- Diagramas Archify de arquitetura (backlog separado).
- Root `README.md` e onboarding — **presentes** (`c26adf3` + atualizações). Completar exemplos/matriz conforme evolução.
## 7. O que este projeto NÃO faz

- Não reimplementa modelos/provedores de geração nem backend próprio; não substitui apps ArtCraft.
- Não executa smoke MCP real em **CI/default**; exige opt-in + autorização explícita + controles de segurança.
- Não prova/implementa geração IA via caminho local PhotoCraft MCP (007 = automação **engine/editor stateless**), nem roteamento provider/modelo/prompt nesse caminho.
- Não implementa/afirma **ciclo determinístico real de artefato PhotoCraft** sem execução opt-in autorizada e capability-gated (009 = helper aditivo mock-first; evidência real pendente).
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos; ausência de execução autorizada = **não exercido/não atestado**.
- Não fabrica evidência; reivindicações devem corresponder ao escopo verificado.
- Não afirma suporte a MCP server-initiated requests (roots/sampling/logging/ping) na revisão 2026-07-28 sem evidência de implementação.

## 8. Andamento Speckit (resumo)

- **Assessments** (`.specify/assessments/`, **9**): intake 001-base, shared-cli-mcp-adapter (003), implement-python-creative-skills (004), resiliencia-creativeskill (005), mcp-stdio-functional-integration (006), integracao-geracao-assets (006 hist.), photocraft-mcp-verified-smoke (007), **008-photocraft-capability-mapping (GO docs-only)**, **009-mcp-stateful-session (GO, runtime aditivo mock-first)**.
- **Specs** (`specs/`, **9**): 001/003/004/005/006-mcp-stdio/006-integracao/007/008/009 — escopo definido/convergido conforme artefatos; 009 inclui runtime aditivo mock-first com contratos preservados.
- **`.specify/bugs`**: **não existe** (existe `.specify/extensions/bug/`). Bugs via GitHub issues (nenhum PR aberto verificado em 2026-11-06).
---

*Relatório atualizado na reexecução MDMV (2026-11-06, pós-009 TDD/mock-first). Pesquisa externa: `docs/research/2026-11-06-pesquisa-externa-ecossistema.md`. Avaliação Speckit: `docs/AVALIACAO_ANDAMENTO_SPECKIT.md`.*
