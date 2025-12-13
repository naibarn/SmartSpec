# /smartspec_deployment_planner Manual (v6.0, English)

## Overview

The `/smartspec_deployment_planner` workflow (v6.1.1) is a critical component of the SmartSpec release process, designed to automate the generation of necessary deployment artifacts for a given specification.

**Purpose:** To generate a deployment plan, evidence-based release notes, and an optional CI pipeline patch (GitHub Actions YAML) for a specification defined by `spec.md`.

**Key Features:**

*   **Preview-First:** By default, the workflow generates reports and a `change_plan.md` showing intended changes without writing governed artifacts.
*   **Governed Writes:** Requires the `--apply` flag to write deployment plans and release notes into the `specs/**` directory.
*   **Evidence-Based Release Notes:** Release notes are derived from strict verification evidence (`--verify-summary`), ensuring accuracy and preventing claims based solely on unchecked task lists.
*   **Security Hardening:** Enforces strict path normalization, symlink protection, output root safety, and spec-ID constraints (SmartSpec v6 hardening).

**Role:** `release/deployment`

## Usage

### CLI Usage

The Command Line Interface (CLI) is the primary method for executing this workflow, supporting both preview mode and governed application.

#### Preview Mode (Reports Only)

This command generates all artifacts (deployment plan, release notes, and change plan) into the specified output directory without modifying any governed files (e.g., files under `specs/`).

```bash
/smartspec_deployment_planner \
  specs/feature/my-new-feature/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/run-123/summary.json \
  --target-env staging \
  --out .spec/reports/deployment-planner-run-123 \
  --json
```

#### Apply Mode (Governed Writes)

This command applies the generated deployment plan and release notes to the specification's deployment directory (`specs/<category>/<spec-id>/deployment/`) after generating the change plan.

```bash
/smartspec_deployment_planner \
  specs/feature/my-new-feature/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/run-123/summary.json \
  --target-env prod \
  --apply \
  --out .spec/reports/deployment-planner-run-123
```

#### Apply Mode with CI Workflow Generation

This command applies governed writes *and* generates the CI workflow patch into `.github/workflows/`. This requires explicit opt-in via the `--write-ci-workflow` flag, in addition to `--apply`.

```bash
/smartspec_deployment_planner \
  specs/infra/database-migration/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/run-456/summary.json \
  --apply \
  --write-ci-workflow \
  --ci-provider github-actions \
  --ci-template deploy-basic \
  --out .spec/reports/deployment-planner-run-456
```

### Kilo Code Usage

The workflow can be integrated into Kilo pipelines using the Kilo Code syntax.

```bash
# Example Kilo Code block for a deployment step
workflow_step "Generate Deployment Artifacts" {
  name: "/smartspec_deployment_planner"
  input {
    spec_md: "specs/feature/my-new-feature/spec.md"
    verify_summary: ".spec/reports/verify-tasks-progress/run-123/summary.json"
    target_env: "prod"
    apply: true
    out: ".spec/reports/deployment-planner-kilo-run"
    platform: "kilo"
  }
}
```

## Use Cases

### Use Case 1: Generating a Production Deployment Plan (Preview)

**Scenario:** A developer needs to review the final deployment plan and release notes for a feature before committing the artifacts. They want to ensure the release notes accurately reflect verified tasks and target the production environment.

**Command (CLI):**

```bash
/smartspec_deployment_planner \
  specs/feature/user-auth-v2/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/auth-run-789/summary.json \
  --target-env prod \
  --out .spec/reports/auth-v2-preview
```

**Expected Result:**

1.  Files are written to `.spec/reports/auth-v2-preview/`.
2.  `change_plan.md` shows the intent to write `specs/feature/user-auth-v2/deployment/plan.md` and `release_notes.md`, but notes that `--apply` is missing.
3.  `deployment_plan.preview.md` and `release_notes.preview.md` are generated, based on the provided verification summary.
4.  Exit Code: `0`.

### Use Case 2: Applying Draft Release Notes (Normal Mode, Missing Evidence)

**Scenario:** The verification step has not been run yet, but the release manager needs to generate a draft deployment plan and release notes for review. The workflow must not fail but must clearly mark the release notes as a draft.

**Command (CLI):**

```bash
/smartspec_deployment_planner \
  specs/hotfix/bug-fix-101/spec.md \
  --target-env dev \
  --apply
```

**Expected Result:**

1.  The workflow runs in `--mode=normal` (default).
2.  A warning is issued (Check DEP-101) that verification evidence is missing.
3.  `specs/hotfix/bug-fix-101/deployment/release_notes.md` is written, containing a prominent note: "Verification evidence not provided; status may be inaccurate."
4.  `summary.json` shows `"draft_release_notes": true`.
5.  Exit Code: `0`.

### Use Case 3: Generating and Applying CI Workflow (Strict Mode)

**Scenario:** The team needs to generate the final deployment artifacts and automatically create the corresponding GitHub Actions workflow file, ensuring all security checks pass and failing if verification evidence is absent.

**Command (CLI):**

```bash
/smartspec_deployment_planner \
  specs/service/api-gateway/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress/api-run-100/summary.json \
  --apply \
  --strict \
  --write-ci-workflow \
  --ci-template deploy-basic
```

**Expected Result:**

1.  The workflow validates the `spec-id` and ensures the CI output path is safe (Check DEP-201).
2.  The deployment plan and release notes are written to `specs/service/api-gateway/deployment/`.
3.  The CI workflow file `.github/workflows/deploy-api-gateway.yml` is written atomically (Check DEP-301).
4.  Exit Code: `0`.

## Parameters

The following parameters and flags are supported by `/smartspec_deployment_planner`:

| Parameter/Flag | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `spec_md` (positional) | Path | Yes | Path to the primary specification file (e.g., `specs/<category>/<spec-id>/spec.md`). |
| `--tasks` | Path | No | Override path to the tasks file (read-only). |
| `--verify-summary` | Path | No | Path to the strict verification `summary.json` evidence (output of `smartspec_verify_tasks_progress_strict`). |
| `--previous-release-tag` | String | No | Git tag used for generating diff context in release notes. |
| `--target-env` | Enum | No | Influences plan/checklist generation (`dev`, `staging`, `prod`, `other`). |
| `--mode` | Enum | No | Execution mode (`normal` or `strict`). Default is `normal`. |
| `--strict` | Flag | No | Alias for `--mode=strict`. |
| `--ci-provider` | Enum | No | CI system provider (`github-actions`, `other`). Default: `github-actions`. |
| `--ci-template` | String | No | Name of the validated CI template to use for generation. |
| `--write-ci-workflow` | Flag | No | Enables the governed write of the CI workflow file into `.github/workflows/**` (requires `--apply`). |
| `--config` | Path | No | Universal: Path to the SmartSpec configuration file. |
| `--lang` | Enum | No | Universal: Output language (`th`, `en`). |
| `--platform` | Enum | No | Universal: Execution platform context (`cli`, `kilo`, `ci`, `other`). |
| `--apply` | Flag | No | Universal: Enables governed writes of deployment artifacts. |
| `--out`