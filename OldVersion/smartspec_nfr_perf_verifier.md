---
name: /smartspec_nfr_perf_verifier
version: 5.7.0
role: verification/governance
write_guard: NO-WRITE
purpose: Verify NFR, performance, and reliability targets against runtime evidence (test reports, metrics, logs) under SmartSpec v5.7 governance (multi-repo, multi-registry, safety-mode, UI metadata). Verifier-only; no modifications to specs/tasks/code/registries.
version_notes:
  - v5.6.2: baseline NFR/perf verifier
  - v5.7.0: governance alignment; expanded safety-mode; multi-repo/registry parity; UI metadata signals; clarified UNKNOWN/NOT_MET rules; backward-compatible; documentation-only update
---

# /smartspec_nfr_perf_verifier (v5.7.0)

This workflow verifies **non-functional requirements (NFRs)**, performance, and reliability goals using existing **evidence**:
- performance/load test reports,
- metrics from monitoring systems,
- logs and SLO dashboards,
- NFR definitions from specs, SPEC_INDEX, and policy documents.

It is a **verifier-only**, **NO-WRITE** workflow. It never:
- runs performance tests,
- modifies tests/configs/specs/tasks,
- alters registries or code.

Its output is an NFR verification report used by:
- `/smartspec_release_readiness`,
- portfolio governance reviews,
- CI quality gates.

All v5.6.2 behavior is preserved.

---
## 1) Responsibilities
- Resolve canonical index & registry under v5.7 rules.
- Extract NFRs from specs, SPEC_INDEX, and NFR policy files.
- Map NFRs to thresholds, criticality, env, and scope.
- Locate, parse, and evaluate evidence (reports/metrics/logs).
- Evaluate each NFR as: **MET / NOT_MET / UNKNOWN**.
- Apply stricter rules under `--safety-mode=strict`.
- Produce a structured report (md/json).
- Highlight critical gaps and blocking risks for release governance.

---
## 2) Inputs
### 2.1 Artifacts (read-only)
- SPEC_INDEX (canonical detection order):
  1. `.spec/SPEC_INDEX.json`
  2. `SPEC_INDEX.json`
  3. `.smartspec/SPEC_INDEX.json`
  4. `specs/SPEC_INDEX.json`
- specs (`spec.md`), tasks (`tasks.md`)
- registries (primary + supplemental)
- NFR policy files
- performance/load test reports
- metrics/monitoring snapshots

### 2.2 Flags
- `--spec-ids=<csv>`
- `--include-dependencies`
- `--run-label=<string>`
- `--target-env=<env>`
- `--time-window=<duration>`
- `--baseline-window=<duration>`
- `--perf-report-paths=<glob>`
- `--metrics-export-paths=<glob>`
- `--nfr-policy-paths=<glob>`
- `--workspace-roots=<csv>`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots=<csv>`
- `--index=<path>` / `--specindex=<legacy>`
- `--safety-mode=<normal|strict>` (default normal)
- `--strict` alias
- `--report-format=<md|json>`
- `--report-dir=<path>`
- `--stdout-summary`
- `--kilocode`
- `--nosubtasks`

---
## 3) Safety Mode (v5.7)
### normal (default)
- Missing evidence = `UNKNOWN`
- Critical gaps flagged but not automatically blocking

### strict
- Critical NFR with **no evidence** → `UNKNOWN (CRITICAL GAP)` + `blocking_for_release=true`
- Critical NFR with failing evidence → `NOT_MET` + `blocking_for_release=true`
- Multi-repo inconsistencies escalate warnings to blocking

Critical NFRs determined by:
- spec metadata
- SPEC_INDEX criticality
- policy files (org-level SLO/NFR classifications)

---
## 4) NFR Extraction
Sources:
- spec.md (NFR, SLA/SLO, Performance, Reliability)
- policy files
- SPEC_INDEX (NFR metadata)
- registries (e.g., slo-registry when present)
- optional UI JSON for UX NFRs

Extracted structure:
```
{
  id,
  category,        # latency | throughput | availability | resource | error_rate | UX ...
  threshold,
  environment,
  criticality,
  scope,           # local | end_to_end
  source_path
}
```

---
## 5) Evidence Mapping
Match NFRs to:
- perf reports (k6, JMeter, Gatling, Locust, etc.)
- metrics exports (Prometheus, Cloud Monitoring, etc.)
- logs
- SLO dashboards

Selection filtered by:
- `--target-env`
- `--time-window`
- evidence timestamps

Baseline comparison available via `--baseline-window`.

---
## 6) Evaluation Rules
### MET
- Evidence clearly meets or exceeds threshold.

### NOT_MET
- Evidence clearly violates threshold.

### UNKNOWN
- No evidence or inconclusive evidence.
- Under strict mode, critical NFRs without evidence → `UNKNOWN (CRITICAL GAP)`.

Each NFR evaluation includes:
- status (MET / NOT_MET / UNKNOWN)
- blocking_for_release suggestion (policy-driven)
- evidence summary
- involved services (for end-to-end)
- regression status (optional)

Regression status when baseline is provided:
- `IMPROVED` | `UNCHANGED` | `REGRESSED` | `UNKNOWN`

---
## 7) UI Addendum (v5.7)
For UX/Frontend NFRs:
- use UI perf metrics when available
- detect UX latency, LCP, TTI, interaction delays
- incorporate UI JSON metadata when present:
  - `source`, `generator`, `generated_at`
  - `design_system_version`, `style_preset`, `review_status`
- Missing UI JSON is non-blocking here but surfaced as a governance risk

---
## 8) Multi-Repo & Registry Awareness
- Use `--repos-config` for consistent multi-repo mapping.
- Fall back to `--workspace-roots`.
- Validate ownership using registries.
- End-to-end NFRs list all participating services.

Strict mode blocking examples:
- missing registry entries for critical shared APIs
- contradictory definitions between primary and supplemental registries

---
## 9) Output
Default directory:
```
.spec/reports/smartspec_nfr_perf_verifier/
```
Files:
- `<timestamp>_<run-label>.md`
- `<timestamp>_<run-label>.json` (if json output requested)

Report includes:
- header (scope, env, windows, safety-mode)
- NFR inventory
- per-NFR evaluations
- evidence mapping
- regression comparison (optional)
- design gaps & proposed NFRs (non-binding)
- multi-repo + registry notes
- aggregated release-risk summary

`--stdout-summary` prints compact metrics.

---
## 10) KiloCode Semantics
- `--kilocode` enables Kilo-aware Ask/Architect mode
- Orchestrator-per-NFR-category loop (read-only) when subtasks enabled
- `--nosubtasks` disables decomposition
- Write guard remains NO-WRITE

---
## 11) Stop Conditions
The workflow MUST STOP after:
- reading all evidence,
- evaluating NFRs,
- generating the report (or simulating with `--dry-run`).

It MUST NOT:
- run perf tests
- modify code/specs/tasks/registries
- invoke other workflows (may only recommend them)

---
## 12) Legacy Flags Inventory
Kept:
- `--strict` alias

Additive-only in v5.7 (no removals):
- all scope, evidence, multi-repo, registry, safety, and output flags.

