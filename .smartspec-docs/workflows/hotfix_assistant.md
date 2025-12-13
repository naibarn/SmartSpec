# /smartspec_hotfix_assistant Manual (v6.0, English)

## Overview

The `/smartspec_hotfix_assistant` is a highly privileged workflow designed to **orchestrate a safe and evidence-gated hotfix process** within a SmartSpec-governed repository.

**Purpose:** To automate the sequence of operations required for a production hotfix: branching from a stable release tag, cherry-picking approved fixes, running mandatory tests, merging, and tagging the new release.

**Version:** 6.1.1

**Key Features:**
1.  **Preview-First:** Generates a detailed step-by-step plan (`plan.md`) and a deterministic rollback plan (`rollback_plan.md`) without executing any VCS operation unless the `--apply` flag is used.
2.  **Evidence-First Gating:** Integrates with other SmartSpec workflows (e.g., `verify-tasks-progress`, `deployment-planner`) by requiring their summary outputs as evidence before proceeding, especially in `--strict` mode.
3.  **Security Hardening:** Executes only allowlisted `git` commands without a shell, enforces strict path and identifier constraints, and requires explicit network permission (`--allow-network`) for remote operations.
4.  **Reports-Only:** All outputs are restricted to the `.spec/reports/hotfix-assistant/**` directory.

---

## Usage

### CLI Usage

The workflow is invoked via the command-line interface.

**Preview Mode (Safe Simulation):**
Used to generate the plan and check all preflight and evidence gates without modifying the repository.

```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <approved_commit_sha> \
  --verify-summary .spec/reports/verify-tasks-progress/run-123/summary.json \
  --deployment-summary .spec/reports/deployment-planner/run-456/summary.json
```

**Apply Mode (Execution):**
Used to execute the hotfix operations (branching, cherry-picking, testing, merging, tagging). Requires `--apply` and usually `--allow-network` for push/fetch operations.

```bash
/smartspec_hotfix_assistant \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <approved_commit_sha> \
  --remote origin \
  --allow-network \
  --require-tests-pass \
  --verify-summary <path_to_evidence> \
  --deployment-summary <path_to_evidence> \
  --apply
```

### Kilo Code Usage

When integrating the workflow into a larger SmartSpec pipeline (e.g., in a CI/CD environment), use the Kilo Code invocation format.

```bash
/smartspec_hotfix_assistant.md \
  --base-tag v1.2.3 \
  --hotfix-version v1.2.4 \
  --commit-sha <approved_commit_sha> \
  --remote origin \
  --main-branch main \
  --allow-network \
  --require-tests-pass \
  --verify-summary .spec/reports/verify-tasks-progress/run-123/summary.json \
  --deployment-summary .spec/reports/deployment-planner/run-456/summary.json \
  --apply \
  --out .spec/reports/hotfix-assistant \
  --json \
  --kilocode
```

---

## Use Cases

### Use Case 1: Previewing a Critical Hotfix (Strict Mode)

**Scenario:** A critical bug fix (commit `c0ffee1`) needs to be applied to the stable release `v2.5.0`. The team requires a full plan and verification that all evidence (task verification and deployment planning) is present before execution.

**Goal:** Generate the hotfix plan and verify evidence without making any repository changes.

**Command (CLI):**

```bash
/smartspec_hotfix_assistant \
  --base-tag v2.5.0 \
  --hotfix-version v2.5.1 \
  --commit-sha c0ffee1c0ffee1c0ffee1c0ffee1c0ffee1 \
  --remote upstream \
  --strict \
  --verify-summary .spec/reports/verify-tasks-progress/run-999/summary.json \
  --deployment-summary .spec/reports/deployment-planner/run-888/summary.json \
  --out .spec/reports/hotfix-preview-v251
```

**Expected Result:**
The workflow runs checks (HFX-101, HFX-102) to ensure the summary files exist. Since `--apply` is missing, it generates:
1.  `./spec/reports/hotfix-preview-v251/plan.md`: Details the creation of branch `hotfix/v2.5.1`, the cherry-pick, the test invocation, the merge, and the tagging process.
2.  `./spec/reports/hotfix-preview-v251/rollback_plan.md`: Instructions on how to clean up the local branch and undo the merge (if applicable).
3.  Exit code `0`.

### Use Case 2: Executing a Hotfix with Mandatory Testing and Publishing

**Scenario:** The plan from UC1 is approved. The hotfix must be applied, tests must pass, and the resulting tag must be pushed to the remote `origin`.

**Goal:** Execute the full hotfix sequence, including network operations and quality gates.

**Command (Kilo Code):**

```bash
/smartspec_hotfix_assistant.md \
  --base-tag v2.5.0 \
  --hotfix-version v2.5.1 \
  --commit-sha c0ffee1c0ffee1c0ffee1c0ffee1c0ffee1 \
  --remote origin \
  --main-branch main \
  --allow-network \
  --require-tests-pass \
  --verify-summary .spec/reports/verify-tasks-progress/run-999/summary.json \
  --deployment-summary .spec/reports/deployment-planner/run-888/summary.json \
  --test-script ci-hotfix-tests \
  --apply \
  --kilocode
```

**Expected Result:**
1.  **VCS Operations:** Branch `hotfix/v2.5.1` is created, `c0ffee1` is cherry-picked.
2.  **Testing:** `/smartspec_test_suite_runner` is invoked with `--test-script ci-hotfix-tests`. If tests fail, the workflow blocks and exits with code `1` (HFX-302).
3.  **Merge & Push:** The hotfix branch is merged into `main`, and the changes are pushed to `origin` (HFX-202 satisfied by `--allow-network`).
4.  **Tagging:** `/smartspec_release_tagger` is called to create and publish tag `v2.5.1`.
5.  `summary.json` reflects `tests_passed: true`, `merged_to_main: true`, and `tagged: true`.
6.  Exit code `0`.

---

## Parameters

The following parameters (inputs and flags) control the workflow execution.

### Required Parameters

| Parameter | Description | Constraints |
| :--- | :--- | :--- |
| `--base-tag <tag>` | Existing release tag to branch the hotfix from. | Must match SemVer pattern. |
| `--hotfix-version <version>` | The new version tag to be created. | Must match safe SemVer pattern. |
| `--commit-sha <sha>` | The specific commit hash to cherry-pick onto the hotfix branch. | Must be a valid SHA (7 to 40 hex characters). |

### Recommended (Evidence) Parameters

These parameters link to outputs from preceding SmartSpec workflows, acting as evidence gates.

| Parameter | Description | Usage |
| :--- | :--- | :--- |
| `--verify-summary <path>` | Path to the strict verification summary (e.g., task progress). | Required in `--strict` mode (HFX-101). |
| `--deployment-summary <path>` | Path to the deployment planner summary. | Required in `--strict` mode (HFX-102). |
| `--release-notes <path>` | Path to the release notes markdown file. | Passed to the `release_tagger` upon successful hotfix. |

### Optional Parameters

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `--remote <name>` | The name of the Git remote to use for fetch/push operations. | `origin` |
| `--main-branch <name>` | The name of the main branch to merge the hotfix into. | `main` |
| `--