| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_design_system_migration_assistant Manual (EN) | 6.0 | /smartspec_design_system_migration_assistant | 6.0.x |

# /smartspec_design_system_migration_assistant Manual (v6.0, English)

## 1. Overview

The `/smartspec_design_system_migration_assistant` workflow assists in migrating UI components to new design systems.

**Purpose:** Assist in migrating UI components to new design systems, providing migration guides and component mappings.

**Version:** 6.0  
**Category:** ui-design

---

## 2. Usage

### 🔗 CLI Usage

```bash
/smartspec_design_system_migration_assistant \
  <spec_md> \
  [--from-system <name>] \
  [--to-system <name>] \
  [--apply]
```

### Kilo Code Usage

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_design_system_migration_assistant.md \
  <spec_md> \
  [--from-system <name>] \
  [--to-system <name>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Migrating Design System (CLI)

**Scenario:** Migrate from Material UI to Tailwind.

**Command:**

```bash
/smartspec_design_system_migration_assistant specs/ui/dashboard/spec.md \
  --from-system material-ui \
  --to-system tailwind
```

**Expected Result:**

1. Migration guide generated.
2. Exit code `0` (Success).

### Use Case 2: Automated Migration (Kilo Code)

**Scenario:** CI generates migration plan.

**Command (Kilo Code Snippet):**

```bash
/smartspec_design_system_migration_assistant.md \
  specs/ui/forms/spec.md \
  --from-system bootstrap \
  --to-system chakra-ui \
  --apply \
  --platform kilo
```

**Expected Result:**

1. Migration plan generated and saved.
2. Exit code `0` (Success).

### Use Case 3: Preview Migration (CLI)

**Scenario:** Preview migration without applying.

**Command:**

```bash
/smartspec_design_system_migration_assistant specs/ui/navigation/spec.md \
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
| `--apply` | Save migration guide. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--from-system` | Source design system name. | (Auto-detect) | `cli` \| `kilo` \| `ci` \| `other` |
| `--to-system` | Target design system name. | (Required) | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/design-system-migration/<run-id>/migration_guide.md` | Migration guide. |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo`.

---

**End of Manual**
