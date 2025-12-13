# /smartspec_design_system_migration_assistant Manual (v6.0, English)

## Overview

The `/smartspec_design_system_migration_assistant` workflow (Version: 6.1.1) is designed to facilitate a controlled migration between different UI component libraries or design token systems.

**Purpose:** It generates **deterministic patches** and **risk-scored change sets** to automate the refactoring process.

The workflow operates in two primary modes:

1.  **Preview Mode (Default):** Generates reports, diffs, and patches showing proposed changes without modifying any source code.
2.  **Apply Mode (`--apply`):** Performs governed code modifications within approved source roots, ensuring backups and atomic writes for safety.

The workflow is non-intrusive: it does not run the application, execute network calls, or install dependencies.

## Usage

### CLI Usage

Execute the workflow directly from the command line.

**Preview Mode (Recommended First Run):**

```bash
/smartspec_design_system_migration_assistant \
  --source-root ./src/ui \
  --from mui \
  --to smartspec-ui \
  --audit-summary .spec/reports/ui-component-audit/latest/summary.json \
  --token-map .smartspec/mappings/design-tokens.json
```

**Apply Mode (After Reviewing Preview):**

```bash
/smartspec_design_system_migration_assistant \
  --source-root ./src/ui \
  --from mui \
  --to smartspec-ui \
  --audit-summary .spec/reports/ui-component-audit/latest/summary.json \
  --token-map .smartspec/mappings/design-tokens.json \
  --apply \
  --confidence-threshold medium
```

### Kilo Code Usage

The workflow can be invoked within a SmartSpec Kilo Code environment.

**Preview Mode:**

```bash
/smartspec_design_system_migration_assistant.md \
  --source-root ./src/ui \
  --from antd \
  --to smartspec-ui \
  --framework react \
  --style-system css-in-js \
  --kilocode
```

**Apply Mode:**

```bash
/smartspec_design_system_migration_assistant.md \
  --source-root ./src/ui \
  --from antd \
  --to smartspec-ui \
  --audit-summary .spec/reports/ui-component-audit/20240101/summary.json \
  --apply \
  --out .spec/reports/design-system-migration/run_antd_to_smartspec \
  --kilocode
```

## Use Cases

### Use Case 1: Component and Token Migration (Preview)

**Scenario:** A development team needs to estimate the effort required to migrate a large React application from the older `MUI` library to a new internal library, `SmartSpec-UI`. They want to see all proposed changes, including component renaming and design token updates, before committing.

**Command (CLI):**

```bash
/smartspec_design_system_migration_assistant \
  --source-root ./src/app \
  --from mui \
  --to smartspec-ui \
  --audit-summary .spec/reports/ui-component-audit/latest/summary.json \
  --token-map .smartspec/mappings/mui_to_smartspec.json \
  --framework react \
  --confidence-threshold high \
  --include-globs "**/*.tsx"
```

**Expected Result:**

The workflow runs in Preview Mode (default). It generates a `report.md` detailing:
1.  The number of high-confidence changes (e.g., `Button` -> `SmartButton`).
2.  The number of medium-confidence changes (e.g., prop mapping changes).
3.  A `changes.patch` file showing the unified diff for all proposed modifications.
4.  A list of manual follow-ups for low-confidence or unsupported patterns.
5.  Exit code `0`. No source files are modified.

### Use Case 2: Applying High-Confidence Changes Only

**Scenario:** After reviewing the preview, the team decides to automatically apply only the safest, high-confidence changes (like import path updates and simple component renames) to minimize manual review time, while leaving medium and low confidence changes for later.

**Command (CLI):**

```bash
/smartspec_design_system_migration_assistant \
  --source-root ./src/app \
  --from mui \
  --to smartspec-ui \
  --audit-summary .spec/reports/ui-component-audit/latest/summary.json \
  --token-map .smartspec/mappings/mui_to_smartspec.json \
  --apply \
  --confidence-threshold high \
  --apply-scope high_only
```

**Expected Result:**

1.  The workflow validates all paths and trust rules (DSM-000, DSM-001).
2.  For every file modified, a backup is created under `.spec/reports/design-system-migration/<run-id>/backups/`.
3.  Only changes labeled with `high` confidence are applied using atomic writes.
4.  The final `report.md` confirms that `--apply` was used, lists the files changed, and provides instructions for rollback using the backup location.
5.  Exit code `0`.

### Use Case 3: Targeted Migration in Kilo Code

**Scenario:** A specific feature branch only uses Vue components and needs migration from `Chakra` to `SmartSpec-UI`. The migration must be bounded to prevent long execution times.

**Command (Kilo Code):**

```bash
/smartspec_design_system_migration_assistant.md \
  --source-root ./src/features/new-dashboard \
  --from chakra \
  --to smartspec-ui \
  --framework vue \
  --max-files 50 \
  --exclude-globs "**/tests/**" \
  --kilocode
```

**Expected Result:**

1.  The workflow scans a maximum of 50 files within the specified source root, excluding test files.
2.  A preview report is generated, focusing on Vue component transformations (e.g., template syntax changes).
3.  If the file limit is reached, the report includes a **DSM-201 Reduced Coverage** warning, indicating that the migration is partial.
4.  Exit code `0`.

## Parameters

| Parameter | Type | Required | Description | Governance Notes |
| :--- | :--- | :--- | :--- | :--- |
| `--source-root <path>` | Path | **Yes** | Root directory of UI source code to migrate. | Must exist and be a directory. |
| `--from <name>` | String | **Yes** | Source design system/library identifier (e.g., `mui`, `antd`). | |
| `--to <name>` | String | **Yes** | Target design system/library identifier. | |
| `--apply` | Flag | No | Enables governed code modifications (Apply Mode). | Triggers backup and atomic write requirements. |
| `--audit-summary <path>` | Path | No | Path to a `smartspec_ui_component_audit` `summary.json`. | Used for token paths and findings. Must pass trust rules (DSM-001). |
| `--token-map <path>` | Path | No | Explicit mapping file (JSON/YAML) defining token and component mappings. | |
| `--include-globs <glob>` | String | No | Restrict migration to matching files (comma-separated). | |
| `--exclude-globs <glob>` | String | No | Exclude files from migration (comma-separated). | |
| `--framework <type>` | String | No | Target framework (`react`, `next`, `vue`, `svelte`, `auto`). | Default: `auto`. |
| `--style-system <type>` | String | No | Style system used (`css`, `tailwind`, `css-in-js`, `auto`). | Default: `auto`. |
| `--max-files <int>` | Integer | No | Bounded scanning limit (number of files). | |
| `--max-bytes <int>` | Integer | No | Bounded scanning limit (total size in bytes). | |
| `--max-seconds <int>` | Integer | No | Bounded scanning limit (execution time). | |
| `--confidence-threshold <level>` | String | No | Minimum confidence required for auto-apply transformations (`high` or `medium`). | Default: `high`. |
| `--apply-scope <scope>` | String | No | Defines which confidence levels are applied (`high_only` or `high_and_medium`). | Default: `high_only`. |
| `--out <output-root>` | Path | No | Requested base output root for reports. | Must pass output root safety checks. |
| `--json` | Flag | No | Output primary report as JSON (in addition to standard