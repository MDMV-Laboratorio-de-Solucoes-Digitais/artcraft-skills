# Contract: artcraft_app_client

Module: `skills.core.artcraft_app_client`

Version: `__version__` currently `0.2.0` (initial `0.1.0`). Public façade: `__all__`.

## Functions

### discover_cli(cli_path: str | None = None) -> str | None
Discover ArtCraft app CLI binary. Checks provided path, then `shutil.which('photocraft-cli')`, then common locations. Returns `None` when unavailable (never raises).

### discover_generation_command(commands: Mapping[str, Any] | Sequence[Any] | None, keywords: Sequence[str] | None = None, override: str | None = None) -> str | None
Discover generation command from commands list/dict. Uses keyword matching (default: ['generate', 'gen', 'image.generate']). Returns `override` when provided. Returns `None` when no match.

### normalize_output(out: Mapping[str, Any] | None = None, keys: Sequence[str] | None = None) -> dict[str, Any]
Returns a new dict (does not mutate input) with keys from `keys` (default: image_url, image_path, asset_id, format, width, height, metadata), each set from `out` or `None`.

### normalize_mcp_config(cfg: Mapping[str, Any] | None = None) -> dict[str, Any]
Returns a new dict (does not mutate input). Ensures `transport` is set (bridge if bridge/token present, else stdio).

### run_cli(cli_path: str, args: Sequence[str], timeout: int = 300) -> subprocess.CompletedProcess
Runs CLI with subprocess. Timeout/OS errors propagate unchanged.

### discover_cli_commands(cli_path: str, timeout: int = 300) -> list[dict[str, Any]] | Any
Runs `cli_path commands` and returns parsed JSON or `[]` on error.

### run_cli_generation(cli_path: str, command_id: str, params: Mapping[str, Any], timeout: int = 300) -> subprocess.CompletedProcess
Runs `cli_path run --cmd <command_id> --params <json>`.

### select_mode(requested_mode: str, cli_available: bool, mcp_available: bool) -> str
Pure mode decision. Returns one of `cli`, `mcp`, `auto`-resolved concrete mode, or `none`. Raises `ValueError` for invalid `requested_mode`.

### standardize_error(reason: str, message: str, metadata: Mapping[str, Any] | None = None) -> dict[str, Any]
Transport-neutral error shape: `{code, message, details, retryable}` plus provided metadata. Reason codes: `cli_not_found`, `mcp_unavailable`, `neither_available`, `is_error`.