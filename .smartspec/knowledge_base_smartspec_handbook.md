# SmartSpec Canonical Handbook

> **Version:** 6.0.0 (Canonical)  
> **Status:** Production Ready  
> **Single source of truth:** This file defines governance, security, and command contracts.
>
> Any other SmartSpec docs must be *thin wrappers* that link to sections here and MUST NOT redefine rules.

---

## 0) Sources of truth and precedence

1) This Handbook (governance + contracts + security)
2) Workflow docs under `.smartspec/workflows/` (command semantics)
3) Project config + registries (implementation context)

If a workflow doc conflicts with this Handbook, **this Handbook wins**.

---

## 1) Goals and principles

SmartSpec is a structured, auditable, multi-phase system for:

- SPEC design
- PLAN and TASKS derivation
- Evidence-driven verification
- Prompted implementation refinement
- Quality gates and audits (reports-first)

Principles:

- **Deterministic artifacts**: outputs can be reproduced.
- **Traceability**: decisions and sources are recorded.
- **Evidence-first**: progress claims require evidence.
- **No duplication**: reuse existing specs/components via references.
- **Secure-by-default**: constrained writes; no secrets.
- **No source pollution**: workflow outputs must not pollute application runtime source trees.
- **Low-friction usage**: config-first, minimal flags, positional-first.

---

## 2) Canonical folder layout

```text
.spec/
  smartspec.config.yaml
  SPEC_INDEX.json
  WORKFLOWS_INDEX.yaml
  registry/
  reports/

.smartspec/
  workflows/
  prompts/
  generated-scripts/
  cache/
  logs/

specs/
  <category>/
    <spec-id>/
      spec.md
      plan.md
      tasks.md
      references/
        sources.yaml
        decisions.md
        notes.md
      design/
      ui/
      schema/
      api/
      testplan/
```

Rules:

- `.spec/SPEC_INDEX.json` is the canonical spec registry.
- `.spec/WORKFLOWS_INDEX.yaml` is the canonical workflow registry.
- `.spec/smartspec.config.yaml` is the canonical configuration.
- `references/` is mandatory when a spec uses external references or APIs.

---

## 3) Write model (safe outputs vs governed artifacts)

### 3.1 Definitions

- **Safe outputs (allowed by default)**
  - reports: `.spec/reports/**`
  - prompts: `.smartspec/prompts/**`
  - generated helper scripts: `.smartspec/generated-scripts/**`

- **Governed artifacts (require explicit apply)**
  - anything under `specs/**`
  - `.spec/SPEC_INDEX.json`
  - `.spec/WORKFLOWS_INDEX.yaml`

### 3.2 Rules

- Workflows may always read the project.
- Workflows may write **safe outputs** without `--apply`.
- Workflows MUST require `--apply` to modify governed artifacts.
- Any workflow that can modify governed artifacts MUST output a **Change Plan** first.

### 3.3 Allowed write scopes

- Spec workflows: `specs/<category>/<spec-id>/**` (governed)
- Spec index updates: `.spec/SPEC_INDEX.json` (governed)
- Workflow index updates: `.spec/WORKFLOWS_INDEX.yaml` (governed)
- Reports: `.spec/reports/**` (safe)
- Prompter outputs: `.smartspec/prompts/**` (safe)
- Generated scripts: `.smartspec/generated-scripts/**` (safe)
  - scripts must never be written into runtime source folders (e.g., `src/`, `app/`, `server/`, `packages/`, `services/`) unless explicitly requested by a human and reviewed.
- Checkbox sync: only checkbox state changes in `tasks.md` (governed)

### 3.4 Security hardening (mandatory)

Workflows that write must enforce:

- **Path normalization**: reject traversal (`..`), absolute paths, control chars.
- **No symlink escape**: do not write through symlinks that resolve outside allowed scopes.
- **Spec-id constraints**: `[a-z0-9_\-]{3,64}`.
- **No secrets**: redact tokens/keys; use placeholders.
- **Atomic registry updates**: governed registries must be lock + atomic (temp + rename). If not possible, do not write.

---

## 4) Configuration (config-first)

### 4.1 Canonical config file

Default path: `.spec/smartspec.config.yaml`

The config file is the single place for environment wiring:

- workspace roots / multi-repo
- registry roots
- language and platform defaults
- output roots
- safety settings

### 4.2 CLI flags are overrides only

Workflows must not require long flag lists for normal usage.

---

## 5) Universal flag contract (minimal)

Every workflow MUST support these flags (same names, same behavior):

- `--config <path>` (default: `.spec/smartspec.config.yaml`)
- `--lang <th|en>` (optional override)
- `--platform <cli|kilo|ci|other>` (optional override)
- `--apply` (required only when modifying governed artifacts)
- `--out <path>`
- `--json`
- `--quiet`

Rules:

- **No new global flags** may be introduced without updating this Handbook.
- Breaking changes are allowed in v6; do not keep legacy flags unless absolutely required.

---

## 6) Positional-first command style

To reduce parameter sprawl, workflows should accept the primary input as a positional argument.

Examples:

- `smartspec_generate_plan <spec.md> --apply`
- `smartspec_generate_tasks <spec.md> --apply`
- `smartspec_verify_tasks_progress_strict <tasks.md> --out <dir> --json`

---

## 7) SPEC_INDEX governance (reuse + de-dup)

Any workflow that creates a new spec MUST:

1) Load `.spec/SPEC_INDEX.json`
2) Search for overlap against title/summary/tags/integrations/components
3) Decide reuse vs extend vs supersede

If a strong match exists, **do not create a new overlapping spec**.

---

## 8) Reference system and research requirements

- Reference types: UX benchmark, UI inspiration, API docs, Internal spec reuse
- Reference IDs: `REF-UX-###`, `REF-UI-###`, `REF-API-###`, `REF-SPEC-###`
- Specs using references must provide `references/sources.yaml`
- API integrations must include implementable details (auth, endpoints, error modes, rate limits, etc.)
- No-cloning rule: inspiration only (do not copy layouts/assets/microcopy)

---

## 9) UI/UX minimum standard

Every product-facing spec must include:

- personas/roles + key journeys
- IA (navigation map)
- screens + flows
- state coverage: loading/empty/error/success
- accessibility baseline
- responsive notes
- microcopy guidance

---

## 10) Workflow registry (single source for listing)

Only `.spec/WORKFLOWS_INDEX.yaml` lists **all** workflows.
KB docs must not copy full lists.

---

## 11) Workflow semantics (core chain)

- `/smartspec_generate_spec`
- `/smartspec_generate_plan`
- `/smartspec_generate_tasks`
- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_report_implement_prompter`
- `/smartspec_sync_tasks_checkboxes`
- `/smartspec_project_copilot`

### 11.1 Platform rendering

- CLI: `/workflow_name ...`
- Kilo Code: `/workflow_name.md ...`

---

## 12) Versioning policy

### 12.1 Minimum workflow version

- All workflow docs under `.smartspec/workflows/*.md` MUST use **version `6.0.0` or higher**.
- Rationale: the legacy line already used `5.x.y`; `6.0.0` is the next major line.

### 12.2 What version means

- Workflow doc `Version:` is the **behavior contract version** (human-facing).
- YAML `version: 1` fields (e.g., config/index schemas) are **schema versions** and may remain `1` while contracts move to `6.x.y`.

### 12.3 Optional enforcement (recommended)

Add to `.spec/smartspec.config.yaml`:

```yaml
safety:
  workflow_version_min: "6.0.0"
```

Validators (e.g., `smartspec_validate_index`) should fail if any workflow header version is below the minimum.

---

# End of Canonical Handbook

