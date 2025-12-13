| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_security_audit_reporter Manual (EN) | 6.0 | /smartspec_security_audit_reporter | 6.0.x |

# /smartspec_security_audit_reporter Manual (v6.0, English)

## 1. Overview

The `/smartspec_security_audit_reporter` workflow generates comprehensive security audit reports based on threat models and security scans.

**Purpose:** Generate comprehensive security audit reports based on threat models, vulnerability scans, and compliance checks.

**Version:** 6.0  
**Category:** security-audit

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_security_audit_reporter \
  <spec_md> \
  [--include-recommendations] \
  [--compliance <standard>]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_security_audit_reporter.md \
  <spec_md> \
  [--include-recommendations] \
  [--compliance <standard>] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Security Audit Report (CLI)

**Scenario:** Generate comprehensive security audit report.

**Command:**

```bash
/smartspec_security_audit_reporter specs/api/payment_gateway/spec.md \
  --include-recommendations
```

**Expected Result:**

1. Security audit performed.
2. Report with recommendations generated.
3. Exit code `0` (Success).

### Use Case 2: Compliance Check (Kilo Code)

**Scenario:** Check compliance with security standard.

**Command (Kilo Code Snippet):**

```bash
/smartspec_security_audit_reporter.md \
  specs/data/pii_storage/spec.md \
  --compliance GDPR \
  --platform kilo
```

**Expected Result:**

1. Compliance audit performed.
2. Exit code `0` (Success).

### Use Case 3: JSON Output (CLI)

**Scenario:** Structured audit data.

**Command:**

```bash
/smartspec_security_audit_reporter specs/auth/mfa/spec.md \
  --json
```

**Expected Result:**

1. Audit with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to spec.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--include-recommendations` | Include security recommendations in report. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--compliance` | Check compliance with standard (e.g., GDPR, HIPAA, PCI-DSS). | (None) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/security-audit-reporter/<run-id>/audit_report.md` | Security audit report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Compliance Standards:** Supports GDPR, HIPAA, PCI-DSS, and others.

---

**End of Manual**
