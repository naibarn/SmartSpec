---
description: SmartSpec Reverse to Spec Guide (v5.2)
version: 5.2
last_updated: 2025-12-08
---

# `/smartspec_reverse_to_spec`

**Derive or repair a SPEC from an existing codebase, keeping it aligned with the SmartSpec ecosystem instead of inventing a completely new description.**

This guide updates the legacy intent of `reverse_to_spec` for **SmartSpec v5.2**, while preserving the spirit:

- Use real code as evidence.
- Rebuild or refine `spec.md` so it reflects the current system.
- Avoid breaking existing SPEC indexing and registry rules.

---

## v5.2 Alignment Notes

SmartSpec v5.2 distinguishes between **tooling** and **project-owned truth**.

- **Project-owned canonical space:** `.spec/`
- **Canonical index (preferred):** `.spec/SPEC_INDEX.json`
- **Shared registries (optional):** `.spec/registry/`
- **Legacy mirror (optional):** `SPEC_INDEX.json` at repo root
- **Deprecated tooling index:** `.smartspec/SPEC_INDEX.json`

When this workflow needs to understand spec IDs or relationships, and you do not provide `--index`, it should resolve the index in this order:

1) `.spec/SPEC_INDEX.json` (canonical)
2) `SPEC_INDEX.json` at repo root (legacy mirror)
3) `.smartspec/SPEC_INDEX.json` (deprecated fallback)
4) `specs/SPEC_INDEX.json` (older layout)

The **generated or updated specs** live in the standard `specs/` tree, not under `.smartspec/`.

---

## 1. Summary

`/smartspec_reverse_to_spec` helps when code exists **before** specs, or when specs have become outdated.

- It scans code in a target area.
- Infers responsibilities, data models, key flows, and cross-cutting concerns.
- Produces a new `spec.md` or proposes repairs to an existing one.

### What it solves

- Bringing legacy or orphaned code under SmartSpec governance.
- Recovering design intent after years of code-first evolution.
- Preparing older modules for portfolio planning, lifecycle management, and registry auditing.

### When to use it

- You inherit a codebase with missing or incomplete specs.
- A module has evolved far beyond its original spec.
- You want to add a subsystem into the SmartSpec ecosystem.

---

## 2. Usage

### Basic usage

```bash
/smartspec_reverse_to_spec <code_path> [options...]
```

Where `<code_path>` can be:
- a directory (recommended)
- a single file (for very small modules)

### Spec-aware usage (if spec folder already exists)

```bash
/smartspec_reverse_to_spec --spec specs/feature/spec-004-financial-system/spec.md --code src/
```

This form prefers to **repair** the existing spec instead of generating a completely new one.

---

## 3. Parameters & Options

### Primary Inputs

| Option / Arg | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `<code_path>` | `string` | ✅ Yes (basic form) | Root directory or file to analyze | `src/` |
| `--code` | `string` | Optional | Explicit code root (for spec-aware form) | `--code src/` |
| `--spec` | `string` | Optional | Existing `spec.md` to repair | `--spec specs/feature/spec-004-financial-system/spec.md` |

### Output Options

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--output` | `string` | auto | Output path for new spec | `--output specs/legacy/spec-legacy-001-legacy-module/spec.md` |
| `--id` | `string` | auto | Suggested spec ID if creating a new spec folder | `--id spec-legacy-001-legacy-module` |

### Mode Options

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--mode` | `string` | `generate` | `generate`, `repair`, `compare` | `--mode repair` |

**Mode meanings:**

- `generate`: create a new spec from code evidence.
- `repair`: use code to update or extend an existing spec (additive changes).
- `compare`: produce a report highlighting differences between spec and code, without writing changes.

### Index / Registry Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--index` | `string` | auto-detect | Override SPEC_INDEX path |
| `--specindex` | `string` | alias | Legacy-compatible alias for `--index` |
| `--registry-dir` | `string` | `.spec/registry` | Override registry directory |

When reverse engineering a module that should integrate with other specs, the workflow should **consult registries** to avoid inventing new names for existing concepts.

### Safety / Preview

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--dry-run` | `flag` | `false` | Show proposed spec/changes without writing files | `--dry-run` |
| `--no-write` | `flag` | alias | Alias for `--dry-run` | `--no-write` |
| `--summary-only` | `flag` | `false` | Output only a high-level spec summary | `--summary-only` |

---

## 4. Output Placement Rules

### New Specs

When generating a new spec, the recommended layout is:

```text
specs/<area>/<spec-id>/
  spec.md
  tasks.md        (optional, generated later)
  plan.md         (optional, generated later)
  ui.json         (UI specs only, design-owned)
