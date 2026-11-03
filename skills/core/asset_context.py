#!/usr/bin/env python3
"""Shared asset/context/style layer for cross-product workflows."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class AssetContext:
    """Shared context for cross-product asset workflows."""
    assets: Dict[str, Any] = field(default_factory=dict)
    styles: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_asset(self, asset_id: str, asset: Any):
        """Add asset to context."""
        self.assets[asset_id] = asset
        self.history.append({"action": "add_asset", "asset_id": asset_id})
    
    def get_asset(self, asset_id: str) -> Optional[Any]:
        """Get asset from context."""
        return self.assets.get(asset_id)
    
    def add_style(self, style_id: str, style: Any):
        """Add style to context."""
        self.styles[style_id] = style
        self.history.append({"action": "add_style", "style_id": style_id})
    
    def get_style(self, style_id: str) -> Optional[Any]:
        """Get style from context."""
        return self.styles.get(style_id)
    
    def merge(self, other: 'AssetContext'):
        """Merge another context into this one."""
        self.assets.update(other.assets)
        self.styles.update(other.styles)
        self.metadata.update(other.metadata)
        self.history.extend(other.history)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize context to dict."""
        return {
            "assets": self.assets,
            "styles": self.styles,
            "metadata": self.metadata,
            "history": self.history
        }
