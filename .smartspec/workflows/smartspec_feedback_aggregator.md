---
name: /smartspec_feedback_aggregator
version: 1.0.0
role: continuous-improvement
category: core
write_guard: ALLOW-WRITE
purpose: Aggregate feedback from multiple sources to drive continuous improvement.
description: Aggregate feedback from multiple sources to drive continuous improvement.
workflow: /smartspec_feedback_aggregator
---

# smartspec_feedback_aggregator

> **Canonical path:** `.smartspec/workflows/smartspec_feedback_aggregator.md`  
> **Version:** 1.0.0  
> **Status:** Production Ready  
> **Category:** continuous-improvement

## Purpose

This workflow closes the loop between production and development by aggregating feedback from multiple sources and translating it into actionable insights. It is the engine of continuous improvement in the SmartSpec ecosystem.

This workflow MUST:

-   Collect data from various sources: production monitoring, incident post-mortems, user feedback channels, and manual inputs.
-   Analyze and categorize the feedback.
-   Identify trends and recurring issues.
-   Generate suggestions for new specs, spec updates, or technical debt tasks.
-   Create a feedback dashboard for easy visualization.

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

- `.spec/reports/feedback/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`

### `--apply` behavior

- This workflow does not have an `--apply` behavior as it does not write to governed paths.

---

## Threat model (minimum)

This workflow must defend against:

- **User Privacy:** All user feedback must be handled with respect for privacy, and PII must be redacted.
- **Data Integrity:** Ensure that feedback data is not tampered with.
- **Unauthorized Access:** Access to feedback sources must be properly authenticated and authorized.

---

## Invocation

```bash
/smartspec_feedback_aggregator \
  --run-once
```

---

## Inputs

-   `--run-once`: Run the aggregation process once and exit.

---

## Flags (Universal)

- `--help`: Show help message.
- `--version`: Show version.
- `--verbose`: Enable verbose logging.
- `--quiet`: Suppress all output except errors.

---

## Behavior (Vibe Coding)

### Phase 1: Data Collection

1.  **Poll Sources:** On a schedule, poll all configured feedback sources:
    -   `.spec/reports/production-monitoring/` for performance reports.
    -   `.spec/reports/post-mortems/` for action items from incidents.
    -   User feedback channels (e.g., via API integration with Zendesk, Intercom, etc.).
2.  **Normalize Data:** Convert all incoming data into a standardized feedback format.

### Phase 2: Analysis & Categorization

1.  **Categorize Feedback:** Classify each feedback item (e.g., bug report, feature request, performance issue, usability problem).
2.  **Identify Trends:** Use NLP and statistical analysis to identify trends, such as a spike in bug reports after a recent deployment or a common feature request.
3.  **Prioritize:** Score and prioritize feedback items based on their impact and frequency.

### Phase 3: Suggestion Generation

1.  **Generate Suggestions:** Based on the analysis, generate concrete suggestions:
    -   **For new features:** Create a draft prompt for `smartspec_generate_spec_from_prompt`.
    -   **For bugs or performance issues:** Create a draft spec update or a new task for the backlog.
    -   **For usability problems:** Suggest a UI/UX audit or a new design spec.
2.  **Link to Evidence:** Each suggestion MUST be linked back to the raw feedback that generated it.

### Phase 4: Reporting

1.  **Update Feedback Dashboard:** Update a central dashboard that visualizes feedback trends and the status of suggestions.
2.  **Send Summary Report:** Send a summary report to stakeholders.

---

## Output Structure

-   **Feedback Dashboard:** A web-based dashboard for visualizing feedback.
-   **Suggestions:** Saved in `.spec/reports/feedback/suggestions/`.
-   **Summary Reports:** Sent to stakeholders.

---

## `summary.json` Schema

```json
{
  "workflow": "smartspec_feedback_aggregator",
  "version": "1.0.0",
  "run_id": "string",
  "feedback_items_processed": 0,
  "suggestions_generated": 0,
  "trends_identified": []
}
```
