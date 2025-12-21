# knowledge_base_smartspec_install_and_usage.md

# SmartSpec Installation & Usage

> **Version:** 6.2.0
> **Status:** Production Ready
> **This document is a thin wrapper.**
> Canonical governance lives in: `knowledge_base_smartspec_handbook.md`.

---

## 0) What to read first

Read the Canonical Handbook for:

- governance rules, write model, and security
- universal flag contract
- privileged operation policy (no-shell, allowlist, allow-network gate)
- Change Plan requirement
- SPEC_INDEX reuse/de-dup policy
- reference/research requirements
- UI/UX minimum standard
- workflow registry rules

This wrapper focuses on installation, standard execution sequence, and a complete workflow listing.

---

## 1) Installation overview

Install the SmartSpec workflow suite into your environment (CLI/Kilo/CI) using your platform’s standard method.

After installation, verify these directories exist:

- `.smartspec/workflows/`
- `.spec/` (contains `SPEC_INDEX.json`, `WORKFLOWS_INDEX.yaml`, `smartspec.config.yaml`)

---

## 2) What’s included

### 2.1 Canonical chain (most-used)

```text
SPEC → PLAN → TASKS → implement → STRICT VERIFY → SYNC CHECKBOXES
```

### 2.2 Full Workflow Listing (40 Workflows)

The complete list of workflows, organized by category. For detailed command arguments, see the respective guide or use the `--help` flag.

#### Core Development (5 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_generate_spec` | Create or refine a formal specification from a draft. |
| `/smartspec_generate_spec_from_prompt` | Generate a draft `spec.md` from a natural language prompt. |
| `/smartspec_generate_plan` | Generate a high-level execution plan from a `spec.md`. |
| `/smartspec_generate_tasks` | Generate a detailed, actionable `tasks.md` from a `spec.md`. |
| `/smartspec_implement_tasks` | Implement code and other artifacts based on a `tasks.md`. |

#### Production & Operations (8 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_deployment_planner` | Plan deployment strategy and generate release artifacts. |
| `/smartspec_release_tagger` | Create and push version tags for releases. |
| `/smartspec_production_monitor` | Monitor production health and alert on SLO breaches. |
| `/smartspec_observability_configurator` | Configure monitoring, logging, and tracing. |
| `/smartspec_incident_response` | Manage production incidents from triage to post-mortem. |
| `/smartspec_hotfix_assistant` | Guide the creation and deployment of emergency hotfixes. |
| `/smartspec_rollback` | Plan and execute safe, automated deployment rollbacks. |
| `/smartspec_feedback_aggregator` | Aggregate production feedback into the development cycle. |

#### Maintenance & Optimization (8 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_dependency_updater` | Scan for outdated dependencies and plan safe updates. |
| `/smartspec_refactor_planner` | Detect code smells and plan refactoring efforts. |
| `/smartspec_performance_profiler` | Profile code to find and plan performance optimizations. |
| `/smartspec_data_migration_generator` | Generate database migration scripts from data model changes. |
| `/smartspec_design_system_migration_assistant` | Assist in migrating to a new design system or component library. |
| `/smartspec_reindex_specs` | Rebuild the spec index for improved search and reuse. |
| `/smartspec_reindex_workflows` | Rebuild the workflow index for the copilot. |
| `/smartspec_validate_index` | Validate the integrity of spec and workflow indexes. |

#### Quality & Testing (12 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_generate_tests` | Generate unit, integration, and E2E tests from a `spec.md`. |
| `/smartspec_test_suite_runner` | Run a specified test suite and generate a report. |
| `/smartspec_test_report_analyzer` | Analyze test reports to identify failure patterns. |
| `/smartspec_ci_quality_gate` | Act as a CI gatekeeper, failing builds that don't meet quality standards. |
| `/smartspec_verify_tasks_progress_strict` | Verify progress for a given `tasks.md` using **evidence-only checks**. |
| `/smartspec_sync_tasks_checkboxes` | Synchronize `tasks.md` checkbox markers (`[x]` / `[ ]`) to match the **latest strict verification report**. |
| `/smartspec_api_contract_validator` | Validate API implementation against its OpenAPI/Swagger contract. |
| `/smartspec_data_model_validator` | Validate database schema against the defined data models. |
| `/smartspec_ui_component_audit` | Audit UI components for consistency and adherence to design system. |
| `/smartspec_ui_validation` | Validate UI implementation against design mockups or specs. |
| `/smartspec_nfr_perf_planner` | Plan performance tests based on Non-Functional Requirements. |
| `/smartspec_nfr_perf_verifier` | Verify system performance against NFRs. |

