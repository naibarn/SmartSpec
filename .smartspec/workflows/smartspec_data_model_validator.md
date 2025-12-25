---
description: Validate data models and database schemas.
version: 6.0.0
workflow: /smartspec_data_model_validator
---

# smartspec_data_model_validator

> **Version:** 6.1.1  
> **Status:** Proposed  
> **Category:** quality

## Purpose

Validate that an application's data model (ORM models / schema files / migrations) is consistent with the data model described in a SmartSpec `spec.md`.

This workflow performs **static analysis** only. It **does not** connect to a live database and **does not** execute migrations.

It is a **reports-only** workflow, safe to run locally or in CI.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Reports: `.spec/reports/data-model-validation/**`

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under`
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Any runtime source tree modifications

### `--apply` behavior (universal flag)

- Accepted for compatibility but **ignored**.
- The report header MUST note that `--apply` was ignored if provided.

---

## Threat model (minimum)

This workflow must defend against:

- Path traversal / symlink escape when reading schema/model files and when writing reports.
- Secret leakage in reports (e.g., credentials embedded in config snippets or migration comments).
- Accidental network usage.
- Runaway scans / CI cost spikes due to overly broad globs.

### Hardening requirements (MANDATORY)

- **No network access:** Respect `safety.network_policy.default=deny`.
- **No shell execution:** Do not run arbitrary commands from inputs.
- **Path normalization (reads + writes):** Reject traversal (`..`), absolute paths, and control characters on any user-supplied path.
- **No symlink escape (reads + writes):** Do not read/write through symlinks that resolve outside allowed scopes.
- **Read scope enforcement:** All file reads MUST remain within the project root.
- **Output root safety:** If `--out` is provided, it is a *requested* base output root and MUST:
  - resolve under config `safety.allow_writes_only_under`
  - not fall under config `safety.deny_writes_under`
  - not be a runtime source folder
  - hard-fail with usage/config error (`exit 2`) if invalid
- **Redaction:** Apply `safety.redaction` patterns to all report outputs.
- **Excerpt policy:** Do not paste large code/log dumps; reference file paths and symbols/IDs instead.
- **Output collision:** Respect `safety.output_collision` (never overwrite existing run folders).
- **Bounded scanning:** Apply timeouts and content limits per config `safety.content_limits`.

---

## Invocation

### CLI

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

## Inputs

### Positional

- `spec_md` (required): Path to `spec.md`.

### Optional file globs

- `--schema-files`: Comma-separated globs for schema sources (e.g., `prisma/schema.prisma`, `db/schema.sql`, `schema/**/*.sql`).
- `--model-files`: Comma-separated globs for ORM model definitions (e.g., `src/models/**/*.ts`, `app/models/**/*.rb`).
- `--migration-files`: Comma-separated globs for migrations (e.g., `migrations/**/*.sql`, `prisma/migrations/**/migration.sql`).

### Input validation (MANDATORY)

- `spec_md` MUST exist and be a file.
- Each provided glob MUST match at least 1 file, otherwise fail with usage error (`exit 2`).
- Every matched file path MUST:
  - resolve within the project root
  - be rejected if it escapes via symlink
  - be rejected if it contains traversal (`..`), is absolute, or contains control characters
- If no file globs are provided, the workflow MUST:
  - emit `DMV-204 Reduced Coverage` (warning) describing what it could not validate, OR
  - fail with `exit 2` in `--strict` if MUST checks cannot be evaluated.

### Scan scope defaults (RECOMMENDED baseline)

Unless config overrides, the workflow SHOULD:

- ignore common vendor/build dirs: `node_modules/`, `dist/`, `build/`, `.git/`, `vendor/`, `.cache/`, `.next/`, `coverage/`
- enforce caps (and report them): max files, max bytes scanned, max depth, max time
- on limits reached: emit `DMV-204 Reduced Coverage` and clearly state reduced confidence; in `--strict`, fail only if a MUST check becomes unevaluable

---

## Flags

### Universal flags (must support)

- `--config <path>`
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply` (ignored)
- `--out <path>`
- `--json`
- `--quiet`

### Workflow-specific flags

- `--schema-files <glob[,glob...]>`
- `--model-files <glob[,glob...]>`
- `--migration-files <glob[,glob...]>`
- `--dialect <postgres|mysql|sqlite|mssql|other>`
- `--orm <prisma|typeorm|sequelize|django|rails|sqlalchemy|other>`
- `--strict`

---

## Output structure

Outputs are always written under a run folder to prevent overwrites.

- Default root: `.spec/reports/data-model-validation/<run-id>/...`
- If `--out` is provided, it is treated as a *requested* base output root and MUST pass Output root safety validation; otherwise `exit 2`.

