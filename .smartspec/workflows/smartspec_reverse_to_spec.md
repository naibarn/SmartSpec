---
description: Reverse-engineer implementation into SmartSpec artifacts with centralization (.spec) and UI JSON addendum
version: 5.2
---

# /smartspec_reverse_to_spec

Reverse-engineer existing code and project structure into SmartSpec-compatible specification artifacts while enforcing centralized, conflict-resistant governance.

This workflow is intended for:
- legacy projects without consistent specs
- partially documented systems
- migration to SmartSpec v5.2 centralization

It enforces:
- **`.spec/` as the canonical project-owned space**
- **`.spec/SPEC_INDEX.json` as canonical index**
- **`.spec/registry/` as shared source of truth**
- `.smartspec/` as tooling-only
- **UI design source of truth in `ui.json`** when UI specs exist

---

## What It Does

1) Resolves canonical index and registry paths.
2) Scans codebase for:
   - modules/services
   - API routes
   - data models
   - domain vocabulary
   - shared patterns
   - UI components
3) Proposes or generates:
   - new spec folders
   - draft `spec.md` files
   - optional `ui.json` placeholders for UI specs
   - additive registry suggestions
4) Produces a reconciliation report that highlights:
   - missing specs
   - overlapping responsibilities
   - naming conflicts
   - candidates for shared patterns

---

## When to Use

- Migrating a mature codebase into SmartSpec.
- Auditing architecture drift.
- Preparing a portfolio of specs for large teams.

---

## Inputs

- Repository codebase
- Optional scope hints:
  - folders
  - modules
  - domains

---

## Outputs

- Proposed or generated spec folders under `specs/`.
- Draft `spec.md` for each newly inferred spec.
- Index update recommendations.
- Registry update recommendations.
- A reverse-engineering report.

---

## Flags

- `--index` Path to SPEC_INDEX (optional)  
  default: auto-detect

- `--registry-dir` Registry directory (optional)  
  default: `.spec/registry`

- `--scope` Limit scanning to a path/module (optional)

- `--mode` `recommend` | `generate-drafts` | `repair-legacy`  
  default: `recommend`

- `--mirror-root` Update legacy root mirror after canonical update (optional)

- `--strict` Fail on high-risk ambiguity (optional)

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_PATH="${FLAGS_index:-}"

if [ -z "$INDEX_PATH" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_PATH="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_PATH=".smartspec/SPEC_INDEX.json" # deprecated
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_PATH="specs/SPEC_INDEX.json"
  fi
fi

if [ -n "$INDEX_PATH" ] && [ -f "$INDEX_PATH" ]; then
  echo "✅ Using SPEC_INDEX: $INDEX_PATH"
else
  echo "⚠️ SPEC_INDEX not found. Reverse run may bootstrap a new canonical index in generate modes."
  INDEX_PATH=""
fi

REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
mkdir -p "$REGISTRY_DIR"

MODE="${FLAGS_mode:-recommend}"
SCOPE="${FLAGS_scope:-}"
```

---

## 1) Determine Reverse Scope

- If `--scope` provided:
  - limit scanning to that path/module.
- Otherwise:
  - scan key directories for service, domain, infra, and UI layers.

---

## 2) Extract Architectural Signals

Identify candidates for spec boundaries using:

- folder/module cohesion
- domain naming
- API namespace segmentation
- shared libraries usage
- data schema separation

Extract:
- potential spec IDs and titles
- likely categories (`core`, `security`, `service`, `data`, `ui`, `platform`, etc.)
- dependency candidates

Do not infer overly fine-grained specs unless the codebase clearly isolates responsibilities.

---

## 3) Cross-Check With Existing Index

If `INDEX_PATH` exists:

- Match discovered modules to existing specs.
- Classify findings into:
  1) Already covered
  2) Partially covered (missing sections)
  3) Not covered (candidate new spec)
  4) Overlapping (potential split/merge)

---

## 4) Registry Alignment Discovery

If registry files exist, compare extracted names to canonical entries:

- API routes → `api-registry.json`
- Data models → `data-model-registry.json`
- Terms → `glossary.json`
- Critical cross-cutting behaviors → `critical-sections-registry.json`
- Patterns → `patterns-registry.json`

Rules:
- Prefer aligning inferred names to existing registry names.
- When a rename/migration seems needed:
  - record a recommendation
  - do not auto-rename in code in this workflow

---

## 5) UI JSON Addendum (Conditional)

Apply when:
- the inferred/spec-matched category is `ui`, or
- UI component layers are detected, or
- an existing UI spec folder contains `ui.json`.

Rules:
- UI design source of truth must be **JSON** to support Penpot.
- `ui.json` should not embed business logic.
- Extract UI concerns into:
  - visual structure
  - component mapping
  - tokens/variants

Required outputs (in generate modes):
- If a UI spec is inferred and no `ui.json` exists:
  - create a **placeholder** `ui.json` draft suggestion (not mandatory write unless allowed).

If the project does not use UI JSON:
- You may allow a non-blocking pathway:
  - keep UI information in `spec.md`
  - recommend adopting `ui.json` for design-team workflow

---

## 6) Mode Behavior

### 6.1 `recommend` (default)

- Produce a reverse report.
- Suggest:
  - new specs
  - missing sections
  - registry additions
  - index improvements
- Do not write new files.

### 6.2 `generate-drafts`

- Create draft spec folders for uncovered modules:
  - `specs/<category>/<spec-id>/`
- Generate minimal `spec.md` skeletons.
- If UI spec:
  - generate a minimal `ui.json` placeholder template.
- Do not overwrite existing `spec.md`.

### 6.3 `repair-legacy`

- Intended to support older SmartSpec projects.
- May add **additive metadata** or companion files to align with v5.2.
- Must not delete or rewrite core content of legacy `spec.md`.

---

## 7) Canonical Index Update Strategy

If `MODE` is `generate-drafts` or `repair-legacy`:

- Prefer writing/merging into **`.spec/SPEC_INDEX.json`**.
- If only root mirror exists:
  - read it to bootstrap fields
  - write canonical output

Optional root mirror update:
- enabled only when `--mirror-root=true` or root mirror already exists.

Do not write `.smartspec/SPEC_INDEX.json`.

---

## 8) Output Reverse Report

Default report location:
- `.spec/reports/`

Include:
- Coverage map: code modules → specs
- New spec candidates
- Overlap/conflict warnings
- Dependency suggestions
- Registry alignment summary
- UI JSON adoption/compliance notes

---

## 9) Recommended Follow-ups

- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_spec --repair-legacy` (for older specs)
- `/smartspec_sync_spec_tasks --mode=additive` (after review)

---

## Notes

- This workflow is a bridge for legacy modernization.
- It is intentionally conservative to avoid creating new cross-SPEC conflicts automatically.
- Canonical shared truth lives in `.spec/` when present.

