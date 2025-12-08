---
name: /smartspec_security_evidence_audit
version: 5.6.2
role: verification/governance
write_guard: NO-WRITE
purpose: Map security requirements to concrete evidence, detect missing or
         weak enforcement, and produce a security evidence report without
         modifying code, configs, CI, or infrastructure.
---

## 1) Summary

`/smartspec_security_evidence_audit` reads SmartSpec artifacts, security
requirements, and security-related evidence (tests, scanner reports,
configurations, logs/alerts) and produces a **security evidence audit
report**.

It focuses on:

- discovering **security requirements** from specs, policies, and registries
- mapping each requirement to **code/config/test evidence**
- assessing **coverage** (covered / partial / none / unknown) and
  **finding status** (no known findings / has open findings / unknown)
- assessing **evidence freshness** to distinguish between recent and stale
  scans or checks
- identifying **gaps**:
  - requirements with no evidence
  - areas with evidence but unresolved findings
  - duplicated or conflicting security behavior
- producing a structured report the org can use for:
  - release readiness
  - risk reviews
  - audit/compliance preparation

> **Verifier-only:**
> This workflow is **not** a security scanner and does **not** modify
> anything. It only reads artifacts and summarizes evidence vs
> requirements.
>
> Generating or changing tests, CI pipelines, configs, or code belongs to
> other workflows (e.g., `/smartspec_ci_quality_gate`, implementation
> workflows, or dedicated remediation flows).
>
> The report MUST NOT reproduce secrets, passwords, private keys, tokens,
> or other sensitive values from evidence. It may reference their presence
> (e.g., "secret found in log X") but must not copy raw values.

Use it when you want a SmartSpec-aligned view of
"which security promises are backed by real, fresh evidence, and where are
 the gaps?".

---

## 2) When to Use

Use `/smartspec_security_evidence_audit` when:

- security requirements or controls are defined in:
  - specs / SPEC_INDEX
  - security policy documents
  - compliance/regulatory docs
- you have some combination of:
  - security tests (unit/integration/E2E security checks)
  - SAST/DAST/IAST scanner reports
  - dependency and container image scan reports
  - infrastructure-as-code (IaC) and configuration analysis results
  - identity/RBAC configuration and access logs
- you need a **structured evidence matrix** for:
  - release governance
  - internal/external security audits
  - risk reviews and prioritization

Typical placement in the chain:

`generate_spec → generate_plan → generate_tasks → implement_core_logic → generate_tests (incl. security) → run_CI / scanners / checks → /smartspec_security_evidence_audit → /smartspec_release_readiness`

Do **not** use this workflow to:

- run or configure security scanners directly
- manage credentials, secrets, or keys
- change firewall rules, IAM policies, or other security configs
- make final risk acceptance decisions (it only provides structured input)

---

## 3) Inputs / Outputs

### 3.1 Inputs (artifacts)

Read-only artifacts expected:

- **Index**
  - `.spec/SPEC_INDEX.json` (canonical)
  - `SPEC_INDEX.json` at repo root (legacy mirror)
  - `.smartspec/SPEC_INDEX.json` (deprecated)
  - `specs/SPEC_INDEX.json` (older layout)

- **Specs & tasks**
  - `specs/<category>/<spec-id>/spec.md`
  - `specs/<category>/<spec-id>/tasks.md`
  - optional security-specific docs (e.g., `security.md`, `threat_model.md`)
    referenced from SPEC_INDEX or spec

- **Security / policy files (optional)**
  - any paths matching `--security-policy-paths`, for example:
    - org security baseline
    - OWASP/cheat sheet style internal guidance
    - compliance mappings

- **Registries (optional)**
  - `.spec/registry/service-registry.json`
  - `.spec/registry/api-registry.json`
  - `.spec/registry/data-classification-registry.json` (if present)
  - `.spec/registry/security-registry.json` (if project defines one)

