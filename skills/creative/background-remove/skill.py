"""Background Remove Skill - CLI/MCP integration with ArtCraft apps.

Removes backgrounds from images with precise matting using the shared
CLI/MCP adapter.
"""

from __future__ import annotations

from typing import Any, Dict

from skills.core.artcraft_app_client import (
    REASON_CLI_NOT_FOUND,
    REASON_MCP_UNAVAILABLE,
    REASON_NEITHER_AVAILABLE,
)
from skills.core.base_skill import BaseSkill, SkillResult
from skills.core.creative_skill import CreativeSkill


class BackgroundRemoveSkill(CreativeSkill):
    """Remove backgrounds from images with precise matting via ArtCraft
    app CLI/MCP."""

    def __init__(self):
        super().__init__(
            name="background-remove",
            description="Remove backgrounds and isolate subjects with precise matting using ArtCraft app CLI/MCP",
            command_keywords=["background", "remove", "matting", "cutout", "isolate"],
            generation_command=None,
        )

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["image"],
            "properties": {
                "image": {"type": "string"},
                "model": {"type": "string"},
                "return_mask": {"type": "boolean"},
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
                "mask_url": {"type": "string"},
                "asset_id": {"type": "string"},
                "format": {"type": "string"},
                "metadata": {"type": "object"},
            },
        }

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        if not isinstance(inputs, dict):
            return False
        if "image" not in inputs:
            return False
        if not isinstance(inputs.get("image"), str) or not inputs.get("image").strip():
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        return True

    def _build_params(self, inputs: Dict[str, Any]) -> dict[str, Any]:
        params: dict[str, Any] = {
            "image": inputs.get("image"),
        }
        if inputs.get("model"):
            params["model"] = inputs["model"]
        if inputs.get("return_mask") is not None:
            params["return_mask"] = inputs["return_mask"]
        return params

    def _get_default_keywords(self) -> list[str]:
        return ["background", "remove", "matting", "cutout", "isolate"]


__all__ = ["BackgroundRemoveSkill"]


def main() -> None:
    """CLI entry point for testing the skill directly."""
    import sys

    skill = BackgroundRemoveSkill()
    if len(sys.argv) < 2:
        print("Usage: python -m skills.creative.background-remove.skill <image_path> [mode]")
        sys.exit(1)

    image_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "auto"

    result = skill.execute({"image": image_path, "mode": mode})
    if result.success:
        print(f"Success: {result.data}")
    else:
        print(f"Error: {result.error} (reason: {result.metadata.get('reason')})")
        sys.exit(1)


if __name__ == "__main__":
    main()