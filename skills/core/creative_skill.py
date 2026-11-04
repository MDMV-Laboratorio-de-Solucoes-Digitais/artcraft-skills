"""Shared base class for creative skills using ArtCraft CLI/MCP adapter."""

import json
import subprocess
from typing import Any, Dict, Optional, List

from skills.core.base_skill import BaseSkill, SkillResult
from skills.core import artcraft_app_client


class CreativeSkill(BaseSkill):
    """Base class encapsulating discover→resolve→invoke→normalize→degrade flow."""

    def __init__(self, name: str, description: str, command_keywords: Optional[List[str]] = None):
        super().__init__(name=name, description=description)
        self._command_keywords = command_keywords or []

    def _discover_cli(self, cli_path: Optional[str] = None) -> Optional[str]:
        return artcraft_app_client.discover_cli(cli_path)

    def _discover_generation_command(self, commands, keywords=None, override=None):
        kws = keywords if keywords is not None else self._command_keywords
        return artcraft_app_client.discover_generation_command(commands, kws, override)

    def _normalize_output(self, out: Dict[str, Any]) -> Dict[str, Any]:
        return artcraft_app_client.normalize_output(out)

    def _normalize_mcp_config(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        return artcraft_app_client.normalize_mcp_config(cfg)

    def _mcp_available(self, cfg: Dict[str, Any]) -> bool:
        cfg = self._normalize_mcp_config(cfg)
        return False

    def _mcp_command_list(self, cfg: Dict[str, Any]):
        return []

    def _mcp_command_run(self, cfg: Dict[str, Any], tool_id: str, params: Dict[str, Any], timeout: int):
        return {"is_error": True, "error": "not implemented"}

    def _build_cli_params(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Build params dict for CLI call. Override in subclasses."""
        params: Dict[str, Any] = {}
        if inputs.get("prompt"):
            params["prompt"] = inputs["prompt"]
        if inputs.get("image"):
            params["image"] = inputs["image"]
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
        if inputs.get("mask"):
            params["mask"] = inputs["mask"]
        if inputs.get("scale") is not None:
            params["scale"] = inputs["scale"]
        if inputs.get("enhance") is not None:
            params["enhance"] = inputs["enhance"]
        if inputs.get("format"):
            params["format"] = inputs["format"]
        if inputs.get("return_mask") is not None:
            params["return_mask"] = inputs["return_mask"]
        if inputs.get("mode_edit"):
            params["mode_edit"] = inputs["mode_edit"]
        if inputs.get("strength") is not None:
            params["strength"] = inputs["strength"]
        return params

    def _execute_cli(self, inputs: Dict[str, Any], cli_path: str, mode: str) -> SkillResult:
        keywords = inputs.get("command_keywords") or self._command_keywords
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
            params = self._build_cli_params(inputs)
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
                    out = {"image_path": res.stdout.strip()} if hasattr(self, '_output_is_mesh') and getattr(self, '_output_is_mesh') else {"image_path": res.stdout.strip()}
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
            return SkillResult(success=False, error="MCP server unavailable", metadata={"mode": mode, "reason": artcraft_app_client.REASON_MCP_UNAVAILABLE})
        try:
            keywords = inputs.get("command_keywords") or self._command_keywords
            override = inputs.get("generation_command")
            timeout = inputs.get("timeout") or 300
            cmds = self._mcp_command_list(cfg) if hasattr(self, "_mcp_command_list") else []
            gen_cmd = self._discover_generation_command(cmds, keywords, override)
            if not gen_cmd:
                return SkillResult(success=False, error="No image-generation capability found in app version", metadata={"mode": mode})
            params = self._build_cli_params(inputs)
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
            # Try to give specific error messages like image-generate does
            if isinstance(inputs, dict):
                if self.name == "image-generate" or "prompt" in getattr(self, '_required_for_prompt', []):
                    pass  # handle below
            # Generic validation error
            if not isinstance(inputs, dict):
                return SkillResult(success=False, error="Invalid input", metadata={})
            # Common cases
            if "prompt" in self.get_input_schema().get("required", []) and ("prompt" not in inputs or not isinstance(inputs.get("prompt"), str) or not inputs.get("prompt").strip()):
                return SkillResult(success=False, error="Invalid input: prompt: required", metadata={})
            if "image" in self.get_input_schema().get("required", []) and ("image" not in inputs or not inputs.get("image")):
                return SkillResult(success=False, error="Invalid input: image: required", metadata={})
            if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
                return SkillResult(success=False, error="Invalid input: mode: invalid", metadata={})
            if "width" in inputs and isinstance(inputs["width"], (int, float)) and inputs["width"] <= 0:
                return SkillResult(success=False, error="Invalid input: width: invalid", metadata={})
            if "height" in inputs and isinstance(inputs["height"], (int, float)) and inputs["height"] <= 0:
                return SkillResult(success=False, error="Invalid input: height: invalid", metadata={})
            return SkillResult(success=False, error="Invalid input", metadata={})

        mode = inputs.get("mode") or "auto"
        if mode == "cli":
            cli_path = self._discover_cli(inputs.get("cli_path"))
            if not cli_path:
                return SkillResult(success=False, error="CLI not found: photocraft-cli", metadata={"mode": mode, "reason": artcraft_app_client.REASON_CLI_NOT_FOUND})
            return self._execute_cli(inputs, cli_path, mode)
        elif mode == "mcp":
            return self._execute_mcp(inputs, mode)
        else:  # auto
            cli_path = self._discover_cli(inputs.get("cli_path"))
            mcp_available = bool(getattr(self, "_mcp_available", None) and self._mcp_available(inputs.get("mcp_config") or {}))
            selected = artcraft_app_client.select_mode("auto", bool(cli_path), mcp_available)
            if selected == "cli" and cli_path:
                return self._execute_cli(inputs, cli_path, mode)
            if selected == "mcp":
                res = self._execute_mcp(inputs, mode)
                if res.success:
                    return res
            return SkillResult(success=False, error="No ArtCraft interface available (CLI or MCP)", metadata={"mode": mode, "reason": artcraft_app_client.REASON_NEITHER_AVAILABLE})


__all__ = ["CreativeSkill"]