- **Security evidence (optional)**
  - any paths matching:
    - `--sast-report-paths` (SAST scanner outputs)
    - `--dast-report-paths` (DAST scanner outputs)
    - `--dependency-report-paths` (SBOM, dependency vulnerability scans)
    - `--container-report-paths` (image scan results)
    - `--iac-report-paths` (IaC and config scan results)
    - `--security-test-report-paths` (security-specific test suites)
    - `--audit-log-paths` (access / auth / admin action logs)

All of the above are treated as **read-only evidence sources**.

### 3.2 Inputs (flags)

See **5) Flags**.

### 3.3 Outputs

- **Security evidence report** (human-readable + structured)
  - default location:
    - `.spec/reports/smartspec_security_evidence_audit/<timestamp>_<run-label>.md`
  - if `--report-format=json` is used:
    - `.spec/reports/smartspec_security_evidence_audit/<timestamp>_<run-label>.json`

The report SHOULD include, at minimum:

1. **Security requirement inventory**
   - per spec-id and (optionally) environment/scope
   - each requirement with:
     - id/name
     - category (authn, authz, data_at_rest, data_in_transit,
       input_validation, secrets, dependency_vulns, infra_network,
       logging_monitoring, compliance, etc.)
     - data sensitivity / classification (if available)
     - criticality (`critical` | `high` | `medium` | `low`)
     - source (spec, policy, registry, etc.)

2. **Evidence mapping, coverage & freshness**
   - for each requirement:
     - `coverage_status`:
       - `COVERED` (clear evidence exists)
       - `PARTIAL` (some evidence, notable gaps)
       - `NONE` (no evidence found)
       - `UNKNOWN` (cannot determine)
     - `evidence_freshness_status`:
       - `FRESH` (evidence within acceptable age bounds)
       - `STALE` (evidence older than configured max age)
       - `UNKNOWN` (age unclear or not applicable)
     - evidence sources (paths, kinds: test, scanner, config, log)
     - `finding_status`:
       - `NO_KNOWN_FINDINGS`
       - `HAS_OPEN_FINDINGS`
       - `UNKNOWN`
     - `blocking_for_release`: `true|false` (recommendation)
     - short explanation / notes

3. **Gaps & risks**
   - list of requirements with:
     - `coverage_status=NONE`, or
     - `HAS_OPEN_FINDINGS`, or
     - `evidence_freshness_status=STALE` for critical requirements.
   - prioritized by criticality and affected systems.

4. **Aggregated summary**
   - per spec-id / service / environment:
     - counts by coverage status and criticality
     - counts of requirements with open findings
     - counts of stale evidence
   - global summary:
     - total requirements
     - coverage distribution
     - evidence freshness distribution
     - top risk areas

Optional **stdout summary** when `--stdout-summary` is enabled.

---

## 4) Modes

### 4.1 Role & write guard

- Role: **Verification / Governance**
- Write guard: **NO-WRITE**

MUST NOT:

- run or configure security scanners
- modify specs, tasks, registries, configs, or code
- update vulnerability status in tracking systems

MAY:

- read all allowed artifacts and reports
- generate new reports under `.spec/reports/smartspec_security_evidence_audit/`
- print textual summaries

### 4.2 Platform semantics

- Tool-agnostic by default (no specific vendor integration implied).

- Under Kilo (when `--kilocode` and Kilo environment is detected):
  - effective mode: **Ask / Architect** (no write operations)
  - use **Orchestrator-per-security-domain** for reasoning only:
    - for each domain (authn, authz, data_protection, input_validation,
      dependency_vulns, infra_network, secrets, logging_monitoring,
      compliance):
      1) Orchestrator enumerates relevant requirements from specs/policies.
      2) Code mode (read-only) scans evidence files for matching signals.
      3) Orchestrator synthesizes coverage, freshness, and risk per domain.

- If `--kilocode` is present but Kilo is not available:
  - treat `--kilocode` as a **no-op meta-flag**
  - proceed in a generic LLM mode and note this in the report header.

Write guard remains **NO-WRITE** in all modes.

---

## 5) Flags

> All flags are new and additive; no existing flags are removed or repurposed.

### 5.1 Scope & labeling

