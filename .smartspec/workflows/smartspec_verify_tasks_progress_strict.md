---
name: /smartspec_verify_tasks_progress_strict
version: 1.0.0
role: verification/governance
write_guard: NO-WRITE
purpose: Provide a **strict, evidence-first** verification workflow that can independently determine implementation progress for a spec, without relying on external scripts, while leaving existing `/smartspec_verify_tasks_progress` behavior intact.
version_notes:
  - v1.0.0: initial strict workflow; replaces legacy verify behavior for teams that opt in.
---

# /smartspec_verify_tasks_progress_strict (v1.0.0)

This workflow is a **new, stricter verification command** that is designed to:

- Determine implementation progress **purely from evidence** (code, tests, docs, deployment artifacts).
- Work **out-of-the-box** for all specs using **built-in evidence providers**.
- Avoid reliance on external scripts.
- Provide **clear reasons** when tasks are incomplete or mismatched.
- Avoid infinite verification/implementation loops by surfacing configuration/mapping problems explicitly.

This workflow does **not** modify spec, tasks, code, or registries. It emits reports only.

> Scope
>
> - Read-only: `spec.md`, `tasks.md`, source code, tests, docs, deployment files, SPEC_INDEX, registries.
> - Write: reports under `.spec/reports/verify-tasks-progress/` (markdown and/or JSON).
> - This workflow is intended as a **drop-in strict replacement** for the legacy verify command for teams that opt in.

---

## 1. High-Level Behavior

1. Resolve the target spec and tasks file.
2. Parse `tasks.md` into a structured tree (tasks + subtasks) with IDs and checkbox states.
3. For each task:
   - Infer what kind of evidence is expected (endpoint, service method, tests, docs, deployment) using:
     - task ID (e.g., `T047`),
     - keywords in the title/description (e.g., "endpoint", "unit tests", "OpenAPI"),
     - optional per-spec evidence config (YAML/JSON).
   - Use built-in evidence providers to search the codebase.
   - Classify evidence level and produce a **verdict**.
4. Aggregate per-task verdicts into totals, percentages, and risk scores.
5. Output a **strict report** with progress metrics and concrete missing-evidence reasons.

No external evidence script is required. All logic is contained here, with an **optional per-spec config file** to refine behavior.

---

## 2. Inputs & Flags

### 2.1 Required / Core Inputs

```bash
--spec=<path>         # spec file path
--tasks=<path>        # tasks file path (optional; auto-resolved from spec when omitted)
```

If `--tasks` is omitted, the workflow attempts to locate `tasks.md` next to the spec.

### 2.2 Optional Evidence Config

```bash
--evidence-config=<path>
```

- Optional per-spec config file, e.g.:
  - `specs/feature/spec-002-user-management/evidence.yaml`
- Used to:
  - map task IDs → expected endpoints, services, tests, docs, deployment files.
  - customize rules for specific specs.

If no config is provided, the workflow uses built-in heuristics only.

### 2.3 Reporting

```bash
--report-dir=<path>          # default: .spec/reports/verify-tasks-progress/
--report=<summary|detailed>  # level of markdown detail (default: summary)
--report-format=<md|json|both>  # default: md
--dry-run                    # print report to stdout only; no files written
```

### 2.4 Safety / Strictness

```bash
--safety-mode=<strict|dev>   # default: strict
--strict                     # alias for --safety-mode=strict
```

- `strict` mode:
  - Any missing or ambiguous evidence leads to `incomplete` or `partial` verdicts.
  - Failing tests downgrade verdicts.
- `dev` mode:
  - More forgiving; missing config is logged as warnings, but the workflow still attempts best-effort evaluation.

---

## 3. Evidence Model

For each task (and optionally subtask), the workflow computes:

- `declared_status`:
  - `checked | unchecked | missing` (from `tasks.md`).
- `observed_evidence`:
  - `none | partial | complete` based on built-in evidence checks.
- `verdict`:
  - `complete` → strong evidence found for all required artifacts.
  - `unsynced_complete` → strong evidence found, but task was unchecked.
  - `false_positive` → no evidence, but task was checked.
  - `partial` → some evidence present, but missing key elements.
  - `incomplete` → no evidence found.

### 3.1 Progress Calculation

```text
progress = (complete + unsynced_complete) / total_tasks
```

Checkboxes do **not** determine progress; they are only reported for comparison.

---

## 4. Built-in Evidence Providers

This workflow includes **generic providers** that work without external scripts:

### 4.1 Route Evidence

- Scans typical route locations, e.g.:
  - `src/routes/**/*.ts`
  - `src/http/**/*.ts`
