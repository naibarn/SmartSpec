---
name: /smartspec_nfr_perf_verifier
version: 5.6.2
role: verification/governance
write_guard: NO-WRITE
purpose: Verify NFR, performance, and reliability targets against available
         test results and runtime evidence, and produce an NFR verification
         report without modifying code, specs, tests, or infrastructure.
---

## 1) Summary

`/smartspec_nfr_perf_verifier` reads SmartSpec artifacts and performance-
related evidence (load test reports, metrics, logs) and verifies whether
**non-functional requirements (NFRs)** and **performance/reliability targets**
are being met for a given scope and environment.

It focuses on:

- extracting NFRs from specs / SPEC_INDEX / policy files
- mapping NFRs to concrete metrics (latency, throughput, error rate,
  availability, resource usage, UX timings, etc.)
- reading existing performance/load/reliability test outputs and runtime
  metrics (read-only)
- evaluating each NFR as **`MET` / `NOT_MET` / `UNKNOWN`** with clear
  justification and criticality
- marking **critical gaps** that should be treated as blocking risks by
  release governance workflows
- producing a structured **NFR verification report** bound to spec-ids,
  environments, time windows, and (optionally) baseline comparisons

> **Verifier-only:**
> This workflow is purely a **verifier**. It does *not* design performance
> tests or generate tasks.
>
> Designing/generating performance/load test tasks is the responsibility of
> a separate workflow: `/smartspec_nfr_perf_planner` (planner/generator).

The workflow is:

- **strictly NO-WRITE**:
  - does not run tests
  - does not modify tests or configs
  - does not change specs or tasks
- intended to be used as an **evidence summarizer and verifier**, not as a
  test runner or NFR designer.

Use it as a supporting gate before `/smartspec_release_readiness`, and to keep
NFR/performance compliance visible over time.

---

## 2) When to Use

Use `/smartspec_nfr_perf_verifier` when:

- you have defined NFRs (e.g., latency, throughput, error budgets,
  availability, resource ceilings, UX timings) in specs or policy docs
- you have some combination of:
  - load/perf test reports (e.g., k6, JMeter, Locust, Gatling)
  - metrics from monitoring systems (latency, error rate, saturation, etc.)
  - availability / SLO dashboards
- you want a **SmartSpec-bound report** that answers:
  - which NFRs are being met?
  - which NFRs are failed?
  - which NFRs cannot be evaluated with current evidence?

Typical placement in the chain:

`generate_spec → generate_plan → generate_tasks → implement_tasks → generate_tests → run_perf_tests (outside SmartSpec) → /smartspec_nfr_perf_verifier → /smartspec_release_readiness`

For planning and generating performance/load test tasks from NFRs, use:

- `/smartspec_nfr_perf_planner` (separate workflow) **before** running tests
  and **before** calling this verifier.

Do **not** use this workflow to:

- invent new NFRs or change their targets (thresholds/SLOs)
- design performance test plans from scratch
- directly configure monitoring/observability backends

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts)

Read-only artifacts expected:

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs & tasks for each spec-id in scope**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`
  - optional NFR-specific docs (e.g., `nfr.md`) if referenced from SPEC_INDEX
    or spec

- **Registries (optional but recommended)**
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-model-registry.json`
  - `.spec/registry/critical-sections-registry.json`
  - `.spec/registry/service-registry.json` (if project defines one)
  - `.spec/registry/slo-registry.json` (if project defines one)

- **NFR/policy files (optional)**
  - any paths matching `--nfr-policy-paths` for global or team-level NFR
    standards (e.g., org-wide latency/availability baselines)

- **Performance/load test reports (optional)**
  - any paths matching `--perf-report-paths` (JSON, CSV, JUnit-XML-like,
    vendor-specific formats)

- **Monitoring/metrics exports (optional)**
  - any paths matching `--metrics-export-paths` (snapshots from Prometheus,
    Cloud Monitoring, etc.)

All of the above are treated as **read-only evidence**.

### 3.2 Inputs (flags)

See **5) Flags**.

### 3.3 Outputs

