# Decision: Integração MCP funcional (stdio, escopo mínimo)

- **Slug**: mcp-stdio-functional-integration
- **Decided**: 2026-11-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

| Criterion | Rating | Justification |
|---|---|---|
| Problem validity | strong | MCP permanece stub/parcial enquanto CLI+fallback funcionam; gap arquitetural real confirmado por ROADMAP/OBJETIVO e estado do código (`CreativeSkill` MCP hooks stubados). |
| Evidence strength | adequate | Fontes primárias MCP (spec stdio 2025-11-25/2026-07-28), Python SDK oficial, docs PhotoCraft MCP e evidência local do repo sustentam o recorte; incertezas de alvo/tool/dependência permanecem, mas não invalidam o problema nem o conceito mínimo. |
| Value vs. inaction | strong | Fechar o gap habilita validação real da estratégia CLI/MCP/fallback e reduz risco para fases futuras; manter stubs preserva dívida no item de maior valor arquitetural restante. |
| Feasibility / appetite | adequate | Option A é `small` (1 alvo, 1–2 operações, `tools/list`+`tools/call`, mock-first, sem quebra de contratos) e aproveita adapter/hooks/test patterns existentes; viabilidade depende de confirmar alvo e mapeamento mínimo em `/speckit.specify`. |
| Strategic fit | strong | Alinha com constituição/repo: CLI/MCP-first, vendor-neutral, `SkillResult` preservado, graceful degradation, TDD/property/contract tests, 80/20. |
| Risk posture | adequate | Riscos conhecidos (subprocess/protocolo, alvo incerto, ordem `auto`, SDK vs JSON-RPC mínimo) podem ser mitigados por escopo mínimo, mock-first, reason codes e back-compat; não construir sem clarificações carregadas para specify. |

## Verdict & Rationale

**go**. O problema é válido e estrategicamente alinhado, a evidência é adequada para autorizar especificação do recorte mínimo (Option A), e o valor de fechar o gap MCP supera o custo da inação quando o escopo permanece limitado: stdio, descoberta+invocação mínima, normalização para `SkillResult`, degradação graciosa e testes determinísticos mock-first sem alterar schemas públicos. O GO não ignora incertezas: alvo MCP inicial, ferramentas mínimas, dependência SDK/cliente mínimo, ordem `auto` e controles operacionais devem ser resolvidos ou explicitamente delimitados em `/speckit.specify`.

## If needs-clarification

- **Blocking questions**: N/A (ver carried-forward open questions no handoff)
- **Revisit stage**: N/A

## If go — Handoff to `/speckit.specify`

- **Problem**: Habilitar descoberta e invocação MCP funcional (stdio) para skills criativas no menor recorte útil, preservando CLI+fallback, contratos públicos e testes determinísticos.
- **Chosen approach**: Option A — cliente MCP stdio mínimo (mock-first) para 1 app alvo + 1–2 operações (`tools/list` + `tools/call`), com normalização para `SkillResult` e graceful degradation.
- **In scope / out of scope**:
  - *In*: 1 transport stdio; 1 alvo inicial confirmado; 1–2 operações MCP de valor end-to-end; `tools/list`/`tools/call`; adapter/hooks MCP reais mínimos; reason codes/erros estruturados; timeouts/stderr handling básicos; testes unit/contract/property/characterization mock-first; documentação de política/limites.
  - *Out*: multi-app/multi-tool amplo; transportes além de stdio; resources/prompts/HTTP avançado; mudanças em schemas públicos; remoção CLI/fallback; backend/provedor novo; e2e real obrigatório em CI; credenciais/rede/binários reais obrigatórios.
- **Success metrics**: recorte MCP mínimo passa em testes determinísticos mockados; `>=373 passed` e `12/12 validated` sem regressão; falhas MCP (indisponível, timeout, resposta inválida, tool ausente/erro) retornam `SkillResult` estruturado com degradação adequada; alvo/tools/ordem `auto`/limites documentados.
- **Carried-forward open questions**:
  - [NEEDS CLARIFICATION: Alvo MCP inicial (candidato: PhotoCraft `photocraft-cli mcp` headless com roots)?]
  - [NEEDS CLARIFICATION: Quais 1–2 ferramentas/operações MCP mínimas e critério de valor end-to-end (ex.: `command_list`+`command_run` mapeadas a uma skill suportada)?]
  - [NEEDS CLARIFICATION: Usar SDK Python MCP oficial (`mcp`) ou cliente JSON-RPC stdio mínimo/sync-friendly?]
  - [NEEDS CLARIFICATION: Ordem em modo `auto` (CLI→MCP→fallback, MCP→CLI→fallback, configurável) preservando comportamento atual?]
  - [NEEDS CLARIFICATION: Controles mínimos obrigatórios: timeout default, cancelamento, stderr capture, roots allowlist (PhotoCraft), retries vs resiliência existente, reason codes adicionais?]
  - [NEEDS CLARIFICATION: Suíte opcional de integração real local/CI (`@pytest.mark.integration`) quando binário/roots disponíveis?]
  - [NEEDS CLARIFICATION: Owner/stakeholder formal para priorização e aceite?]
