"""Image Edit Skill - CLI/MCP integration with ArtCraft apps."""

from typing import Any, Dict

from skills.core.creative_skill import CreativeSkill
from skills.core.base_skill import SkillResult
from skills.core import artcraft_app_client


class ImageEditSkill(CreativeSkill):
    """Edit images via ArtCraft app CLI or MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="image-edit",
            description="Edit existing images using ArtCraft app CLI/MCP",
            command_keywords=["edit", "inpaint", "outpaint", "composite", "modify", "change"],
        )

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": ["image", "prompt"],
            "properties": {
                "image": {"type": "string"},
                "prompt": {"type": "string"},
                "mask": {"type": "string"},
                "mode_edit": {"type": "string"},
                "model": {"type": "string"},
                "strength": {"type": "number"},
                "width": {"type": "number"},
                "height": {"type": "number"},
                "aspect_ratio": {"type": "string"},
                "seed": {"type": ["number", "string"]},
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
        if "prompt" not in inputs or not isinstance(inputs.get("prompt"), str) or not inputs.get("prompt").strip():
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        if "width" in inputs and isinstance(inputs["width"], (int, float)) and inputs["width"] <= 0:
            return False
        if "height" in inputs and isinstance(inputs["height"], (int, float)) and inputs["height"] <= 0:
            return False
        return True


__all__ = ["ImageEditSkill"]
