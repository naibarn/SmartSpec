---
name: /smartspec_observability_runbook_generator
version: 5.6.2
role: design/planning (runbook generation)
write_guard: NO-WRITE
purpose: Generate observability runbooks (incident/runbook guides) from
         existing specs, SLOs, alerts, dashboards, logs/traces
         configuration, without modifying code, configs, CI, or
         observability systems.
---

## 1) Summary

`/smartspec_observability_runbook_generator` reads SmartSpec artifacts and
observability-related configuration and generates **observability runbook
documents** as suggestions.

Runbooks are intended for:

- on-call and SREs handling incidents
- developers debugging production/staging issues
- platform and observability engineers maintaining shared runbooks

The workflow focuses on:

- discovering **critical paths** and **SLOs/NFRs** from specs/registries
- mapping them to **alerts, dashboards, metrics, logs, traces**
- generating **structured runbooks** per service/spec-id (and optionally
  per incident-type or symptom)
- keeping **ownership and boundaries** clear in multi-repo/multi-service
  environments

> **Planner / generator only**
>
> - This workflow **does not** modify dashboards, alerts, or code.
> - It **proposes** runbook content as markdown/JSON under `.spec/`.
> - Humans or other workflows may later sync/merge runbooks into
>   official docs or tools.
>
> **Sensitive data rule:**  
> - Runbooks MUST NOT reproduce secrets, tokens, passwords, private keys,
>   or sensitive PII from logs/traces (e.g., full card numbers,
>   national IDs).
> - They MAY reference the existence and location of such issues (e.g.,
>   “user PII appears in log X”) but must not copy raw values.

Use this workflow when you want **consistent, SmartSpec-aligned
observability runbooks** for services, features, and critical flows.

---

## 2) When to Use

Use `/smartspec_observability_runbook_generator` when:

- services already have:
  - specs + SPEC_INDEX
  - SLOs / NFRs (latency, error rate, availability, etc.)
  - some combination of:
    - alert rules
    - dashboards (metrics)
    - logging/tracing configurations
- you want:
  - **standardized runbooks** for incident response
  - to improve on-call readiness
  - better linkage between SLOs → alerts → dashboards → runbooks

Typical chain:

`generate_spec → define_SLOs/NFRs → configure_observability (alerts/dashboards/logs) → /smartspec_observability_runbook_generator → review/merge_runbooks → on-call usage → /smartspec_release_readiness`

Do **not** use this workflow to:

- create or modify alert rules and dashboards directly
- change SLOs/NFRs (it may suggest gaps, but cannot declare new SLOs)
- manage real-time incident execution (it only provides runbook content)

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts, read-only)

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs & tasks**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`
  - any observability-specific docs referenced from spec or SPEC_INDEX
    (e.g., `observability.md`, `slo.md`, `runbook_notes.md`)

- **SLO / NFR artifacts (optional)**
  - SLO/NFR documents referenced by SPEC_INDEX
  - `.spec/registry/slo-registry.json` (if defined)
  - `.spec/registry/critical-sections-registry.json`

- **Service and topology registries (optional)**
  - `.spec/registry/service-registry.json`
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-classification-registry.json`

- **Observability configuration (optional, read-only)**
  - any paths matching:
    - `--alert-config-paths` (alert rule definitions)
    - `--dashboard-config-paths` (dashboard/chart definitions)
    - `--log-config-paths` (log pipelines, routing, formats)
    - `--trace-config-paths` (tracing setup: spans, sampling rules)
    - `--runtime-metrics-paths` (exporter configs, metrics naming docs)

All artifacts are treated as **read-only** context.

### 3.2 Inputs (flags)

See **5) Flags**.

### 3.3 Outputs

- **Runbook suggestions** (per spec-id/service)
  - default location:
    `.spec/suggestions/smartspec_observability_runbook_generator/<timestamp>_<runbook-label>.md`
  - optional JSON representation:
    `.spec/suggestions/smartspec_observability_runbook_generator/<timestamp>_<runbook-label>.json`

A typical runbook (per service/spec-id) includes:

- metadata:
  - spec-id, service name, environment(s)
  - primary owner / team (if registry provides)
- **scenarios / incident types**, such as:
  - SLO breach (latency, error rate, availability)
  - high error rate on specific API
  - saturation (CPU/memory/disk/queue)
  - dependency issues (upstream/downstream problems)
