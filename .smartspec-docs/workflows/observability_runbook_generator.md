---
manual_name: /smartspec_observability_runbook_generator Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_observability_runbook_generator
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, dev, on-call)
---

# /smartspec_observability_runbook_generator Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_observability_runbook_generator v5.6.2`

The workflow helps you:

> "Generate **observability runbooks** aligned with spec / SLO / alerts /
> dashboards so on-call and developers can handle incidents in a more
> structured way."

Key properties:

- Role: **design / planning / runbook-generation**
- `write_guard: NO-WRITE`
  - does **not** change `spec.md`, `tasks.md`, configs, CI, or observability
    backends
  - only produces **runbook suggestions** under
    `.spec/suggestions/smartspec_observability_runbook_generator/`
- Reads (read-only):
  - SPEC_INDEX, specs, SLO/NFR, service registries
  - alert rules, dashboard definitions, log/trace configs, metrics configs
- Designed to work alongside:
  - `/smartspec_release_readiness`
  - `/smartspec_ci_quality_gate`

In short:

- This is a **runbook generator**, not an automation tool.
- It helps translate existing knowledge (SLOs, alerts, dashboards, logs,
  traces) into human-readable runbooks.

---

## 2. What’s New in v5.6

### 2.1 Kilo Orchestrator-per-task support

- When `--kilocode` is used under Kilo:
  - For each top-level task (each spec-id/service), Orchestrator is used
    to decompose subtasks before generating that runbook.
  - Default under Kilo is **subtasks ON** (unless `--nosubtasks` is given).

### 2.2 Safety-mode for runbook generation

- `--safety-mode=normal` (default):
  - may include exploratory suggestions.
  - clearly marks which steps are “standard” vs “optional”.
- `--safety-mode=strict` / `--strict`:
  - every `critical` / `high` SLO or critical section must either:
    - have at least one scenario + troubleshooting path, or
    - be explicitly marked as an `observability_gap`.
  - must **not** propose unsafe operations (e.g., ad-hoc DB writes) as
    default actions.

### 2.3 Sensitive data rules (secrets & PII)

- Runbooks MUST NOT reproduce:
  - secrets, tokens, passwords, private keys
  - sensitive PII (e.g., full card numbers, national IDs)
- Runbooks MAY state:
  - that such data appears in logs/traces, in which files/indices/patterns,
    but without copying raw values.

### 2.4 Multi-repo / multi-registry aware

- Uses `--repos-config`, `--workspace-roots`, `--registry-dir`,
  `--registry-roots` to understand service topology and ownership.
- Cross-service scenarios identify all services involved and clarify which
  team owns which part.

---

## 3. Backward Compatibility Notes

- This v5.6 manual targets `/smartspec_observability_runbook_generator`
  starting from **v5.6.2** (5.6.x series).
- No existing flags or behaviors are removed.
- `--strict` remains an alias for `--safety-mode=strict`.
- Canonical folders and multi-repo semantics match other SmartSpec
  workflows (e.g., release readiness, CI quality gate).

---

## 4. Core Concepts

### 4.1 Observability runbook

A runbook is a document that describes:

- symptoms (alerts, SLO breaches, customer-visible issues)
- where to look (dashboards, metrics, logs, traces)
- how to diagnose (step-by-step checks)
- how to mitigate/rollback (within existing change processes)
- post-incident verification and follow-ups

The generator produces **proposed** runbooks that teams can review and
adapt into official operational docs.

### 4.2 Mapping SLO/NFR → runbook

Conceptual flow:

1. Read SLOs/NFRs from specs, SLO registry, and policies.
2. Identify critical paths / critical sections.
3. Map them to observability configs (alerts, dashboards, logs, traces).
4. Derive incident scenarios and troubleshooting flows.
5. Serialize as runbook content.

### 4.3 Observability gaps

- When SLOs / critical paths lack appropriate alerts/dashboards/logs/traces,
  the generator:
  - adds an `observability_gap` section.
  - describes the gap and, optionally, suggests what observability elements
    are missing.
- Gaps are **proposals**, not existing behavior.

---

## 5. Quick Start Examples

### 5.1 Generate a runbook for a single service

```bash
smartspec_observability_runbook_generator \
  --spec-ids=checkout_api \
  --runbook-label=checkout-observability \
  --alert-config-paths=".config/alerts/checkout/*.yml" \
  --dashboard-config-paths=".config/dashboards/checkout/*.json" \
  --log-config-paths=".config/logging/checkout/*.yml" \
  --trace-config-paths=".config/tracing/checkout/*.yml" \
  --runbook-format=md \
  --stdout-summary
```

Result:

- runbook at:
  `.spec/suggestions/smartspec_observability_runbook_generator/<timestamp>_checkout-observability.md`

### 5.2 Strict mode for a core payments service

```bash
smartspec_observability_runbook_generator \
  --spec-ids=core_payments \
  --runbook-label=core-payments-observability \
  --alert-config-paths=".config/alerts/core_payments/*.yml" \
  --dashboard-config-paths=".config/dashboards/core_payments/*.json" \
  --trace-config-paths=".config/tracing/core_payments/*.yml" \
  --safety-mode=strict \
  --runbook-format=json \
  --stdout-summary
```

In strict mode:

- all critical/high SLOs must have runbook coverage or be called out as
  `observability_gap`.
- dangerous steps (e.g., direct DB edits) are not proposed as defaults.

### 5.3 Multiple services with dependencies

