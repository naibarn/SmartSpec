---
name: /smartspec_nfr_perf_planner
version: 5.7.0
role: design/planning
write_guard: NO-WRITE
purpose: Generate performance/load/reliability test task proposals from existing NFRs, SLOs, policies, and SmartSpec artifacts under full SmartSpec v5.7 governance (multi-repo, multi-registry, safety-mode, UI JSON signals). Planner-only; never modifies specs, tasks, CI, or code.
version_notes:
  - v5.6.2: baseline NFR→perf task planner
  - v5.7.0: governance alignment; safety-mode expansion; multi-repo/registry parity; UI metadata; clarified NFR extraction; backward-compatible (no behavior removed)
---

# /smartspec_nfr_perf_planner (v5.7.0)

Planner-only workflow that converts **NFRs** (latency, throughput, error rate, availability, UX timings, etc.) into structured **performance/load/reliability task proposals**.

All v5.6.2 capabilities are preserved; additions are governance-only.

---
## 1) Responsibilities
- Extract NFRs from specs, SPEC_INDEX, and policy files
- Detect missing perf/load/reliability coverage
- Map NFRs → proposed perf tasks per environment
- Avoid duplicates with existing tasks
- Incorporate multi-repo + multi-registry context
- Optionally use UI JSON metadata for UX perf planning
- Output a perf plan file (md/json)

---
## 2) Outputs
Default directory:
```
.spec/suggestions/smartspec_nfr_perf_planner/
```
File name example:
```
<timestamp>_<plan-label>.md
```
Optional JSON when using `--plan-format=json`.

Contents include:
- proposed_perf_tasks (grouped by spec-id)
- mapping NFR → task list
- acceptance criteria
- environment coverage
- tool hints
- relationship to existing tasks
- optional proposed_nfrs (non-binding)

---
## 3) Inputs
### Artifacts (read-only)
- SPEC_INDEX
- specs + tasks
- NFR policy files
- primary + supplemental registries
- UI JSON (optional)

### Flags (expanded v5.7)
- `--spec-ids=<csv>`
- `--include-dependencies`
- `--plan-label=<string>`
- `--nfr-policy-paths=<glob>`
- `--workspace-roots=<csv>`
- `--repos-config=<path>` (preferred)
- `--registry-dir=<path>`
- `--registry-roots=<csv>`
- `--index=<path>` / `--specindex=<legacy>`
- `--safety-mode=<normal|strict>` (default: normal)
- `--strict` alias
- `--target-envs=<csv>`
- `--preferred-tools=<csv>`
- `--intensity-level=<light|normal|heavy>`
- `--max-tasks-per-nfr=<int>`
- `--plan-format=<md|json>` (default md)
- `--plan-dir=<path>` (default planner root)
- `--stdout-summary`
- `--kilocode`
- `--nosubtasks`

---
## 4) Safety Model (v5.7)
### normal (default)
- may propose optional exploratory scenarios
- may suggest missing NFRs as ideas (non-binding)

### strict
- must cover all declared NFRs
- cannot propose scenarios conflicting with formal policy
- must mark evidence-critical tasks as `priority=high`

---
## 5) Canonical Detection Rules
### SPEC_INDEX resolution
1. `.spec/SPEC_INDEX.json`
2. `SPEC_INDEX.json`
3. `.smartspec/SPEC_INDEX.json`
4. `specs/SPEC_INDEX.json`

### Registries
- primary: `.spec/registry/`
- supplemental: read-only from `--registry-roots`

### Multi-repo
- prefer repos-config for mapping
- fallback: workspace-roots + current repo
- strict-mode: mismatches = blocking

---
## 6) NFR Extraction
Sources:
- spec.md (sections: NFR, SLA, SLO, Performance, Reliability)
- NFR policy files
- SPEC_INDEX references
- registries (slo-registry when present)
- UI JSON (UX timings)

Each NFR extracted as:
```
{
  id,
  category,
  threshold,
  environment,
  criticality,
  source_path
}
```

---
## 7) Existing Task Detection
- scan tasks.md for perf/load/reliability tasks
- classify by type: load, stress, soak, spike, chaos-reliability, UX-perf
- avoid generating duplicates
- propose `extends` or `refines` where appropriate

---
## 8) Proposed Task Generation
For each NFR:
- propose tasks with:
  - type (load/stress/soak/spike/...)
  - environment
  - acceptance criteria
  - intensity-level
  - preferred-tools
  - dependency/service notes
  - relationship to existing tasks

Under strict mode:
- ensure coverage of all NFRs
- label critical tasks as required

---
## 9) UI Addendum (v5.7)
If UI/UX NFRs present:
- tasks for synthetic journeys
- measure UX metrics (LCP/TTI/latency)
- use UI JSON metadata when available
- if UI JSON missing: warning only

---
## 10) Plan Assembly
- group tasks by spec-id, environment
- include mapping NFR → tasks
- include cross-repo context (ownership, dependencies)
- include proposed_nfrs section (optional; non-binding)

---
## 11) Output Generation
Write to target directory:
- `<timestamp>_<plan-label>.md`
- `<timestamp>_<plan-label>.json` (if requested)

Markdown sections:
- overview
- scope
- extracted NFRs
- existing vs proposed tasks
- proposed scenarios by environment
- dependencies + registry notes
- optional proposed_nfrs

---
## 12) KiloCode Behavior
- `--kilocode` → Ask/Architect (read-only)
- Orchestrator-per-NFR when subtasks enabled
- Orchestrator decomposes NFR → scenarios → tasks
- code/analysis modes inspect existing tasks

---
## 13) Weakness & Risk Check
Ensure:
- NO-WRITE always respected
- never modify specs/tasks/registries/UI JSON/CI configs
- never redefine NFRs (only propose)
- never invent spec-ids
- avoid duplicates
- align tasks with verifier expectations

---
## 14) Legacy Flags Inventory
Kept:
- `--strict` (alias)

Additive-only:
- All other flags remain; behavior unchanged from v5.6.2

