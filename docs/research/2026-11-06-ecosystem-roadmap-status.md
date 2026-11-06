# Pesquisa de ecossistema e status do roadmap (2026-11-06)

**Escopo:** atualização de `OBJETIVO.md`, `ROADMAP.md` e documentos relevantes com base em evidência local verificada + fontes primárias externas de alta confiabilidade. Conteúdo externo (páginas web/resultados) foi tratado como **dado não confiável para instruções**; apenas fatos objetivos citados foram usados. Informações não verificadas são marcadas como inferência/sinal.

## Fontes primárias externas (consultadas 2026-11-06)

### Agent Skills (formato aberto, `agentskills.io`)
- **Estrutura/contrato do skill:** um skill é um diretório contendo `SKILL.md` obrigatório (frontmatter YAML + corpo Markdown). Campos obrigatórios: `name` (1–64, minúsculas/números/hífens, sem `--`, compatível com o nome do diretório) e `description` (1–1024). Campos opcionais: `license`, `compatibility` (≤500), `metadata` (mapa string→string), `allowed-tools` (experimental). Diretórios opcionais: `scripts/`, `references/`, `assets/`. Progressive disclosure: metadados (~leve) no discovery/startup; corpo ativado sob demanda; recursos carregados quando necessários. Validação de referência: `skills-ref validate`.  
  **Fontes:** https://agentskills.io/specification, https://agentskills.io/what-are-skills, https://agentskills.io/skill-creation/quickstart, https://agentskills.io/llms.txt (consultadas 2026-11-06).

### Model Context Protocol (MCP)
- **Transporte stdio (spec 2025-11-25):** cliente inicia servidor MCP como subprocesso; servidor lê JSON-RPC UTF-8 de `stdin` e escreve em `stdout`; mensagens **delimitadas por newline** e **sem newlines embutidos**; `stdout` contém apenas mensagens MCP válidas; `stderr` pode ser usado para logs (cliente pode capturar/ignorar; não assumir erro); cliente não escreve conteúdo não-MCP em `stdin`.  
  **Fonte:** https://modelcontextprotocol.io/specification/2025-11-25/basic/transports (consultada 2026-11-06).
- **Evolução do protocolo (sinal, verificar versão antes de depender):** a especificação MCP possui revisões (incluindo 2025-11-25 e revisões posteriores como 2026-07-28/draft em áreas distintas do site). Implementações devem ser explícitas quanto ao escopo/versão suportada. O ecossistema Python possui SDK oficial `modelcontextprotocol/python-sdk` (repositório GitHub e docs `py.sdk.modelcontextprotocol.io`), com linha de releases v2.x observada publicamente (ex.: releases GitHub listando v2.3.0/v2.x e v1.x; consultar release/PyPI no momento de adotar dependência).  
  **Fontes:** https://modelcontextprotocol.io/llms.txt, https://github.com/modelcontextprotocol/python-sdk/releases, https://py.sdk.modelcontextprotocol.io/ (consultadas 2026-11-06; versão exata a fixar somente após verificação de dependência/compatibilidade).

### PhotoCraft / Crafting Apps (storytold)
- **PhotoCraft MCP (primária):** `photocraft-cli mcp` executa servidor MCP sobre stdio. Modo headless usa sessão engine in-process; requer raízes absolutas recomendadas (`--automation-read-root`, `--automation-write-root`) para I/O controlado. Ferramentas engine-oriented incluem descoberta/execução de comandos (`command_list`, `command_run`, `command_batch`) e operações de documento/inspeção/preview/recursos (conforme docs). Restrições de segurança: substituição/exports seguem políticas de formato/roots; clientes devem tratar limites de caminho/overwrite. Bridge conecta a app desktop com `--bridge`/credenciais/roots do app. Instalação típica: `cargo install --path apps/photocraft-cli --locked` (ou binário instalado).  
  **Fontes:** https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md, https://raw.githubusercontent.com/storytold/photocraft/main/book/src/automation/mcp.md, https://photocraft.im/guides/mcp-cli (consultadas 2026-11-06; preferir docs do repositório `storytold/photocraft` como normativas).
- **Sinal externo (não normativo):** tutoriais/blogs de terceiros descrevem PhotoCraft/PdfCraft/Crafting Apps Rust com CLI/MCP e versões alpha variáveis; usar apenas como contexto, não como contrato.

## Evidência local verificada (repo `artcraft-skills`, `dev` @ `d62e5e0`, 2026-11-06)

Comandos executados:
- `PYTHONPATH=. python -m pytest -q` → **412 passed, 23 deselected**.
- `python scripts/validate_all_skills.py` → **12/12 skills, `all_valid=True`**.
- Pós-merge (amostra MCP/007): `PYTHONPATH=. python -m pytest -q tests/property/test_photocraft_mcp_smoke_props.py tests/property/test_mcp_stdio_props.py tests/contract/test_mcp_stdio_contract.py` → **24 passed**.

