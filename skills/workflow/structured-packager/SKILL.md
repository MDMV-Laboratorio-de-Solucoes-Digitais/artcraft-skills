---
name: structured-packager
description: Package structured data and assets into organized, reproducible bundles
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: workflow
---

# Structured Packager

## Purpose
Package files, assets, and metadata into organized bundles with templates and validation.

## When to Use
When you need to create reproducible, structured packages for delivery or archival.

## Inputs
- `sources` (array, required): Source files/assets to package
- `template` (string, optional): Packaging template
- `metadata` (object, optional): Additional metadata

## Outputs
- `package_path` (string): Path to created package
- `manifest` (object): Package manifest with contents

## Usage
Generalizable packaging workflow for assets and documentation.

## Limitations
No assumptions about specific project structures.
