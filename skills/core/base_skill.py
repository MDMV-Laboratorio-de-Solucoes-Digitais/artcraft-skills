"""Base skill interface and contracts."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class SkillResult:
    """Result of skill execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseSkill(ABC):
    """Base class for all skills."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_input_schema(self) -> Dict[str, Any]:
        """Return JSON schema for inputs."""
        pass
    
    @abstractmethod
    def get_output_schema(self) -> Dict[str, Any]:
        """Return JSON schema for outputs."""
        pass
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        """Execute the skill."""
        pass
    
    def validate_inputs(self, inputs: Dict[str, Any]) -> bool:
        """Validate inputs against schema."""
        # Basic validation - can be enhanced
        return isinstance(inputs, dict)
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get skill metadata."""
        return {
            'name': self.name,
            'description': self.description,
            'type': 'atomic'
        }
