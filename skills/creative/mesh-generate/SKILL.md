---
name: mesh-generate
description: Generate 3D meshes from images or text prompts
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: creative
---

# Mesh Generate

## Purpose
Generate 3D meshes from text prompts or images with support for multiple models.

## When to Use
When you need to create 3D assets for scenes, games, or 3D workflows.

## Inputs
- `prompt` (string, optional): Text description of the 3D object
- `image` (string, optional): Source image for image-to-3D
- `model` (string, optional): Model to use
- `format` (string, optional): Output format (glb, obj, etc.)

## Outputs
- `mesh_url` (string): URL of generated mesh
- `asset_id` (string): Asset identifier
- `job_token` (string): Job tracking token

## Usage
Use with core abstractions for cost estimation and job orchestration.

## Limitations
Requires appropriate API credentials and may incur costs. Generation times can be longer for complex meshes.
