---
description: Audit global registries across all specs with v5.2 centralization, multi-repo awareness, and UI JSON addendum
---

# /smartspec_global_registry_audit

Audit shared registries across the SmartSpec ecosystem to prevent cross-SPEC drift, naming collisions, and inconsistent cross-cutting rules.

This workflow is **SmartSpec v5.2 centralization compatible** and **multi-repo-aware**.

## Core Principles (v5.2)

- **Project-owned canonical space:** `.spec/`
- **Canonical index:** `.spec/SPEC_INDEX.json`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json` (read-only if present)
- **Shared registries:** `.spec/registry/`
- **UI design source of truth (when applicable):** `ui.json` (Penpot-aligned)

This workflow is read-only for specs by default, and should not introduce breaking schema changes.

---

## What This Audits

If present, the workflow audits these registries:

1) `api-registry.json`
2) `data-model-registry.json`
3) `glossary.json`
4) `critical-sections-registry.json`
5) `patterns-registry.json` (optional)
6) `ui-component-registry.json` (optional)

It also audits cross-SPEC usage signals from:

- the canonical SPEC_INDEX
- spec metadata in `spec.md`
- tasks signals (when adjacent `tasks.md` exists)
- UI JSON references (when `ui.json` exists)

---

## When to Use

- After adding several new specs
- After large naming refactors
- Before major releases
- When you suspect registry drift between public/private repos
- After onboarding/handovers

---

## Outputs

- A structured audit report under:
  - `.spec/reports/registry-audit/`

This report is **project-owned** and should be version-controlled.

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
  - Path to a JSON config describing known repos and aliases.
  - Recommended location:
    - `.spec/smartspec.repos.json`

### Audit Interpretation

- `--mode` `portfolio | runtime`
  - `portfolio`:
    - tolerates planned/backlog gaps
    - focuses on roadmap-level normalization
  - `runtime`:
    - stricter alignment for active/core specs
  - default: `portfolio`

### Reporting

- `--report-dir` Output report directory (optional)
  - default: `.spec/reports/registry-audit/`

- `--strict`
  - Fail on high-risk drift patterns

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

if [ ! -d "$REGISTRY_DIR" ]; then
  echo "⚠️ Registry directory not found at $REGISTRY_DIR"
  echo "Audit will run in index-only mode."
fi
```

### 0.3 Resolve Report Dir

```bash
REPORT_DIR="${FLAGS_report_dir:-.spec/reports/registry-audit}"
mkdir -p "$REPORT_DIR"
```

---

## 1) Resolve Multi-Repo Roots

This audit must be able to see specs distributed across sibling repos.

Priority rules:

1) If `--repos-config` is provided and valid → use it.
2) Else if `--workspace-roots` is provided → use it.
3) Else → fall back to current repo root only.

Suggested config file: `.spec/smartspec.repos.json`

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

---

## 2) Load Canonical Knowledge

- Load SPEC_INDEX.
- Build a list of all indexed specs and dependency relationships.

If registries exist:
- Load all registry files.

---

## 3) Extract Cross-SPEC Usage Signals

For each indexed spec:

- Resolve `spec.md` across repo roots.
- If adjacent `tasks.md` exists, parse shared-name signals.
- Detect UI presence by:
  - category = `ui`, OR
  - `ui.json` existence.

This workflow must not rewrite any spec artifact.

---

## 4) Audit Rules

### 4.1 API Registry

Detect:
- duplicate logical endpoint names
- inconsistent versioning rules
- conflicting ownership across specs

### 4.2 Data Model Registry

Detect:
- model name collisions
- incompatible model evolution notes
- ambiguous shared vs local models

### 4.3 Glossary

Detect:
- duplicate terms with divergent definitions
- inconsistent capitalization/namespace rules

### 4.4 Critical Sections

Detect:
- cross-cutting requirements that differ between core specs
  - auth
  - authorization
  - audit
  - rate limiting
  - observability

### 4.5 Patterns Registry (optional)

Detect:
- repeated patterns that should be extracted into shared docs

### 4.6 UI Component Registry (optional)

When UI specs exist:

- Validate that component names referenced in UI specs/tasks align with registry.
- Flag components that appear in multiple UI specs but are not registered.

---

## 5) Status-Aware Severity (Portfolio vs Runtime)

To avoid forcing low-quality placeholder specs, severity is interpreted based on mode:

### Portfolio Mode (default)

- Missing shared-name declarations in planned specs → warning
- Inconsistent definitions across core active specs → error

### Runtime Mode

- Any drift impacting active/core specs → error
- Conflicts that could break contracts → error

If a spec has no explicit status, assume `active`.

---

## 6) Cross-Repo Drift Lens

If multi-repo roots are configured:

- Identify shared names that exist only in one repo’s specs.
- Identify registry entries referenced heavily in private specs but not in public ones.

Report these as:

- "Cross-Repo Consistency Risks"

This helps your public/private split remain intentional.

---

## 7) Report Structure

Write a structured report including:

- Index path used
- Registry dir used
- Repo roots resolved
- Counts per registry type
- Top collisions/drift risks
- Cross-repo risk summary
- UI component alignment summary
- Recommended remediation workflows

Suggested follow-ups:

- `/smartspec_validate_index`
- `/smartspec_sync_spec_tasks --mode=additive`
- `/smartspec_reindex_specs`
- `/smartspec_generate_spec --repair-legacy --repair-additive-meta`

---

## Notes

- This workflow is **analysis-first**; it should not mutate registries by default.
- If your team later wants an auto-append mode, add it explicitly and keep it append-only.
- `.spec/` remains the canonical shared truth for SmartSpec v5.2 projects.

