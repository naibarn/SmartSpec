| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_security_threat_modeler Manual (EN) | 6.0 | /smartspec_security_threat_modeler | 6.0.x |

# /smartspec_security_threat_modeler Manual (v6.0, English)

## 1. Overview

The `/smartspec_security_threat_modeler` workflow analyzes specifications to identify security threats and generate threat models.

**Purpose:** Analyze specifications to identify security threats, vulnerabilities, and generate comprehensive threat models.

**Version:** 6.0  
**Category:** security-audit

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_security_threat_modeler \
  <spec_md> \
  [--threat-level <low|medium|high>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_security_threat_modeler.md \
  <spec_md> \
  [--threat-level <low|medium|high>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Threat Model (CLI)

**Scenario:** Security analyst generates threat model for new API.

**Command:**

```bash
/smartspec_security_threat_modeler specs/api/payment_gateway/spec.md \
  --threat-level high
```

**Expected Result:**

1. Spec analyzed for security threats.
2. Threat model generated.
3. Exit code `0` (Success).

### Use Case 2: CI Pipeline Security Check (Kilo Code)

**Scenario:** Automated threat modeling in CI.

**Command (Kilo Code Snippet):**

```bash
/smartspec_security_threat_modeler.md \
  specs/auth/oauth/spec.md \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Threat model generated and saved.
2. Exit code `0` (Success).

### Use Case 3: JSON Output (CLI)

**Scenario:** Structured threat data for security dashboard.

**Command:**

```bash
/smartspec_security_threat_modeler specs/data/user_data/spec.md \
  --json
```

**Expected Result:**

1. Threat model with JSON output.
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
| `--config` | Path to configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Save threat model to spec folder. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--threat-level` | Minimum threat level to report: `low`, `medium`, `high`. | `medium` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/security-threat-modeler/<run-id>/threat_model.md` | Generated threat model. |
| `specs/**/security/threat_model.md` | Saved threat model (with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Threat Levels:** Adjust `--threat-level` based on security requirements.

---

**End of Manual**