- for each scenario:
  - symptom/alert patterns (e.g., specific alerts, SLO burn)
  - **where to look**:
    - dashboards & metrics queries
    - log queries and trace filters
  - **how to diagnose** (step-by-step checks)
  - **how to mitigate / rollback**:
    - known playbooks
    - feature flags / traffic shifting / rate limiting
    - rollback paths (via existing deployment/change processes)
  - **post-incident**:
    - verification checks
    - follow-up items (e.g., add alerts, refine SLOs, improve dashboards)

Optionally, a **stdout summary** when `--stdout-summary` is set.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **design / planning / runbook-generation**
- Write guard: **NO-WRITE**

MUST NOT:

- modify specs, tasks, CI configs, alert/dashboards, or code
- push changes to observability backends or tools
- manage live incidents or execute runbook steps

MAY:

- read artifacts and configs as inputs
- generate proposed runbook content (markdown/JSON)
- print human-readable summaries

### 4.2 Platform semantics

- Tool-agnostic w.r.t. observability vendors (no vendor lock-in).

- Under Kilo (with `--kilocode` and Kilo detected):

  - effective mode: **Ask / Architect (READ-ONLY)** with **NO-WRITE**
  - must follow **Kilo Orchestrator-per-task rule**:
    - **before each top-level task** (each spec-id / service runbook),
      switch to Orchestrator to decompose subtasks, unless `--nosubtasks`
      is explicitly set.
  - default under Kilo is **subtasks ON**; `--nosubtasks` is an explicit
    opt-out.

  - typical loop:
    1) Orchestrator selects one spec-id/service (top-level task).
    2) Subtasks:
       - gather SLOs/NFRs and critical paths
       - collect observability configs (alerts/dashboards/logs/traces)
       - synthesize scenarios and runbook sections
    3) Code mode (read-only) parses configs and SPEC_INDEX.
    4) Orchestrator assembles the runbook for that spec-id.
    5) Repeat for the next spec-id.

- If `--kilocode` is present but Kilo is not detected:
  - treat `--kilocode` as a **no-op meta-flag**
  - continue with a single reasoning flow

Write guard stays **NO-WRITE** in all modes.

---

## 5) Flags

> No legacy flags are removed or changed. All flags below are additive.

### 5.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
  - spec-ids for which runbooks should be generated
  - all IDs must exist in SPEC_INDEX

- `--include-dependencies`
  - expand scope (via SPEC_INDEX + registries) to include dependent
    services (e.g., upstream APIs, shared auth/logging/gateway services)

- `--runbook-label=<string>`
  - label for this runbook generation run
  - used in filenames and headings
  - e.g., `checkout-observability`, `q4-2025-runbooks`

### 5.2 Environment

- `--target-envs=<env1,env2,...>`
  - e.g., `dev,staging,prod`
  - used mainly for contextual differences (e.g., different alert thresholds)

### 5.3 Observability configuration paths

- `--alert-config-paths="<glob1>;<glob2>;..."`
- `--dashboard-config-paths="<glob1>;<glob2>;..."`
- `--log-config-paths="<glob1>;<glob2>;..."`
- `--trace-config-paths="<glob1>;<glob2>;..."`
- `--runtime-metrics-paths="<glob1>;<glob2>;..."`

All are **read-only** sources; the workflow does not change them.

### 5.4 Multi-repo / registry / index / safety

