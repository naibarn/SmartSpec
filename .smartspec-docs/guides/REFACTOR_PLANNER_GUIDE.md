# Guide: smartspec_refactor_planner

## 📚 Overview

`/smartspec_refactor_planner` is a workflow dedicated to improving code quality by automatically detecting code smells, identifying refactoring opportunities, and creating detailed plans for implementation.

**Key Features:**
- ✅ Scans codebase for common code smells (e.g., long methods, large classes, duplicated code)
- ✅ Identifies architectural patterns and anti-patterns
- ✅ Suggests refactoring opportunities with clear justifications
- ✅ Generates refactoring plans with step-by-step instructions
- ✅ Creates tasks for refactoring work in `tasks.md`

---

## 🎯 Basic Usage

This workflow can be run on-demand by developers or architects.

### Running the Analysis

```bash
/smartspec_refactor_planner --run-analysis --scope src/core/
```

**Behavior:**
1.  Analyzes the code in the `src/core/` directory.
2.  Generates a report in `.spec/reports/refactoring/` with identified opportunities.

### Creating Refactoring Tasks

```bash
/smartspec_refactor_planner --run-analysis --apply --min-impact high
```

**Behavior:**
1.  Runs the analysis on the entire codebase.
2.  Generates a report.
3.  Creates a `tasks.md` file with tasks for all high-impact refactoring opportunities.

---

## ⚙️ Workflow Cycle

1.  **Analyze:** The workflow scans the codebase for code smells.
2.  **Identify:** It identifies and prioritizes refactoring opportunities.
3.  **Plan:** It generates detailed refactoring plans.
4.  **Taskify:** With `--apply`, it creates a `tasks.md` file.
5.  **Implement:** Developers use the plans and tasks to perform the refactoring.

---

## 🚩 Flags

- `--run-analysis`: **(Required)** Run the code analysis.
- `--scope <path>`: Limit the analysis to a specific directory or file.
- `--min-impact <level>`: Report only opportunities with a minimum impact level (e.g., `medium`, `high`).
- `--auto-plan`: Automatically generate plans for all high-impact opportunities.
- `--apply`: Create a `tasks.md` file with refactoring tasks.
