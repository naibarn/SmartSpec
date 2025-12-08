---
description: SmartSpec Generate Plan Manual (v5.6)
version: 5.6
last_updated: 2025-12-08
---

# `/smartspec_generate_plan`

Generate a high-level, dependency-aware `plan.md` from one or more SmartSpec specs.

This v5.6 manual preserves the original planning intent:

- Provide a strategic, phased roadmap.
- Keep planning high-level; detailed execution belongs in `tasks.md`.
- Respect centralization rules.

And extends it to align with the v5.6 chain for multi-repo portfolios.

---

## 1. Summary

`/smartspec_generate_plan`:

1) Reads target `spec.md` files.
2) Uses `SPEC_INDEX.json` (when available) to build a dependency-first plan.
3) Validates shared-name assumptions against registries.
4) Produces a structured plan that can safely drive downstream tasks generation.
5) Adds reconciliation steps when governance ambiguity is detected.

In v5.6, planning is explicitly **multi-repo** and **multi-registry aware**.

---

## 2. Usage

```bash
/smartspec_generate_plan <spec_path> [options...]
```

Examples:

```bash
/smartspec_generate_plan specs/checkout/spec.md

/smartspec_generate_plan specs/checkout/spec.md \
  --ui-mode=auto

# Multi-repo planning
/smartspec_generate_plan specs/checkout/spec.md \
  --repos-config=.spec/smartspec.repos.json \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry" \
  --report=detailed
```

---

## 3. Inputs & Outputs

### Inputs

- One primary `spec.md` path
- Optional additional spec IDs (when supported)
- Optional index + registries
- (UI specs) optional `ui.json`

### Outputs

- `plan.md` next to the primary spec (default)
- Optional custom output path via `--output`
- Report: `.spec/reports/generate-plan/`

---

## 4. Centralization & Index Rules

### Canonical Sources

- `.spec/SPEC_INDEX.json` (canonical)
- `.spec/registry/` (canonical shared naming)
- Root `SPEC_INDEX.json` (legacy mirror)

### SPEC_INDEX Auto-Detect Order

1) `.spec/SPEC_INDEX.json`
2) `SPEC_INDEX.json`
3) `.smartspec/SPEC_INDEX.json` (deprecated)
4) `specs/SPEC_INDEX.json`

---

## 5. Key Flags

### 5.1 Output

```bash
--output=<path>
--dry-run
--nogenerate          # alias if supported
```

### 5.2 Index & Registry

```bash
--index=<path>
--specindex=<path>    # legacy alias
--registry-dir=<dir>
--registry-roots=<csv>
```

Registry precedence:

1) `--registry-dir` is authoritative.
2) `--registry-roots` are read-only validation sources.

### 5.3 Multi-Repo

```bash
--workspace-roots=<csv>
--repos-config=<path>
```

- `--repos-config` takes precedence over `--workspace-roots`.

### 5.4 Safety

```bash
--safety-mode=<strict|dev>
--strict                  # legacy alias
```

### 5.5 UI Mode Alignment

```bash
--ui-mode=<auto|json|inline>
--no-ui-json              # alias for inline (if supported)
```

---

## 6. How Planning Works (High-Level)

1) Resolve the canonical index and registry roots.
2) Build multi-repo search roots when configured.
3) Identify planning scope:
   - the target spec
   - optional related specs by ID/category
4) Read specs (read-only).
5) Build or validate the dependency graph.
6) Detect shared entities and ownership signals.
7) Validate against the merged registry view.
8) Produce phased plan:
   - Foundations
   - Shared contracts and patterns
   - Data models and domain
   - Services and use cases
   - APIs and integrations
   - Observability and security
   - UI (conditional)
9) Add explicit reconciliation items when governance ambiguity exists.

---

## 7. Multi-Repo Planning Rules (v5.6)

When a dependency spec resolves to another repository:

- Label it as **external dependency**.
- Emphasize **reuse-not-rebuild**.
- Ensure the plan does not schedule parallel creation of shared APIs/models owned elsewhere.

If a critical dependency cannot be resolved in `strict` safety mode:

- The plan must include an early blocking milestone:
  - “Resolve missing dependency spec and confirm ownership boundaries.”

---

## 8. Multi-Registry Rules (v5.6)

- The plan must treat any shared-name that exists in **any loaded registry** as a reuse candidate.
- If the same name appears in multiple registries with inconsistent meaning:
  - Add an explicit reconciliation milestone.
- The plan must not instruct creation of a shared entity that would collide with any loaded registry view.

---

## 9. UI Addendum

UI sections are included when:

- Index category is `ui`, or
- `ui.json` exists, or
- the spec declares JSON-driven UI workflows.

Planning rules:

- In `json` UI mode:
  - Plan `ui.json` validation/update before component implementation.
  - Plan component mapping and design-token alignment.
  - Keep business logic outside UI JSON.

- In `inline` UI mode:
  - Plan modern responsive UI implementation guided by the spec narrative.
  - Still emphasize shared component reuse.

---

## 10. Best Practices

### Single Repo

```bash
/smartspec_generate_plan specs/.../spec.md
```

### Two or More Repos

```bash
/smartspec_generate_plan specs/.../spec.md \
  --repos-config=.spec/smartspec.repos.json \
  --registry-dir=.spec/registry \
  --registry-roots="../Repo-A/.spec/registry,../Repo-B/.spec/registry"
```

---

## 11. Related Workflows

- `/smartspec_validate_index`
- `/smartspec_generate_spec`
- `/smartspec_generate_tasks`
- `/smartspec_generate_tests`
- `/smartspec_sync_spec_tasks`

---

## 12. For the LLM

When using a plan to guide tasks and implementation:

- Treat registries as authoritative for shared naming.
- Respect cross-repo ownership boundaries.
- Do not invent new shared APIs/models when reuse is indicated.
- If index and spec dependencies conflict, stop and reconcile.
- Re-run planning when upstream specs change materially.

---

## 13. Summary

`/smartspec_generate_plan v5.6` provides a governance-aware roadmap that remains compatible with legacy SmartSpec expectations while protecting multi-repo programs from duplicated shared work and naming drift.

