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

### Quick Install (One-liner)

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

### Verification

After installation, verify these directories exist:

- `.smartspec/workflows/`
- `.spec/` (contains `SPEC_INDEX.json`, `WORKFLOWS_INDEX.yaml`, `smartspec.config.yaml`)

---

## 1.5) Directory Structure and Design Principle (MUST READ)

SmartSpec follows a **strict separation** between read-only knowledge and read-write data:

### `.smartspec/` - Read-Only (Knowledge Base)

**LLM reads only, NEVER modifies**

**Contents:**
- `workflows/` - 58 workflow markdown files
- `scripts/` - 42 Python helper scripts
- `knowledge_base_*.md` - Knowledge files
- `system_prompt_smartspec.md` - System prompt

**Rules:**
- ❌ **NEVER write to `.smartspec/`**
- ❌ **NEVER modify workflows or scripts**
- ✅ Read workflows and follow instructions

### `.spec/` - Read-Write (Project Data)

**LLM reads and writes**

**Contents:**
- `reports/` - **Generated reports** ✨ (ALL workflow outputs)
- `registry/` - Component registry
- `SPEC_INDEX.json` - Spec index
- `WORKFLOWS_INDEX.yaml` - Workflow registry
- `smartspec.config.yaml` - Configuration

**Rules:**
- ✅ **Write reports to `.spec/reports/`**
- ✅ Update registry and specs as needed
- ❌ **NEVER write to `.smartspec/`**

### Correct Path Examples

**Reports (CORRECT):**
```
.spec/reports/implement-tasks/spec-core-001-auth/report.md
.spec/reports/verify-tasks-progress/spec-core-001-auth/summary.json
```

**Reports (INCORRECT):**
```
.smartspec/reports/...  ❌ (read-only area)
```

### Command Examples

**CLI:**
```bash
/smartspec_implement_tasks \
  specs/core/spec-core-001-auth/tasks.md \
  --out .spec/reports/implement-tasks/spec-core-001-auth \
  --apply
```

**Kilo Code:**
```bash
/smartspec_implement_tasks.md \
  specs/core/spec-core-001-auth/tasks.md \
  --out .spec/reports/implement-tasks/spec-core-001-auth \
  --apply \
  --platform kilo
```

**NEVER use:**
```bash
--out .smartspec/reports/...  ❌
```

For detailed explanation, see Section 0.5 in `knowledge_base_smartspec_handbook.md`.

---

## 2) What's included

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
- Some workflows may require additional workflow-specific opt-in flags for runtime-tree writes (check individual workflow documentation).
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
- Writing code/tests/config requires `--apply`.
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

---

## 6) Complete Workflow Parameter Reference

This section provides comprehensive parameter documentation for all 40 workflows, enabling AI agents to accurately answer user questions about workflow usage and available parameters.

### 6.1 smartspec_api_contract_validator