```bash
smartspec_observability_runbook_generator \
  --spec-ids=search_api,ranking_service \
  --include-dependencies \
  --runbook-label=search-stack-observability \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --runbook-format=md
```

- Runbooks cover search_api, ranking_service and key dependencies.

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--runbook-label=<string>`

### 6.2 Environment

- `--target-envs=dev,staging,prod,...`

### 6.3 Observability config paths

- `--alert-config-paths="..."`
- `--dashboard-config-paths="..."`
- `--log-config-paths="..."`
- `--trace-config-paths="..."`
- `--runtime-metrics-paths="..."`

### 6.4 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (or `--strict`)

### 6.5 Output & KiloCode

- `--runbook-format=md|json`
- `--runbook-dir=.spec/suggestions/smartspec_observability_runbook_generator/`
- `--stdout-summary`
- `--kilocode`, `--nosubtasks`

---

## 7. Reading Generated Runbooks

Typical content layout:

- Metadata:
  - service/spec-id
  - owner/team
  - relevant environments
- Scenario list:
  - e.g., `slo_latency_breach`, `5xx_spike`, `cpu_saturation`, `db_latency`,
    `dependency_down`
- For each scenario:
  - symptoms and related alerts
  - dashboards/metrics to check
  - log/trace queries (without raw secrets/PII)
  - diagnosis steps (step-by-step)
  - mitigation/rollback within existing deployment/change processes
  - verification checks and post-incident actions
- `observability_gap` section:
  - identifies SLOs/critical paths lacking adequate observability.

---

## 8. KiloCode Usage Examples

### 8.1 Large-scope runbook generation on Kilo

```bash
smartspec_observability_runbook_generator \
  --spec-ids=checkout_api,inventory_api \
  --runbook-label=checkout-inventory-observability \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --kilocode \
  --stdout-summary
```

On Kilo:

- Orchestrator processes one spec-id at a time (top-level tasks).
- For each, subtasks gather SLOs, map alerts/dashboards, and construct
  scenarios.
- Code mode reads configs read-only.
- Orchestrator assembles a consolidated runbook.

### 8.2 Disabling subtasks for small services

```bash
smartspec_observability_runbook_generator \
  --spec-ids=small_service \
  --runbook-label=small-service-observability \
  --alert-config-paths=".config/alerts/small_service/*.yml" \
  --kilocode \
  --nosubtasks
```

- Uses a simpler single-flow reasoning per service.
- Useful for small scopes or initial experiments.

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo with multiple services

```bash
smartspec_observability_runbook_generator \
  --spec-ids=search_api,ranking_service \
  --runbook-label=search-stack-observability \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --alert-config-paths=".config/alerts/**/*.yml" \
  --dashboard-config-paths=".config/dashboards/**/*.json" \
  --runtime-metrics-paths=".config/metrics/**/*.yml"
```

- Uses registries + repos-config to understand relationships
  (search ↔ ranking ↔ dependencies).
- Runbooks describe which metrics/dashboards/logs to consult when
  search error rate spikes.

### 9.2 Cross-team, multi-repo scenario

```bash
smartspec_observability_runbook_generator \
  --spec-ids=teamA_checkout,teamB_payments \
  --runbook-label=checkout-payments-observability \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --alert-config-paths="../teamA/.config/alerts/**/*.yml;../teamB/.config/alerts/**/*.yml" \
  --dashboard-config-paths="../teamA/.config/dashboards/**/*.json;../teamB/.config/dashboards/**/*.json"
```

- Runbooks show when incidents require coordination across two teams.
- Makes clear which team owns which part of the observability stack.

---

## 10. UI Observability Examples

For UI-heavy services:

- typical requirements include:
  - Web Vitals (LCP, FID, CLS)
  - frontend error rate
  - API latency that affects key screens.

Runbooks may:

- point to Web Vitals / frontend error dashboards.
- map screens/flows to backend APIs.
- suggest log/trace queries per route or component.

UI governance considerations:

- **JSON-first UI (`ui.json`)**:
  - runbooks may reference screens/flows from `ui.json` and associate them
    with observability signals.
- **UI JSON opt-out / inline UI**:
  - do not assume `ui.json` exists.
  - still generate E2E/flow-based runbooks from specs and configs.

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Define SLOs/NFRs and configure basic observability (alerts/dashboards/logs)
  before running the generator for best results.
- Re-run the generator when:
  - observability configuration changes significantly.
  - before major releases.
- Review runbooks with on-call/SRE before adopting them.
- Store runbook suggestions in version control.
- Use `--safety-mode=strict` for critical/high-value services.

### 11.2 Anti-patterns

- Expecting the generator to invent SLOs/alerts from scratch with no
  specs/policies.
- Copying secrets/PII from logs into runbooks.
- Treating runbooks as the only source of truth without respecting
  change/approval processes.

---

## 12. FAQ / Troubleshooting

### Q1: What if we have almost no observability yet?

- You will still get runbooks, but with many `observability_gap` entries.
- Use them as guidance to build better alerts/dashboards/logs first.

### Q2: Is this useful for dev environments?

- Yes, especially for validating naming conventions and tracing setups.
- Maximum value usually comes in staging/prod.

### Q3: Do I need `/smartspec_release_readiness` as well?

- Not required, but recommended:
  - release readiness → are we ready to ship?
  - runbook generator → if something goes wrong, how do we troubleshoot?

---

End of `/smartspec_observability_runbook_generator v5.6.2` manual (English).
If future versions significantly change semantics or add major modes,
issue a new manual (e.g., v5.7) and document compatible workflow versions
clearly.

