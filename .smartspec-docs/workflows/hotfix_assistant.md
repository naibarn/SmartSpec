| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_hotfix_assistant Manual (EN) | 6.0 | /smartspec_hotfix_assistant | 6.0.x |

# /smartspec_hotfix_assistant Manual (v6.0, English)

## 1. Overview

The `/smartspec_hotfix_assistant` workflow assists in creating and managing hotfixes for production issues.

**Purpose:** Assist in creating and managing hotfixes, providing guidance for emergency production fixes.

**Version:** 6.0  
**Category:** operations-deployment

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_hotfix_assistant \
  --issue <description> \
  [--severity <critical|high|medium>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_hotfix_assistant.md \
  --issue <description> \
  [--severity <critical|high|medium>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Creating Hotfix Plan (CLI)

**Scenario:** Create hotfix for critical production bug.

**Command:**

```bash
/smartspec_hotfix_assistant \
  --issue "Payment processing timeout" \
  --severity critical
```

**Expected Result:**

1. Hotfix plan generated.
2. Exit code `0` (Success).

### Use Case 2: High Severity Hotfix (Kilo Code)

**Scenario:** Automated hotfix assistance.

**Command (Kilo Code Snippet):**

```bash
/smartspec_hotfix_assistant.md \
  --issue "Authentication service down" \
  --severity high \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Hotfix plan generated and saved.
2. Exit code `0` (Success).

### Use Case 3: Medium Severity Issue (CLI)

**Scenario:** Plan hotfix for medium severity issue.

**Command:**

```bash
/smartspec_hotfix_assistant \
  --issue "UI rendering glitch" \
  --severity medium \
  --json
```

**Expected Result:**

1. Hotfix plan with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--issue` | `<string>` | Description of the issue requiring hotfix. | Must not be empty. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Save hotfix plan. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--severity` | Issue severity: `critical`, `high`, `medium`. | `high` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/hotfix-assistant/<run-id>/hotfix_plan.md` | Hotfix plan. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
