| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_data_model_validator Manual (EN) | 6.0 | /smartspec_data_model_validator | 6.0.x |

# /smartspec_data_model_validator Manual (v6.0, English)

## 1. Overview

The `/smartspec_data_model_validator` workflow validates data models against specifications and database schemas.

**Purpose:** Validate data models against specifications, ensuring database schemas, entities, and relationships match defined structures.

**Version:** 6.0  
**Category:** quality-testing

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_data_model_validator \
  <spec_md> \
  [--schema-file <path>] \
  [--strict]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_data_model_validator.md \
  <spec_md> \
  [--schema-file <path>] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Validating Data Model (CLI)

**Scenario:** A developer needs to validate database schema against spec.

**Command:**

```bash
/smartspec_data_model_validator specs/data/user_profile/spec.md \
  --schema-file db/schema.sql
```

**Expected Result:**

1. The workflow validates data model against spec.
2. A validation report is generated.
3. Exit code `0` if valid, `1` if violations found.

### Use Case 2: Strict Validation (Kilo Code)

**Scenario:** CI pipeline requires strict schema validation.

**Command (Kilo Code Snippet):**

```bash
/smartspec_data_model_validator.md \
  specs/data/orders/spec.md \
  --strict \
  --platform kilo
```

**Expected Result:**

1. Strict validation is performed.
2. Exit code `0` if perfect, `1` if issues.

### Use Case 3: JSON Output (CLI)

**Scenario:** Integration requires JSON validation results.

**Command:**

```bash
/smartspec_data_model_validator specs/data/products/spec.md \
  --json
```

**Expected Result:**

1. Validation performed with JSON output.
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
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--schema-file` | Path to database schema file. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--strict` | Enable strict validation mode. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/data-model-validator/<run-id>/validation.md` | Validation report. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
