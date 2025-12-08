---
manual_name: /smartspec_security_evidence_audit Manual (EN)
manual_version: 5.6
compatible_workflow: /smartspec_security_evidence_audit
compatible_workflow_versions: 5.6.2 – 5.6.x
role: user/operator manual (security, platform, SRE, tech leads)
---

# /smartspec_security_evidence_audit Manual (v5.6, English)

## 1. Overview

This manual explains how to use the workflow:

> `/smartspec_security_evidence_audit v5.6.2`

The workflow answers:

> "To what extent are our **security requirements** backed by **real and
> fresh evidence**? Where are the gaps, and which items should be treated as
> release risks?"

Key properties:

- Role: **verification / governance** (not a scanner)
- `write_guard: NO-WRITE`
  - does **not** run SAST/DAST itself
  - does **not** modify specs / tasks / CI / code / configs
  - reads evidence **read-only** and produces a **security evidence report**
- **Verifier-only:**
  - does **not** generate new tests / pipelines / configs
  - remediation and adding checks belongs to `/smartspec_ci_quality_gate`
    and other implementation workflows
- **No secret leakage in reports:**
  - the report MUST NOT copy secrets/passwords/tokens/keys from evidence
  - it may say "secret found in log X" but must not include the raw value

Use this workflow as the security evidence layer before
`/smartspec_release_readiness`, and during internal/external audits or risk
reviews.

---

## 2. What’s New in v5.6

### 2.1 Evidence freshness

- Introduces `evidence_freshness_status` per requirement:
  - `FRESH` – evidence is within acceptable age (based on
    `--evidence-max-age`)
  - `STALE` – older than configured max age
  - `UNKNOWN` – timestamp unclear or not time-bound
- This prevents old scans from being treated as equivalent to fresh
  evidence.

### 2.2 Strict mode + stale evidence semantics

In `--safety-mode=strict`:

- `critical` + `coverage_status=NONE` → blocking
- `critical` + `HAS_OPEN_FINDINGS` → blocking
- `critical` + `evidence_freshness_status=STALE` → treated as having **no
  current evidence** and should usually be blocking unless clear mitigation
  is documented.

### 2.3 Explicit secret-handling rules

- The spec now explicitly states that reports:
  - must **not** reproduce secrets, tokens, passwords, private keys
  - may reference the **existence** and **location** of such issues only

### 2.4 Clear requirement status model

For each requirement the report aims to provide:

- `coverage_status` = `COVERED | PARTIAL | NONE | UNKNOWN`
- `finding_status` = `NO_KNOWN_FINDINGS | HAS_OPEN_FINDINGS | UNKNOWN`
- `evidence_freshness_status` = `FRESH | STALE | UNKNOWN`
- `blocking_for_release` = `true | false`

---

## 3. Backward Compatibility Notes

- This v5.6 manual targets `/smartspec_security_evidence_audit` from
  **v5.6.2 onwards** (5.6.x).
- No legacy flags or behaviors are removed (the workflow is new in the
  security family).
- `--strict` remains an alias for `--safety-mode=strict`.
- Path / canonical folders / multi-repo / `--kilocode` semantics match other
  SmartSpec governance workflows:
  - `/smartspec_release_readiness`
  - `/smartspec_ci_quality_gate`

---

## 4. Core Concepts

### 4.1 Security requirement inventory

Requirements are gathered from:

- specs (`spec.md`)
- SPEC_INDEX
- security policies and baselines
- registries such as security-registry, data-classification, etc.

Each requirement is described by:

- id/name
- category (e.g. authn, authz, data_at_rest, data_in_transit,
  input_validation, secrets, dependency_vulns, infra_network,
  logging_monitoring, compliance)
- data classification / sensitivity (if available)
- criticality: `critical` | `high` | `medium` | `low`
- source (spec / policy / registry)

### 4.2 coverage_status

- `COVERED` – clear, relevant evidence exists, e.g.:
  - a test suite specifically designed for this requirement
  - recent, clean scan results for the relevant area
- `PARTIAL` – some evidence exists but gaps remain (e.g., only partial
  coverage of endpoints or resources)
- `NONE` – no evidence found that maps to this requirement
- `UNKNOWN` – cannot determine because of missing or ambiguous data

### 4.3 finding_status

- `NO_KNOWN_FINDINGS` – no open findings visible in the evidence
- `HAS_OPEN_FINDINGS` – at least one finding/vulnerability is unresolved
- `UNKNOWN` – unsure due to incomplete parsing/format

### 4.4 evidence_freshness_status

