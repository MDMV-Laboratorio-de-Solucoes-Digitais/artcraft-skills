"""Asset/Media Handler for managing creative assets."""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class AssetType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    MESH_3D = "3d_mesh"
    SPLAT_3D = "3d_splat"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"


@dataclass
class Asset:
    asset_id: str
    asset_type: AssetType
    format: str
    url: Optional[str] = None
    media_token: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AssetHandler:
    """Handle assets across different formats and providers."""
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
    
    def upload(self, asset_data: bytes, asset_type: AssetType, 
               metadata: Dict[str, Any] = None) -> Asset:
        """Upload asset."""
        import uuid
        asset_id = str(uuid.uuid4())
        asset = Asset(
            asset_id=asset_id,
            asset_type=asset_type,
            format=metadata.get('format', 'unknown') if metadata else 'unknown',
            metadata=metadata or {}
        )
        self.assets[asset_id] = asset
        return asset
    
    def get(self, asset_id: str) -> Optional[Asset]:
        """Get asset by ID."""
        return self.assets.get(asset_id)
    
    def list(self, asset_type: Optional[AssetType] = None) -> List[Asset]:
        """List assets."""
        assets = list(self.assets.values())
        if asset_type:
            assets = [a for a in assets if a.asset_type == asset_type]
        return assets
