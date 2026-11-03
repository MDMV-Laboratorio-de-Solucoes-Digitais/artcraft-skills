---
name: image-edit
description: Edit images with inpainting, outpainting, and compositing capabilities
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Image Edit

## Purpose
Edit existing images using inpainting, outpainting, and compositing operations with precise control.

## When to Use
When you need to modify specific regions of an image, extend image boundaries, or composite elements.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `prompt` (string, required): Description of desired edit
- `mask` (string, optional): Mask for inpainting region
- `mode` (string, optional): Edit mode (inpaint, outpaint, composite)
- `model` (string, optional): Model to use

## Outputs
- `image_url` (string): URL of edited image
- `asset_id` (string): Asset identifier
- `job_token` (string): Job tracking token

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
Requires source image and may incur costs depending on operation.
