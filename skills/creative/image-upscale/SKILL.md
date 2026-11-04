---
name: image-upscale
description: Upscale and enhance images
license: MIT
compatibility: Requires ArtCraft CLI or MCP
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Image Upscale

Upscale images using AI-powered super-resolution.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `scale` (number, optional): Upscale factor (2x, 4x, default: 2)
- `model` (string, optional): Upscaling model to use
- `enhance` (boolean, optional): Apply additional enhancements
- `mode` (string, optional): Execution mode (cli, mcp, auto)
- `cli_path` (string, optional): Path to CLI binary
- `mcp_config` (object, optional): MCP configuration
- `command_keywords` (array, optional): Keywords for command discovery
- `generation_command` (string, optional): Explicit command override
- `timeout` (number, optional): Timeout in seconds

## Outputs
- `image_url` (string): URL of upscaled image
- `image_path` (string): Path to upscaled image
- `asset_id` (string): Asset identifier
- `format` (string): Image format
- `width` (number): Image width
- `height` (number): Image height
- `metadata` (object): Additional metadata

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
May introduce artifacts; processing time increases with scale factor.
