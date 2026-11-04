---
name: mesh-generate
description: Generate 3D meshes from images or text
license: MIT
compatibility: Requires ArtCraft CLI or MCP
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Mesh Generate

Generate 3D meshes from text prompts or images.

## Inputs
- `prompt` (string, optional): Text description of the 3D object
- `image` (string, optional): Source image for image-to-3D
- `model` (string, optional): Model to use
- `format` (string, optional): Output format (glb, obj, etc.)
- `mode` (string, optional): Execution mode (cli, mcp, auto)
- `cli_path` (string, optional): Path to CLI binary
- `mcp_config` (object, optional): MCP configuration
- `command_keywords` (array, optional): Keywords for command discovery
- `generation_command` (string, optional): Explicit command override
- `timeout` (number, optional): Timeout in seconds

## Outputs
- `mesh_url` (string): URL of generated mesh
- `mesh_path` (string): Path to generated mesh
- `asset_id` (string): Asset identifier
- `format` (string): Mesh format
- `metadata` (object): Additional metadata

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
Requires appropriate API credentials and may incur costs. Generation times can be longer for complex meshes.
