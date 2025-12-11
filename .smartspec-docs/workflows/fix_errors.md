# SmartSpec v5.7.1 — /smartspec_fix_errors.md Manual

This is the **official user manual** for the workflow:
```
/smartspec_fix_errors.md
```
With full support for KiloCode Orchestrator, multi-repo governance, SPEC_INDEX resolution, registries, and the new v5.7.1 capability:

```
--report=<path>
```
plus auto-discovery of implementation reports.

This manual is rewritten *entirely* to match the new workflow specification.

---

# 1. Purpose
`/smartspec_fix_errors.md` is used to:
- Diagnose **build errors**, **compiler/type errors**, **test failures**, **integration failures**, **contract mismatches**, and **UI inconsistencies**.
- Use **SPEC_INDEX**, **registries**, and **tasks.md** to determine which SPEC is responsible.
- Generate a **Fix Report** with root-cause analysis + safe fix recommendations.
- Support **KiloCode Orchestrator**, allowing the assistant to read structured error information and implementation reports.
- Optionally apply **additive metadata fixes** (if host implementation supports it).

This workflow **DOES NOT** directly modify implementation code. It recommends fixes or updates metadata only.

---

# 2. When to Use
Use `/smartspec_fix_errors.md` when:
- You just ran `/smartspec_implement_tasks.md` and encountered test failures.
- KiloCode stopped due to compiler or runtime errors.
- CI shows failing tests, type errors, or contract mismatches.
- A SPEC’s implementation is partially complete and needs repair.
- You want the system to read an **implementation report** instead of re-running tests.

Do **NOT** use it when designing a new feature (use `/smartspec_generate_spec`).

---

# 3. Quick Start Examples

## 3.1 Standard fix run under Kilo
```
/smartspec_fix_errors.md --kilocode
```
The system will:
- Ingest error logs from the current Kilo session.
- Auto-discover any related implementation report.
- Produce a fix report.

## 3.2 Explicitly provide an implementation report
```
/smartspec_fix_errors.md --kilocode \
  --report=.spec/reports/implement-tasks/T026-T040-implementation-report.md
```
Use this when:
- You started a new Kilo task.
- You want `/smartspec_fix_errors` to use the **same context** from your implementation run.

## 3.3 Provide custom logs
```
/smartspec_fix_errors.md --kilocode \
  --error-log=logs/test-output.txt
```

---

# 4. Flag Reference

### 4.1 Kilo / Orchestrator
- `--kilocode`
  - Enables Kilo Orchestrator mode.
  - Allows ingestion of test output, compiler errors, and structured context from Kilo.

### 4.2 Report Ingestion (v5.7.1)
- `--report=<path>`
  Explicitly provide an implementation or fix report.

If not provided, the system will:
1. Look in `.spec/reports/implement-tasks/` for the newest matching report.
2. Match by SPEC identifier and error patterns.
3. Use it automatically as the structured context.

### 4.3 Registry / Index
- `--index=<path>` override SPEC_INDEX
- `--registry-dir=<path>`
- `--registry-roots=<paths>` read-only supplemental registries

### 4.4 Repo resolution
- `--workspace-roots=<paths>`
- `--repos-config=<path>` (preferred for multi-repo)

### 4.5 Target selection
- `--spec=<path>`
- `--tasks=<path>`
- `--error-log=<path>` explicit error logs

### 4.6 Safety & Mode
- `--mode=recommend` (default: no write)
- `--mode=additive-meta` (safe metadata write only)
- `--safety-mode=strict` (default)
- `--safety-mode=dev`
- `--dry-run` (simulate metadata writes)

### 4.7 Output
- `--report-dir=<path>` default: `.spec/reports/smartspec_fix_errors/`
- `--report-format=md|json`

---

# 5. How Error Understanding Works
Regardless of where the error originates, `/smartspec_fix_errors.md` gathers error context from:

### (A) Explicit Sources
- `--report=<path>` (primary input when provided)
- `--error-log=<paths>`

### (B) Orchestrator Runtime Context (when using `--kilocode`)
- stdout / stderr from the failed implement run
- compiler errors
- failed test suite output
- structured Kilo error packets

