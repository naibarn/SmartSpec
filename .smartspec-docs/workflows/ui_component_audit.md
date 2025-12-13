| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_ui_component_audit Manual (EN) | 6.0 | /smartspec_ui_component_audit | 6.0.x |

# /smartspec_ui_component_audit Manual (v6.0, English)

## 1. Overview

The `/smartspec_ui_component_audit` workflow audits UI components against design specifications and accessibility standards.

**Purpose:** Audit UI components against design specifications, ensuring consistency and accessibility compliance.

**Version:** 6.0  
**Category:** quality-testing

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_ui_component_audit \
  <spec_md> \
  [--ui-file <path>] \
  [--a11y]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_ui_component_audit.md \
  <spec_md> \
  [--ui-file <path>] \
  [--a11y] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Auditing UI Components (CLI)

**Scenario:** Audit UI components against spec.

**Command:**

```bash
/smartspec_ui_component_audit specs/ui/dashboard/spec.md \
  --ui-file ui/dashboard.json
```

**Expected Result:**

1. UI components audited.
2. Report generated.
3. Exit code `0` (Success).

### Use Case 2: Accessibility Audit (Kilo Code)

**Scenario:** CI pipeline checks accessibility.

**Command (Kilo Code Snippet):**

```bash
/smartspec_ui_component_audit.md \
  specs/ui/forms/spec.md \
  --a11y \
  --platform kilo
```

**Expected Result:**

1. Accessibility audit performed.
2. Exit code `0` (Success).

### Use Case 3: JSON Output (CLI)

**Scenario:** Structured audit results.

**Command:**

```bash
/smartspec_ui_component_audit specs/ui/navigation/spec.md \
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
| `--ui-file` | Path to UI definition file. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--a11y` | Enable accessibility audit. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/ui-component-audit/<run-id>/audit.md` | Audit report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
