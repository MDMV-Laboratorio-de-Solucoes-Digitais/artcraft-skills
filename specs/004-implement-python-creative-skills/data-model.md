# Data Model: Implement Python Creative Skills

**Feature**: Implement Python Creative Skills
**Slug**: implement-python-creative-skills
**Date**: 2026-11-04

## Entities

### SkillResult

Returned by `skill.execute(inputs)`. Defined in `skills/core/base_skill.py`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `success` | `bool` | Yes | Whether the skill execution succeeded |
| `data` | `dict[str, Any]` | No | Normalized output data (see `normalize_output` contract) |
| `error` | `str \| None` | No | Error message if execution failed |
| `metadata` | `dict[str, Any]` | No | Metadata including `mode`, `command`, `interface`, `cli_path`, `exit_code`, `timeout_s`, `reason` |

### Skill

Abstract base class. Defined in `skills/core/base_skill.py`.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | `str` | Yes | Skill name (kebab-case, matches directory name) |
| `description` | `str` | Yes | Human-readable skill description |

| Method | Returns | Description |
|--------|---------|-------------|
| `get_input_schema()` | `dict[str, Any]` | JSON schema for skill inputs |
| `get_output_schema()` | `dict[str, Any]` | JSON schema for skill outputs |
| `validate_inputs(inputs)` | `bool` | Whether inputs are valid |
| `execute(inputs)` | `SkillResult` | Execute the skill |

### Adapter Function (`skills/core/artcraft_app_client.py`)

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `discover_cli(cli_path=None)` | `(str \| None = None) -> str \| None` | `str \| None` | Discover ArtCraft CLI binary |
| `discover_generation_command(commands, keywords, override)` | `(Mapping\|Sequence\|None, Sequence[str]\|None, str\|None) -> str \| None` | `str \| None` | Discover generation command from commands collection |
| `normalize_output(out, keys)` | `(Mapping\|None, Sequence[str]\|None) -> dict[str, Any]` | `dict[str, Any]` | Normalize CLI/MCP output (default 7 keys) |
| `normalize_mcp_config(cfg)` | `(Mapping\|None) -> dict[str, Any]` | `dict[str, Any]` | Normalize MCP config (ensures `transport` key) |
| `run_cli(cli_path, args, timeout)` | `(str, Sequence[str], int=300) -> CompletedProcess` | `subprocess.CompletedProcess` | Run CLI command |
| `discover_cli_commands(cli_path, timeout)` | `(str, int=300) -> list[dict[str, Any]] \| Any` | `list[dict[str, Any]] \| []` | Discover CLI commands via `commands` subcommand |
| `run_cli_generation(cli_path, command_id, params, timeout)` | `(str, str, Mapping[str, Any], int=300) -> CompletedProcess` | `subprocess.CompletedProcess` | Run generation via CLI |
| `select_mode(requested_mode, cli_available, mcp_available)` | `(str, bool, bool) -> str` | `str` | Pure mode decision (auto/cli/mcp/none) |
| `standardize_error(reason, message, metadata)` | `(str, str, Mapping\|None) -> dict[str, Any]` | `dict[str, Any]` | Transport-neutral error shape |

### Reason Codes

| Code | Value | Usage |
|------|-------|-------|
| `REASON_CLI_NOT_FOUND` | `"cli_not_found"` | CLI binary not found |
| `REASON_MCP_UNAVAILABLE` | `"mcp_unavailable"` | MCP server unavailable |
| `REASON_NEITHER_AVAILABLE` | `"neither_available"` | Neither CLI nor MCP available |
| `REASON_IS_ERROR` | `"is_error"` | Generic error |

### SkillConfig (conceptual, not yet implemented)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | Yes | Skill name |
| `description` | `str` | Yes | Skill description |
| `command_keywords` | `list[str]` | Yes | Keywords for command discovery |
| `command_override` | `str \| None` | No | Explicit command ID override |
| `required_params` | `list[str]` | Yes | Required input parameter names |
| `optional_params` | `dict[str, Any]` | No | Optional parameter defaults |
| `output_keys` | `list[str]` | Yes | Output keys for normalization |
