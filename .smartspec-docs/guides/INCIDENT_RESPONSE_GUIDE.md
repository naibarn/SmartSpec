# Guide: smartspec_incident_response

## 📚 Overview

`/smartspec_incident_response` is a critical workflow for **production operations**. It provides a structured, repeatable process for managing production incidents, ensuring they are resolved quickly and that lessons are learned.

**Key Features:**
- ✅ Integrates with alerting systems like `smartspec_production_monitor`.
- ✅ Provides a clear SEV-based triage process.
- ✅ Automates stakeholder communication.
- ✅ Facilitates blameless post-mortems.
- ✅ Feeds action items back into the development loop.

---

## 🎯 Basic Usage

This workflow is typically **triggered automatically** by another system, not run manually.

### Triggering an Incident

```bash
/smartspec_incident_response --alert-payload '{
  "source": "production_monitor",
  "spec_id": "spec-core-001-authentication",
  "metric": "p99_latency",
  "value": 350,
  "slo": 200,
  "severity": "SEV-2"
}'
```

**Behavior:**
1.  Creates a new incident record.
2.  Assigns an Incident Commander.
3.  Creates a dedicated Slack channel for the incident.
4.  Sends an initial notification to stakeholders.

---

## ⚙️ Incident Lifecycle

### 1. Triage
- An alert is received.
- Severity is assessed (SEV-1 to SEV-4).
- An Incident Commander is assigned.

### 2. Investigation & Mitigation
- The team investigates the root cause.
- A mitigation plan is proposed (e.g., rollback, hotfix).
- The plan is executed. This may trigger other workflows:
  - `/smartspec_rollback --failed-deployment-id <id>`
  - `/smartspec_hotfix_assistant --incident-id <id>`

### 3. Resolution
- The fix is verified.
- The incident is marked as "Resolved".
- A final communication is sent.

### 4. Post-Mortem
- A blameless post-mortem is conducted.
- A report is generated with a timeline, RCA, and action items.
- Action items are sent to `/smartspec_feedback_aggregator` to create new tasks or specs.

---

## 💡 Key Concepts

- **Incident Commander:** The single person responsible for leading the incident response.
- **Blameless Post-Mortem:** The focus is on learning and improving the system, not on blaming individuals.
- **Action Items:** Concrete tasks that are created to prevent the incident from recurring.

---

## 🚩 Flags

- `--alert-payload <json>`: **(Required)** The JSON payload of the alert.
- `--manual-incident`: Create a manual incident without an alert payload.
- `--severity <SEV-1|SEV-2|SEV-3|SEV-4>`: Manually set the severity level.
