# /smartspec_release_tagger Manual (v6.0, English)

## Overview

The `/smartspec_release_tagger` workflow (version **6.1.1**) is a **privileged** tool designed to manage software releases by creating Git tags and optionally publishing corresponding releases on platforms like GitHub or GitLab.

**Purpose:** Create a git tag and (optionally) a GitHub/GitLab release using evidence-first inputs.

**Key Features:**

1.  **Evidence-First:** It integrates with other SmartSpec workflows (e.g., `verify-tasks-progress`, `deployment-planner`) by consuming their summary reports to ensure the release is based on verified work.
2.  **Preview-First:** By default, it operates in preview mode, generating a detailed report of planned actions without making changes.
3.  **Safety & Hardening:** It adheres to strict safety protocols, including no-shell execution, path normalization, and mandatory identifier constraints (SemVer, SHA).
4.  **Privileged Operations:** Tagging, pushing, and publishing require the explicit `--apply` flag and, for remote operations, the `--allow-network` flag.

**Security Note:** This workflow executes allowlisted CLIs (`git`, `gh`, `glab`) in **no-shell** mode and is subject to strict governance contracts (see section 0 in the workflow file).

## Usage

The workflow can be executed via the Command Line Interface (CLI) or integrated into other SmartSpec workflows using Kilo Code.

### CLI Usage

The CLI is used for direct execution, typically for previewing or applying the release operation.

#### Preview Mode (Default)

This command generates a plan and report without creating tags or publishing releases. It is mandatory to provide the target version and commit SHA.

**Scenario:** Previewing the creation of tag `v1.2.3` based on evidence summaries.

```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha 7a1b3c8d4e9f0a2b1c3d4e5f6a7b8c9d0e1f2a3b \
  --spec-id feature-deployment \
  --release-notes specs/feature/feature-deployment/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/run-123/summary.json \
  --deployment-summary .spec/reports/deployment-planner/run-456/summary.json \
  --out .spec/reports/release-tagger/preview-v1.2.3 \
  --json
```

**Expected Result:** A `summary.json` and `report.md` are created under the specified `--out` path, detailing the planned `git tag` and potential `gh release create` commands. The `results.tag_created`, `results.tag_pushed`, and `results.release_published` fields in the JSON will be `false`.

#### Apply Mode (Tag and Publish)

This command executes the planned actions. It requires `--apply` and `--allow-network` for remote operations (pushing tags, creating GitHub/GitLab releases).

**Scenario:** Applying the release `v1.2.3` and publishing it to GitHub.

```bash
/smartspec_release_tagger \
  --version v1.2.3 \
  --commit-sha 7a1b3c8d4e9f0a2b1c3d4e5f6a7b8c9d0e1f2a3b \
  --spec-id feature-deployment \
  --release-notes .spec/reports/deployment-planner/run-456/release_notes.preview.md \
  --remote origin \
  --provider github \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger/final-v1.2.3
```

**Expected Result:**
1.  The workflow performs mandatory remote verification (RLT-201).
2.  An annotated Git tag `v1.2.3` is created locally.
3.  The tag is pushed to the `origin` remote.
4.  A GitHub release entry is created using `gh`.
5.  The final `summary.json` will show `results.tag_created: true`, `results.tag_pushed: true`, and `results.release_published: true`, along with the `results.release_url`.
6.  Exit code 0 (Success).

### Kilo Code Usage

Kilo Code allows embedding the workflow execution within a SmartSpec specification, typically used in CI/CD pipelines.

**Scenario:** Integrating release tagging into a deployment specification using strict mode, ensuring all evidence is present before proceeding.

```bash
# .spec/workflows/release_pipeline.kilo

/smartspec_release_tagger.md \
  --version $RELEASE_VERSION \
  --commit-sha $CI_COMMIT_SHA \
  --spec-id $SPEC_ID \
  --release-notes specs/$SPEC_CATEGORY/$SPEC_ID/deployment/release_notes.md \
  --verify-summary .spec/reports/verify-tasks-progress/$VERIFY_RUN_ID/summary.json \
  --deployment-summary .spec/reports/deployment-planner/$DEPLOY_RUN_ID/summary.json \
  --provider gitlab \
  --remote origin \
  --mode strict \
  --allow-network \
  --apply \
  --out .spec/reports/release-tagger/$RELEASE_VERSION \
  --kilocode
```

**Expected Result (Strict Mode):** If any required evidence summary (`--verify-summary` or `--deployment-summary`) is missing, the workflow will block and exit with code 1, preventing the release. If all checks pass, the GitLab tag and release will be created.

## Use Cases

### Use Case 1: Evidence-Gated Release Preview

**Scenario:** A developer wants to confirm that the release process for version `v2.0.0-rc1` is ready, ensuring that the verification and deployment planning steps have successfully completed, but without committing any changes yet.

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| `--version` | `v2.0.0-rc1` | Target version. |
| `--commit-sha` | `f00b4c1d` | Target commit (must be 7-40 hex chars). |
| `--mode` | `strict` | Requires evidence to be present. |
| `--provider` | `github` | Plan to publish to GitHub later. |
| `--verify-summary` | `path/to/verify.json` | Required evidence. |
| `--deployment-summary`| `path/to/deploy.json` | Required evidence. |

**CLI Command:**

```bash
/smartspec_release_tagger \
  --version v2.0.0-rc1 \
  --commit-sha f00b4c1d \
  --mode strict \
  --provider github \
  --verify-summary path/to/verify.json \
  --deployment-summary path/to/deploy.json \
  --out .spec/reports/v2.0.0-rc1-preview
```

**Expected Result:** If `path/to/verify.json` or `path/to/deploy.json` are missing or invalid, the workflow exits with code 1 (Strict-mode blocking issue). If valid, a detailed report is generated showing the planned `git tag` and `gh release create` commands, but no changes are applied.

### Use Case 2: Applying a Git-Only Tag

**Scenario:** The user needs to create a simple, local Git tag (`v3.1.0`) and push it to the remote, without creating a formal release entry on GitHub/GitLab.

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| `--version` | `v3.1.0` | Target version. |
| `--commit-sha` | `a1b2c3d4e5f6` | Target commit. |
| `--provider` | `git-only` | Prevents calls to `gh` or `glab`. |
| `--remote` | `upstream` | Push to the `upstream` remote. |
| `--allow-network` | (Set) | Required for pushing the tag. |
| `--apply` | (Set) | Execute the operation. |

**Kilo Code Example:**

```bash
/smartspec_release_tagger.md \
  --version v3.1.0 \
  --commit-sha a1b2c3d4e5f6 \
  --provider git-only \
  --remote upstream \
  --allow-network \
  --apply \
  --kilocode
```

**Expected Result:** The workflow executes `git tag v3.1.0 a1b2c3d4e5f6` and `git push upstream v3.