- `--spec-ids=<id1,id2,...>`
  - spec-ids whose security requirements should be audited.
  - all IDs must exist in SPEC_INDEX.

- `--include-dependencies`
  - expand scope via SPEC_INDEX and registries to include dependent services
    (e.g., upstream APIs, shared auth services).

- `--run-label=<string>`
  - label for this audit run, used in filenames and report headers.
  - e.g., `q4-2025-security-audit`, `release-1.3.0-security`.

### 5.2 Environment, time window & evidence age

- `--target-env=<env>`
  - e.g., `dev`, `staging`, `prod`.
  - used as a filter for environment-specific evidence when applicable.

- `--time-window=<duration>`
  - e.g., `24h`, `7d`, `30d`.
  - used primarily when examining logs and other time-bounded evidence.

- `--evidence-max-age=<duration>`
  - optional maximum age for considering evidence "fresh" (e.g., `30d`,
    `90d`).
  - used together with timestamps in reports/logs to set
    `evidence_freshness_status`.

### 5.3 Security requirement & policy inputs

- `--security-policy-paths="<glob1>;<glob2>;..."`
  - paths to security policies, standards, and guidance documents.

### 5.4 Evidence locations

- `--sast-report-paths="<glob1>;<glob2>;..."`
- `--dast-report-paths="<glob1>;<glob2>;..."`
- `--dependency-report-paths="<glob1>;<glob2>;..."`
- `--container-report-paths="<glob1>;<glob2>;..."`
- `--iac-report-paths="<glob1>;<glob2>;..."`
- `--security-test-report-paths="<glob1>;<glob2>;..."`
- `--audit-log-paths="<glob1>;<glob2>;..."`

### 5.5 Multi-repo / registry / index / safety

- `--workspace-roots="<path1>;<path2>;..."`
- `--repos-config=<path>`
- `--registry-dir=<path>`
- `--registry-roots="<path1>;<path2>;..."`
- `--index=<path>` / `--specindex=<path>`
- `--safety-mode=<normal|strict>`
  - `--strict` is a legacy alias for `--safety-mode=strict`.

Semantics:

- `--repos-config` is preferred for precise multi-repo topology.
- `--workspace-roots` is a discovery hint when `--repos-config` is missing.
- `--registry-dir` is the primary registry root (default `.spec/registry`).
- `--registry-roots` are read-only supplemental registries.

**Safety mode behavior:**

- `normal` (default):
  - gaps in coverage and open findings are reported with recommendations.
  - `blocking_for_release` is set conservatively, focusing on
    `critical` / `high` requirements with:
    - `coverage_status=NONE`, or
    - clear `HAS_OPEN_FINDINGS`.
  - stale evidence (`evidence_freshness_status=STALE`) for critical
    requirements must at least be called out as risks, even if not always
    blocking.

- `strict` / `--strict`:
  - any `critical` requirement with `coverage_status=NONE` must be marked
    as `blocking_for_release=true`.
  - any `critical` requirement with `HAS_OPEN_FINDINGS` must also be
    marked `blocking_for_release=true`.
  - any `critical` requirement with `evidence_freshness_status=STALE` is
    treated as if there is effectively **no current evidence** and should
    lean toward `blocking_for_release=true` unless there is a clearly
    documented mitigation.
  - for `high` requirements, the workflow should lean toward
    `blocking_for_release=true` when evidence is weak, missing, or stale,
    while still explaining rationale.

### 5.6 Kilo / subtasks

- `--kilocode`
  - enables Kilo-aware Orchestrator-per-security-domain behavior.

- `--nosubtasks`
  - disables automatic subtask decomposition.

### 5.7 Output control

- `--report-format=<md|json>`
  - default: `md`.

- `--report-dir=<path>`
  - default: `.spec/reports/smartspec_security_evidence_audit/`.

- `--stdout-summary`
  - prints a short summary (counts by coverage status, critical gaps,
    stale evidence, etc.).

---

## 6) Canonical Folders & File Placement

The workflow MUST follow SmartSpec canonical folder rules:

