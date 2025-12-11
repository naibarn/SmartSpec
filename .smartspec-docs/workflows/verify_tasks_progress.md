# SmartSpec Workflow Manual
## `/smartspec_verify_tasks_progress` — Evidence-First Verification Workflow
**English Version (Standalone Manual)**

---
# 1. Purpose
`/smartspec_verify_tasks_progress` is the **official verification workflow** in the SmartSpec system for determining the *true* implementation status of a spec’s tasks.

This workflow performs **evidence-first analysis**, meaning:
- Checkboxes in `tasks.md` are treated only as *hints*.
- **Actual code, tests, documentation, and deployment artifacts** determine progress.
- A task is never considered complete unless real evidence exists.
- The workflow is **read-only**: it never modifies spec, tasks, code, or registries.

This manual explains how to use the workflow effectively in real projects.

---
# 2. What This Workflow Does
### ✔ Reads and analyzes:
- `spec.md`
- `tasks.md`
- Source code (services, routes, helpers)
- Tests (unit, integration, performance)
- Documentation
- Deployment files (K8s, CI/CD, monitoring)
- Optional custom evidence from user-supplied scripts

### ✔ Produces:
- A **Markdown report** (human-readable)
- A **JSON report** (for automation workflows like checkbox syncing)

### ✔ Computes a verdict for every task:
| Verdict | Meaning |
|--------|---------|
| **complete** | Evidence fully matches expectations |
| **unsynced_complete** | Evidence complete but task was unchecked |
| **false_positive** | Task checked but no evidence found |
| **partial** | Some evidence exists but is incomplete |
| **incomplete** | No evidence exists |

The workflow enforces **strict governance** and ensures progress cannot be overstated.

---
# 3. Flags & Options
## 3.1 Evidence-First Controls
```bash
--evidence-only
```
Ignore checkboxes completely — use evidence only.

```bash
--run-tests
```
Execute or query tests; failing tests downgrade verdicts.

```bash
--evidence-script=<path>
```
Run a custom script (Python/JS) that returns additional evidence.

---
## 3.2 Input Selection
```bash
--spec=<path>
--tasks=<path>
--spec-id=<id>
```
If `--tasks` is omitted, SmartSpec auto-detects it from the spec.

---
## 3.3 Legacy Flags (Fully Preserved)
### SPEC_INDEX / Registry
```bash
--index=<path>
--specindex=<path>
--registry-dir=<path>
--registry-roots=<csv>
```
### Multi-Repo
```bash
--workspace-roots=<csv>
--repos-config=<path>
```
### Reporting
```bash
--report-dir=<path>
--report=<summary|detailed>
--report-format=<md|json>
--dry-run
```
### Safety
```bash
--safety-mode=<strict|dev>
--strict
```
All original workflow capabilities remain fully supported.

---
# 4. JSON Output Format
Used by automation workflows such as `/smartspec_sync_tasks_checkboxes`.

Example:
```json
{
  "spec_id": "spec-002-user-management",
  "tasks_path": "specs/feature/spec-002-user-management/tasks.md",
  "summary": {
    "total_tasks": 78,
    "complete": 40,
    "unsynced_complete": 5,
    "false_positive": 6,
    "partial": 15,
    "incomplete": 12,
    "progress_percent": 57.7,
    "risk_level": "MEDIUM"
  },
  "tasks": [
    {
      "id": "T047",
      "declared_status": "checked",
      "observed_evidence": "none",
      "verdict": "false_positive",
      "evidence": {
        "routes": [],
        "tests": [],
        "services": []
      }
    }
  ]
}
```

---
# 5. How the Workflow Evaluates Tasks
### Step 1: Parse `tasks.md`
Extract IDs, titles, nesting, and checkbox states.

### Step 2: Collect Evidence
- Scan for matching code
- Scan tests
- Run optional evidence script
- Run tests (if enabled)

### Step 3: Compute Verdicts
Rules:
- If evidence = complete → `complete` or `unsynced_complete`
- If evidence = none + checkbox checked → `false_positive`
- If evidence = none + checkbox unchecked → `incomplete`
- If evidence = partial → `partial`

### Step 4: Generate Reports
Markdown and/or JSON depending on flags.

---
# 6. Example Commands
## 6.1 Basic Verification
```bash
/smartspec_verify_tasks_progress \
  --spec specs/feature/spec-002-user-management/spec.md
```

## 6.2 Generate Markdown + JSON Reports
```bash
/smartspec_verify_tasks_progress \
  --spec specs/feature/spec-002-user-management/spec.md \
  --report-format=json --report=summary
```

## 6.3 Use a Custom Evidence Script
```bash
/smartspec_verify_tasks_progress \
  --spec specs/feature/spec-002-user-management/spec.md \
  --evidence-script=scripts/check_tasks_evidence.py
```

## 6.4 Run Tests as Part of Evidence
```bash
/smartspec_verify_tasks_progress \
  --spec specs/feature/spec-002-user-management/spec.md \
  --run-tests --report-format=json
```

---
# 7. Governance Rules
- **Read-only** workflow
- Must not modify:
  - `spec.md`
  - `tasks.md`
  - code files
  - registries
  - SPEC_INDEX
  - UI JSON
- Must preserve all capabilities from v5.7 while extending functionality in v5.8.

This workflow is designed to be **safe**, **accurate**, and **compatible** with all SmartSpec governance rules.

---
# 8. Best-Practice Workflow for Teams
1. Implement code normally
2. Run:
   ```bash
   /smartspec_verify_tasks_progress --report-format=json
   ```
3. Review the JSON report
4. (Optional) Sync checkboxes using a separate workflow
5. Use the verified results for planning and sprint reviews

---
# 9. When to Use This Workflow
Use it whenever you need:
- Evidence-based progress reports
- Reliable progress numbers for management
- Automatic detection of missing code/tests
- Governance-friendly verification
- CI/CD accuracy

---
# 10. Need the Thai Manual Too?
Just say **“สร้างคู่มือภาษาไทยด้วย”** and I will create a second canvas containing the Thai version.

End of manual. 🚀