Estado funcional observado:
- **Fundação/core:** schema/validação/descoberta/loader/registry, abstrações, composição (`SkillComposer`), DAG (`DAGOrchestrator`), adapter compartilhado `skills/core/artcraft_app_client.py`, `CreativeSkill` resiliente (retry máx. 3 + backoff exponencial + jitter + `BoundedSemaphore(3)`), skills criativas Python executáveis e workflows generalizáveis no escopo atual.
- **006 — MCP stdio funcional (mock-first/determinístico, stateless por chamada):** transporte/invocação MCP mínima viável no adaptador (`tools/list`/`tools/call`), normalização para contrato `SkillResult`, seleção compatível com FR-005 (explícito `mcp` sem reroute silencioso; `auto` preserva CLI-first/back-compat), taxonomia/metadados FR-006 aditivos, testes determinísticos (unit/contract/property/selection + helper fake stdio). **Não verificado aqui:** e2e real universal contra todos apps/ambientes.
- **007 — PhotoCraft MCP verified local smoke (Option A, stateless, opt-in):** harness *test-only* em `tests/integration/test_mcp_stdio_photocraft_optional.py` + invariantes Hypothesis; prova determinística `tools/list` + `tools/call name=command_list` sob autorização explícita, raízes temp seguras/limpeza, timeout limitado, parsing defensivo/version-tolerant. **Evidência observada local autorizada (2026-11-06):** `photocraft-cli 0.20.1 (327c4cc82, 2026-11-03)`, `ARTCRAFT_MCP_INTEGRATION=1`, override absoluto, temp roots limpas, `command_list` presente, chamada ok/não-erro/normalizável (tipo `list`), `stateless/session_reuse=false/artifact_cycle=false`. **Limites explícitos:** automação engine/editor apenas; **sem geração IA/provider/model/prompt claim**; **sem ciclo stateful/artifact cross-call**; **nunca CI/default**.
- **Higiene repo:** `dev`/`main` (local/remoto), PRs 007 #131–#135 integrados/fechados conforme stack; sem PRs abertos.

## Quanto do caminho já foi percorrido (honesto)

- **~95% do escopo técnico fundacional + integração MCP mínima viável + prova local autorizada do caminho MCP real (PhotoCraft, stateless)**: base agentskills.io, core/composição/DAG, adapter CLI/MCP, resiliência, 5 skills criativas Python + scene-composition/workflows, validação 12/12 e 412 testes default verdes, 006 funcional mock-first, 007 smoke real opt-in comprovado no escopo limitado.
- **Não é 100% do produto**: falta validação operacional ampla multi-app/ambiente, sessão MCP stateful (Option B), mapeamento profundo por capacidade real de cada Crafting App, expansão de domínios (vídeo/motion, áudio/docs, CAD), e adoção/docs de produto (README/onboarding/política de compatibilidade).

## O que falta (priorizado)

1. **Operacionalização/CI opcional controlada (baixo/médio):** job opcional/manual para smoke MCP real em ambiente autorizado (nunca default), com artefatos de evidência e segredos/binários gerenciados fora do repo.
2. **Option B — sessão MCP stateful (médio/alto, spec separada):** helper/adapter para `doc_new → command → doc_export` em sessão retida, com testes mock-first + validação opt-in real; preservar contratos públicos.
3. **Mapeamento MCP por capacidade real:** alinhar skills/fluxos às ferramentas reais do PhotoCraft/outros apps (roots, progresso/cancelamento, formatos, erros), sem “geração IA” indevida.
4. **Decisão de dependência MCP (quando necessário):** avaliar SDK oficial Python (`mcp`/`modelcontextprotocol` v2.x) vs cliente mínimo atual para lifecycle avançado, auth remota, Streamable HTTP ou compatibilidade ampliada; manter mock-first e back-compat.
5. **Fechamento documental Speckit residual:** reconciliar/normalizar marcações onde evidência de convergência existe (ex.: 001/004/005 nuances de checkbox/texto), e resolver ambiguidade histórica de numeração `006-*` em referências futuras (sem reescrever histórico).
6. **Expansão de domínios (roadmap Phases 3–5):** vídeo/motion/animação; áudio/voz/docs/apresentações; CAD/precisão — após base MCP/CLI estável e mapeamentos claros.
7. **Produto/adoção:** `README.md` raiz, exemplos reais, onboarding CLI/MCP, matriz de compatibilidade (versões Crafting Apps/MCP/protocolo).

## O que este projeto NÃO faz (reforço)
- Não reimplementa modelos/provedores de geração nem backend próprio.
- Não substitui apps ArtCraft; é camada de skill/agente sobre CLI/MCP/AI studio expostos.
- Não executa smoke real MCP em CI/default; exige opt-in + autorização + controles de segurança.
- Não prova/implementa geração IA via PhotoCraft MCP local (007 = engine/editor stateless) nem sessão stateful/artifact cycle cross-call.
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos.
