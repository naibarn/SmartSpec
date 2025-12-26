---
name: /smartspec_deployment_planner
version: 6.1.1
role: release/deployment
write_guard: REPORTS-ONLY+GOVERNED-WRITE-WITH-APPLY
purpose: Generate a deployment plan, release notes, and optional CI pipeline patch
  for a spec. Preview-first; governed writes only with --apply and explicit CI write
  enable.
version_notes:
- v6.1.1: Align to SmartSpec v6 hardening (path normalization + no symlink escape
    + spec-id constraints); evidence-first release notes via strict verify report;
    CI workflow generation is patch-first and requires explicit opt-in to write into
    .github/workflows; universal flags + output root safety; safer git usage.
description: Generate deployment plans and checklists.
workflow: /smartspec_deployment_planner
---


# /smartspec_deployment_planner (v6.1.1)

Generate:

- a **deployment plan** (`deployment_plan.md`)
- **release notes** (`release_notes.md`) based on **verification evidence**
- an optional **CI/CD pipeline patch** (GitHub Actions YAML template) for deploying the spec

This workflow is **preview-first**.

- Default: writes **reports only**.
- With `--apply`: may write governed artifacts under `specs/**`.
- Writing into `.github/workflows/**` is **disabled by default** and requires an explicit flag and allowlist validation.

---

## 0) Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### 0.1 Write scopes (enforced)

**Always allowed writes (safe outputs):**

- Reports: `.spec/reports/deployment-planner/**`
- Optional prompts: `.spec/prompts/**`
- Optional generated scripts: `.smartspec/generated-scripts/**`

**Governed writes (ONLY with `--apply`):**

- `specs/<category>/<spec-id>/deployment/plan.md`
- `specs/<category>/<spec-id>/deployment/release_notes.md`

**CI workflow writes (SPECIAL, ONLY with `--apply` + `--write-ci-workflow`):**

- `.github/workflows/deploy-<spec-id>.yml`