- `FRESH` – evidence age <= `--evidence-max-age`
- `STALE` – evidence is older than `--evidence-max-age`
- `UNKNOWN` – timestamp missing or not relevant

### 4.5 blocking_for_release

A Boolean recommendation indicating whether a requirement should be treated
as a **blocking risk** for release.

It is derived using:

- criticality
- coverage_status
- finding_status
- evidence_freshness_status
- safety-mode (`normal` vs `strict`)

---

## 5. Quick Start Examples

### 5.1 Audit a single service in staging

```bash
smartspec_security_evidence_audit \
  --spec-ids=checkout_api \
  --target-env=staging \
  --run-label=checkout-staging-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/checkout/*.json" \
  --dast-report-paths="reports/dast/checkout/*.json" \
  --dependency-report-paths="reports/deps/checkout/*.json" \
  --report-format=md \
  --stdout-summary
```

Result:

- Report at:
  `.spec/reports/smartspec_security_evidence_audit/<timestamp>_checkout-staging-security.md`
- Summary of security requirements and evidence for `checkout_api` in
  staging.

### 5.2 Strict pre-prod security audit with evidence age

```bash
smartspec_security_evidence_audit \
  --spec-ids=payments_gateway \
  --target-env=prod \
  --run-label=payments-prod-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/payments/*.json" \
  --dast-report-paths="reports/dast/payments/*.json" \
  --dependency-report-paths="reports/deps/payments/*.json" \
  --evidence-max-age=30d \
  --safety-mode=strict \
  --report-format=json \
  --stdout-summary
```

In strict mode + evidence-max-age:

- critical + `coverage_status=NONE` → blocking
- critical + `HAS_OPEN_FINDINGS` → blocking
- critical + `STALE` evidence → treated as effectively no current evidence →
  usually blocking.

### 5.3 Combining IaC reports and audit logs

```bash
smartspec_security_evidence_audit \
  --spec-ids=admin_portal \
  --target-env=prod \
  --run-label=admin-portal-security \
  --iac-report-paths="reports/iac/admin/**/*.json" \
  --audit-log-paths="logs/security/admin_portal/*.json" \
  --report-format=md
```

- IaC reports give infra/config coverage.
- Audit logs highlight admin/access behavior.

---

## 6. CLI / Flags Cheat Sheet

### 6.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
- `--include-dependencies`
- `--run-label=<string>`

### 6.2 Environment, time & evidence age

- `--target-env=dev|staging|prod|...`
- `--time-window=24h|7d|30d|...`
- `--evidence-max-age=30d|90d|...`

### 6.3 Security requirement & policy

- `--security-policy-paths="..."`

### 6.4 Evidence paths

- `--sast-report-paths="..."`
- `--dast-report-paths="..."`
- `--dependency-report-paths="..."`
- `--container-report-paths="..."`
- `--iac-report-paths="..."`
- `--security-test-report-paths="..."`
- `--audit-log-paths="..."`

### 6.5 Multi-repo / registry / index / safety

- `--workspace-roots`
- `--repos-config`
- `--registry-dir`
- `--registry-roots`
- `--index`, `--specindex`
- `--safety-mode=normal|strict` (or `--strict`)

### 6.6 Kilo / output

- `--kilocode`, `--nosubtasks`
- `--report-format=md|json`
- `--report-dir` (default:
  `.spec/reports/smartspec_security_evidence_audit/`)
- `--stdout-summary`

---

## 7. Interpreting coverage / findings / freshness

### 7.1 Example of a "good" critical requirement

- `coverage_status = COVERED`
- `finding_status = NO_KNOWN_FINDINGS`
- `evidence_freshness_status = FRESH`
- In strict mode: usually non-blocking.

### 7.2 Examples of problematic states

- `coverage_status = NONE` → no evidence
- `coverage_status = PARTIAL` with `HAS_OPEN_FINDINGS` → risky
- `evidence_freshness_status = STALE` → old scans/tests
- `HAS_OPEN_FINDINGS` → unresolved vulnerabilities/issues

### 7.3 UNKNOWN vs NONE

- `NONE` = we know there is no relevant evidence
- `UNKNOWN` = we cannot tell (data incomplete, unsupported format, etc.)

In strict mode for critical requirements:

- `NONE` and `STALE` should generally be treated as high risk.

---

## 8. KiloCode Usage Examples

### 8.1 Core auth service on Kilo

