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


---

## 15) Complete Workflow Reference

SmartSpec v6 includes **56 workflows** organized into categories. For detailed usage of each workflow, see the corresponding manual in `.smartspec-docs/workflows/`.

### 15.1 Core Workflows

*Essential workflows for SPEC → PLAN → TASKS chain*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_generate_spec` | Refine spec.md (SPEC-first) with deterministic preview/diff + completeness/reuse checks | cli, kilo, ci |
| `/smartspec_generate_plan` | Convert spec.md → plan.md (preview-first; dependency-aware; reuse-first; governed apply) | cli, kilo, ci |
| `/smartspec_generate_tasks` | Convert spec.md (or plan.md) → tasks.md (verification-ready; preserves IDs/checkboxes; reports always written) | cli, kilo, ci |
| `/smartspec_generate_cursor_prompt` | Generate prompts for Cursor IDE | cli, kilo |
| `/smartspec_generate_implement_prompt` | Generate implementation prompts | cli, kilo |

### 15.2 Verification Workflows

*Task progress and evidence verification*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_verify_tasks_progress_strict` | Strict evidence-only verification using parseable evidence hooks (evidence: type key=value...) | cli, kilo, ci |
| `/smartspec_verify_tasks_progress` | Task progress verification | cli, kilo |

### 15.3 Implementation Workflows

*Code implementation and fixes*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_implement_tasks` | Implement code changes strictly from tasks.md with SmartSpec v6 governance | cli |
| `/smartspec_code_assistant` | Consolidated implementation helper (implement/fix/refactor) producing reports/prompts | cli, kilo |
| `/smartspec_fix_errors` | Fix errors in codebase | cli, kilo |
| `/smartspec_refactor_code` | Refactor code following best practices | cli, kilo |

### 15.4 Prompter Workflows

*Generate implementation prompts*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_report_implement_prompter` | Generate implementation prompt packs from spec + tasks + optional strict verify report | cli, kilo |

### 15.5 Spec Generation

*Bootstrap and reverse-engineer specs*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_generate_spec_from_prompt` | Bootstrap starter specs from a natural-language prompt (reuse-first; reference-pack aware; no-network) | cli, kilo |
| `/smartspec_reverse_to_spec` | Reverse-engineer a spec from existing implementation | cli, kilo |

### 15.6 Governance Workflows

*Spec lifecycle and metadata management*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_spec_lifecycle_manager` | Manage spec lifecycle fields and index links | cli, kilo |
| `/smartspec_sync_spec_tasks` | Keep spec/plan/tasks metadata aligned | cli, kilo |
| `/smartspec_data_migration_governance` | Define migration governance and produce helper artifacts (reports/scripts) | cli, kilo, ci |

### 15.7 Index Maintenance

*Registry and index operations*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_reindex_specs` | Rebuild/refresh SPEC_INDEX.json from specs/** (non-destructive; reports always written) | cli, kilo, ci |
| `/smartspec_reindex_workflows` | Rebuild/refresh WORKFLOWS_INDEX.yaml from .smartspec/workflows/** (non-destructive; reports always written) | cli, kilo, ci |
| `/smartspec_validate_index` | Validate SPEC_INDEX and WORKFLOWS_INDEX integrity | cli, kilo, ci |
| `/smartspec_global_registry_audit` | Audit global registry for consistency | cli, kilo |
| `/smartspec_smartspec_reindex_workflows` | Reindex SmartSpec workflows | cli, kilo |

### 15.8 Quality Assurance

*Quality gates and testing*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_quality_gate` | Consolidated quality gate (replaces ci_quality_gate + release_readiness) | cli, kilo, ci |
| `/smartspec_ci_quality_gate` | CI/CD quality gate checks | cli, kilo, ci |
| `/smartspec_generate_tests` | Generate test artifacts/suggestions (prompts/scripts/reports) | cli, kilo |
| `/smartspec_test_suite_runner` | Run test suites and generate reports | cli, kilo, ci |
| `/smartspec_test_report_analyzer` | Analyze test reports and generate insights | cli, kilo, ci |

