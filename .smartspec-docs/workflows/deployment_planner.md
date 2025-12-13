_# SmartSpec Workflow: Deployment Planner

**Workflow:** `/smartspec_deployment_planner`  
**Version:** 6.1.1

## 1. Overview

The Deployment Planner is a release management workflow that automates the creation of key deployment artifacts. It helps bridge the gap between development and operations by generating a clear, evidence-based plan for releasing a new version of your software.

This is a **preview-first** workflow. It generates reports by default and requires explicit flags to write governed artifacts like release notes or CI pipeline files.

## 2. Key Features

- **Deployment Plan Generation:** Creates a detailed `deployment_plan.md` with checklists for pre-flight, deployment, and post-flight verification.
- **Evidence-First Release Notes:** Generates `release_notes.md` based on the proven, completed work from a `/smartspec_verify_tasks_progress_strict` report, not just checked boxes in `tasks.md`.
- **CI/CD Pipeline Patching:** Can generate a draft GitHub Actions workflow file (`deploy-<spec-id>.yml`) to automate the deployment.
- **Environment Targeting:** Tailors the deployment plan based on the target environment (e.g., dev, staging, prod).

## 3. How It Works

1.  **Gathers Evidence:** Takes a `spec.md` and, most importantly, a `summary.json` from a strict verification run as input.
2.  **Analyzes Scope:** Determines the changes and completed tasks from the verification report.
3.  **Generates Artifacts:** Creates the deployment plan, release notes, and an optional CI workflow patch.
4.  **Previews Changes:** By default, it outputs a report showing what *would* be written.
5.  **Applies Changes (Optional):** With `--apply`, it writes the generated artifacts to the appropriate directories (`specs/**/deployment/` or `.github/workflows/`).

## 4. Usage

### Generate a Deployment Plan (Preview)

```bash
/smartspec_deployment_planner \
  specs/my-feature/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress-strict/run-123/summary.json \
  --target-env staging
```

### Apply and Generate a CI Workflow

```bash
/smartspec_deployment_planner \
  specs/my-feature/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress-strict/run-123/summary.json \
  --target-env prod \
  --apply \
  --write-ci-workflow
```

## 5. Input and Flags

- **`spec_md` (Required):** Path to the `spec.md` file.
- **`--verify-summary <path>` (Required for strict mode):** Path to the `summary.json` from a `/smartspec_verify_tasks_progress_strict` run.
- **`--target-env <name>` (Optional):** The target environment (e.g., `dev`, `staging`, `prod`).
- **`--apply` (Optional):** Applies the changes and writes the governed artifacts.
- **`--write-ci-workflow` (Optional):** Enables writing the CI workflow file (requires `--apply`).

## 6. Output: Deployment Artifacts

-   **Report:** A preview of all changes in `.spec/reports/deployment-planner/`.
-   **Deployment Plan:** `specs/<spec-id>/deployment/plan.md`.
-   **Release Notes:** `specs/<spec-id>/deployment/release_notes.md`.
-   **CI Workflow:** `.github/workflows/deploy-<spec-id>.yml`.

## 7. Use Cases

- **Automate Release Notes:** Generate accurate, evidence-based release notes for stakeholders.
- **Standardize Deployments:** Create consistent, repeatable deployment plans for every release.
- **Bootstrap CI/CD:** Quickly generate a starting GitHub Actions workflow for a new service or feature.
_
