"""Scene Composition skill (T103, SC-003, FR-010)."""
from __future__ import annotations

from typing import Any, Dict, List

from skills.core.base_skill import BaseSkill, SkillResult
from skills.core.asset_context import AssetContext


class SceneCompositionSkill(BaseSkill):
    """Compose scenes from multiple asset types (cross-product workflow)."""

    def get_input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "assets": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Assets to compose (each with id/type/uri or metadata)",
                },
                "layout": {"type": "object"},
                "camera": {"type": "object"},
                "context": {"type": "object"},
            },
            "required": ["assets"],
        }

    def get_output_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "scene_id": {"type": "string"},
                "scene_url": {"type": "string"},
                "asset_ids": {"type": "array", "items": {"type": "string"}},
                "context": {"type": "object"},
            },
            "required": ["scene_id"],
        }

    def validate_inputs(self, inputs: Dict[str, Any]) -> SkillResult:
        assets = inputs.get("assets")
        if not assets or not isinstance(assets, list):
            return SkillResult(success=False, error="assets (non-empty array) is required")
        return SkillResult(success=True, data=inputs)

    def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        v = self.validate_inputs(inputs)
        if not v.success:
            return v
        assets: List[Dict[str, Any]] = inputs["assets"]
        ctx = AssetContext()
        incoming_ctx = inputs.get("context") or {}
        if isinstance(incoming_ctx, dict):
            for k, s in (incoming_ctx.get("styles") or {}).items():
                ctx.add_style(k, s)
            ctx.metadata.update(incoming_ctx.get("metadata") or {})
        asset_ids = []
        for i, asset in enumerate(assets):
            if not isinstance(asset, dict):
                continue
            aid = asset.get("id") or f"asset_{i}"
            asset_ids.append(aid)
            ctx.add_asset(aid, asset)
        scene_id = f"scene_{len(asset_ids)}_{abs(hash(tuple(asset_ids))) % 10**8}"
        scene_url = f"asset://scenes/{scene_id}"
        return SkillResult(
            success=True,
            data={
                "scene_id": scene_id,
                "scene_url": scene_url,
                "asset_ids": asset_ids,
                "context": ctx.to_dict(),
            },
            metadata={"skill": "scene-composition", "asset_count": len(asset_ids)},
        )
