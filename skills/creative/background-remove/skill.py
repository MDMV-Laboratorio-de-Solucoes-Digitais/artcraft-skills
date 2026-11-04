"""Background Remove Skill - CLI/MCP integration with ArtCraft apps."""

from typing import Any, Dict

from skills.core.creative_skill import CreativeSkill


class BackgroundRemoveSkill(CreativeSkill):
    """Remove background via ArtCraft app CLI or MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="background-remove",
            description="Remove image background using ArtCraft app CLI/MCP",
            command_keywords=["background", "remove", "matting", "cutout", "isolate"],
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
                "timeout": {"type": "number"},
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
        if "image" not in inputs or not inputs.get("image"):
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        return True


__all__ = ["BackgroundRemoveSkill"]