- `--workspace-roots="<path1>;<path2>;..."`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots="<path1>;<path2>;..."`
- `--index=<path>` / `--specindex=<path>`
- `--safety-mode=<normal|strict>`
  - `--strict` is a legacy alias for `--safety-mode=strict`.

Semantics:

- `--repos-config` is preferred to map spec-ids → repos/services.
- `--workspace-roots` is only a discovery hint if `--repos-config` is missing.
- `--registry-dir` is the primary registry root (default `.spec/registry`).
- `--registry-roots` are read-only supplemental registries.

**Safety mode behavior:**

- `normal` (default):
  - generator may include exploratory suggestions
  - clearly marks “optional” vs “standard” steps
  - observability gaps (e.g., SLO without corresponding alerts) are
    documented under an `observability_gap` or similar section, not as
    existing steps.

- `strict`:
  - for each `critical` / `high` SLO or critical section:
    - the runbook must either:
      - provide at least a baseline scenario + troubleshooting path, or
      - clearly declare an `observability_gap` for that SLO/section.
  - must **not** suggest runbook steps that violate production safety
    or governance (e.g., ad-hoc DB writes) as default actions.
    - if such operations are mentioned, they must be:
      - clearly labeled as “requires additional approvals/change process”
      - non-default / last-resort, and ideally reference a separate,
        approved change runbook.

### 5.5 Output control

- `--runbook-format=<md|json>`
  - default: `md`

- `--runbook-dir=<path>`
  - default: `.spec/suggestions/smartspec_observability_runbook_generator/`

- `--stdout-summary`
  - print a short summary (services covered, number of scenarios, gaps)

### 5.6 Kilo / subtasks

- `--kilocode`
- `--nosubtasks`
  - disables automatic subtask decomposition even under Kilo;
    still uses Orchestrator-per-task rule conceptually but performs
    reasoning in a single combined flow per spec-id.

---

## 6) Canonical Folders & File Placement

The workflow MUST follow SmartSpec canonical layout:

1. **Index detection order** (read-only):
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. **Specs & tasks**:
   - `specs/<category>/<spec-id>/spec.md`
   - `specs/<category>/<spec-id>/tasks.md`

3. **Registries**:
   - primary: `.spec/registry/`
   - supplemental (read-only): `--registry-roots`

4. **Runbook suggestions (outputs)**:
   - default root:
     `.spec/suggestions/smartspec_observability_runbook_generator/`
   - file name pattern:
     `<timestamp>_<runbook-label>.{md|json}`

The workflow MUST NOT create new top-level folders outside `.spec/` by
default.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow spec as complete, verify that it:

1. **Respects NO-WRITE**
   - never modifies configs, alerts, dashboards, CI, or code
   - only generates runbook content as output.

2. **Avoids guessing observability from thin air**
   - does not invent metrics/dashboards/alerts that contradict existing
     configs.
   - may propose *gaps* (e.g., “missing alert for SLO X”) but clearly
     labels them as proposals, not existing state.

3. **Aligns with SLO/NFRs**
   - ensures runbook sections are anchored in real SLOs/NFRs where available.
   - under `strict`, every critical/high SLO or critical section is either:
     - covered by at least one runbook scenario, or
     - logged as an explicit `observability_gap`.

4. **Respects multi-repo ownership**
   - uses registries + `--repos-config` to map services and dependencies.
   - does not assign remediation steps outside the owning team without
     marking them as cross-team coordination.

5. **Protects sensitive data**
   - does not reproduce secrets, tokens, passwords, private keys.
   - avoids including raw PII (e.g., full card numbers, national IDs) in
     log/trace examples.
   - instead references patterns/locations (e.g., “login error logs”) only.

6. **Keeps incident execution out of scope**
   - does not claim to execute runbook steps or change system state.
   - focuses on documentation, guidance, checklists.

7. **Uses safety-mode consistently**
   - `normal` vs `strict` behaviors clearly differentiated.
   - “dangerous” operations (e.g., direct DB changes, disabling safeguards)
     are either omitted or clearly marked as non-default and subject to
     separate approval/change processes.

---

## 8) Legacy Flags Inventory

New workflow:

- **Kept as-is**:
  - (none – new workflow)

- **Legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--runbook-label`
  - `--target-envs`
  - `--alert-config-paths`
  - `--dashboard-config-paths`
  - `--log-config-paths`
  - `--trace-config-paths`
  - `--runtime-metrics-paths`
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`
  - `--registry-roots`
  - `--index`
  - `--specindex`
  - `--safety-mode`
  - `--runbook-format`
  - `--runbook-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

As a planning/runbook-generating workflow:

- accepts `--kilocode`.
- role under Kilo: **Ask / Architect**, **READ-ONLY**, **NO-WRITE**.
- follows **Kilo Orchestrator-per-task rule**:
  - before each top-level task (each spec-id runbook), use Orchestrator
    to decompose into subtasks (unless `--nosubtasks` is set).

### 9.1 Orchestrator loop (Kilo + subtasks)

For each selected spec-id/service:

1. Orchestrator groups:
   - SLOs/NFRs.
   - critical endpoints/flows.
   - dependencies (from registries).
2. Code mode (read-only) inspects:
   - observability configs (alerts/dashboards/logs/traces).
   - specs/tasks for additional hints (e.g., health checks).
3. Orchestrator generates a structured runbook:
   - scenarios, signals, where-to-look, diagnosis, mitigation, verification.

### 9.2 Non-Kilo environments

