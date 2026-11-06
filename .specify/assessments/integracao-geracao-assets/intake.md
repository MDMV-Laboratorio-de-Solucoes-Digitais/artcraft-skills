# Idea Intake: Integração de geração de assets com ArtCraft

- **Slug**: integracao-geracao-assets
- **Created**: 2026-11-05
- **Source**: "pasted text"
- **Type**: improvement

## Idea (as captured)

> "1. Usar o CLI/MCP que realmente expõe comandos de geração - Se o Photocraft/ArtCraft app neste ambiente tiver uma interface de geração, precisamos descobrir quais são esses comandos e configurar generation_command ou command_keywords para apontá-los.
> 2. Estender as skills para usar comandos de edição disponíveis - Como photocraft-cli tem paint.bucket, edit.fill, paint.stroke, etc., poderíamos criar um caminho alternativo nas skills para gerar pixel art simples usando esses comandos quando não houver comandos de geração."

## Restated

Melhorar a integração das skills criativas do ArtCraft com os aplicativos reais (Photocraft e derivados) para gerar assets necessários aos projetos da MDMV. Quando houver comandos de geração disponíveis via CLI/MCP, usá-los; caso contrário, estender o fluxo para gerar assets simples usando comandos de edição disponíveis no photocraft-cli.

## Origin & Context

- **Raised by**: Usuário (contexto: tentativa de gerar assets para projetos Stardew Valley usando skills criativas)
- **Trigger**: Ao tentar usar as skills `image-generate`/`image-edit` via CLI, o adapter não encontrou comandos de geração no `photocraft-cli` deste ambiente (apenas comandos de edição/documento), resultando em falha graciosa mas sem geração de assets

## First-Glance Unknowns

- [NEEDS CLARIFICATION: Quais comandos de geração existem realmente no Photocraft/ArtCraft apps instalados neste ambiente?]
- [NEEDS CLARIFICATION: Existe MCP server ativo ou configurado que exponha ferramentas de geração?]
- [NEEDS CLARIFICATION: Quais capacidades de geração estão disponíveis (texto-para-imagem, edição, etc.)?]
- [NEEDS CLARIFICATION: Devemos estender as skills existentes (`image-generate`, `image-edit`) ou criar um novo caminho na `CreativeSkill` base class?]
- [NEEDS CLARIFICATION: Qual o escopo - apenas pixel art simples ou geração geral?]
