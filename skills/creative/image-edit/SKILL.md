---
name: image-edit
description: Edit existing images using AI
license: MIT
compatibility: Requires ArtCraft CLI or MCP
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Image Edit

Edit existing images with AI-powered inpainting, outpainting, and compositing.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `prompt` (string, required): Description of desired edit
- `mask` (string, optional): Mask for inpainting region
- `mode_edit` (string, optional): Edit mode (inpaint, outpaint, composite)
- `model` (string, optional): Model to use
- `strength` (number, optional): Edit strength
- `width` (number, optional): Output width
- `height` (number, optional): Output height
- `aspect_ratio` (string, optional): Aspect ratio
- `seed` (number/string, optional): Random seed
- `mode` (string, optional): Execution mode (cli, mcp, auto)
- `cli_path` (string, optional): Path to CLI binary
- `mcp_config` (object, optional): MCP configuration
- `command_keywords` (array, optional): Keywords for command discovery
- `generation_command` (string, optional): Explicit command override
- `timeout` (number, optional): Timeout in seconds

## Outputs
- `image_url` (string): URL of edited image
- `image_path` (string): Path to edited image
- `asset_id` (string): Asset identifier
- `format` (string): Image format
- `width` (number): Image width
- `height` (number): Image height
- `metadata` (object): Additional metadata

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
Requires source image and may incur costs depending on operation.
