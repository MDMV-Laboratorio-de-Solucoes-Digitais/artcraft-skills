---
name: image-generate
description: Generate images from text prompts using various AI models with composition controls
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Image Generate

## Purpose
Generate images from text prompts with support for multiple models and composition controls.

## When to Use
When you need to create images from text descriptions, with control over style, composition, and model selection.

## Inputs
- `prompt` (string, required): Text description of the image
- `model` (string, optional): Model to use (default: nano-banana)
- `width` (number, optional): Image width
- `height` (number, optional): Image height

## Outputs
- `image_url` (string): URL of generated image
- `asset_id` (string): Asset identifier
- `job_token` (string): Job tracking token

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
Requires appropriate API credentials and may incur costs.
