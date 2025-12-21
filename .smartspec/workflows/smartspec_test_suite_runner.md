---
description: Run test suites and generate reports.
version: 6.0.0
workflow: /smartspec_test_suite_runner
---

# smartspec_test_suite_runner

> **Version:** 6.1.1  
> **Status:** Proposed  
> **Category:** quality

## Purpose

Execute a project's test suite (e.g., Jest, Vitest, Cypress) and generate a standardized SmartSpec report.

This is a **reports-only** workflow, but it executes an external test process, which is a **privileged operation**.

- It **does not** modify specs, registries, or application source code.
- It **does not** install dependencies.
- It writes only report artifacts under `.spec/reports/**`.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/test-suite-runner/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any intentional writes to application source code

> Note: test frameworks may create artifacts (coverage, screenshots). This workflow MUST treat those as **unexpected writes** unless they are configured to land under the run folder.

### `--apply` behavior (universal flag)

- Accepted for compatibility but **ignored**.
- The report header MUST note that `--apply` was ignored if provided.

---

## Threat model (minimum)

This workflow must defend against:

- **Arbitrary Code Execution**: running project-defined scripts is inherently powerful.
- **Shell injection**: unsafe concatenation of args/paths into shell strings.
- **Path traversal / symlink escape**: unsafe `--out` or `--junit-report-path`.
- **Infinite loops / hanging tests**: unbounded execution.
- **Secret leakage**: stdout/stderr, junit XML, screenshots, traces.
- **Network access**: tests making unexpected outbound calls.
- **Workspace pollution**: tests writing artifacts outside approved report folder.

### Hardening requirements (MANDATORY)

- **Path normalization (reads + writes):** Reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape (reads + writes):** Do not read/write through symlinks that resolve outside allowed scopes.
- **Output root safety (`--out`):** If provided, it is a *requested* base output root and MUST:
  - resolve under config `safety.allow_writes_only_under`
  - not fall under config `safety.deny_writes_under`
  - not be a runtime source folder
  - hard-fail with usage/config error (`exit 2`) if invalid
- **`--junit-report-path` safety:** If provided, the path MUST be relative to project root OR under the validated `--out` run folder; it MUST NOT escape via symlinks.
- **No arbitrary command execution:** The workflow MUST NOT accept a raw command string. It MAY only run `npm run <script>` (or configured package manager) where `<script>` is validated against `package.json` `scripts` keys.
- **No shell string concatenation:** The runner MUST spawn processes without invoking a shell (no `sh -c` style execution). Paths MUST NOT be interpolated into shell strings.
- **Timeouts:** Enforce a non-negotiable wall-clock timeout on the test process.
- **Redaction:** Apply `safety.redaction` patterns to all captured output and all report artifacts.
- **Network policy:** Default network access MUST be denied; network may be allowed only via `--allow-network`.
  - If the environment cannot technically enforce network denial, the workflow MUST emit `TSR-206 Network Not Enforced` (warning) and record the limitation.
- **Workspace isolation (best-effort, MUST document):**
  - Set `CI=1` for the test process.
  - Set `TMPDIR` (or platform equivalent) to a temp dir under the run folder.
  - Prefer setting `HOME` to a temp home under the run folder.
- **Unexpected writes detection:** After the run, the workflow MUST detect and report filesystem writes outside the run folder if possible (see TSR-205).

---

## Invocation

### CLI

```bash
/smartspec_test_suite_runner \
  --test-script <npm-script-name> \
  [--junit-report-path <relative/path/to/junit.xml>] \
  [--timeout 600] \
  [--allow-network] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

```bash
/smartspec_test_suite_runner.md \
  --test-script test:unit \
  --junit-report-path .spec/reports/test-suite-runner/_tmp/junit.xml \
  --timeout 600 \
  --out .spec/reports/test-suite-runner \
  --json \
  --platform kilo
```

---

## Inputs

### Required

- `--test-script <name>`: The name of the script in `package.json` to execute (e.g., `test`, `test:unit`, `test:e2e`).

### Optional

- `--junit-report-path <path>`: Path to where the test runner will write a JUnit XML report.
  - This workflow will attempt a **safe** runner-aware configuration so a JUnit report is produced.
  - If it cannot safely configure JUnit generation, it will fall back to stdout parsing and mark reduced confidence.
- `--timeout <seconds>`: Timeout for the entire test run. Defaults to `300`.
- `--allow-network`: Explicitly allows outbound network calls.

### Input validation (MANDATORY)

- `--test-script` MUST exist as a key in the `scripts` section of the nearest `package.json` in project root.
- Any provided paths (`--out`, `--junit-report-path`) MUST pass path normalization + no symlink escape rules.

---

## Flags

### Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply` (ignored)
- `--out <path>`
- `--json`
- `--quiet`

### Workflow-specific flags

- `--test-script <name>` (required)
- `--junit-report-path <path>` (optional)
- `--timeout <seconds>` (optional)
- `--allow-network` (optional)

---

## Output structure

Outputs are always written under a run folder to prevent overwrites.

- Default root: `.spec/reports/test-suite-runner/<run-id>/...`
- If `--out` is provided, it is treated as a *requested* base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts:

