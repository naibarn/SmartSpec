# SmartSpec Validate SPEC_INDEX Workflow
## Cross-Check Index + Registry Integrity (v5.6 Alignment for Multi-Repo Spec→Tasks Chain)

---
description: |
  Validate SPEC_INDEX.json integrity and system governance health.

  v5.6 alignment goals:
  - Keep canonical index rules (.spec/SPEC_INDEX.json first)
  - Validate cross-SPEC dependency graph
  - Validate registry completeness and detect cross-repo naming collisions
  - Support multi-repo spec resolution using the same config patterns as:
      /smartspec_generate_spec v5.6
      /smartspec_generate_tasks v5.6
  - Provide a single health gate for the entire chain:
      validate → generate_spec → generate_tasks

flags:
  - name: --fix
    description: Automatically fix safe issues (metadata, dependents, timestamps). Must not alter ownership semantics.
    type: boolean
    default: false

  - name: --report
    description: Report detail level
    type: enum
    values: [summary, detailed]
    default: summary

  - name: --index
    description: Path to SPEC_INDEX.json file (optional). If omitted, SmartSpec will auto-detect.
    type: string
    optional: true

  - name: --specindex
    description: Legacy alias for --index
    type: string
    optional: true

  - name: --registry-dir
    description: Primary registry directory (authoritative)
    type: string
    optional: true

  - name: --registry-roots
    description: Comma-separated list of supplemental registry directories for read-only cross-repo validation
    type: string
    optional: true

  - name: --workspace-roots
    description: Comma-separated list of additional repository roots to search for referenced specs
    type: string
    optional: true

  - name: --repos-config
    description: JSON config mapping repo IDs to physical roots; takes precedence over --workspace-roots
    type: string
    optional: true

  - name: --mode
    description: Validation mode controlling strictness of runtime vs portfolio checks
    type: enum
    values: [runtime, portfolio]
    default: portfolio

examples:
  - command: /smartspec_validate_index
    description: Validate with summary report (auto-detect canonical index)

  - command: /smartspec_validate_index --report=detailed
    description: Generate detailed report

  - command: /smartspec_validate_index --fix --report=detailed
    description: Validate and apply safe auto-fixes

  - command: /smartspec_validate_index --workspace-roots="../Repo-A,../Repo-B"
    description: Validate across multiple sibling repositories (lightweight)

  - command: /smartspec_validate_index --repos-config=.spec/smartspec.repos.json --mode=runtime
    description: Use structured multi-repo config and enforce stricter runtime rules

  - command: /smartspec_validate_index \
      --repos-config=.spec/smartspec.repos.json \
      --registry-dir=.spec/registry \
      --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry" \
      --report=detailed
    description: Full multi-repo + multi-registry validation prior to spec/tasks generation

version: 5.6.0
author: SmartSpec Team
---

## Overview

This workflow validates SPEC_INDEX.json and its ecosystem so that downstream workflows can safely generate specs and tasks.

It is designed to be the **first gate** in the SmartSpec chain:

1) `/smartspec_validate_index`
2) `/smartspec_generate_spec`
3) `/smartspec_generate_tasks`

---

## 1) Canonical Index Resolution

Detection order:

1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` (legacy root mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (older layout)

If `--index` or `--specindex` is provided, it overrides detection.

---

## 2) Multi-Repo Root Resolution

The validator must construct the repo root search list:

1) Current repo root
2) `--repos-config` roots (if provided)
3) `--workspace-roots` (if provided)

### 2.1 Repo Mapping Integrity Check (New)

If `--repos-config` is provided and the index contains `repo:` fields:

- Validate that each `repo` label used by index entries has a corresponding `id` in the config.

Severity:
- `mode=runtime` → blocking error
- `mode=portfolio` → high-visibility warning

---

## 3) Registry Resolution

Primary registry:
- `--registry-dir` if provided, else `.spec/registry` when present.

Supplemental registries:
- `--registry-roots` when provided.

### 3.1 Registry Precedence

1) Primary registry is authoritative.
2) Supplemental registries are read-only validation sources.

### 3.2 Cross-Repo Naming Collision Check (New)

If the same API/model/term/UI component exists in multiple registries with conflicting definitions:

- `mode=runtime` → blocking error
- `mode=portfolio` → warning + remediation guidance

---

## 4) Index Integrity Checks

Validate:
- unique spec IDs
- paths exist
- status values are valid
- dependency graph has no cycles
- dependency IDs exist

For each spec path:

- Attempt to resolve the file across multi-repo roots.
- If unresolved:
  - `mode=runtime` → blocking error
  - `mode=portfolio` → warning

---

## 5) Cross-Workflow Alignment Checks (v5.6)

This validator should confirm that governance assumptions needed by downstream workflows are present:

### 5.1 Spec→Tasks Chain Readiness

- Index has enough metadata to locate specs and dependency owners.
- Registry set is sufficient to avoid duplicate shared-name creation.

If not sufficient:
- The report must explicitly recommend:
  - initializing missing registries
  - adopting `--registry-roots` for multi-repo projects
  - adding or repairing repo mappings

---

## 6) Safe Auto-Fix Rules

When `--fix` is enabled:

Allowed:
- normalize timestamps
- repair missing optional metadata
- infer safe dependents lists

Forbidden:
- changing ownership semantics
- changing dependency meaning
- renaming spec IDs
- rewriting registry entries

---

## 7) Report Output

The report should include:

- Index path used
- Multi-repo configuration used
- Registry configuration used
- Missing spec files
- Dependency graph issues
- Cross-repo mapping issues
- Cross-registry collision findings
- Summary readiness assessment for:
  - generate_spec v5.6
  - generate_tasks v5.6

---

## 8) Recommended Usage Patterns

### Single Repo

```bash
/smartspec_validate_index --report=detailed
```

### Two or More Repos

```bash
/smartspec_validate_index \
  --repos-config=.spec/smartspec.repos.json \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry" \
  --report=detailed
```

---

## Final Notes

- This v5.6 validator is intentionally aligned with:
  - `/smartspec_generate_spec v5.6`
  - `/smartspec_generate_tasks v5.6`
- The three documents should be maintained together to prevent governance drift.
- Multi-repo and multi-registry flags are optional for single-repo projects but strongly recommended for shared-platform architectures.

