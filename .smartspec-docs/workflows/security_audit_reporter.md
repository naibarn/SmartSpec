_# SmartSpec Workflow: Security Audit Reporter

**Workflow:** `/smartspec_security_audit_reporter`  
**Version:** 6.1.1

## 1. Overview

The Security Audit Reporter is a crucial workflow for security assurance. It cross-references the threats identified by the `/smartspec_security_threat_modeler` with the mitigation tasks in `tasks.md`, and then validates whether those mitigations have been implemented using evidence from a `/smartspec_verify_tasks_progress_strict` run.

This is a **reports-only** workflow, making it a safe and essential tool for generating compliance and audit artifacts.

## 2. Key Features

- **Evidence-Based Audit:** Bases its report on cryptographic proof of completed work, not just checked boxes.
- **Threat-to-Mitigation Mapping:** Clearly shows which threats have been addressed and which are still outstanding.
- **Automated Compliance:** Generates a formal audit report that can be used for security reviews and compliance checks.
- **Workflow Integration:** Tightly integrates with the Threat Modeler and Strict Verifier to complete the security lifecycle.

## 3. How It Works

1.  **Gathers Inputs:** Reads the `spec.md`, the associated `threats.md`, `tasks.md`, and the `summary.json` from a strict verification run.
2.  **Correlates Threats and Tasks:** Identifies which tasks in `tasks.md` are intended to mitigate which threats from `threats.md`.
3.  **Validates Evidence:** Checks the verification report to see if the mitigation tasks have been successfully and verifiably completed.
4.  **Generates Audit Report:** Produces a `report.md` and `summary.json` that details the status of each threat:
    -   **Mitigated:** The task was completed and verified.
    -   **Not Mitigated:** The task was not completed or not verified.
    -   **No Mitigation:** No task was defined to address the threat.

## 4. Usage

This workflow is typically the final step in the security assurance process.

### Prerequisite Workflow Chain

1.  `/smartspec_security_threat_modeler` -> `threats.md`
2.  `/smartspec_generate_tasks` -> `tasks.md` (with mitigation tasks)
3.  `/smartspec_verify_tasks_progress_strict` -> `summary.json` (verification evidence)

### Generate the Audit Report

```bash
/smartspec_security_audit_reporter \
  specs/my-feature/spec.md \
  --verify-summary .spec/reports/verify-tasks-progress-strict/run-xyz/summary.json
```

## 5. Input and Flags

- **`spec_md` (Required):** Path to the `spec.md` file. The workflow finds `threats.md` and `tasks.md` in the same directory.
- **`--verify-summary <path>` (Required):** Path to the `summary.json` from a `/smartspec_verify_tasks_progress_strict` run.
- **`--report-format <summary|detailed>` (Optional):** Controls the level of detail in the report.

## 6. Output: Security Audit Report

The workflow generates a report in `.spec/reports/security-audit/`.

### Example Report Snippet

```markdown
### Threat: SQL Injection (STRIDE: Tampering)

- **Threat ID:** TH-001
- **Mitigation Task:** TASK-015 - Implement parameterized queries
- **Status:** ✅ **Mitigated**
- **Evidence:** Verified in run `xyz` with commit `abc1234`.

### Threat: Cross-Site Scripting (XSS) (STRIDE: Spoofing)

- **Threat ID:** TH-002
- **Mitigation Task:** TASK-016 - Sanitize all user inputs
- **Status:** ❌ **Not Mitigated**
- **Evidence:** Task not found in verification report.
```

## 7. Use Cases

- **Pre-Deployment Security Check:** Run as a final gate before deploying to ensure all identified threats have been addressed.
- **Automated Compliance Reporting:** Generate reports for security audits and compliance requirements (e.g., SOC 2, ISO 27001).
- **Continuous Security Monitoring:** Integrate into your CI/CD pipeline to continuously monitor the security posture of your application.
_
