# Objetivo do Projeto

## Visão Geral

ArtCraft Skills Suite tem como objetivo construir um ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O projeto capacita artistas, designers e criadores a transformar prompts em *crafting* intencional, com controle preciso e fluxos compostos em vez de geração *one-shot*.

As skills não reimplementam motores de geração: expõem, de forma composável e governada, capacidades reais dos apps ArtCraft (PhotoCraft, PdfCraft e demais “Crafting Apps” Rust da organização `storytold`) via superfícies de **CLI** (`photocraft-cli`, 500+ comandos) e **MCP server**, além do AI studio da ArtCraft. O repositório é a *camada de skill/agente* sobre essas superfícies.

## Estado Atual (Verificado — 2026-11-06)

- **Branch:** `dev` (sincronizado com `origin/dev`, merge `d62e5e0` integrando stack 007 #131–#135). Remoto/local: apenas `dev` e `main`. Sem PRs abertos.
- **Gates padrão (verificados):** **421 passed, 23 deselected** (`PYTHONPATH=. python -m pytest -q`); **12/12 skills validadas** (`python scripts/validate_all_skills.py`). Testes `@pytest.mark.integration` ficam excluídos por padrão (`pytest.ini: -m "not integration"`).
- **Convergência Speckit (escopo definido):** 001, 003, 004, 005 (resiliência) e 006-MCP stdio funcional convergidos com evidência em `specs/*`. **007 PhotoCraft MCP Verified Local Smoke (Option A, stateless)** concluído/convergido (T001–T023): harness *test-only* opt-in, mock-first preservado, **SC-001 exercido sob autorização explícita** no ambiente local (escopo limitado, engine/editor; sem IA/provider/model), com evidência em `specs/007-photocraft-mcp-smoke/quickstart.md`.
- **Conformidade agentskills.io:** 12/12 skills validadas com `SKILL.md` frontmatter YAML (name kebab-case 1–64 chars, description 1–1024 chars), progressive disclosure (~100 tokens metadata, <5000 tokens instruções), scripts/ e references/ opcionais. Fonte: https://agentskills.io/specification.
- **MCP:** transporte stdio mínimo viável implementado em `skills/core/artcraft_app_client.py` (`__version__ 0.4.0`, aditivo 009: `mcp_stateful_session`/`MCPStatefulSession` com subprocesso retido, preservando APIs stateless 006) com `tools/list` e `tools/call`, JSON-RPC newline-delimited, stdout apenas protocolo, bounded timeout, request-id correlation, safe subprocess cleanup, FR-005 (seleção de modo) e FR-006 (reason codes aditivos). Compatível com MCP 2025-11-25 e alinhado com a revisão 2026-07-28 (_meta obrigatório, server/discover, sem handshake/sessão na nova revisão). Fontes: https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md, https://py.sdk.modelcontextprotocol.io/v2/whats-new/.
- **MCP Python SDK avaliado:** `modelcontextprotocol/python-sdk` v2 (v2.3.0 atual, v2.0.0 estável desde 2026-07-28) fala a revisão 2026-07-28 e serve ambas as revisões (2025-11-25 e 2026-07-28) simultaneamente; cliente mínimo atual do adapter preservado por back-compat/mock-first. Fonte: https://py.sdk.modelcontextprotocol.io/v2/whats-new/.
## O que funciona (verificado)

- Schema/validação/descoberta/carregamento agentskills.io, core abstractions, composição (`SkillComposer`) e DAG (`DAGOrchestrator`).
- Adapter compartilhado `skills/core/artcraft_app_client.py`: discovery/invocação CLI, transport MCP stdio mínimo (`tools/list`/`tools/call`) com normalização para `SkillResult`, reason codes/taxonomia FR-006 aditiva, seleção FR-005 (explícito `mcp` sem reroute silencioso; `auto` preserva CLI-first/back-compat), fallback de edição (`generate_via_editing_commands`).
- `CreativeSkill` resiliente: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)`.
- 5 skills criativas Python executáveis: `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate`; `scene-composition` executável; workflows generalizáveis.
- **Adapter `artcraft_app_client` normaliza resultados MCP `content[].text` / `structured` para `SkillResult`, com `standardize_error` (FR-006) e `isError` propagation.**
- **PhotoCraft `photocraft-cli 0.20.1` observado localmente retornando 26 MCP tools (`command_list`, `command_run`, `command_batch`, `doc_new/open/save/export/inspect/render_preview`, `jobs_*`, `session_list`, UI/bridge) via `tools/list` e `command_list` com engine command metadata (`file.new`, `edit.fill`, `paint.stroke`, `file.export.quickExport`, `layer.exportAs`, `doc.export`).**
- **Operacionalização opcional controlada:** job/manual para smoke MCP real em ambiente autorizado (nunca default), com gestão segura de binário/evidência. Binário `photocraft-cli` resolvido via `ARTCRAFT_MCP_PHOTOCRAFT_BIN` (absoluto, preferido) ou PATH apenas em modo opt-in; identidade/versão registradas quando disponíveis.
- **009 / 007 Option B (aditivo, mock-first, 2026-11-06):** helper de sessão MCP stateful (`mcp_stateful_session`/`MCPStatefulSession`, subprocesso stdio retido, ids correlacionados, cleanup bounded, FR-006-aligned) implementado com testes determinísticos; preserva 006 stateless/FR-005/FR-006/schemas. **Ciclo real de artefato PhotoCraft permanece opt-in autorizado** (007/008, capability-gated). MCP 2026-07-28: client-retained process state; sem assumir sessão server-side. **Sem** geração IA, **sem** bridge/UI, **sem** CI/default real.
- **Mapeamento MCP por capacidade real** (PhotoCraft/outros Crafting Apps): ferramentas PhotoCraft documentadas: `command_list` (filter, enabled_only), `command_run` (id, params, wait), `command_batch` (steps, stop_on_error), `doc_inspect`, `render_preview` (index, max_side ≤ 2048), `doc_export_layers`/`doc_export_data_sets` (recusam overwrite), roots de leitura/escrita com autoridade de filesystem, progresso via `_meta.progressToken` (0–1, ≤10/s), cancelamento via `notifications/cancelled`. Sem reivindicar geração IA indevida.
- **Decisão de dependência MCP (quando necessário):** SDK v2.3.0 disponível (`pip install mcp` instala 2.x); avaliar migração do cliente mínimo para `mcp.Client` + `StdioServerParameters` vs manter cliente mínimo atual para lifecycle/auth remota/Streamable HTTP/compatibilidade ampliada; manter mock-first/back-compat.
- **Documentar alinhamento com MCP 2026-07-28** (_meta obrigatório, server/discover, sem _Mcp-Session-Id_ no 2026 path, subscriptions/listen substitui resources/subscribe) nos specs e quickstart do 006/007.
- **Criar diagrama(s) Archify (HTML standalone)** documentando arquitetura, classe, sequência MCP stdio, dataflow e workflow do CreativeSkill (pendente de plano separado `codegraph-archify-diagrams`).
- **Backlog Speckit:** `specs/005-resiliencia-creativeskill` tem checkboxes de implementação parcialmente marcados (evidência de convergência existe — reconciliar); `specs/006-integracao-geracao-assets` (0/11) permanece backlog/numeração ambígua com `006-mcp-stdio-functional-integration` — normalizar referências sem reescrever histórico.
- **Expansão de domínios (Phases 3–5):** vídeo/motion/animação; áudio/voz/docs/apresentações; CAD/precisão/técnico.
- **Produto/adoção:** `README.md` raiz, exemplos reais, onboarding CLI/MCP, matriz de compatibilidade (Crafting Apps/MCP).
  

## O que este projeto NÃO faz

- Não reimplementa modelos/provedores de geração nem backend próprio; orquestra superfícies reais ArtCraft.
- Não substitui os apps ArtCraft.
- **Não executa smoke MCP real em CI/default**; exige opt-in + autorização explícita + controles de segurança.
- **Não prova/implementa geração IA** via PhotoCraft MCP local (007 = automação engine/editor stateless), nem roteamento provider/modelo/prompt nesse caminho.
- **Não implementa** sessão MCP stateful/ciclo de artefato cross-call (Option B adiada).
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos.
- Não fabrica evidência (ausência de execução autorizada = não exercido/não atestado).
- Não afirma suporte a MCP server-initiated requests (roots/sampling/logging/ping) na revisão 2026-07-28; esses foram removidos ou deprecated.
- Não garante interoperabilidade com PhotoCraft bridge mode (UI tools, desktop app, control token) além do escopo stateless headless.

## Métricas (verificadas)

- ✅ **421/421** testes default passando, **23** deselected (integração opcional)
- ✅ **12/12** skills validadas (agentskills.io)
- ✅ 001/003/004/005/006-MCP convergidos (escopo definido)
- ✅ 007 convergido (Option A stateless); SC-001 exercido localmente sob autorização (escopo limitado)
- ✅ Adapter alinhado com MCP 2025-11-25 e revisão 2026-07-28 (_meta, server/discover, sem handshake na nova revisão)
- ✅ 009 stateful session helper aditivo (007 Option B, mock-first) — ✓; ciclo real de artefato opt-in pendente
- ⏳ Avaliação MCP SDK v2 (modelcontextprotocol/python-sdk v2.3.0) — backlog, decisão pendente

## Pesquisa de ecossistema externa (2026-11-06)

- **agentskills.io**: especificação confirma `SKILL.md` com frontmatter YAML (`name` kebab-case 1–64, `description` 1–1024) + Markdown; progressive disclosure; estrutura com `scripts/`/`references/`/`assets/` opcionais. Alinhamento do repo: **12/12 skills validadas**. Fonte: https://agentskills.io/specification (acesso 2026-11-06).
- **MCP Python SDK / protocolo**: `modelcontextprotocol/python-sdk` **v2.3.0** (2026-10-02) fala a revisão **2026-07-28** e serve 2025-11-25 e 2026-07-28; `server/discover` e mudanças de negociação/_meta na 2026-07-28. Decisão de migração do cliente mínimo (006) para SDK v2 permanece backlog (mock-first/back-compat). Fontes: https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0, https://modelcontextprotocol.io/specification/2026-07-28/changelog (acesso 2026-11-06).
- **PhotoCraft (`storytold/photocraft`)**: **evidência pública** do repositório/docs MCP (`docs/mcp.md`, `book/src/automation/mcp.md`) confirmada em pesquisa; operação real continua dependente de binário/ambiente local autorizado e do escopo verificado (006/007, engine/editor stateless, sem claim de geração IA). Fontes: https://github.com/storytold/photocraft (acesso 2026-11-06).
- **Artefatos desta rodada (fluxo MDMV, plano `local://mdmv-fluxo-artcraft-skills-plan.md`)**: `docs/RELATORIO_ESTADO_PROJETO.md`, `docs/research/2026-11-06-pesquisa-externa-ecossistema.md`, `docs/AVALIACAO_ANDAMENTO_SPECKIT.md` (P9), spec 80/20 `008-photocraft-capability-mapping` (P7–P8, em especificação).

