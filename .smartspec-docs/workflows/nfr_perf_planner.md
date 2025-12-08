---
manual_name: /smartspec_nfr_perf_planner Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_nfr_perf_planner
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (SRE, platform, tech leads, performance owners)
---

# /smartspec_nfr_perf_planner Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_nfr_perf_planner v5.6.2`

The workflow helps you:

> "Turn existing NFRs/SLOs into **performance / load / reliability test
> tasks** that can be added to `tasks.md` or other planning systems in a
> consistent way."

Key properties:

- Role: **design / planning / prompt-generating**
- `write_guard: NO-WRITE`
  - does **not** modify `tasks.md`, CI, or code directly
  - produces **proposed** perf plans and task snippets
- Designed to work alongside:
  - `/smartspec_nfr_perf_verifier` (which checks whether NFRs are actually
    met using test reports and metrics)

In short:

- **planner** = generate perf/load/reliability tasks from NFRs
- **verifier** = check whether NFRs are met based on executed tests and data

---

## 2. What’s New in v5.6

Version 5.6.2 strengthens the planner and closes key gaps:

### 2.1 Clear separation from verifier

- Planner focuses on **what to test** (tasks, scenarios), not outcomes.
- Verifier focuses on **whether targets are met**.
- Prevents the planner from accidentally taking on governance duties.

### 2.2 No direct writes to task files

- `write_guard: NO-WRITE` is enforced at workflow level.
- Primary output is a **perf plan** file under:
  - `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_<plan-label>.{md|json}`
- Humans or separate sync tooling decide which tasks to merge into `tasks.md`.

### 2.3 Respect existing NFRs (no threshold changes)

- NFRs must come from:
  - specs / SPEC_INDEX / policies / registries
- The planner must **not**:
  - change thresholds/SLOs
  - declare new NFRs as official
- New NFR ideas should be placed into a `proposed_nfrs` section, clearly
  marked as non-binding.

### 2.4 Multi-repo & shared service safety

- Uses `--repos-config` and registries to:
  - detect service ownership
  - avoid pushing heavy scenarios into many repos
- Heavy scenarios are generally assigned to the **owning repo** for a shared
  service, while consumer repos get lighter smoke checks if needed.

### 2.5 Safety-mode for planning

- `normal` mode:
  - can propose broader or experimental scenarios
  - can include optional tasks, clearly marked as such

- `strict` mode:
  - aims to give **every critical NFR** at least one or two tasks
  - avoids scenarios that contradict policy unless labeled experimental
  - marks tasks required to produce evidence for critical NFRs as
    `priority=high`

---

## 3. Backward Compatibility Notes

- Manual v5.6 targets `/smartspec_nfr_perf_planner` from **v5.6.2 onwards**
  (5.6.x).
- No legacy flags or behavior are removed (this is a new workflow).
- `--strict` remains an alias for `--safety-mode=strict`.
- Path and canonical folder rules match other SmartSpec workflows.

---

## 4. Core Concepts

### 4.1 NFR → Testable criteria → Tasks

Typical planner flow:

1. Read NFRs from spec / SPEC_INDEX / policies.
2. Convert them into **testable criteria**, e.g.:
   - P95 latency <= 300ms under X req/s
   - error rate < 0.1% under typical daily load
3. From those criteria, generate **perf/load tasks**, such as:
   - build k6 scenario A for `/checkout`
   - run a 2h soak test at 70% peak load

### 4.2 Perf plan vs tasks.md

- The perf plan is a **proposal** document.
- `tasks.md` is the authoritative list of committed tasks.
- The planner reduces manual work when translating NFRs into tasks, but does
  not overwrite or auto-edit `tasks.md`.

### 4.3 Relationship with verifier

- Planner should design tasks such that:
  - once implemented and executed, their reports/metrics become
    easy-to-consume evidence for `/smartspec_nfr_perf_verifier`.

---

## 5. Quick Start Examples

### 5.1 Plan perf tasks for a single service

```bash
smartspec_nfr_perf_planner \
  --spec-ids=checkout_api \
  --plan-label=checkout-perf-plan \
  --nfr-policy-paths=".spec/policies/nfr/*.md" \
  --target-envs=staging,prod \
  --preferred-tools=k6,jmeter \
  --intensity-level=normal \
  --plan-format=md \
  --stdout-summary
```

Result:

- Plan at:
  `.spec/suggestions/smartspec_nfr_perf_planner/<timestamp>_checkout-perf-plan.md`
- Contains NFR → proposed tasks per environment.

### 5.2 Strict planning for a core service

```bash
smartspec_nfr_perf_planner \
  --spec-ids=core_payments \
  --plan-label=core-payments-perf \
  --target-envs=staging,prod \
  --safety-mode=strict \
  --preferred-tools=k6 \
  --intensity-level=heavy \
  --stdout-summary
```

In strict mode:

