---
name: 2d-to-3d-workflow
description: Cross-product workflow converting 2D assets to 3D meshes
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: integration
---

# 2D to 3D Workflow

## Purpose
Orchestrate workflow converting 2D images/assets to 3D meshes with composition controls.

## When to Use
When you need to generate 3D assets from 2D references.

## Inputs
- `image` (string, required): Source 2D image
- `prompt` (string, optional): Additional guidance
- `options` (object, optional): Workflow options

## Outputs
- `mesh_url` (string): Generated 3D mesh
- `asset_id` (string): Asset identifier

## Usage
Composes image processing and mesh generation skills.

## Limitations
Requires compatible skills and may incur costs.
