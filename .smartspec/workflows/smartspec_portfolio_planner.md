---
description: Plan and prioritize a SmartSpec portfolio with v5.6 multi-repo + multi-registry awareness, registry gap analysis, and chain-consistent safety semantics
version: 5.6
---

# /smartspec_portfolio_planner

Generate a portfolio-level roadmap and prioritization view across many specs.

This v5.6 workflow preserves the v5.2 strengths:

- Whole-portfolio dependency-aware planning
- Index-first reasoning when available
- Registry gap lens
- Multi-repo scan support

And adds v5.6 alignment features:

- Multi-registry awareness with explicit precedence
- `--specindex` alias consistency
- `--safety-mode` semantics separated from `--mode portfolio|runtime`
- Chain readiness hints for spec/tasks generation

---

## Core Principles

- `.spec/` is the canonical governance space.
- `.spec/SPEC_INDEX.json` is the canonical index.
- `.spec/registry/` is the primary naming source of truth.
- Root `SPEC_INDEX.json` is a legacy mirror.
- `.smartspec/` is tooling-only.

---

## What It Does

- Resolves index, registries, and multi-repo roots.
- Loads a portfolio of specs.
- Builds an end-to-end dependency graph.
- Identifies cross-cutting shared work.
- Produces a prioritized roadmap with:
  - foundation phases
  - shared contract milestones
  - cross-team sequencing
  - risk and governance notes
- Runs a registry gap analysis across the merged registry view.
- Emits a structured report and optional plan output.

---

## Inputs

- SPEC_INDEX (recommended)
- Spec files referenced by the index
- Primary registry
- Optional supplemental registries
- Optional multi-repo configuration

---

## Outputs

- Portfolio plan document (implementation-dependent)
- Report under:
  - `.spec/reports/portfolio-planner/`

---

## Flags

### Portfolio Mode (Legacy Semantics Preserved)

```bash
--mode=<portfolio|runtime>
```

- `portfolio` (default)
  - prioritization, roadmap, governance maturity

- `runtime`
  - CI-friendly checks for release readiness

### Safety (NEW, v5.6-aligned)

```bash
--safety-mode=<strict|dev>
--strict
```

- `strict` (default)
  - block recommendations that would cause cross-repo duplication risk

- `dev`
  - proceed with warnings

`--strict` remains a legacy alias.

### Index

```bash
--index=<path>
--specindex=<path>    # legacy alias
```

### Registries

```bash
--registry-dir=<dir>
--registry-roots=<csv>
```

Registry precedence:

1) Primary registry is authoritative.
2) Supplemental registries are read-only validation sources.

### Multi-Repo

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence.
- Recommended path: `.spec/smartspec.repos.json`.

### Scope Selection

Implementation-dependent options may include:

```bash
--categories=<csv>
--spec-ids=<csv>
--include-drafts=<true|false>
```

### Output

```bash
--output=<path>
--report=<summary|detailed>
--dry-run
```

---

## 0) Resolve Canonical Context

### 0.1 Resolve SPEC_INDEX

Auto-detect order (unless overridden):

1) `.spec/SPEC_INDEX.json`
2) `SPEC_INDEX.json`
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json`

### 0.2 Resolve Registry View

- Load primary registry directory.
- Load supplemental registries (if provided) read-only.

Precedence:

- Primary registry entries override supplemental entries of the same name.

### 0.3 Resolve Multi-Repo Roots

- Build repo root list using `--repos-config` when provided.
- Otherwise add `--workspace-roots`.

If `--repos-config` is provided and index entries contain `repo:` labels:

- Validate mapping coverage.

---

## 1) Load Portfolio Scope

If index exists:

- Use the index as the primary portfolio map.
- Optionally filter by category or explicit spec IDs.

If index does not exist:

- Fall back to scanning `specs/` roots.
- Insert a report recommendation to run `/smartspec_reindex_specs`.

---

## 2) Dependency Graph & Sequencing

- Build a global dependency DAG.
- Detect cycles and missing nodes.
- Mark cross-repo dependencies as **external**.

In strict safety mode:

- If critical external dependencies cannot be resolved:
  - mark them as blocking items in the roadmap.

---

## 3) Registry Gap Lens (v5.6-Expanded)

Compute:

- Which shared names are referenced by many specs.
- Which of those are missing from the primary registry.
- Which exist only in supplemental registries.

Rules:

- Names found only in supplemental registries should be flagged as likely cross-repo owners.
- The planner must not recommend creating new shared names that would collide with any loaded registry view.

---

## 4) Risk & Governance Lens

Include:

- ownership ambiguity hotspots
- cross-repo duplication risks
- inconsistent status metadata
- UI portfolio consistency signals (if UI registries exist)

---

## 5) Report Structure

Write a report under `.spec/reports/portfolio-planner/` containing:

- Index path used
- Primary registry dir
- Supplemental registry roots
- Multi-repo roots summary
- Portfolio scope summary
- Dependency sequencing summary
- Registry gap findings
- Cross-repo duplication risk list
- Suggested governance actions
- **Chain readiness notes** for:
  - `/smartspec_generate_spec v5.6`
  - `/smartspec_generate_tasks v5.6`

---

## 6) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_global_registry_audit`
- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`

---

## Notes

- This workflow is a strategic governance and prioritization tool.
- It remains backward compatible with v5.2 index schemas.
- Multi-registry support is essential for accurate portfolio insights in multi-repo platforms.

