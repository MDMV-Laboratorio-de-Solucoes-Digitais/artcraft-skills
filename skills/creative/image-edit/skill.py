"""Image Edit Skill - CLI/MCP integration with ArtCraft apps."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Dict, Optional

from skills.core.base_skill import BaseSkill, SkillResult
from skills.core import artcraft_app_client
from skills.core.creative_skill import CreativeSkill


class ImageEditSkill(CreativeSkill):
    """Edit images via ArtCraft app CLI/MCP (no API)."""

    def __init__(self):
        super().__init__(
            name="image-edit",
            description="Edit images with inpainting, outpainting, and compositing capabilities using ArtCraft app CLI/MCP",
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
                "mode_edit": {"type": "string", "enum": ["inpaint", "outpaint", "composite"]},
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
        if "image" not in inputs or not isinstance(inputs.get("image"), str) or not inputs.get("image").strip():
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

    def _build_params(self, inputs: Mapping[str, Any]) -> dict[str, Any]:
        """Build CLI generation params from validated inputs."""
        params: dict[str, Any] = {
            "image": inputs.get("image"),
            "prompt": inputs.get("prompt"),
        }
        if inputs.get("mask"):
            params["mask"] = inputs["mask"]
        if inputs.get("mode_edit"):
            params["mode"] = inputs["mode_edit"]
        if inputs.get("model"):
            params["model"] = inputs["model"]
        if inputs.get("strength") is not None:
            params["strength"] = inputs["strength"]
        if inputs.get("width") is not None:
            params["width"] = inputs["width"]
        if inputs.get("height") is not None:
            params["height"] = inputs["height"]
        if inputs.get("aspect_ratio"):
            params["aspect_ratio"] = inputs["aspect_ratio"]
        if inputs.get("seed") is not None:
            params["seed"] = inputs["seed"]
        return params

    def _get_default_keywords(self) -> list[str]:
        return ["edit", "inpaint", "outpaint", "composite", "modify", "change"]


__all__ = ["ImageEditSkill"]