```bash
smartspec_security_evidence_audit \
  --spec-ids=core_auth \
  --target-env=prod \
  --run-label=core-auth-security \
  --security-policy-paths=".spec/policies/security/*.md" \
  --sast-report-paths="reports/sast/core_auth/*.json" \
  --dast-report-paths="reports/dast/core_auth/*.json" \
  --dependency-report-paths="reports/deps/core_auth/*.json" \
  --evidence-max-age=30d \
  --safety-mode=strict \
  --kilocode \
  --stdout-summary
```

On Kilo:

- Orchestrator iterates per security domain (authn, authz, data_protection,
  etc.).
- Code mode reads reports read-only.
- Orchestrator synthesizes coverage, freshness, and risk by domain.

### 8.2 Disabling subtasks

```bash
smartspec_security_evidence_audit \
  --spec-ids=small_service \
  --target-env=staging \
  --run-label=small-service-security \
  --kilocode \
  --nosubtasks
```

- Simpler, single-flow reasoning, good for small scopes.

---

## 9. Multi-repo / Multi-registry Examples

### 9.1 Monorepo with multiple services

```bash
smartspec_security_evidence_audit \
  --spec-ids=search_api,ranking_service \
  --target-env=prod \
  --run-label=search-stack-security \
  --repos-config=.spec/repos.yaml \
  --registry-dir=.spec/registry \
  --sast-report-paths="reports/sast/**/*.json" \
  --dast-report-paths="reports/dast/**/*.json" \
  --dependency-report-paths="reports/deps/**/*.json" \
  --safety-mode=strict
```

- Uses repos-config + registries to map cross-service requirements.
- Shows coverage and risk per service and per domain.

### 9.2 Multiple repos / teams

```bash
smartspec_security_evidence_audit \
  --spec-ids=teamA_checkout,teamB_payments \
  --target-env=staging \
  --run-label=checkout-payments-security \
  --workspace-roots="../teamA;../teamB" \
  --registry-dir=../platform/.spec/registry \
  --sast-report-paths="../teamA/reports/sast/**/*.json;../teamB/reports/sast/**/*.json" \
  --dast-report-paths="../teamA/reports/dast/**/*.json;../teamB/reports/dast/**/*.json" \
  --dependency-report-paths="../teamA/reports/deps/**/*.json;../teamB/reports/deps/**/*.json"
```

- The report will highlight cross-team requirements and which repo provides
  which evidence.

---

## 10. UI Security Examples

Typical UI-related security requirements:

- XSS protection (CSP, output encoding)
- CSRF defenses (tokens, SameSite cookies)
- clickjacking protection (X-Frame-Options, CSP frame-ancestors)
- secure cookie usage (Secure, HttpOnly, SameSite)

The workflow should:

- map these requirements to evidence like:
  - scanner reports for XSS/CSRF
  - security headers from gateway/backend
  - UI security/regression tests
- treat UI governance (JSON-first / inline / opt-out) purely as context for
  locating components; it does **not** change the pass/fail semantics.

---

## 11. Best Practices & Anti-patterns

### 11.1 Best Practices

- Write security requirements in specs/policies; do not rely on tribal
  knowledge.
- Integrate SAST/DAST/dependency scans into CI early.
- Use `--safety-mode=strict` for high-value/sensitive systems.
- Set `--evidence-max-age` appropriately (e.g., 30–90 days depending on
  risk).
- Store reports as artifacts in version control or CI.
- Combine results with `/smartspec_release_readiness` and
  `/smartspec_ci_quality_gate`.

### 11.2 Anti-patterns

- Assuming "we scanned once last year" means "we are still secure".
- Expecting the workflow to invent requirements rather than reading them
  from specs/policies.
- Using the report as a rubber-stamp audit without a clear risk acceptance
  process.

---

## 12. FAQ / Troubleshooting

### Q1: What if there are no reports or logs at all?

- Most requirements will have `coverage_status=NONE` or `UNKNOWN`.
- In strict mode, critical requirements become critical gaps/blocking.
- You should add scanners/tests via `/smartspec_ci_quality_gate` and CI
  first.

### Q2: What if evidence is very old and lacks clear timestamps?

- `evidence_freshness_status` becomes `UNKNOWN`.
- Treat this as a risk and improve your logging/reporting to include
  timestamps.

### Q3: What if secrets are found in logs or reports?

- The audit may say "secret found in log X",
  but must **not** reproduce the secret value.
- Rotating credentials and cleaning up logs is the responsibility of
  security/infra teams.

---

End of `/smartspec_security_evidence_audit v5.6.2` manual (English).
If future versions change key semantics (e.g., evidence age handling or
finding mapping), issue a new manual (e.g., v5.7) and document supported
workflow versions.

