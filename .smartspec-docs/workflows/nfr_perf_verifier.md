---
manual_name: /smartspec_nfr_perf_verifier Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_nfr_perf_verifier
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, tech leads, performance owners)
---

# /smartspec_nfr_perf_verifier Manual (v5.6, English)

## 1. Overview

This manual describes how to use the workflow:

> `/smartspec_nfr_perf_verifier v5.6.2`

The workflow verifies whether **Non-Functional Requirements (NFRs)** and
**performance/reliability targets** defined in your specs and policies are
actually being met, based on existing test reports and runtime metrics.

It answers questions like:

- Which NFRs are currently **met**?
- Which NFRs are clearly **not met**?
- Which NFRs are **unknown** because we lack evidence?

Key properties:

- Role: **verification / governance** (not a test runner)
- `write_guard: NO-WRITE`
  - does **not** run perf/load tests
  - does **not** change specs / tasks / CI / code
  - reads artifacts **read-only** and produces an **NFR verification report**
- **Verifier-only:**
  - does **not** design performance plans
  - does **not** generate tasks from NFRs
  - planning/generation is delegated to `/smartspec_nfr_perf_planner`

Use this workflow as an evidence layer before
`/smartspec_release_readiness`, and to continuously monitor NFR health over
 time.

---

## 2. What’s New in v5.6

Version 5.6.2 introduces several important behaviors:

### 2.1 Clear verifier-only boundary

- Explicitly declares it is **only a verifier**.
- Refers to `/smartspec_nfr_perf_planner` for planning/generation.
- Prevents scope confusion between "defining tests" and "checking results".

### 2.2 Structured report format

The recommended report now includes:

- `NFR inventory` (category, scope, criticality, target, source)
- `NFR evaluations` (status + `blocking_for_release` flag)
- `nfr_design_gaps` (critical paths without explicit NFRs)
- `proposed_nfrs` (non-binding suggestions)
- `regression_status` per NFR when a baseline window is provided
- aggregate summary by spec-id, environment, category, and criticality

### 2.3 Strict mode with explicit blocking semantics

- `--safety-mode=strict` (or `--strict`) ensures:
  - critical NFRs with **no evidence at all** →
    - status: `UNKNOWN (CRITICAL GAP)`
    - `blocking_for_release=true`
  - critical NFRs with `NOT_MET` → `blocking_for_release=true`
- This provides a direct signal to `/smartspec_release_readiness` about which
  NFRs should be considered blocking risks.

### 2.4 Multi-service / end-to-end NFR support

- Adds:
  - `scope: local | end_to_end`
  - `involved_services` + per-service sub-status
- Helps visualize how a single NFR may span multiple services and which ones
  contribute positively or negatively.

### 2.5 Regression vs baseline window

- With `--baseline-window`, the report includes `regression_status` per NFR:
  - `IMPROVED`, `UNCHANGED`, `REGRESSED`, or `UNKNOWN`
- Regression does **not** automatically flip `MET` to `NOT_MET`, but is
  reported as an additional risk dimension.

---

## 3. Backward Compatibility Notes

- This manual v5.6 applies to `/smartspec_nfr_perf_verifier` from
  **v5.6.2 onwards** (5.6.x).
- No legacy flags or behaviors are removed (workflow is new in the NFR
  family).
- `--strict` remains an alias for `--safety-mode=strict`.
- Multi-repo, `--kilocode`, and canonical folder semantics match existing
  governance workflows:
  - `/smartspec_release_readiness`
  - `/smartspec_ci_quality_gate`

Patch releases within 5.6.x that do not change core semantics remain
compatible with this manual.

---

## 4. Core Concepts

### 4.1 NFR inventory

NFRs are collected from:

- `spec.md`
- `tasks.md` (if NFR sections exist)
- SPEC_INDEX
- NFR policy files
- relevant registries (e.g., an SLO registry)

For each NFR, the workflow aims to capture at least:

