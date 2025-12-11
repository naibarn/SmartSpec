# SmartSpec Knowledge Base V2 (Governance, Architecture, and Workflow System)
## Fully Rewritten Edition — Preserving All Legacy Rules + Supporting New Strict Verification Framework
---

# 1. Purpose of This Knowledge Base
This Knowledge Base (KB V2) defines the **governance, architectural rules, workflow semantics, write-guards, safety model, registries, and UI governance** for the SmartSpec system used across:
- **Kilo Code**
- **Claude Code**
- **Google Antigravity**

This version:
- **Retains all legacy governance from KB V1 (no deletions)**
- **Adds next-generation strict verification model**
- **Adds new workflow: `/smartspec_sync_tasks_checkboxes`**
- **Formally deprecates the old `/smartspec_verify_tasks_progress`**

It acts as a foundational reference for all SmartSpec tools.

---
# 2. SmartSpec Architecture Overview
SmartSpec enforces a structured, deterministic development lifecycle:

```
SPEC → PLAN → TASKS → IMPLEMENT → VERIFY (strict) → SYNC → DELIVERY
```

Where:
- **SPEC** — requirements, constraints, boundaries
- **PLAN** — engineering design, decomposition
- **TASKS** — actionable implementation units
- **IMPLEMENT** — code generation and development
- **VERIFY (strict)** — *evidence-first, audit-grade verification*
- **SYNC** — checkbox synchronization for planning accuracy
- **DELIVERY** — deployment, integration, publication

All workflows must operate within SmartSpec governance.

---
# 3. Governance Model
## 3.1 Write Guards
Each workflow declares a `write_guard`:
- **NO-WRITE:** may not modify any project file
- **TASKS-ONLY:** may modify only `tasks.md`
- **REGISTRY-ONLY:** may update registry directories
- **UI-ONLY:** may update UI schema JSON files

Governance prohibits workflows from writing outside their allowed domain.

---
## 3.2 SPEC Index
`SPEC_INDEX` defines:
- dependencies
- spec composition
- component ownership
- critical paths

All workflows referencing specs MUST check the SPEC_INDEX for:
- spec discovery
- dependency resolution
- scope validation

---
## 3.3 Registries
Registries hold cross-SPEC metadata.
- **API Registry**
- **Data Model Registry**
- **Critical Sections Registry**

Workflows must honor:
- `--registry-roots`
- `--registry-dir`

Registries are append-only unless a workflow specifically states overwrite permission.

---
## 3.4 Multi-Repo Governance
SmartSpec supports:
```
--workspace-roots
--repos-config
```
Rules:
- Workflows must resolve paths across monorepos and multi-service architectures.
- Verification workflows must treat each repo root as isolated unless explicitly connected.

---
# 4. UI Governance
SmartSpec enforces a consistent UI system:
- JSON-first UI schema
- Approved design tokens
- App Components only
- No custom CSS unless explicitly allowed
- UI workflows may not write outside UI directories

---
# 5. Standard Workflows (All Legacy Functions Preserved)
All legacy SmartSpec workflows remain valid and unchanged.

### 5.1 `/smartspec_generate_spec`
Generates new structured SPEC.

### 5.2 `/smartspec_generate_plan`
Derives engineering PLAN.

### 5.3 `/smartspec_generate_tasks`
Creates complete `tasks.md` from PLAN.

### 5.4 `/smartspec_generate_implement`
Provides implementation scaffolding.

### 5.5 `/smartspec_format`, `/smartspec_lint`
Formatting and linting utilities.

### 5.6 `/smartspec_project_copilot`
Guides next-step decisions.

### 5.7 `/smartspec_ui_*`
UI scaffolding + validation.

**All above workflows remain functional and unchanged in V2.**

---
# 6. DEPRECATED Workflow (MANDATORY NOTICE)
## `/smartspec_verify_tasks_progress` — **DEPRECATED (DO NOT USE)**
### Status
```
Deprecated — superseded by strict verifier
```