### (C) Auto-Discovered Reports
If user does not provide `--report`, the workflow will:
1. Scan `.spec/reports/implement-tasks/`.
2. Find the latest report matching:
   - same SPEC folder
   - same error patterns
3. Ingest that report.

### (D) SPEC + Tasks
- Read `spec.md` and `tasks.md`
- Determine the **responsible SPEC** and task mapping.

---

# 6. Fix Workflow Steps (High-Level)

### Step 1 — Resolve SPEC_INDEX + Registries
Determine ownership, responsible specs, shared definitions.

### Step 2 — Ingest Error Context
Priority:
1. `--report`
2. Auto-discovered `.spec/reports/implement-tasks/`
3. Error logs / Kilo session
4. stdin or prompt content

### Step 3 — Classify Errors
- Build / type errors
- Unit test failures
- Integration mismatches
- Security gaps
- UI mismatches
- Cross-spec naming drift
- Config / environment mismatches

### Step 4 — Analyze SPEC Responsibilities
Use SPEC_INDEX + tasks.md to map errors to:
- SPEC ID
- specific tasks
- module ownership

### Step 5 — Produce Fix Plan
Includes:
- hypotheses
- evidence
- recommended safe fixes
- metadata suggestions
- risk levels

### Step 6 — Write Fix Report
Default location:
```
.spec/reports/smartspec_fix_errors/
```
Format: Markdown or JSON

---

# 7. When to Provide `--report`
Use it when:
- You have started a new Kilo task and want to carry over the previous session’s context.
- Your previous implement run generated a detailed report.
- You want fixes based on that exact scope.

Examples:
```
--report=.spec/reports/implement-tasks/T026-T040-implementation-report.md
```

---

# 8. When You Do *Not* Provide `--report`
The workflow will:
1. Search `.spec/reports/implement-tasks/`.
2. Select the newest report matching your SPEC.
3. Use that as structured context.

This is safe and recommended when your run is in the same Kilo session.

---

# 9. Sample Real Workflow Under Kilo

### Run 1 — Implement tasks
```
/smartspec_implement_tasks.md specs/.../tasks.md --kilocode
```
Implementation report created:
```
.spec/reports/implement-tasks/T026-T040-implementation-report.md
```

### Run 2 — Fix errors using report
```
/smartspec_fix_errors.md --kilocode \
  --report=.spec/reports/implement-tasks/T026-T040-implementation-report.md
```
Output:
- New fix report under `.spec/reports/smartspec_fix_errors/`
- Root-cause analysis
- Precise fix plan

---

# 10. Notes for Kilo Users
**IMPORTANT:** Each Kilo "Task" is an isolated session.

- When you press **New Task**, runtime context (errors, logs) is cleared.
- Reports stored on disk **do not disappear**.
- Use `--report` to preserve continuity across tasks.

---

# 11. Best Practices
- Always use `--kilocode` inside Kilo.
- Always preserve implementation reports.
- Use `--report` when switching tasks.
- Avoid guessing the responsible spec — let SPEC_INDEX decide.
- When multiple specs appear related, use strict mode to catch inconsistencies.

---

# 12. FAQ

### Q: Do I need to re-run tests before running fix_errors?
No. If you provide `--report` or if auto-discovery finds a report, the workflow uses structured error context.

### Q: Can fix_errors change code directly?
No — it only recommends code changes or updates metadata in `additive-meta` mode.

### Q: Does it work without `--kilocode`?
Yes, but you lose automatic ingestion of Kilo’s structured error logs.

---

# 13. Output Example
A typical fix report contains:
- summary of failing tests
- impacted API routes / models
- SPEC ownership mapping
- recommended fixes
- registry alignment notes
- risk assessment
- links to reports used as input

---

# 14. Conclusion
This manual now fully matches SmartSpec v5.7.1 and supports the new report-driven workflow, Orchestrator integration, and canonical governance model.

You may now safely run:
```
/smartspec_fix_errors.md --kilocode --report=<path>
```
with full confidence.

