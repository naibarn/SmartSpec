# /smartspec_implement_tasks Manual (v6.0, English)

## Overview

The `/smartspec_implement_tasks` workflow is the core execution engine within the SmartSpec ecosystem. Its primary purpose is to implement code changes strictly based on the tasks defined in `tasks.md`.

This workflow operates under strict SmartSpec v6 governance, emphasizing a tasks-first execution model, safe write gating, multi-repo read-only context, and mandatory reporting for evidence. It enforces privileged-ops hardening (no-shell, allowlist, timeouts) and is designed to integrate seamlessly with the Kilo Code Orchestrator for complex, multi-step implementations.

**Version:** 6.2.0
**Role:** implementation/execution

---

## Usage

### CLI Usage

The workflow is invoked via the command line, requiring the path to the `tasks.md` file as the primary positional argument. Write operations require explicit dual-gating (`--apply` and `--write-code`).

**Basic Syntax (Validate Only):**

```bash
/smartspec_implement_tasks <tasks.md_path> [flags]
```

**Example (Applying Changes):**

```bash
/smartspec_implement_tasks specs/feature_x/my_spec/tasks.md \
  --apply \
  --write-code \
  --tasks T001,T002 \
  --safety-mode strict
```

### Kilo Code Usage

When running under Kilo Code, the `--kilocode` flag must be used. For complex tasks, the workflow enforces Kilo Orchestrator sub-task decomposition (Invariants 0.2, 0.4). Kilo Code users often use the `.md` extension for clarity, though the execution is the same.

**Basic Syntax (Kilo Code):**

```bash
/smartspec_implement_tasks.md <tasks.md_path> --kilocode [flags]
```

**Example (Orchestrated Implementation):**

This example forces Orchestrator usage and applies changes, assuming it is running within a single Kilo sub-task focused on a specific range.

```bash
/smartspec_implement_tasks.md specs/feature_x/my_spec/tasks.md \
  --kilocode \
  --require-orchestrator \
  --apply \
  --write-code \
  --range 5-10 \
  --json
```

---

## Use Cases

### Use Case 1: Validating Implementation Plan (Dry Run)

**Scenario:** A developer wants to confirm the workflow can parse the tasks, identify the target files, and generate a change plan without modifying any code or task status.

**Goal:** Generate `change_plan.md` and `report.md` in validate-only mode.

**CLI Command:**

```bash
/smartspec_implement_tasks specs/api_refactor/v2/tasks.md \
  --validate-only \
  --tasks T005 \
  --out .spec/reports/api_refactor_v2_T005_dryrun
```

**Expected Result:**

1.  Exit code `0`.
2.  No changes to source code or `tasks.md`.
3.  Output directory `.spec/reports/api_refactor_v2_T005_dryrun` contains:
    *   `report.md`: Details the proposed implementation steps for T005.
    *   `change_plan.md`: A structured description of the file edits that *would* have occurred.
    *   `summary.json`: Status marked as `"status": "success"`, `"applied": false`.

### Use Case 2: Implementing a Set of Tasks with Code Writes

**Scenario:** The plan is approved. The developer needs to implement tasks T001, T002, and T003, which involve modifying source code and updating the `tasks.md` checkboxes.

**Goal:** Apply code changes, update checkboxes, and generate a final report.

**CLI Command:**

```bash
/smartspec_implement_tasks specs/ui_update/dark_mode/tasks.md \
  --apply \
  --write-code \
  --tasks T001,T002,T003 \
  --safety-mode strict
```

**Expected Result:**

1.  Exit code `0` (if successful).
2.  Source files (code/tests) are modified according to the implementation plan for T001-T003.
3.  The corresponding checkboxes for T001, T002, and T003 in `tasks.md` are marked as complete (`[x]`).
4.  A report is generated detailing the applied changes, with `summary.json` showing `"applied": true` and listing the files modified under the `writes` section.

### Use Case 3: Kilo Orchestration and Network Access

**Scenario:** Running under Kilo Code, the implementation requires fetching a new external dependency (network access) to complete task T010. The run must be orchestrated.

**Goal:** Implement T010, allowing network access, under Kilo Orchestrator control.

**Kilo Code Command:**

```bash
/smartspec_implement_tasks.md specs/deps_upgrade/tasks.md \
  --kilocode \
  --require-orchestrator \
  --apply \
  --write-code \
  --task T010 \
  --allow-network
```

**Expected Result:**

1.  The workflow verifies the Kilo Orchestrator context. If missing, it fails fast due to `--require-orchestrator`.
2.  Network access is temporarily granted for dependency resolution/fetch.
3.  Task T010 is implemented, modifying code and potentially lock files.
4.  Control is handed back to the Kilo Orchestrator upon sub-task completion, allowing the Orchestrator to decide the next step (e.g., running verification).
5.  A report is generated noting the use of `--allow-network`.

---

## Parameters

The following parameters (flags) are supported by `/smartspec_implement_tasks`:

| Category | Flag | Type | Description | Default |
| :--- | :--- | :--- | :--- | :--- |
| **Inputs** | Positional | Path | Path to the `tasks.md` file. | Required |
| **Inputs** | `--tasks-path` | Path | Overrides the positional path for `tasks.md`. | - |
| **Inputs** | `--spec-path` | Path | Override auto-detection of `spec.md`. | Auto-detect |
| **Inputs** | `--spec-id` | String | Resolve spec via `SPEC_INDEX.json`. | - |
| **Task Selection** | `--task <n>` | String | Select a single task number (e.g., T001). | - |
| **Task Selection** | `--tasks <csv>` | CSV | Select multiple tasks by comma-separated list. | - |
| **Task Selection** | `--range <a-b>` | Range | Select a range of tasks (e.g., 5-10). | - |
| **Task Selection** | `--from <n>` | Int | Start implementation from task number `n`. | - |
| **Task Selection** | `--start-from <Tnnn>` | String | Legacy alias for starting from a specific task ID. | - |
| **Task Selection** | `--skip-completed` | Flag | Skip tasks already marked complete. | Default |
| **Task Selection** | `--force-all` | Flag | Implement all tasks, regardless of completion status. | - |
| **Task Selection** | `--resume` | Flag | Attempt to resume a previously stalled run. | - |
| **Phases** | `--phase <n>` | Int | Select tasks tagged with a specific phase number. | - |
| **Phases** | `--phases <csv>` | CSV | Select tasks tagged with multiple phases. | - |
| **Phases** | `--phase-range <a-b>` | Range | Select tasks within a phase range. | - |
| **Write Gates** | `--apply` | Flag | **Gate 1:** Enables governed writes (reports, `tasks.md` notes/checkboxes). | Disabled |
| **Write Gates** | `--write-code` | Flag | **Gate 2:** Explicit opt-in to modify runtime source trees (requires `--apply`). | Disabled |
| **Safety/Preview** | `--validate-only` | Flag | Run in dry-run mode (no code or task status writes). | - |
| **Safety/Preview** | `--dry-run` | Flag | Alias for `--validate-only`. | - |
| **Safety/Preview** | `--safety-mode <strict|dev>` | String | Set the governance safety level. | `strict` |
| **Safety/Preview** | `--strict` | Flag | Alias for `--safety-mode strict`. | - |
| **Kilo/Orchestrator** | `--kilocode` | Flag | Enable Kilo integration semantics. | Disabled |
| **Kilo/Orchestrator**