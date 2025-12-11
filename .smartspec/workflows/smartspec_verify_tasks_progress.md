---
name: /smartspec_verify_tasks_progress
version: 5.8.0
role: verification/governance
write_guard: NO-WRITE
purpose: Verify real implementation progress against tasks/specs and the centralized SmartSpec layer using an **evidence-first** model, while preserving all v5.7 capabilities (SPEC_INDEX, registry, multi-repo).
version_notes:
  - v5.2.0: initial verify-tasks workflow
  - v5.6.0: centralization + multi-repo / multi-registry alignment
  - v5.7.0: governance alignment; documentation-only update
  - v5.8.0: evidence-first progress model; per-task verdicts; JSON reports for sync workflows
---

# /smartspec_verify_tasks_progress (v5.8.0)

This workflow verifies implementation progress against `tasks.md`, `spec.md`, and the canonical SmartSpec layer.

v5.8.0 introduces an **evidence-first model** while keeping all v5.7 behavior intact:

- Checkboxes in `tasks.md` are *signals*, not the source of truth.
- Completion is based on **real evidence** in code, tests, docs, and deployment artifacts.
- v5.7 features (SPEC_INDEX, registry alignment, multi-repo support, safety flags) are preserved.

> Scope
>
> - Read-only for: code, spec, tasks, registries, UI JSON, SPEC_INDEX.
> - Writes: reports only, under `.spec/reports/verify-tasks-progress/` (unless `--dry-run`).
> - This workflow NEVER edits `tasks.md` or SPEC_INDEX.

---

## 1. Inputs & Flags

### 1.1 Target Selection (legacy, preserved)

```bash
--spec=<path>         # explicit spec path
--tasks=<path>        # explicit tasks path (optional; resolved from spec when omitted)
--spec-id=<id>        # optional logical spec id; resolved via SPEC_INDEX
```

Resolution order (unchanged from v5.7):

1. If `--spec` is provided → use that file.
2. Else if `--spec-id` is provided → resolve via SPEC_INDEX.
3. Auto-detect `spec.md` in the working directory or parent folders (implementation-dependent).
4. `tasks.md` is resolved adjacent to `spec.md` when not explicitly provided.

### 1.2 SPEC_INDEX & Registry (legacy, preserved)

```bash
--index=<path>          # SPEC_INDEX path (default: .spec/SPEC_INDEX.json)
--specindex=<path>      # legacy alias for --index
--registry-dir=<path>   # primary registry directory (default: .spec/registry)
--registry-roots=<csv>  # additional registry roots (read-only)
```

Behavior (unchanged):

- SPEC_INDEX is used to:
  - map spec-id → spec path, tasks path, registry roots
  - discover cross-spec dependencies for richer context
- Registry directories are read-only in this workflow; used only for validation/analysis.

### 1.3 Multi-Repo Support (legacy, preserved)

```bash
--workspace-roots=<csv>  # additional repo roots for monorepo / multi-repo
--repos-config=<path>    # structured multi-repo config (takes precedence over workspace-roots)
```

Behavior:

- `workspace-roots` allows the workflow to scan multiple repos/workspaces.
- `repos-config` may define per-repo:
  - root path
  - spec/registry locations
  - language/tooling hints

### 1.4 Reporting (legacy + v5.8 extensions)

```bash
--report-dir=<path>        # output directory (default: .spec/reports/verify-tasks-progress/)
--report=<summary|detailed> # markdown report detail level (default: summary)
--report-format=<md|json>  # md (markdown) or json; default: md
--dry-run                  # print report to stdout only; no file written
```

- When `--report-format=md` → writes markdown report (v5.7 behavior).
- When `--report-format=json` → writes JSON report (new in v5.8) suitable for automation.
- Implementations MAY emit both md + json when requested.

### 1.5 Evidence-First Controls (new in v5.8)

```bash
--evidence-only            # ignore checkbox state; compute metrics from evidence only
--run-tests                # optionally run or query tests while collecting evidence
--evidence-script=<path>   # optional custom evidence provider script
```

- `--evidence-only`:
  - progress and verdicts are computed purely from evidence; `declared_status` is still reported but ignored for scoring.
- `--run-tests`:
  - enables test execution or CI result queries; failing tests downgrade verdicts to `partial` in strict mode.
- `--evidence-script`:
  - allows integration with project-local scripts (e.g., `scripts/check_tasks_evidence.py`) that return additional evidence.

### 1.6 Safety (legacy, preserved)

```bash
--safety-mode=<strict|dev>  # default: strict
--strict                    # alias for --safety-mode=strict
```

Behavior:

- `strict`:
  - failures in evidence scripts or test hooks cause conservative verdicts (`partial` or `incomplete`).
- `dev`:
  - best-effort; missing evidence sources are logged but do not fail the workflow.

---

## 2. Evidence Model (v5.8)

For each task (and optionally subtask) in `tasks.md`, the workflow computes:

