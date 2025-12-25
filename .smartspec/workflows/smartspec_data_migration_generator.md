---
description: Generate data migration scripts and documentation.
version: 6.0.0
workflow: /smartspec_data_migration_generator
---

# smartspec_data_migration_generator

> **Version:** 6.1.0  
> **Status:** Proposed  
> **Category:** implement

## Purpose

To automate the creation of draft Data Migration scripts based on the discrepancies identified by `/smartspec_data_model_validator`. This workflow translates the validation report into an executable migration file for tools like Flyway, Liquibase, or raw SQL.

This is a **Governed Write Workflow** that is **preview-first**.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

**Always allowed writes (safe outputs):**

- Reports: `.spec/reports/data-migration-generator/**`

**Governed writes (ONLY with `--apply`):**

- Migration Scripts: A configurable path, e.g., `db/migrations/V*__{spec_id}.sql`.

**Forbidden writes (must hard-fail):**

- Any path not explicitly allowed.

### `--apply` behavior

- Without `--apply`: MUST generate a **Preview** of the migration script to be created.
- With `--apply`: MUST write the migration script to the governed path.

---

## Threat model (minimum)

This workflow must defend against:

- **SQL Injection**: The generator must not blindly trust content from the spec or validation report. It must generate safe, validated DDL statements.
- **Unintended Destructive Operations**: The workflow must clearly label potentially destructive changes (e.g., `DROP TABLE`, `DROP COLUMN`) in its preview. An extra flag (`--allow-destructive`) is required to generate scripts containing such operations.
- **Path Traversal**: Standard hardening for write paths.

### Hardening requirements

- **No network access**.
- **No shell execution**.
- **Strict Sanitization**: All inputs from the validation report must be sanitized before being used in DDL statements.
- **Destructive Action Guard**: The workflow must fail if it detects a destructive operation unless `--allow-destructive` is provided.
- **Path Normalization**: All write paths must be normalized and validated.

---

## Invocation

### CLI

```bash
/smartspec_data_migration_generator \
  --report <path/to/validation-report.json> \
  --migration-tool <flyway|liquibase|raw-sql> \
  --output-dir <path/to/migrations> \
  [--allow-destructive] \
  [--apply]
```

### Kilo Code

```bash
/smartspec_data_migration_generator.md \
  --report .spec/reports/data-model-validation/<run-id>/summary.json \
  --migration-tool flyway \
  --output-dir db/migrations
```

---

## Inputs

### Required

- `--report <path>`: Path to the `summary.json` file from a `/smartspec_data_model_validator` run.
- `--migration-tool <tool>`: The target migration tool format. Supported: `flyway`, `liquibase`, `raw-sql`.
- `--output-dir <path>`: The directory where the generated migration script will be placed.

### Optional

- `--allow-destructive`: If present, allows the generation of scripts with destructive operations (e.g., `DROP`).

### Input validation (mandatory)

- `--report` path must exist and be a valid JSON report.
- `--migration-tool` must be one of the supported values.
- `--output-dir` must be a valid, existing directory.

---

## Flags

### Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>`
- `--json`
- `--quiet`

### Workflow-specific flags

- `--report <path>` (required)
- `--migration-tool <tool>` (required)
- `--output-dir <path>` (required)
- `--allow-destructive` (optional)

---

## Output structure

- **Report Path**: `.spec/reports/data-migration-generator/<run-id>/`

### Artifacts (safe outputs)

- `report.md`: A report detailing the migration script that was (or would be) generated.
- `summary.json`: A JSON summary of the operation.

### Governed Artifacts (with `--apply`)

- A new migration script file, named according to the conventions of the specified migration tool (e.g., `V<timestamp>__<spec_id>.sql` for Flyway).

### Exit codes

- `0`: Migration script generated successfully (or preview generated).
- `1`: Errors during execution (e.g., destructive operation found without `--allow-destructive`).
- `2`: Usage/config error.

---

## Core Logic

1.  **Parse Report**: Load and parse the JSON report from `/smartspec_data_model_validator`.
2.  **Analyze Diffs**: Iterate through the `diffs` array in the report.
3.  **Generate DDL**: For each diff, generate the corresponding DDL statement:
    -   `missing_table` -> `CREATE TABLE ...`
    -   `extra_table` -> `DROP TABLE ...` (requires `--allow-destructive`)
    -   `missing_column` -> `ALTER TABLE ... ADD COLUMN ...`
    -   `extra_column` -> `ALTER TABLE ... DROP COLUMN ...` (requires `--allow-destructive`)
    -   `type_mismatch` -> `ALTER TABLE ... ALTER COLUMN ... TYPE ...`
4.  **Check for Destructive Ops**: If any destructive DDL is generated and `--allow-destructive` is not present, fail with an error.
5.  **Format Script**: Wrap the generated DDL statements in the format required by the `--migration-tool` (e.g., add Flyway/Liquibase headers).
6.  **Generate Preview**: Create a `report.md` that shows the user the exact content of the migration script to be created.
7.  **Apply (optional)**: If `--apply` is used, write the script to a new file in the `--output-dir`.

---

## Workflow Chain Integration

This workflow acts as the "fix" for issues found by the validator.

```bash
# Step 1: Validate the current data model against the spec
/smartspec_data_model_validator \
  specs/project/my-app/spec.md \
  --schema-files "db/schema.prisma"

# Step 2: Review the validation report for discrepancies
# cat .spec/reports/data-model-validation/<run-id>/summary.json

# Step 3: Generate a draft migration script to fix the discrepancies
/smartspec_data_migration_generator \
  --report .spec/reports/data-model-validation/<run-id>/summary.json \
  --migration-tool flyway \
  --output-dir db/migrations \
  --apply

# Step 4: Developer reviews and refines the generated migration script
# (e.g., add default values, handle data transformation)

# Step 5: The migration script is included in the next deployment
```

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_data_migration_generator",
  "version": "6.1.0",
  "run_id": "string",
  "status": "success",
  "applied": true,
  "scope": {
    "validation_report": "string",
    "migration_tool": "flyway"
  },
  "summary": {
    "script_generated": true,
    "script_path": "db/migrations/V20251213103000__my-app.sql",
    "operations": {
      "create_table": 1,
      "add_column": 3,
      "drop_column": 0
    },
    "destructive_operations_found": false
  },
  "writes": {
    "reports": [...],
    "governed": ["db/migrations/V20251213103000__my-app.sql"]
  }
}
```

---

# End of workflow doc
