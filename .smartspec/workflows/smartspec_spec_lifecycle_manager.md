---
description: Manage SPEC lifecycle states with v5.2 centralization, multi-repo awareness, and UI JSON addendum
version: 5.2
---

# /smartspec_spec_lifecycle_manager

Manage specification lifecycle across large, multi-repo SmartSpec portfolios without breaking the existing `SPEC_INDEX.json` schema already used in production.

This workflow is **SmartSpec v5.2 centralization compatible** and **multi-repo-aware**.

---

## Core Principles (v5.2)

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json` (read-only if present)
- **Shared registries:** `.spec/registry/`
- **UI design source of truth (when applicable):** `ui.json` (Penpot-aligned)

This workflow updates **index metadata** (lifecycle/status fields) safely and does not rewrite `spec.md` by default.

---

## What It Does

- Resolves canonical index and registry.
- Supports **multi-repo spec resolution** for analysis.
- Provides lifecycle operations:
  - set status
  - promote/demote maturity
  - archive/deprecate
  - mark planned → active
  - detect lifecycle risk pockets
- Validates whether transitions violate:
  - dependency safety
  - cross-SPEC shared contracts
  - UI design separation rules
- Writes updates to **canonical index** and optionally mirrors root.
- Generates a lifecycle report under `.spec/reports/`.

---

## When to Use

- During roadmap grooming
- When moving a spec from planned to delivery
- Before release gates
- When deprecating core interfaces
- When coordinating public/private splits

---

## Inputs

- SPEC_INDEX
- Optional target spec ID(s)
- Optional scope filters by category/status

---

## Outputs

- Updated **canonical index**:
  - `.spec/SPEC_INDEX.json`
- Optional updated **legacy mirror**:
  - `SPEC_INDEX.json`
- Lifecycle report:
  - `.spec/reports/spec-lifecycle/`

---

## Flags

### Index / Registry

- `--index` Path to SPEC_INDEX (optional)
  - default: auto-detect

- `--registry-dir` Registry directory (optional)
  - default: `.spec/registry`

### Multi-Repo Support

- `--workspace-roots`
  - Comma-separated list of additional repo roots to search for spec files.
  - Example:
    - `--workspace-roots="../Smart-AI-Hub,../smart-ai-hub-enterprise-security"`

- `--repos-config`
  - Path to JSON config describing known repos and aliases.
  - Recommended location:
    - `.spec/smartspec.repos.json`

### Target Selection

- `--spec-id` Single spec ID (optional)
- `--spec-ids` Comma-separated spec IDs (optional)
- `--category` Filter by category (optional)
- `--status` Filter by status (optional)

### Lifecycle Operation

- `--set-status` Set status for selected specs (optional)
  - common values: `planned`, `backlog`, `draft`, `active`, `in-progress`, `stable`, `deprecated`, `archived`

- `--promote` Promote maturity one level (optional)
- `--demote` Demote maturity one level (optional)

- `--archive` Shortcut for `--set-status=archived`
- `--deprecate` Shortcut for `--set-status=deprecated`

### Interpretation Mode

- `--mode` `portfolio | runtime`
  - `portfolio`:
    - optimized for roadmap-level lifecycle management
    - allows planned/backlog specs to be file-incomplete
  - `runtime`:
    - stricter checks when altering active/core specs
  - default: `portfolio`

### Mirroring / Safety

- `--mirror-root` `true|false`
  - default: `true` if root mirror already exists, else `false`

- `--strict`
  - Fail on high-risk transition violations

- `--dry-run`
  - Show planned index changes without writing

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)
2) `SPEC_INDEX.json` (legacy root mirror)
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json` (older layout)

```bash
INDEX_IN="${FLAGS_index:-}"

if [ -z "$INDEX_IN" ]; then
  if [ -f ".spec/SPEC_INDEX.json" ]; then
    INDEX_IN=".spec/SPEC_INDEX.json"
  elif [ -f "SPEC_INDEX.json" ]; then
    INDEX_IN="SPEC_INDEX.json"
  elif [ -f ".smartspec/SPEC_INDEX.json" ]; then
    INDEX_IN=".smartspec/SPEC_INDEX.json" # deprecated
  elif [ -f "specs/SPEC_INDEX.json" ]; then
    INDEX_IN="specs/SPEC_INDEX.json"
  fi
fi

if [ ! -f "$INDEX_IN" ]; then
  echo "❌ SPEC_INDEX not found. Run /smartspec_reindex_specs first."
  exit 1
fi

echo "✅ Using SPEC_INDEX input: $INDEX_IN"

CANONICAL_OUT=".spec/SPEC_INDEX.json"
mkdir -p ".spec"

REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"

REPORT_DIR=".spec/reports/spec-lifecycle"
mkdir -p "$REPORT_DIR"
```

