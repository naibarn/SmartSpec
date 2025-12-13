# knowledge_base_smartspec_install_and_usage.md

# SmartSpec Installation & Usage

> **Version:** 6.1.2  
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

This wrapper focuses on installation, standard execution sequence, and short quickstart commands.

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
/smartspec_generate_spec
/smartspec_generate_plan
/smartspec_generate_tasks
/smartspec_implement_tasks
/smartspec_verify_tasks_progress_strict
/smartspec_sync_tasks_checkboxes
/smartspec_project_copilot
```

### 2.2 Full listing

The complete list of workflows, aliases, write scopes, and supported platforms is stored in:

- `.spec/WORKFLOWS_INDEX.yaml`

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

---

## 4) Quickstart (positional-first + dual command examples)

> Replace paths with your own spec folder.

### 4.1 Generate / refine SPEC (governed → needs apply)

#### CLI

```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_spec.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply \
  --kilocode
```

### 4.2 Generate PLAN (governed → needs apply)

#### CLI

```bash
/smartspec_generate_plan \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_plan.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply \
  --kilocode
```

### 4.3 Generate TASKS (governed → needs apply)

#### CLI

```bash
/smartspec_generate_tasks \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_tasks.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply \
  --kilocode
```

### 4.4 Implement from TASKS

`/smartspec_implement_tasks` is **tasks-first** and refuses to expand scope beyond selected tasks.

- Validate-only (no writes): use `--validate-only`.
- Writing code/tests/config requires **two gates**: `--apply` + `--write-code`.
- Any action that needs network (dependency install/download/remote fetch) requires `--allow-network`.

#### CLI (validate-only)

```bash
/smartspec_implement_tasks \
  specs/feature/spec-002-user-management/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks/spec-002 \
  --json
```

#### CLI (apply + write code)

```bash
/smartspec_implement_tasks \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --write-code \
  --out .spec/reports/implement-tasks/spec-002 \
  --json
```

#### Kilo Code

```bash
/smartspec_implement_tasks.md \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --write-code \
  --require-orchestrator \
  --out .spec/reports/implement-tasks/spec-002 \
  --json \
  --kilocode
```

### 4.5 Strict verify (safe output → no apply)

#### CLI

```bash
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json
```

#### Kilo Code

```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json \
  --kilocode
```

### 4.6 (Optional) Implementation prompter (safe output → no apply)

Recommended before implement for large/complex changes.

#### CLI

```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --out .smartspec/prompts/spec-002-user-management \
  --json
```

#### Kilo Code

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --out .smartspec/prompts/spec-002-user-management \
  --json \
  --kilocode
```

### 4.7 Sync tasks checkboxes (governed → needs apply)

#### CLI

```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-002-user-management/tasks.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --kilocode
```

---

## 5) Common patterns for newer workflows (v6.1.x)

This section does not list every workflow (see `.spec/WORKFLOWS_INDEX.yaml`). It documents **common contracts** used by newer workflows.

### 5.1 Platform flag collision avoidance

- `--platform` is universal and reserved for `cli|kilo|ci|other`.
- Workflow-specific platforms must use namespaced flags:
  - `--obs-platform` (observability)
  - `--publish-platform` (docs publishing)

### 5.2 Network gating for privileged or tool-driven flows

- Any workflow that fetches/pushes/publishes or runs tools that may touch the network requires `--allow-network`.
- If your environment cannot enforce deny-by-default, expect a warning in reports.

### 5.3 Runtime tree writes require an extra opt-in gate

- Writing into runtime trees (code/tests/config, `docs/`, deployment configs) requires BOTH:
  - `--apply`
  - an explicit opt-in such as `--write-code` / `--write-docs` / `--write-runtime-config`

### 5.4 Implement → verify → sync (example)

#### CLI

```bash
/smartspec_implement_tasks \
  specs/<category>/<spec-id>/tasks.md \
  --apply \
  --write-code \
  --out .spec/reports/implement-tasks \
  --json

/smartspec_verify_tasks_progress_strict \
  specs/<category>/<spec-id>/tasks.md \
  --out .spec/reports/verify-tasks-progress \
  --json

/smartspec_sync_tasks_checkboxes \
  specs/<category>/<spec-id>/tasks.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_implement_tasks.md \
  specs/<category>/<spec-id>/tasks.md \
  --apply \
  --write-code \
  --require-orchestrator \
  --out .spec/reports/implement-tasks \
  --json \
  --kilocode

/smartspec_verify_tasks_progress_strict.md \
  specs/<category>/<spec-id>/tasks.md \
  --out .spec/reports/verify-tasks-progress \
  --json \
  --kilocode

/smartspec_sync_tasks_checkboxes.md \
  specs/<category>/<spec-id>/tasks.md \
  --apply \
  --kilocode
```