**Description:** Validate API contracts and OpenAPI specifications.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--contract` | Required | Path to the API contract file (e.g., OpenAPI v3 YAML/JSON, GraphQL schema) |
| `--implementation-root` | Required | Path to the root directory of the API source code |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Requested base output root |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Optional | Path to spec file for context |
| `--spec-id` | Optional | Alternative to --spec when project supports spec ID lookup |
| `--strict` | Optional | Fail the gate on any unmet MUST requirement |

**Usage Example:**
```bash
/smartspec_api_contract_validator \
  --contract <path/to/openapi.yaml> \
  --implementation-root <path/to/src> \
  [--spec <path/to/spec.md>] \
  [--spec-id <id>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

---

### 6.2 smartspec_code_assistant

**Description:** Consolidated implementation helper (implement/fix/refactor) producing implementation prompts and code suggestions.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--context` | Optional | Path to log or error file for context |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--mode` | Required | Operation mode (implement\|fix\|refactor) |
| `--out` | Optional | Output directory for generated files |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Optional | Path to spec file |
| `--tasks` | Optional | Path to tasks file |

**Usage Example:**
```bash
/smartspec_code_assistant \
  --mode <implement|fix|refactor> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--context <path/to/log-or-error.txt>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.3 smartspec_data_migration_generator

**Description:** Generate data migration scripts and documentation.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--migration-tool` | Required | Migration tool to use (flyway\|liquibase\|raw-sql) |
| `--out` | Optional | Output directory for migration scripts |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--report` | Required | Path to validation report JSON |

**Usage Example:**
```bash
/smartspec_data_migration_generator \
  --report <path/to/validation-report.json> \
  --migration-tool <flyway|liquibase|raw-sql> \
  [--out <output-root>] \
  [--json]
```

---

### 6.4 smartspec_data_model_validator

**Description:** Validate database schema against defined data models.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--model` | Required | Path to data model definition |
| `--out` | Optional | Output directory for validation report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--schema` | Required | Path to database schema file or connection string |
| `--strict` | Optional | Fail on any validation warning |

**Usage Example:**
```bash
/smartspec_data_model_validator \
  --model <path/to/model.yaml> \
  --schema <path/to/schema.sql> \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

---

### 6.5 smartspec_dependency_updater

**Description:** Scan for outdated dependencies and plan safe updates.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for update plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--scope` | Optional | Scope of dependencies to check (all\|prod\|dev) |

**Usage Example:**
```bash
/smartspec_dependency_updater \
  [--scope <all|prod|dev>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.6 smartspec_deployment_planner

**Description:** Plan deployment strategy and generate release artifacts.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--environment` | Required | Target environment (dev\|staging\|prod) |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for deployment plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Optional | Path to spec file |

**Usage Example:**
```bash
/smartspec_deployment_planner \
  --environment <dev|staging|prod> \
  [--spec <path/to/spec.md>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.7 smartspec_design_system_migration_assistant

**Description:** Assist in migrating to a new design system or component library.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--from` | Required | Current design system identifier |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for migration plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--to` | Required | Target design system identifier |

**Usage Example:**
```bash
/smartspec_design_system_migration_assistant \
  --from <current-design-system> \
  --to <target-design-system> \
  [--out <output-root>] \
  [--json]
```

---

### 6.8 smartspec_docs_generator

**Description:** Generate project documentation from specs and code comments.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--format` | Optional | Output format (markdown\|html\|pdf) |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for generated docs |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--scope` | Optional | Documentation scope (all\|api\|user\|dev) |

**Usage Example:**
```bash
/smartspec_docs_generator \
  [--scope <all|api|user|dev>] \
  [--format <markdown|html|pdf>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.9 smartspec_docs_publisher

**Description:** Publish generated documentation to a static site or wiki.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--docs-dir` | Required | Path to generated documentation directory |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--target` | Required | Publishing target (github-pages\|wiki\|s3\|custom) |

**Usage Example:**
```bash
/smartspec_docs_publisher \
  --docs-dir <path/to/docs> \
  --target <github-pages|wiki|s3|custom> \
  [--json]
```

---

### 6.10 smartspec_feedback_aggregator

**Description:** Aggregate production feedback into the development cycle.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for aggregated feedback |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--source` | Required | Feedback source (logs\|tickets\|surveys\|analytics) |

**Usage Example:**
```bash
/smartspec_feedback_aggregator \
  --source <logs|tickets|surveys|analytics> \
  [--out <output-root>] \
  [--json]
```

---

### 6.11 smartspec_generate_plan

**Description:** Generate a high-level execution plan from a spec.md.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file (positional or --spec) |

**Usage Example:**
```bash
/smartspec_generate_plan \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

---

### 6.12 smartspec_generate_spec

**Description:** Create or refine a formal specification from a draft.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file to refine |

**Usage Example:**
```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply
```

---

### 6.13 smartspec_generate_spec_from_prompt

**Description:** Generate a draft spec.md from a natural language prompt.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for generated spec draft |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--prompt` | Required | Natural language prompt describing the feature (positional) |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_generate_spec_from_prompt \
  "<your feature/product prompt>" \
  --out .spec/reports/generate-spec-from-prompt \
  --json
```

---

### 6.14 smartspec_generate_tasks

**Description:** Generate a detailed, actionable tasks.md from a spec.md.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file (positional or --spec) |

**Usage Example:**
```bash
/smartspec_generate_tasks \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

---

### 6.15 smartspec_generate_tests

**Description:** Generate unit, integration, and E2E tests from a spec.md.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for generated tests |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file |
| `--test-type` | Optional | Type of tests to generate (unit\|integration\|e2e\|all) |

**Usage Example:**
```bash
/smartspec_generate_tests \
  --spec <path/to/spec.md> \
  [--test-type <unit|integration|e2e|all>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.16 smartspec_hotfix_assistant

**Description:** Guide the creation and deployment of emergency hotfixes.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--incident-id` | Required | Incident identifier for tracking |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for hotfix plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_hotfix_assistant \
  --incident-id <incident-id> \
  [--out <output-root>] \
  [--json]
```

---

### 6.17 smartspec_implement_tasks

**Description:** Implement code and other artifacts based on a tasks.md.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--allow-network` | Optional | Allow network access for dependency installation |
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for implementation reports |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--tasks` | Required | Path to tasks file (positional or --tasks) |
| `--validate-only` | Optional | Validate without writing any files |
| `--apply` | Optional | Apply changes (required for actual implementation) |

**Usage Example:**
```bash
/smartspec_implement_tasks \
  specs/feature/spec-002-user-management/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-002 \
  --json
```

---

### 6.18 smartspec_incident_response

**Description:** Manage production incidents from triage to post-mortem.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--incident-id` | Required | Incident identifier for tracking |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--mode` | Required | Operation mode (triage\|investigate\|postmortem) |
| `--out` | Optional | Output directory for incident reports |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_incident_response \
  --incident-id <incident-id> \
  --mode <triage|investigate|postmortem> \
  [--out <output-root>] \
  [--json]
```

---

### 6.19 smartspec_nfr_perf_planner

**Description:** Plan performance tests based on Non-Functional Requirements.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for performance test plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file with NFRs |

**Usage Example:**
```bash
/smartspec_nfr_perf_planner \
  --spec <path/to/spec.md> \
  [--out <output-root>] \
  [--json]
```

---

### 6.20 smartspec_nfr_perf_verifier

**Description:** Verify system performance against NFRs.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for verification report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--results` | Required | Path to performance test results |
| `--spec` | Required | Path to spec file with NFRs |

**Usage Example:**
```bash
/smartspec_nfr_perf_verifier \
  --spec <path/to/spec.md> \
  --results <path/to/results.json> \
  [--out <output-root>] \
  [--json]
```

---

### 6.21 smartspec_observability_configurator

**Description:** Configure monitoring, logging, and tracing.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for observability configs |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--stack` | Required | Observability stack (prometheus\|datadog\|newrelic\|custom) |

**Usage Example:**
```bash
/smartspec_observability_configurator \
  --stack <prometheus|datadog|newrelic|custom> \
  [--out <output-root>] \
  [--json]
```

---

### 6.22 smartspec_performance_profiler

**Description:** Profile code to find and plan performance optimizations.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for profiling report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--target` | Required | Path to code or module to profile |

**Usage Example:**
```bash
/smartspec_performance_profiler \
  --target <path/to/code> \
  [--out <output-root>] \
  [--json]
```

---

### 6.23 smartspec_production_monitor

**Description:** Monitor production health and alert on SLO breaches.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for monitoring reports |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--slo-config` | Required | Path to SLO configuration file |

**Usage Example:**
```bash
/smartspec_production_monitor \
  --slo-config <path/to/slo-config.yaml> \
  [--out <output-root>] \
  [--json]
```

---

### 6.24 smartspec_project_copilot

**Description:** The read-only front door into a SmartSpec-enabled repo.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--query` | Required | Natural language query about the project |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_project_copilot \
  --query "<your question about the project>" \
  [--json]
```

---

### 6.25 smartspec_quality_gate

**Description:** Act as a CI gatekeeper, failing builds that don't meet quality standards.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for quality gate report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--strict` | Optional | Fail on any quality warning |

**Usage Example:**
```bash
/smartspec_quality_gate \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

---

### 6.26 smartspec_refactor_planner

**Description:** Detect code smells and plan refactoring efforts.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for refactoring plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--target` | Required | Path to code to analyze for refactoring |

**Usage Example:**
```bash
/smartspec_refactor_planner \
  --target <path/to/code> \
  [--out <output-root>] \
  [--json]
```

---

### 6.27 smartspec_reindex_specs

**Description:** Rebuild the spec index for improved search and reuse.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_reindex_specs \
  --apply \
  [--json]
```

---

### 6.28 smartspec_reindex_workflows

**Description:** Rebuild the workflow index for the copilot.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |

**Usage Example:**
```bash
/smartspec_reindex_workflows \
  --apply \
  [--json]
```

---

### 6.29 smartspec_release_tagger

**Description:** Create and push version tags for releases.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--version` | Required | Version tag to create (e.g., v1.2.3) |

**Usage Example:**
```bash
/smartspec_release_tagger \
  --version <v1.2.3> \
  [--json]
```

---

### 6.30 smartspec_report_implement_prompter

**Description:** Generate implementation prompt packs from verification reports.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for prompt packs |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--report` | Required | Path to verification report |
| `--spec` | Optional | Path to spec file for context |
| `--tasks` | Optional | Path to tasks file for context |

**Usage Example:**
```bash
/smartspec_report_implement_prompter \
  --report <path/to/report.json> \
  [--spec <path/to/spec.md>] \
  [--tasks <path/to/tasks.md>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.31 smartspec_rollback

**Description:** Plan and execute safe, automated deployment rollbacks.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--environment` | Required | Target environment (dev\|staging\|prod) |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for rollback plan |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--version` | Required | Version to roll back to |

**Usage Example:**
```bash
/smartspec_rollback \
  --environment <dev|staging|prod> \
  --version <v1.2.2> \
  [--out <output-root>] \
  [--json]
```

---

### 6.32 smartspec_security_audit_reporter

**Description:** Scan code for vulnerabilities and generate an audit report.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for audit report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--scope` | Optional | Audit scope (all\|dependencies\|code\|config) |

**Usage Example:**
```bash
/smartspec_security_audit_reporter \
  [--scope <all|dependencies|code|config>] \
  [--out <output-root>] \
  [--json]
```

---

### 6.33 smartspec_security_threat_modeler

**Description:** Analyze specs to identify and model potential security threats.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for threat model |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--spec` | Required | Path to spec file to analyze |

**Usage Example:**
```bash
/smartspec_security_threat_modeler \
  --spec <path/to/spec.md> \
  [--out <output-root>] \
  [--json]
```

---

### 6.34 smartspec_sync_tasks_checkboxes

**Description:** Synchronize tasks.md checkbox markers to match the latest strict verification report.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--apply` | Optional | Apply changes to governed artifacts |
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--tasks` | Required | Path to tasks file (positional or --tasks) |

**Usage Example:**
```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-002-user-management/tasks.md \
  --apply
```

---

### 6.35 smartspec_test_report_analyzer

**Description:** Analyze test reports to identify failure patterns.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for analysis report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--report` | Required | Path to test report file |

**Usage Example:**
```bash
/smartspec_test_report_analyzer \
  --report <path/to/test-report.xml> \
  [--out <output-root>] \
  [--json]
```

---

### 6.36 smartspec_test_suite_runner

**Description:** Run a specified test suite and generate a report.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for test report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--suite` | Required | Test suite to run (unit\|integration\|e2e\|all) |

**Usage Example:**
```bash
/smartspec_test_suite_runner \
  --suite <unit|integration|e2e|all> \
  [--out <output-root>] \
  [--json]
```

---

### 6.37 smartspec_ui_component_audit

**Description:** Audit UI components for consistency and adherence to design system.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for audit report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--strict` | Optional | Fail on any design system violation |

**Usage Example:**
```bash
/smartspec_ui_component_audit \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

---

### 6.38 smartspec_ui_validation

**Description:** UI audit/validation (includes consistency mode).

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--mode` | Required | Validation mode (validation\|consistency) |
| `--out` | Optional | Output directory for validation report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--scope` | Optional | Validation scope (global\|spec\|ui-registry) |
| `--spec` | Optional | Path to spec file |
| `--spec-id` | Optional | Spec ID for lookup |
| `--strict` | Optional | Fail on any validation warning |

**Usage Example:**
```bash
/smartspec_ui_validation \
  --mode <validation|consistency> \
  [--spec <path/to/spec.md>|--spec-id <id>] \
  [--scope <global|spec|ui-registry>] \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

---

### 6.39 smartspec_validate_index

**Description:** Validate SPEC_INDEX and WORKFLOWS_INDEX integrity.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for validation report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--strict` | Optional | Fail on any validation warning |

**Usage Example:**
```bash
/smartspec_validate_index \
  [--out <output-root>] \
  [--json] \
  [--strict]
```

---

### 6.40 smartspec_verify_tasks_progress_strict

**Description:** Strict evidence-only verification using parseable evidence hooks.

**Version:** 6.0.0

**Parameters:**

| Parameter | Status | Description |
|---|---|---|
| `--config` | Optional | Path to custom config file |
| `--json` | Optional | Output in JSON format |
| `--lang` | Optional | Language for output (th\|en) |
| `--out` | Optional | Output directory for verification report |
| `--platform` | Optional | Platform mode (cli\|kilo\|ci\|other) |
| `--quiet` | Optional | Suppress non-essential output |
| `--report-format` | Optional | Report format (md\|json\|both) |
| `--tasks` | Required | Path to tasks file (positional) |

**Usage Example:**
```bash
/smartspec_verify_tasks_progress_strict <path/to/tasks.md> [--report-format <md|json|both>] [--json]
```

---

## 7) Notes on Parameter Documentation

**Universal Flags:** All workflows support the following universal flags:
- `--config <path>`: Path to custom config file
- `--lang <th|en>`: Language for output
- `--platform <cli|kilo|ci|other>`: Platform mode
- `--apply`: Apply changes to governed artifacts (where applicable)
- `--out <path>`: Output directory
- `--json`: Output in JSON format
- `--quiet`: Suppress non-essential output

**Kilo Code Execution:** When executing workflows via Kilo Code, you must:
1. Use the `.md` extension in the workflow name (e.g., `/smartspec_generate_spec.md`)
2. Include the `--platform kilo` flag

**Governed Artifacts:** Workflows that modify governed artifacts (specs, plans, tasks, indexes) require the `--apply` flag.

**Safe Outputs:** Workflows that only generate reports, prompts, or scripts do not require `--apply`.

---

# End of Knowledge Base