- id/name
- category: `latency`, `throughput`, `availability`, `error_budget`,
  `resource`, `UX`, etc.
- scope: `local` (single service) vs `end_to_end`
- target/threshold
- criticality: `critical` | `high` | `medium` | `low`
- source: where this NFR is defined

### 4.2 Status: MET / NOT_MET / UNKNOWN

- `MET`
  - Evidence clearly shows that the measured metric meets or exceeds the
    target.

- `NOT_MET`
  - Evidence clearly shows that the metric fails the target.

- `UNKNOWN`
  - No relevant evidence is available, or
  - Evidence is incomplete/inconclusive.

- `UNKNOWN (CRITICAL GAP)`
  - A critical NFR with no evidence at all (especially under strict mode).

### 4.3 blocking_for_release

A boolean flag per NFR, indicating whether it should be treated as a
**blocking risk** in release decisions.

It considers:

- criticality
- status (MET / NOT_MET / UNKNOWN)
- safety-mode (`normal` vs `strict`)

---

## 5. Quick Start Examples

### 5.1 Check NFRs for one service in staging

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=checkout_api \
  --target-env=staging \
  --run-label=checkout-staging-nfr \
  --nfr-policy-paths=".spec/policies/nfr/*.md" \
  --perf-report-paths="reports/perf/checkout/*.json" \
  --metrics-export-paths="metrics/checkout/*.json" \
  --report-format=md \
  --stdout-summary
```

Result:

- Report at:
  `.spec/reports/smartspec_nfr_perf_verifier/<timestamp>_checkout-staging-nfr.md`
- Summary for `checkout_api` in `staging`.

### 5.2 Strict mode before production release

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=payments_gateway \
  --target-env=prod \
  --run-label=payments-prod-nfr \
  --perf-report-paths="reports/perf/payments/*.json" \
  --metrics-export-paths="metrics/payments/*.json" \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

In strict mode:

- critical NFRs with no evidence → `UNKNOWN (CRITICAL GAP)` + blocking
- critical NFRs with `NOT_MET` → blocking

### 5.3 Regression vs baseline

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=search_api \
  --target-env=prod \
  --run-label=search-prod-nfr \
  --perf-report-paths="reports/perf/search/*.json" \
  --metrics-export-paths="metrics/search/*.json" \
  --time-window=7d \
  --baseline-window=30d \
  --report-format=md
```

The report will show `regression_status` per NFR comparing the last 7 days
against a 30-day baseline.

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--run-label=<string>`

### 6.2 Environment & time

- `--target-env=dev|staging|prod|...`
- `--time-window=24h|7d|30d|...`
- `--baseline-window=7d|30d|...`

### 6.3 Evidence paths

- `--nfr-policy-paths="..."`
- `--perf-report-paths="..."`
- `--metrics-export-paths="..."`

### 6.4 Multi-repo / registry / index

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`

### 6.5 Safety / kilocode / output

- `--safety-mode=normal|strict` (or `--strict`)
- `--kilocode`, `--nosubtasks`
- `--report-format=md|json`
- `--report-dir` (default
  `.spec/reports/smartspec_nfr_perf_verifier/`)
- `--stdout-summary`

---

## 7. Interpreting MET / NOT_MET / UNKNOWN

### 7.1 MET

- Clear evidence that the NFR target is met, e.g.:
  - P95 latency <= target
  - error rate below threshold
  - availability above SLO

### 7.2 NOT_MET

- Evidence clearly shows the target is not met.
- Typically requires explicit risk acceptance or mitigation.

### 7.3 UNKNOWN

- No test or metrics mapped to that NFR, or
- Data is too weak, incomplete, or inconsistent to conclude.

### 7.4 UNKNOWN (CRITICAL GAP)

- Critical NFR with **no evidence at all** (especially in strict mode).
- Should be treated as **not ready** for release until evidence is created.

---

## 8. KiloCode Usage Examples

