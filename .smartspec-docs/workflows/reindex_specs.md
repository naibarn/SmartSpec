| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_reindex_specs Manual (EN) | 6.0 | /smartspec_reindex_specs | 6.0.x |

# /smartspec_reindex_specs Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_reindex_specs` workflow rebuilds the `.spec/SPEC_INDEX.json` by scanning all specs under `specs/**` and updating the index with current metadata.

**Purpose:** Rebuild the spec index by scanning all specifications and updating metadata, ensuring the index is synchronized with the actual spec files.

**Version:** 6.0  
**Category:** index-management

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

```bash
/smartspec_reindex_specs \
  [--apply] \
  [--validate]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_reindex_specs.md \
  [--apply] \
  [--validate] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Rebuilding Spec Index (CLI)

**Scenario:** A developer has added several new specs and needs to rebuild the index.

**Command:**

```bash
/smartspec_reindex_specs --apply
```

**Expected Result:**

1. The workflow scans all specs under `specs/**`.
2. It extracts metadata from each spec.
3. The `.spec/SPEC_INDEX.json` is rebuilt with current data.
4. Exit code `0` (Success).

### Use Case 2: Validating Index Without Changes (Kilo Code)

**Scenario:** A CI pipeline needs to validate that the index is up-to-date without making changes.

**Command (Kilo Code Snippet):**

```bash
/smartspec_reindex_specs.md \
  --validate \
  --platform kilo
```

**Expected Result:**

1. The workflow scans all specs and compares with the index.
2. It reports any discrepancies.
3. No changes are made to the index.
4. Exit code `0` if synchronized, `1` if out of sync.

### Use Case 3: Preview Reindexing (CLI)

**Scenario:** A user wants to see what changes would be made to the index before applying them.

**Command:**

```bash
/smartspec_reindex_specs --json
```

**Expected Result:**

1. The workflow generates a preview of index changes.
2. Output includes `summary.json` with proposed changes.
3. No changes are applied.
4. Exit code `0` (Success).

---

## 4. Parameters

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation. | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (updating SPEC_INDEX.json). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/reindex-specs/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--validate` | Validate index synchronization without making changes. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/reindex-specs/<run-id>/...` | Reindexing reports and logs. |
| `.spec/SPEC_INDEX.json` | Updated spec index (only with `--apply`). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Validation Mode:** Use `--validate` to check synchronization without changes.
- **Governed Writes:** Use `--apply` to actually update the index.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
