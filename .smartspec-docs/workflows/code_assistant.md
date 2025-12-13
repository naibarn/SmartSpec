| manual_name | manual_version | compatible_workflow | compatible_workflow_versions |
|-------------|----------------|---------------------|------------------------------|
| /smartspec_code_assistant Manual (EN) | 6.0 | /smartspec_code_assistant | 6.0.x |

# /smartspec_code_assistant Manual (v6.0, English)

## 1. Overview

This manual explains how to use the workflow:

The `/smartspec_code_assistant` workflow provides AI-powered code assistance for implementing tasks, fixing errors, and refactoring code within the SmartSpec governance framework.

**Purpose:** Assist developers with code implementation, error fixing, and refactoring while maintaining SmartSpec governance principles and code quality standards.

**Version:** 6.0  
**Category:** implementation

---

## 2. Usage

This workflow supports invocation via the Command Line Interface (CLI) and Kilo Code (internal scripting environment).

### 🔗 CLI Usage

The CLI invocation requires specifying the assistance type and target files or tasks.

```bash
/smartspec_code_assistant \
  --mode <implement|fix|refactor> \
  --target <file_or_task> \
  [--context <spec_or_plan>] \
  [--apply]
```

### Kilo Code Usage

The Kilo Code invocation is identical to the CLI structure, typically used within automated pipelines or internal scripts.

**Important:** When using Kilo Code, you MUST include `--platform kilo` flag.

```bash
/smartspec_code_assistant.md \
  --mode <implement|fix|refactor> \
  --target <file_or_task> \
  [--context <spec_or_plan>] \
  [--apply] \
  --platform kilo
```

---

## 3. Use Cases

### Use Case 1: Implementing a Task (CLI)

**Scenario:** A developer needs assistance implementing a specific task from the tasks.md file.

**Command:**

```bash
/smartspec_code_assistant \
  --mode implement \
  --target "TASK-001" \
  --context specs/auth/login_service/spec.md
```

**Expected Result:**

1. The workflow loads the task and spec context.
2. It generates implementation code suggestions.
3. A preview bundle is written to `.spec/reports/code-assistant/<run-id>/`.
4. No code changes are applied (no `--apply` flag).
5. Exit code `0` (Success).

### Use Case 2: Fixing Errors in a File (Kilo Code)

**Scenario:** A CI pipeline detects errors in a source file and needs automated fix suggestions.

**Command (Kilo Code Snippet):**

```bash
/smartspec_code_assistant.md \
  --mode fix \
  --target src/services/payment.ts \
  --apply \
  --platform kilo
```

**Expected Result:**

1. The workflow analyzes the target file for errors.
2. It generates fix suggestions based on error patterns.
3. With `--apply`, the fixes are applied to the file.
4. Exit code `0` (Success).

### Use Case 3: Refactoring Code (CLI)

**Scenario:** A developer wants to refactor a module to improve code quality and maintainability.

**Command:**

```bash
/smartspec_code_assistant \
  --mode refactor \
  --target src/utils/validation.ts \
  --json
```

**Expected Result:**

1. The workflow analyzes the target file.
2. It generates refactoring suggestions.
3. Output includes `summary.json` with refactoring recommendations.
4. No code changes are applied (no `--apply` flag).
5. Exit code `0` (Success).

---

## 4. Parameters

The following parameters and flags control the execution and behavior of the `/smartspec_code_assistant` workflow.

### Required Parameters

| Parameter | Type | Description | Validation |
| :--- | :--- | :--- | :--- |
| `--mode` | `<string>` | Assistance mode: `implement`, `fix`, or `refactor`. | Must be one of the allowed values. |
| `--target` | `<string>` | Target file path or task ID. | Must exist and be accessible. |

### Universal Flags

| Flag | Description | Default | Platform Support |
| :--- | :--- | :--- | :--- |
| `--config` | Path to the SmartSpec configuration file. | `.spec/smartspec.config.yaml` | `cli` \| `kilo` \| `ci` \| `other` |
| `--lang` | Language for report generation (e.g., `th`, `en`). | (System default) | `cli` \| `kilo` \| `ci` \| `other` |
| `--platform` | Execution platform context. **Required for Kilo Code.** | (Inferred) | `cli` \| `kilo` \| `ci` \| `other` |
| `--apply` | Enables code changes to be applied. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--out` | Base path for safe outputs. | `.spec/reports/code-assistant/` | `cli` \| `kilo` \| `ci` \| `other` |
| `--json` | Output in JSON format. | `false` | `cli` \| `kilo` \| `ci` \| `other` |
| `--quiet` | Suppress standard output logs. | `false` | `cli` \| `kilo` \| `ci` \| `other` |

### Workflow-Specific Flags

| Flag | Description | Platform Support |
| :--- | :--- | :--- |
| `--context` | Path to spec or plan file for additional context. | `cli` \| `kilo` \| `ci` \| `other` |

---

## 5. Output

The workflow generates output artifacts according to its configuration.

### Output Files

| File Path | Description |
| :--- | :--- |
| `.spec/reports/code-assistant/<run-id>/...` | Safe output artifacts (code suggestions, analysis reports). |

---

## 6. Notes

- **Platform Flag:** When using Kilo Code, always include `--platform kilo` to ensure proper context and logging.
- **Preview Mode:** Without `--apply`, the workflow generates safe previews without modifying code files.
- **Governed Writes:** Use `--apply` flag to enable code changes.
- **Context Awareness:** Provide `--context` with spec or plan files for better code suggestions.
- **Configuration:** The workflow respects settings in `.spec/smartspec.config.yaml`.

---

**End of Manual**