### 5.5 Docs generation → publishing (example chain)

#### CLI

```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json

/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

#### Kilo Code

```bash
/smartspec_docs_generator.md \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json \
  --kilocode

/smartspec_docs_publisher.md \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json \
  --kilocode
```

---

## 6) Universal flags (quick reference)

All workflows share:

- `--config`, `--lang`, `--platform`, `--apply`, `--out`, `--json`, `--quiet`

See the Canonical Handbook for definitions.

---

# End of Thin Wrapper


---

## 7) Complete Workflow Usage Guide

SmartSpec v6 includes **56 workflows** organized by use case. This section provides usage patterns for all workflow categories.

### 7.1 Core Workflows (SPEC → PLAN → TASKS)

**Purpose:** Create and refine specifications, plans, and tasks

#### Generate/Refine SPEC

```bash
# CLI
/smartspec_generate_spec --spec specs/<category>/<spec-id>/spec.md --apply

# Kilo Code
/smartspec_generate_spec.md --spec specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

#### Generate from Natural Language

```bash
# CLI
/smartspec_generate_spec_from_prompt "Build a user authentication system with OAuth2"

# Kilo Code
/smartspec_generate_spec_from_prompt.md "Build a user authentication system with OAuth2" --platform kilo
```

#### Generate PLAN

```bash
# CLI
/smartspec_generate_plan specs/<category>/<spec-id>/spec.md --apply

# Kilo Code
/smartspec_generate_plan.md specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

#### Generate TASKS

```bash
# CLI
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --apply

# Kilo Code
/smartspec_generate_tasks.md specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

---

### 7.2 Implementation Workflows

**Purpose:** Implement code, fix errors, and refactor

#### Implement Tasks

```bash
# CLI (validate only)
/smartspec_implement_tasks specs/<category>/<spec-id>/tasks.md --validate-only

# CLI (apply + write code)
/smartspec_implement_tasks specs/<category>/<spec-id>/tasks.md --apply --write-code

# Kilo Code
/smartspec_implement_tasks.md specs/<category>/<spec-id>/tasks.md --apply --write-code --platform kilo
```

#### Code Assistant (Consolidated)

```bash
# CLI
/smartspec_code_assistant --mode implement --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_code_assistant.md --mode implement --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Fix Errors

```bash
# CLI
/smartspec_fix_errors --error-log <path> --apply --write-code

# Kilo Code
/smartspec_fix_errors.md --error-log <path> --apply --write-code --platform kilo
```

#### Refactor Code

```bash
# CLI
/smartspec_refactor_code --target <path> --apply --write-code

# Kilo Code
/smartspec_refactor_code.md --target <path> --apply --write-code --platform kilo
```

---

### 7.3 Verification Workflows

**Purpose:** Verify task progress and evidence

#### Strict Verification

```bash
# CLI
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md --json

# Kilo Code
/smartspec_verify_tasks_progress_strict.md specs/<category>/<spec-id>/tasks.md --json --platform kilo
```

#### Sync Checkboxes

```bash
# CLI
/smartspec_sync_tasks_checkboxes specs/<category>/<spec-id>/tasks.md --apply

# Kilo Code
/smartspec_sync_tasks_checkboxes.md specs/<category>/<spec-id>/tasks.md --apply --platform kilo
```

---

### 7.4 Quality Assurance Workflows

**Purpose:** Quality gates, testing, and test analysis

#### Quality Gate

```bash
# CLI
/smartspec_quality_gate --spec specs/<category>/<spec-id>/spec.md --json

# Kilo Code
/smartspec_quality_gate.md --spec specs/<category>/<spec-id>/spec.md --json --platform kilo
```

#### Generate Tests

```bash
# CLI
/smartspec_generate_tests --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_generate_tests.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Run Test Suite

```bash
# CLI
/smartspec_test_suite_runner --test-dir tests/ --json

# Kilo Code
/smartspec_test_suite_runner.md --test-dir tests/ --json --platform kilo
```

#### Analyze Test Reports

```bash
# CLI
/smartspec_test_report_analyzer --report <path> --json

# Kilo Code
/smartspec_test_report_analyzer.md --report <path> --json --platform kilo
```

---

### 7.5 Security Workflows

**Purpose:** Security analysis, threat modeling, and audits

