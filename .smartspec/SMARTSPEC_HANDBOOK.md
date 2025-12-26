# SmartSpec Handbook

**Version:** 2.0.0  
**Date:** 2025-12-26  
**Purpose:** Complete handbook for installation, configuration, and usage

---

## 📖 Table of Contents

1. [Installation & Setup](#installation--setup)
2. [Core Concepts](#core-concepts)
3. [Workflow Selection](#workflow-selection)
4. [Configuration](#configuration)
5. [Usage Patterns](#usage-patterns)
6. [Best Practices](#best-practices)

---


---

# knowledge_base_smartspec_handbook.md

> **Version:** 6.2.0 (Canonical)
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

## 0.5) Directory Structure and Design Principle (CRITICAL)

SmartSpec follows a **strict separation** between read-only knowledge and read-write data to prevent LLM from accidentally modifying workflow logic:

### `.smartspec/` - Read-Only (Knowledge Base)

**Purpose:**
- Store workflows, scripts, and knowledge base
- LLM **reads only**, **NEVER modifies**
- Prevents accidental alteration of workflow logic

**Contents:**
- `workflows/` - 58 workflow markdown files
- `scripts/` - 42 Python helper scripts
- `knowledge_base_*.md` - Knowledge files (this file, install guide, etc.)
- `system_prompt_smartspec.md` - System prompt
- `WORKFLOW_PARAMETERS_REFERENCE.md` - Complete parameter reference
- `WORKFLOW_SCENARIOS_GUIDE.md` - Scenario-based guidance

**Rules:**
- ❌ **NEVER write to `.smartspec/`**
- ❌ **NEVER modify workflows or scripts**
- ❌ **NEVER create files in `.smartspec/`**
- ✅ Read workflows and follow instructions
- ✅ Reference scripts in documentation

### `.spec/` - Read-Write (Project Data)

**Purpose:**
- Store project-specific data
- LLM **reads and writes**
- Reports, specs, registry, configuration

**Contents:**
- `reports/` - **Generated reports** ✨ (ALL workflow outputs)
- `registry/` - Component registry
- `SPEC_INDEX.json` - Spec index
- `WORKFLOWS_INDEX.yaml` - Workflow registry (canonical in-repo)
- `smartspec.config.yaml` - Configuration

**Rules:**
- ✅ **Write reports to `.spec/reports/`**
- ✅ Update registry in `.spec/registry/`
- ✅ Modify specs and data as needed
- ❌ **NEVER write to `.smartspec/`**

### Why This Separation?

1. **Prevent LLM hallucinations**: LLM cannot accidentally modify workflow logic
2. **Version control**: `.smartspec/` can be tracked separately from project data
3. **Security**: Read-only workflows prevent unauthorized modifications
4. **Clarity**: Clear separation between "what to do" (workflows) and "what was done" (reports)

### Correct Path Examples

**Reports (CORRECT):**
```
.spec/reports/implement-tasks/spec-core-001-auth/report.md
.spec/reports/verify-tasks-progress/spec-core-001-auth/summary.json
.spec/reports/ui-component-audit/dashboard/audit.json
.spec/reports/security-audit/api/findings.json
```

**Reports (INCORRECT - DO NOT USE):**
```
.smartspec/reports/...  ❌ (read-only area)
reports/...  ❌ (ambiguous, missing .spec/ prefix)
```

**Registry (CORRECT):**
```
.spec/registry/components.json
.spec/SPEC_INDEX.json
.spec/WORKFLOWS_INDEX.yaml
```

**Workflows (READ ONLY):**
```
.smartspec/workflows/smartspec_implement_tasks.md  ✅ (read only)
.smartspec/scripts/verify_evidence_strict.py  ✅ (read only)
```

### Command Examples with Correct Paths

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
--out .smartspec/reports/...  ❌ (violates read-only principle)
```

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

## 2) Workflow Loops: The Big Picture

SmartSpec is designed around **8 critical workflow loops** that cover the entire software development lifecycle. These loops are not rigid sequences but flexible, interconnected processes that combine multiple workflows to achieve a specific goal.

### 2.1 Understanding Loops vs. Categories

- **6 Categories** (in README): Group workflows by **function** (e.g., Quality, Security). This helps you find the right tool for a job.
- **8 Loops**: Group workflows by **process** (e.g., Debugging, Incident Response). This shows you how to combine tools to solve a problem from end to end.

### 2.2 The 8 Workflow Loops

Here is a summary of each loop, its purpose, and its typical flow.

| # | Loop | Purpose | Typical Flow |
|:-:|:---|:---|:---|
| 1 | **Happy Path Loop** | The primary development cycle from idea to production. | `Ideation → Deploy → Monitor` |
| 2 | **Debugging Loop** | Isolate, fix, and verify bugs found during testing. | `Test Failure → Fix → Verify` |
| 3 | **Incident Response Loop** | Manage and resolve live production incidents. | `Alert → Triage → Resolve` |
| 4 | **Continuous Improvement Loop** | Use production data to drive new features and fixes. | `Metrics → Feedback → Update` |
| 5 | **Rollback Loop** | Safely revert a failed deployment to a stable state. | `Failure → Decision → Execute` |
| 6 | **Dependency Management Loop** | Proactively manage and update third-party dependencies. | `Scan → Analyze → Update` |
| 7 | **Code Quality Loop** | Identify and refactor code smells and technical debt. | `Analyze → Refactor → Verify` |
| 8 | **Performance Optimization Loop** | Find and eliminate performance bottlenecks. | `Profile → Optimize → Measure` |

### 2.3 Canonical Execution Chain (Happy Path)

The most common sequence follows the Happy Path Loop:

`SPEC → PLAN → TASKS → implement → STRICT VERIFY → SYNC CHECKBOXES`

Where:

- **SPEC stage** (two-step when starting from an idea):
  - Draft: `/smartspec_generate_spec_from_prompt` (creates a first-draft spec)
  - Human edit (mandatory): clarify intent, scope, constraints, and NFRs
  - Refine/normalize: `/smartspec_generate_spec` (brings the draft to SmartSpec standards)
- **PLAN**: `/smartspec_generate_plan`
- **TASKS**: `/smartspec_generate_tasks`
- **implement**: `/smartspec_implement_tasks`
- **STRICT VERIFY**: `/smartspec_verify_tasks_progress_strict`
- **SYNC CHECKBOXES**: `/smartspec_sync_tasks_checkboxes`

---

## 3) Canonical folder layout

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

.smartspec-docs/
  guides/
  reports/
  workflows/

.smartspec-assets/
  infographics/

specs/
  <category>/
    <spec-id>/
      spec.md
      plan.md
      tasks.md
      references/
      ...
```

---

## 4) Write model

### 4.1 Definitions

- **Safe outputs (allowed by default)**
  - reports: `.spec/reports/**`
  - prompts: `.spec/prompts/**`
  - generated helper scripts: `.smartspec/generated-scripts/**`

- **Governed artifacts (require explicit apply)**
  - anything under `specs/**`
  - `.spec/SPEC_INDEX.json`
  - `.spec/WORKFLOWS_INDEX.yaml`
  - any runtime source tree changes (see §4.5)

### 4.2 Rules

- Workflows may always read the project.
- Workflows may write **safe outputs** without `--apply`.
- Workflows MUST require `--apply` to modify governed artifacts.
- Any workflow that can modify governed artifacts MUST output a **Change Plan** first.

### 4.3 Allowed write scopes

- Spec workflows: `specs/<category>/<spec-id>/**` (governed)
- Spec index updates: `.spec/SPEC_INDEX.json` (governed)
- Workflow index updates: `.spec/WORKFLOWS_INDEX.yaml` (governed)
- Reports: `.spec/reports/**` (safe)
- Prompter outputs: `.spec/prompts/**` (safe)
- Generated scripts: `.smartspec/generated-scripts/**` (safe)

### 4.4 Security hardening (mandatory)

Workflows that read or write filesystem paths MUST enforce:

- **Path normalization**: reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape**: do not read/write through symlinks that resolve outside allowed scopes.
- **Output root safety**: any user-provided `--out` MUST resolve under a configured allowlist.
- **Spec-id constraints**: `^[a-z0-9_\-]{3,64}$`.
- **No secrets**: redact tokens/keys; use placeholders.
- **Bounded scanning**: enforce config limits (max files/bytes/time).

### 4.5 No source pollution + explicit runtime-tree opt-in

Default rule: SmartSpec workflows MUST NOT modify application runtime source trees.

If a workflow *must* write to a runtime tree, it MUST require `--apply` and may require additional workflow-specific opt-in flags (check individual workflow documentation).

---

## 5) Configuration (config-first)

- **Canonical config file**: `.spec/smartspec.config.yaml`
- **CLI flags are overrides only**: Workflows must not require long flag lists for normal usage.

---

## 6) Universal flag contract (minimal)

Every workflow MUST support these flags:

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>` (e.g., `--platform kilo` for Kilo Code)
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

**Reserved names:** workflow-specific flags MUST NOT reuse a universal flag name with a different meaning. Use a namespaced flag such as `--obs-platform` or `--publish-platform`.

---

## 7) Positional-first command style

Workflows should accept the primary input as a positional argument.

Examples:

- `smartspec_generate_plan <spec.md> --apply`
- `smartspec_implement_tasks <tasks.md> --apply`
- `smartspec_verify_tasks_progress_strict <tasks.md> --out <dir> --json`

---

## 8) Privileged operations: execution + network policy

### 8.1 No-shell + allowlist + timeouts

Any workflow that executes external commands MUST:

- spawn without a shell (no `sh -c`)
- use an allowlist of binaries
- enforce timeouts
- redact captured stdout/stderr

### 8.2 Network deny-by-default + allow-network gate

Default: network access is denied.

If a workflow needs network, it MUST require an explicit gate flag (e.g., `--allow-network`).

### 8.3 Secret handling for privileged workflows

- Secrets MUST NOT be accepted as raw CLI flags.
- Prefer environment variables or secret references (e.g., `env:NAME`).

---

## 9) Change Plan requirement (governed writes)

Any workflow that can write governed artifacts MUST produce a Change Plan *before apply*.

Minimum Change Plan contents:

- list of files to be created/modified
- diff summary (or patch files)
- rationale and safety notes

---

## 10) Workflow registry (single source)

Only `.spec/WORKFLOWS_INDEX.yaml` lists **all** workflows. This Handbook defines the contracts; it does not duplicate the entire registry.

All workflow files (`.smartspec/workflows/*.md`) MUST include proper YAML frontmatter for antigravity compatibility.

---

## 11) Versioning policy

- All workflow docs under `.smartspec/workflows/*.md` MUST use **version `6.0.0` or higher**.
- The `version:` in a workflow doc is the **behavior contract version**.

---

## 12) A2UI Cross-Spec Binding

### 12.1 Overview

A2UI (Agent-to-User Interface) specifications are declarative and self-contained for implementation, but they must interact with other parts of the system. Cross-spec binding is the declarative method for defining these interactions.

### 12.2 Four Types of Cross-Spec Binding

| Binding Type | Purpose | Keywords |
|:---|:---|:---|
| **Data Binding** | Connect to backend APIs | `data_bindings`, `endpoint_ref` |
| **Action Binding** | Connect to business logic services | `logic_bindings`, `service_ref`, `function_ref` |
| **Component Reference** | Reuse UI components from other specs | `imports`, `component_ref` |
| **State Binding** | Connect to global application state | `state_bindings`, `state_ref` |

### 12.3 Data Binding Example

**API Spec** (`specs/api/booking-api.json`):
```json
{
  "spec_id": "booking-api",
  "endpoints": [
    {
      "id": "get_available_times",
      "path": "/api/bookings/available-times",
      "method": "GET"
    }
  ]
}
```

**UI Spec** (`specs/ui/booking-form.json`):
```json
{
  "metadata": {
    "api_spec": "specs/api/booking-api.json"
  },
  "components": [
    {
      "id": "booking-form",
      "data_bindings": {
        "load_times": {
          "source": "api",
          "endpoint_ref": "booking-api:get_available_times",
          "trigger": "date_field.onChange",
          "target": "time_field.options"
        }
      }
    }
  ]
}
```

### 12.4 Validation Workflow

Before implementation, run validation to verify all cross-spec references:

```bash
/smartspec_validate_cross_spec_bindings --spec specs/ui/booking-form.json
```

**Checks performed:**
- Existence of referenced spec files
- Availability of referenced resources (endpoints, functions, components)
- Version compatibility between specs
- Schema matching for parameters and outputs

### 12.5 Governance Principles

1. **Explicit Dependencies**: All dependencies between specs must be declared
2. **Spec-as-API**: Every spec is treated as a contract that others can consume
3. **Declarative Bindings**: Bindings use consistent JSON structure for code generation
4. **Type Safety**: Generated code includes type checking for cross-spec interactions

**For detailed examples and concepts, see:** `docs/a2ui/A2UI_CROSS_SPEC_BINDING_GUIDE.md`

---

## Section 13: A2UI Catalog Export

### 13.1 Overview

SmartSpec uses a **server-side, centrally-governed component catalog** for stronger governance and simpler developer experience. The `smartspec_export_catalog` workflow allows you to export this catalog to **standard A2UI v0.8 format** for interoperability with other A2UI renderers.

### 13.2 Export Workflow

**Command:**
```bash
/smartspec_export_catalog \
  --input-catalog .spec/ui-catalog.json \
  --output-file public/web-catalog.json \
  --catalog-id "https://my-app.com/web-catalog-v1" \
  --platform web
```

**What it does:**
1. Reads SmartSpec UI catalog (`.spec/ui-catalog.json`)
2. Transforms components to A2UI v0.8 format
3. Maps SmartSpec properties to A2UI properties
4. Generates catalog with specified `catalogId`
5. Outputs standard A2UI catalog JSON

### 13.3 Use Cases

**1. Multi-Platform Deployment**
- Export web catalog for browser renderer
- Export Flutter catalog for mobile renderer
- Maintain single source of truth in SmartSpec

**2. Third-Party Integration**
- Share catalog with external teams
- Enable A2UI-compatible tools to consume your components
- Preserve SmartSpec governance internally

**3. Build Pipeline Integration**
```bash
# In CI/CD pipeline
/smartspec_export_catalog \
  --input-catalog .spec/ui-catalog.json \
  --output-file dist/catalog.json \
  --catalog-id "https://cdn.example.com/catalog-v1"
```

### 13.4 SmartSpec-Flavored A2UI

SmartSpec implements **SmartSpec-Flavored A2UI**, which means:
- **Design Time**: Use SmartSpec governance (duplicate prevention, validation)
- **Build Time**: Export to standard A2UI format
- **Runtime**: Use A2UI protocol for catalog negotiation

**Benefits:**
- ✅ Stronger governance at design time
- ✅ Simpler developer experience
- ✅ Standard A2UI interoperability at runtime

**For detailed design and concepts, see:** `docs/guides/A2UI_EXPORT_UTILITY_DESIGN.md`

---

# End of Canonical Handbook



---

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



---

# Knowledge Base: Workflow Selection Guide

## 1. Introduction

SmartSpec offers a powerful suite of workflows for UI generation. This guide provides a clear decision-making framework to help you select the most appropriate workflow for your specific task, ensuring you get the right output for your needs.

## 2. The Core Question: What Are You Building?

The first and most important question to ask is: **What is the primary purpose of the UI I am trying to create?**

-   **A. A standalone, complex form?**
-   **B. A component, page, or entire UI that needs to be data-bound?**

Your answer to this question is the primary driver for your workflow choice.

## 3. The Decision Tree

Use this visual decision tree to navigate your choice. Start at the top and answer the questions to arrive at the recommended workflow.

```mermaid
graph TD
    A[Start: What are you building?] --> B{A standalone form?};
    B -->|Yes| C{Are you using the RJSF library?};
    B -->|No, a full page/component| D[/smartspec_generate_ui_spec];

    C -->|Yes| E[/smartspec_generate_rjsf_schema];
    C -->|No, I have a custom A2UI renderer| D;

    subgraph Legend
        F[Decision Point]
        G[Recommended Workflow]
    end

    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
```

### How to Read the Decision Tree

1.  **Start:** Begin by defining your goal.
2.  **Standalone Form?:** If your goal is simply to create a form (e.g., for a contact page, a settings panel), follow the "Yes" path. If you are building anything else (a dashboard, a card, a layout), follow the "No" path directly to `/smartspec_generate_ui_spec`.
3.  **Using RJSF?:** If you are building a form, the next critical question is about your rendering engine. If you are using the popular **React JSON Schema Form (RJSF)** library, the clear choice is `/smartspec_generate_rjsf_schema`. If you are using a custom A2UI renderer, you should still use `/smartspec_generate_ui_spec` and describe the form in the prompt.

## 4. Rule of Thumb: A Quick Guide

For a faster decision, use this simple rule of thumb:

| If your goal is to... | And your renderer is... | Then use... |
| :--- | :--- | :--- |
| Build a **form** | **React JSON Schema Form (RJSF)** | `/smartspec_generate_rjsf_schema` |
| Build a **form** | A **custom A2UI renderer** | `/smartspec_generate_ui_spec` |
| Build **anything else** (page, component, layout) | A **custom A2UI renderer** | `/smartspec_generate_ui_spec` |

> In short: Unless you are specifically targeting the RJSF library, your default choice should always be **`/smartspec_generate_ui_spec`**.

## 5. Summary of Outputs

Remember that each workflow produces a different output for a different renderer.

-   **`/smartspec_generate_rjsf_schema`**
    -   **Output:** `schema.json` + `uiSchema.json`
    -   **For:** RJSF Renderer

-   **`/smartspec_generate_ui_spec`**
    -   **Output:** `ui-spec.json`
    -   **For:** A2UI Renderer

Choosing the correct workflow from the start will prevent compatibility issues and ensure a smooth development process. When in doubt, refer to this guide and the [UI JSON Formats Comparison](ui-json-formats-comparison.md) guide.


---

**Version:** 2.0.0  
**Last Updated:** 2025-12-26  
**Consolidated From:**
- knowledge_base_smartspec_handbook.md
- knowledge_base_smartspec_install_and_usage.md
- workflow-selection-guide.md
