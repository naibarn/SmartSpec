---
description: Manage SmartSpec lifecycle transitions with v5.6 multi-repo + multi-registry checks, non-destructive policy, and chain-consistent safety semantics
version: 5.6
---

# /smartspec_spec_lifecycle_manager

Manage lifecycle states (draft → ready → active → deprecated → archived) across a SmartSpec portfolio.

This v5.6 workflow preserves the v5.2 strengths:

- Index-first lifecycle orchestration
- Multi-repo awareness
- Non-destructive behavior
- Clear separation between portfolio and runtime contexts

And adds v5.6 alignment:

- Multi-registry awareness to prevent cross-repo naming drift
- `--specindex` alias consistency
- `--safety-mode` strictness separated from `--mode portfolio|runtime`
- Optional UI-mode-aware lifecycle checks
- Chain readiness reporting for generate_spec/tasks

---

## Core Principles

- `.spec/` is the canonical governance space.
- `.spec/SPEC_INDEX.json` is the canonical index.
- `.spec/registry/` contains authoritative shared naming.
- Root `SPEC_INDEX.json` remains a legacy mirror.
- `.smartspec/` is tooling-only.

Lifecycle management must remain **non-destructive**:

- Do not rewrite spec narratives.
- Do not rewrite tasks.
- Do not mutate registries by default.

---

## What It Does

- Resolves index, registries, and multi-repo roots.
- Loads a lifecycle target set (one spec or a group).
- Validates readiness criteria per lifecycle transition.
- Detects cross-SPEC/cross-repo ownership ambiguity.
- Emits a transition plan or applies safe status updates where allowed.
- Produces a structured report.

---

## Inputs

- SPEC_INDEX (recommended)
- Target `spec.md` files
- Primary registry
- Optional supplemental registries
- Optional multi-repo config

---

## Outputs

- Lifecycle report under:
  - `.spec/reports/spec-lifecycle-manager/`

- Optional safe updates to index status fields (implementation policy dependent)

---

## Flags

### Lifecycle Mode (Legacy Semantics Preserved)

```bash
--mode=<portfolio|runtime>
```

- `portfolio` (default)
  - Broad governance checks, readiness summaries, and transition recommendations.

- `runtime`
  - CI-grade readiness checks for release gating.

### Safety (NEW, v5.6-aligned)

```bash
--safety-mode=<strict|dev>
--strict
```

- `strict` (default)
  - Block transitions when ambiguity could cause cross-repo duplication or breaking naming drift.

- `dev`
  - Continue with warnings and require next-action notes.

### Index

```bash
--index=<path>
--specindex=<path>
```

### Registries

```bash
--registry-dir=<dir>
--registry-roots=<csv>
```

Precedence:

1) Primary registry authoritative.
2) Supplemental registries read-only validation.

### Multi-Repo

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence.

### Target Selection

Implementation-dependent options may include:

```bash
--spec=<path>
--spec-ids=<csv>
--categories=<csv>
--include-drafts=<true|false>
```

### Optional UI Alignment

```bash
--ui-mode=<auto|json|inline>
```

Default: `auto`.

### Preview / Reporting

```bash
--report=<summary|detailed>
--dry-run
--apply=<true|false>   # if supported
```

---

## 0) Resolve Canonical Context

### 0.1 Resolve SPEC_INDEX

Auto-detect order:

1) `.spec/SPEC_INDEX.json`
2) `SPEC_INDEX.json`
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json`

### 0.2 Resolve Registry View

- Load primary registry.
- Load supplemental registries (if configured) read-only.

If a shared name exists only in supplemental registries:

- Treat it as a cross-repo owner candidate.
- Require explicit ownership notes before promoting lifecycle state in strict mode.

### 0.3 Resolve Multi-Repo Roots

- Use `--repos-config` roots when provided.
- Otherwise add `--workspace-roots`.

If index entries contain `repo:` labels:

- Validate mapping coverage when repos-config is used.

---

## 1) Determine Lifecycle Targets

Priority:

1) `--spec` if provided.
2) `--spec-ids` if index exists.
3) Category-based selection when supported.

If no index exists:

- The manager operates in local-only mode and recommends reindexing.

---

## 2) Read Specs (Read-Only)

Extract:

- declared status
- scope stability signals
- dependency declarations
- API/model/term references
- UI markers

Do not modify spec content.

---

## 3) Readiness Rules (High-Level)

### 3.1 Draft → Ready

Require:

- core sections present
- dependencies declared
- no critical contradictions with index

In multi-repo strict mode:

- require explicit Ownership & Reuse notes for cross-repo dependencies.

### 3.2 Ready → Active

Require:

- stable APIs/models naming alignment with primary registry
- no unresolved critical cross-registry collisions
- dependency specs in active/ready states when policy requires

### 3.3 Active → Deprecated

Require:

- migration notes
- backward compatibility plan when applicable
- registry deprecation markers (if your registry schema supports them)

### 3.4 Deprecated → Archived

Require:

- no active dependents
- documentation snapshot policy satisfied

---

## 4) Cross-Registry & Cross-Repo Gates (NEW)

Before recommending or applying any promotion to `ready` or `active`:

- Validate that shared entity names referenced by the spec:
  - do not conflict with any loaded registry view
  - are not ambiguously owned across repos

If conflicts exist:

- `mode=runtime` + `safety-mode=strict` → blocking
- `mode=portfolio` → warning + remediation tasks

---

## 5) UI Lifecycle Notes (Optional)

When UI addendum applies:

- For JSON-first UI specs:
  - ensure `ui.json` exists or is planned
  - ensure UI component naming aligns with any UI registries

---

## 6) Report Structure

Write a report under `.spec/reports/spec-lifecycle-manager/` containing:

- Index path used
- Registry context used
- Multi-repo roots used
- Targets evaluated
- Transition recommendations
- Blocking issues (if any)
- Cross-repo ownership ambiguity list
- Cross-registry collision summary
- UI readiness notes (if applicable)
- **Chain readiness notes** for:
  - `/smartspec_generate_spec v5.6`
  - `/smartspec_generate_tasks v5.6`

---

## 7) Recommended Follow-ups

- `/smartspec_validate_index`
- `/smartspec_global_registry_audit`
- `/smartspec_generate_spec` (ownership clarification)
- `/smartspec_generate_tasks`
- `/smartspec_sync_spec_tasks`

---

## Notes

- This workflow provides governance safety without rewriting spec content.
- Multi-registry awareness is critical for reliable lifecycle decisions in multi-repo platforms.
- The primary enforcement gates remain validate/spec/tasks in the v5.6 chain.

