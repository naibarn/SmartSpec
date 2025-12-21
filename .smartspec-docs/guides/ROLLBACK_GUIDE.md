# Guide: smartspec_rollback

## 📚 Overview

`/smartspec_rollback` is a critical safety workflow for **production operations**. It provides a safe, automated way to revert a failed deployment to a previously known stable version.

**Key Features:**
- ✅ Integrates with deployment systems.
- ✅ Can be triggered automatically or manually.
- ✅ Generates a clear, verifiable rollback plan.
- ✅ Performs safety checks before execution.
- ✅ Requires manual approval for high-risk rollbacks.

---

## 🎯 Basic Usage

### 1. Triggering a Rollback During an Incident

This is the most common use case. It is typically run by an engineer in an incident response channel.

```bash
/smartspec_rollback --failed-deployment-id deploy-12345
```

**Behavior:**
1.  Identifies the last known good version (e.g., `v1.2.0`).
2.  Generates a rollback plan.
3.  **Asks for manual approval** in the incident channel.
4.  Executes the rollback after approval.
5.  Verifies the system is stable.
6.  Posts a report to the incident channel.

### 2. Automatic Rollback from a Quality Gate

This workflow can be integrated into a CI/CD pipeline.

```bash
# In your CI/CD script
/smartspec_quality_gate --deployment-id deploy-12345
if [ $? -ne 0 ]; then
  /smartspec_rollback --failed-deployment-id deploy-12345 --auto-approve
fi
```

**Behavior:**
- If the quality gate fails, the rollback is triggered automatically.
- `--auto-approve` skips the manual approval step, allowing for faster, fully automated rollbacks in CI/CD.

---

## ⚙️ The Rollback Plan

Before executing, the workflow generates a plan that looks like this:

```markdown
# Rollback Plan: deploy-12345

**Reason:** Quality gate failed (p99 latency > 200ms)
**From Version:** `v1.2.1`
**To Version:** `v1.2.0`

## ⚠️ Safety Checks

- [✅] No breaking database schema changes detected.
- [✅] No data loss risk identified.

## Steps

1.  Switch production traffic from `v1.2.1` to `v1.2.0`.
2.  Scale down `v1.2.1` instances to 0.
3.  Run verification tests on `v1.2.0`.

**Approve this plan? (yes/no)**
```

---

## 🚩 Flags

- `--failed-deployment-id <id>`: **(Required)** The ID of the deployment that failed.
- `--target-version <version>`: Manually specify the version to roll back to.
- `--auto-approve`: Skip manual approval. **Use with caution.**
- `--dry-run`: Generate the rollback plan but do not execute it.
