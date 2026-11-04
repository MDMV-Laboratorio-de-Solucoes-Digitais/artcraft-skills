# Quickstart: Implement Python Creative Skills

**Feature**: Implement Python Creative Skills
**Slug**: implement-python-creative-skills
**Date**: 2026-11-04

## Prerequisites

- Python 3.11+
- `photocraft-cli` installed and available on PATH (or provide `cli_path` parameter)
- ArtCraft app CLI (PhotoCraft) installed
- Repository at `/home/luis/development/artcraft-skills`

## Installation

No installation required — this feature adds Python skill files to the existing ArtCraft Skills Suite repository.

## Quickstart: Run Each Skill

### 1. image-edit

Edit an image using the image-edit skill:

```python
from skills.creative.image_edit.skill import ImageEditSkill

skill = ImageEditSkill()
result = skill.execute({
    "image": "/path/to/input.png",
    "prompt": "make it blue",
    "mode": "cli",
    "cli_path": "/usr/bin/photocraft-cli",
})

if result.success:
    print(f"Edited image: {result.data.get('image_path')}")
else:
    print(f"Error: {result.error} (reason: {result.metadata.get('reason')})")
```

### 2. background-remove

Remove background from an image:

```python
from skills.creative.background_remove.skill import BackgroundRemoveSkill

skill = BackgroundRemoveSkill()
result = skill.execute({
    "image": "/path/to/input.png",
    "mode": "cli",
    "cli_path": "/usr/bin/photocraft-cli",
})

if result.success:
    print(f"Background removed: {result.data.get('image_path')}")
else:
    print(f"Error: {result.error} (reason: {result.metadata.get('reason')})")
```

### 3. image-upscale

Upscale an image 2x:

```python
from skills.creative.image_upscale.skill import ImageUpscaleSkill

skill = ImageUpscaleSkill()
result = skill.execute({
    "image": "/path/to/input.png",
    "scale": 2,
    "mode": "cli",
    "cli_path": "/usr/bin/photocraft-cli",
})

if result.success:
    print(f"Upscaled image: {result.data.get('image_path')}")
else:
    print(f"Error: {result.error} (reason: {result.metadata.get('reason')})")
```

### 4. mesh-generate

Generate a 3D mesh from a text prompt:

```python
from skills.creative.mesh_generate.skill import MeshGenerateSkill

skill = MeshGenerateSkill()
result = skill.execute({
    "prompt": "a low-poly tree",
    "mode": "cli",
    "cli_path": "/usr/bin/photocraft-cli",
})

if result.success:
    print(f"Mesh generated: {result.data.get('mesh_path')}")
else:
    print(f"Error: {result.error} (reason: {result.metadata.get('reason')})")
```

## Validation

Validate each skill:

```bash
python scripts/validate_skill.py skills/creative/image-edit
python scripts/validate_skill.py skills/creative/background-remove
python scripts/validate_skill.py skills/creative/image-upscale
python scripts/validate_skill.py skills/creative/mesh-generate
```

Validate all skills:

```bash
python scripts/validate_all_skills.py
```

## Expected Outputs

Each successful skill execution returns a `SkillResult` with:

| Field | Example Value |
|-------|---------------|
| `success` | `True` |
| `data` | `{"image_url": null, "image_path": "/tmp/output.png", "asset_id": null, "format": null, "width": 1024, "height": 768, "metadata": null}` |
| `error` | `None` |
| `metadata` | `{"mode": "cli", "command": "image.edit", "interface": "cli", "cli_path": "/usr/bin/photocraft-cli"}` |

Each failed skill execution returns a `SkillResult` with:

| Field | Example Value |
|-------|---------------|
| `success` | `False` |
| `data` | `None` |
| `error` | `"CLI not found: photocraft-cli"` |
| `metadata` | `{"mode": "cli", "reason": "cli_not_found"}` |

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| `cli_not_found` | `photocraft-cli` not installed or not on PATH | Install ArtCraft CLI or provide `cli_path` parameter |
| `neither_available` | Neither CLI nor MCP available | Install `photocraft-cli` or configure MCP |
| `mcp_unavailable` | MCP server unreachable | Use CLI mode instead (`mode: "cli"`) |
| `Invalid input: prompt: required` | Missing required `prompt` parameter | Provide `prompt` in inputs |
| `No image-generation capability found` | CLI command not found for this skill | Check keyword matching or provide `generation_command` override |
| `Operation timed out after 300s` | CLI command took too long | Increase `timeout` parameter or simplify operation |
