---
name: /smartspec_incident_response
version: 1.0.0
role: production-ops
category: core
write_guard: ALLOW-WRITE
purpose: Manage production incidents from triage to resolution and post-mortem.
description: Manage production incidents from triage to resolution and post-mortem.
workflow: /smartspec_incident_response
---

# smartspec_incident_response

> **Canonical path:** `.smartspec/workflows/smartspec_incident_response.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** production-ops

## Purpose

This workflow provides a structured, repeatable process for managing production incidents, from initial alert to final post-mortem. It ensures that incidents are resolved quickly, stakeholders are kept informed, and lessons are learned to prevent recurrence.

This workflow MUST:

- Integrate with alerting systems (e.g., `smartspec_production_monitor`).
- Provide a clear process for incident triage, assignment, and escalation.
- Automate communication to stakeholders.
- Facilitate root cause analysis (RCA).
- Generate post-mortem reports to feed back into the development lifecycle.

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

- `.spec/reports/incidents/**`
- `.spec/reports/post-mortems/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`

### `--apply` behavior

- This workflow does not have an `--apply` behavior as it does not write to governed paths.

---

## Threat model (minimum)

This workflow must defend against:

- **PII Leakage:** All incident data and communications must be sanitized to remove personally identifiable information.
- **Unauthorized Actions:** Triggering other workflows (e.g., `smartspec_rollback`) must require proper authorization and auditing.
- **Data Loss:** Incident reports and post-mortems must be stored durably.

---

## Invocation

```bash
/smartspec_incident_response \
  --alert-payload <json-payload>
```

---

## Inputs

- `--alert-payload <json-payload>`: The JSON payload of the alert that triggered the incident.

---

## Flags (Universal)

- `--help`: Show help message.
- `--version`: Show version.
- `--verbose`: Enable verbose logging.
- `--quiet`: Suppress all output except errors.

---

## Behavior (Vibe Coding)

### Phase 1: Incident Triage

1.  **Receive Alert:** Receive a structured alert from an upstream system (e.g., `smartspec_production_monitor`).
2.  **Create Incident:** Create a new incident record with a unique ID.
3.  **Assess Severity:** Determine the severity level (SEV-1 to SEV-4) based on the impact described in the alert.
4.  **Assign Commander:** Assign an Incident Commander to lead the response.
5.  **Notify Stakeholders:** Send an initial notification to the relevant stakeholders (e.g., via Slack, email).

### Phase 2: Investigation & Mitigation

1.  **Assemble Team:** The Incident Commander assembles a team of engineers to investigate.
2.  **Investigate:** The team works to identify the root cause of the incident.
3.  **Propose Mitigation:** The team proposes a plan to mitigate the impact (e.g., a hotfix, a rollback, a configuration change).
4.  **Execute Mitigation:** The team executes the mitigation plan. This may involve triggering other workflows like `smartspec_hotfix_assistant` or `smartspec_rollback`.

### Phase 3: Resolution

1.  **Verify Fix:** The team verifies that the mitigation has resolved the issue and the service has returned to a healthy state.
2.  **Update Status:** The Incident Commander updates the incident status to "Resolved".
3.  **Send Final Communication:** A final communication is sent to stakeholders.

### Phase 4: Post-Mortem

1.  **Schedule Post-Mortem Meeting:** A post-mortem meeting is scheduled.
2.  **Generate Post-Mortem Report:** The workflow generates a draft post-mortem report containing:
    -   A timeline of the incident.
    -   The root cause analysis.
    -   The mitigation steps taken.
    -   Action items to prevent recurrence.
3.  **Finalize Report:** The team finalizes the report in the post-mortem meeting.
4.  **Feed Back:** The action items from the post-mortem are fed into the `smartspec_feedback_aggregator` to create new specs or tasks.

---

## Output Structure

- **Incident Reports:** Saved in `.spec/reports/incidents/`.
- **Post-Mortems:** Saved in `.spec/reports/post-mortems/`.
- **Action Items:** Sent to `smartspec_feedback_aggregator`.

---

## `summary.json` Schema

```json
{
  "workflow": "smartspec_incident_response",
  "version": "1.0.0",
  "run_id": "string",
  "incident_id": "string",
  "severity": "SEV-1|SEV-2|SEV-3|SEV-4",
  "status": "open|investigating|mitigating|resolved|closed",
  "root_cause_identified": false,
  "action_items_created": 0
}
```