### Reasons
- Relied on checkbox-first logic
- Allowed false positives and incorrect progress reports
- Failed for EPIC-scale specs and evidence validation
- Created verification loops where tasks never resolved

### Replacement
Use:
```
/smartspec_verify_tasks_progress_strict
```

All workflows, documentation, CI systems, and governance must migrate to the strict version.

---
# 7. New Verification Workflow (Canonical)
# `/smartspec_verify_tasks_progress_strict`
## Purpose
To validate SPEC/TASKS/IMPLEMENT progress using **evidence-first logic**, independent of checkbox state.

## 7.1 Key Rules
- Tasks are **complete only when evidence exists**:
  - implementation code
  - test files (unit, integration, performance)
  - documentation (if applicable)
  - deployment/CI files (if applicable)
- Checkbox state is ignored for progress calculations
- Missing evidence yields `incomplete`, even if checkbox is checked
- Evidence > checkbox
- Supports optional `evidence-config` for highly specialized specs

## 7.2 Built-in Evidence Providers
Strict verifier includes internal scanners:
- Route detector
- Service detector
- Test detector
- Documentation detector
- Deployment detector

Works without any external script.

## 7.3 Verdicts
```
complete
unsynced_complete
false_positive
partial
incomplete
```
Strict mode penalizes:
- missing tests
- missing endpoints
- wrong folder structure
- unverified implementations

## 7.4 Anti-Loop Diagnostics
If a task is incomplete across multiple runs, strict verifier will report:
```
Task <id> repeatedly has no evidence; mapping or implementation may be incorrect.
```

## 7.5 Usage Example
```
/smartspec_verify_tasks_progress_strict \
  --spec specs/feature/spec-002/spec.md \
  --report-format=both \
  --report=detailed
```

---
# 8. New Sync Workflow
# `/smartspec_sync_tasks_checkboxes`
## Purpose
To sync checkbox states in `tasks.md` based on strict evidence report.

## 8.1 Rules
- Write-guard: `TASKS-ONLY`
- Updates checkboxes only
- Does not modify:
  - spec.md
  - code
  - tests
  - registries
- Driven solely by strict verifier JSON report

## 8.2 Usage Example
```
/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/spec-002/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002.json \
  --mode=auto
```

---
# 9. Official Workflow Chain (Updated for V2)
```
1) smartspec_generate_spec
2) smartspec_generate_plan
3) smartspec_generate_tasks
4) smartspec_generate_implement
5) smartspec_verify_tasks_progress_strict     (mandatory)
6) smartspec_sync_tasks_checkboxes            (optional but recommended)
```

This replaces the old chain where verification was non-strict.

---
# 10. Multi-Repo and CI Governance
Strict verification MUST run with:
```
--workspace-roots
--repos-config
```
When part of multi-service environments.

Example CI:
```
/smartspec_verify_tasks_progress_strict --spec $SPEC --report-format=json > strict.json
/smartspec_sync_tasks_checkboxes --tasks $TASKS --report strict.json --mode=auto
```

---
# 11. Evidence-First Governance (New Core Rule)
SmartSpec V2 introduces a new foundation:

### Checkbox = Signal ONLY
### Evidence = Source of Truth

Tasks MUST NOT be marked complete unless:
- implementation exists
- tests exist
- docs (if required) exist
- deployment files (if required) exist

Governance mandates:
```
Evidence > Checkbox
Strict verifier > legacy verifier
```

---
# 12. Summary of Changes Introduced in KB V2
| Feature | Status |
|--------|--------|
| Legacy Verify | ❌ Deprecated |
| Strict Verify | ✅ Canonical |
| Sync Tasks | ✅ Added |
| Evidence Model | ✅ Mandatory |
| Governance | ⚡ Enhanced |
| Backward Compatibility | 👍 Preserved for all non-verify workflows |

---
# End of SmartSpec Knowledge Base V2