- **Primary NFR verification report** (human-readable + structured)
  - Default location:
    - `.spec/reports/smartspec_nfr_perf_verifier/<timestamp>_<run-label>.md`
  - If `--report-format=json` is used:
    - `.spec/reports/smartspec_nfr_perf_verifier/<timestamp>_<run-label>.json`

The report SHOULD provide, at minimum, these structures:

1. **NFR inventory** per spec-id and environment
   - each NFR with:
     - id/name
     - category (latency, throughput, availability, error_budget,
       resource, UX, etc.)
     - scope: `local` | `end_to_end`
     - criticality: `critical` | `high` | `medium` | `low`
     - target/threshold
     - definition source (spec, SPEC_INDEX, policy file, registry)

2. **NFR evaluations** per spec-id and environment
   - for each NFR:
     - evaluation status:
       - `MET`
       - `NOT_MET`
       - `UNKNOWN`
     - `blocking_for_release`: `true|false` (recommendation for
       release governance)
     - evidence sources (reports/metrics paths + time ranges)
     - explanation summary (why MET/NOT_MET/UNKNOWN)
     - for multi-service/end-to-end NFRs:
       - `involved_services`: list
       - per-service sub-status (if evidence available)

3. **NFR design gaps & proposed NFRs**
   - `nfr_design_gaps`:
     - critical paths or components with no explicit NFRs
     - always clearly marked as *gaps in design*, not failures
   - `proposed_nfrs`:
     - suggested NFRs the system might need
     - must be clearly labeled as **proposals only** (non-binding)

4. **Regression / baseline comparison** (if `--baseline-window` used)
   - per NFR:
     - `regression_status`: `IMPROVED` | `UNCHANGED` | `REGRESSED` |
       `UNKNOWN` (for the measured period vs baseline)
     - optional change magnitude (% change, absolute delta)
   - regression does *not* automatically change `MET` to `NOT_MET`, but
     should be surfaced as a risk.

5. **Aggregate summary**
   - per spec-id and environment:
     - counts of NFRs by status and criticality
     - list of critical gaps
   - global summary for the run:
     - total NFRs
     - `MET` / `NOT_MET` / `UNKNOWN` counts

Optional **stdout summary** when `--stdout-summary` is enabled, showing:

- number of NFRs evaluated
- counts of `MET`, `NOT_MET`, `UNKNOWN`
- count of `UNKNOWN (CRITICAL GAP)`
- link/path to the report file.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **Verification / Governance**
- Write guard: **NO-WRITE**

MUST NOT:

- run performance tests
- modify performance test configs or scenarios
- modify specs, tasks, registries, or code

MAY:

- read all allowed artifacts (specs, tasks, reports, metrics exports)
- generate new reports under `.spec/reports/smartspec_nfr_perf_verifier/`
- print textual summaries

### 4.2 Platform semantics

- Tool-agnostic by default.
- Under Kilo (when `--kilocode` is active and Kilo environment is detected):
  - Effective mode: **Ask / Architect** (never Code-for-write)
  - Use **Orchestrator-per-NFR-category** for reasoning only:
    - For each NFR category (latency, throughput, error rate, availability,
      resource usage, UX timings, etc.):
      1) Switch to Orchestrator.
      2) Decompose into sub-checks (e.g., P95 latency, P99 latency,
         tail spikes, percentile windows).
      3) In Code mode (read-only), parse relevant reports/metrics.
      4) Return summarized evaluation per category.
  - Write guard stays NO-WRITE at all times.

If `--kilocode` is present but Kilo does not appear to be available:

- treat `--kilocode` as a **no-op meta-flag**
- proceed in a generic LLM mode
- log a note about this in the report header.

---

## 5) Flags

> This is a new workflow; no existing flags are removed or repurposed.

### 5.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
  - Comma-separated spec IDs in scope.
  - All IDs must exist in SPEC_INDEX.

- `--include-dependencies`
  - Expand scope via SPEC_INDEX + registries to include dependent specs
    (e.g., upstream services, shared components).