- treat `--kilocode` as no-op.
- perform the same logical sequence in a single reasoning flow.

---

## 10) Inline Detection Rules

The workflow must not call other SmartSpec workflows for detection.
Instead, it:

1. inspects environment/system prompts for Kilo/ClaudeCode/Antigravity
   markers.
2. checks for presence of `--kilocode`.
3. if ambiguous, defaults to tool-agnostic behavior and may note in the
   runbook header that no specific platform was detected.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` (when provided) to map spec-ids to repos/services.
2. Use `--workspace-roots` only as a discovery hint, never to invent
   spec-ids outside SPEC_INDEX.
3. Use registries (service/API/data/critical-sections) to:
   - identify critical paths and cross-service flows.
   - highlight shared infrastructure (e.g., auth gateway, logging layer).
   - suggest where shared/global runbooks might help.
4. For cross-service scenarios:
   - include all involved services in the runbook.
   - clearly describe where to look in each service’s observability stack.
   - keep ownership clear for each service/team.

---

## 12) UI Addendum (Observability Runbooks for UI)

For UI-facing specs, the generator should:

1. Identify UI-related SLOs/NFRs (e.g., page load, error rate, UX latency).
2. Link runbook steps to:
   - frontend metrics (Web Vitals, JS error rate, front-end latency).
   - backend API metrics powering UI.
   - logs/traces tied to specific routes/components.
3. Respect UI governance from SPEC_INDEX/config:
   - **JSON-first UI**:
     - may reference `ui.json` to list screens/flows and map them to
       metrics/dashboards/logs/traces.
   - **UI JSON opt-out / inline UI**:
     - avoid assuming `ui.json` exists.
     - still propose E2E/UX-centric scenarios based on specs and configs.

---

## 13) Best Practices (for Users)

- Define SLOs/NFRs and set up basic observability (alerts/dashboards/logs)
  before generating runbooks, for best results.
- Run the generator:
  - after significant observability changes.
  - before major releases.
  - periodically for core services (e.g., quarterly).
- Review generated runbooks with on-call/SRE teams before adopting them.
- Store runbook suggestions in version control and track their evolution.
- Use `--safety-mode=strict` for core, high-value systems.
- Be careful not to paste raw PII or secrets when manually editing runbooks.
- Combine runbook insights with `/smartspec_release_readiness` to assess
  operational readiness.

---

## 14) For the LLM / Step-by-Step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve scope**
   - parse `--spec-ids`, `--include-dependencies`, `--runbook-label`,
     `--target-envs`.
   - load SPEC_INDEX in canonical order.
   - validate all spec-ids exist.
   - expand to dependent specs if requested.

2. **Gather artifacts**
   - load specs/tasks for selected spec-ids.
   - load SLO/NFR docs and registries (SLO, service, API, critical-sections).
   - load observability configs from all `--*config-paths`.

3. **Identify critical paths & SLOs**
   - per spec-id: extract critical user journeys, endpoints, and SLOs.
   - record criticality (critical/high/medium/low).

4. **Map observability coverage**
   - for each critical path/SLO:
     - map to alerts, dashboards, metrics, logs, traces.
     - note missing elements as potential `observability_gap` items.

5. **Generate runbook content**
   - per spec-id/service:
     - define scenarios (SLO breach, high error rate, saturation, etc.).
     - for each scenario:
       - describe symptoms and triggering alerts.
       - list dashboards/metrics/log/trace queries (no raw secrets/PII).
       - propose diagnosis steps.
       - propose mitigations that align with policy (no unsafe ad-hoc ops).
       - propose verification checks and follow-ups.

6. **Apply safety-mode**
   - in `strict`:
     - ensure every critical/high SLO or critical section is either
       covered or reported as an `observability_gap`.
     - avoid unsafe operational steps as defaults.

7. **Write runbook output**
   - serialize to `.md` or `.json` in `--runbook-dir`.
   - include metadata about scope and inputs used.

8. **Optional stdout summary**
   - if `--stdout-summary`, print:
     - number of services/spec-ids processed.
     - number of runbooks generated.
     - count of scenarios and observability gaps.

### 14.2 Stop conditions

The workflow MUST stop after:

- writing (or simulating writing) the runbook suggestion file(s), and
- printing any optional stdout summary.

It MUST NOT:

- modify specs, tasks, CI, or observability configs.
- call or orchestrate other SmartSpec workflows directly.
- execute runbook steps or change system state.

