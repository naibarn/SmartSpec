---
name: /smartspec_nfr_perf_planner
version: 5.6.2
role: design/planning
write_guard: NO-WRITE
purpose: Plan and generate performance/load/reliability test task proposals
         and scenarios from existing NFRs and SLOs, without modifying specs,
         tasks, CI, or code directly.
---

## 1) Summary

`/smartspec_nfr_perf_planner` reads SmartSpec artifacts and NFR definitions
and produces **performance/load/reliability test task plans** that engineers
can review and merge into `tasks.md` or other planning artifacts.

It focuses on:

- extracting NFRs (latency, throughput, error rate, availability, resource,
  UX timings, etc.) from specs, SPEC_INDEX, and policy files
- mapping NFRs to concrete **testable criteria** (metrics, thresholds,
  workloads, conditions)
- proposing **performance/load/reliability test tasks** grouped by spec-id
  and environment
- optionally suggesting tool-specific patterns (e.g., k6, JMeter, Locust,
  Gatling) without binding the project to any single tool

> **Planner-only:**
> This workflow is a **planner / prompt generator**. It proposes perf/load
> tasks but does *not* write them into `tasks.md` or any CI/test configs.
> Humans or separate sync workflows apply the plan.

It is the natural complement to `/smartspec_nfr_perf_verifier`:

- **planner**: generates perf/load tasks based on existing NFRs
- **verifier**: checks later whether those NFRs are actually met based on
  executed tests and metrics

The workflow is:

- **design/planning-only** with `write_guard: NO-WRITE`
  - outputs **proposed task content/snippets** as plan files and/or stdout
  - does NOT modify `tasks.md`, CI, or code

Use this workflow when you want to turn NFRs into concrete perf/load test
work items in a consistent, SmartSpec-aligned way.

---

## 2) When to Use

Use `/smartspec_nfr_perf_planner` when:

- NFRs (SLOs) have been defined but performance/load tests are incomplete or
  missing
- you want to standardize how teams express perf/load test tasks
- you are starting a new service and want NFR-aligned perf test tasks from
  day one
- you are introducing `/smartspec_nfr_perf_verifier` and need test coverage
  that produces the required evidence

Typical chain:

`generate_spec → generate_plan → generate_tasks → implement_core_logic → /smartspec_nfr_perf_planner → implement_perf_tasks → run_perf_tests → /smartspec_nfr_perf_verifier → /smartspec_release_readiness`

Do **not** use this workflow to:

- run performance/load tests
- declare new NFRs as official policy (it may suggest them, but cannot
  promote them by itself)
- modify `tasks.md`, CI configs, or code directly

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts)

