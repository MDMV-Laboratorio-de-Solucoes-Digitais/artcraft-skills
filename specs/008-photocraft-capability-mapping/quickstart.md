# Quickstart: PhotoCraft MCP capability mapping (008)

**Purpose**: revisar e usar o mapeamento de capacidades PhotoCraft MCP (docs-only). **Não** executa MCP real por padrão.

## 1) Revisão documental (default)

```bash
cd /home/luis/development/artcraft-skills
# Gates de regressão (docs-only; esperados verdes)
PYTHONPATH=. python -m pytest -q
python scripts/validate_all_skills.py
```

Revisar:
- `specs/008-photocraft-capability-mapping/spec.md` (FR/SC, exclusões)
- `contracts/capability-map-contract.md` (gating defensivo, evidência)
- `checklists/requirements.md`
- Assessment GO: `.specify/assessments/008-photocraft-capability-mapping/decision.md`

## 2) Como usar o mapa (para specs/skills futuras)

1. Rodar discovery defensiva: `tools/list`; para engine commands, `command_list` (padrões 006/007).
2. Confirmar presença de tool/command e parâmetros antes de invocar; não assumir contagem/catálogo fixo.
3. Respeitar roots, overwrite/format constraints, timeout e FR-006.
4. **Recusar** claims de geração IA e **não** assumir ciclo cross-call stateful (adapter 006 stateless; 007 Option B deferida).
5. Bridge/UI/headless boundary: usar apenas escopo headless salvo spec separada.

## 3) Validação real opt-in futura (NÃO executar agora)

Somente com **autorização explícita** e ambiente controlado, reutilizar controles do runbook 007 (`specs/007-photocraft-mcp-smoke/quickstart.md`):
- `ARTCRAFT_MCP_INTEGRATION=1` (ou mecanismo equivalente definido pela spec futura)
- binário absoluto explícito preferido; PATH só em modo opt-in
- read/write roots absolutos seguros; temp roots auto-criadas limpas; overrides explícitos maintainer-managed
- timeout limitado; cleanup; sem segredos/PII
- evidência registra: versão/binário, tools/capability observada, stateless boundary, limites, **sem claim de IA**
- **nunca** CI/default

## 4) Limites explícitos

- Engine/editor automation only. No prompt-based AI generation/provider/model routing.
- No stateful MCP cross-call artifact cycle in current adapter (007 Option B deferred; MCP 2026-07-28 considerations apply).
- No bridge/UI/desktop control token scope in 008.
- Capability/protocol details may drift by `photocraft-cli` version; treat observed data as scoped evidence.