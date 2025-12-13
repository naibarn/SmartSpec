# /smartspec_data_model_validator Manual (v6.0, English)

## Overview

The `/smartspec_data_model_validator` workflow (Version 6.1.1) is a **quality** assurance tool designed to validate the consistency between an application's implemented data model (ORM models, schema files, or migrations) and the data model defined in a SmartSpec `spec.md` file.

This workflow performs **static analysis only**. It analyzes file contents (source code, schema definitions) without connecting to a live database or executing any code, making it safe for continuous integration (CI) environments.

It is a **reports-only** workflow. It generates detailed reports (`report.md` and `summary.json`) detailing any drift, missing coverage, or inconsistency found between the specification and the implementation.

---

## Usage

### CLI

To run the validator from the command line, you must specify the target `spec.md` and provide globs pointing to your implementation files (schema, models, or migrations).

```bash
/smartspec_data_model_validator \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

### Kilo Code

The Kilo Code invocation is identical to the CLI structure, often used within SmartSpec orchestration files or environments where Kilo Code execution is preferred.

```bash
/smartspec_data_model_validator.md \
  specs/<category>/<spec-id>/spec.md \
  [--schema-files <glob[,glob...]>] \
  [--model-files <glob[,glob...]>] \
  [--migration-files <glob[,glob...]>] \
  [--dialect <postgres|mysql|sqlite|mssql|other>] \
  [--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>] \
  [--strict] \
  [--out <output-root>] \
  [--json]
```

---

## Use Cases

### Use Case 1: Validating Prisma Schema Consistency

**Scenario:** A development team uses SmartSpec to define the `User` and `Product` entities, and implements the data model using Prisma ORM. They need to ensure the `prisma/schema.prisma` file accurately reflects the spec, especially regarding required fields.

**Implementation Details:**
*   **Spec Path:** `specs/core/user-management/spec.md`
*   **Implementation:** Prisma schema file.
*   **Goal:** Check for required fields and entity coverage.

**CLI Command:**

```bash
/smartspec_data_model_validator \
  specs/core/user-management/spec.md \
  --schema-files "prisma/schema.prisma" \
  --orm prisma \
  --dialect postgres \
  --strict
```

**Expected Result:**
The workflow runs in strict mode. If the `User.email` field is marked as required in `spec.md` but optional (`?`) in `schema.prisma`, the workflow will fail with Check **DMV-102 Nullable/Optional Drift** (Severity: High). Output reports are generated under `.spec/reports/data-model-validation/<run-id>/`.

**Kilo Code Example:**

```markdown
# Validate User Model
/smartspec_data_model_validator.md \
  specs/core/user-management/spec.md \
  --schema-files "prisma/schema.prisma" \
  --orm prisma \
  --dialect postgres \
  --strict \
  --out .spec/reports/dmv/user-check
```

### Use Case 2: Checking Rails Model Coverage

**Scenario:** A legacy Rails application uses SmartSpec for documentation. The team wants to verify that every entity defined in the `specs/legacy/data-model/spec.md` has a corresponding Ruby model file, even if the field definitions are complex.

**Implementation Details:**
*   **Spec Path:** `specs/legacy/data-model/spec.md`
*   **Implementation:** Ruby model files (`app/models/**/*.rb`).
*   **Goal:** Ensure **DMV-003 Coverage (Spec → Implementation)** passes.

**CLI Command:**

```bash
/smartspec_data_model_validator \
  specs/legacy/data-model/spec.md \
  --model-files "app/models/**/*.rb" \
  --orm rails \
  --out .spec/reports/rails-coverage
```

**Expected Result:**
If the spec defines an entity called `AuditLog`, but no file `app/models/audit_log.rb` exists, the workflow will fail Check **DMV-003 Coverage**. If all entities are covered, it will pass, potentially issuing warnings for **DMV-101 Extra Entities** if the implementation has models not yet documented in the spec.

### Use Case 3: Migration and Schema Drift Analysis

**Scenario:** A team needs to check if recent SQL migrations introduce fields that violate the constraints defined in the core spec, focusing on naming conventions and field types.

**Implementation Details:**
*   **Spec Path:** `specs/api/v2/spec.md`
*   **Implementation:** SQL schema and migration files.
*   **Goal:** Check type and naming consistency across schema and migrations.

**CLI Command:**

```bash
/smartspec_data_model_validator \
  specs/api/v2/spec.md \
  --schema-files "db/schema.sql" \
  --migration-files "db/migrations/**/*.sql" \
  --dialect mysql
```

**Expected Result:**
The validator analyzes both the current schema and the migrations. If a migration file adds a column with a type incompatible with the spec (e.g., `VARCHAR(10)` in the spec vs. `TEXT` in the migration), it triggers **DMV-004 Field Type Drift** (Warning or Failure, depending on the severity of the drift).

---

## Parameters

### Positional Argument

| Parameter | Required | Description |
| :--- | :--- | :--- |
| `spec_md` | Yes | Path to the SmartSpec definition file (`spec.md`). |

### Workflow-Specific Flags

| Flag | Required | Description |
| :--- | :--- | :--- |
| `--schema-files <glob[,glob...]>` | No | Comma-separated globs pointing to declarative schema files (e.g., `schema.sql`, `schema.prisma`). |
| `--model-files <glob[,glob...]>` | No | Comma-separated globs pointing to ORM model definitions (e.g., TypeScript classes, Ruby models). |
| `--migration-files <glob[,glob...]>` | No | Comma-separated globs pointing to database migration scripts (e.g., `*.sql` migration files). |
| `--dialect <dialect>` | No | Specifies the target database dialect to aid parsing (e.g., `postgres`, `mysql`, `sqlite`, `mssql`, `other`). |
| `--orm <orm>` | No | Specifies the ORM/framework used for implementation (e.g., `prisma`, `typeorm`, `sequelize`, `django`, `rails`, `sqlalchemy`, `other`). |
| `--strict` | No | If set, the workflow will fail (`exit 1`) on any SHOULD check violation (DMV-1xx, DMV-2xx) in addition to MUST checks (DMV-0xx). |

### Universal Flags (Supported)

| Flag | Description |
| :--- | :--- |
| `--out <output-root>` | Specifies the base directory for output artifacts. Must adhere to safety constraints. |
| `--json` | Outputs the final report structure to standard output in JSON format, in addition to writing `summary.json`. |
| `--apply` | Accepted for compatibility but **ignored**. The report header will note this flag was ignored. |
| `--config <path>` | Path to an alternate SmartSpec configuration file. |
| `--quiet` | Suppress non-critical output to stdout/stderr. |

---

## Output

The workflow writes artifacts into a unique run folder, typically under `.spec/reports/data-model-validation/`.

**Default Output Root:**
`.spec/reports/data-model-validation/<run-id>/`

**Artifacts:**

1.  **`report.md`**: A human-readable markdown report detailing the validation scope, findings (errors and warnings), evidence references, and overall summary.
2.  **`summary.json`**: A machine-readable JSON file containing structured results, check IDs, severity, confidence, and scope details, conforming to the defined schema.

### Exit Codes

| Code | Meaning | Description |
| :--- | :--- | :--- |
| `0` | Success