- Attempts to cover every critical NFR with at least one or two tasks.
- Marks tasks needed to produce evidence for critical NFRs as
  `priority=high`.

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--plan-label=<string>`

### 6.2 NFR & policy

- `--nfr-policy-paths="..."`

### 6.3 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (or `--strict`)

### 6.4 Planning options

- `--target-envs="dev,staging,prod"`
- `--preferred-tools="k6,jmeter,locust,gatling"`
- `--intensity-level=<light|normal|heavy>`
- `--max-tasks-per-nfr=<int>`

### 6.5 Output & KiloCode

- `--plan-format=md|json`
- `--plan-dir=.spec/suggestions/smartspec_nfr_perf_planner/`
- `--stdout-summary`
- `--kilocode`, `--nosubtasks`

---

## 7. Reading a perf plan

A typical plan file (md/json) includes:

- spec-ids and environments
- NFR → tasks mapping
- For each task:
  - type: `load`, `stress`, `soak`, `spike`, `chaos_reliability`,
    `latency_sampling`, etc.
  - target environment(s)
  - tool hints (from `--preferred-tools`)
  - intensity/duration
  - acceptance criteria
  - relation to existing tasks (`extends`, `duplicate_of`, etc.)
  - whether it is `required` or `optional`

All tasks are **proposals** – teams choose what to adopt.

---

## 8. KiloCode Usage Examples

### 8.1 Planner on Kilo

```bash
smartspec_nfr_perf_planner \
  --spec-ids=checkout_api \
  --plan-label=checkout-perf-plan \
  --target-envs=staging,prod \
  --preferred-tools=k6 \
  --kilocode \
  --stdout-summary
```

Under Kilo:

- Orchestrator enumerates NFRs and turns each into candidate scenarios.
- Code mode inspects current `tasks.md` to reduce duplication.
- Orchestrator assembles a single coherent perf plan.

### 8.2 Disabling subtasks

```bash
smartspec_nfr_perf_planner \
  --spec-ids=small_service \
  --plan-label=small-service-perf \
  --target-envs=staging \
  --kilocode \
  --nosubtasks
```

- Uses a simpler, single-flow reasoning path – good for small scopes.

---

## 9. Multi-repo / Shared Service Examples

### 9.1 Monorepo with multiple services

```bash
smartspec_nfr_perf_planner \
  --spec-ids=search_api,ranking_service \
  --plan-label=search-stack-perf \
  --target-envs=staging,prod \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --preferred-tools=k6,locust
```

- Uses registry + repos-config to place scenarios at appropriate services.
- Avoids cloning heavy scenarios across all services.

### 9.2 Shared service / platform owner

```bash
smartspec_nfr_perf_planner \
  --spec-ids=platform_auth \
  --plan-label=platform-auth-perf \
  --target-envs=prod \
  --registry-dir=.spec/registry \
  --safety-mode=strict
```

- Heavy scenarios are proposed in the owning repo.
- Consumer repos get lighter smoke checks where appropriate.

---

## 10. UI/UX Perf Tasks

If specs contain UI/UX NFRs, such as:

- LCP, TTI, input latency, responsiveness

The planner can:

- propose tasks for:
  - synthetic user journeys on key flows
  - Web Vitals collection in synthetic or RUM setups
- Respect UI governance from SPEC_INDEX/config:
  - JSON-first UI: may reference `ui.json` to identify screens/flows
  - opt-out: avoids assuming `ui.json` exists, but still proposes E2E/UX
    perf tasks

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Run the planner **after** NFRs are reasonably defined.
- Review perf plans collaboratively before merging tasks into `tasks.md`.
- Make `plan-label` meaningful (release name, initiative, etc.).
- Use `--safety-mode=strict` for core/critical services.
- Store perf plans in version control with specs.
- Ensure planner/verifier share the same NFR sources to avoid drift.

### 11.2 Anti-patterns

- Expecting the planner to adjust specs/NFRs by itself (it cannot).
- Blindly merging all suggested tasks without review.
- Ignoring existing tasks, leading to duplicated scenarios.

---

## 12. FAQ / Troubleshooting

### Q1: What if there are no NFRs defined yet?

- The planner may only produce generic `proposed_nfrs` and sample tasks.
- You should first define NFRs in specs/policies, then re-run the planner.

### Q2: What if perf tasks already exist?

- The planner attempts to scan `tasks.md` to avoid duplicates.
- When similar tasks are required, it should mark them as `extends` or
  `refines` rather than duplicating them.

### Q3: Do I need both planner and verifier?

- Not strictly required, but strongly recommended:
  - planner → shapes coverage
  - verifier → checks if NFRs are met

---

End of `/smartspec_nfr_perf_planner v5.6.2` manual (English).
If future versions change semantics or add major modes, issue a new manual
(e.g., v5.7) and document compatible workflow versions clearly.
