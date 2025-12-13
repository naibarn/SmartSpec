---
name: /smartspec_observability_runbook_generator
version: 5.7.0
role: observability/governance
write_guard: NO-WRITE
purpose: Generate observability runbooks from SmartSpec artifacts, SLO/NFR definitions, and observability policies under SmartSpec v5.7 governance. Planner-only; never modifies configs/code/tests/specs.
version_notes:
  - v5.6.2: baseline observability runbook generator
  - v5.7.0: governance alignment; multi-repo/registry parity; strict-mode updates; UI metadata integration; improved SLO/NFR extraction; backward-compatible
---

# /smartspec_observability_runbook_generator (v5.7.0)

Generates **observability runbooks**—diagnostic steps, dashboards, alerts, SLO context, failure modes—based on:
- NFR/SLO definitions in specs
- SPEC_INDEX metadata
- observability policy files
- registry-based ownership mapping
- multi-repo dependencies
- optional UI JSON metadata

Preserves all behavior from v5.6.2.

---
## 1) Responsibilities
- resolve canonical SPEC_INDEX
- extract relevant NFR/SLO
- map to observability components (logs, metrics, traces, dashboards)
- detect observability gaps (v5.7 rules)
- produce runbook sections per failure mode
- respect multi-repo ownership
- incorporate UI metadata for UI-facing services

---
## 2) Inputs
### Artifacts (read-only)
- SPEC_INDEX
- spec.md, tasks.md
- observability policy files
- registries (service, API, data classification)
- UI JSON (optional)

### Evidence (read-only)
- monitoring dashboards
- alert definitions
- logs/trace schemas
- metrics definitions

---
## 3) Outputs
Default directory:
```
.spec/runbooks/smartspec_observability_runbook_generator/
```
Outputs:
- `<timestamp>_<label>.md`
- `<timestamp>_<label>.json` (optional)

Includes:
- SLO/NFR inventory
- failure modes
- recommended dashboards
- runbook steps
- observability gaps
- multi-repo interactions
- UI addendum

---
## 4) Flags
- `--spec-ids=<csv>`
- `--include-dependencies`
- `--runbook-label=<string>`
- `--observability-policy-paths=<glob>`
- `--workspace-roots=<csv>`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots=<csv>`
- `--index=<path>` / `--specindex=<legacy>`
- `--target-env=<env>`
- `--plan-format=<md|json>`
- `--plan-dir=<path>`
- `--stdout-summary`
- `--kilocode`
- `--nosubtasks`
- `--safety-mode=<normal|strict>`
- `--strict` alias

---
## 5) Safety-mode (v5.7)
### normal
- gap detection is advisory
- allows exploratory runbook steps

### strict
- all critical SLOs must have runbook coverage
- missing observability assets → high-severity gap
- contradictory registry ownership → blocking gap

---
## 6) Canonical Resolution
### SPEC_INDEX
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

### Registries
- primary + supplemental (read-only)

### Multi-repo
- prefer repos-config
- fallback workspace-roots + current repo

---
## 7) NFR/SLO Extraction
Sources:
- spec NFR/SLA/SLO sections
- observability policies
- SPEC_INDEX metadata
- registries (e.g., slo-registry)
- UI JSON (UX latency/interaction metrics)

Extracted fields:
```
{id, category, threshold, criticality, environment, scope, source_path}
```

---
## 8) Failure-mode Mapping
Common categories:
- latency regression
- error-rate spikes
- availability drops
- slow UI metrics (LCP, TTI)
- dependency failures
- resource exhaustion
- misconfigurations

Each failure mode includes:
```
- symptoms
- dashboards
- logs/traces
- diagnostic steps
- remediation guidance
```

---
## 9) Observability Gap Detection
Detect missing:
- dashboards
- alerts
- logs/metrics coverage
- trace instrumentation
- UI performance metrics
- cross-service visibility for end-to-end SLOs

Strict-mode: critical gaps are blocking.

---
## 10) UI Addendum (v5.7)
When UI JSON is present:
- use metadata (`source`, `generator`, `generated_at`, `design_system_version`, `style_preset`, `review_status`)
- propose UI observability tasks (synthetic journeys, UX latency)
Missing UI JSON = governance risk.

---
## 11) Runbook Assembly
Sections:
- overview
- SLO/NFR inventory
- failure modes
- diagnostic steps
- observability gaps
- cross-repo context
- recommended next steps

---
## 12) KiloCode Behavior
- Ask/Architect only
- Orchestrator-per-failure-mode when subtasks allowed
- never write to configs/code

---
## 13) Legacy Flags
Kept:
- all flags from v5.6.2
Additive:
- `--safety-mode`, `--registry-roots`, `--repos-config`, `--plan-format`

