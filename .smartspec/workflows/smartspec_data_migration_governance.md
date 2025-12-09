---
name: /smartspec_data_migration_governance
version: 5.6.2
role: verification/governance
write_guard: NO-WRITE
purpose: Govern and assess data migration plans and executions against
         data model, classification, retention, compliance, residency,
         and safety requirements, without modifying code, configs, or
         running migration jobs.
---

## 1) Summary

`/smartspec_data_migration_governance` reads SmartSpec artifacts, data
models, migration plans, and related policies to produce a **data
migration governance report**.

It focuses on:

- discovering **data migration scope** from specs, registries, and
  migration plans
- checking alignment with:
  - data model and schema evolution
  - data classification and privacy rules
  - retention and legal/compliance requirements
  - data residency / region constraints
- assessing the presence and quality of:
  - backup strategy
  - rollback strategy
  - dry-run and verification steps
  - data quality validation
- identifying **gaps and risks** such as:
  - missing migration coverage for key datasets
  - risk of data loss, corruption, or privacy violations
  - missing backups or rollbacks
  - cross-region / residency issues
  - multi-tenant isolation/segmentation risks

> **Governance-only:**
> - This workflow does **not** create or modify migration scripts,
>   pipelines, or jobs.
> - It does **not** execute migrations.
> - It does **not** change schemas, configs, or data.
> - It only reads artifacts and produces a governance report.
>
> **Sensitive data rule:**
> - The report MUST NOT contain real data values, PII samples, or
>   secrets from migrated datasets.
> - It may refer to field names, table names, and schema-level
>   information only.
>
> **Executable code rule:**
> - The workflow may describe migration patterns conceptually but MUST
>   NOT emit ready-to-run SQL/ETL scripts labeled as "approved" or
>   implicitly safe to execute.

Use it when you want a **structured, SmartSpec-aligned view of whether
planned or executed data migrations are safe, compliant, reversible, and
release-ready**.

The `blocking_for_release` recommendations produced by this workflow are
intended to be consumed alongside other governance workflows such as
`/smartspec_release_readiness`; they provide an additional signal rather
than overriding other workflows.

---

## 2) When to Use

Use `/smartspec_data_migration_governance` when:

- you plan to:
  - migrate data between schemas, databases, or storage systems
  - introduce new columns/tables with backfill
  - deprecate or archive data according to policy
  - migrate data across regions or legal boundaries
- you have some combination of:
  - migration design docs (data migration specs)
  - migration scripts (SQL, ETL, batch/stream jobs)
  - data model / schema files
  - data classification / retention / residency policies
  - related runbooks and incident procedures

Typical chain:

`design_feature → design_data_model → design_migration_plan → implement_migration_scripts → dry_run / test_migration → /smartspec_data_migration_governance → /smartspec_release_readiness`

Do **not** use this workflow to:

- generate or edit SQL / ETL / pipeline code
- deploy or run migrations in any environment
- manage credentials or data access
- override legal or compliance decisions (it only surfaces issues)

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
  - migration-related docs referenced by spec / SPEC_INDEX
    (e.g., `data_migration.md`, `schema_evolution.md`)

- **Data model / schema (optional)**
  - any paths matching `--data-model-paths`
  - may include:
    - schema definition files (SQL, JSON, YAML)
    - ORM models (if referenced/described in docs)
    - migration metadata (e.g., versioned schema docs)

- **Data classification / policy (optional)**
  - `.spec/registry/data-classification-registry.json`
  - `.spec/registry/security-registry.json`
  - any paths matching:
    - `--data-policy-paths` (retention, privacy, residency policies)

- **Migration plan docs (optional)**
  - paths from `--migration-plan-paths`
  - human-readable plans describing:
    - source/target systems
    - datasets/tables/fields involved
    - migration phases and milestones
    - migration style (in-place, backfill, dual-write, etc.)
    - approximate data volume (if mentioned)

- **Migration scripts / jobs (optional)**
  - paths from:
    - `--migration-script-paths` (SQL/ETL/ELT scripts)
    - `--pipeline-config-paths` (ETL/ELT pipeline configs)
  - all treated as **read-only** for inspection only.

- **Verification / execution evidence (optional)**
  - any paths matching:
    - `--migration-report-paths` (dry-run / test migration / production run reports)
    - `--data-quality-report-paths` (data quality checks)
    - `--audit-log-paths` (migration activity logs, data access logs)

All artifacts are read-only.

### 3.2 Inputs (flags)

See **5) Flags**.

### 3.3 Outputs