### 0.2 Resolve Multi-Repo Roots

Priority rules:

1) If `--repos-config` is provided and valid → use it.
2) Else if `--workspace-roots` is provided → use it.
3) Else → fall back to current repo root only.

---

## 1) Load Index (Schema-Preserving)

- Load JSON.
- Validate required top-level fields.
- Do not change schema shape.

---

## 2) Select Target Specs

Selection order:

1) `--spec-id` / `--spec-ids`
2) `--category`
3) `--status`
4) fallback: no-op with a warning

If no selection is provided, this workflow should only generate an analysis report.

---

## 3) Optional Multi-Repo Artifact Checks

For selected specs:

- Try to resolve `spec.path/spec.md` across repo roots.
- If UI spec:
  - try to resolve `ui.json` across repo roots.

These checks inform transition risk but should not block portfolio mode unless `--strict`.

---

## 4) Transition Rules (Compatibility-First)

This workflow must support existing projects where `status` is already used.

### 4.1 Suggested Status Buckets

- **Planned:** `planned`, `backlog`, `idea`, `draft`
- **Active:** `active`, `in-progress`, `stable`, `core`
- **End-of-life:** `deprecated`, `archived`

If a spec has no status, assume `active`.

### 4.2 Allowed Transitions (General)

- planned → active
- active → stable
- stable → deprecated
- deprecated → archived

### 4.3 Protected Transitions

If a spec is a dependency for active/core specs:

- Deprecation/archival requires:
  - an explicit migration note in the report
  - a recommended replacement target

In `--strict` mode:
- block the transition when dependents remain active.

---

## 5) Dependency Safety Checks

For each selected spec:

- Identify dependents from index.
- Warn when:
  - a planned spec is marked as a required dependency for active specs
  - a core spec is being demoted without a migration plan

In runtime mode:
- treat these warnings as errors for active/core transitions.

---

## 6) Registry Awareness (Non-Destructive)

If `.spec/registry` exists:

- Check whether the spec owns or heavily references:
  - shared APIs
  - shared models
  - shared terms

When deprecating:
- require a note in the lifecycle report indicating which registry items are affected.

This workflow does not modify registries.

---

## 7) UI JSON Addendum (Lifecycle-Aware)

Apply when **any** of these are true:

- category = `ui`
- `spec.ui === true`
- `ui.json` exists in the spec folder (in any repo root)

Rules:

1) `ui.json` remains design-owned.
2) Lifecycle changes must not force UI design artifacts to move into `.smartspec/`.
3) Planned UI specs may be missing `spec.md` in portfolio mode.
4) If a UI spec is promoted to active:
   - recommend ensuring `ui.json` exists (warn if missing)

If `ui-component-registry.json` exists:
- list component impact notes when deprecating/archiving UI specs.

---

## 8) Write Index Updates (Safe)

If not `--dry-run` and a lifecycle operation is requested:

- Apply status/maturity changes to the in-memory index.
- Recompute counts if your schema supports them.
- Write to:
  - **`CANONICAL_OUT`**

### 8.1 Optional Root Mirror

Determine mirror behavior:

- If `--mirror-root` explicitly set → honor it.
- Else:
  - mirror only if `SPEC_INDEX.json` already exists at root.

Write root mirror **after** canonical write.

Never write `.smartspec/SPEC_INDEX.json`.

---

## 9) Report

Write a structured report to:

- `.spec/reports/spec-lifecycle/`

Include:

- Index input path used
- Canonical output path
- Repo roots used
- Specs selected
- Transition intent
- Dependency risk summary
- Registry impact notes
- UI JSON compliance notes (if applicable)
- Recommended next workflows

---

## 10) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_portfolio_planner`
- `/smartspec_sync_spec_tasks --mode=additive` (after review)
- `/smartspec_generate_spec --repair-legacy --repair-additive-meta`

---

## Notes

- This workflow is designed to keep lifecycle governance **safe, incremental, and schema-compatible**.
- `.spec/SPEC_INDEX.json` remains the canonical truth.
- Root `SPEC_INDEX.json` is a legacy mirror for backward compatibility only.

