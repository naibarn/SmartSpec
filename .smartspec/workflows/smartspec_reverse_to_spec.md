---
name: /smartspec_reverse_to_spec
version: 5.7.0
role: reverse-engineering/authoring
write_guard: ALLOW-WRITE
purpose: Reverse-engineer existing implementation into SmartSpec-compatible specs and registries while enforcing centralized governance (.spec/, SPEC_INDEX, registries, UI JSON).
version_notes:
  - v5.2: initial reverse-to-spec workflow for SmartSpec centralization
  - v5.7.0: documentation alignment with SmartSpec v5.6–v5.7 chain; behavior remains backward-compatible with v5.2
---

# /smartspec_reverse_to_spec

Reverse-engineer existing code and project structure into SmartSpec-compatible specification artifacts while enforcing centralized, conflict-resistant governance.

This workflow is intended for:
- legacy projects without consistent specs
- partially documented systems
- migration to SmartSpec centralization

It enforces:
- **`.spec/` as the canonical project-owned space**
- **`.spec/SPEC_INDEX.json` as canonical index**
- **`.spec/registry/` as shared source of truth**
- `.smartspec/` as tooling-only
- **UI design source of truth in `ui.json`** when UI specs exist

> **Write guard & modes (v5.7.0 clarification)**
> - Role: reverse-engineering/authoring.
> - Default write behavior by mode:
>   - `recommend`: read-only (NO-WRITE), only reports.
>   - `generate-drafts`: ALLOW-WRITE for new spec folders/files.
>   - `repair-legacy`: ALLOW-WRITE for additive metadata/companion files.
> - Must never delete or destructively overwrite existing `spec.md` or registry entries.

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

> **Additive v5.7.0 flags (optional)**
> - `--registry-roots` Supplemental registry roots (read-only; for cross-repo collision detection).
> - `--workspace-roots` Additional repo roots to scan.
> - `--repos-config` Preferred JSON mapping of repos; takes precedence over `--workspace-roots`.
> - `--safety-mode=<strict|dev>` (alias: `--strict` → `strict`).
> - `--dry-run` Simulate generate/repair modes without writing files.

---

## 0) Resolve Canonical Index & Registry

### 0.1 Resolve SPEC_INDEX (Single Source of Truth)

Detection order:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` (legacy root mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated)  
4) `specs/SPEC_INDEX.json` (older layout)

If none is found:
- in `recommend` mode: continue with warnings.
- in `generate-drafts`/`repair-legacy` + `--safety-mode=strict`: treat as high-risk; prefer `--dry-run` and recommendations over writes.

### 0.2 Resolve Registry Directory

- primary registry: `--registry-dir` (default `.spec/registry`).
- supplemental registries (v5.7.0): from `--registry-roots` (read-only).

Registry rules:
- primary registry is authoritative.
- supplemental registries detect collisions and ownership ambiguity.

### 0.3 Resolve Multi-Repo Roots (v5.7.0)

- build repo roots from `--repos-config` when present.
- otherwise merge `--workspace-roots` with current repo.
- treat other repos as **read-only**; do not write specs into sibling repos unless explicitly allowed by governance.

---

## 1) Determine Reverse Scope

- If `--scope` provided:
  - limit scanning to that path/module.
- Otherwise:
  - scan key directories for service, domain, infra, and UI layers.

Scope decisions should favor cohesive, meaningful boundaries over overly fine-grained specs.

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

If SPEC_INDEX exists:

- Match discovered modules to existing specs.
- Classify findings into:
  1) Already covered
  2) Partially covered (missing sections)
  3) Not covered (candidate new spec)
  4) Overlapping (potential split/merge)

Under `--safety-mode=strict` / `--strict`:
- avoid automatically reassigning ownership.
- prefer recommendations over destructive moves.

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
  - do not auto-rename in code in this workflow.

If a name appears in supplemental registries with conflicting meaning:
- mark as **cross-repo ownership ambiguity**.
- recommend governance reconciliation.

---

## 5) UI JSON Addendum (Conditional)

Apply when:
- the inferred/spec-matched category is `ui`, or
- UI component layers are detected, or
- an existing UI spec folder contains `ui.json`.

Rules:

- UI design source of truth should be **JSON** (`ui.json`) for Penpot/JSON-first flows.
- `ui.json` should not embed business logic.
- Extract UI concerns into:
  - visual structure
  - component mapping
  - tokens/variants

When generating drafts:
- if a UI spec is inferred and no `ui.json` exists:
  - create a **placeholder** `ui.json` draft suggestion or file (depending on mode).

If the project does not use UI JSON:
- allow a non-blocking pathway:
  - keep UI information in `spec.md`.
  - recommend adopting `ui.json` for design-team workflows.

For v5.7.0, when creating or suggesting `ui.json`, prefer including a `meta` block:

```jsonc
{
  "meta": {
    "source": "reverse_to_spec",            // tool identifier
    "generator": "smartspec_reverse_to_spec", // workflow name
    "generated_at": "<timestamp>",
    "design_system_version": "TODO_review",
    "style_preset": "TODO_review",
    "review_status": "unreviewed"           // unreviewed | designer_approved | overridden
  },
  "screens": []
}
```

This makes future UI governance and AI-assisted updates safer.

---

## 6) Mode Behavior

### 6.1 `recommend` (default)

- Produce a reverse report only.
- Suggest:
  - new specs
  - missing sections
  - registry additions
  - index improvements
- Do **not** write new files.

### 6.2 `generate-drafts`

- Create draft spec folders for uncovered modules:
  - `specs/<category>/<spec-id>/`
- Generate minimal `spec.md` skeletons.
- If UI spec:
  - generate a minimal `ui.json` placeholder template.
- Do not overwrite existing `spec.md`.
- Respect `--dry-run` by simulating writes.

### 6.3 `repair-legacy`

- Intended to support older SmartSpec projects.
- May add **additive metadata** or companion files to align with centralization.
- Must not delete or rewrite core content of legacy `spec.md`.

Under `--safety-mode=strict`:
- prefer recommendations or `--dry-run` when ambiguity is high.

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

## 10) Weakness & Risk Check (v5.7.0)

Before treating this workflow as stable in a repo, verify:

1. It never deletes or destructively rewrites existing specs.
2. It keeps `.spec/` as canonical and uses mirrors only as secondary.
3. It respects registry precedence and cross-repo ownership.
4. It clearly marks speculative inferences vs. confirmed mappings.
5. It treats UI JSON as design-owned and does not embed business logic.
6. It records high-ambiguity findings as recommendations instead of applying changes directly.

---

## 11) Legacy Flags Inventory

- **Kept (legacy):**
  - `--index`
  - `--registry-dir`
  - `--scope`
  - `--mode`
  - `--mirror-root`
  - `--strict`

- **New additive (v5.7.0):**
  - `--registry-roots`
  - `--workspace-roots`
  - `--repos-config`
  - `--safety-mode` (with `--strict` as alias)
  - `--dry-run`

No legacy flags are removed or weakened.