### 15.9 Security Workflows

*Security analysis and audits*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_security_threat_modeler` | Model security threats and generate mitigation strategies | cli, kilo, ci |
| `/smartspec_security_audit_reporter` | Generate security audit reports | cli, kilo, ci |
| `/smartspec_security_evidence_audit` | Audit security evidence and controls (reports) | cli, kilo, ci |

### 15.10 Audit Workflows

*Component and system audits*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_api_contract_validator` | Validate API contracts and OpenAPI specifications | cli, kilo, ci |
| `/smartspec_data_model_validator` | Validate data models and database schemas | cli, kilo, ci |
| `/smartspec_ui_component_audit` | Audit UI components for consistency and best practices | cli, kilo, ci |
| `/smartspec_ui_validation` | UI audit/validation (includes consistency mode) | cli, kilo, ci |
| `/smartspec_ui_consistency_audit_manual` | UI consistency audit manual | cli, kilo |
| `/smartspec_ui_validation_manual` | UI validation manual | cli, kilo |

### 15.11 Deployment & Operations

*Release, deployment, and operational workflows*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_deployment_planner` | Plan deployment strategies and generate deployment artifacts | cli, kilo, ci |
| `/smartspec_hotfix_assistant` | Assist in creating and managing hotfixes | cli, kilo, ci |
| `/smartspec_release_tagger` | Tag releases and manage version control | cli, kilo, ci |
| `/smartspec_data_migration_generator` | Generate data migration scripts and plans | cli, kilo, ci |
| `/smartspec_release_readiness` | Check release readiness | cli, kilo |
| `/smartspec_nfr_perf_planner` | Plan non-functional requirements for performance | cli, kilo, ci |
| `/smartspec_nfr_perf_verifier` | Verify performance non-functional requirements | cli, kilo, ci |
| `/smartspec_observability_configurator` | Configure observability and monitoring | cli, kilo, ci |
| `/smartspec_observability_runbook_generator` | Generate operational runbooks | cli, kilo, ci |
| `/smartspec_portfolio_planner` | Plan and manage project portfolios | cli, kilo |

### 15.12 Documentation Workflows

*Documentation generation and publishing*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_docs_generator` | Generate documentation from specs | cli, kilo, ci |
| `/smartspec_docs_publisher` | Publish documentation to various platforms | cli, kilo, ci |
| `/smartspec_project_copilot` | Read-only project copilot that summarizes status and routes users to correct SmartSpec workflows | cli, kilo |
| `/smartspec_project_copilot_manual` | Project copilot manual | cli, kilo |
| `/smartspec_smart_spec_install_manual` | SmartSpec installation manual | cli, kilo |
| `/smartspec_smart_spec_manuals_aligned_workflows` | Align manuals with workflows | cli, kilo |

### 15.13 Utility Workflows

*Helper and support workflows*

| Workflow | Purpose | Platforms |
|----------|---------|-----------|
| `/smartspec_sync_tasks_checkboxes` | Sync checkbox states in tasks.md using a strict verifier summary.json (checkbox-only governed write; preview-first) | cli, kilo |
| `/smartspec_tasks_checkboxes` | Manage task checkboxes | cli, kilo |
| `/smartspec_design_system_migration_assistant` | Assist in migrating between design systems (e.g., MUI to Ant Design) | cli, kilo, ci |
| `/smartspec_smartspec_workflow_overview_guide` | Overview guide for SmartSpec workflows | cli, kilo |

---

### 15.14 Workflow Discovery

To find the right workflow for your task:

1. **Check WORKFLOWS_INDEX.yaml**: `.spec/WORKFLOWS_INDEX.yaml` contains the complete registry with categories, purposes, and platform support
2. **Use project copilot**: `/smartspec_project_copilot "your question"` can recommend the appropriate workflow
3. **Browse by category**: Workflows are organized by category (core, verify, implement, quality, security, etc.)
4. **Read manuals**: Each workflow has a detailed manual in `.smartspec-docs/workflows/<workflow_name>.md`

---

# End of Canonical Handbook

