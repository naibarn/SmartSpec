---
manual_name: /smartspec_data_migration_governance Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_data_migration_governance
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (data platform, infra, security, product, release)
---

# /smartspec_data_migration_governance Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_data_migration_governance v5.6.2`

The workflow acts as a **governance layer** for data migrations:

- checks alignment of migration plans/executions with:
  - data model / schema evolution
  - data classification (critical/high/medium/low)
  - data privacy / retention / residency policies
- assesses the presence and quality of:
  - backup strategies
  - rollback strategies
  - dry-run and verification steps
  - data quality checks
- evaluates **risk per migration unit**
  (table/dataset/shard/tenant segment)
- provides `blocking_for_release` recommendations as an input into
  release readiness decisions

### 1.1 Why you need this workflow

Data migrations are inherently risky because:

- mistakes can affect **customer data** and **core business records**
  in ways that are hard or impossible to fully undo
- many migrations are treated as “one-off scripts” with little or no
  governance trail
- regulators and auditors frequently expect evidence that:
  - backups and rollbacks exist and are used
  - migrations do not violate policies or legal constraints

`/smartspec_data_migration_governance` pulls these concerns together into
one structured, repeatable governance view.

### 1.2 Benefits of using it

- Gives a unified view of a migration:
  - which datasets/tables are affected
  - how each unit scores on backup/rollback/verification
  - where policy/residency risks are
- Produces `blocking_for_release` as a clear signal for
  `/smartspec_release_readiness` and release gates.
- Provides a shared language (status model) that data owners,
  platform, security, and compliance can all understand.
- Creates an audit-ready artifact showing that migration risks were
  considered before a release window.

### 1.3 Typical failure modes if you *don’t* use it (or equivalent governance)

- Running migrations without clear **backup/rollback**:
  - a single mistake requires ad-hoc/manual recovery.
- Forgetting **data classification and policies**:
  - sensitive/regulated data moved into environments/regions where it
    should not be.
- Skipping **post-migration data quality checks**:
  - business reports, dashboards, and ML models silently break.
- Having no governance artifact:
  - responding to regulators/auditors becomes difficult.
- Multi-tenant systems:
  - tenant isolation boundaries may be broken, mixing data across
    customers.

This workflow does not guarantee safety, but it significantly reduces
“we never thought about that risk” incidents.

---

## 2. What’s New in v5.6

### 2.1 Per-unit status model

Introduces a clear status model per migration unit, including:

- `coverage_status = IN_SCOPE | OUT_OF_SCOPE | UNKNOWN`
- `backup_status = PRESENT | PARTIAL | NONE | UNKNOWN`
- `rollback_status = PRESENT | WEAK | NONE | UNKNOWN`
- `verification_status = STRONG | BASIC | NONE | UNKNOWN`
- `policy_alignment_status = ALIGNED | RISKY_BUT_JUSTIFIED | VIOLATES | UNKNOWN`
- `residency_risk_status = NONE | POTENTIAL | CONFIRMED | UNKNOWN`
- `migration_style = IN_PLACE | BACKFILL | DUAL_WRITE | OTHER | UNKNOWN`
- `migration_volume = SMALL | MEDIUM | LARGE | UNKNOWN`
- `multi_tenant_risk = NONE | POTENTIAL | CONFIRMED | UNKNOWN`
- `risk_level = LOW | MEDIUM | HIGH | CRITICAL`
- `blocking_for_release = true | false`

### 2.2 Clear strict-mode rules

In `--safety-mode=strict`:

- for units with `data_class in {critical, high}`:
  - `backup_status=NONE/UNKNOWN` → blocking
  - `rollback_status=NONE/UNKNOWN` → blocking
  - `policy_alignment_status=VIOLATES` → blocking
  - `residency_risk_status=CONFIRMED` with no explicit policy allowance
    → blocking
  - `verification_status=NONE` + large volume or risky style → usually
    blocking unless mitigation is strongly documented.

