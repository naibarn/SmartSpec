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
