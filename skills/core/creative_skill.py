"""Shared base class for creative skills using ArtCraft CLI/MCP adapter."""

import json
import subprocess
import threading
import time
import random
import os
from typing import Any, Dict, Optional, List

from skills.core.base_skill import BaseSkill, SkillResult
from skills.core import artcraft_app_client


class CreativeSkill(BaseSkill):
    """Base class encapsulating discover→resolve→invoke→normalize→degrade flow."""

    def __init__(self, name: str, description: str, command_keywords: Optional[List[str]] = None):
        super().__init__(name=name, description=description)
        self._command_keywords = command_keywords or []
        self._cli_semaphore = threading.BoundedSemaphore(3)
        self._max_retries = 3
        self._retry_backoff_base = 0.5

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
        """006: stdio MCP considered configured/available when command is present."""
        try:
            cfg_n = self._normalize_mcp_config(cfg or {})
            if cfg_n.get("transport") not in (None, "stdio"):
                return bool(cfg_n.get("command") or cfg_n.get("server"))
            cmd = cfg_n.get("command")
            if isinstance(cmd, str) and cmd.strip():
                return True
            server = cfg_n.get("server")
            if isinstance(server, dict) and server.get("command"):
                return True
            return False
        except Exception:
            return False

    def _mcp_command_list(self, cfg: Dict[str, Any]):
        try:
            return artcraft_app_client.mcp_tools_list(cfg)
        except Exception as e:
            return artcraft_app_client._mcp_failure(
                artcraft_app_client.REASON_MCP_UNAVAILABLE,
                f"MCP tools/list failed: {e}",
                error_stage="discovery",
            )

    def _mcp_command_run(self, cfg: Dict[str, Any], tool_id: str, params: Dict[str, Any], timeout: int):
        try:
            return artcraft_app_client.mcp_tools_call(cfg, tool_id, params, timeout=timeout)
        except Exception as e:
            return artcraft_app_client._mcp_failure(
                artcraft_app_client.REASON_MCP_TOOL_ERROR,
                f"MCP tools/call failed: {e}",
                error_stage="invocation",
                tool=tool_id,
            )

    def _result_from_mcp_error(self, payload: Dict[str, Any], mode: str, tool: Optional[str] = None) -> SkillResult:
        md = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
        md = dict(md)
        md.setdefault("mode", mode)
        md.setdefault("interface", "mcp")
        if tool and not md.get("tool"):
            md["tool"] = tool
        md.setdefault("reason", payload.get("reason") or artcraft_app_client.REASON_MCP_UNAVAILABLE)
        return SkillResult(
            success=False,
            error=payload.get("error") or "MCP operation failed",
            metadata=md,
        )

    def _build_cli_params(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Build params dict for CLI/MCP call. Override in subclasses."""
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

    def _execute_cli_with_fallback(self, inputs: Dict[str, Any], cli_path: str, mode: str) -> SkillResult:
        keywords = inputs.get("command_keywords") or self._command_keywords
        override = inputs.get("generation_command")
        timeout = inputs.get("timeout") or 300
        last_error = None
        for attempt in range(self._max_retries):
            try:
                with self._cli_semaphore:
                    cmds = artcraft_app_client.discover_cli_commands(cli_path, timeout)
                    gen_cmd = self._discover_generation_command(cmds, keywords, override)
                    if not gen_cmd:
                        # Try fallback to editing commands for simple pixel art
                        try:
                            width = inputs.get("width") or 16
                            height = inputs.get("height") or 16
                            output_path = inputs.get("output_path") or f"/tmp/artcraft-{int(time.time())}.png"
                            res = artcraft_app_client.generate_via_editing_commands(cli_path, output_path, int(width), int(height), timeout=timeout)
                            if res.returncode == 0 and os.path.exists(output_path):
                                return SkillResult(success=True, data={"image_path": output_path, "width": width, "height": height}, 
                                                 metadata={"mode": mode, "interface": "cli", "method": "fallback_editing"})
                            last_error = SkillResult(success=False, error="Fallback via editing commands failed", 
                                                    metadata={"mode": mode, "cli_path": cli_path})
                        except Exception as e:
                            last_error = SkillResult(success=False, error=f"No image-generation capability found in app version ({cli_path})", 
                                                    metadata={"mode": mode, "cli_path": cli_path})
                        return last_error
                    params = self._build_cli_params(inputs)
                    res = artcraft_app_client.run_cli_generation(cli_path, gen_cmd, params, timeout)
                    if res.returncode != 0:
                        last_error = SkillResult(
                            success=False,
                            error=res.stderr or "CLI command failed",
                            metadata={"mode": mode, "exit_code": res.returncode, "command": gen_cmd, "duration_ms": None, "timeout_s": timeout},
                        )
                        if attempt < self._max_retries - 1:
                            sleep_time = self._retry_backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                            time.sleep(sleep_time)
                            continue
                        return last_error
                    out = {}
                    if res.stdout:
                        try:
                            out = json.loads(res.stdout)
                        except Exception:
                            out = {"image_path": res.stdout.strip()}
                    data = self._normalize_output(out)
                    return SkillResult(success=True, data=data, metadata={"mode": mode, "command": gen_cmd, "interface": "cli"})
            except subprocess.TimeoutExpired:
                last_error = SkillResult(
                    success=False,
                    error=f"Operation timed out after {timeout}s",
                    metadata={"mode": mode, "timeout_s": timeout},
                )
                if attempt < self._max_retries - 1:
                    sleep_time = self._retry_backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    continue
                return last_error
            except Exception as e:
                last_error = SkillResult(success=False, error=str(e), metadata={"mode": mode})
                if attempt < self._max_retries - 1:
                    sleep_time = self._retry_backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    continue
                return last_error
        return last_error or SkillResult(success=False, error="Unknown error", metadata={"mode": mode})

    def _execute_cli(self, inputs: Dict[str, Any], cli_path: str, mode: str) -> SkillResult:
        return self._execute_cli_with_fallback(inputs, cli_path, mode)

    def _execute_mcp(self, inputs: Dict[str, Any], mode: str) -> SkillResult:
        cfg = inputs.get("mcp_config") or {}
        cfg_n = self._normalize_mcp_config(cfg)
        timeout = inputs.get("timeout") or int(cfg_n.get("timeout") or 300)
        if not self._mcp_available(cfg_n):
            return SkillResult(
                success=False,
                error="MCP server unavailable or misconfigured: provide valid stdio mcp_config.command",
                metadata={"mode": mode, "reason": artcraft_app_client.REASON_MCP_UNAVAILABLE, "interface": "mcp", "error_stage": "launch"},
            )
        try:
            keywords = inputs.get("command_keywords") or self._command_keywords
            override = inputs.get("generation_command")
            cmds_res = self._mcp_command_list(cfg_n)
            if isinstance(cmds_res, dict) and (cmds_res.get("is_error") or cmds_res.get("success") is False):
                return self._result_from_mcp_error(cmds_res, mode)
            gen_cmd = self._discover_generation_command(cmds_res, keywords, override)
            if not gen_cmd:
                return SkillResult(
                    success=False,
                    error="No supported MCP capability found for requested operation",
                    metadata={
                        "mode": mode,
                        "reason": artcraft_app_client.REASON_MCP_MISSING_CAPABILITY,
                        "interface": "mcp",
                        "error_stage": "discovery",
                    },
                )
            params = self._build_cli_params(inputs)
            res = self._mcp_command_run(cfg_n, gen_cmd, params, timeout)
            if isinstance(res, dict) and (res.get("is_error") or res.get("success") is False):
                return self._result_from_mcp_error(res, mode, tool=gen_cmd)
            data = self._normalize_output(res if isinstance(res, dict) else {})
            return SkillResult(
                success=True,
                data=data,
                metadata={"mode": mode, "interface": "mcp", "tool": gen_cmd},
            )
        except Exception as e:
            return SkillResult(
                success=False,
                error=f"MCP execution failed: {e}",
                metadata={"mode": mode, "reason": artcraft_app_client.REASON_MCP_TOOL_ERROR, "interface": "mcp", "error_stage": "invocation"},
            )

    def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        if not self.validate_inputs(inputs):
            if not isinstance(inputs, dict):
                return SkillResult(success=False, error="Invalid input", metadata={})
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
            # FR-005: explicit mode wins, no silent CLI/fallback reroute
            return self._execute_mcp(inputs, mode)
        else:  # auto - back-compatible: CLI first, then MCP when CLI unavailable and MCP configured
            cli_path = self._discover_cli(inputs.get("cli_path"))
            if cli_path:
                return self._execute_cli(inputs, cli_path, mode)
            mcp_cfg = inputs.get("mcp_config") or {}
            if self._mcp_available(mcp_cfg):
                return self._execute_mcp(inputs, mode)
            return SkillResult(
                success=False,
                error="No ArtCraft interface available (CLI or MCP)",
                metadata={"mode": mode, "reason": artcraft_app_client.REASON_NEITHER_AVAILABLE},
            )


__all__ = ["CreativeSkill"]
