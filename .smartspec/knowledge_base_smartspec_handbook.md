# knowledge_base_smartspec_handbook.md

> **Version:** 6.1.2 (Canonical)  
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
- Tasks-driven implementation
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

## 3) Write model

### 3.1 Definitions

- **Safe outputs (allowed by default)**
  - reports: `.spec/reports/**`
  - prompts: `.smartspec/prompts/**`
  - generated helper scripts: `.smartspec/generated-scripts/**`

- **Governed artifacts (require explicit apply)**
  - anything under `specs/**`
  - `.spec/SPEC_INDEX.json`
  - `.spec/WORKFLOWS_INDEX.yaml`
  - any runtime source tree changes (see §3.5)

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

Workflows that read or write filesystem paths MUST enforce:

- **Path normalization**: reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape**: do not read/write through symlinks that resolve outside allowed scopes.
- **Output root safety**: any user-provided `--out` (and any governed target dir) MUST:
  - resolve under config allowlist (e.g., `safety.allow_writes_only_under`)
  - NOT fall under config denylist (e.g., `safety.deny_writes_under`)
  - hard-fail when invalid
- **Spec-id constraints**: `^[a-z0-9_\-]{3,64}$`.
- **No secrets**: redact tokens/keys; use placeholders.
- **Excerpt policy**: reports MUST NOT dump full configs/logs/docs; prefer diffs + short excerpts + hashes.
- **Bounded scanning**: enforce config limits (max files/bytes/time); record reduced coverage when limits are hit.

Workflows that write governed files MUST additionally enforce:

- **Atomic writes**: write via temp+rename (and lock when configured) to avoid partial updates.
- **Output collision**: do not overwrite existing run folders unless explicitly configured.

### 3.5 No source pollution + explicit runtime-tree opt-in

Default rule: SmartSpec workflows MUST NOT modify application runtime source trees.

If a workflow *must* write to a runtime tree (examples: code/tests, `docs/`, `.github/workflows/`, deployment/runtime configs), it MUST require **two gates**:

1) `--apply` (governed)
2) a workflow-specific explicit opt-in flag (examples):
   - `--write-code` (runtime code/tests/config writes)
   - `--write-docs`
   - `--write-ci-workflow`
   - `--write-runtime-config`

Both gates MUST be documented and enforced.

### 3.6 Temporary workspace allowance (for privileged workflows)

Some privileged workflows (e.g., publish/tag flows) may require a temporary workspace (clone/worktree/copy).

Allowed workspace rule:

- Workspace is allowed **only** under the run folder:
  - `.spec/reports/<workflow>/<run-id>/workspace/**`
- Workspace paths MUST still obey §3.4 hardening.
- Workspace contents MUST NOT be treated as governed artifacts.

---

## 4) Configuration (config-first)

### 4.1 Canonical config file

Default path: `.spec/smartspec.config.yaml`

The config file is the single place for environment wiring:

- workspace roots / multi-repo
- registry roots
- language and platform defaults
- output roots
- safety settings (allow/deny roots, redaction, limits, network policy)

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

- **Reserved names:** workflow-specific flags MUST NOT reuse a universal flag name with a different meaning.
  - Example: do NOT use `--platform` to mean "datadog" or "github-pages".
  - Use a namespaced flag such as `--obs-platform` or `--publish-platform`.
- **No new global flags** may be introduced without updating this Handbook.

---

## 6) Positional-first command style

To reduce parameter sprawl, workflows should accept the primary input as a positional argument.

Examples:

- `smartspec_generate_plan <spec.md> --apply`
- `smartspec_generate_tasks <spec.md> --apply`
- `smartspec_implement_tasks <tasks.md> --apply --write-code`
- `smartspec_verify_tasks_progress_strict <tasks.md> --out <dir> --json`

---

## 7) Privileged operations: execution + network policy

### 7.1 No-shell + allowlist + timeouts

Any workflow that executes external commands MUST:

- spawn without a shell (no `sh -c`, no command-string concatenation)
- use an allowlist of binaries (and subcommands where applicable)
- enforce timeouts for every command
- redact captured stdout/stderr using configured redaction

### 7.2 Network deny-by-default + allow-network gate

Default: network access is denied.

If a workflow needs network (fetch/push/publish/webhook, dependency installs, remote downloads), it MUST:

- require an explicit gate flag (recommended: `--allow-network`)
- record in the report whether network was used
- if the runtime cannot enforce deny-by-default, the workflow MUST emit a warning in its summary/report

### 7.3 Secret handling for privileged workflows

- Secrets MUST NOT be accepted as raw CLI flags.
- Prefer environment variables or secret references (e.g., `env:NAME`).
- Reports MUST NOT print secret values; only redaction counts and safe placeholders.

---

## 8) Change Plan requirement (governed writes)

Any workflow that can write governed artifacts MUST produce a Change Plan *before apply*.

Minimum Change Plan contents:

- list of files to be created/modified
- diff summary (or patch files), with redaction
- rationale and safety notes
- hashes of final intended file contents (optional but recommended)

---

## 9) SPEC_INDEX governance (reuse + de-dup)

Any workflow that creates a new spec MUST:

1) Load `.spec/SPEC_INDEX.json`
2) Search for overlap against title/summary/tags/integrations/components
3) Decide reuse vs extend vs supersede

If a strong match exists, **do not create a new overlapping spec**.

---

## 10) Reference system and research requirements

- Reference types: UX benchmark, UI inspiration, API docs, Internal spec reuse
- Reference IDs: `REF-UX-###`, `REF-UI-###`, `REF-API-###`, `REF-SPEC-###`
- Specs using references must provide `references/sources.yaml`
- API integrations must include implementable details (auth, endpoints, error modes, rate limits, etc.)
- No-cloning rule: inspiration only (do not copy layouts/assets/microcopy)

---

## 11) UI/UX minimum standard

Every product-facing spec must include:

- personas/roles + key journeys
- IA (navigation map)
- screens + flows
- state coverage: loading/empty/error/success
- accessibility baseline
- responsive notes
- microcopy guidance

---

## 12) Workflow registry (single source)

Only `.spec/WORKFLOWS_INDEX.yaml` lists **all** workflows.
This Handbook defines the contracts; it does not duplicate the entire registry.

---

## 13) Workflow semantics (core chain)

### 13.1 Canonical execution chain (preferred)

`SPEC → PLAN → TASKS → implement → STRICT VERIFY → SYNC CHECKBOXES`

Where:

- SPEC: `/smartspec_generate_spec`
- PLAN: `/smartspec_generate_plan`
- TASKS: `/smartspec_generate_tasks`
- implement: `/smartspec_implement_tasks`
- STRICT VERIFY: `/smartspec_verify_tasks_progress_strict`
- SYNC CHECKBOXES: `/smartspec_sync_tasks_checkboxes`

### 13.2 Optional helpers (non-canonical)

- PROMPTER: `/smartspec_report_implement_prompter` (recommended before implement for large/complex changes)
- Project routing: `/smartspec_project_copilot`

### 13.3 Dual-command rule

- CLI: `/workflow_name ...`
- Kilo Code: `/workflow_name.md ... --kilocode`

---

## 14) Versioning policy

### 14.1 Minimum workflow version

- All workflow docs under `.smartspec/workflows/*.md` MUST use **version `6.0.0` or higher**.

### 14.2 What version means

- Workflow doc `version:` is the **behavior contract version**.
- YAML `version: 1` fields (e.g., config/index schemas) are **schema versions**.

### 14.3 Optional enforcement (recommended)

Add to `.spec/smartspec.config.yaml`:

```yaml
safety:
  workflow_version_min: "6.0.0"
```

Index validators should fail if any workflow header version is below the minimum.

---

# End of Canonical Handbook

