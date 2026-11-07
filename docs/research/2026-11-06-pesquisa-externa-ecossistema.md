# Pesquisa Externa de Ecossistema — ArtCraft Skills

- **Data de acesso**: 2026-11-06
- **Escopo**: pesquisa web para atualizar entendimento de agentskills.io, MCP (Python SDK/protocolo) e evidência pública sobre `storytold/photocraft`. Restrições: factual, fontes confiáveis, sem afirmar suporte não verificado no repositório.
- **Limitação**: resultados de busca agregados (web_search) + verificação local do repo/gates nesta reexecução MDMV (2026-11-06). Evidência pública não substitui execução local autorizada.

---

## 1. agentskills.io — especificação e requisitos de `SKILL.md`

- **Fonte**: [Agent Skills Specification](https://agentskills.io/specification) (agentskills.io). Data de acesso: 2026-11-06.
- **Resumo (conforme busca)**: formato padrão para skills de agentes. Uma skill é um diretório contendo, no mínimo, `SKILL.md`. `SKILL.md` requer frontmatter YAML com metadados (campos como `name`, `description`; opcionais como `license`, `compatibility`, `metadata`, `allowed-tools` conforme a spec) seguido de instruções em Markdown. Estrutura típica inclui `scripts/`, `references/`, `assets/` opcionais; progressive disclosure (metadados ~100 tokens; instruções <5000 tokens, conforme prática do repo).
- **Implicação para artcraft-skills**: **alinhado**. Gates verificados: **12/12 skills validadas** (`python scripts/validate_all_skills.py`), frontmatter YAML com `name` kebab-case (1–64 chars) e `description` (1–1024 chars). Nenhuma mudança de contrato necessária identificada por esta busca.

## 2. MCP Python SDK v2.x e revisão do protocolo 2026-07-28

- **Fontes**:
  - [Release v2.3.0 · modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0) (GitHub, publicado 2026-10-02). Data de acesso: 2026-11-06.
  - [What's new in v2 — MCP Python SDK](https://py.sdk.modelcontextprotocol.io/v2/whats-new/) (docs SDK). Data de acesso: 2026-11-06.
  - [Key Changes — MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog) e [Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover) (modelcontextprotocol.io). Data de acesso: 2026-11-06.
- **Resumo (conforme busca)**:
  - `modelcontextprotocol/python-sdk` **v2.3.0** (tag `v2.3.0`, 2026-10-02). SDK v2 fala a revisão **2026-07-28** e, segundo as docs do SDK, serve ambas as revisões (2025-11-25 e 2026-07-28) simultaneamente. Instalação típica: `pip install -U mcp` (instala 2.x conforme releases/docs).
  - MCP **2026-07-28** (conforme changelog/discovery): introduz `server/discover` (consulta de versões/capacidades/identidade antes de outras requests; servidor DEVE implementar); mudanças de versionamento/negociação; remoção de handshake/sessão server-side na nova revisão (sem `_Mcp-Session-Id` no caminho 2026, conforme entendimento já registrado no repo); `_meta` e semânticas de tools evoluídas. Server-initiated requests (roots/sampling/logging) e ping têm mudanças/depreciações conforme a revisão — **não afirmar suporte no adapter sem evidência**.
- **Implicação para artcraft-skills**: o adapter (`skills/core/artcraft_app_client.py` **v0.4.0**) mantém **cliente mínimo síncrono** (006) para `tools/list`/`tools/call` stateless + **helper aditivo 009** (`mcp_stateful_session`/`MCPStatefulSession`, subprocesso retido, mock-first/TDD) — preservando 006/FR-005/FR-006/schemas. Decisão de migração para `mcp.Client`/SDK v2 permanece **pendente** (lifecycle/auth remota/Streamable HTTP/compatibilidade ampliada), mantendo mock-first/back-compat. 009 usa client-retained process state; não assume sessão server-side MCP 2026-07-28.

## 3. Evidência pública sobre `storytold/ArtCraft` / `photocraft-cli`

- **Fontes (conforme busca)**:
  - [photocraft/docs/mcp.md at main · storytold/photocraft](https://github.com/storytold/photocraft/blob/main/docs/mcp.md) (GitHub). Data de acesso: 2026-11-06.
  - [photocraft/book/src/automation/mcp.md at main · storytold/photocraft](https://github.com/storytold/photocraft/blob/main/book/src/automation/mcp.md) (GitHub). Data de acesso: 2026-11-06.
  - [GitHub - storytold/photocraft](https://github.com/storytold/photocraft) (repositório). Data de acesso: 2026-11-06.
- **Resumo (conforme busca)**: **há evidência pública** de que `storytold/photocraft` existe (repositório GitHub público) e expõe documentação de MCP/automação (`docs/mcp.md`, `book/src/automation/mcp.md`). Isso **não substitui** evidência local do binário/ambiente nem autoriza claims além do escopo verificado no repo (006/007). O smoke 007 permanece **opt-in, test-only, engine/editor stateless, sem claim de geração IA**.
- **Implicação para artcraft-skills**: atualizar linguagem de "provável ausência de fontes públicas" (hipótese do plano) para **"há repositório/docs públicos do PhotoCraft; ainda assim, operação real depende de binário/ambiente local autorizado e do escopo verificado"**. Nenhuma mudança de comportamento de runtime.

## 4. MCP 2026-07-28 — mudanças relevantes (síntese para mapeamento)

- **Fonte**: [Key Changes — 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog), [Discovery](https://modelcontextprotocol.io/specification/2026-07-28/server/discover). Data de acesso: 2026-11-06.
- **Pontos de atenção (conforme busca, não exaustivos)**: `server/discover` para descoberta prévia de versões/capacidades/identidade; negociação/versionamento evoluídos; no caminho 2026, sem handshake/sessão server-side conforme registrado no repo; ferramentas com `_meta`/semânticas atualizadas. 009 (007 Option B) implementa **subprocesso stdio retido client-side** (mock-first) com consciência disso (sem assumir `_Mcp-Session-Id` server-side); **ciclo real PhotoCraft permanece opt-in autorizado**.
- **Implicação para artcraft-skills**: 008 (capability mapping) e 009 (helper aditivo) avançam mapeamento/viabilização sem overclaim; real artifact cycle ainda capability-gated/opt-in.

---

## Conclusões e ações aplicadas

1. **agentskills.io**: alinhamento confirmado no nível de especificação; gates 12/12 válidas mantidos.
2. **MCP SDK v2.3.0 / 2026-07-28**: SDK maduro para a revisão 2026-07-28; decisão de migração permanece backlog; cliente mínimo 006 preservado.
3. **PhotoCraft público**: docs/repo públicos existem (`storytold/photocraft`); execução real continua dependente de ambiente autorizado e escopo verificado (006/007).
4. **Ação**: incorporar esta pesquisa (e correção da hipótese sobre evidência pública do PhotoCraft) em `OBJETIVO.md`/`ROADMAP.md` (P6) e no relatório de estado (P4 já criado; P6 pode atualizar se necessário).

*Gerado no contexto do plano `local://mdmv-fluxo-artcraft-skills-plan.md` (P5).*
