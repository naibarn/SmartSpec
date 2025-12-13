| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_validate_index Manual (EN) | 6.0 | /smartspec_validate_index | 6.0.x |

# /smartspec_validate_index Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_validate_index` workflow validates the integrity and consistency of `.spec/SPEC_INDEX.json` against actual spec files.

**Purpose:** Validate the integrity and consistency of the spec index, ensuring all references are valid and metadata is accurate.

**Version:** 6.0  
**Category:** index-management

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

```bash
/smartspec_validate_index \
  [--fix] \
  [--strict]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_validate_index.md \
  [--fix] \
  [--strict] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Validating Index Integrity (CLI)

**Scenario:** A developer wants to check if the spec index is valid and consistent.

**Command:**

```bash
/smartspec_validate_index
```

**Expected Result:**

1. The workflow validates `.spec/SPEC_INDEX.json`.
2. It checks for broken references and invalid metadata.
3. A validation report is generated.
4. Exit code `0` if valid, `1` if violations found.

### Use Case 2: Fixing Index Issues Automatically (Kilo Code)

**Scenario:** A CI pipeline needs to validate and automatically fix any index issues.

**Command (Kilo Code Snippet):**

```bash
/smartspec_validate_index.md \
  --fix \
  --platform kilo
```

**Expected Result:**

1. The workflow validates the index.
2. It automatically fixes detected issues.
3. The updated index is written.
4. Exit code `0` (Success).

### Use Case 3: Strict Validation Mode (CLI)

**Scenario:** A user wants strict validation that fails on any warnings or inconsistencies.

**Command:**

```bash
/smartspec_validate_index \
  --strict \
  --json
```

**Expected Result:**

1. The workflow performs strict validation.
2. Any warnings are treated as errors.
3. Output includes `validation.json` with detailed results.
4. Exit code `0` if perfect, `1` if any issues.

---

## 4. Parameters

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation. | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/validate-index/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--fix` | Automatically fix detected issues. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--strict` | Enable strict validation mode (fail on warnings). | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/validate-index/<run-id>/validation.md` | Validation report. |
| `.spec/SPEC_INDEX.json` | Fixed index (only with `--fix`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Fix Mode:** Use `--fix` to automatically repair detected issues.
- **Strict Mode:** Use `--strict` to enforce zero-tolerance validation.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
