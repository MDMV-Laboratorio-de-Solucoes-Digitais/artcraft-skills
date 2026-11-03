---
name: background-remove
description: Remove backgrounds and isolate subjects with precise matting
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Background Remove

## Purpose
Remove backgrounds from images and isolate subjects with high-quality matting.

## When to Use
When you need clean cutouts for compositing or subject isolation.

## Inputs
- `image` (string, required): Source image URL or asset ID
- `model` (string, optional): Matting model to use
- `return_mask` (boolean, optional): Also return alpha mask

## Outputs
- `image_url` (string): URL of image with transparent/background removed
- `mask_url` (string): URL of alpha mask if requested
- `asset_id` (string): Asset identifier

## Usage
Use with core abstractions for asset handling.

## Limitations
May struggle with fine hair or complex edges depending on model.
