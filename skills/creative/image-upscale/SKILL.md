---
name: image-upscale
description: Enhance and upscale images with AI-powered upscaling
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Image Upscale

## Purpose
Upscale and enhance images using AI to improve resolution and detail.

## When to Use
When you need higher resolution images while preserving or enhancing details.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `scale` (number, optional): Upscale factor (2x, 4x, default: 2)
- `model` (string, optional): Upscaling model to use
- `enhance` (boolean, optional): Apply additional enhancements

## Outputs
- `image_url` (string): URL of upscaled image
- `asset_id` (string): Asset identifier
- `job_token` (string): Job tracking token

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
May introduce artifacts; processing time increases with scale factor.