- **Data migration governance report** (human-readable + structured)
  - default location:
    - `.spec/reports/smartspec_data_migration_governance/<timestamp>_<run-label>.md`
  - if `--report-format=json`:
    - `.spec/reports/smartspec_data_migration_governance/<timestamp>_<run-label>.json`

#### 3.3.1 Per-migration-unit status model

For each migration "unit" (e.g. table, dataset, shard, tenant segment),
the report SHOULD capture at least:

- `unit_id`:
  - identifier such as `<db>.<schema>.<table>`, dataset path, or
    a stable logical name.

- `data_class`:
  - derived from data-classification registries/policies when available,
    e.g. `critical`, `high`, `medium`, `low`.

- `coverage_status`:
  - `IN_SCOPE` – the unit is explicitly included in the migration plan.
  - `OUT_OF_SCOPE` – explicitly documented as not being migrated.
  - `UNKNOWN` – unclear if/how this unit is affected.

- `backup_status`:
  - `PRESENT` – clear, defined backup strategy exists.
  - `PARTIAL` – some backup, but with known gaps.
  - `NONE` – no backup strategy found.
  - `UNKNOWN` – unclear.

- `rollback_status`:
  - `PRESENT` – explicit rollback strategy with steps.
  - `WEAK` – implicit or weak rollback, high uncertainty.
  - `NONE` – no rollback strategy found.
  - `UNKNOWN` – unclear.

- `verification_status`:
  - `STRONG` – clear data-quality checks and reconciliation steps defined.
  - `BASIC` – minimal checks (e.g. row counts only).
  - `NONE` – no verification checks.
  - `UNKNOWN` – unclear.

- `policy_alignment_status`:
  - `ALIGNED` – appears consistent with known policies.
  - `RISKY_BUT_JUSTIFIED` – deviations documented with explicit rationale.
  - `VIOLATES` – conflicts with policies / requirements.
  - `UNKNOWN` – unclear or not enough information.

- `residency_risk_status`:
  - `NONE` – no cross-region/residency concern detected.
  - `POTENTIAL` – might cross regions/residency boundaries; requires review.
  - `CONFIRMED` – clearly crosses restricted boundaries.
  - `UNKNOWN` – no information.

- `migration_style` (best-effort inference from plans):
  - `IN_PLACE` – same storage, schema change with in-place updates.
  - `BACKFILL` – write-new-then-swap / backfill approach.
  - `DUAL_WRITE` – period of writing to both old and new stores.
  - `OTHER` – other documented pattern.
  - `UNKNOWN` – not described.

- `migration_volume` (best-effort categorical, if documented):
  - `SMALL` – limited subset / small table.
  - `MEDIUM` – moderate dataset.
  - `LARGE` – bulk/warehouse-scale data.
  - `UNKNOWN` – not specified.

- `multi_tenant_risk`:
  - `NONE` – not multi-tenant or no segmentation risk.
  - `POTENTIAL` – multi-tenant or per-customer segmentation implied,
    but handling is not fully clear.
  - `CONFIRMED` – clear risk of tenant mis-routing / data mixing.
  - `UNKNOWN` – cannot determine.

- `risk_level`:
  - `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` (overall governance risk).

- `blocking_for_release`:
  - `true` | `false` – recommendation for release gating.

- `notes`:
  - free-form explanation / rationale.

#### 3.3.2 Aggregated summary

The report SHOULD also include:

- counts of units by `risk_level`
- counts of units by `blocking_for_release`
- counts of units with:
  - `backup_status=NONE` or `rollback_status=NONE`
  - `policy_alignment_status=VIOLATES`
  - `residency_risk_status=CONFIRMED`
  - `multi_tenant_risk=CONFIRMED`

Optionally, a **stdout summary** when `--stdout-summary` is enabled.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **Verification / Governance**
- Write guard: **NO-WRITE**

MUST NOT:

- run migration scripts/jobs or alter schedules.
- modify schemas, configs, pipelines, or code.
- update policies or registry entries.

MAY:

- read artifacts and scripts as inputs.
- generate reports under `.spec/reports/smartspec_data_migration_governance/`.
- print textual summaries.

### 4.2 Platform semantics

- Tool/vendor-agnostic for DB/ETL platforms.

