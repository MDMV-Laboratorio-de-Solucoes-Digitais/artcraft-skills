"""Image Upscale Skill - CLI/MCP integration with ArtCraft apps."""

from typing import Any, Dict

from skills.core.creative_skill import CreativeSkill


class ImageUpscaleSkill(CreativeSkill):
    """Upscale images via ArtCraft app CLI or MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="image-upscale",
            description="Upscale images using ArtCraft app CLI/MCP",
            command_keywords=["upscale", "enhance", "super-resolution", "scale", "resize"],
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
                "timeout": {"type": "number"},
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
        if "image" not in inputs or not inputs.get("image"):
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        if "scale" in inputs and isinstance(inputs["scale"], (int, float)) and inputs["scale"] <= 0:
            return False
        return True


__all__ = ["ImageUpscaleSkill"]