- Extracts HTTP methods & paths using framework-agnostic heuristics (e.g., regex-based scan for method + path strings).
- Tasks mentioning keywords like `endpoint`, `GET /`, `POST /`, or containing explicit paths will be matched to discovered routes.

### 4.2 Service Evidence

- Scans service-like directories:
  - `src/services/**/*.ts`
  - `src/modules/**/services/**/*.ts`
- Uses class/function names and keywords from task titles/descriptions to infer required service methods.

### 4.3 Test Evidence

- Scans for tests in:
  - `tests/unit/**/*`
  - `tests/integration/**/*`
  - `tests/performance/**/*`
  - `__tests__/**/*` (where applicable)
- Connects tasks mentioning `unit test`, `integration test`, `performance`, etc. to matching test files.

### 4.4 Documentation Evidence

- Scans `docs/**/*` for:
  - API docs (keywords: `OpenAPI`, `Swagger`, `API`, etc.).
  - Deployment docs (keywords: `deploy`, `production`, `Kubernetes`).

### 4.5 Deployment Evidence

- Scans:
  - `k8s/**/*`, `deploy/**/*`, `.github/workflows/**/*`, etc.
- Connects tasks mentioning `Kubernetes`, `monitoring`, `CI/CD`, etc. to relevant files.

If a spec provides an `--evidence-config`, these defaults are refined or extended using the config.

---

## 5. Per-Spec Evidence Config (Optional)

An evidence config file allows more precise, spec-specific rules **without changing this workflow**.

Example `evidence.yaml`:

```yaml
tasks:
  T047:
    endpoints:
      - method: POST
        path: /api/v1/users/me/phone
    tests:
      - tests/integration/users.phone.test.ts
  T072:
    performance_tests:
      - tests/performance/permission-cache.test.ts
```

The workflow will:

- Look for the specified routes/tests.
- Mark tasks `partial` or `incomplete` if required artifacts are missing.

If the config is missing or incomplete, the workflow falls back to heuristics.

---

## 6. Evaluation Flow

1. **Resolve spec & tasks** using `--spec` and `--tasks`.
2. **Load evidence config** when `--evidence-config` is provided.
3. **Parse tasks** from `tasks.md` into a structured model.
4. For each task:
   - Determine expected evidence kinds (endpoint/service/tests/docs/deploy), using:
     - evidence config (if present),
     - fallback heuristics (based on task title/description/ID).
   - Run built-in providers to collect evidence.
   - Compute `observed_evidence` and `verdict`.
5. Compute overall progress and risk level.
6. Emit markdown and/or JSON report.

---

## 7. JSON Report Format

The JSON report provides machine-readable results for every task.

Example structure:

```jsonc
{
  "spec_path": "specs/feature/spec-002-user-management/spec.md",
  "tasks_path": "specs/feature/spec-002-user-management/tasks.md",
  "summary": {
    "total_tasks": 78,
    "complete": 45,
    "unsynced_complete": 3,
    "false_positive": 4,
    "partial": 16,
    "incomplete": 10,
    "progress_percent": 61.5,
    "risk_level": "HIGH"
  },
  "tasks": [
    {
      "id": "T047",
      "title": "Implement phone verification endpoints",
      "declared_status": "checked",
      "observed_evidence": "none",
      "verdict": "false_positive",
      "missing": [
        "endpoint POST /api/v1/users/me/phone",
        "test tests/integration/users.phone.test.ts"
      ],
      "found": []
    }
  ]
}
```

This report is suitable for:

- CI dashboards
- internal tooling
- follow-up workflows (e.g., syncing checkboxes in tasks.md)

---

## 8. Anti-Loop & Failure Diagnostics

To avoid endless verify/implement loops:

- The workflow will track tasks that repeatedly have `false_positive` or `incomplete` verdicts across runs.
- When a task has no evidence after multiple runs, the report will include a diagnostic note, e.g.:

```text
WARNING: Task T047 has no detectable evidence after multiple verification cycles.
This likely indicates incorrect mapping, missing evidence config, or implementation in non-standard locations.
```

This helps teams fix the underlying cause instead of blindly re-running implementation.

---

## 9. Governance

- This workflow is **strictly read-only**.
- It is intended as a **new, stricter alternative** to the legacy `/smartspec_verify_tasks_progress`.
- Teams may:
  - continue using the legacy workflow, or
  - adopt `/smartspec_verify_tasks_progress_strict` as the canonical verifier.

No backward-compatibility guarantees are provided for this strict workflow; it is allowed to diverge in behavior to maximize correctness and safety.