Read-only:

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs & tasks**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`
  - optional `nfr.md` or other NFR documents referenced from SPEC_INDEX or
    spec

- **NFR/policy files (optional)**
  - paths in `--nfr-policy-paths` (org/team-level NFR standards)

- **Registries (optional)**
  - `.spec/registry/service-registry.json` (service topology)
  - `.spec/registry/api-registry.json`
  - `.spec/registry/critical-sections-registry.json`
  - `.spec/registry/slo-registry.json` (if defined)

Existing artifacts are used to:

- detect missing perf tasks
- avoid duplicating existing tasks
- understand service dependencies and critical paths

### 3.2 Inputs (flags)

See **5) Flags**.

### 3.3 Outputs

- **Perf test plan file** (proposed tasks + scenarios)
  - default location:
    - `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_<plan-label>.md`

The plan should include, per spec-id and environment:

- list of **proposed tasks** for performance/load/reliability testing
- mapping from NFR → one or more test tasks
- proposed attributes per task, such as:
  - type: `load`, `stress`, `soak`, `spike`, `latency_sampling`,
    `chaos_reliability`, etc.
  - target environment(s)
  - suggested tools (non-binding; based on `--preferred-tools` when present)
  - notes and acceptance criteria
  - relationship to existing tasks (e.g., `extends_task_id`, `duplicate_of`)

Optionally, a **JSON companion** file for machine processing may be created
if `--plan-format=json` is used:

- `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_<plan-label>.json`

Optional **stdout summary** when `--stdout-summary` is enabled.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **design/planning / prompt-generating**
- Write guard: **NO-WRITE**

MUST NOT:

- modify `tasks.md` directly
- modify specs, registries, CI configs, or code

MAY:

- read all allowed artifacts
- generate suggested task content/snippets as plan files or text

### 4.2 Platform semantics

- Tool-agnostic by default.

- Under Kilo (with `--kilocode` and Kilo detected):
  - Effective mode: **Ask / Architect (READ-ONLY)**
  - Use **Orchestrator-per-NFR** when subtasks are enabled:
    - For each NFR, Orchestrator decomposes into candidate scenarios and
      tasks.
    - Code mode (read-only) inspects existing tasks to avoid duplicates.
    - Orchestrator assembles structured task proposals.

- If Kilo is not detected:
  - treat `--kilocode` as no-op
  - generate proposals in a single reasoning flow

Write guard stays **NO-WRITE** in all modes.

---

## 5) Flags

> No legacy flags are removed; all flags below are additive.

### 5.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
  - scope of specs whose NFRs should be turned into perf tasks
  - all IDs must exist in SPEC_INDEX

- `--include-dependencies`
  - also generate tasks for dependent specs (e.g., upstream services)

- `--plan-label=<string>`
  - label for this plan, used in filenames/headings
  - e.g., `checkout-perf-plan`, `q4-nfr-planning`

### 5.2 NFR & policy inputs

- `--nfr-policy-paths="<glob1>;<glob2>;..."`
  - global/team-level NFR policies and examples

### 5.3 Multi-repo / registry / index / safety

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

**Safety mode behavior:**

- `normal` (default):
  - planner may:
    - propose broader or experimental scenarios
    - suggest optional tasks beyond strict policy, clearly marked as
      `optional`.

- `strict` / `--strict`:
  - planner must:
    - cover all NFRs without silently omitting any
    - avoid proposing scenarios that *conflict* with defined policies
      (e.g., unrealistic loads beyond named capacity unless labeled as
      experiment)
    - mark tasks required to produce evidence for critical NFRs as
      `priority=high` in the plan structure.

### 5.4 Planning options

- `--target-envs="dev,staging,prod"`
  - environments you want perf tests for

- `--preferred-tools="k6,jmeter,locust,gatling"`
  - list of tools teams are comfortable with
  - planner may reference these in task descriptions

- `--intensity-level=<light|normal|heavy>`
  - hint for how aggressive scenarios should be (used in descriptions only)

- `--max-tasks-per-nfr=<int>`
  - optional upper bound to avoid over-generating tasks for a single NFR

### 5.5 Output control

- `--plan-format=<md|json>`
  - default: `md`

- `--plan-dir=<path>`
  - default: `.spec/suggestions/smartspec_nfr_perf_planner/`

- `--stdout-summary`
  - print a short summary of proposed tasks to stdout

### 5.6 Kilo / subtasks

- `--kilocode`
- `--nosubtasks`

---

## 6) Canonical Folders & File Placement

1. **Index detection order**:
   - `.spec/SPEC_INDEX.json` (canonical)
   - `SPEC_INDEX.json` at repo root
   - `.smartspec/SPEC_INDEX.json` (deprecated)
   - `specs/SPEC_INDEX.json` (older layout)

2. **Specs and tasks**:
   - `specs/<category>/<spec-id>/spec.md`
   - `specs/<category>/<spec-id>/tasks.md`

3. **Registries**:
   - `.spec/registry/` as primary
   - `--registry-roots` as read-only supplemental

4. **Perf plans (outputs)**:
   - `.spec/suggestions/smartspec_nfr_perf_planner/` as default root
   - file name: `<timestamp>_<plan-label>.{md|json}`

The workflow must not create new top-level folders outside `.spec/` by
default.

---

## 7) Weakness & Risk Check (Quality Gate)

Ensure this planner workflow:

1. **Respects NO-WRITE**
   - never edits `tasks.md`, CI configs, or code directly
   - all changes are proposals via plan files or stdout

2. **Avoids redefining NFRs**
   - NFRs come from specs/SPEC_INDEX/policies
   - planner must not change thresholds or declare new official NFRs
   - new NFR ideas must go into a `proposed_nfrs` or equivalent section
     within the plan, clearly labeled as non-binding

3. **Avoids duplicating tasks**
   - existing perf/load tasks in `tasks.md` should be detected and referenced
     to avoid suggesting exact duplicates
   - when similar tasks are needed, mark them as `extends` or `refines`
     existing tasks instead of new ones

4. **Aligns with verifier**
   - tasks generated here should be designed so that
     `/smartspec_nfr_perf_verifier` can later use their results as evidence
   - planner should prefer metrics and scenarios that map cleanly to NFR
     definitions

5. **Multi-repo safety**
   - do not assign tasks to repos/specs that do not exist in SPEC_INDEX
   - for shared services, prefer hosting heavy scenarios in the owner repo
     and lighter checks in dependent repos

6. **Tool neutrality**
   - suggestions may mention tools from `--preferred-tools`, but must not
     hard-bind the project to any specific vendor or SaaS

---

## 8) Legacy Flags Inventory

New workflow:

- **Kept as-is**: (none)

- **Legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--plan-label`
  - `--nfr-policy-paths`
  - `--workspace-roots`
  - `--repos-config`
  - `--registry-dir`
  - `--registry-roots`
  - `--index`
  - `--specindex`
  - `--safety-mode`
  - `--target-envs`
  - `--preferred-tools`
  - `--intensity-level`
  - `--max-tasks-per-nfr`
  - `--plan-format`
  - `--plan-dir`
  - `--stdout-summary`
  - `--kilocode`
  - `--nosubtasks`

