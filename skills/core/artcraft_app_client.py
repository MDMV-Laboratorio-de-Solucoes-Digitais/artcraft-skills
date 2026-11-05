"""Shared CLI/MCP adapter for ArtCraft apps.

Extracted from skills.creative.image-generate to enable reuse across
creative skills (image-edit, background-remove, image-upscale, mesh-generate, etc.)
following Constitution v2.1.0 (CLI/MCP only, no API).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from typing import Any

__version__ = "0.2.0"

REASON_CLI_NOT_FOUND = "cli_not_found"
REASON_MCP_UNAVAILABLE = "mcp_unavailable"
REASON_NEITHER_AVAILABLE = "neither_available"
REASON_IS_ERROR = "is_error"


def discover_cli(cli_path: str | None = None) -> str | None:
    """Discover ArtCraft app CLI binary.

    Checks provided path, then ``shutil.which('photocraft-cli')``, then common
    locations. Returns ``None`` when unavailable (never raises).
    """
    if cli_path:
        if os.path.exists(cli_path):
            return cli_path
        return None
    path = shutil.which("photocraft-cli")
    if path:
        return path
    common = [
        "/usr/bin/photocraft-cli",
        os.path.expanduser("~/.local/bin/photocraft-cli"),
        "/Applications/PhotoCraft.app/Contents/MacOS/photocraft-cli",
    ]
    for c in common:
        if os.path.exists(c):
            return c
    return None


def discover_generation_command(
    commands: Mapping[str, Any] | Sequence[Any] | None = None,
    keywords: Sequence[str] | None = None,
    override: str | None = None,
) -> str | None:
    """Discover generation command/tool from a commands collection."""
    if override:
        return override
    if not keywords:
        keywords = ["generate", "gen", "image.generate"]
    cmd_list: list[Any] = []
    if isinstance(commands, Mapping):
        cmd_list = list(commands.get("commands") or commands.get("items") or [])
    elif isinstance(commands, Sequence) and not isinstance(commands, (str, bytes)):
        cmd_list = list(commands)
    for cmd in cmd_list:
        if isinstance(cmd, Mapping):
            cid = cmd.get("id") or cmd.get("name") or ""
            label = cmd.get("label") or cmd.get("description") or ""
        else:
            cid = str(cmd)
            label = ""
        cid_l = str(cid).lower()
        label_l = str(label).lower()
        for k in keywords:
            k_l = str(k).lower()
            if k_l in cid_l or k_l in label_l:
                return str(cid) if cid is not None else None
    return None


def normalize_output(
    out: Mapping[str, Any] | None = None,
    keys: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Normalize CLI/MCP output to a standard format. Does not mutate input."""
    if not isinstance(out, Mapping):
        out = {}
    if not keys:
        keys = ["image_url", "image_path", "asset_id", "format", "width", "height", "metadata"]
    result: dict[str, Any] = {}
    for key in keys:
        result[key] = out.get(key)
    return result


def normalize_mcp_config(cfg: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Normalize MCP configuration. Does not mutate input."""
    if not isinstance(cfg, Mapping):
        cfg = {}
    result = dict(cfg)
    if "transport" not in result:
        if result.get("bridge") or result.get("token"):
            result["transport"] = "bridge"
        else:
            result["transport"] = "stdio"
    return result


def run_cli(cli_path: str, args: Sequence[str], timeout: int = 300) -> subprocess.CompletedProcess:
    """Run CLI command with standard error handling."""
    return subprocess.run([cli_path] + list(args), capture_output=True, text=True, timeout=timeout)


def discover_cli_commands(cli_path: str, timeout: int = 300) -> list[dict[str, Any]] | Any:
    """Discover available CLI commands."""
    try:
        res = run_cli(cli_path, ["commands"], timeout=timeout)
        if res.returncode == 0 and res.stdout:
            try:
                parsed = json.loads(res.stdout)
                return parsed
            except Exception:
                return []
        return []
    except Exception:
        return []


def run_cli_generation(
    cli_path: str,
    command_id: str,
    params: Mapping[str, Any],
    timeout: int = 300,
) -> subprocess.CompletedProcess:
    """Run generation via CLI."""
    args = ["run", "--cmd", command_id, "--params", json.dumps(params)]
    return run_cli(cli_path, args, timeout=timeout)


def select_mode(requested_mode: str, cli_available: bool, mcp_available: bool) -> str:
    """Pure mode decision."""
    if requested_mode not in ("auto", "cli", "mcp"):
        raise ValueError(f"Invalid mode: {requested_mode}")
    if requested_mode == "cli":
        return "cli"
    if requested_mode == "mcp":
        return "mcp"
    if cli_available:
        return "cli"
    if mcp_available:
        return "mcp"
    return "none"


def standardize_error(
    reason: str,
    message: str,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a transport-neutral error shape."""
    if metadata is None:
        metadata = {}
    result: dict[str, Any] = {
        "code": reason,
        "message": message,
        "details": dict(metadata),
        "retryable": reason in ("timeout",),
    }
    for k, v in metadata.items():
        if k not in result:
            result[k] = v
    return result


def generate_via_editing_commands(
    cli_path: str,
    output_path: str,
    width: int = 16,
    height: int = 16,
    color: tuple = (101, 67, 33, 255),
    timeout: int = 300,
) -> subprocess.CompletedProcess:
    """Fallback: generate simple pixel art using available editing commands."""
    params = {"width": width, "height": height}
    args = ["run", "--new", json.dumps(params), "--cmd", "paint.bucket", 
            "--params", json.dumps({"color": list(color)}), "--out", output_path]
    return run_cli(cli_path, args, timeout=timeout)


__all__ = [
    "discover_cli",
    "discover_generation_command",
    "normalize_output",
    "normalize_mcp_config",
    "run_cli",
    "discover_cli_commands",
    "run_cli_generation",
    "select_mode",
    "standardize_error",
    "generate_via_editing_commands",
]