1. **Index detection order** (read-only):
   1) `.spec/SPEC_INDEX.json` (canonical)
   2) `SPEC_INDEX.json` at repo root (legacy mirror)
   3) `.smartspec/SPEC_INDEX.json` (deprecated)
   4) `specs/SPEC_INDEX.json` (older layout)

2. **Specs & tasks**:
   - `specs/<category>/<spec-id>/spec.md`
   - `specs/<category>/<spec-id>/tasks.md`

3. **Registries**:
   - primary: `.spec/registry/`
   - supplemental: `--registry-roots` (read-only)

4. **Reports (outputs)**:
   - default:
     - `.spec/reports/smartspec_security_evidence_audit/<timestamp>_<run-label>.{md|json}`
   - workflow MUST NOT create `.smartspec/` or other non-canonical
     top-level folders by default.

---

## 7) Weakness & Risk Check (Quality Gate for This Workflow)

Before treating this workflow spec as complete, check that it:

1. **Preserves NO-WRITE**
   - explicitly forbids running scanners or changing artifacts.
   - never edits security configs, policies, or code.

2. **Avoids "security by guessing"**
   - does not assume security is fine when there is no evidence.
   - clearly distinguishes between `COVERED`, `PARTIAL`, `NONE`, and
     `UNKNOWN` coverage.

3. **Handles evidence freshness correctly**
   - does not treat very old scans as equivalent to fresh evidence when
     `--evidence-max-age` is provided.
   - uses `evidence_freshness_status` and the safety-mode rules to
     surface stale evidence as a risk.

4. **Avoids redefining security requirements**
   - requirements and their criticality come from specs/policies/registries.
   - suggestions for new or stronger requirements must be clearly labeled
     as proposals only, outside the canonical inventory.

5. **Protects sensitive values in output**
   - does not reproduce secrets, tokens, passwords, or private keys in the
     report.
   - refers to findings and locations, not raw secret values.

6. **Clarifies blocking_for_release**
   - uses safety-mode semantics consistently.
   - does not silently change the criteria used by other workflows.

7. **Respects multi-repo ownership**
   - uses SPEC_INDEX + registries + `--repos-config` to map requirements
     to services/repos.
   - does not assign remediation ownership outside the owning team without
     marking it as cross-team dependency.

8. **Handles environment & time properly**
   - labels environment and time window for evidence used (esp. logs).
   - avoids mixing environments without clear separation.

9. **Maintains verifier-only boundary**
   - does not generate CI configurations, test code, or patches.
   - can recommend using `/smartspec_ci_quality_gate` or other workflows
     but never invokes them directly.

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
  - `--evidence-max-age`
  - `--security-policy-paths`
  - `--sast-report-paths`
  - `--dast-report-paths`
  - `--dependency-report-paths`
  - `--container-report-paths`
  - `--iac-report-paths`
  - `--security-test-report-paths`
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
- role under Kilo: **Ask / Architect**, **NO-WRITE** enforced.
- uses Orchestrator-per-security-domain when subtasks are enabled.

### 9.1 Orchestrator loop (Kilo + subtasks)

For each security domain (authn, authz, data_protection, input_validation,
dependency_vulns, infra_network, secrets, logging_monitoring, compliance):

1. Orchestrator groups relevant requirements.
2. Code mode (read-only) inspects available evidence.
3. Orchestrator synthesizes coverage, freshness, and risk.
4. Results are merged into the global report structure.

### 9.2 Non-Kilo environments

- treat `--kilocode` as a no-op.
- use a single-flow reasoning process (still respecting NO-WRITE).

---

## 10) Inline Detection Rules

The workflow must not call other SmartSpec workflows for detection.
Instead, it:

1. Inspects environment/system prompts for Kilo/ClaudeCode/Antigravity
   markers.
2. Checks for the presence of `--kilocode`.
3. If signals are ambiguous, defaults to tool-agnostic behavior and notes
   this in the report header.

---

## 11) Multi-repo / Multi-registry Rules

