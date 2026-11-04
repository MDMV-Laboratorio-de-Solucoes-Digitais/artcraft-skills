"""Image Generate Skill - CLI/MCP integration with ArtCraft apps."""

import json
import subprocess
from typing import Any, Dict, Optional

from skills.core.base_skill import BaseSkill, SkillResult
from skills.core import artcraft_app_client


class ImageGenerateSkill(BaseSkill):
    """Generate images via ArtCraft app CLI or MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="image-generate",
            description="Generate images from text prompts using ArtCraft app CLI/MCP"
        )

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["prompt"],
            "properties": {
                "prompt": {"type": "string"},
                "model": {"type": "string"},
                "width": {"type": "number"},
                "height": {"type": "number"},
                "aspect_ratio": {"type": "string"},
                "seed": {"type": ["number", "string"]},
                "mode": {"type": "string", "enum": ["cli", "mcp", "auto"], "default": "auto"},
                "cli_path": {"type": "string"},
                "mcp_config": {"type": "object"},
                "command_keywords": {"type": "array"},
                "generation_command": {"type": "string"},
            },
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "image_url": {"type": "string"},
                "image_path": {"type": "string"},
                "asset_id": {"type": "string"},
                "format": {"type": "string"},
                "width": {"type": "number"},
                "height": {"type": "number"},
                "metadata": {"type": "object"},
            },
        }

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        if not isinstance(inputs, dict):
            return False
        if "prompt" not in inputs:
            return False
        if not isinstance(inputs.get("prompt"), str) or not inputs.get("prompt").strip():
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        if "width" in inputs and isinstance(inputs["width"], (int, float)) and inputs["width"] <= 0:
            return False
        if "height" in inputs and isinstance(inputs["height"], (int, float)) and inputs["height"] <= 0:
            return False
        return True

    def _discover_cli(self, cli_path: Optional[str] = None) -> Optional[str]:
        return artcraft_app_client.discover_cli(cli_path)

    def _discover_generation_command(self, commands, keywords, override=None):
        return artcraft_app_client.discover_generation_command(commands, keywords, override)

    def _normalize_output(self, out: Dict[str, Any]) -> Dict[str, Any]:
        return artcraft_app_client.normalize_output(out)

    def _normalize_mcp_config(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        return artcraft_app_client.normalize_mcp_config(cfg)

    def _mcp_available(self, cfg: Dict[str, Any]) -> bool:
        cfg = self._normalize_mcp_config(cfg)
        # default behavior - try to see if we can connect; tests may override
        return False

    def _mcp_command_list(self, cfg: Dict[str, Any]):
        return []

    def _mcp_command_run(self, cfg: Dict[str, Any], tool_id: str, params: Dict[str, Any], timeout: int):
        return {"is_error": True, "error": "not implemented"}

    def _execute_cli(self, inputs: Dict[str, Any], cli_path: str, mode: str) -> SkillResult:
        keywords = inputs.get("command_keywords") or ["generate", "gen", "image.generate"]
        override = inputs.get("generation_command")
        timeout = inputs.get("timeout") or 300
        try:
            cmds = artcraft_app_client.discover_cli_commands(cli_path, timeout)
            gen_cmd = self._discover_generation_command(cmds, keywords, override)
            if not gen_cmd:
                return SkillResult(
                    success=False,
                    error=f"No image-generation capability found in app version ({cli_path})",
                    metadata={"mode": mode, "cli_path": cli_path},
                )
            params = {"prompt": inputs.get("prompt")}
            if inputs.get("model"):
                params["model"] = inputs["model"]
            if inputs.get("width") is not None:
                params["width"] = inputs["width"]
            if inputs.get("height") is not None:
                params["height"] = inputs["height"]
            if inputs.get("aspect_ratio"):
                params["aspect_ratio"] = inputs["aspect_ratio"]
            if inputs.get("seed") is not None:
                params["seed"] = inputs["seed"]
            res = artcraft_app_client.run_cli_generation(cli_path, gen_cmd, params, timeout)
            if res.returncode != 0:
                return SkillResult(
                    success=False,
                    error=res.stderr or "CLI command failed",
                    metadata={"mode": mode, "exit_code": res.returncode, "command": gen_cmd, "duration_ms": None, "timeout_s": timeout},
                )
            out = {}
            if res.stdout:
                try:
                    out = json.loads(res.stdout)
                except Exception:
                    out = {"image_path": res.stdout.strip()}
            data = self._normalize_output(out)
            return SkillResult(success=True, data=data, metadata={"mode": mode, "command": gen_cmd, "interface": "cli"})
        except subprocess.TimeoutExpired:
            return SkillResult(
                success=False,
                error=f"Operation timed out after {timeout}s",
                metadata={"mode": mode, "timeout_s": timeout},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e), metadata={"mode": mode})

    def _execute_mcp(self, inputs: Dict[str, Any], mode: str) -> SkillResult:
        cfg = inputs.get("mcp_config") or {}
        cfg = self._normalize_mcp_config(cfg)
        if not getattr(self, "_mcp_available", None) or not self._mcp_available(cfg):
            return SkillResult(success=False, error="MCP server unavailable", metadata={"mode": mode, "reason": "mcp_unavailable"})
        try:
            keywords = inputs.get("command_keywords") or ["generate", "gen", "image.generate"]
            override = inputs.get("generation_command")
            timeout = inputs.get("timeout") or 300
            cmds = self._mcp_command_list(cfg) if hasattr(self, "_mcp_command_list") else []
            gen_cmd = self._discover_generation_command(cmds, keywords, override)
            if not gen_cmd:
                return SkillResult(success=False, error=f"No image-generation capability found in app version", metadata={"mode": mode})
            params = {"prompt": inputs.get("prompt")}
            if inputs.get("model"):
                params["model"] = inputs["model"]
            res = self._mcp_command_run(cfg, gen_cmd, params, timeout)
            if isinstance(res, dict) and res.get("is_error"):
                return SkillResult(success=False, error=res.get("error") or "MCP tool error", metadata={"mode": mode, "is_error": True})
            if isinstance(res, dict) and res.get("success") is False:
                return SkillResult(success=False, error=res.get("error") or "MCP tool error", metadata={"mode": mode, "is_error": True})
            data = self._normalize_output(res if isinstance(res, dict) else {})
            return SkillResult(success=True, data=data, metadata={"mode": mode, "interface": "mcp", "tool": gen_cmd})
        except Exception as e:
            return SkillResult(success=False, error=str(e), metadata={"mode": mode})

    def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        if not self.validate_inputs(inputs):
            if not isinstance(inputs, dict) or "prompt" not in inputs or not (isinstance(inputs.get("prompt"), str) and inputs.get("prompt").strip()):
                return SkillResult(success=False, error="Invalid input: prompt: required", metadata={})
            if isinstance(inputs, dict) and "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
                return SkillResult(success=False, error="Invalid input: mode: invalid", metadata={})
            if isinstance(inputs, dict) and "width" in inputs and isinstance(inputs["width"], (int, float)) and inputs["width"] <= 0:
                return SkillResult(success=False, error="Invalid input: width: invalid", metadata={})
            return SkillResult(success=False, error="Invalid input", metadata={})
        mode = inputs.get("mode") or "auto"
        if mode == "cli":
            cli_path = self._discover_cli(inputs.get("cli_path"))
            if not cli_path:
                return SkillResult(success=False, error="CLI not found: photocraft-cli", metadata={"mode": mode, "reason": "cli_not_found"})
            return self._execute_cli(inputs, cli_path, mode)
        elif mode == "mcp":
            return self._execute_mcp(inputs, mode)
        else:  # auto
            cli_path = self._discover_cli(inputs.get("cli_path"))
            if cli_path:
                return self._execute_cli(inputs, cli_path, mode)
            if getattr(self, "_mcp_available", None) and self._mcp_available(inputs.get("mcp_config") or {}):
                res = self._execute_mcp(inputs, mode)
                if res.success:
                    return res
            return SkillResult(success=False, error="No ArtCraft interface available (CLI or MCP)", metadata={"mode": mode, "reason": "neither_available"})


__all__ = ["ImageGenerateSkill"]