- Under Kilo (with `--kilocode` and Kilo detected):

  - effective mode: **Ask / Architect**, **NO-WRITE**.
  - must follow **Kilo Orchestrator-per-task rule**:
    - before each top-level task (each migration scope/spec-id/group),
      switch to Orchestrator and decompose subtasks, unless `--nosubtasks`
      is explicitly set.
  - default under Kilo is **subtasks ON**.

  - typical loop:
    1) Orchestrator selects one migration scope (e.g., one spec-id or
       logical group of datasets).
    2) Subtasks (examples):
       - identify datasets & data classes.
       - inspect migration plans/scripts.
       - assess backup/rollback/verification.
       - assess policy & residency.
    3) Code mode (read-only) inspects artifacts.
    4) Orchestrator synthesizes governance results for that scope.

- If `--kilocode` is present but Kilo is not detected:
  - treat `--kilocode` as a **no-op meta-flag**.
  - run a single-flow reasoning path.

Write guard stays **NO-WRITE** in all modes.

---

## 5) Flags

> All flags are additive; no legacy flags are changed.

### 5.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
  - spec-ids whose data migrations should be governed.
  - all IDs must exist in SPEC_INDEX.

- `--include-dependencies`
  - include dependent services/systems (from SPEC_INDEX + registries),
    e.g., upstream data producers, downstream consumers.

- `--run-label=<string>`
  - label for this governance run (used in filenames and headers).
  - e.g., `q4-2025-migration`, `user-table-migration-prod`.

### 5.2 Migration-specific scope

- `--migration-plan-paths="<glob1>;<glob2>;..."`
  - human-readable migration design docs.

- `--migration-script-paths="<glob1>;<glob2>;..."`
  - SQL/ETL/ELT scripts defining migrations.

- `--pipeline-config-paths="<glob1>;<glob2>;..."`
  - configs for batch/streaming pipelines used in migration.

- `--data-model-paths="<glob1>;<glob2>;..."`
  - data model/schema definition files.

### 5.3 Policy & classification

- `--data-policy-paths="<glob1>;<glob2>;..."`
  - data retention / privacy / residency policies.

(Plus registries under `--registry-dir` / `--registry-roots`, see
sections 6 and 11.)

### 5.4 Environment & residency

- `--source-env=<env>`
  - e.g., `staging`, `prod`, `legacy-prod`.

- `--target-env=<env>`
  - e.g., `prod`, `new-prod-region`.

- `--region-pairs="<src1:dst1;src2:dst2;...>"`
  - optional mapping of source→target regions for residency analysis.

### 5.5 Evidence of runs / tests

- `--migration-report-paths="<glob1>;<glob2>;..."`
  - execution reports for dry-runs / test migrations / actual runs.

- `--data-quality-report-paths="<glob1>;<glob2>;..."`
  - data quality verification reports post-migration.

- `--audit-log-paths="<glob1>;<glob2>;..."`
  - audit logs for migration activity, data access, etc.

### 5.6 Multi-repo / registry / index / safety

