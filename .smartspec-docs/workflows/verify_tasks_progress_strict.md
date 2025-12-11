# SmartSpec Strict Verification Workflow Manual
## `/smartspec_verify_tasks_progress_strict` — Evidence-First, Strict Enforcement Verification
**English Version** — Dedicated Manual for the Strict Workflow

---
# 1. Purpose
`/smartspec_verify_tasks_progress_strict` is a **next-generation, strict, evidence-first verification workflow** designed to replace the legacy verification system where necessary.

This workflow enforces:
- **Zero trust in checkboxes** inside `tasks.md`
- **100% evidence-required validation** (code + tests + docs + deploy artifacts)
- **Spec-agnostic but accurate heuristics** using built-in evidence providers
- **Optional per-spec evidence configs** for high precision
- **Strict scoring, clear failure reasons, and anti-loop diagnostics**

This workflow is **read-only** and writes only verification reports.

Use this workflow when accuracy, reliability, and audit-grade progress reports are required.

---
# 2. Key Features
### ✔ 2.1 Evidence-First Verification
Progress is calculated strictly from observed evidence:
- Implementation files
- Test files (unit / integration / performance)
- API route definitions
- Documentation (API / deployment)
- Deployment & CI/CD files

Checkboxes do not determine completion — they only appear in the report.

---
### ✔ 2.2 Strict Verdict System
Each task receives one of the following verdicts:

| Verdict | Meaning |
|--------|---------|
| **complete** | All required evidence exists and is consistent |
| **unsynced_complete** | Evidence exists but checkbox was unchecked |
| **false_positive** | Checkbox checked but no evidence exists |
| **partial** | Some evidence exists but incomplete |
| **incomplete** | No evidence found |

Strict mode ensures no task can be accidentally marked complete.

---
### ✔ 2.3 Built-In Evidence Providers (No Script Required)
Includes automatic detection of:
- HTTP routes
- Service methods
- Test files & categories
- Docs (API, deployment, architecture)
- Deployment files (K8s, CI/CD)

Works out-of-the-box with zero configuration.

---
### ✔ 2.4 Optional Evidence Config
A spec may include a config file to fine-tune expected evidence:

Example: `specs/.../evidence.yaml`
```yaml
tasks:
  T047:
    endpoints:
      - path: /api/v1/users/me/phone
        method: POST
    tests:
      - tests/integration/users.phone.test.ts
```
Supports:
- endpoint mapping
- service method mapping
- required tests
- required docs
- required deployment artifacts

---
### ✔ 2.5 Anti-Loop Diagnostics
If a task consistently shows no evidence across runs, the report includes warnings:
```
WARNING: T047 has no detectable evidence after repeated verification cycles.
This indicates mapping issues or missing implementation in non-standard locations.
```
Prevents infinite loops of verify → implement → verify.

---
# 3. Inputs & Flags
## 3.1 Required Inputs
```
--spec=<path>
--tasks=<path>       # Optional; auto-detected if omitted
```

## 3.2 Optional Inputs
### Evidence config
```
--evidence-config=<path>
```

### Reporting
```
--report-dir=<path>
--report=<summary|detailed>
--report-format=<md|json|both>
--dry-run
```

### Strictness
```
--safety-mode=<strict|dev>
--strict    # alias for strict mode
```

---
# 4. Evidence Providers (Built-in)
The strict workflow includes analyzer modules that search for evidence:

### 4.1 Route Detector
Searches common directories:
- `src/routes/**/*`
- `src/http/**/*`

Recognizes HTTP method + path via heuristics.

### 4.2 Service Detector
Searches:
- `src/services/**/*`
- `src/modules/**/services/**/*`

Extracts class/function names and matches keywords.

### 4.3 Test Detector
Searches:
- `tests/unit/**/*`
- `tests/integration/**/*`
- `tests/performance/**/*`
- `__tests__/**/*`

Categorizes tests by task-relevant keywords.

### 4.4 Documentation Detector
Searches `docs/**/*` for:
- API docs (OpenAPI, Swagger)
- Deployment docs

### 4.5 Deployment Detector
Searches:
- `k8s/**/*`
- `deploy/**/*`
- `.github/workflows/**/*`

Matches tasks requiring deployment, monitoring, or CI/CD artifacts.

---
# 5. Evaluation Flow
### Step 1 — Resolve Spec & Tasks
Identify the appropriate files.

### Step 2 — Load Optional Evidence Config
If present, it overrides or extends heuristics.

### Step 3 — Parse Tasks
Convert `tasks.md` into structured nodes.

### Step 4 — Collect Evidence per Task
Search for endpoints, service methods, tests, docs, deploy files.

### Step 5 — Compute Verdicts
Apply strict evidence rules:

- Missing test → **partial**
- Missing implementation → **incomplete**
- Checked but no code → **false_positive**
- Evidence found but unchecked → **unsynced_complete**

### Step 6 — Generate Reports
Output markdown, JSON, or both.

---
# 6. JSON Report Format
Example:
```json
{
  "spec_path": "specs/.../spec.md",
  "tasks_path": "specs/.../tasks.md",
  "summary": {
    "total": 78,
    "complete": 45,
    "unsynced_complete": 3,
    "false_positive": 4,
    "partial": 16,
    "incomplete": 10,
    "progress_percent": 61.5,
    "risk": "HIGH"
  }
}
```

Each task entry contains:
- expected evidence
- missing evidence
- matched evidence
- verdict

---
# 7. Example Usage
## Minimal
```bash
/smartspec_verify_tasks_progress_strict \
  --spec specs/.../spec.md
```

## With JSON Output
```bash
/smartspec_verify_tasks_progress_strict \
  --spec specs/.../spec.md \
  --report-format=json
```

## With Evidence Config
```bash
/smartspec_verify_tasks_progress_strict \
  --spec specs/.../spec.md \
  --evidence-config specs/.../evidence.yaml
```

## Detailed Report
```bash
/smartspec_verify_tasks_progress_strict \
  --spec specs/.../spec.md \
  --report=detailed --report-format=both
```

---
# 8. Governance
The workflow:
- **Must not modify**: spec.md, tasks.md, code, registries, SPEC_INDEX, UI JSON
- Writes only: markdown/JSON reports
- Is intentionally **not backward-compatible** with the legacy verify workflow
- Provides maximum safety and correctness

---
# 9. When to Use This Workflow
Use when you need:
- Reliable progress reports grounded in code, not checkboxes
- CI/CD verification for readiness
- Governance/audit-grade reporting
- Automatic detection of incomplete tasks
- No chance of false completion

---
# 10. Thai Version
A Thai-language manual can be created in a separate Canvas.
Say: **“สร้างคู่มือภาษาไทย”**

---
End of Manual 🚀