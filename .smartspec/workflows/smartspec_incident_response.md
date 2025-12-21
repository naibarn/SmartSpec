---
description: Manage production incidents from triage to resolution and post-mortem.
version: 1.0.0
workflow: /smartspec_incident_response
---

# smartspec_incident_response

> **Canonical path:** `.smartspec/workflows/smartspec_incident_response.md`  
> **Version:** 1.0.0  
> **Status:** New  
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

## Governance contract

- This workflow MUST have the ability to trigger other workflows (e.g., `smartspec_rollback`).
- All incident data MUST be stored securely.
- Post-mortem reports MUST be blameless.

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

## Output

- **Incident Reports:** Saved in `.spec/reports/incidents/`.
- **Post-Mortems:** Saved in `.spec/reports/post-mortems/`.
- **Action Items:** Sent to `smartspec_feedback_aggregator`.