- `--workspace-roots="<path1>;<path2>;..."`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots="<path1>;<path2>;..."`
- `--index=<path>` / `--specindex=<path>`
- `--safety-mode=<normal|strict>`
  - `--strict` is a legacy alias for `--safety-mode=strict`.

Semantics:

- `--repos-config` is preferred for mapping spec-ids ↔ repos/services.
- `--workspace-roots` is a discovery hint only.
- `--registry-dir` is primary registry root (default `.spec/registry`).
- `--registry-roots` are read-only supplemental registries.

### 5.7 Safety-mode rules (normal vs strict)

**Normal (default)**

- Reports gaps & risks with recommendations.
- `blocking_for_release` used mainly for:
  - `CRITICAL` risk units, especially when:
    - `backup_status=NONE` or `rollback_status=NONE`, or
    - `policy_alignment_status=VIOLATES`, or
    - `residency_risk_status=CONFIRMED`.
- Some ambiguous cases may be non-blocking but still highlighted.

**Strict (`--safety-mode=strict` / `--strict`)**

Under strict mode, the workflow MUST apply at least these rules:

- For any unit with `data_class in {critical, high}`:

  - If `backup_status=NONE` or `backup_status=UNKNOWN` →
    `blocking_for_release=true`.

  - If `rollback_status=NONE` or `rollback_status=UNKNOWN` →
    `blocking_for_release=true`.

  - If `policy_alignment_status=VIOLATES` →
    `blocking_for_release=true`.

  - If `residency_risk_status=CONFIRMED` and policies do not clearly
    allow such movement →
    `blocking_for_release=true`.

  - If `verification_status=NONE` and `migration_style` is `BACKFILL`
    or `DUAL_WRITE` or `IN_PLACE` with `migration_volume=LARGE` →
    strongly prefer `blocking_for_release=true`, unless there is a
    clearly documented and bounded mitigation.

- For units with `data_class=medium`:
  - similar rules apply but may allow more discretion:
    - if combined risk (e.g., `backup_status=NONE` AND
      `migration_volume=LARGE`) is high, lean to blocking.

- For units with `data_class=low`:
  - blocking is typically reserved for clear policy violations or
    severe residency issues.

The workflow MUST explain in notes why `blocking_for_release=true`
was chosen for each unit.

### 5.8 Output control

- `--report-format=<md|json>`
  - default: `md`.

- `--report-dir=<path>`
  - default: `.spec/reports/smartspec_data_migration_governance/`.

- `--stdout-summary`
  - print a short summary to stdout.

### 5.9 Kilo / subtasks

- `--kilocode`
- `--nosubtasks`
  - disables Orchestrator auto-subtasking even under Kilo, but still
    follows the Orchestrator-per-task concept logically.

---

## 6) Canonical Folders & File Placement

The workflow MUST follow SmartSpec canonical layout:

1. **Index detection order (read-only)**:
   1) `.spec/SPEC_INDEX.json` (canonical).
   2) `SPEC_INDEX.json` at repo root (legacy).
   3) `.smartspec/SPEC_INDEX.json` (deprecated).
   4) `specs/SPEC_INDEX.json` (older layout).

2. **Specs & tasks**:
   - `specs/<category>/<spec-id>/spec.md`.
   - `specs/<category>/<spec-id>/tasks.md`.

3. **Registries**:
   - primary: `.spec/registry/`.
   - supplemental (read-only): `--registry-roots`.

4. **Reports (outputs)**:
   - default root:
     `.spec/reports/smartspec_data_migration_governance/`.
   - file name pattern:
     `<timestamp>_<run-label>.{md|json}`.

The workflow MUST NOT create new top-level folders outside `.spec/`
by default.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow spec as complete, verify that it:

1. **Preserves NO-WRITE**
   - does not modify migration scripts, schemas, pipelines, or configs.
   - does not execute migration jobs.

2. **Avoids "migration by guessing"**
   - does not invent migration steps contradicting the actual plans/scripts.
   - separates known facts from speculative proposals.

3. **Respects data classification & policies**
   - uses data classification and policy registries/docs.
   - does not redefine criticality or alter policy semantics.

4. **Enforces backup/rollback requirements under strict mode**
   - for critical/high data classes, missing/unknown backup or rollback
     must be blocking.
   - clearly calls out missing or weak strategies.

5. **Handles residency / cross-region transfers**
   - surfaces region pairs and potential policy conflicts.
   - under strict mode, cross-region movement of regulated data is
     treated as high risk unless clearly allowed by policy.

6. **Acknowledges migration style & volume**
   - uses migration style and volume (where inferable) as inputs to
     `risk_level` and strict-mode decisions.

7. **Accounts for multi-tenant / segmentation risks**
   - notes potential/confirmed risks where migration might break tenant
     isolation or mix data across tenants.

8. **Protects sensitive data in reports**
   - no raw data values, secrets, or PII samples.
   - uses schema-level names, dataset identifiers, and categories only.

9. **Respects multi-repo ownership**
   - uses SPEC_INDEX + registries + `--repos-config` for ownership
     mapping.
   - clearly marks cross-team dependencies.

10. **Maintains governance-only boundary**
    - does not generate executable migration scripts or operational
      runbooks.
    - may recommend follow-up workflows, but does not invoke them.

---

## 8) Legacy Flags Inventory

New workflow:

- **Kept as-is**:
  - (none – new workflow).

- **Legacy alias**:
  - `--strict` → alias for `--safety-mode=strict`.

- **New additive flags**:
  - `--spec-ids`
  - `--include-dependencies`
  - `--run-label`
  - `--migration-plan-paths`
  - `--migration-script-paths`
  - `--pipeline-config-paths`
  - `--data-model-paths`
  - `--data-policy-paths`
  - `--source-env`
  - `--target-env`
  - `--region-pairs`
  - `--migration-report-paths`
  - `--data-quality-report-paths`
  - `--audit-log-paths`
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

As a verification/governance workflow:

- accepts `--kilocode`.
- role under Kilo: **Ask / Architect**, **NO-WRITE**.
- default under Kilo: **subtasks ON**, unless `--nosubtasks` is set.
- must follow the **Kilo Orchestrator-per-task rule**.

### 9.1 Orchestrator loop (Kilo + subtasks)

For each migration scope (spec-id or logical group):

1. Orchestrator gathers:
   - involved datasets, data classes, and ownership.
   - migration plans, scripts, configs, and evidence.
2. Code mode (read-only) inspects artifacts and computes per-unit
   statuses.
3. Orchestrator synthesizes governance results:
   - per-unit statuses and risk.
   - aggregated findings.

### 9.2 Non-Kilo environments

- treat `--kilocode` as a no-op.
- use a single reasoning flow with equivalent semantics.

---

## 10) Inline Detection Rules

The workflow must not call other SmartSpec workflows for detection.
Instead, it:

1. inspects environment/system prompts for Kilo/ClaudeCode/Antigravity
   markers.
2. checks for presence of `--kilocode`.
3. if ambiguous, defaults to tool-agnostic behavior and may note this in
   the report header.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` to map spec-ids to repos/services.
