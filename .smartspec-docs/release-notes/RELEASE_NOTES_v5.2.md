# SmartSpec v5.2 Release Notes

Release line: **v5.2.0–v5.2.1**  
Focus: **Centralization-compatible governance for large, multi-team specs**  
Status: **Backward compatible with the existing `SPEC_INDEX.json` schema**

---

## Overview

SmartSpec v5.2 introduces a centralization model that reduces cross-SPEC conflicts in large projects by separating:

- **Project-owned governance** (long-lived, canonical)
- **Tool-owned runtime artifacts** (ephemeral, versioned by the tool)

This release keeps the **existing `SPEC_INDEX.json` entry structure** intact while upgrading how workflows **find, validate, and reuse** shared data.

---

## Highlights

- **Project Spec Hub**: new default location for project-owned SmartSpec governance files.  
  Recommended: `.spec/`
- **Global Registries**: standardized location and usage pattern for shared naming/contracts:
  - critical sections fingerprints
  - data models and fields
  - APIs/endpoints
  - glossary terms
- **Consistent Resolvers** across workflows for:
  - SPEC_INDEX
  - config
  - registry directory
- **Legacy-safe Repair Mode** for existing specs:
  - read-only spec parsing
  - additive metadata allowed only when explicitly enabled

---

## What’s New in v5.2.0

### 1) Centralization model

**New recommended structure**

```text
project-root/
  .spec/                      # project-owned (canonical governance)
    smartspec.config.json
    registry/
  .smartspec/                 # tool-owned runtime
    system_prompt.md
    Knowledge-Base.md
    constitution.md
    backups/
    reports/
    logs/
  specs/
    core/
    feature/
    ui/
```

**Key behaviors**
- `.spec/` is the home for **project governance**.
- `.smartspec/` remains the home for **tool prompts and run artifacts**.
- No breaking changes to `SPEC_INDEX.json` schema.

### 2) Registry-first conflict prevention

Workflows now prioritize global registries to prevent:
- duplicate or inconsistent entity names
- API namespace drift
- conflicting glossary terms
- uncontrolled edits to critical spec sections

### 3) New flags

- `--spec-hub-dir`
- `--registry-dir`
- `--config-path`
- `--specindex`
- `--repo=public|private|shared`

These allow explicit overrides while keeping sensible defaults.

### 4) Output dir semantics clarified

`--output-dir` (default `.smartspec/`) is now strictly for:
- backups
- reports
- logs

Registries are **not created under output dir** by default.

---

## What’s New in v5.2.1

### Legacy Repair Support

Two new safety flags for upgrading older projects without disrupting their specs:

- `--repair-legacy`
  - reads `spec.md` as read-only
  - creates/repairs required centralization files (hub, registries, index copy)
  - generates a repair report

- `--repair-additive-meta`
  - only valid with `--repair-legacy`
  - allows appending a small additive metadata block to `spec.md`
  - **no edits to existing narrative content**

This upgrade path is designed to stabilize large spec portfolios before deeper refactors.

---

## Updated Workflows (Centralization-Compatible)

The following workflows were updated to share the same centralization contract:

### Core execution
- `smartspec_generate_spec`
- `smartspec_generate_plan`
- `smartspec_generate_tasks`
- `smartspec_implement_tasks`
- `smartspec_verify_tasks_progress`

### Quality & maintenance
- `smartspec_fix_errors`
- `smartspec_refactor_code`
- `smartspec_generate_tests`
- `smartspec_sync_spec_tasks`
- `smartspec_reverse_to_spec`
- `smartspec_reindex_specs`
- `smartspec_validate_index`

### Prompt helpers
- `smartspec_generate_implement_prompt`
- `smartspec_generate_cursor_prompt`

**Common upgrades across the set**
- Shared resolver order for index/config/registries
- Registry-first naming
- Index “preflight gate” before plan/tasks/implement/verify
- Safer write scopes:
  - generate workflows may update registries/index (with guards)
  - implement/verify workflows treat registries/index as read-only

---

## New Workflows Added in the v5.2 Line

These governance workflows extend SmartSpec from single-spec execution
to **portfolio-level stability**:

1) **Portfolio Planner**
   - builds roadmap views from `SPEC_INDEX`
   - highlights dependency bottlenecks, priority hotspots, and repo-policy risks

2) **Spec Lifecycle Manager**
   - introduces system-wide handling for:
     - draft → active → deprecated → archived
   - runs impact analysis for dependents

3) **Global Registry Audit**
   - scans registries + specs/tasks to detect semantic drift
   - outputs alignment recommendations without auto-rewriting tasks

---

## UI Track Support (Penpot JSON-First)

v5.2 introduces a safe and scalable rule set for UI-category specs:

- **`ui.json` is the design source of truth** (Penpot-editable).
- **Business logic must not live in `ui.json`.**
- Optional UI registry:
  - `.spec/registry/ui-component-registry.json`

Workflows handling UI specs should split tasks into:
1) Design (UI team)
2) Component binding (Penpot → code)
3) Logic (dev team)

Legacy UI projects (no JSON yet) should be treated as:
- **WARN** with optional migration tasks, not hard failures.

---

## Migration Notes

### Recommended upgrade path

1) Create the project hub:
   - `.spec/`
   - `.spec/registry/`

2) For existing specs:
   - run `generate-spec` with:
     - `--repair-legacy`
     - `--repair-additive-meta` (only if you want minimal metadata linkage)

3) Validate and rebuild governance:
   - `smartspec_validate_index`
   - `smartspec_reindex_specs --migrate` (if applicable)

4) Normalize shared contracts:
   - `smartspec_global_registry_audit`
   - then re-run `smartspec_generate_tasks` on high-priority specs

### Compatibility

- The `SPEC_INDEX.json` schema remains unchanged.
- Legacy root indexes remain readable.
- `.smartspec/` remains valid for tool prompts and runtime outputs.

---

## Breaking Changes

**None.**  
This release is designed for incremental adoption.

---

## Known Limitations

- Repo policy enforcement (public ↔ private) is supported by metadata and rules,
  but may require team-specific config to become fully strict.
- Registry semantics beyond naming (deep domain equivalence) still benefit from
  human review during audits.

---

## What’s Next

The v5.2 line establishes the foundation for:
- stronger public/private contract enforcement
- richer spec quality scoring
- production feedback loops (SLA/observability) tied back into specs
- automated portfolio risk dashboards

---

## Appendix: Flag Quick Reference

```text
Centralization
  --spec-hub-dir
  --registry-dir
  --config-path
  --specindex
  --repo=public|private|shared

Legacy repair
  --repair-legacy
  --repair-additive-meta
```
