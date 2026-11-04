"""Image Upscale Skill - CLI/MCP integration with ArtCraft apps.

Enhances and upscales images with AI-powered upscaling using the shared
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


class ImageUpscaleSkill(CreativeSkill):
    """Upscale images via ArtCraft app CLI/MCP with AI-powered upscaling."""

    def __init__(self):
        super().__init__(
            name="image-upscale",
            description="Enhance and upscale images with AI-powered upscaling using ArtCraft app CLI/MCP",
            command_keywords=["upscale", "enhance", "super-resolution", "scale", "resize"],
            generation_command=None,
        )

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["image"],
            "properties": {
                "image": {"type": "string"},
                "scale": {"type": "number"},
                "model": {"type": "string"},
                "enhance": {"type": "boolean"},
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
        if "image" not in inputs:
            return False
        if not isinstance(inputs.get("image"), str) or not inputs.get("image").strip():
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        if "width" in inputs and isinstance(inputs["width"], (int, float)) and inputs["width"] <= 0:
            return False
        if "height" in inputs and isinstance(inputs["height"], (int, float)) and inputs["height"] <= 0:
            return False
        return True

    def _build_params(self, inputs: Dict[str, Any]) -> dict[str, Any]:
        params: dict[str, Any] = {
            "image": inputs.get("image"),
        }
        if inputs.get("scale") is not None:
            params["scale"] = inputs["scale"]
        if inputs.get("model"):
            params["model"] = inputs["model"]
        if inputs.get("enhance") is not None:
            params["enhance"] = inputs["enhance"]
        return params

    def _get_default_keywords(self) -> list[str]:
        return ["upscale", "enhance", "super-resolution", "scale", "resize"]


__all__ = ["ImageUpscaleSkill"]


def main() -> None:
    """CLI entry point for testing the skill directly."""
    import sys

    skill = ImageUpscaleSkill()
    if len(sys.argv) < 2:
        print("Usage: python -m skills.creative.image-upscale.skill <image_path> [mode]")
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