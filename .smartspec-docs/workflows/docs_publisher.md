| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_docs_publisher Manual (EN) | 6.0 | /smartspec_docs_publisher | 6.0.x |

# /smartspec_docs_publisher Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_docs_publisher` workflow publishes generated documentation to configured targets (static sites, wikis, or documentation platforms).

**Purpose:** Publish generated documentation to configured targets including static sites, wikis, and documentation platforms.

**Version:** 6.0  
**Category:** documentation

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

```bash
/smartspec_docs_publisher \
  <docs_path> \
  [--target <static|wiki|platform>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_docs_publisher.md \
  <docs_path> \
  [--target <static|wiki|platform>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Publishing to Static Site (CLI)

**Scenario:** A developer wants to publish documentation to a static site generator.

**Command:**

```bash
/smartspec_docs_publisher docs/ \
  --target static \
  --apply
```

**Expected Result:**

1. The workflow loads documentation files.
2. It publishes to the configured static site target.
3. Exit code `0` (Success).

### Use Case 2: Publishing to Wiki (Kilo Code)

**Scenario:** A CI pipeline needs to automatically publish documentation to a wiki.

**Command (Kilo Code Snippet):**

```bash
/smartspec_docs_publisher.md \
  docs/ \
  --target wiki \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Documentation is published to the wiki.
2. Exit code `0` (Success).

### Use Case 3: Preview Publishing (CLI)

**Scenario:** A user wants to preview what would be published without actually publishing.

**Command:**

```bash
/smartspec_docs_publisher docs/ \
  --target platform \
  --json
```

**Expected Result:**

1. A preview report is generated.
2. No actual publishing occurs.
3. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<docs_path>` | `<path>` | Path to documentation directory. | Must exist and be accessible. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation. | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables actual publishing. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/docs-publisher/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--target` | Publishing target: `static`, `wiki`, or `platform`. | `static` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/docs-publisher/<run-id>/...` | Publishing reports and logs. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.
- **Preview Mode:** Without `--apply`, generates preview without actual publishing.
- **Configuration:** Publishing targets must be configured in `.spec/smartspec.config.yaml`.

---

**End of Manual**