1. Use `--repos-config` (when provided) to map spec-ids to services/repos.
2. Use `--workspace-roots` only as a discovery hint, never to invent
   spec-ids outside SPEC_INDEX.
3. Use registries (service, API, data classification, security) to:
   - understand which services hold sensitive data
   - identify shared security components (e.g., auth gateways)
   - highlight cross-service trust boundaries.
4. When a requirement spans multiple services, the report should:
   - list all involved services
   - try to summarize coverage/evidence per service
   - still provide an overall risk summary.

---

## 12) UI Addendum (Security for UI)

For UI-facing specs, this workflow should:

1. Identify UI-related security requirements, e.g.:
   - XSS protection
   - CSRF defenses
   - clickjacking protection
   - secure cookie usage
   - content security policy (CSP) requirements

2. Look for evidence such as:
   - frontend security tests (e.g., XSS regression tests)
   - security headers set by backend or gateway
   - scanner reports focused on UI vulnerabilities

3. Respect UI governance (JSON-first vs inline vs UI JSON opt-out) as
   context only:
   - use it to locate where UI components are defined and wired.
   - do **not** change pass/fail semantics for security requirements.

---

## 13) Best Practices (for Users)

- Ensure security requirements are written down in specs or policy docs; do
  not rely on tribal knowledge.
- Integrate security scanning and tests into CI **before** relying on this
  audit for a strong signal.
- Use `--safety-mode=strict` for production releases of high-value systems.
- Run audits periodically (e.g., each sprint or release) to track progress
  and detect regressions or staleness in evidence.
- Store security evidence reports as versioned artifacts.
- Combine results with `/smartspec_release_readiness` to get a full view of
  release risk.
- Use `/smartspec_ci_quality_gate` or other workflows to add missing checks
  identified as gaps.

---

## 14) For the LLM / Step-by-Step Flow & Stop Conditions

### 14.1 Step-by-step flow

1. **Resolve scope**
   - parse `--spec-ids`, `--include-dependencies`, `--target-env`,
     `--run-label`.
   - load SPEC_INDEX using canonical order.
   - validate that all spec-ids exist.
   - expand to dependent specs if requested.

2. **Gather artifacts**
   - load specs/tasks for scoped spec-ids.
   - load security/policy files (`--security-policy-paths`).
   - load registries (`--registry-dir`, `--registry-roots`).
   - load evidence files from all `--*report-paths` and `--audit-log-paths`.

3. **Extract security requirements**
   - identify security-related requirements from specs/policies/registries.
   - capture category, criticality, data classification, and source.

4. **Map evidence to requirements**
   - for each requirement, map to relevant tests/reports/configs/logs.
   - respect `--target-env` and `--time-window` when applicable.
   - when timestamps and `--evidence-max-age` are available, derive
     `evidence_freshness_status`.

5. **Assess coverage, freshness & findings**
   - set `coverage_status` (COVERED/PARTIAL/NONE/UNKNOWN).
   - set `evidence_freshness_status` (FRESH/STALE/UNKNOWN).
   - determine `finding_status` (NO_KNOWN_FINDINGS/HAS_OPEN_FINDINGS/
     UNKNOWN) based on evidence contents.
   - determine `blocking_for_release` using safety-mode, criticality, and
     freshness rules.

6. **Aggregate by service / domain**
   - summarize coverage, freshness, and risks per spec-id, service, and
     domain.

7. **Generate report**
   - serialize to `.md` or `.json` under `--report-dir`.
   - include:
     - requirement inventory
     - evidence mapping and statuses
     - gaps and high-risk items
     - notes on environment, time window, and evidence age.

8. **Optional stdout summary**
   - if `--stdout-summary` is set, print a short summary:
     - totals by coverage status
     - number of critical gaps
     - number of requirements with stale evidence
     - list of top-risk spec-ids.

### 14.2 Stop conditions

The workflow MUST stop after:

- writing (or simulating writing) the security evidence report, and
- printing any optional stdout summary.

It MUST NOT:

- modify specs, tasks, code, or configs
- trigger or reconfigure scanners
- invoke other workflows directly (may only mention them as recommendations).