- `--run-label=<string>`
  - Human-readable label for this verification run, used in filenames and
    report headers, e.g. `perf-check-2025-12-10`, `v1.3.0-rc1-prod`.

### 5.2 Environment & time window

- `--target-env=<env>`
  - e.g., `dev`, `staging`, `prod`.
  - Used to filter/select evidence for that environment only.

- `--time-window=<duration>`
  - e.g., `24h`, `7d`, `30d`.
  - Interpreted as a look-back window for metrics and logs when applicable.

- `--baseline-window=<duration>`
  - Optional reference window for baseline comparison (e.g., previous week for
    regression checks).

### 5.3 Evidence locations

- `--nfr-policy-paths="<glob1>;<glob2>;..."`
  - Optional paths to global/team-level NFR policy files.

- `--perf-report-paths="<glob1>;<glob2>;..."`
  - Optional paths to performance/load test reports.

- `--metrics-export-paths="<glob1>;<glob2>;..."`
  - Optional paths to metrics/monitoring exports.

### 5.4 Multi-repo / registry / index

- `--workspace-roots="<path1>;<path2>;..."`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots="<path1>;<path2>;..."`
- `--index=<path>` / `--specindex=<path>`
- `--safety-mode=<normal|strict>`
  - `--strict` as legacy alias for `--safety-mode=strict`.

Semantics:

- `--repos-config` preferred for precise multi-repo topology.
- `--workspace-roots` used as fallback when `--repos-config` is absent.
- `--registry-dir` is primary registry root (default `.spec/registry`).
- `--registry-roots` are read-only supplemental registries.

**Criticality & safety mode behavior:**

- `normal` (default):
  - gaps in evidence (no test/metric for an NFR) are recorded as
    `UNKNOWN` with recommendations.
  - `blocking_for_release` is only set to `true` when the evidence shows
    `NOT_MET` for critical NFRs.

- `strict` / `--strict`:
  - "critical NFRs" are defined as:
    - NFRs explicitly marked critical/high in specs, SPEC_INDEX, or policy
      files, or
    - NFRs in categories such as availability or core latency for specs
      tagged as core/critical services.
  - any critical NFR with **no evidence at all** must be marked as
    `UNKNOWN (CRITICAL GAP)` and `blocking_for_release=true`.
  - critical NFRs that are `NOT_MET` must also set `blocking_for_release=true`.

### 5.5 Kilo / subtasks

- `--kilocode`
  - Enables Kilo-aware behavior (Orchestrator-per-NFR-category).

- `--nosubtasks`
  - Disables automatic subtask decomposition.

### 5.6 Output control

- `--report-format=<md|json>`
  - Default: `md`.

- `--report-dir=<path>`
  - Default: `.spec/reports/smartspec_nfr_perf_verifier/`.

- `--stdout-summary`
  - Prints a brief summary (counts of MET/NOT_MET/UNKNOWN, etc.).

---

## 6) Canonical Folders & File Placement

The workflow MUST follow SmartSpec canonical folder rules:

1. **Index detection order** (read-only):
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy mirror)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. **Registries**:
   - Primary: `.spec/registry/`
   - Supplemental: any `--registry-roots` (read-only)

3. **Specs**:
   - `specs/<category>/<spec-id>/spec.md`
   - `specs/<category>/<spec-id>/tasks.md`

4. **Reports**:
   - Default:
     - `.spec/reports/smartspec_nfr_perf_verifier/<timestamp>_<run-label>.{md|json}`
   - The workflow MUST NOT default to `.smartspec/` for new reports.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow spec as complete, check that it:

1. **Preserves NO-WRITE**
   - Explicitly forbids running tests or changing artifacts.

2. **Avoids NFR drift**
   - NFR definitions and thresholds must come from:
     - specs
     - SPEC_INDEX
     - NFR policy files
   - The workflow must NOT:
     - change thresholds/SLOs
     - drop existing NFRs from evaluation
     - introduce brand new NFRs as if they were official.
   - Suggestions for new NFRs must be clearly labeled as proposals in
     `proposed_nfrs`.

3. **Clarifies UNKNOWN vs NOT_MET**
   - `NOT_MET` only when evidence shows the NFR fails.
   - `UNKNOWN` when evidence is missing or inconclusive.
   - `UNKNOWN (CRITICAL GAP)` specifically when a **critical** NFR has no
     evidence at all (especially under strict mode).

4. **Handles environment & time correctly**
   - Evaluations clearly state `--target-env` and `--time-window`.
   - Avoids mixing dev/staging/prod metrics without labeling.
   - When `--baseline-window` is used, regression status is derived but does
     not silently change core pass/fail status.

5. **Aligns with other workflows**
   - The report is usable by `/smartspec_release_readiness` as evidence.
   - Safety mode semantics (`normal` vs `strict`) are consistent with
     other governance workflows.
   - CI-related recommendations should reference
     `/smartspec_ci_quality_gate` when missing tests prevent NFR evaluation.

6. **Multi-repo awareness**
   - For distributed systems, the report highlights when an NFR depends on
     multiple services and which services have evidence.
   - End-to-end NFRs distinguish between global status and per-service
     sub-status.

7. **Verifier-only boundary**
   - Test planning and task generation are explicitly out of scope here and
     delegated to `/smartspec_nfr_perf_planner`.

---

## 8) Legacy Flags Inventory

New workflow:

- **Kept as-is**:
  - (none)

- **Legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--run-label`
  - `--target-env`
  - `--time-window`
  - `--baseline-window`
  - `--nfr-policy-paths`
  - `--perf-report-paths`
  - `--metrics-export-paths`
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`
  - `--registry-roots`
  - `--index`
  - `--specindex`
  - `--safety-mode`
  - `--report-format`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

### 9.1 Role-based semantics

As a verification/governance workflow:

- Accepts `--kilocode`.
- Must remain in **Ask / Architect** role under Kilo.
- Write guard: always **NO-WRITE**.

### 9.2 Orchestrator-per-NFR-category loop

With `--kilocode` and Kilo available:

For each NFR category (latency, throughput, availability, error budget,
resource usage, UX timings, etc.):

1. Orchestrator enumerates sub-metrics (e.g., P95 latency, P99 latency,
   percentile windows, error types, resource ceilings).
2. Code mode (read-only) parses relevant report/metric files.
3. Orchestrator evaluates pass/fail/unknown per sub-metric.
4. Orchestrator aggregates into final status per NFR and category,
   including criticality and `blocking_for_release` suggestions.

`--nosubtasks` disables step 1 (no automatic decomposition) while keeping
other logic.

### 9.3 Non-Kilo environments

- Treat `--kilocode` as no-op.
- Use a more linear reasoning flow.

---

## 10) Inline Detection Rules

The workflow must not invoke other workflows for detection. Instead it:

1. Inspects system prompt / environment metadata for mentions of
   Kilo/Claude Code/Antigravity.

2. Inspects flags for `--kilocode`.

3. If signals are ambiguous:
   - defaults to tool-agnostic behavior
   - notes uncertainty in the report header.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` (when provided) to map spec-ids to services/repos.

