"""Canonicalize SkillResult for golden-master / differential comparison."""

from typing import Any, Dict


def canonicalize_skill_result(res: Any) -> Dict[str, Any]:
    """Return a stable dict for comparison, pinning volatile timing fields."""
    if not hasattr(res, "success"):
        return {}
    metadata = dict(getattr(res, "metadata", {}) or {})
    # Pin volatile timing fields to stable values.
    if "duration_ms" in metadata:
        metadata["duration_ms"] = None
    if "timeout_s" in metadata and metadata.get("timeout_s") is not None:
        metadata["timeout_s"] = metadata.get("timeout_s", 300)
    data = getattr(res, "data", None)
    if isinstance(data, dict):
        data = {k: data.get(k) for k in sorted(data.keys())}
    return {
        "success": getattr(res, "success", None),
        "data": data,
        "error": getattr(res, "error", None),
        "metadata": {k: metadata[k] for k in sorted(metadata.keys())},
    }