#### Threat Modeling

```bash
# CLI
/smartspec_security_threat_modeler --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_security_threat_modeler.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Security Audit

```bash
# CLI
/smartspec_security_audit_reporter --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_security_audit_reporter.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Security Evidence Audit

```bash
# CLI
/smartspec_security_evidence_audit --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_security_evidence_audit.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

---

### 7.6 Audit Workflows

**Purpose:** Validate contracts, models, and UI components

#### API Contract Validation

```bash
# CLI
/smartspec_api_contract_validator --openapi <path> --json

# Kilo Code
/smartspec_api_contract_validator.md --openapi <path> --json --platform kilo
```

#### Data Model Validation

```bash
# CLI
/smartspec_data_model_validator --schema <path> --json

# Kilo Code
/smartspec_data_model_validator.md --schema <path> --json --platform kilo
```

#### UI Component Audit

```bash
# CLI
/smartspec_ui_component_audit --component-dir src/components/ --json

# Kilo Code
/smartspec_ui_component_audit.md --component-dir src/components/ --json --platform kilo
```

#### UI Validation

```bash
# CLI
/smartspec_ui_validation --mode consistency --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_ui_validation.md --mode consistency --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

---

### 7.7 Deployment & Operations Workflows

**Purpose:** Deployment planning, hotfixes, releases, and monitoring

#### Deployment Planning

```bash
# CLI
/smartspec_deployment_planner --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_deployment_planner.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Hotfix Assistant

```bash
# CLI
/smartspec_hotfix_assistant --issue <description> --apply --write-code

# Kilo Code
/smartspec_hotfix_assistant.md --issue <description> --apply --write-code --platform kilo
```

#### Release Tagging

```bash
# CLI
/smartspec_release_tagger --version v1.2.3 --apply --allow-network

# Kilo Code
/smartspec_release_tagger.md --version v1.2.3 --apply --allow-network --platform kilo
```

#### Data Migration

```bash
# CLI
/smartspec_data_migration_generator --from-schema <old> --to-schema <new>

# Kilo Code
/smartspec_data_migration_generator.md --from-schema <old> --to-schema <new> --platform kilo
```

#### NFR Performance Planning

```bash
# CLI
/smartspec_nfr_perf_planner --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_nfr_perf_planner.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### NFR Performance Verification

```bash
# CLI
/smartspec_nfr_perf_verifier --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_nfr_perf_verifier.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Observability Configuration

```bash
# CLI
/smartspec_observability_configurator --obs-platform datadog --apply

# Kilo Code
/smartspec_observability_configurator.md --obs-platform datadog --apply --platform kilo
```

---

### 7.8 Documentation Workflows

**Purpose:** Generate and publish documentation

#### Generate Documentation

```bash
# CLI
/smartspec_docs_generator --mode user-guide --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_docs_generator.md --mode user-guide --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

#### Publish Documentation

```bash
# CLI
/smartspec_docs_publisher --docs-dir <path> --publish-platform github-pages --allow-network --apply

# Kilo Code
/smartspec_docs_publisher.md --docs-dir <path> --publish-platform github-pages --allow-network --apply --platform kilo
```

---

### 7.9 Index & Registry Workflows

**Purpose:** Maintain indexes and registries

#### Reindex Specs

```bash
# CLI
/smartspec_reindex_specs --apply

# Kilo Code
/smartspec_reindex_specs.md --apply --platform kilo
```

#### Reindex Workflows

```bash
# CLI
/smartspec_reindex_workflows --apply

# Kilo Code
/smartspec_reindex_workflows.md --apply --platform kilo
```

#### Validate Index

```bash
# CLI
/smartspec_validate_index --strict

# Kilo Code
/smartspec_validate_index.md --strict --platform kilo
```

#### Global Registry Audit

```bash
# CLI
/smartspec_global_registry_audit --json

# Kilo Code
/smartspec_global_registry_audit.md --json --platform kilo
```

---

### 7.10 Governance Workflows

**Purpose:** Manage spec lifecycle and metadata

#### Spec Lifecycle Management

```bash
# CLI
/smartspec_spec_lifecycle_manager --spec-id <spec-id> --action promote --apply

# Kilo Code
/smartspec_spec_lifecycle_manager.md --spec-id <spec-id> --action promote --apply --platform kilo
```

#### Sync Spec/Tasks Metadata

```bash
# CLI
/smartspec_sync_spec_tasks --spec specs/<category>/<spec-id>/spec.md --apply

# Kilo Code
/smartspec_sync_spec_tasks.md --spec specs/<category>/<spec-id>/spec.md --apply --platform kilo
```

