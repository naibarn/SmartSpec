---
name: /smartspec_security_evidence_audit
version: 5.7.0
role: verification/governance
write_guard: NO-WRITE
purpose: Audit security requirements vs evidence (tests, scans, configs, logs) under SmartSpec v5.7 governance: multi-repo, multi-registry, safety-mode, evidence-freshness, UI metadata signals. Verifier-only; never runs scanners or modifies artifacts.
version_notes:
  - v5.6.2: baseline security evidence audit
  - v5.7.0: governance alignment; multi-repo/registry parity; evidence-freshness rules; strict-mode criteria; UI metadata; backward-compatible
---

# /smartspec_security_evidence_audit (v5.7.0)

Security **verifier-only** workflow. Reads security requirements from specs, policies, and registries; maps them to security evidence; evaluates coverage, freshness, and findings; and produces a structured audit report.

All v5.6.2 behavior is preserved.

---
## 1) Responsibilities
- resolve canonical SPEC_INDEX
- load specs, tasks, policies, registries
- extract security requirements + criticality
- load evidence (tests, scans, configs, logs)
- evaluate requirement coverage + freshness + findings
- determine `blocking_for_release` according to safety-mode
- generate audit report (md/json)

---
## 2) Inputs (read-only)
- SPEC_INDEX (canonical order)
- spec.md, tasks.md
- security policies
- registries (primary + supplemental)
- SAST/DAST/dependency/container/IaC reports
- security test reports
- audit/access logs
- UI JSON metadata (optional)

---
## 3) Outputs
Default:
```
.spec/reports/smartspec_security_evidence_audit/<timestamp>_<run-label>.{md|json}
```
Report contains:
- requirement inventory
- evidence mapping
- coverage_status
- evidence_freshness_status
- finding_status
- blocking_for_release suggestion
- gaps & risks summary
- aggregated summary

---
## 4) Safety-mode (v5.7)
### normal
- missing evidence → `UNKNOWN`
- stale evidence → risk, not necessarily blocking
- open findings for critical/high → blocking=true

### strict / --strict
- critical requirement with NONE or UNKNOWN or STALE → blocking=true
- critical requirement with HAS_OPEN_FINDINGS → blocking=true
- high criticality: lean toward blocking when weak/stale/unknown

---
## 5) Flags
### Scope
- `--spec-ids=<csv>`
- `--include-dependencies`
- `--run-label=<string>`
- `--target-env=<env>`
- `--time-window=<duration>`
- `--evidence-max-age=<duration>`

### Policy & Evidence
- `--security-policy-paths=<glob>`
- `--sast-report-paths=<glob>`
- `--dast-report-paths=<glob>`
- `--dependency-report-paths=<glob>`
- `--container-report-paths=<glob>`
- `--iac-report-paths=<glob>`
- `--security-test-report-paths=<glob>`
- `--audit-log-paths=<glob>`

### Multi-repo / Registry / Index
- `--workspace-roots=<csv>`
- `--repos-config=<path>` (preferred)
- `--registry-dir=<path>`
- `--registry-roots=<csv>` (read-only)
- `--index=<path>` / `--specindex=<legacy>`

### Safety
- `--safety-mode=<normal|strict>`
- `--strict` alias

### Output
- `--report-format=<md|json>`
- `--report-dir=<path>`
- `--stdout-summary`
- `--kilocode`
- `--nosubtasks`

---
## 6) Requirement Extraction
Sources:
- specs (security, compliance, data protection, input validation, authn/authz, secrets mgmt)
- policies (org standards, compliance docs)
- registries (security, data classification, API/service registries)
- UI JSON for UI security requirements (CSP, XSS, CSRF, headers)

Requirement fields:
```
{id, category, criticality, data_classification, threshold, env, scope, source_path}
```

---
## 7) Evidence Mapping
Match requirement ↔ evidence:
- test reports
- SAST/DAST/IAST
- dependency + container scans
- IaC config scans
- logs / audit logs
- UI security tests, security headers, CSP indicators

Respect:
- `--time-window`
- `--evidence-max-age`
- `--target-env`

---
## 8) Evaluation Rules
### coverage_status
- COVERED → strong evidence
- PARTIAL → incomplete or mixed evidence
- NONE → no evidence found
- UNKNOWN → evidence unclear or cannot map

### evidence_freshness_status
- FRESH
- STALE (timestamp > max-age)
- UNKNOWN

### finding_status
- NO_KNOWN_FINDINGS
- HAS_OPEN_FINDINGS
- UNKNOWN

### blocking_for_release
- determined from safety-mode + criticality + findings + freshness

---
## 9) UI Addendum (v5.7)
For UI-facing requirements:
- detect UI security requirements (XSS, CSRF, clickjacking, CSP, secure cookies)
- use UI JSON metadata when present
- check UI security test results + gateway headers
- missing UI JSON = risk (not blocking)

---
## 10) Multi-repo & Registry Awareness
- use repos-config when available
- fallback to workspace-roots
- registries used to infer:
  - sensitive data services
  - shared auth gateways
  - cross-service trust boundaries

Strict-mode:
- contradictory registry definitions for critical areas → blocking

---
## 11) Report Structure
- header: scope, env, time window, safety-mode
- requirement inventory
- evidence table per requirement
- coverage + freshness + findings
- blocking_for_release determination
- gaps & risks
- aggregated summary

---
## 12) KiloCode
- Ask/Architect mode only
- Orchestrator-per-security-domain (read-only)
- never writes or modifies artifacts

---
## 13) Weakness & Risk Check
Ensure:
- NO-WRITE strictness
- no reproduction of secrets
- no "security by guessing"
- evidence freshness rules consistent
- multi-repo + registry safety
- clear blocking semantics

---
## 14) Legacy Flags Inventory
Kept:
- `--strict` alias
Additive-only:
- all other flags
