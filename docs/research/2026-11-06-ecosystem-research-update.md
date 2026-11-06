# Ecosystem Research Update — 2026-11-06

## Fontes primárias consultadas

1. https://agentskills.io/specification — agentskills.io specification (SKILL.md frontmatter, progressive disclosure, validação via skills-ref).
2. https://modelcontextprotocol.io/specification/2026-07-28/server/tools.md — MCP Tools, revisão 2026-07-28.
3. https://py.sdk.modelcontextprotocol.io/v2/whats-new/ — MCP Python SDK v2 whats-new, v2.3.0.
4. https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md — PhotoCraft MCP conventions, main branch.

Data de acesso: 2026-11-06.

## Principais achados

### agentskills.io specification
- Uma skill é um diretório contendo, no mínimo, um arquivo `SKILL.md` com YAML frontmatter seguido de conteúdo Markdown.
- Frontmatter obrigatório: `name` (máx. 64 chars, kebab-case `^[a-z0-9]+(-[a-z0-9]+)*$`, não pode iniciar ou terminar com hífen, não pode conter hífenes duplos, deve bater com o nome do diretório) e `description` (máx. 1024 chars, não vazio, descreve o que a skill faz e quando usá-la).
- Frontmatter opcional: `license`, `compatibility` (máx. 500 chars), `metadata` (map string→string), `allowed-tools` (experimental, space-separated).
- Progressive disclosure: metadata (~100 tokens) carregado no startup; instruções (< 5000 tokens) carregadas quando a skill é ativada; recursos (scripts/, references/, assets/) carregados sob demanda.
- Diretórios opcionais: `scripts/` (código executável), `references/` (documentação adicional), `assets/` (recursos estáticos).
- Validação via `skills-ref` (referência library do agentskills/agentskills).

### MCP specification 2026-07-28 (revisão mais recente)
- `tools/list`: suporta paginação (`cursor`) e caching (`ttlMs`, `cacheScope`, `resultType: "complete"`). Servidores devem retornar tools em ordem determinística.
- `tools/call`: argumentos `name` e `arguments`. Resposta com `content` (array de content blocks) e `isError`.
- `InputRequiredResult`: servers podem responder com `resultType: "input_required"` para indicar que input adicional é necessário (multi round-trip requests).
- `_meta` obrigatório em todo request: `io.modelcontextprotocol/protocolVersion`, `io.modelcontextprotocol/clientInfo`, `io.modelcontextprotocol/clientCapabilities`.
- Capacidades do servidor: `capabilities.tools.listChanged` indica se o servidor emite notificações quando a lista de tools muda.
- `listChanged` notification: `notifications/tools/list_changed` via `subscriptions/listen`.
- Revisão 2026-07-28 remove handshake/sessão e server-initiated requests (roots, sampling, logging deprecados; ping removido). `server/discover` substitui `initialize` na nova revisão.

### MCP Python SDK v2 (v2.3.0)
- `pip install mcp` instala 2.x. v2.0.0 estável desde 2026-07-28.
- `FastMCP` renomeado para `MCPServer`; `mcp.server.fastmcp.*` movido para `mcp.server.mcpserver.*`.
- `Client` primeira classe: um objeto que conecta e negocia a versão do protocolo automaticamente (serve tanto 2025-11-25 quanto 2026-07-28 simultaneamente).
- Wire types movidos para distribuição separada `mcp-types`; todos os atributos Python são `snake_case` (JSON no wire continua camelCase).
- Transporte stdio disponível; WebSocket transport removido; Tasks API experimental removida (movida para SEP-2663).
- `McpError` renomeado para `MCPError`; `get_context()` e `mount_path=` removidos.
- Sync handlers rodam em worker thread (não bloqueiam o event loop).

### PhotoCraft MCP docs (main branch, storytold/photocraft)
- `photocraft-cli mcp --automation-read-root <abs> --automation-write-root <abs>` inicia sessão headless MCP.
- Roots concedem autoridade de filesystem: leitura abaixo do read root, escrita/export abaixo do write root.
- `doc_save`/`doc_export` substituem arquivo existente apenas se extensão for formato de imagem/documento que PhotoCraft escreve (PNG, JPEG, TIFF, PSD, PSB, .pcraft, OpenRaster, PDF, …) ou bytes forem imagem; qualquer outro é recusado.
- Multi-file exports (layers, data sets) nunca substituem arquivo.
- Bridge mode usa `--bridge` e `--control-token-file`; roots configuradas no desktop app (flags de root em `--bridge` são rejeitadas).
- Tools: `command_list` (discover engine ids, params, enabled state; aceita `filter` e `enabled_only`), `command_run` (`id`, `params`, `wait`), `command_batch` (ordered `steps`, `stop_on_error` default true, não é atomic transaction), `doc_inspect` (layer tree, history, selection), `render_preview` (bounded PNG, `index`, `max_side` default 1024 máximo 2048), `ui_inspect`/`ui_screenshot` (bridge mode).
- Reads são idempotentes; `doc_new`/`doc_open`/`doc_place`/`doc_select` não destrutivos; `doc_export_layers`/`doc_export_data_sets` recusam overwrite.
- Progress via `_meta.progressToken` (0–1, throttled a ≤10/s, inclui `total`); cancelamento via `notifications/cancelled`.
- Campos MCP 2026-07-28: result/cache fields em list/read responses.
- Recursos `photocraft://document` e `photocraft://commands` retornam JSON ao vivo.

## Implicações para o projeto

1. **Conformidade agentskills.io já atendida:** 12/12 skills validadas com `SKILL.md` frontmatter YAML (name kebab-case 1–64 chars, description 1–1024 chars), progressive disclosure. Nenhuma ação adicional necessária.
2. **Alinhamento MCP 2026-07-28 a documentar/implementar:** o adapter atual (`artcraft_app_client.py`, `__version__ 0.3.0`) implementa transporte stdio mínimo viável compatível com MCP 2025-11-25 e alinhado com a revisão 2026-07-28 (_meta obrigatório, server/discover, sem handshake/sessão na nova revisão). Deve ser documentado nos specs e quickstarts do 006/007.
3. **Decisão de dependência MCP SDK v2 pendente:** `modelcontextprotocol/python-sdk` v2.3.0 está disponível (`pip install mcp` instala 2.x), fala a revisão 2026-07-28 e serve ambas as revisões simultaneamente. Avaliar migração do cliente mínimo atual para `mcp.Client` + `StdioServerParameters` vs manter cliente mínimo atual, preservando mock-first/back-compat.
4. **007 Option B deve considerar ausência de handshake/sessão server-side:** MCP 2026-07-28 remove handshake e sessão server-side; sessão stateful (007 Option B) deve reter estado client-side ou usar multi-round-trip (InputRequiredResult), não depender de sessão server-side.
5. **PhotoCraft `photocraft-cli 0.20.1` observado localmente:** 26 MCP tools via `tools/list`, incluindo `command_list`, `command_run`, `command_batch`, `doc_new/open/save/export/inspect/render_preview`, `jobs_*`, `session_list`, e tools UI/bridge. `command_list` retorna engine command metadata (`file.new`, `edit.fill`, `paint.stroke`; export: `file.export.quickExport`, `layer.exportAs`, `doc.export`). `doc_inspect` mostra sessão não-persistente entre chamadas separadas do adapter.

## Fontes secundárias (ecosystem signal, não normativo)

- https://agentskills.io/llms.txt (agentskills.io)
- https://modelcontextprotocol.io/llms.txt (Model Context Protocol)
- https://github.com/storytold/photocraft (PhotoCraft repo)
- https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.0.0 (MCP Python SDK v2.0.0 release)
