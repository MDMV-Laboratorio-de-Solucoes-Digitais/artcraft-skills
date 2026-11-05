# Idea Intake: Integração MCP funcional (stdio, escopo mínimo)

- **Slug**: mcp-stdio-functional-integration
- **Created**: 2026-11-05
- **Source**: pasted text (user request)
- **Type**: improvement

## Idea (as captured)

> Pesquisar e avaliar a implementação de **integração MCP funcional** como próximo passo 80/20. Estado verificado: features 001/003/004/005/006 convergidas; `373 passed` (`python -m pytest -q`), `12/12 validated` (`scripts/validate_all_skills.py`). Gap real restante: integração MCP funcional (hoje majoritariamente stubs/descoberta parcial; CLI + fallback de edição já funcionam — feature 006). `ROADMAP.md`/`OBJETIVO.md` estavam desatualizados (já corrigidos).
>
> Pesquisa citada (fontes públicas): MCP stdio é transporte padrão local (cliente lança servidor MCP como subprocesso, comunica por stdin/stdout; spec 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio). Python MCP SDK oficial (v2.x) suporta cliente/servidor stdio/Streamable HTTP, lifecycle `async with session`, descoberta de tools/resources/prompts (https://py.sdk.modelcontextprotocol.io/v2/, https://github.com/modelcontextprotocol/python-sdk/releases). Ecossistema criativo via MCP em crescimento 2025–2026 (ex.: https://github.com/scenario-labs/skills, https://flux-1.ai/ai-image-generation-mcp, https://www.wireflow.ai/blog/best-ai-video-generation-mcp-tools-in-2026). ArtCraft/PhotoCraft expõem MCP via CLI/automação (ex.: https://github.com/storytold/photocraft/blob/main/docs/mcp.md, https://artcraftai.org/tutorials/photocraft-cli-mcp).
>
> Escopo mínimo sugerido: camada MCP em `artcraft_app_client`/adapter com stdio subprocess, descoberta `tools/list` + invocação `tools/call` para 1–2 operações suportadas, normalização para `SkillResult`, fallback CLI→MCP→degradação conforme contrato; testes unit/contract/property/characterization com MCP server mockado/subprocess fake (determinístico); sem alterar schemas públicos; sem exigir credenciais reais nem cobrir todos os domínios.

## Restated

Implementar uma integração MCP funcional mínima, baseada em transporte stdio, para permitir descoberta e invocação real de ferramentas MCP dos apps ArtCraft a partir da camada de adapter/skills, preservando contratos existentes, degradação graciosa e cobertura de testes determinísticos.

## Origin & Context

- **Raised by**: [NEEDS CLARIFICATION: stakeholder/autor específico]
- **Trigger**: Revisão do estado do repositório após convergência das features 001/003/004/005/006 identificou MCP funcional como principal gap arquitetural restante; análise 80/20 indicou MCP stdio mínimo como maior avanço com menor esforço (2026-11-05).

## First-Glance Unknowns

- [NEEDS CLARIFICATION: Quais apps/servidores MCP ArtCraft (ex.: PhotoCraft, PdfCraft, outros) são alvo inicial e qual comando/entrypoint stdio é suportado em cada ambiente?]
- [NEEDS CLARIFICATION: Quais 1–2 operações/ferramentas MCP devem ser suportadas no escopo mínimo para validar valor end-to-end?]
- [NEEDS CLARIFICATION: O SDK Python MCP oficial (`mcp`) será dependência direta ou a integração usará implementação mínima JSON-RPC/stdio própria para reduzir dependências?]
- [NEEDS CLARIFICATION: Como o adapter selecionará/ordenará CLI vs MCP vs fallback de edição por skill, configuração e disponibilidade?]
- [NEEDS CLARIFICATION: Quais requisitos de segurança/sandbox, timeouts, cancelamento e tratamento de erros do subprocesso MCP são necessários para produção?]
- [NEEDS CLARIFICATION: A estratégia mock-first será suficiente sem testes de integração contra um servidor MCP real em CI/local opcional?]
