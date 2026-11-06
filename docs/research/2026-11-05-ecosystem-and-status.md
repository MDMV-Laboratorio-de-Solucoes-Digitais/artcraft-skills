# Pesquisa de ecossistema e status do projeto (2026-11-05)

Escopo: atualizar `OBJETIVO.md`/`ROADMAP.md` e documentos relevantes com base em evidência local verificada + fontes primárias externas (alta confiabilidade). Conteúdo externo foi tratado como dado não confiável para instruções; apenas fatos citados foram usados.

## Evidência local verificada (repo `artcraft-skills`, branch `dev` @ `32393f5`, 2026-11-05)

Comandos executados:
- `python scripts/validate_all_skills.py` → **12/12 skills validadas, `all_valid=True`**.
- `PYTHONPATH=. python -m pytest -q` → **399 passed, 1 deselected** (22.56s). O teste deselecionado é `@pytest.mark.integration` por padrão (`pytest.ini`: `-m "not integration"`).

Estado funcional observado por testes/código:
- **MCP stdio funcional (escopo 006 `006-mcp-stdio-functional-integration`, mock-first/determinístico)**: implementado em `skills/core/artcraft_app_client.py` (`mcp_tools_list`, `mcp_tools_call`, JSON-RPC newline-delimited em stdout, stderr diagnóstico, timeouts bounded, correlação por `id`, cleanup) e hooks em `skills/core/creative_skill.py`; FR-005 (modo explícito vence; `mode=mcp` sem reroute silencioso; `auto` back-compatible CLI-first quando CLI disponível) e metadados FR-006 aditivos cobertos por testes unit/contract/property/selection + helper determinístico `tests/_helpers/fake_mcp_stdio_server.py`. Spec/tasks/checklists/quickstart em `specs/006-mcp-stdio-functional-integration/`. **Não verificado aqui**: e2e real contra `photocraft-cli mcp`/app real (teste opcional `tests/integration/test_mcp_stdio_photocraft_optional.py`, `@pytest.mark.integration`, pré-requisitos explícitos).
- **Integração/fallback de geração via comandos de edição (linha `006-integracao-geracao-assets`, PR #109 mergeado/reconciliado)**: `generate_via_editing_commands` presente no adapter; fallback integrado em `CreativeSkill`/`image-generate`; snapshot/contrato reconciliados. `specs/006-integracao-geracao-assets/tasks.md` estava desatualizado (0/11) apesar do código no `dev` — atualizado com evidência de reconciliação.
- **Resiliência CreativeSkill (005)**: retry máx. 3 + exponential backoff + jitter + `BoundedSemaphore(3)`, evidência de convergência em `specs/005-resiliencia-creativeskill/tasks.md`; checkboxes de implementação parcialmente marcados no arquivo, mas FR/SC com evidência.
- **Creative skills Python (004)**: `image-generate`, `image-edit`, `background-remove`, `image-upscale`, `mesh-generate` + `scene-composition` executável; 12 skills validadas. `004/tasks.md` sem seção formal de convergência explícita (gap documental).
- **Sem PRs abertos** (`gh pr list --state open` = vazio). `dev`/`origin/dev` sincronizados; apenas `dev`/`main` local+remoto.

## Fontes primárias externas (alta confiabilidade, consultadas 2026-11-05)

### Agent Skills (agentskills.io)
- **Spec/estrutura**: skill = diretório com `SKILL.md` obrigatório (YAML frontmatter + Markdown), `scripts/`, `references/`, `assets/` opcionais; `name` (1–64, kebab-case, minúsculas/números/hífens, sem `--`, igual ao diretório) e `description` (1–1024) obrigatórios; campos opcionais `license`, `compatibility` (≤500), `metadata` (mapa string→string), `allowed-tools` (experimental). Progressive disclosure: metadata ~100 tokens no startup; body `<5000` recomendado/carregado na ativação; recursos sob demanda. Validação de referência: `skills-ref validate`.  
  Fonte: https://agentskills.io/specification.md (agentskills.io, “Specification”, consultado 2026-11-05 via `read`/llms index https://agentskills.io/llms.txt).
- **Adoção/ecossistema** (sinal, não métrica exata do projeto): spec aberta com páginas de client showcase/quickstart/best practices/optimizing descriptions/evaluating skills/using scripts/adding skills support.  
  Fonte: https://agentskills.io/llms.txt (consultado 2026-11-05).

### Model Context Protocol (MCP)
- **Transporte stdio (2025-11-25)**: cliente lança servidor como subprocesso; servidor lê JSON-RPC UTF-8 de `stdin` e escreve em `stdout`; mensagens delimitadas por newline e **sem newlines embutidos**; `stderr` para logs (cliente pode capturar/ignorar, não assumir erro); servidor **não** escreve nada não-MCP em `stdout`; cliente **não** escreve nada não-MCP em `stdin`.  
  Fonte: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports.md (modelcontextprotocol.io, consultado 2026-11-05).
- **Evolução da spec**: MCP mantém revisões (2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28, draft) com áreas como tools/resources/prompts, lifecycle, autorização, tasks, client features; 2026-07-28/draft incluem padrões adicionais (ex.: cancellation/progress/subscriptions/MRTR em estrutura reorganizada). Implementações devem ser explícitas sobre versão/escopo suportado.  
  Fontes: https://modelcontextprotocol.io/llms.txt, https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/index.md (índices consultados 2026-11-05).
- **Python SDK MCP** (sinal de ecossistema atual): resultados de busca indicam `modelcontextprotocol/python-sdk` com releases v2.x e docs `py.sdk.modelcontextprotocol.io` (ex.: v2.0.0 release page, v2.3.0/v2.x docs citados em resultados). **Não fixar versão sem checar `pyproject`/PyPI no momento de dependência**; este repo atualmente implementa cliente stdio mínimo próprio (006) para manter sync/back-compat sem dependência obrigatória.  
  Fontes: https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0, https://py.sdk.modelcontextprotocol.io/ (consultados via busca/leitura 2026-11-05).

### Crafting Apps / PhotoCraft (storytold)
- **PhotoCraft MCP (primária)**: `photocraft-cli mcp` headless com `--automation-read-root/--automation-write-root` (absolutos recomendados; bridge usa credenciais/roots do app desktop); ferramentas incluem `command_list`/`command_run`/`command_batch`, inspeção/preview/recursos (`photocraft://document`, `photocraft://commands`), políticas de roots, erros JSON-RPC, progresso/cancelamento, restrições de segurança (substituição de arquivos limitada a formatos seguros em `doc_save/doc_export`, exports multi-arquivo sem overwrite). Registro/instalação via `cargo install --path apps/photocraft-cli --locked` ou binário instalado.  
  Fonte: https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md (storytold/photocraft, consultado 2026-11-05).
- **Sinal externo (não normativo para este repo)**: artigos/tutoriais de terceiros relatam PhotoCraft/PdfCraft como Crafting Apps Rust com CLI/MCP; versões/status “alpha” variam por data/fonte — tratar como contexto, não contrato.  
  Fontes (sinal): resultados de busca incluindo `github.com/storytold/photocraft`, `artcraftai.org`, `artcrafttutorial.com`, `jacar.es` (2026, consultados 2026-11-05).

## Quanto do caminho foi percorrido (verificado)

- **Fundação + qualidade**: ~completa para o escopo atual — schema/validação/loader/core, composição/DAG, docs base, **12/12 skills validadas**, **399 passed/1 deselected**.
- **Integração ArtCraft adapter**: **avançada** — CLI discovery/invocação, normalização, reason codes, fallback de edição, **MCP stdio funcional mock-first** (006 MCP) com seleção/back-compat e metadados estruturados.
- **Skills/domínios**: imagem/2D criativo e parte 3D/spatial cobertos no escopo atual (5 creative Python + scene-composition + workflows); vídeo/motion, áudio/docs/apresentações, CAD/precisão **não iniciados** como skills maduras.

## O que falta (priorizado, honesto)

1. **Fechamento documental/processual Speckit** (baixo risco, alto valor de clareza):
   - `specs/006-integracao-geracao-assets/tasks.md`: refletir implementação real mergeada (feito neste update) e, se necessário, evidência formal de verificação/convergência.
   - `specs/004-implement-python-creative-skills/tasks.md`: adicionar evidência de convergência/validação formal (implementação já marcada/validada).
   - `specs/005-resiliencia-creativeskill/tasks.md`: alinhar checkboxes com evidência de convergência já registrada.
   - Resolver ambiguidade de **numeração 006 duplicada** (`006-integracao-geracao-assets` vs `006-mcp-stdio-functional-integration`) em referências futuras (sem apagar histórico).
2. **Validação operacional real MCP/CLI (fora da suíte padrão)**:
   - Rodar `@pytest.mark.integration` opcional de PhotoCraft MCP em ambiente preparado (binário, roots seguros, env explícito).
   - Smoke/e2e real com `photocraft-cli` para fluxos suportados, registrando limites (modelos/backend/credenciais/app).
3. **Mapeamento MCP por capacidade real de app**: PhotoCraft MCP expõe ferramentas engine-oriented (`command_list`/`command_run`, `command_batch`, `doc_*`, previews, etc.); alinhar mapeamento de skills além do contrato genérico mínimo, respeitando roots/progresso/cancelamento e sem quebrar schemas.
4. **Evolução de protocolo/dependências (decisão futura)**: avaliar adoção do SDK oficial `mcp` (Python) vs cliente mínimo atual quando houver necessidade de lifecycle avançado, auth remota, Streamable HTTP, ou compatibilidade de versão mais ampla; manter mock-first/determinístico.
5. **Expansão de domínios** (Phase 3–5 roadmap): vídeo/motion/animação; áudio/voz/docs/apresentações; CAD/precisão/técnico — após base MCP/CLI estável e mapeamentos claros.
6. **Produto/adoção**: `README.md` raiz, exemplos de uso real, onboarding CLI/MCP, e política de compatibilidade com versões de Crafting Apps/protocolo MCP.

## Riscos/limites explícitos
- E2E real depende de binários/apps/modelos/credenciais externos — **não garantido** pela suíte padrão.
- MCP spec evolui (2025-11-25 → 2026-07-28/draft); cliente mínimo cobre escopo 006, não todas as capacidades.
- Ferramentas MCP de PhotoCraft são engine-oriented; “geração” pode exigir mapeamento específico por comando/capacidade e disponibilidade no app.