#### Data Migration Governance

```bash
# CLI
/smartspec_data_migration_governance --spec specs/<category>/<spec-id>/spec.md

# Kilo Code
/smartspec_data_migration_governance.md --spec specs/<category>/<spec-id>/spec.md --platform kilo
```

---

### 7.11 Utility Workflows

**Purpose:** Helper tools and assistants

#### Project Copilot

```bash
# CLI
/smartspec_project_copilot "What workflow should I use to implement feature X?"

# Kilo Code
/smartspec_project_copilot.md "What workflow should I use to implement feature X?" --platform kilo
```

#### Design System Migration

```bash
# CLI
/smartspec_design_system_migration_assistant --from mui --to antd --apply --write-code

# Kilo Code
/smartspec_design_system_migration_assistant.md --from mui --to antd --apply --write-code --platform kilo
```

---

### 7.12 Prompter Workflows

**Purpose:** Generate implementation prompts

#### Implementation Prompter

```bash
# CLI
/smartspec_report_implement_prompter \
  --spec specs/<category>/<spec-id>/spec.md \
  --tasks specs/<category>/<spec-id>/tasks.md \
  --verify-report .spec/reports/verify-tasks-progress/<run-id>/summary.json

# Kilo Code
/smartspec_report_implement_prompter.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --tasks specs/<category>/<spec-id>/tasks.md \
  --verify-report .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --platform kilo
```

---

### 7.13 Common Workflow Patterns

#### Pattern 1: Full Development Cycle

```bash
# 1. Generate spec from idea
/smartspec_generate_spec_from_prompt "Your feature idea" --apply

# 2. Generate plan
/smartspec_generate_plan specs/<category>/<spec-id>/spec.md --apply

# 3. Generate tasks
/smartspec_generate_tasks specs/<category>/<spec-id>/spec.md --apply

# 4. Generate implementation prompts
/smartspec_report_implement_prompter \
  --spec specs/<category>/<spec-id>/spec.md \
  --tasks specs/<category>/<spec-id>/tasks.md

# 5. Implement
/smartspec_implement_tasks specs/<category>/<spec-id>/tasks.md --apply --write-code

# 6. Verify
/smartspec_verify_tasks_progress_strict specs/<category>/<spec-id>/tasks.md

# 7. Sync checkboxes
/smartspec_sync_tasks_checkboxes specs/<category>/<spec-id>/tasks.md --apply
```

#### Pattern 2: Quality & Security Check

```bash
# 1. Run quality gate
/smartspec_quality_gate --spec specs/<category>/<spec-id>/spec.md

# 2. Security threat modeling
/smartspec_security_threat_modeler --spec specs/<category>/<spec-id>/spec.md

# 3. API contract validation
/smartspec_api_contract_validator --openapi api/openapi.yaml

# 4. UI component audit
/smartspec_ui_component_audit --component-dir src/components/
```

#### Pattern 3: Release Workflow

```bash
# 1. Check release readiness
/smartspec_release_readiness --spec specs/<category>/<spec-id>/spec.md

# 2. Generate documentation
/smartspec_docs_generator --mode user-guide --spec specs/<category>/<spec-id>/spec.md

# 3. Publish documentation
/smartspec_docs_publisher --docs-dir <path> --publish-platform github-pages --allow-network --apply

# 4. Tag release
/smartspec_release_tagger --version v1.2.3 --apply --allow-network
```

---

### 7.14 Finding the Right Workflow

**By Task Type:**
- **Creating specs:** `generate_spec`, `generate_spec_from_prompt`, `reverse_to_spec`
- **Planning:** `generate_plan`, `deployment_planner`, `portfolio_planner`
- **Implementation:** `implement_tasks`, `code_assistant`, `fix_errors`, `refactor_code`
- **Testing:** `generate_tests`, `test_suite_runner`, `test_report_analyzer`
- **Verification:** `verify_tasks_progress_strict`, `quality_gate`
- **Security:** `security_threat_modeler`, `security_audit_reporter`
- **Documentation:** `docs_generator`, `docs_publisher`
- **Deployment:** `deployment_planner`, `hotfix_assistant`, `release_tagger`

**By Platform:**
- **CLI only:** `implement_tasks`
- **CLI + Kilo:** Most workflows
- **CLI + Kilo + CI:** Core workflows, quality gates, audits

**Need Help?**
```bash
/smartspec_project_copilot "your question here"
```

---

# End of Thin Wrapper