2. Use `--workspace-roots` only as a discovery hint, never to guess
   spec-ids outside SPEC_INDEX.

3. Use registries to:
   - understand service boundaries and dependencies
   - map NFRs that span multiple services (e.g., end-to-end latency across
     multiple APIs).

4. NFRs that depend on multiple services should:
   - list involved services/repos
   - show per-service evidence status when available
   - still provide a clear end-to-end verdict.

---

## 12) UI Addendum (UX-related NFRs)

Some NFRs may relate directly to UI/UX (e.g., page load time, time-to-first-
interaction). This workflow should:

1. Identify UX-related NFRs from specs/policies.

2. Map them to metrics such as:
   - page load time
   - Largest Contentful Paint (LCP)
   - Time to Interactive (TTI)
   - input latency

3. Use available frontend perf reports/metrics as evidence.

4. Respect the project’s UI governance (JSON-first vs inline, including
   any UI JSON opt-out) as context only:
   - governance mode helps interpret where evidence comes from
   - it does not change pass/fail rules for the NFR itself.

---

## 13) Best Practices

- Ensure NFRs are explicitly written in specs or policy docs; avoid relying
  on tribal knowledge.

- Use `/smartspec_nfr_perf_planner` to derive concrete perf/load test tasks
  from NFRs, then implement and run those tests before using this verifier.

