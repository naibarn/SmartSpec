| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_docs_generator Manual (EN) | 6.0 | /smartspec_docs_generator | 6.0.x |

# /smartspec_docs_generator Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_docs_generator` workflow generates comprehensive documentation from specifications, plans, and tasks within the SmartSpec framework.

**Purpose:** Generate comprehensive documentation from specs, plans, and tasks, producing user guides, API documentation, and technical references.

**Version:** 6.0  
**Category:** documentation

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

```bash
/smartspec_docs_generator \
  <spec_or_plan> \
  [--doc-type <user-guide|api-docs|technical-ref>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_docs_generator.md \
  <spec_or_plan> \
  [--doc-type <user-guide|api-docs|technical-ref>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating User Guide from Spec (CLI)

**Scenario:** A technical writer needs to generate a user guide from a specification.

**Command:**

```bash
/smartspec_docs_generator specs/auth/login_service/spec.md \
  --doc-type user-guide \
  --apply
```

**Expected Result:**

1. The workflow loads the spec file.
2. It generates a user-friendly guide.
3. Documentation is written to the docs folder.
4. Exit code `0` (Success).

### Use Case 2: API Documentation Generation (Kilo Code)

**Scenario:** A CI pipeline needs to generate API documentation automatically.

**Command (Kilo Code Snippet):**

```bash
/smartspec_docs_generator.md \
  specs/api/rest_endpoints/spec.md \
  --doc-type api-docs \
  --apply \
  --platform kilo
```

**Expected Result:**

1. The workflow generates API documentation.
2. Documentation includes endpoints, parameters, and examples.
3. Exit code `0` (Success).

### Use Case 3: Technical Reference Generation (CLI)

**Scenario:** A developer needs technical reference documentation for a complex system.

**Command:**

```bash
/smartspec_docs_generator specs/system/architecture/spec.md \
  --doc-type technical-ref \
  --json
```

**Expected Result:**

1. The workflow generates technical reference documentation.
2. Output includes structured JSON metadata.
3. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_or_plan>` | `<path>` | Path to spec.md or plan.md file. | Must resolve under `specs/**`. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation. | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/docs-generator/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--doc-type` | Documentation type: `user-guide`, `api-docs`, or `technical-ref`. | `user-guide` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/docs-generator/<run-id>/...` | Safe output artifacts (generated documentation). |
| `docs/**/*.md` | Generated documentation files (only with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Documentation Types:** Choose appropriate doc-type for your audience.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
