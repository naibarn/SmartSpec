---
description: Audit global registries for cross-SPEC and cross-repo naming integrity with SmartSpec v5.6 multi-registry precedence, multi-repo awareness, and chain readiness guarantees
version: 5.6
---

# /smartspec_global_registry_audit

Audit SmartSpec registries to detect naming drift, duplicate shared entities, and cross-repo conflicts before they reach implementation.

This v5.6 workflow preserves the v5.2 audit intent and scope while adding:

- **Multi-registry support** with explicit precedence rules.
- **Multi-repo awareness** aligned with the v5.6 chain.
- **Safety-mode strictness** separated from the existing `--mode` semantics.
- **Chain readiness reporting** for `/smartspec_generate_spec v5.6` and `/smartspec_generate_tasks v5.6`.

Recommended chain placement:

1) `/smartspec_reindex_specs` (when portfolio structure changes)
2) `/smartspec_validate_index`
3) `/smartspec_global_registry_audit`
4) `/smartspec_generate_spec`
5) `/smartspec_generate_plan`
6) `/smartspec_generate_tasks`
7) `/smartspec_sync_spec_tasks`

---

## Core Principles

- **`.spec/` is the canonical project-owned governance layer**.
- **`.spec/registry/` is the primary shared naming source of truth** for the current repo.
- **Supplemental registries may exist in sibling repos**.
- **Audit must not rewrite registry contents** unless a separate future “fix” policy explicitly allows safe normalization.

---

## What It Does

- Resolves primary registry and optional supplemental registries.
- Builds a merged validation view with deterministic precedence.
- Loads SPEC_INDEX if available for coverage and ownership signals.
- Audits:
  - API registries
  - data-model registries
  - glossary
  - critical sections
  - patterns (optional)
  - UI components (optional)
  - file-ownership (optional)
- Detects:
  - same-name/different-meaning conflicts
  - same-meaning/different-name duplication
  - missing ownership signals for high-impact shared entities
  - registry coverage gaps for heavily referenced shared names
- Produces a structured report with remediation guidance.

---

## Inputs

- Primary registry directory (default `.spec/registry`)
- Optional supplemental registry roots
- Optional SPEC_INDEX
- Optional multi-repo configuration to locate index/specs for coverage analysis

---

## Outputs

- Audit report under:
  - `.spec/reports/global-registry-audit/`

---

## Flags

### Mode (Legacy Semantics Preserved)

```bash
--mode=<portfolio|runtime>
```

- `portfolio` (default)
  - Broad, program-level audit.
  - Emphasizes coverage, duplication risk, and long-term consistency.

- `runtime`
  - CI-friendly strictness for naming safety.
  - Emphasizes collision, ownership ambiguity, and breaking risk.

### Safety (NEW, v5.6-aligned)

```bash
--safety-mode=<strict|dev>
--strict
```

- `strict` (default)
  - Treat cross-registry conflicts as high-severity.
  - Require explicit remediation steps in the report.

- `dev`
  - Continue with warnings.

`--strict` acts as a legacy alias for strict gating.

### Index

```bash
--index=<path>
--specindex=<path>     # legacy alias
```

### Primary Registry

```bash
--registry-dir=<dir>
```

Default:
- `.spec/registry`

### Supplemental Registries (NEW)

```bash
--registry-roots=<csv>
```

- Comma-separated registry directories loaded **read-only**.
- Intended for multi-repo platforms.

### Multi-Repo (Alignment)

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence over `--workspace-roots`.
- Recommended path: `.spec/smartspec.repos.json`.

### Reporting

```bash
--report=<summary|detailed>
--dry-run
```

---

## 0) Resolve Index & Registry Context

### 0.1 Resolve SPEC_INDEX

Detection order (unless overridden):

1) `.spec/SPEC_INDEX.json`
2) `SPEC_INDEX.json`
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json`

### 0.2 Resolve Registry View

1) Load **primary** registry directory.
2) Load **supplemental** registries (if provided) as read-only.

**Precedence Rules (v5.6):**

- If a name exists in the primary registry, it is authoritative.
- If a name exists only in supplemental registries:
  - treat as cross-repo candidate
  - audit for potential duplication risk if the primary registry lacks an equivalent entry

---

## 1) Registry Families to Audit

Expected files when present:

- `api-registry.json`
- `data-model-registry.json`
- `glossary.json`
- `critical-sections-registry.json`
- `patterns-registry.json` (optional)
- `ui-component-registry.json` (optional)
- `file-ownership-registry.json` (optional)

Missing optional registries are not errors by default.

---

## 2) Conflict Classification (NEW)

For each registry family, identify:

### 2.1 Same Name, Different Meaning

Example patterns:

- Different signatures for the same API name.
- Different field sets for the same model name.
- Divergent definitions for the same term.

### 2.2 Same Meaning, Different Name

Example patterns:

- Two models that appear structurally identical but are named differently.
- Two API endpoints that expose identical semantics under different names.

### 2.3 Ownership Ambiguity

- A registry entry referenced by multiple specs without clear owner.
- A cross-repo candidate lacking an owner spec mapping.

---

## 3) Coverage & Reference Analysis (Index-Aware)

If SPEC_INDEX is available:

- Compute which specs reference which shared entities.
- Flag high-frequency names that are not present in the primary registry.
- In multi-repo mode, attempt to resolve owner specs across configured repo roots.

---

## 4) Severity Rules

Severity is determined by both `--mode` and `--safety-mode`.

### 4.1 Baseline Severity by `--mode`

- `runtime`:
  - Cross-registry same-name conflicts are **blocking**.
  - Ownership ambiguity for high-impact shared names is **blocking**.

- `portfolio`:
  - Same-name conflicts are **high-visibility warnings** with remediation steps.

### 4.2 Safety Overrides

- `safety-mode=strict`:
  - Escalate cross-repo collisions to blocking for runtime contexts.

- `safety-mode=dev`:
  - Downgrade to warnings, but require explicit next actions.

---

## 5) Report Structure

Write a report under `.spec/reports/global-registry-audit/` containing:

- Index path used
- Primary registry dir
- Supplemental registry roots
- Multi-repo config summary
- Conflicts by family:
  - same-name/different-meaning
  - same-meaning/different-name
- Ownership ambiguity list
- Coverage gaps
- UI registry summary (if present)
- Recommended remediation steps
- **Chain readiness notes** for:
  - `/smartspec_generate_spec v5.6`
  - `/smartspec_generate_tasks v5.6`

---

## 6) Recommended Follow-ups

- `/smartspec_validate_index --report=detailed`
- `/smartspec_reindex_specs` (when large structural changes occurred)
- `/smartspec_generate_spec` for owner clarification
- `/smartspec_sync_spec_tasks --mode=additive` after governance review

---

## Notes

- This audit is intentionally conservative.
- It prioritizes early detection of cross-repo naming drift.
- It does not mutate registries by default.
- Multi-registry flags are optional for single-repo projects but strongly recommended for shared-platform architectures.

