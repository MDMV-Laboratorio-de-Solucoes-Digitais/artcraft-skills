"""Mesh Generate Skill - CLI/MCP integration with ArtCraft apps."""

from typing import Any, Dict

from skills.core.creative_skill import CreativeSkill


class MeshGenerateSkill(CreativeSkill):
    """Generate meshes via ArtCraft app CLI or MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="mesh-generate",
            description="Generate 3D meshes using ArtCraft app CLI/MCP",
            command_keywords=["mesh", "3d", "mesh.generate", "image-to-3d", "model"],
        )

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "required": [],
            "properties": {
                "prompt": {"type": "string"},
                "image": {"type": "string"},
                "model": {"type": "string"},
                "format": {"type": "string"},
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
                "mesh_url": {"type": "string"},
                "mesh_path": {"type": "string"},
                "asset_id": {"type": "string"},
                "format": {"type": "string"},
                "metadata": {"type": "object"},
            },
        }

    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        if not isinstance(inputs, dict):
            return False
        if not inputs.get("prompt") and not inputs.get("image"):
            return False
        if "mode" in inputs and inputs["mode"] not in ("cli", "mcp", "auto"):
            return False
        return True


__all__ = ["MeshGenerateSkill"]
