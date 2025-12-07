---
description: Plan and prioritize a SmartSpec portfolio with v5.2 centralization, multi-repo awareness, and UI JSON addendum
version: 5.2
---

# /smartspec_portfolio_planner

Create a strategic, multi-SPEC portfolio plan that helps large teams coordinate delivery across **public/private** and other multi-repo layouts while preventing cross-SPEC drift.

This workflow is **SmartSpec v5.2 centralization compatible** and **multi-repo-aware**.

---

## Core Principles (v5.2)

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json` (read-only if present)
- **Shared registries:** `.spec/registry/`
- **UI design source of truth (when applicable):** `ui.json` (Penpot-aligned)

This workflow is primarily analytical and should not mutate specs by default.

---

## What It Does

- Resolves canonical index and registry.
- Supports **multi-repo spec resolution** for analysis.
- Builds high-level portfolio views:
  - dependency-first roadmap
  - category-based streams
  - cross-cutting capability map (security/observability/data/platform/ui)
  - public ↔ private split lens
  - UI design-to-component readiness lens
- Detects:
  - missing foundational specs
  - duplicate or overlapping responsibilities
  - orphaned planned specs
  - risk clusters in dependency graphs
  - registry gaps that block multi-team execution
- Generates a portfolio report under `.spec/reports/`.

---

## When to Use

- Quarterly/half-year planning
- Large-scale re-architecture
- Before onboarding multiple teams
- When public/private repos must be synchronized deliberately
- After major reindex or lifecycle changes

---

## Inputs

- Canonical SPEC_INDEX
- Optional registries
- Optional scope filters

---

## Outputs

- Portfolio report under:
  - `.spec/reports/portfolio-planner/`

This report is project-owned and should be version-controlled when useful.

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

### Planning Views

- `--view` Optional focus view selector
  - values: `full`, `dependency`, `category`, `capability`, `public-private`, `ui`
  - default: `full`

### Interpretation

- `--mode` `portfolio | runtime`
  - `portfolio`:
    - optimized for roadmap-level planning and incomplete planned specs
  - `runtime`:
    - emphasizes delivery readiness of active/core specs
  - default: `portfolio`

### Reporting

- `--report-dir` Output report directory (optional)
  - default: `.spec/reports/portfolio-planner/`

- `--strict`
  - Fail only on critical structural inconsistencies (rare for planning)

- `--dry-run`
  - Print findings without writing files

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX

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

if [ ! -f "$INDEX_PATH" ]; then
  echo "❌ SPEC_INDEX not found. Run /smartspec_reindex_specs first."
  exit 1
fi

echo "✅ Using SPEC_INDEX: $INDEX_PATH"
```

### 0.2 Resolve Registry Dir

```bash
REGISTRY_DIR="${FLAGS_registry_dir:-.spec/registry}"
REGISTRY_AVAILABLE=false

if [ -d "$REGISTRY_DIR" ]; then
  REGISTRY_AVAILABLE=true
  echo "✅ Registry detected at: $REGISTRY_DIR"
else
  echo "ℹ️ Registry not found at $REGISTRY_DIR (planner will run in index-first mode)"
fi
```

### 0.3 Resolve Report Dir

```bash
REPORT_DIR="${FLAGS_report_dir:-.spec/reports/portfolio-planner}"
mkdir -p "$REPORT_DIR"

VIEW="${FLAGS_view:-full}"
MODE="${FLAGS_mode:-portfolio}"
STRICT="${FLAGS_strict:-false}"
DRY_RUN="${FLAGS_dry_run:-false}"
```

---

## 1) Resolve Multi-Repo Roots

Priority rules:

1) If `--repos-config` is provided and valid → use it.
2) Else if `--workspace-roots` is provided → use it.
3) Else → fall back to current repo root only.

Recommended config file: `.spec/smartspec.repos.json`

Example:

```json
{
  "version": "1.0",
  "repos": [
    { "id": "public", "root": "../Smart-AI-Hub" },
    { "id": "private", "root": "../smart-ai-hub-enterprise-security" }
  ]
}
```

The planner uses these roots to:
- verify path plausibility
- enhance UI evidence checks
- improve public/private readiness assessments

It does not rewrite files in other repos.

---

## 2) Load Canonical Knowledge

- Load SPEC_INDEX.
- Build summary counts by:
  - category
  - status
  - dependency depth

If registries exist:
- Load registry metadata for gap detection.

---

## 3) Portfolio Views

### 3.1 Dependency View

Generate:
- topological ordering (best-effort)
- identify blockers:
  - planned specs required by active specs
  - circular clusters (reference validate reports)

In runtime mode:
- emphasize active/core sequences.

### 3.2 Category View

Group by category using your existing taxonomy.

Highlight:
- over-concentration in one category
- missing foundational categories

### 3.3 Capability View

Map specs to cross-cutting capabilities:

- security
- observability
- data platform
- infra
- integration
- ui

This view helps identify that core pillars exist before feature-level specs scale.

### 3.4 Public ↔ Private View

This view is advisory and avoids schema changes.

Heuristics:
- infer repo scope from path prefix patterns when available
- infer by category tags if present

Flag risks:
- private-only core dependency with no public integration plan
- duplicated ownership of the same domain concept across repos

### 3.5 UI View (Conditional)

Apply when the portfolio contains UI specs.

Detect UI specs by:
- category = `ui`, OR
- `spec.ui === true`, OR
- `ui.json` presence in any repo root.

Report:
- UI specs missing `ui.json` (warn)
- UI component naming alignment with registry (if present)
- UI specs that embed heavy business logic in tasks/spec text

Non-UI projects:
- This view should be empty without error.

---

## 4) Registry Gap Lens (Read-Only)

If `REGISTRY_AVAILABLE=true`:

- Estimate whether the portfolio references shared names that are:
  - unregistered
  - inconsistently defined
  - duplicated

Output:
- prioritized registry hardening recommendations.

This workflow does not write registries.

---

## 5) Status-Aware Planning Semantics

To avoid forcing low-quality placeholders:

### Portfolio Mode (default)

- Planned/backlog/idea/draft specs may:
  - be missing `spec.md`
  - be orphaned
  - have incomplete dependencies

These result in:
- info/warn-level planning notes.

### Runtime Mode

- Active/core/stable specs are expected to:
  - have resolvable artifacts
  - have valid dependency chains

These become:
- readiness risks.

If a spec has no explicit status, assume `active`.

---

## 6) Output Report Structure

Write a structured report containing:

- Index path used
- Registry availability
- Repo roots used
- Overall portfolio counts
- View-specific sections based on `--view`
- Top risks and blockers
- Cross-repo alignment notes
- UI readiness section (if applicable)
- Suggested next workflows

Default location:
- `.spec/reports/portfolio-planner/portfolio-report.md`

If `--dry-run`:
- print only.

---

## 7) Recommended Follow-ups

- `/smartspec_validate_index --mode=portfolio`
- `/smartspec_spec_lifecycle_manager`
- `/smartspec_reindex_specs`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_global_registry_audit`

---

## Notes

- The portfolio planner is an **executive-level lens** that complements strict validation.
- It should help teams decide what to build next without creating new cross-SPEC conflicts.
- `.spec/` remains the canonical project-owned space for SmartSpec v5.2 projects.