Artifacts:

- `report.md`
- `summary.json`

### Exit codes

- `0`: Validation passed (warnings possible in non-strict mode).
- `1`: Validation failed (strict mode) or critical validation failures were found.
- `2`: Usage/config error (missing inputs, unsafe paths, invalid globs, disallowed output root).

---

## Checks (v6.1)

Each check MUST emit a stable ID (`DMV-xxx`).

### Preflight safety checks (always enforced)

- **DMV-000 Preflight Safety**: Validate input paths, glob expansions, read/write constraints (path normalization + no symlink escape), and output root safety. Fail with `exit 2` on violation.

### MUST checks (fail in `--strict`)

- **DMV-001 Spec Parsable**: `spec.md` is parsable and yields at least one model/entity definition (best-effort parsing).
- **DMV-002 Schema/Models Parsable**: Provided schema/model files are parsable enough to extract entities/fields.
- **DMV-003 Coverage (Spec → Implementation)**: Every entity in `spec.md` has a corresponding model/schema representation.
- **DMV-004 Field Type Drift**: For covered entities, field types/constraints do not materially contradict the spec (best-effort static analysis).

### SHOULD checks (warnings unless `--strict`)

- **DMV-101 Extra Entities (Implementation → Spec)**: Entities exist in schema/models but not in `spec.md`.
- **DMV-102 Nullable/Optional Drift**: A field is required in one place but optional/nullable in the other.
- **DMV-103 Enum / Allowed Values Drift**: Enum values or constraint sets differ.
- **DMV-104 Index / Uniqueness Drift**: Uniqueness/index constraints differ where the spec expresses intent.
- **DMV-105 Naming / Consistency**: Naming conventions or mapping rules differ (warn-only unless strict).
- **DMV-204 Reduced Coverage**: Limits reached, no globs provided, or parsing incomplete; report reduced confidence.

---

## Core Logic

1. **Preflight Safety**: Validate `spec_md`, `--out`, and all globs (DMV-000).
2. **Resolve Inputs**: Expand globs to a bounded file list (respect ignore dirs and content limits).
3. **Parse Spec Models**: Extract entities/fields/constraints from `spec.md` (best-effort; report parsing assumptions).
4. **Parse Implementation Models**: Extract entities/fields/constraints from schema/model files (best-effort; report tool limitations).
5. **Correlate**: Map spec entities ↔ implementation entities (by name and declared aliases if present).
6. **Compute Findings**: Run DMV-001..DMV-105, classify severity and confidence.
7. **Generate Artifacts**: Write `report.md` and `summary.json` under the run folder.

---

## `report.md` required content

The report MUST include:

1. **Summary**: Pass/Fail/Warn, counts of entities checked, error/warn counts.
2. **Scope**: Spec path, lists of input globs, resolved file counts, ignore/limit settings.
3. **Results Table**: Entity-by-entity status.
4. **Findings**: Check ID, severity, confidence, rationale, evidence file paths/line refs (when possible).
5. **Coverage Notes**: Any reduced coverage (DMV-204) and what was not evaluated.
6. **Recommended Next Commands**:
   - Recommend next steps that are guaranteed to exist in your project registry (`.spec/WORKFLOWS_INDEX.yaml`).
   - If suggesting a SmartSpec workflow, include both CLI + Kilo forms.

Template (replace with real registry-backed commands):

CLI:
`/<workflow_name> <primary-input> [--out <dir>] [--json]`

Kilo:
`/<workflow_name>.md <primary-input> [--out <dir>] [--json] --platform kilo`

---

## `summary.json` schema (minimum)

```json
{
  "workflow": "smartspec_data_model_validator",
  "version": "6.1.1",
  "run_id": "string",
  "status": "pass|fail|warn",
  "strict": true,
  "scope": {
    "spec_path": "string",
    "schema_globs": ["string"],
    "model_globs": ["string"],
    "migration_globs": ["string"],
    "dialect": "string|null",
    "orm": "string|null"
  },
  "summary": {
    "entities_total": 0,
    "entities_covered": 0,
    "errors": 0,
    "warnings": 0,
    "reduced_coverage": false
  },
  "results": [
    {
      "check_id": "DMV-003",
      "entity": "User",
      "status": "pass|fail|warn|na",
      "severity": "high|medium|low|info",
      "confidence": "high|medium|low",
      "why": "string",
      "evidence": [
        {"path": "string", "ref": "string"}
      ]
    }
  ],
  "warnings": [
    {"check_id": "DMV-204", "message": "string"}
  ],
  "writes": {"reports": ["path/to/report.md", "path/to/summary.json"]}
}
```

---

# End of workflow doc

