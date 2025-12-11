# SmartSpec Knowledge Base V2 (English)
## Installation, Usage, Governance, and Workflow Definitions
### Fully Rewritten Version Supporting New Strict Verification System
---

# 1. Overview
SmartSpec is a structured software architecture and development workflow system used across:
- **Kilo Code**
- **Claude Code**
- **Google Antigravity**

SmartSpec provides:
- A complete lifecycle: **SPEC → PLAN → TASKS → IMPLEMENT**
- Workflow automation
- Governance and safety policies
- Registries and cross-project indexing
- UI schema and design rules

This Knowledge Base V2 is a **full rewrite**, preserving **all existing functionality**, while adding support for:
- `/smartspec_verify_tasks_progress_strict` (new canonical verifier)
- `/smartspec_sync_tasks_checkboxes` (new evidence-driven task sync)

The legacy `/smartspec_verify_tasks_progress` is now deprecated.

---

# 2. Architecture Summary
SmartSpec enforces a predictable chain of development artifacts:

```
SPEC → PLAN → TASKS → IMPLEMENT → DELIVERY
```
Each stage is generated, validated, and governed via SmartSpec workflows.

---
# 3. Installation
SmartSpec installs differently depending on platform.

## 3.1 Kilo Code
Run installation workflow:
```
/smartspec_install --kilocode
```
This installs:
- command wrappers
- IDE hooks
- task verification tools

## 3.2 Claude Code
```
/smartspec_install
```

## 3.3 Google Antigravity
```
/smartspec_install --workspace-roots=<paths>
```
Multi-repo mode supported.

---
# 4. Directory Conventions
```
project/
  specs/
    feature/<spec-id>/spec.md
    feature/<spec-id>/tasks.md
  .smartspec/
    workflows/
    registries/
    reports/
  src/
  tests/
  docs/
```

---
# 5. Governance Rules
## 5.1 Write Guards
Each workflow declares write permissions:
- `NO-WRITE` — read-only
- `TASKS-ONLY` — allowed to modify tasks.md only
- `REGISTRY-ONLY`, etc.

## 5.2 Registries
Registries store cross-project metadata.
- API registry
- Data model registry
- Critical sections registry

Workflows must respect:
- `--registry-roots`
- `--registry-dir`

## 5.3 SPEC_INDEX
Maintains dependency structure of specs.
Used by generate/verify workflows.

## 5.4 UI / Design Rules
SmartSpec UI governance requires:
- JSON-first UI definitions
- Approved App Components only
- No raw CSS unless allowed


---
# 6. Standard Workflows
All original workflows remain valid.

## 6.1 /smartspec_generate_spec
Creates initial `spec.md` based on project request.

## 6.2 /smartspec_generate_plan
Transforms spec → engineering plan.

## 6.3 /smartspec_generate_tasks
Creates `tasks.md` from plan.

## 6.4 /smartspec_generate_implement
Creates scaffolding code from tasks.

## 6.5 /smartspec_lint, /smartspec_format
Linting & formatting.

## 6.6 /smartspec_project_copilot
Guides next actions in project lifecycle.

## 6.7 /smartspec_ui_*
UI creation & validation workflows.

All of these work unchanged.

---
# 7. **Deprecated Workflow (DO NOT USE)**
### `/smartspec_verify_tasks_progress`
```
STATUS: DEPRECATED — NOT RECOMMENDED FOR USE
```
### Reason for Deprecation
The legacy workflow:
- Relied on checkbox-first logic
- Could not reliably detect missing implementation
- Failed when tasks were improperly mapped
- Caused verification loops where tasks never resolved properly

### Replacement Workflow
Use **`/smartspec_verify_tasks_progress_strict`** instead.

---
# 8. New Strict Workflow (Replaces Legacy Verify)
# `/smartspec_verify_tasks_progress_strict`
### Purpose
A strict, evidence-first verification workflow ensuring tasks are only considered complete when:
- Implementation exists
- Tests exist
- Documentation exists (when required)
- Deployment artifacts exist (when required)

### Key Features
- Built-in evidence scanners (no external script needed)
- JSON + Markdown report generation
- Strict verdicts: `complete`, `partial`, `incomplete`, `false_positive`, `unsynced_complete`
- Anti-loop diagnostics
- Optional per-spec evidence config

### Example Usage
```
/smartspec_verify_tasks_progress_strict \
  --spec specs/feature/spec-002/spec.md \
  --report-format=both \
  --report=detailed
```

### JSON Report Example
```
/spec/reports/verify-tasks-progress/spec-002.json
```
Contains:
- task verdicts
- missing evidence
- matched evidence
- progress metrics

---
# 9. New Workflow
# `/smartspec_sync_tasks_checkboxes`
### Purpose
Synchronize checkboxes in `tasks.md` based on verified evidence from strict workflow.

### Rules
- Only modifies `tasks.md`
- Uses JSON report from strict verify
- Safe & Auto modes available

### Example
```
/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/spec-002/tasks.md \
  --report .spec/reports/verify-tasks-progress/spec-002.json \
  --mode=auto
```

---
# 10. Recommended Flow
```
# 1. Verify real implementation
/smartspec_verify_tasks_progress_strict --spec <path> --report-format=json

# 2. Sync checkboxes based on evidence
/smartspec_sync_tasks_checkboxes --tasks <path> --report <json>
```

---
# 11. CI/CD Integration Example
```
- name: SmartSpec Strict Verification
  run: |
    /smartspec_verify_tasks_progress_strict --spec $SPEC --report-format=json > strict.json
    /smartspec_sync_tasks_checkboxes --tasks $TASKS --report strict.json --mode=auto
```

---
# 12. Multi-Repo Use
SmartSpec supports multi-workspace verification via:
```
--workspace-roots=<paths>
--repos-config=<file>
```

This applies equally to strict verification and sync workflows.

---
# 13. Error Handling & Diagnostics
The strict verifier reports:
- Missing evidence per task
- Wrong file locations
- Mapping problems
- Tasks stuck in repeated incomplete state

Sync workflow handles:
- Missing JSON report
- Unknown task IDs
- Dry-run safety mode

---
# 14. Summary
SmartSpec Knowledge Base V2 introduces:
- A fully reliable strict verification system
- Evidence-driven task syncing
- Cleaner governance and workflow design
- Official deprecation of flawed legacy verify system

All original functionality remains intact, but strict verification is now the standard method for progress validation.

---
End of Knowledge Base V2