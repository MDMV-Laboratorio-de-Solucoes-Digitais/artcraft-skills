---
name: background-remove
description: Remove backgrounds from images
license: MIT
compatibility: Requires ArtCraft CLI or MCP
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Background Remove

Automatically remove backgrounds from images to isolate subjects.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `model` (string, optional): Matting model to use
- `return_mask` (boolean, optional): Also return alpha mask
- `mode` (string, optional): Execution mode (cli, mcp, auto)
- `cli_path` (string, optional): Path to CLI binary
- `mcp_config` (object, optional): MCP configuration
- `command_keywords` (array, optional): Keywords for command discovery
- `generation_command` (string, optional): Explicit command override
- `timeout` (number, optional): Timeout in seconds

## Outputs
- `image_url` (string): URL of image with transparent/background removed
- `image_path` (string): Path to processed image
- `mask_url` (string): URL of alpha mask if requested
- `asset_id` (string): Asset identifier
- `format` (string): Image format
- `metadata` (object): Additional metadata

## Usage
Use with core abstractions for asset handling.

## Limitations
May struggle with fine hair or complex edges depending on model.