### 2.3 Migration style/volume/multi-tenant as first-class factors

- `migration_style`, `migration_volume`, and `multi_tenant_risk` now
  directly influence `risk_level` and `blocking_for_release` decisions.

### 2.4 Relationship with release readiness

- Output from this workflow (especially `blocking_for_release`) is
  designed as an additional signal for `/smartspec_release_readiness`
  and other governance workflows, not a replacement.

---

## 3. Backward Compatibility Notes

- This v5.6 manual targets `/smartspec_data_migration_governance`
  starting from **v5.6.2** (5.6.x series).
- No existing flags or behaviors have been removed (this workflow is new
  in the governance family).
- `--strict` remains an alias for `--safety-mode=strict`.

---

## 4. Core Concepts

### 4.1 Migration unit

A “unit” of migration risk assessment, typically:

- table or view
- dataset or partition
- shard or tenant segment

Each unit gets a consistent status record:

- how well it is covered by the plan (`coverage_status`)
- backup/rollback/verification strength
- policy/residency alignment
- multi-tenant isolation risk
- overall `risk_level` and `blocking_for_release` recommendation

### 4.2 Risk model & blocking_for_release

- `risk_level` and `blocking_for_release` synthesize:
  - data classification
  - backup/rollback/verification status
  - policy/residency alignment
  - migration style/volume
  - multi-tenant risks
- strict mode uses a more conservative rule set than normal mode.

### 4.3 Governance-only scope

This workflow:

- does **not** generate or modify SQL/ETL code
- does **not** run migration jobs or alter schedules
- does **not** change schemas or configs
- only **reads** docs/scripts and produces a governance report

---

## 5. Quick Start Examples

### 5.1 Govern a user table migration (prod)

```bash
smartspec_data_migration_governance \
  --spec-ids=user_service \
  --run-label=user-table-migration-prod \
  --data-model-paths="schemas/user/*.sql" \
  --migration-plan-paths="docs/migration/user_table/*.md" \
  --migration-script-paths="migrations/user/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --report-format=md \
  --stdout-summary
```

### 5.2 Strict mode for a PII-critical dataset

```bash
smartspec_data_migration_governance \
  --spec-ids=payments_service \
  --run-label=payments-pii-migration \
  --data-model-paths="schemas/payments/*.sql" \
  --migration-plan-paths="docs/migration/payments/*.md" \
  --migration-script-paths="migrations/payments/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --source-env=prod \
  --target-env=prod \
  --region-pairs="eu-central-1:eu-central-1" \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

### 5.3 Cross-service migration

```bash
smartspec_data_migration_governance \
  --spec-ids=orders_service,inventory_service \
  --include-dependencies \
  --run-label=orders-inventory-migration \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --report-format=md
```

---

## 6. CLI / Flags Cheat Sheet

- Scope & label
  - `--spec-ids`
  - `--include-dependencies`
  - `--run-label`
- Migration artifacts
  - `--migration-plan-paths`
  - `--migration-script-paths`
  - `--pipeline-config-paths`
  - `--data-model-paths`
- Policy & classification
  - `--data-policy-paths`
  - `--registry-dir`, `--registry-roots`
- Environment & residency
  - `--source-env`, `--target-env`
  - `--region-pairs`
- Evidence of runs/tests
  - `--migration-report-paths`
  - `--data-quality-report-paths`
  - `--audit-log-paths`
- Multi-repo & index & safety
  - `--workspace-roots`
  - `--repos-config`
  - `--index`, `--specindex`
  - `--safety-mode=normal|strict` (`--strict`)
- Output & KiloCode
  - `--report-format=md|json`
  - `--report-dir`
  - `--stdout-summary`
  - `--kilocode`, `--nosubtasks`

---

## 7. Reading the Governance Report

The report is typically structured as:

1. **Scope overview**
   - affected spec-ids/services
   - environments/regions
   - high-level migration description

2. **Per-unit status table**
   - for each unit:
     - `unit_id`, `data_class`, `coverage_status`, `backup_status`,
       `rollback_status`, `verification_status`,
       `policy_alignment_status`, `residency_risk_status`,
       `migration_style`, `migration_volume`, `multi_tenant_risk`,
       `risk_level`, `blocking_for_release`, `notes`

3. **Gaps & risks**
   - list of units with the highest `risk_level` and
     `blocking_for_release=true`

4. **Summary**
   - counts by risk level
   - counts by blocking/non-blocking

---

## 8. KiloCode Usage Examples

### 8.1 Large-scope migration on Kilo

```bash
smartspec_data_migration_governance \
  --spec-ids=billing_service,invoice_service \
  --include-dependencies \
  --run-label=billing-invoice-migration \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --data-policy-paths=".spec/policies/data/*.md" \
  --kilocode \
  --stdout-summary