---

## 9) KiloCode Support (Meta-Flag)

As a planning/prompt-generating workflow:

- accepts `--kilocode`
- role under Kilo: **Ask/Architect, READ-ONLY**
- uses Orchestrator-per-NFR when subtasks are enabled

### 9.1 Orchestrator loop (when Kilo + subtasks)

1. Enumerate NFRs per spec-id.
2. For each NFR, Orchestrator breaks it into candidate scenarios and tasks.
3. Code mode (read-only) inspects specs/tasks/registries to:
   - avoid duplicates
   - respect dependencies and critical sections
4. Orchestrator assembles tasks into a coherent plan per spec-id and
   environment.

### 9.2 Non-Kilo

- do the same steps in a single reasoning flow
- still respect NO-WRITE and all safety rules

---

## 10) Multi-repo / Multi-registry Rules

- Use `--repos-config` when available to map spec-ids to repos/services.
- Use `--workspace-roots` only as a discovery hint, never to invent
  spec-ids.
- Use registries to:
  - understand where traffic flows
  - identify critical sections and shared services that need perf tasks

Perf tasks for shared services should:

- favor the **owning repo** as the primary place to host heavy scenarios
- propose lighter/smoke perf checks in dependent repos, if needed

---

## 11) UI Addendum (UI/UX Perf Tasks)

For UI-facing specs with UX NFRs (LCP, TTI, input latency, etc.), the
planner should:

1. Generate tasks for:
   - synthetic user journeys
   - frontend perf measurement
   - capturing relevant UX metrics

2. Respect UI governance mode from SPEC_INDEX/config:
   - JSON-first vs inline UI is context to locate components/screens
   - it does not change the fact that tasks must map back to UX NFRs

3. If there is a UI JSON opt-out:
   - avoid proposing tasks that assume `ui.json` exists
   - still propose functional/UX perf tasks (e.g., E2E flows)

---

## 12) Best Practices (for Users)

- Run `/smartspec_nfr_perf_planner` after NFRs are reasonably defined.
- Review the generated perf plan and merge relevant tasks into `tasks.md`
  manually or via a separate sync workflow.
- Keep `plan-label` aligned with release or project names.
- Use `--safety-mode=strict` for critical/core services to ensure complete
  coverage of NFRs and avoid forgotten scenarios.
- Use the same NFR set for both planner and verifier to avoid drift.
- Store perf plans in version control alongside specs for traceability.

---

## 13) For the LLM / Step-by-Step Flow & Stop Conditions

### 13.1 Step-by-step flow

1. **Resolve scope**
   - parse `--spec-ids`, `--include-dependencies`, `--plan-label`
   - load SPEC_INDEX in canonical order
   - ensure spec-ids exist; do not guess

2. **Gather artifacts**
   - load specs/tasks for selected specs
   - load NFR/policy files
   - load relevant registries for topology/critical sections

3. **Extract NFRs**
   - identify NFRs per spec-id and environment (from specs/policies)
   - capture category, target/threshold, and any criticality markers

4. **Review existing perf tasks**
   - scan `tasks.md` for existing perf/load/reliability tasks
   - link new proposals to existing tasks where relevant
   - avoid suggesting exact duplicates

5. **Generate proposed perf tasks**
   - for each NFR, propose one or more tasks:
     - type, environment, tool hints, intensity, acceptance criteria
     - indicate whether each is `required` or `optional` according to
       safety-mode and policy

6. **Group into a plan**
   - group tasks by spec-id and environment
   - include mapping to NFRs and any notes about dependencies/ownership

7. **Write plan output**
   - serialize to `.md` or `.json` in `--plan-dir`
   - include a small section for `proposed_nfrs` if new NFR ideas emerge,
     clearly labeled as non-binding

8. **Optional stdout summary**
   - number of specs, tasks, and NFRs covered
   - highlight count of `required` vs `optional` tasks

### 13.2 Stop conditions

The workflow MUST stop after:

- writing (or simulating) the perf plan file(s)
- printing optional stdout summary

It MUST NOT:

- modify `tasks.md` directly
- modify specs, registries, CI configs, or code
- invoke other workflows directly (may reference them in narrative only).

