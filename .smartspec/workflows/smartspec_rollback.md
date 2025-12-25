---
name: /smartspec_rollback
version: 1.0.0
role: production-ops
category: core
write_guard: ALLOW-WRITE
purpose: Safely roll back a failed deployment to a previous stable version.
description: Safely roll back a failed deployment to a previous stable version.
workflow: /smartspec_rollback
---

# smartspec_rollback

> **Canonical path:** `.smartspec/workflows/smartspec_rollback.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** production-ops

## Purpose

This workflow provides a safe, automated, and verifiable process for rolling back a failed deployment to a previously known stable version. It is a critical component of deployment safety and incident response.

This workflow MUST:

- Integrate with the deployment system and `smartspec_deployment_planner`.
- Be triggered automatically by a failed quality gate or manually during an incident.
- Generate a clear rollback plan.
- Execute the rollback.
- Verify that the rollback was successful and the system is stable.
- Generate a report for audit purposes.

---

## File Locations (Important for AI Agents)

**All SmartSpec configuration and registry files are located in the `.spec/` folder:**
- **Config:** `.spec/smartspec.config.yaml`
- **Spec Index:** `.spec/SPEC_INDEX.json`
- **Registry:** `.spec/registry/`
- **Reports:** `.spec/reports/`

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v7)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs):

- `.spec/reports/rollbacks/**`

Governed writes (**requires** `--apply`):

- Production deployment configuration

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`

### `--apply` behavior

- Without `--apply`: Generate a rollback plan and save it to `.spec/reports/rollbacks/`.
- With `--apply`: Execute the rollback plan.

---

## Threat model (minimum)

This workflow must defend against:

- **Data Loss:** The rollback plan must include checks to prevent data loss.
- **Further Instability:** The rollback must be verified to ensure it doesn't cause more problems.
- **Unauthorized Rollbacks:** All rollback actions must be audited, and high-risk rollbacks must require manual approval.

---

## Invocation

```bash
/smartspec_rollback \
  --failed-deployment-id <id> \
  [--target-version <version>] \
  [--auto-approve]
```

---

## Inputs

- `--failed-deployment-id <id>`: The ID of the deployment that failed.
- `--target-version <version>`: (Optional) The specific version to roll back to. Defaults to the last known good version.
- `--auto-approve`: (Optional) Skip manual approval for high-risk rollbacks. Use with caution.

---

## Flags (Universal)

- `--help`: Show help message.
- `--version`: Show version.
- `--verbose`: Enable verbose logging.
- `--quiet`: Suppress all output except errors.

---

## Behavior (Vibe Coding)

### Phase 1: Initialization

1.  **Receive Trigger:** Receive a trigger from a failed deployment, a failed quality gate, or a manual invocation from `smartspec_incident_response`.
2.  **Identify Target Version:** Determine the target version to roll back to (usually the last known good version).
3.  **Load Deployment Plan:** Load the deployment plan for the failed version to understand what was changed.

### Phase 2: Rollback Planning

1.  **Generate Rollback Plan:** Create a step-by-step plan to revert the changes made in the failed deployment. This may include:
    -   Switching traffic back to the old version (e.g., in a blue/green deployment).
    -   Reverting database schema changes (if possible).
    -   Reverting configuration changes.
2.  **Run Safety Checks:** Analyze the rollback plan for potential risks (e.g., data loss, further instability).
3.  **Require Manual Approval:** For high-risk rollbacks, require manual approval from the Incident Commander before proceeding.

### Phase 3: Execution

1.  **Execute Plan:** Execute the steps in the rollback plan.
2.  **Monitor Progress:** Continuously monitor the system as the rollback proceeds.

### Phase 4: Verification

1.  **Run Verification Tests:** Execute a suite of verification tests to ensure that the system is stable and functioning correctly on the rolled-back version.
2.  **Check Health Metrics:** Query `smartspec_production_monitor` to confirm that health metrics have returned to normal.

### Phase 5: Reporting

1.  **Generate Rollback Report:** Create a report detailing the rollback process, including the reason for the rollback, the steps taken, and the verification results.
2.  **Save Report:** Save the report in `.spec/reports/rollbacks/`.
3.  **Notify Stakeholders:** Notify stakeholders that the rollback is complete.

---

## Output Structure

- **Rollback Reports:** Saved in `.spec/reports/rollbacks/`.

---

## `summary.json` Schema

```json
{
  "workflow": "smartspec_rollback",
  "version": "1.0.0",
  "run_id": "string",
  "rollback_id": "string",
  "status": "success|failure",
  "reason": "string",
  "from_version": "string",
  "to_version": "string"
}
```