```

On Kilo:

- Orchestrator processes one migration scope at a time
- Subtasks cover backup, rollback, verification, policy, residency
- Code mode reads artifacts read-only

### 8.2 Disabling subtasks for small scopes

```bash
smartspec_data_migration_governance \
  --spec-ids=small_service \
  --run-label=small-migration \
  --migration-plan-paths="docs/migration/small_service/*.md" \
  --kilocode \
  --nosubtasks
```

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo with many services

```bash
smartspec_data_migration_governance \
  --spec-ids=search_service,analytics_service \
  --run-label=search-analytics-migration \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --migration-plan-paths="docs/migration/**/*.md" \
  --migration-script-paths="migrations/**/*.sql" \
  --report-format=md
```

### 9.2 Multi-repo, multi-team scenario

```bash
smartspec_data_migration_governance \
  --spec-ids=teamA_users,teamB_subscriptions \
  --run-label=users-subscriptions-migration \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --migration-plan-paths="../teamA/docs/migration/**/*.md;../teamB/docs/migration/**/*.md" \
  --migration-script-paths="../teamA/migrations/**/*.sql;../teamB/migrations/**/*.sql"
```

---

## 10. UI / UX Data Migration

If the migration affects UI-related data such as:

- user preferences
- UI configuration
- feature flags / personalization state

additional considerations include:

- consistency of UI state across users/segments after migration
- avoiding PII leakage during migration and in logs
- mapping between UI governance (JSON-first vs inline) and
  the underlying data stores

---

## 11. Benefits vs Risks of Not Using This Workflow

### 11.1 Benefits of using

- Reduces human “blind spots” in migration governance.
- Provides a shared, structured status model.
- Makes reviews by data owners, security, and compliance more concrete.
- Provides a clear `blocking_for_release` signal for release gating.

### 11.2 Risks if you don’t use it (or equivalent governance)

- Migrations without clear backup/rollback → difficult or incomplete
  recovery on failure.
- Cross-region or cross-environment migrations that ignore policies →
  potential legal/contractual violations.
- Multi-tenant migrations that don’t check isolation → accidental data
  mixing across customers.
- Lack of governance artifacts → harder auditor/regulator conversations
  and weaker internal accountability.

---

## 12. FAQ / Troubleshooting

**Q1: What if we don’t have migration plans documented at all?**  
The workflow will likely classify many units as `coverage_status=UNKNOWN`,
which is itself a signal that you should document the plan before
executing high-risk migrations.

**Q2: Does this workflow guarantee migration safety?**  
No. It is a governance aid, not a proof. It surfaces risks and gaps but
cannot fully validate all runtime behaviors.

**Q3: Should we always use strict mode?**  
Not necessarily. Use `strict` for migrations involving:
- critical/high data classes
- regulated or legally sensitive data

---

End of `/smartspec_data_migration_governance v5.6.2` manual (English).
If future versions change the status model or strict-mode semantics,
issue a new manual (e.g., v5.7) and document compatible workflow
versions clearly.