```

The workflow should propose a folder based on:

- subsystem or bounded context
- naming conventions already used in your SPEC_INDEX

### Repairs

When repairing an existing spec:

- The updated `spec.md` remains in its current folder.
- The workflow should use **additive** patterns by default, minimizing destructive edits.

---

## 5. How It Works (Conceptual)

### Phase 1: Code Discovery

1. Enumerate files under `<code_path>`.
2. Filter by languages and frameworks relevant to your project.
3. Group files by:
   - domain
   - service or module
   - API layer vs core logic vs infra

### Phase 2: Feature & Contract Extraction

The workflow infers:

- Exposed APIs (HTTP, RPC, messaging)
- Data models and their relations
- Key flows or transactions
- Cross-cutting concerns:
  - authentication / authorization
  - audit logging
  - rate limiting
  - observability / metrics

### Phase 3: Cross-check With Index & Registries

To avoid duplicating existing concepts, the workflow should:

- Compare extracted API routes with entries in `api-registry.json` (if present).
- Compare model names to `data-model-registry.json`.
- Compare domain terms to `glossary.json`.
- Recognize critical sections defined in `critical-sections-registry.json`.

### Phase 4: Spec Generation or Repair

**Generate mode:**

- Build a new `spec.md` with sections for:
  - purpose and scope
  - APIs
  - data models
  - flows and scenarios
  - cross-cutting concerns
  - risks / limitations

**Repair mode:**

- Highlight where code diverges from the spec.
- Add missing sections or update descriptions.
- Keep the overall structure and existing valid content.

---

## 6. UI Design Addendum (Conditional)

If the module being reversed clearly maps to UI behavior and your project uses Penpot JSON-first UI:

- The workflow should:
  - Identify React/Vue/SPA components and routes.
  - Describe UI responsibilities and boundaries in `spec.md`.
  - Suggest where `ui.json` could capture layout/structure and component mapping.

- The workflow should **not** auto-generate `ui.json` blindly, but it may:
  - propose a skeleton for `ui.json` in the report, if helpful.

Projects without UI JSON can ignore this behavior.

---

## 7. Examples

### 7.1 Generate a new spec from a legacy module

```bash
/smartspec_reverse_to_spec src/legacy/financial-core --mode generate --id spec-legacy-001-financial-core
```

Result:

- New folder: `specs/legacy/spec-legacy-001-financial-core/`
- New file: `specs/legacy/spec-legacy-001-financial-core/spec.md`

### 7.2 Repair an existing spec based on current code

```bash
/smartspec_reverse_to_spec \
  --spec specs/core/spec-core-004-rate-limiting/spec.md \
  --code src/core/rate-limiting \
  --mode repair
```

Result:

- Existing `spec-core-004-rate-limiting/spec.md` is enriched with:
  - documented real rate limit algorithms
  - up-to-date configuration patterns
  - cross-cutting behavior as implemented

### 7.3 Compare only (no write)

```bash
/smartspec_reverse_to_spec \
  --spec specs/core/spec-core-004-rate-limiting/spec.md \
  --code src/core/rate-limiting \
  --mode compare --dry-run
```

Result:

- A report listing gaps and divergences, but no file changes.

---

## 8. Best Practices

### 1) Use compare/repair before touching core specs

For core specs (auth, authz, audit, rate limiting, etc.):

- Prefer `--mode compare` or `--mode repair` over `generate`.
- Avoid overwriting carefully curated spec narrative.

### 2) Integrate with index and registry

After generating a new spec from code:

```bash
# Rebuild index to include the new spec
/smartspec_reindex_specs

# Validate index health
/smartspec_validate_index --mode=portfolio

# Optionally audit naming
/smartspec_global_registry_audit
```

### 3) Don’t overfit to implementation details

The spec should capture:

- intent
- responsibilities
- contracts
- constraints

Not every line of code or implementation quirk.

---

## 9. Troubleshooting

| Problem | Likely Cause | Solution |
| :--- | :--- | :--- |
| **Spec feels too low-level** | Code is noisy or lacks clear boundaries | Manually refactor the code or run `/smartspec_refactor_code` first. |
| **Spec conflicts with existing registry names** | Module uses different terminology than the rest of the system | Run `/smartspec_global_registry_audit`, then align names and re-run. |
| **New spec folder location feels wrong** | Auto-generated path doesn’t match your domain structure | Move the folder manually and re-run `/smartspec_reindex_specs`. |
| **UI suggestions appear in non-UI module** | Code appears to be UI-like (e.g., React components) but is misclassified | Adjust spec category and re-run with clearer flags. |

---

## 10. Related Workflows

- `/smartspec_generate_spec` (forward direction)
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_implement_tasks`
- `/smartspec_validate_index`
- `/smartspec_reindex_specs`
- `/smartspec_global_registry_audit`
- `/smartspec_refactor_code`

---

## 11. Summary

`/smartspec_reverse_to_spec` is the bridge from **code-first reality** back into the SmartSpec ecosystem. It uses real implementation as evidence to generate or repair specs without breaking centralization rules, while integrating with the canonical index, optional registries, and the UI JSON addendum where applicable.

Use it whenever you need to bring legacy code under governance or re-sync design intent with what actually runs in production.

