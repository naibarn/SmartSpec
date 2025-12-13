| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_release_tagger Manual (EN) | 6.0 | /smartspec_release_tagger | 6.0.x |

# /smartspec_release_tagger Manual (v6.0, English)

## 1. Overview

The `/smartspec_release_tagger` workflow manages release tagging and version management.

**Purpose:** Manage release tagging and version management, creating release tags and updating version metadata.

**Version:** 6.0  
**Category:** operations-deployment

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_release_tagger \
  --version <semver> \
  [--release-notes <path>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_release_tagger.md \
  --version <semver> \
  [--release-notes <path>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Creating Release Tag (CLI)

**Scenario:** Create release tag for new version.

**Command:**

```bash
/smartspec_release_tagger \
  --version 2.1.0 \
  --release-notes RELEASE_NOTES.md \
  --apply
```

**Expected Result:**

1. Release tag created.
2. Exit code `0` (Success).

### Use Case 2: Automated Release (Kilo Code)

**Scenario:** CI pipeline creates release.

**Command (Kilo Code Snippet):**

```bash
/smartspec_release_tagger.md \
  --version 3.0.0 \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Release tag created automatically.
2. Exit code `0` (Success).

### Use Case 3: Preview Release (CLI)

**Scenario:** Preview release without creating tag.

**Command:**

```bash
/smartspec_release_tagger \
  --version 1.5.2 \
  --json
```

**Expected Result:**

1. Release preview with JSON output.
2. Exit code `0` (Success).

---

## 4. Parameters

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--version` | `<semver>` | Semantic version for the release. | Must be valid semver format. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--platform` | Execution platform. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Create release tag. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--release-notes` | Path to release notes file. | (Auto-generate) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/release-tagger/<run-id>/release_info.md` | Release information. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
