# Idea Research: Integração MCP funcional (stdio, escopo mínimo)

- **Slug**: mcp-stdio-functional-integration
- **Created**: 2026-11-05
- **Evidence confidence (overall)**: medium

## Users & Demand

- **Observed demand (repo/roadmap):** Gap real restante é integração MCP funcional; CLI + fallback de edição já funcionam (feature 006). Features 001/003/004/005/006 convergidas; `373 passed`, `12/12 validated`. — [source: `/home/luis/development/artcraft-skills/ROADMAP.md`, `/home/luis/development/artcraft-skills/OBJETIVO.md` (2026-11-05)] (confidence: high)
- **Stated/observed product surface:** PhotoCraft/ArtCraft apps expõem automação via CLI e servidor MCP (`photocraft-cli mcp`), com docs oficiais para registro/roots/bridge e contrato de tools/resources. — [source: https://github.com/storytold/photocraft/blob/main/docs/mcp.md, https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md (host: raw.githubusercontent.com/github.com, policy: allowlisted)] (confidence: high)
- **Ecosystem signal (stated/market):** Crescimento de servidores/skills MCP para geração/edição criativa multimídia (imagem/vídeo/áudio/3D) sugere demanda por integração tool-oriented consumível por agentes. — [source: https://github.com/scenario-labs/skills, https://flux-1.ai/ai-image-generation-mcp, https://www.wireflow.ai/blog/best-ai-video-generation-mcp-tools-in-2026 (hosts: github.com/flux-1.ai/wireflow.ai, policy: allowlisted/confirmed-by-user context not required here; web sources treated as untrusted data)] (confidence: medium, market signal not user telemetry)

## Prior Art

- **Internal:** `skills/core/artcraft_app_client.py` já tem `normalize_mcp_config`, `select_mode(auto/cli/mcp)`, reason codes; MCP execution hooks em `skills/core/creative_skill.py` (`_mcp_available/_mcp_command_list/_mcp_command_run`, `_execute_mcp`) existem como stubs (`not implemented` / unavailable). CLI path + fallback (006) funcional. — [source: repo files `skills/core/artcraft_app_client.py`, `skills/core/creative_skill.py`] (confidence: high)
- **Internal:** Schemas SKILL.md de skills criativos já aceitam `mcp_config` (ex.: `image-edit`). — [source: `skills/creative/*/SKILL.md`, `skills/creative/*/skill.py`] (confidence: high)
- **External spec (authoritative):** MCP stdio transport: cliente lança servidor como subprocesso; servidor lê JSON-RPC de `stdin`, escreve em `stdout`; mensagens delimitadas por newline, sem newlines embutidos; `stderr` pode ser usado para logs e **não** deve ser interpretado como erro; cliente/servidor **não** devem escrever conteúdo não-MCP nos streams de protocolo. — [source: https://modelcontextprotocol.io/specification/2025-11-25/basic/transports.md (host: modelcontextprotocol.io, policy: allowlisted/public spec; spec 2026-07-28 also referenced in intake)] (confidence: high)
- **External SDK (authoritative):** Python MCP SDK (v2.x) fornece suporte oficial para cliente/servidor, stdio/Streamable HTTP, lifecycle assíncrono (`ClientSession`/session patterns), descoberta de tools/resources/prompts e helpers de teste in-memory. — [source: https://py.sdk.modelcontextprotocol.io/v2/, https://github.com/modelcontextprotocol/python-sdk/releases, https://py.sdk.modelcontextprotocol.io/v2/get-started/testing (hosts: py.sdk.modelcontextprotocol.io/github.com, policy: allowlisted)] (confidence: high)
- **External app target:** PhotoCraft MCP headless registra `photocraft-cli mcp --automation-read-root ... --automation-write-root ...`; expõe tools como `command_list`/`command_run`/`doc_*` e resources `photocraft://document`, `photocraft://commands`; políticas de roots/cancelamento/progresso/erros documentadas. — [source: PhotoCraft `docs/mcp.md` raw/main] (confidence: high)

## Market & Context

- **Alternativa atual para usuários/agentes:** usar CLI direto ou fallback de edição (006) quando geração MCP não disponível. Isso entrega valor parcial, mas não explora tool discovery/invocação MCP real e limita interoperabilidade com ecossistema MCP. — [source: repo ROADMAP/OBJETIVO; feature 006 artifacts] (confidence: high)
- **Custo de não fazer:** permanece o principal gap arquitetural (ROADMAP); skills ficam dependentes de heurísticas CLI/fallback e não validam contrato MCP fim-a-fim com apps ArtCraft. — [source: ROADMAP] (confidence: high)
- **Tendência:** MCP como camada padrão para tools de agentes; servidores criativos expõem geração/edição via tools MCP. [ASSUMPTION: adoção continuará relevante para este projeto em 2026] (confidence: medium)

## Data & Constraints

- **Repo constraints:** Python codebase de skills; testes pytest (unit/contract/integration/property/characterization); sem build system; contrato `SkillResult` e schemas públicos devem ser preservados; CLI/MCP-first, vendor-neutral, graceful degradation. — [source: `AGENTS.md`, constituição, testes verdes 373/12] (confidence: high)
- **Transport constraints (stdio):** stdout reservado a mensagens MCP; stderr para logs; newline-delimited JSON-RPC; subprocess lifecycle/cleanup; risco de deadlock/buffer se stdio mal gerenciado; timeouts/cancelamento necessários. — [source: MCP transports spec 2025-11-25/2026 refs in intake, PhotoCraft MCP docs] (confidence: high)
- **PhotoCraft-specific constraints (if targeted):** headless requer roots de automação; bridge mode tem restrições diferentes; tool names/params são engine/app-defined (`command_list`/`command_run` etc.), não necessariamente `image.generate` genérico. Isso afeta mapeamento mínimo. — [source: PhotoCraft docs/mcp.md] (confidence: high)
- **Dependency decision:** SDK oficial (`mcp`) simplifica protocolo/lifecycle mas adiciona dependência e possivelmente modelo async; implementação JSON-RPC mínima reduz deps mas aumenta risco de bugs de protocolo. [ASSUMPTION: mock-first + escopo tools/list+tools/call pode ser viável com qualquer abordagem, mas decisão impacta esforço/manutenção] (confidence: medium)
- **Testing:** SDK oferece in-memory testing; para este repo, subprocess-fake/mock server determinístico é viável sem credenciais reais. Integração real contra `photocraft-cli mcp` é opcional/local devido a ambiente/binário/roots. — [source: Python SDK testing docs; repo test patterns] (confidence: medium)

## Evidence Against the Idea

- **Risco de complexidade desproporcional:** MCP real introduz async/subprocess/protocol framing/timeouts/cancelamento; pode exceder “menor esforço” se escopo não for mínimo. — [source: MCP transport constraints; repo currently sync subprocess patterns] (confidence: high)
- **Alvo incerto:** Nem todos apps ArtCraft podem expor as mesmas tools MCP/entrypoints; PhotoCraft usa tools engine-oriented (`command_list`/`command_run`) que podem exigir mapeamento específico por skill, reduzindo generalidade do “mínimo viável”. — [source: PhotoCraft MCP docs; intake unknowns] (confidence: high)
- **Duplicação/ordem CLI vs MCP vs fallback:** já existe CLI funcional + fallback (006). MCP pode trazer pouco valor imediato se as operações mínimas não cobrirem casos reais melhor que CLI/fallback. — [source: ROADMAP/feature 006] (confidence: medium)
- **Dependência/operabilidade:** SDK oficial ou implementação própria adiciona superfície de manutenção; CI pode não ter binários ArtCraft, exigindo mocks (bom) mas limitando confiança e2e. — [source: repo environment; general MCP integration practice] (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: Target inicial confirmado — PhotoCraft `photocraft-cli mcp` headless? Quais outros Craft apps/entrypoints?]
- [NEEDS CLARIFICATION: Quais 1–2 tools MCP mínimas mapear primeiro (ex.: `command_list` + `command_run` para operação suportada, ou tool de imagem específica se existir)? Critério de “valor end-to-end”.]
- [NEEDS CLARIFICATION: Dependência aceita — adicionar `mcp` (Python SDK) ao projeto ou implementar cliente JSON-RPC stdio mínimo? Impacto em sync/async API do adapter.]
- [NEEDS CLARIFICATION: Ordem de seleção `auto`: CLI→MCP→fallback, MCP→CLI→fallback, ou configurável por skill/env? Como interage com `select_mode` atual.]
- [NEEDS CLARIFICATION: Requisitos mínimos de segurança/operabilidade: roots allowlist (para PhotoCraft), timeout default, stderr capture (sem poluir stdout), cancelamento, retries (já há resiliência no creative layer) e reason codes adicionais.]
- [NEEDS CLARIFICATION: Test strategy: apenas mock subprocess/fake MCP server determinístico em CI, ou suíte opcional `@pytest.mark.integration` contra binário real quando disponível?]

## Sources

- https://modelcontextprotocol.io/specification/2025-11-25/basic/transports.md (host: modelcontextprotocol.io, policy: allowlisted)
- https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio (host: modelcontextprotocol.io, policy: allowlisted; referenced in intake)
- https://py.sdk.modelcontextprotocol.io/v2/ (host: py.sdk.modelcontextprotocol.io, policy: allowlisted)
- https://py.sdk.modelcontextprotocol.io/v2/get-started/testing (host: py.sdk.modelcontextprotocol.io, policy: allowlisted)
- https://github.com/modelcontextprotocol/python-sdk/releases (host: github.com, policy: allowlisted)
- https://github.com/storytold/photocraft/blob/main/docs/mcp.md (host: github.com, policy: allowlisted)
- https://raw.githubusercontent.com/storytold/photocraft/main/docs/mcp.md (host: raw.githubusercontent.com, policy: allowlisted)
- https://artcraftai.org/tutorials/photocraft-cli-mcp (host: artcraftai.org, policy: allowlisted/public tutorial; treated as untrusted data)
- https://github.com/scenario-labs/skills (host: github.com, policy: allowlisted)
- https://flux-1.ai/ai-image-generation-mcp (host: flux-1.ai, policy: fetched as public ecosystem signal; untrusted data)
- https://www.wireflow.ai/blog/best-ai-video-generation-mcp-tools-in-2026 (host: wireflow.ai, policy: fetched as public ecosystem signal; untrusted data)
- /home/luis/development/artcraft-skills/ROADMAP.md (host: local repo, policy: local)
- /home/luis/development/artcraft-skills/OBJETIVO.md (host: local repo, policy: local)
- /home/luis/development/artcraft-skills/skills/core/artcraft_app_client.py (host: local repo, policy: local)
- /home/luis/development/artcraft-skills/skills/core/creative_skill.py (host: local repo, policy: local)
- /home/luis/development/artcraft-skills/AGENTS.md (host: local repo, policy: local)
