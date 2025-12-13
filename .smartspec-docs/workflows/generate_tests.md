| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_generate_tests Manual (EN) | 6.1 | /smartspec_generate_tests | 6.1.x |

# /smartspec_generate_tests Manual (v6.1, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_generate_tests` workflow generates a comprehensive **test plan** from `spec.md` (and adjacent `tasks.md`, optional `ui.json`), aligned with registries and SmartSpec governance.

**Purpose:** Generate a SmartSpec-governed test plan (test matrix + acceptance criteria + required evidence) aligned with SmartSpec v6 governance. Default outputs are reports-only; optional apply writes the test plan into the spec folder under specs/**.

**Version:** 6.1.1  
**Category:** test-planning

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the target spec.md file as a positional argument.

```bash
/smartspec_generate_tests <spec_md> \
  [--apply] \
  [--test-target <path>] \
  [--json]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_generate_tests.md \
  <spec_md> \
  [--apply] \
  [--test-target <path>] \
  [--json] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Generating a Test Plan from a Specification (CLI)

**Scenario:** A QA engineer needs to create a comprehensive test plan for a "Shopping Cart" feature based on its specification (`specs/ecommerce/shopping_cart/spec.md`).

**Command:**

```bash
/smartspec_generate_tests specs/ecommerce/shopping_cart/spec.md
```

**Expected Result:**

1. The workflow loads `specs/ecommerce/shopping_cart/spec.md`.
2. It analyzes the spec content and generates a test matrix with acceptance criteria.
3. A preview bundle is written to `.spec/reports/generate-tests/<run-id>/`.
4. The preview includes `tests_preview.md` with test cases and evidence requirements.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 2: Applying Test Plan with Custom Target Path (Kilo Code)

**Scenario:** A CI pipeline needs to generate and apply a test plan for a spec, storing it in a custom location within the spec folder.

**Command (Kilo Code Snippet):**

```bash
/smartspec_generate_tests.md \
  specs/api/rest_endpoints/spec.md \
  --apply \
  --test-target specs/api/rest_endpoints/testplan/tests.md \
  --platform kilo
```

**Expected Result:**

1. The workflow loads `specs/api/rest_endpoints/spec.md`.
2. It generates a comprehensive test plan.
3. A preview bundle is written to `.spec/reports/generate-tests/<run-id>/`.
4. With `--apply`, the test plan is written to `specs/api/rest_endpoints/testplan/tests.md`.
5. Exit code `0` (Success).

### Use Case 3: Generating Test Plan with UI.json Integration (CLI)

**Scenario:** A developer has a spec with an accompanying `ui.json` file defining UI components. The test plan should include UI-specific test cases.

**Command:**

```bash
/smartspec_generate_tests specs/dashboard/analytics_dashboard/spec.md \
  --json
```

**Expected Result:**

1. The workflow loads `specs/dashboard/analytics_dashboard/spec.md`.
2. It detects and loads the adjacent `ui.json` file.
3. Test cases are generated for both functional and UI requirements.
4. A preview bundle is written to `.spec/reports/generate-tests/<run-id>/`.
5. The output includes `summary.json` with structured test metadata.
6. No governed writes occur (no `--apply` flag).
7. Exit code `0` (Success).

### Use Case 4: Preview-first Change Plan (CLI)

**Scenario:** A team lead wants to review what changes would be made to the test plan before applying them.

**Command:**

```bash
/smartspec_generate_tests specs/auth/oauth_integration/spec.md
```

**Expected Result:**

1. The workflow loads `specs/auth/oauth_integration/spec.md`.
2. It generates a test plan preview.
3. A **Change Plan** is created describing what would be written to governed paths.
4. The preview bundle includes `change_plan.md` with detailed diff.
5. No governed writes occur (no `--apply` flag).
6. Exit code `0` (Success).

### Use Case 5: Refusing Application Due to Path Traversal (CLI)

**Scenario:** A user attempts to specify a test target path that escapes the allowed scope. The workflow should detect this and refuse to proceed.

**Command:**

```bash
/smartspec_generate_tests specs/feature/new_feature/spec.md \
  --apply \
  --test-target ../../outside/tests.md
```

**Expected Result:**

1. The workflow validates the `--test-target` path.
2. It detects path traversal attempt (`..`).
3. The workflow **refuses** to proceed with path validation error.
4. A detailed error message is generated.
5. Exit code `2` (Path Validation Fail).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_generate_tests` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `<spec_md>` | `<path>` | Path to the spec.md file to generate tests from. | Must resolve under `specs/**` and must not escape via symlink. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables governed writes (creating test plan files). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs (reports/previews). | `.spec/reports/generate-tests/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output the primary summary in JSON format (`summary.json`). | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--test-target` | Custom path for the test plan file (requires `--apply`). | `specs/<category>/<spec-id>/testplan/tests.md` | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates two types of output artifacts: Safe Preview Bundles (always) and Governed Artifacts (only with `--apply`).

### Safe Preview Bundle (Always Generated)

A unique run folder is created under the report path (default: `.spec/reports/generate-tests/<run-id>/`).

**Contents:**

| File Path | Description |
| :--- | :--- |
| `tests_preview.md` | The generated test plan content (before apply). |
| `change_plan.md` | Description of what would be written to governed paths. |
| `summary.json` | (If `--json` is used) Structured test metadata and coverage analysis. |
| `report.md` | Detailed analysis including test matrix and evidence requirements. |

### Governed Artifacts (Only with `--apply`)

| File Path | Description |
| :--- | :--- |
| `specs/<category>/<spec-id>/testplan/tests.md` | The generated test plan file written to the governed location. |

---

## 6. Notes

- **Preview-first:** Always generates a Change Plan describing what would be written before applying changes.
- **Test Matrix:** Generated test plans include comprehensive test matrices with acceptance criteria.
- **Evidence Requirements:** Test cases include required evidence hooks for verification workflows.
- **UI Integration:** Automatically detects and integrates adjacent `ui.json` files for UI-specific test cases.
- **Path Security:** Enforces strict path validation to prevent traversal and symlink escape attacks.
- **Atomic Writes:** When `--apply` writes test plans, it uses atomic write semantics (temp+rename).
- **Network Policy:** This workflow respects `safety.network_policy.default=deny` and does not make external network requests.
- **Kilo Code Platform:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.

---

**End of Manual**
