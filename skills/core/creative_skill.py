"""Creative skill base class - shared infrastructure for creative skills.

Provides the discover→invoke→normalize→degrade flow that all
creative skills (image-edit, background-remove, image-upscale, mesh-generate)
share. Each skill is a thin subclass that provides skill-specific keywords,
input/output schemas, and parameter assembly.

Follows the image-generate/skill.py pattern but extracted into a reusable
base class to avoid duplication across creative skills.
"""

from __future__ import annotations

import json
import logging
import subprocess
import threading
import time
from abc import abstractmethod
from typing import Any

from skills.core import artcraft_app_client
from skills.core.base_skill import BaseSkill, SkillResult

logger = logging.getLogger("artcraft-skills")


class CreativeSkill(BaseSkill):
    """Base class for creative skills that wrap the ArtCraft CLI/MCP adapter.

    Provides the shared discovery→invocation→normalization→degrade flow.
    Subclasses must implement:
        - get_input_schema(), get_output_schema() schemas
        - _build_params() for skill-specific parameter assembly
        - _get_default_keywords() for command discovery keywords

    The base class handles:
        - CLI discovery via discover_cli()
        - Command discovery via discover_generation_command()
        - CLI invocation with retry (exponential backoff + jitter)
        - Output normalization via normalize_output()
        - Mode selection via select_mode()
        - Graceful degradation with reason codes
    """

    def __init__(
        self,
        name: str,
        description: str,
        command_keywords: Sequence[str] | None = None,
        generation_command: str | None = None,
    ):
        super().__init__(name, description)
        self.command_keywords = list(command_keywords) if command_keywords else []
        self.generation_command = generation_command
        self._semaphore = threading.Semaphore(3)
        self._retry_max = 3

    @property
    def logger(self) -> logging.Logger:
        return logger

    def _acquire_semaphore(self) -> None:
        """Acquire the concurrency semaphore before CLI invocation."""
        self._semaphore.acquire()

    def _release_semaphore(self) -> None:
        """Release the concurrency semaphore after CLI invocation."""
        self._semaphore.release()

    @abstractmethod
    def _build_params(self, inputs: Mapping[str, Any]) -> dict[str, Any]:
        """Build skill-specific params from validated inputs.

        Subclasses implement this to assemble the params dict that gets
        passed to the CLI run command. Common params (cli_path, mcp_config,
        command_keywords, generation_command, mode) are handled by
        _execute_cli; this method adds skill-specific params.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_default_keywords(self) -> list[str]:
        """Return default keyword list for command discovery.

        Subclasses return their keyword list used to match against the
        photocraft-cli command registry.
        """
        raise NotImplementedError

    def _run_cli_with_retry(
        self,
        cli_path: str,
        args: list[str],
        timeout: int = 300,
        max_retries: int = 3,
    ) -> subprocess.CompletedProcess:
        """Run CLI command with exponential backoff + jitter on failure.

        Retries on subprocess.TimeoutExpired and non-zero return code.
        Uses exponential backoff with jitter: delay = 2^attempt + random(0,1).
        """
        import random

        last_res: subprocess.CompletedProcess | None = None
        last_error: str | None = None

        for attempt in range(max_retries + 1):
            try:
                res = subprocess.run(
                    [cli_path] + list(args),
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                if res.returncode == 0:
                    return res
                last_error = res.stderr or f"CLI command failed (exit code {res.returncode})"
            except subprocess.TimeoutExpired as exc:
                last_error = f"Operation timed out after {timeout}s"
                last_res = exc  # type: ignore[assignment]
            except Exception as exc:
                last_error = str(exc)
                last_res = None  # type: ignore[assignment]

            if attempt < max_retries:
                delay = (2 ** attempt) + random.uniform(0, 1)
                logger.warning(
                    "CLI attempt %d/%d failed: %s. Retrying in %.1fs...",
                    attempt + 1,
                    max_retries + 1,
                    last_error,
                    delay,
                )
                time.sleep(delay)

        # All retries exhausted
        if isinstance(last_res, subprocess.CompletedProcess):
            return last_res
        # Timeout without a CompletedProcess
        raise TimeoutError(last_error or "CLI command timed out")

    def _execute_cli(
        self,
        inputs: Mapping[str, Any],
        cli_path: str,
        mode: str,
    ) -> SkillResult:
        """Execute generation via CLI with discovery, invocation, normalization.

        Follows the image-generate/skill.py pattern:
        1. Discover CLI commands via cli_path commands
        2. Resolve generation command via keyword matching
        3. Build params from skill-specific builder + common params
        4. Run CLI with retry logic
        5. Parse and normalize output
        """
        keywords = inputs.get("command_keywords") or self.command_keywords
        override = inputs.get("generation_command")
        timeout = inputs.get("timeout") or 300

        self._acquire_semaphore()
        try:
            # Discover CLI commands
            cmds = artcraft_app_client.discover_cli_commands(cli_path, timeout)
            gen_cmd = artcraft_app_client.discover_generation_command(
                cmds, keywords, override
            )
            if not gen_cmd:
                return SkillResult(
                    success=False,
                    error=f"No {self.name} capability found in app version ({cli_path})",
                    metadata={"mode": mode, "cli_path": cli_path},
                )

            # Build params from skill-specific builder + common params
            params = self._build_params(inputs)
            params["command"] = gen_cmd

            # Run CLI with retry
            res = self._run_cli_with_retry(
                cli_path,
                ["run", "--cmd", gen_cmd, "--params", json.dumps(params)],
                timeout,
            )

            if res.returncode != 0:
                return SkillResult(
                    success=False,
                    error=res.stderr or "CLI command failed",
                    metadata={
                        "mode": mode,
                        "exit_code": res.returncode,
                        "command": gen_cmd,
                        "timeout_s": timeout,
                    },
                )

            # Parse and normalize output
            out: dict[str, Any] = {}
            if res.stdout:
                try:
                    out = json.loads(res.stdout)
                except Exception:
                    out = {"image_path": res.stdout.strip()}
            data = artcraft_app_client.normalize_output(out)
            return SkillResult(
                success=True,
                data=data,
                metadata={"mode": mode, "command": gen_cmd, "interface": "cli"},
            )
        except subprocess.TimeoutExpired:
            return SkillResult(
                success=False,
                error=f"Operation timed out after {timeout}s",
                metadata={"mode": mode, "timeout_s": timeout},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e), metadata={"mode": mode})
        finally:
            self._release_semaphore()

    def _execute_mcp(self, inputs: Mapping[str, Any], mode: str) -> SkillResult:
        """Execute via MCP stub - MCP discovery/invocation stay skill-level per FR-005.

        The adapter only normalizes MCP config/output. Discovery/invocation
        remain skill-level. This stub returns unavailable so the skill falls
        back to CLI or reports neither_available.
        """
        cfg = inputs.get("mcp_config") or {}
        cfg = artcraft_app_client.normalize_mcp_config(cfg)

        return SkillResult(
            success=False,
            error="MCP server unavailable",
            metadata={
                "mode": mode,
                "reason": artcraft_app_client.REASON_MCP_UNAVAILABLE,
            },
        )

    def execute(self, inputs: Mapping[str, Any]) -> SkillResult:
        """Execute the skill with mode selection, CLI/MCP dispatch,
        and graceful degradation.

        Flow:
        1. Validate inputs
        2. Discover CLI availability and MCP availability
        3. Call select_mode to decide transport
        4. Dispatch to CLI or MCP execution
        5. Return SkillResult with canonicalized output
        """
        if not self.validate_inputs(inputs):
            return SkillResult(
                success=False,
                error="Invalid input",
                metadata={},
            )

        mode = inputs.get("mode") or "auto"
        cli_path = inputs.get("cli_path")
        mcp_config = inputs.get("mcp_config") or {}

        cli_available = artcraft_app_client.discover_cli(cli_path) is not None
        mcp_available = bool(
            getattr(self, "_mcp_available", None)
            and self._mcp_available(mcp_config)
        )

        selected = artcraft_app_client.select_mode(
            requested_mode=mode,
            cli_available=cli_available,
            mcp_available=mcp_available,
        )

        if selected == "cli" and cli_path:
            return self._execute_cli(inputs, cli_path, mode)
        if selected == "mcp":
            res = self._execute_mcp(inputs, mode)
            if res.success:
                return res
        return SkillResult(
            success=False,
            error="No ArtCraft interface available (CLI or MCP)",
            metadata={
                "mode": mode,
                "reason": artcraft_app_client.REASON_NEITHER_AVAILABLE,
            },
        )