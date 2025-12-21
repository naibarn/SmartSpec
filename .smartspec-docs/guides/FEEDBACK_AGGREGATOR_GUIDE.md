# Guide: smartspec_feedback_aggregator

## 📚 Overview

`/smartspec_feedback_aggregator` is the engine of **continuous improvement** in the SmartSpec ecosystem. It closes the loop between production and development by aggregating feedback from multiple sources and turning it into actionable insights.

**Key Features:**
- ✅ Collects data from production monitoring, incidents, and user feedback channels.
- ✅ Uses NLP to analyze and categorize feedback.
- ✅ Identifies trends and recurring issues.
- ✅ Generates suggestions for new specs, tasks, or refactors.
- ✅ Creates a feedback dashboard for visualization.

---

## 🎯 Basic Usage

This workflow is typically run on a schedule (e.g., daily) as a background process.

### Running the Aggregator

```bash
/smartspec_feedback_aggregator --run-once
```

**Behavior:**
1.  Polls all configured feedback sources.
2.  Processes new feedback items.
3.  Updates the feedback dashboard.
4.  Generates new suggestions.
5.  Sends a summary report to stakeholders.

---

## ⚙️ The Feedback Loop

This workflow creates a powerful feedback loop:

1.  **Production Monitoring:** `smartspec_production_monitor` detects a performance degradation and creates a report.
2.  **Feedback Aggregator:** The aggregator processes the report and identifies a trend: "p99 latency for `spec-core-001` has increased by 20% over the last 7 days."
3.  **Suggestion Generation:** The aggregator generates a suggestion:
    -   **Type:** Performance Investigation
    -   **Title:** Investigate p99 latency regression in `spec-core-001`
    -   **Action:** Create a new spec for a performance audit.
4.  **New Spec:** A developer uses the suggestion to create a new spec with `smartspec_generate_spec_from_prompt`.
5.  **Development:** The new spec is planned, tasked, and implemented.
6.  **Deployment:** The fix is deployed to production.
7.  **Monitoring:** `smartspec_production_monitor` confirms that latency has returned to normal.

**The loop is complete!**

---

## 💡 Feedback Sources

This workflow can be configured to pull data from:

-   **SmartSpec Reports:**
    -   `.spec/reports/production-monitoring/`
    -   `.spec/reports/post-mortems/`
-   **User Feedback Tools:**
    -   Zendesk
    -   Intercom
    -   Jira
-   **Version Control:**
    -   GitHub Issues
    -   GitLab Issues

---

## 🚩 Flags

- `--run-once`: **(Required)** Run the aggregation process once and exit.
- `--source <name>`: Run the aggregation for a specific source only.
- `--since <date>`: Process feedback items created since a specific date.