### 8.1 Kilo + strict for a core service

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=core_billing \
  --target-env=prod \
  --run-label=core-billing-nfr \
  --perf-report-paths="reports/perf/core_billing/*.json" \
  --metrics-export-paths="metrics/core_billing/*.json" \
  --safety-mode=strict \
  --kilocode \
  --stdout-summary
```

Under Kilo:

- Orchestrator iterates by NFR category (latency, availability, etc.).
- Code mode parses reports per category (read-only).
- Orchestrator aggregates statuses and `blocking_for_release` flags.

### 8.2 Disabling subtasks

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=small_feature \
  --target-env=staging \
  --run-label=small-feature-nfr \
  --kilocode \
  --nosubtasks
```

- Still Kilo-aware but uses a single reasoning flow, suitable for small
  scopes.

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo with multiple services

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=search_api,ranking_service \
  --target-env=prod \
  --run-label=search-stack-nfr \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --perf-report-paths="reports/perf/**/*.json" \
  --metrics-export-paths="metrics/**/*.json" \
  --safety-mode=strict
```

- Uses repos-config + registry to map end-to-end NFRs.
- Highlights which services contribute to each end-to-end NFR.

### 9.2 Multiple repos / teams

```bash
smartspec_nfr_perf_verifier \
  --spec-ids=teamA_checkout,teamB_payments \
  --target-env=staging \
  --run-label=checkout-payments-nfr \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --perf-report-paths="../teamA/reports/perf/**/*.json;../teamB/reports/perf/**/*.json" \
  --metrics-export-paths="../teamA/metrics/**/*.json;../teamB/metrics/**/*.json"
```

- The report shows cross-team NFRs and which repo provides which evidence.

---

## 10. UI/UX NFR Examples

### 10.1 Page load / LCP / TTI

If specs define UX NFRs like:

- LCP < 2.5s at 95th percentile
- TTI < 5s

and you provide Web Vitals or synthetic monitoring metrics, the workflow
will:

- map metrics to the relevant NFRs
- evaluate them as MET / NOT_MET / UNKNOWN

UI governance mode (JSON-first vs inline) is only context for locating
components/screens; it does **not** change pass/fail criteria.

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Write NFRs clearly in specs/policies before relying on this verifier.
- Use `--safety-mode=strict` for core or critical services.
- Run this workflow periodically (e.g., weekly) for critical systems,
  not just before releases.
- Store reports in version control or CI artifacts.
- Review results together with `/smartspec_ci_quality_gate` and
  `/smartspec_release_readiness`.

### 11.2 Anti-patterns

- Interpreting "no evidence" as "safe" – it is actually `UNKNOWN` or
  `CRITICAL GAP`.
- Ignoring `UNKNOWN (CRITICAL GAP)` for critical NFRs and proceeding to
  release without an exception process.
- Letting the workflow guess spec-ids or mappings from arbitrary names.

---

## 12. FAQ / Troubleshooting

### Q1: What happens if I have no perf tests or metrics at all?

- Most NFRs will be `UNKNOWN`.
- Critical NFRs in strict mode → `UNKNOWN (CRITICAL GAP)` + blocking.
- You should go back and use `/smartspec_nfr_perf_planner` plus
  `/smartspec_ci_quality_gate` to establish tests and CI checks.

### Q2: Why is an NFR marked MET but `regression_status` is REGRESSED?

- The target is still met, but the metric has degraded significantly vs
  the baseline.
- Treat it as an early warning; continued regression may eventually cause
  the NFR to fail.

### Q3: What if an NFR is NOT_MET but we must release?

- The workflow only reports facts and risks.
- Any exception/waiver must be handled by your org's governance process,
  outside this workflow.

---

End of `/smartspec_nfr_perf_verifier v5.6.2` manual (English).
If new capabilities are added (e.g., support for new metrics formats or
material changes to strict-mode semantics), issue a new manual (v5.7) and
clearly document compatible workflow versions.

