"""Core utilities for ArtCraft Skills."""
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional


class SkillError(Exception):
    """Base exception for skill errors."""
    pass


class SkillValidationError(SkillError):
    """Skill validation error."""
    pass


class SkillExecutionError(SkillError):
    """Skill execution error."""
    pass


def setup_logging(name: str = "artcraft-skills") -> logging.Logger:
    """Setup logging for skills."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value from environment or defaults."""
    return os.environ.get(f"ARTCRAFT_SKILLS_{key.upper()}", default)


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path
