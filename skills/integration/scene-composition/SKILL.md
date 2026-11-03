---
name: scene-composition
description: Cross-product workflow for composing scenes from multiple asset types
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: integration
---

# Scene Composition

## Purpose
Orchestrate composition of scenes using assets from multiple domains (2D, 3D, etc.).

## When to Use
When building complex scenes with mixed asset types.

## Inputs
- `assets` (array, required): Assets to compose
- `layout` (object, optional): Scene layout
- `camera` (object, optional): Camera settings

## Outputs
- `scene_url` (string): Composed scene
- `asset_id` (string): Scene asset identifier

## Usage
Composes multiple atomic skills for cross-product workflows.

## Limitations
Requires compatible assets and skills.