2. Use `--workspace-roots` only as a discovery hint, never to invent
   spec-ids outside SPEC_INDEX.
3. Use registries (service, API, data classification, security) to:
   - identify where data lives and flows.
   - identify shared data stores/platforms.
4. For cross-service migrations:
   - list all involved services and data stores.
   - clarify ownership and consumer/producer roles.
   - surface cross-team coordination needs.

---

## 12) UI Addendum (If UI-related Data is Migrated)

For migrations that affect UI-related data (e.g., user preferences, UI
config, feature flags, personalization data):

1. Identify UI-related datasets from specs/registries.
2. Ensure UI governance is respected:
   - JSON-first UI:
     - migration may affect `ui.json`-driven data.
   - opt-out / inline UI:
     - data may be scattered; ensure references are mapped.
3. Governance checks include:
   - consistency of UI behavior across flows/environments after
     migration.
   - risk of inconsistent UI state between users or segments (e.g.,
     feature flags out-of-sync).
   - data minimization and privacy for UI-related data.

(Still governance-only; does not edit UI assets or configs.)

---

## 13) Best Practices (for Users)

- Define and document migration scope and SLOs/NFRs before governance.
- Ensure data classification and policies are up to date.
- Run governance at least:
  - once in the design phase (early); and
  - once pre-release (late), after dry-runs/tests.
- Use `--safety-mode=strict` for migrations touching regulated/sensitive
  or mission-critical data.
- Keep governance reports as release artifacts.
- Combine this workflow with:
  - `/smartspec_security_evidence_audit` for security aspects.
  - `/smartspec_release_readiness` for overall release risk.
- Avoid copying example data into migration docs; describe structure and
  constraints instead.

---

## 14) For the LLM / Step-by-Step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve scope**
   - parse `--spec-ids`, `--include-dependencies`, `--run-label`,
     `--source-env`, `--target-env`, `--region-pairs`.
   - load SPEC_INDEX in canonical order.
   - validate spec-ids exist; expand dependencies if requested.

2. **Gather artifacts**
   - load specs/tasks for scoped spec-ids.
   - load data models (`--data-model-paths`).
   - load classification and policy docs (registries + `--data-policy-paths`).
   - load migration plans (`--migration-plan-paths`).
   - load migration scripts/pipelines.
   - load migration reports, data quality reports, and audit logs if
     provided.

3. **Identify migration units and data classes**
   - derive list of tables/datasets/segments being migrated.
   - attach data classification and relevant policies to each.
   - detect if units appear multi-tenant / per-customer segmented.

4. **Assess governance per unit**
   - determine `coverage_status`, `backup_status`, `rollback_status`,
     `verification_status`, `policy_alignment_status`, `residency_risk_status`,
     `migration_style`, `migration_volume`, `multi_tenant_risk` (best effort).
   - compute `risk_level` and propose `blocking_for_release` using
     safety-mode rules.

5. **Assess residency & multi-tenant risk**
   - if `--region-pairs` or region info is available:
     - identify cross-region data movement.
     - compare with residency/policy constraints.
   - note multi-tenant isolation risks where applicable.

6. **Aggregate by scope**
   - summarize by spec-id/system.
   - compute counts by risk and blocking status.

7. **Generate report**
   - write `.md` or `.json` in `--report-dir`.
   - include:
     - migration scope overview.
     - per-unit governance status.
     - gaps & risks.
     - overall recommendation.

8. **Optional stdout summary**
   - if `--stdout-summary`, print:
     - number of migration units.
     - number of blocking items.
     - top risks.

### 14.2 Stop conditions

The workflow MUST stop after:

- writing (or simulating writing) the governance report, and
- printing any optional stdout summary.

It MUST NOT:

- modify schemas, scripts, pipelines, or configs.
- run migration jobs.
- call other SmartSpec workflows directly (only reference them as
  recommendations).

