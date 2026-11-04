# Data Model: Shared CLI/MCP Adapter

## Entities

### Adapter Functions (Module Interface)
- `discover_cli(cli_path: str | None = None) -> str | None` - Find CLI binary
- `discover_generation_command(commands, keywords=None, override=None) -> str | None` - Find generation command
- `normalize_output(out=None, keys=None) -> dict[str, Any]` - Normalize output (new dict; no mutation)
- `normalize_mcp_config(cfg=None) -> dict[str, Any]` - Normalize MCP config (new dict; no mutation)
- `run_cli(cli_path, args, timeout=300) -> subprocess.CompletedProcess` - Run CLI
- `discover_cli_commands(cli_path, timeout=300) -> list[dict[str, Any]] | Any` - Discover commands
- `run_cli_generation(cli_path, command_id, params, timeout=300) -> subprocess.CompletedProcess` - Run generation
- `select_mode(requested_mode, cli_available, mcp_available) -> str` - Pure mode decision
- `standardize_error(reason, message, metadata=None) -> dict[str, Any]` - Transport-neutral error

No persistent entities - all stateless utilities. Module exposes `__all__` and `__version__` (currently `0.2.0`; initial `0.1.0`).