#### Security (2 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_security_audit_reporter` | Scan code for vulnerabilities and generate an audit report. |
| `/smartspec_security_threat_modeler` | Analyze specs to identify and model potential security threats. |

#### Project Management & Support (5 Workflows)

| Command | Description |
| :--- | :--- |
| `/smartspec_project_copilot` | The **read-only front door** into a SmartSpec-enabled repo. |
| `/smartspec_code_assistant` | A single, consolidated helper workflow for various assistance tasks. |
| `/smartspec_report_implement_prompter` | Generate **implementation prompt packs** from verification reports. |
| `/smartspec_docs_generator` | Generate project documentation from specs and code comments. |
| `/smartspec_docs_publisher` | Publish generated documentation to a static site or wiki. |

---

## 3) Standard execution sequence

```text
SPEC → PLAN → TASKS → implement → STRICT VERIFY → SYNC CHECKBOXES
```

Notes:

- **Governed artifacts** (anything under `specs/**` and registry files) require `--apply`.
- **Safe outputs** (reports/prompts/scripts) may be written without `--apply`.
- Workflow-generated helper scripts must be placed under **`.smartspec/generated-scripts/**`**.
- Some runtime-tree writes require an additional explicit opt-in gate (examples: `--write-code`, `--write-docs`, `--write-runtime-config`, `--write-ci-workflow`).
- SPEC can be either:
  - **draft + refine**: `generate_spec_from_prompt` → human edit → `generate_spec`
  - **refine only**: if `spec.md` already exists

---

## 4) Quickstart Examples

> Replace paths with your own spec folder.

### 4.1 Draft SPEC from prompt (first draft)

Use this when you **do not have `spec.md` yet**.

**CLI:**
```bash
/smartspec_generate_spec_from_prompt \
  "<your feature/product prompt>" \
  --out .spec/reports/generate-spec-from-prompt \
  --json
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_generate_spec_from_prompt.md \
  "<your feature/product prompt>" \
  --out .spec/reports/generate-spec-from-prompt \
  --json \
  --platform kilo
```

Next: **human edit** the draft spec to confirm scope, assumptions, constraints, NFRs, and acceptance criteria.

### 4.2 Refine / normalize SPEC (governed → needs apply)

Use this after the human-edited draft, or when you already have a `spec.md`.

**CLI:**
```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_generate_spec.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply \
  --platform kilo
```

### 4.3 Generate PLAN (governed → needs apply)

**CLI:**
```bash
/smartspec_generate_plan \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_generate_plan.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply \
  --platform kilo
```

### 4.4 Generate TASKS (governed → needs apply)

**CLI:**
```bash
/smartspec_generate_tasks \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_generate_tasks.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply \
  --platform kilo
```

### 4.5 Implement from TASKS

`/smartspec_implement_tasks` is **tasks-first** and refuses to expand scope beyond selected tasks.

- Validate-only (no writes): use `--validate-only`.
- Writing code/tests/config requires **two gates**: `--apply` + `--write-code`.
- Any action that needs network (dependency install/download/remote fetch) requires `--allow-network`.

**CLI:**
```bash
# Validate only
/smartspec_implement_tasks \
  specs/feature/spec-002-user-management/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks/spec-002 \
  --json

# Apply and write code
/smartspec_implement_tasks \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --write-code \
  --out .spec/reports/implement-tasks/spec-002 \
  --json
```

**Kilo Code (must have .md + --platform kilo):**
```bash
# Validate only
/smartspec_implement_tasks.md \
  specs/feature/spec-002-user-management/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks/spec-002 \
  --json \
  --platform kilo

# Apply and write code
/smartspec_implement_tasks.md \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --write-code \
  --out .spec/reports/implement-tasks/spec-002 \
  --json \
  --platform kilo
```

### 4.6 Strict verify (safe output → no apply)

**CLI:**
```bash
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json \
  --platform kilo
```

### 4.7 Sync tasks checkboxes (governed → needs apply)

**CLI:**
```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-002-user-management/tasks.md \
  --apply
```

**Kilo Code (must have .md + --platform kilo):**
```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --platform kilo
```

---

## 5) Universal flags (quick reference)

All workflows share:

- `--config`, `--lang`, `--platform`, `--apply`, `--out`, `--json`, `--quiet`

See the Canonical Handbook for definitions.

---

# End of Thin Wrapper