- Run this workflow **after** performance/load tests have executed for the
  given time window and environment.

- Use consistent `--run-label` naming to correlate reports with CI runs or
  releases.

- Use `--safety-mode=strict` when preparing for production releases.

- Store NFR verification reports in version control or as CI artifacts for
  auditability.

- Periodically run this workflow (e.g., weekly) for critical services to
  catch NFR regressions early, not only before big releases.

- When critical NFRs are `UNKNOWN (CRITICAL GAP)` or `NOT_MET`, ensure that
  `/smartspec_release_readiness` treats them as blocking risks unless an
  explicit exception process exists.

---

## 14) For the LLM / Step-by-Step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve scope**
   - Read `--spec-ids`, `--include-dependencies`, `--target-env`,
     `--run-label`.
   - Load SPEC_INDEX using canonical detection order.
   - Validate all spec-ids exist in SPEC_INDEX.
   - Expand to dependent specs if requested.
   - If scope cannot be resolved without guessing, stop and request
     clarification instead of inventing spec-ids.

2. **Gather artifacts**
   - Load specs/tasks for all spec-ids.
   - Load NFR/policy files (`--nfr-policy-paths`).
   - Load registries (`--registry-dir`, `--registry-roots`).
   - Load performance reports (`--perf-report-paths`).
   - Load metrics exports (`--metrics-export-paths`).

3. **Extract NFRs**
   - From spec and policy files, build an NFR list per spec-id and
     environment, including:
     - NFR id/name and category
     - scope: local vs end-to-end
     - target/threshold
     - criticality (critical/high/medium/low) based on metadata from
       SPEC_INDEX/policies.

4. **Map NFRs to evidence**
   - For each NFR, find relevant entries in perf reports / metrics.
   - Respect `--target-env` and `--time-window` when selecting evidence.
   - If `--baseline-window` is provided, gather baseline data for
     regression comparison where possible.

5. **Evaluate each NFR**
   - Decide `MET`, `NOT_MET`, or `UNKNOWN`:
     - `MET`: evidence clearly shows the metric meets or beats the target.
     - `NOT_MET`: evidence shows the metric fails the target.
     - `UNKNOWN`: insufficient or no evidence.
   - Determine `blocking_for_release` based on safety mode and criticality.
   - For end-to-end NFRs, capture per-service contributions when data allows.

6. **Compute regression vs baseline (optional)**
   - When baseline data is available, compute `regression_status` per NFR
     (`IMPROVED` / `UNCHANGED` / `REGRESSED` / `UNKNOWN`).
   - Do not silently change MET→NOT_MET purely due to regression; report it
     as a separate dimension.

7. **Aggregate results**
   - Per spec-id, per environment, per NFR category.
   - Summarize counts and key risks, especially for critical NFRs.

8. **Create report**
   - Serialize to `.md` or `.json` under the configured `--report-dir`.
   - Include:
     - NFR inventory
     - evaluation table with criticality and blocking suggestions
     - environment/time window
     - critical gaps and recommendations
     - regression summary if applicable
     - `nfr_design_gaps` and `proposed_nfrs` clearly labeled.

9. **Optional stdout summary**
   - If `--stdout-summary` is set, print a short summary with:
     - counts of MET/NOT_MET/UNKNOWN
     - number of critical gaps
     - number of specs/environments
     - report file path.

### 14.2 Stop conditions

The workflow MUST stop after:

- writing the report (or simulating it in dry-run mode), and
- printing any optional stdout summary.

It MUST NOT:

- run or modify performance tests
- modify specs, tasks, or code
- change registry contents
- invoke other workflows directly (it may recommend them only in text).