**Forbidden writes (must hard-fail):**

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact not explicitly targeted (e.g., `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modifications not listed above

### 0.2 Preview-first rule (MANDATORY)

- Without `--apply`: MUST generate a **Change Plan** showing what would be written (including CI patch intent if requested).
- With `--apply`: MUST still generate the Change Plan, then apply changes.

---

## 1) Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape on any read/write paths.
- Untrusted `spec-id` being used in file names.
- Secret leakage into reports or CI YAML.
- Pipeline vulnerabilities (excessive permissions, unpinned actions, unsafe triggers).
- Evidence spoofing (release notes claiming shipped work from checkboxes).
- Command injection via `git` arguments.

### 1.1 Security hardening (MANDATORY)

- **No network access** (unless the environment inherently allows it; then record limitation).
- **No shell execution:** do not construct shell strings; spawn processes without a shell.
- **Path normalization (reads + writes):** reject traversal (`..`), absolute paths, and control characters.
- **No symlink escape (reads + writes):** resolve realpath and ensure it remains within allowed scopes.
- **Output root safety (`--out`):** requested base output root MUST pass allow/deny validation; else `exit 2`.
- **Spec-id constraints (MANDATORY):**
  - `spec-id` MUST match: `^[a-z0-9_\-]{3,64}$`
  - used for file names (e.g., `deploy-<spec-id>.yml`) only after validation
- **Redaction:** apply configured redaction patterns to all reports and generated YAML.
- **Atomic writes (governed):** temp+rename for `specs/**` outputs and CI workflow output.
- **Bounded scanning:** enforce file count/byte/time limits from config.

---

## 2) Evidence-first release notes (MANDATORY)

This workflow MUST NOT treat `tasks.md` checkboxes as proof of completion.

Release notes MUST be derived from **verification evidence**:

- Prefer `--verify-summary <path>` (output of `smartspec_verify_tasks_progress_strict`).
- If `--verify-summary` is not provided:
  - in `--mode=normal`, release notes MUST be marked as **draft** and include a prominent note: "Verification evidence not provided; status may be inaccurate".
  - in `--mode=strict`, hard-fail (`exit 1`).

---

## 3) Inputs

### 3.1 Primary input (positional-first)

- `spec_md` (required, positional): `specs/<category>/<spec-id>/spec.md`

### 3.2 Optional inputs

- `--tasks <path>`: override tasks path (read-only).
- `--verify-summary <path>`: strict verify `summary.json` evidence.
- `--previous-release-tag <tag>`: used only for release notes diff context.
- `--target-env <dev|staging|prod|other>`: influences plan/checklists.

### 3.3 CI pipeline generation inputs

- `--ci-provider <github-actions|other>`: default `github-actions`.
- `--write-ci-workflow`: enable governed write into `.github/workflows/**` (requires `--apply`).
- `--ci-template <name>`: selects a validated template.

---

## 4) Input validation (MANDATORY)

- `spec_md` MUST exist and be a file.
- Derived `spec-id` MUST satisfy spec-id constraints.
- All user-supplied paths MUST reject traversal (`..`), absolute paths, and control characters.
- All resolved paths MUST remain within project root and MUST NOT escape via symlinks.
- If `--verify-summary` is provided:
  - MUST be valid JSON
  - MUST contain `workflow` and `run_id`
- If `--write-ci-workflow` is provided:
  - MUST also have `--apply`
  - CI output path `.github/workflows/deploy-<spec-id>.yml` MUST be allowed by config allow/deny lists, and MUST NOT be a symlink

---

## 5) Flags

### 5.1 Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### 5.2 Workflow-specific flags

- `--tasks <path>`
- `--verify-summary <path>`
- `--previous-release-tag <tag>`
- `--target-env <dev|staging|prod|other>`
- `--mode <normal|strict>` (default: normal)
- `--strict` (alias for `--mode=strict`)
- `--ci-provider <github-actions|other>`
- `--ci-template <name>`
- `--write-ci-workflow`

---

## 6) Invocation

### CLI (preview-only)

```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --target-env prod \
  --out .spec/reports/deployment-planner \
  --json
```

### CLI (apply governed deployment artifacts)

```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --apply \
  --out .spec/reports/deployment-planner \
  --json
```

### CLI (apply + write CI workflow; explicit opt-in)

```bash
/smartspec_deployment_planner \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --apply \
  --write-ci-workflow \
  --ci-provider github-actions \
  --ci-template deploy-basic \
  --out .spec/reports/deployment-planner \
  --json
```

### Kilo Code

```bash
/smartspec_deployment_planner.md \
  specs/<category>/<spec-id>/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/<run-id>/summary.json \
  --target-env prod \
  --out .spec/reports/deployment-planner \
  --json \
  --platform kilo
```

---

## 7) Output structure

Outputs are written under a unique run folder.

- Default root: `.spec/reports/deployment-planner/<run-id>/...`
- If `--out` is provided, it is treated as a requested base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts (safe outputs):

- `report.md`
- `summary.json`
- `change_plan.md` (always)
- `deployment_plan.preview.md`
- `release_notes.preview.md`
- `ci_workflow.patch.yml` (if CI generation enabled; patch/preview always)

Governed artifacts (only with `--apply`):

- `specs/<category>/<spec-id>/deployment/plan.md`
- `specs/<category>/<spec-id>/deployment/release_notes.md`
- `.github/workflows/deploy-<spec-id>.yml` (only with `--apply` + `--write-ci-workflow`)

---

## 8) Git usage policy (if enabled)

Git is optional and used only to assist release note context.

- MUST spawn without a shell.
- MUST treat `--previous-release-tag` as a single sanitized argument.
- MUST enforce a timeout for any git command.
- If git is unavailable or fails, continue in normal mode with a warning; strict mode may block depending on policy.

---

## 9) CI template security requirements (GitHub Actions)

If generating a GitHub Actions workflow, the template MUST:

- set `permissions:` to least privilege
- avoid `pull_request_target` for untrusted forks
- pin third-party actions to a commit SHA (recommended)
- avoid printing secrets; do not enable debug modes that may echo secrets
- prefer environment protections for prod deployments

If a template cannot meet these, it MUST be rejected in strict mode.

---

## 10) Checks

Each check MUST emit a stable ID (`DEP-xxx`).

### Preflight safety

- **DEP-000 Preflight Safety**: path normalization + no symlink escape + output root safety + spec-id constraints.

### Evidence checks

- **DEP-101 Verify Evidence Present**:
  - strict: `--verify-summary` required
  - normal: if missing, mark release notes draft and warn

### CI checks

- **DEP-201 CI Write Gate**: writing `.github/workflows/**` requires `--apply` + `--write-ci-workflow` + allowlist.
- **DEP-202 CI Template Security**: template meets security requirements.

### Quality checks

- **DEP-301 Atomic Writes Enabled**: governed outputs written atomically.
- **DEP-302 Redactions Applied**: redaction patterns applied; report includes counts only.

### Exit codes

- `0`: Generated successfully (preview or apply).
- `1`: Strict-mode blocking issue (evidence missing, template rejected).
- `2`: Usage/config error (unsafe paths, invalid spec-id, disallowed output root).

---

## 11) Core logic

1) **Preflight**: validate paths, spec-id constraints, `--out` safety (DEP-000).
2) **Load inputs**: parse spec/tasks; bound scanning.
3) **Load verification evidence**:
   - strict: require `--verify-summary` (DEP-101)
   - normal: if missing, mark draft release notes.
4) **Generate previews**:
   - deployment plan preview
   - release notes preview (evidence-based)
   - CI workflow patch preview (if requested)
5) **Generate Change Plan**: list governed files that would be written and diffs.
6) **Apply (optional)**:
   - if `--apply`, write governed spec deployment files atomically.
   - if `--apply` + `--write-ci-workflow`, write CI workflow atomically.
7) **Write reports**: report.md + summary.json.

---

## 12) `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_deployment_planner",
  "version": "6.1.1",
  "run_id": "string",
  "mode": "preview|apply",
  "status": "ok|warn|error",
  "scope": {
    "spec_path": "string",
    "verify_summary": "string|null",
    "target_env": "string|null",
    "ci_provider": "string|null",
    "write_ci_workflow": false
  },
  "summary": {
    "draft_release_notes": false,
    "governed_writes": 0,
    "ci_patch_generated": false
  },
  "writes": {
    "reports": ["path/to/report.md", "path/to/summary.json", "path/to/change_plan.md"],
    "governed": ["specs/.../deployment/plan.md", "specs/.../deployment/release_notes.md"],
    "ci": [".github/workflows/deploy-<spec-id>.yml"]
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

