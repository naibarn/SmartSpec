---
name: /smartspec_generate_tests
version: 6.1.1
role: test-planning/governance
write_guard: REPORTS-ONLY+GOVERNED-WRITE-WITH-APPLY
purpose: Generate a SmartSpec-governed test plan (test matrix + acceptance criteria
  + required evidence) aligned with SmartSpec v6 governance. Default outputs are reports-only;
  optional apply writes the test plan into the spec folder under specs/**.
version_notes:
- v6.1.1: v6 governance alignment; resolves NO-WRITE/output mismatch; universal flags;
    preview-first change plan; secure path + symlink hardening; de-dup via SPEC_INDEX/registries;
    reduces overlap by referencing specialized workflows (NFR/UI/contract/security).
description: Generate test artifacts/suggestions (prompts/scripts/reports).
workflow: /smartspec_generate_tests
---


# /smartspec_generate_tests (v6.1.1)

Generate a comprehensive **test plan** from `spec.md` (and adjacent `tasks.md`, optional `ui.json`), aligned with registries and SmartSpec governance.

This workflow is **preview-first**:

- Default: writes **reports only** (safe outputs).
- With `--apply`: may write a governed test plan file under `specs/**`.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

**Always allowed writes (safe outputs):**

- Reports: `.spec/reports/generate-tests/**`

**Governed writes (ONLY with `--apply`):**

- `specs/<category>/<spec-id>/testplan/tests.md` (or configured target path)

**Forbidden writes (must hard-fail):**

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact not explicitly targeted (e.g., `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)

### 0.2 Preview-first rule (MANDATORY)

- Without `--apply`: MUST generate a **Change Plan** describing what would be written to governed paths.
- With `--apply`: MUST still generate the Change Plan, then apply changes.

---

## 1) Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape on read/write paths.
- Writing governed artifacts without `--apply`.
- Reading untrusted artifacts (e.g., `ui.json`) and copying secrets into reports.
- Runaway scans due to huge repos.

### 1.1 Security hardening (MANDATORY)

- **No network access**.
- **No shell execution**.
- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape (reads + writes):** do not read/write through symlinks that resolve outside allowed scopes.
- **Redaction:** apply configured redaction patterns to reports.
- **Excerpt policy:** avoid embedding large raw blocks from spec/tasks/ui.json.
- **Bounded scanning:** enforce file count / byte / time limits from config.
- **Atomic writes (governed):** when `--apply` writes `tests.md`, it MUST write atomically (temp+rename).

### 1.2 Output root safety (`--out`) (MANDATORY)

If `--out` is provided, it is a requested base output root and MUST:

- resolve under config allowlist
- not fall under config denylist
- hard-fail (`exit 2`) if invalid

---

## 2) What it produces

### 2.1 Test plan content

- Scope and assumptions
- Test matrix (unit / integration / contract / security / NFR/perf / observability / UI)
- Test cases grouped by feature and task
- Acceptance criteria per test group
- Fixtures and test data needs
- Evidence requirements (what artifacts must exist to claim coverage)
- Registry alignment notes (terms, API/model names)
- Gaps / risks / TODO list

### 2.2 De-duplication behavior

- Avoid generating duplicate tests when tasks already describe equivalent verification.
- Reuse shared definitions via registries and SPEC_INDEX.
- If names drift from registries, strict mode blocks with an explicit report section.

---

## 3) Inputs (positional-first)

### 3.1 Primary input

- `spec_md` (required, positional): `specs/<category>/<spec-id>/spec.md`

### 3.2 Optional adjacent files (auto-discovered)

- `tasks.md` adjacent to spec
- `ui.json` adjacent to spec (or `specs/<...>/ui/ui.json` depending on project layout)

### 3.3 Multi-repo + registries (config-first)

- Use config wiring for:
  - workspace roots / repos mapping
  - registry roots
  - canonical `.spec/SPEC_INDEX.json`

Optional overrides (read-only):

- `--repos-config <path>`
- `--workspace-roots <csv>`
- `--registry-roots <csv>`
- `--index <path>`

---

## 4) Flags

### 4.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### 4.2 Workflow-specific flags

- `--tasks <path>`: override tasks path (read-only).
- `--ui-json <path>`: override UI JSON path (read-only).
- `--mode <normal|strict>`: default `normal`.
- `--strict`: alias for `--mode=strict`.
- `--plan-format <md|json|both>`: default `md`.
- `--target-path <path>`: governed output path (default: `testplan/tests.md` under the spec folder). Only used with `--apply`.
- `--include-dependencies`: include tests that validate integration points with dependency specs.
- `--max-tests <int>`: cap generated test items (bounded output).

---

## 5) Invocation

### CLI

```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  [--mode strict] \
  [--plan-format both] \
  [--include-dependencies] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

Apply mode (writes governed test plan into spec folder):

```bash
/smartspec_generate_tests \
  specs/<category>/<spec-id>/spec.md \
  --apply \
  [--target-path specs/<category>/<spec-id>/testplan/tests.md] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json]
```

### Kilo Code

```bash
/smartspec_generate_tests.md \
  specs/<category>/<spec-id>/spec.md \
  [--mode strict] \
  [--plan-format both] \
  [--include-dependencies] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json] \
  --platform kilo
```

Apply mode:

```bash
/smartspec_generate_tests.md \
  specs/<category>/<spec-id>/spec.md \
  --apply \
  [--target-path specs/<category>/<spec-id>/testplan/tests.md] \
  [--out .spec/reports/generate-tests/<label>] \
  [--json] \
  --platform kilo
```

---

## 6) Outputs

All outputs are written under a unique run folder.

Default report root:

```
.spec/reports/generate-tests/<run-id>/
```

Artifacts (safe outputs):

- `report.md` (main)
- `summary.json`
- `change_plan.md` (always)
- `change_plan.json` (when `--json` or `--plan-format=json|both`)
- `tests.preview.md` (generated plan preview)
- `tests.preview.json` (optional)

Governed artifact (only with `--apply`):

- `specs/<category>/<spec-id>/testplan/tests.md`

---

## 7) Workflow interoperability and overlap policy

This workflow generates **WHAT to test** and **WHAT evidence is required**, and avoids re-implementing specialized auditors/verifiers/runners.

### 7.1 Canonical evidence hooks (align with updated workflows)

When relevant, the generated plan MUST reference evidence artifacts from the corresponding workflow run folders (if present in the project registry). Use these **paths as the canonical convention**:

- **Test execution evidence**
  - Runner output: `.spec/reports/test-suite-runner/<run-id>/summary.json`
  - Analyzer output: `.spec/reports/test-report-analyzer/<run-id>/summary.json`

- **NFR / Performance evidence**
  - Planner output: `.spec/reports/nfr-perf-planner/<run-id>/summary.json`
  - Verifier output: `.spec/reports/nfr-perf-verifier/<run-id>/summary.json`

- **UI / Design system evidence**
  - UI audit output: `.spec/reports/ui-component-audit/<run-id>/summary.json`
  - Design-system migration preview/apply: `.spec/reports/design-system-migration/<run-id>/summary.json`

- **Security evidence**
  - Threat model input source: `.spec/reports/security-threat-model/<run-id>/threats.md`
  - Security audit output: `.spec/reports/security-audit/<run-id>/summary.json`

- **Data model evidence**
  - Data model validation output: `.spec/reports/data-model-validation/<run-id>/summary.json`

If an evidence hook path does not exist or the workflow is not registered, the plan MUST:

- mark the item as **"evidence pending"** (not a failure in normal mode)
- in `--mode=strict`, treat missing *required* evidence hooks as a blocking gap

### 7.2 Registry-backed rule (MANDATORY)

The plan MUST NOT assume a workflow exists unless it is registry-backed (listed in `.spec/WORKFLOWS_INDEX.yaml`). For any suggested next command, include both CLI + Kilo forms, and keep it as a template if registry resolution is not available at generation time.

---

## 8) Core steps

1) **Preflight safety**: validate all input paths, output root, and limits.
2) **Resolve canonical context**: load `.spec/SPEC_INDEX.json` and registries (primary + supplemental) with collision detection.
3) **Load spec/tasks/ui** (read-only): extract behaviors, contracts, dependencies, NFRs, UI state coverage.
4) **Cross-SPEC alignment gate**: ensure generated tests don’t contradict dependency specs.
5) **Generate test matrix**:
   - unit/integration tests from behaviors + tasks
   - contract tests from API/contract sections
   - security tests from auth/authz/threat notes
   - NFR/perf tests from NFR thresholds
   - observability tests from logging/metrics/tracing requirements
   - UI/component tests from UI flows + state coverage + a11y baseline
6) **De-duplication pass**: remove duplicates; map tests to tasks when possible.
7) **Produce artifacts**: preview plan + change plan + summary.
8) **Apply (optional)**: if `--apply`, write governed `tests.md` atomically.

---

## 9) Checks

Each check MUST emit a stable ID (`GT-xxx`).

### Preflight safety

- **GT-000 Preflight Safety**: path normalization + no symlink escape + output root safety.

### MUST checks (strict blocks)

- **GT-101 Spec Parsable**: `spec.md` parsed sufficiently to extract behaviors/contracts/NFRs.
- **GT-102 Tasks Parsable**: `tasks.md` parsed if present; if required but missing, strict blocks.
- **GT-103 Registry Alignment**: referenced shared names align with canonical registries.

### SHOULD checks (warnings)

- **GT-201 Coverage Gaps**: high-risk features/tasks lack tests.
- **GT-202 Evidence Hooks Missing**: plan references evidence but no matching report root exists (non-blocking; informational).
- **GT-203 Reduced Coverage**: scan limits hit; reduced confidence.
- **GT-204 UI JSON Metadata Missing**: UI JSON lacks required metadata; tests should note reduced confidence.

### Exit codes

- `0`: Generated successfully.
- `1`: Strict-mode blocks (e.g., GT-103 fail).
- `2`: Usage/config error (unsafe paths, invalid output root).

---

## 10) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_generate_tests",
  "version": "6.1.1",
  "run_id": "string",
  "status": "ok|warn|error",
  "mode": "normal|strict",
  "scope": {
    "spec_path": "string",
    "tasks_path": "string|null",
    "ui_json_path": "string|null",
    "include_dependencies": false,
    "target_path": "string|null"
  },
  "summary": {
    "tests_generated": 0,
    "tests_deduped": 0,
    "gaps": 0,
    "reduced_coverage": false
  },
  "writes": {
    "reports": [
      "path/to/report.md",
      "path/to/summary.json",
      "path/to/change_plan.md",
      "path/to/tests.preview.md"
    ],
    "governed": [
      "specs/<category>/<spec-id>/testplan/tests.md"
    ]
  }
}
```

---


---

## Flags

### Universal flags (must support)

All SmartSpec workflows support these universal flags:

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English, `auto` for automatic detection) |
| `--platform` | No | Platform mode (`cli` for CLI, `kilo` for Kilo Code, `ci` for CI/CD, `other` for custom integrations) |
| `--out` | No | Base output directory for reports and generated files (must pass safety checks) |
| `--json` | No | Output results in JSON format for machine parsing and automation |
| `--quiet` | No | Suppress non-essential output, showing only errors and critical information |

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Positional arguments:** When supported, use positional arguments for primary inputs (e.g., spec path) instead of flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file

# End of workflow doc

