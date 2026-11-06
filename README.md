# ArtCraft Skills Suite

Ecossistema open-source e composável de *skills* para agentes de IA, seguindo o padrão [agentskills.io](https://agentskills.io). O objetivo é transformar *prompting* em *crafting* intencional: fluxos compostos, controle preciso e integração com superfícies reais.

**Build before generating.** Este repositório **não** reimplementa motores/modelos/provedores de geração nem backend próprio. Ele é a *camada de skill/agente* sobre capacidades expostas pelos apps ArtCraft / “Crafting Apps” (organização `storytold`, ex.: PhotoCraft, PdfCraft e demais apps Rust) via **CLI** (ex.: `photocraft-cli`) e **MCP server**, além do AI studio da ArtCraft — conforme essas capacidades estejam realmente disponíveis e mapeadas.

> Estado verificado em **2026-11-06** (`dev`). Detalhes: [`OBJETIVO.md`](OBJETIVO.md), [`ROADMAP.md`](ROADMAP.md), [`docs/research/2026-11-06-ecosystem-roadmap-status.md`](docs/research/2026-11-06-ecosystem-roadmap-status.md).

## Status e gates (verificados)

| Gate | Resultado (2026-11-06) | Comando |
|---|---|---|
| Testes padrão (integração opcional excluída por padrão) | **412 passed, 23 deselected** | `PYTHONPATH=. python -m pytest -q` |
| Validação de skills (agentskills.io) | **12/12, `all_valid=True`** | `python scripts/validate_all_skills.py` |

Escopo convergido (evidência em `specs/*`): 001, 003, 004, 005 (resiliência, evidência registrada), 006-MCP stdio funcional (mínimo viável), 007 PhotoCraft MCP smoke **Option A stateless** (T001–T023; SC-001 exercido localmente sob **autorização explícita**, escopo limitado — ver limites).

## Quickstart

```bash
cd /home/luis/development/artcraft-skills  # ou a raiz do clone

# Gate padrão (determinístico; não exige binários/apps externos reais)
PYTHONPATH=. python -m pytest -q

# Validação do formato de skills
python scripts/validate_all_skills.py
```

Pré-requisitos: Python 3, `pytest`/`hypothesis`/`PyYAML` conforme o ambiente do repo (sem gerenciador de pacotes na raiz). Testes marcados `@pytest.mark.integration` ficam **excluídos por padrão** (`pytest.ini`: `-m "not integration"`).

## Arquitetura (resumo)

- **`skills/`** — pacotes por categoria (`core/`, `creative/`, `integration/`, `workflow/`). Skills declarativas (`SKILL.md`, frontmatter YAML + Markdown) e/ou implementações Python (`skill.py`).
- **`skills/core/`** — `BaseSkill`/`SkillResult`, `CreativeSkill` (discover→resolve→invoke→normalize→degrade), adapter compartilhado `artcraft_app_client` (CLI/MCP), composição (`SkillComposer`), DAG (`DAGOrchestrator`), resiliência/utilitários.
- **`scripts/`** — validação (`validate_skill.py`, `validate_all_skills.py`), loader/registro.
- **`tests/`** — `unit/`, `integration/`, `contract/`, `property/`, `characterization/` (+ helpers/golden/reference).
- **`specs/`** — especificações/planos/tasks/contratos/checklists (Spec Kit).
- **`docs/`** — guias e pesquisas (`skill-authoring`, `core-abstractions`, `architecture`, `cross-product`, `generalizable-workflows`, `research/*`).
- **`.specify/`** — constituição, assessments, templates/workflows Speckit.

## Integração MCP (006, mínimo viável) — verificado em mock-first

Spec: [`specs/006-mcp-stdio-functional-integration/`](specs/006-mcp-stdio-functional-integration/) | Quickstart: [`quickstart.md`](specs/006-mcp-stdio-functional-integration/quickstart.md)

- Transporte/invocação MCP stdio mínima no adapter (`tools/list` / `tools/call`) com normalização para contrato `SkillResult`.
- **FR-005 (seleção, preservada):** modo explícito vence; `mode=mcp` **não** faz reroute silencioso para CLI/fallback; `auto` preserva comportamento **CLI-first/back-compat** quando CLI disponível.
- **FR-006:** taxonomia/metadados de razão aditivos e compatíveis.
- **Stateless por chamada** no boundary atual do adapter (006). Contratos públicos/schemas/CLI/fallback preservados.
- Cobertura determinística (unit/contract/property/selection + helper fake stdio). **Não verificado aqui:** e2e real universal contra todos apps/ambientes.

## Smoke MCP real PhotoCraft (007, Option A stateless, opt-in) — escopo limitado

Spec: [`specs/007-photocraft-mcp-smoke/`](specs/007-photocraft-mcp-smoke/) | Runbook/evidência: [`quickstart.md`](specs/007-photocraft-mcp-smoke/quickstart.md)

Prova **opcional, explicitamente autorizada**, *test-only* (reusa adapter 006), **nunca em CI/default**:

- **Opt-in:** `ARTCRAFT_MCP_INTEGRATION=1`.
- **Binário:** `ARTCRAFT_MCP_PHOTOCRAFT_BIN` (absoluto, preferido) ou resolução PATH apenas em modo opt-in lançando executável absoluto resolvido; identidade/versão registradas quando disponíveis.
- **Raízes seguras (absolutas):** temp roots auto-criadas/limpas por padrão; overrides explícitos (`ARTCRAFT_MCP_READ_ROOT`/`ARTCRAFT_MCP_WRITE_ROOT` ou args do harness) são gerenciados pelo mantenedor (não auto-deletados).
- **Timeout limitado**; parsing defensivo/version-tolerant.
- **Prova determinística (stateless):** `tools/list` + `tools/call name=command_list` (presença de capability `command_list`, resultado não-erro/normalizável). Sem reuso de sessão, **sem** ciclo de artefato cross-call.

**Evidência observada local autorizada (2026-11-06, escopo limitado):** `photocraft-cli 0.20.1` (absoluto), temp roots limpas, `command_list` presente, chamada ok/normalizável (`stateless/session_reuse=false/artifact_cycle=false`). Detalhes completos em [`specs/007-photocraft-mcp-smoke/quickstart.md`](specs/007-photocraft-mcp-smoke/quickstart.md).

## O que este projeto NÃO faz (limites explícitos)

- Não reimplementa modelos/provedores de geração, nem backend próprio; não substitui apps ArtCraft.
- Não executa smoke MCP real em **CI/default**; exige opt-in + autorização explícita + controles de segurança.
- **Não prova/implementa geração IA** via caminho de smoke local PhotoCraft MCP (007 = automação **engine/editor stateless**), nem roteamento provider/modelo/prompt nesse caminho.
- Não implementa sessão MCP stateful/ciclo determinístico de artefato cross-call (`doc_new → command → doc_export`) no adapter atual (**007 Option B adiada**, spec separada).
- Não garante funcionamento sem binários/apps/credenciais/ambientes externos; ausência de execução autorizada = **não exercido/não atestado**.
- Não fabrica evidência; reivindicações devem corresponder ao escopo verificado.

## Documentação

- [`OBJETIVO.md`](OBJETIVO.md) — visão, estado, gaps e não-objetivos.
- [`ROADMAP.md`](ROADMAP.md) — fases, progresso (~95% fundação + MCP mínimo + smoke real stateless autorizado) e próximos passos.
- [`AGENTS.md`](AGENTS.md) — diretrizes de engenharia/arquitetura para agentes.
- [`docs/`](docs/) — `architecture.md`, `core-abstractions.md`, `cross-product.md`, `generalizable-workflows.md`, `skill-authoring.md`, [`docs/research/`](docs/research/).
- Specs MCP: [`specs/006-mcp-stdio-functional-integration/`](specs/006-mcp-stdio-functional-integration/), [`specs/007-photocraft-mcp-smoke/`](specs/007-photocraft-mcp-smoke/).

## Licença e contribuição

- Licença: [MIT](LICENSE) (MDMV Laboratorio de Solucoes Digitais, 2026).
- Não há `CONTRIBUTING.md` na raiz neste momento. Contribuições: siga `AGENTS.md`, mantenha contratos públicos/back-compat, use TDD/testes determinísticos quando aplicável, valide com os gates acima e preserve os limites de segurança/evidência descritos aqui (especialmente opt-in MCP real e não-overclaim).
