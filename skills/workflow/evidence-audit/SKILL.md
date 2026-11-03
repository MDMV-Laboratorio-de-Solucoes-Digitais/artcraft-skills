---
name: evidence-audit
description: Audit and track evidence with content addressing and provenance
license: Apache-2.0
metadata:
  author: artcraft
  version: "1.0"
  category: workflow
---

# Evidence Audit

## Purpose
Track, audit, and verify evidence/artifacts with content addressing and provenance tracking.

## When to Use
When you need to maintain audit trails and verify artifact integrity.

## Inputs
- `artifacts` (array, required): Artifacts to audit
- `policy` (object, optional): Audit policy

## Outputs
- `audit_report` (object): Audit report with hashes and provenance
- `verified` (boolean): Verification status

## Usage
Generalizable audit workflow for any artifacts.

## Limitations
Requires content addressing support.