- `declared_status`:
  - `checked | unchecked | missing` → from the checkbox in `tasks.md`.
- `observed_evidence`:
  - `none | partial | complete` → based on code/tests/docs/deploy.
- `verdict` (used for progress):
  - `complete` → evidence `complete` (and tests pass if `--run-tests`).
  - `unsynced_complete` → evidence `complete` but checkbox unchecked.
  - `false_positive` → checkbox checked but evidence `none`.
  - `partial` → evidence `partial` (or tests failing).
  - `incomplete` → evidence `none` and checkbox unchecked.

### 2.1 Progress Calculation

- By default (compatible mode):

  ```text
  progress = (complete + unsynced_complete) / total_tasks
  ```

- When `--evidence-only` is enabled:
  - same formula but `declared_status` is ignored entirely for scoring.

Checkboxes are reported for visibility but never used as the sole source of truth.

---

## 3. Evidence Providers

### 3.1 Built-in Providers

The workflow MAY include built-in providers for:

- Routes:
  - scan HTTP route definitions for expected endpoints.
- Services:
  - scan service files for required methods/classes.
- Tests:
  - scan unit/integration/performance test directories.
- Documentation:
  - scan docs/api, docs/deployment, etc.
- Deployment:
  - scan k8s manifests, monitoring configs, CI/CD configs.

### 3.2 Custom Evidence Script

When `--evidence-script=<path>` is provided:

- The script is invoked with context (e.g., spec path, tasks path).
- Expected to return a JSON structure mapping task IDs → evidence data.
- The workflow merges this data into its internal evidence model.

Example (conceptual):

```bash
python scripts/check_tasks_evidence.py \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md
```

Output is parsed and combined with built-in evidence.

### 3.3 Test Execution (optional)

When `--run-tests` is enabled, implementations MAY:

- Run targeted tests for affected services/endpoints.
- Or, read the latest CI test results from a known location.

Test outcomes affect `observed_evidence` and `verdict` (especially in `strict` mode).

---

## 4. Evaluation Flow (v5.8, replaces old section 12)

1. **Resolve spec/tasks/index/registry** using v5.7 rules and flags.
2. **Parse `tasks.md`** into a structured list of tasks/subtasks with IDs & checkboxes.
3. For each task:
   1. Collect declared data (ID, title, dependencies, `declared_status`).
   2. Invoke built-in evidence providers (code, routes, tests, docs, deploy).
   3. If configured, invoke `--evidence-script` and merge output.
   4. If configured, and allowed by safety mode, `--run-tests` hooks are executed/read.
   5. Compute `observed_evidence` and `verdict`.
4. Aggregate per-task verdicts into:
   - per-phase metrics (if phases are encoded in tasks.md),
   - overall progress metrics,
   - lists of:
     - false positives,
     - unsynced completes,
     - high-risk gaps (e.g., security-critical tasks with no evidence).
5. Render the report (markdown and/or JSON) according to flags.

All v5.7 behaviors (SPEC_INDEX alignment, registry awareness, multi-repo context) remain available and may enrich the analysis (e.g., by knowing cross-spec dependencies).

---

## 5. JSON Report Format (v5.8)

When `--report-format=json` is used, the workflow emits a JSON document with at least:

```jsonc
{
  "spec_id": "spec-002-user-management",
  "spec_path": "specs/feature/spec-002-user-management/spec.md",
  "tasks_path": "specs/feature/spec-002-user-management/tasks.md",
  "summary": {
    "total_tasks": 78,
    "complete": 52,
    "unsynced_complete": 4,
    "false_positive": 6,
    "partial": 10,
    "incomplete": 6,
    "progress_percent": 71.8,
    "risk_level": "MEDIUM"
  },
  "tasks": [
    {
      "id": "T064",
      "title": "Write unit tests for User Service",
      "declared_status": "checked",
      "observed_evidence": "partial",
      "verdict": "partial",
      "evidence": {
        "unit_test_files": ["tests/unit/user.service.test.ts"],
        "last_test_run": {
          "status": "failed",
          "timestamp": "..."
        }
      }
    }
  ]
}
```

This JSON is the canonical input for automation workflows such as:

- `/smartspec_sync_tasks_checkboxes` (to sync checkboxes with evidence),
- CI dashboards,
- custom governance reports.

---

## 6. Output & Storage

By default, markdown reports are stored under:

```text
.spec/reports/verify-tasks-progress/
```

JSON reports may be stored in the same directory or as configured via `--report-dir`.

---

## 7. Governance Guarantees

This workflow must respect the following:

- **NO writes** to:
  - `spec.md`
  - `tasks.md`
  - source code
  - SPEC_INDEX
  - registry files
  - UI JSON / config
- All changes are expressed via:
  - stdout logs
  - markdown reports
  - JSON reports

Any future extensions MUST remain backward-compatible with v5.7 semantics and respect the `NO-WRITE` guard.