- `report.md`
- `summary.json`
- `stdout.txt` (redacted)
- `stderr.txt` (redacted)
- `junit.xml` (if provided/produced; redacted copies only)

### Exit codes

- `0`: All tests passed.
- `1`: One or more tests failed, or strict safety check reported a critical risk.
- `2`: Usage/config error or the test run timed out.

---

## Checks (v6.1)

Each check MUST emit a stable ID (`TSR-xxx`).

### Preflight safety checks (always enforced)

- **TSR-000 Preflight Safety**: Validate `--out` safety, `--junit-report-path` safety, path normalization + no symlink escape. Fail with `exit 2` on violation.
- **TSR-001 Script Exists**: `--test-script` exists in `package.json` `scripts`.

### Execution safety checks

- **TSR-101 Timeout Enforced**: The process is killed if it exceeds `--timeout`.
- **TSR-102 Shell Not Used**: The process spawn path does not invoke an interactive shell wrapper.
- **TSR-103 Network Policy**:
  - If `--allow-network` is NOT set: network is denied (or warning TSR-206 if not enforceable).
  - If `--allow-network` is set: report the risk explicitly.

### Result quality checks

- **TSR-201 JUnit Parsed**: JUnit XML was produced and parsed successfully.
- **TSR-202 Stdout Parsed (Fallback)**: JUnit missing; stdout parsing used with reduced confidence.
- **TSR-203 Redactions Applied**: Captured output was redacted; report includes counts only.
- **TSR-204 Reduced Structure**: Structured results could not be confidently extracted.

### Workspace integrity checks

- **TSR-205 Unexpected Writes**: The workflow detected files created/modified outside the run folder during the test run (best-effort detection). Always a warning, but may be treated as a failure in CI policy.
- **TSR-206 Network Not Enforced**: Environment cannot enforce network denial; recorded as a warning.

---

## Core Logic

1. **Preflight**: Resolve project root; validate paths and flags (TSR-000).
2. **Read `package.json`**: Ensure `--test-script` exists (TSR-001).
3. **Prepare Evidence Paths**:
   - Create run folder.
   - If `--junit-report-path` is set, validate and resolve it to a safe location.
4. **Runner-aware JUnit strategy (safe-only):**
   - The workflow MUST NOT blindly append arbitrary flags to the script command string.
   - It MAY use conservative adapters (e.g., env vars or well-known config hooks) where supported.
   - If no safe adapter applies, proceed without modification and rely on stdout parsing.
5. **Execute**: Run the test suite via the configured package manager command (e.g., `npm run <script>`), using:
   - no shell
   - bounded env (CI=1, temp HOME/TMPDIR under run folder)
   - enforced timeout
   - network denied unless `--allow-network`
6. **Capture**: Write redacted `stdout.txt`/`stderr.txt` to the run folder.
7. **Parse**:
   - If JUnit exists and is safe to read: parse and extract totals, failures, slow tests.
   - Else: fall back to stdout parsing with reduced confidence.
8. **Workspace integrity check** (best-effort): detect unexpected writes outside the run folder (TSR-205).
9. **Generate Artifacts**: `report.md` + `summary.json`.

---

## `report.md` Artifact Structure

```markdown
# Test Suite Report

**Run ID:** <run-id>
**Test Script:** `<script>`
**Timeout (s):** <timeout>
**Network Allowed:** <true|false>

## 1. Summary

- **Overall Status:** ✅ Pass | 🔴 Fail | 🟡 Warn
- **Duration:** <seconds>

| Total | Passed | Failed | Skipped |
| :---- | :----- | :----- | :------ |
| 128   | 125    | 3      | 0       |

## 2. Failures (Top)

- `<test_case>` — `<file>`

## 3. Slowest Tests (Top)

| Duration | Test Case |
| :------- | :-------- |
| 5.2s     | ...       |

## 4. Safety & Integrity

- Redactions applied: <count>
- Unexpected writes detected: <count> (see list)
- Network enforcement: enforced | not_enforced

## 5. Next Steps

- Recommend next steps that are guaranteed to exist in your project registry (`.spec/WORKFLOWS_INDEX.yaml`).
- If suggesting a SmartSpec workflow, include both CLI + Kilo forms.

Template (replace with real registry-backed commands):

CLI:
`/<workflow_name> <primary-input> [--out <dir>] [--json]`

Kilo:
`/<workflow_name>.md <primary-input> [--out <dir>] [--json] --platform kilo`
```

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_test_suite_runner",
  "version": "6.1.1",
  "run_id": "string",
  "status": "pass|fail|warn",
  "scope": {
    "test_script": "string",
    "timeout_seconds": 300,
    "allow_network": false,
    "junit_report_path": "string|null"
  },
  "results": {
    "summary": {
      "total": 0,
      "passed": 0,
      "failed": 0,
      "skipped": 0,
      "duration_seconds": 0
    },
    "failures": [
      {
        "test_case": "string",
        "file": "string|null",
        "error_message": "string"
      }
    ],
    "warnings": [
      {"check_id": "TSR-205", "message": "string"}
    ]
  },
  "writes": {
    "reports": [
      "path/to/report.md",
      "path/to/summary.json",
      "path/to/stdout.txt",
      "path/to/stderr.txt"
    ]
  }
}
```

---

# End of workflow doc

