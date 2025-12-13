| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_data_migration_generator Manual (EN) | 6.0 | /smartspec_data_migration_generator | 6.0.x |

# /smartspec_data_migration_generator Manual (v6.0, English)

## 1. Overview

The `/smartspec_data_migration_generator` workflow generates data migration scripts from schema changes.

**Purpose:** Generate data migration scripts from schema changes, ensuring safe and reversible data transformations.

**Version:** 6.0  
**Category:** operations-deployment

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_data_migration_generator \
  <spec_md> \
  [--from-schema <path>] \
  [--to-schema <path>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_data_migration_generator.md \
  <spec_md> \
  [--from-schema <path>] \
  [--to-schema <path>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating Migration Script (CLI)

**Scenario:** Generate migration for schema change.

**Command:**

```bash
/smartspec_data_migration_generator specs/data/user_profile/spec.md \
  --from-schema db/schema_v1.sql \
  --to-schema db/schema_v2.sql
```

**Expected Result:**

1. Migration script generated.
2. Exit code `0` (Success).

### Use Case 2: Automated Migration (Kilo Code)

**Scenario:** CI generates migration scripts.

**Command (Kilo Code Snippet):**

```bash
/smartspec_data_migration_generator.md \
  specs/data/orders/spec.md \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Migration script generated and saved.
2. Exit code `0` (Success).

### Use Case 3: Preview Migration (CLI)

**Scenario:** Preview migration without applying.

**Command:**

```bash
/smartspec_data_migration_generator specs/data/products/spec.md \
  --json
```

**Expected Result:**

1. Migration preview with JSON output.
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
| `--apply` | Save migration script. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--from-schema` | Path to source schema file. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--to-schema` | Path to target schema file. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/data-migration-generator/<run-id>/migration.sql` | Generated migration script. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
