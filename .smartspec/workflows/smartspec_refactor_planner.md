# smartspec_refactor_planner

---

## 📝 Frontmatter (YAML)

```yaml
version: 1.0.0
workflow_id: smartspec_refactor_planner
summary: "Automated code smell detection and refactor planning"
author: Manus AI
license: MIT

# Governance & Safety
safety:
  allow_writes_only_under:
    - ".spec/reports/refactoring/"
    - ".spec/reports/previews/"
  deny_writes_under:
    - ".git/"
    - ".smartspec/"
    - "src/"

# AI Agent Configuration
ai_config:
  persona: "Experienced software architect focused on code quality"
  capabilities:
    - static_code_analysis
    - architectural_pattern_recognition
    - task_generation

# Universal Flags Support
flags:
  - "--help"
  - "--version"
  - "--dry-run"
  - "--apply"
  - "--verbose"
```

---

## 📚 Overview

`/smartspec_refactor_planner` is a workflow dedicated to improving code quality by automatically detecting code smells, identifying refactoring opportunities, and creating detailed plans for implementation.

**Key Features:**
- ✅ Scans codebase for common code smells (e.g., long methods, large classes, duplicated code)
- ✅ Identifies architectural patterns and anti-patterns
- ✅ Suggests refactoring opportunities with clear justifications
- ✅ Generates refactoring plans with step-by-step instructions
- ✅ Creates tasks for refactoring work in `tasks.md`

---

## 🎯 Behavior

### 1. Analyze Codebase
- The agent performs static analysis on the codebase
- It identifies code smells and technical debt using a variety of metrics
- It recognizes architectural patterns and areas for improvement

### 2. Identify Refactoring Opportunities
- Based on the analysis, the agent identifies a list of potential refactoring opportunities
- Each opportunity is prioritized based on its potential impact and effort required

### 3. Generate Refactoring Plan
- For each high-priority opportunity, the agent generates a detailed refactoring plan
- The plan includes:
  - The problem to be solved
  - The proposed solution (e.g., "Extract Method", "Introduce Facade")
  - Step-by-step implementation guide
  - Verification and testing strategy

### 4. Create Refactoring Tasks (with --apply)
- If `--apply` is used, the agent creates a new `tasks.md` file with tasks for each refactoring item
- Each task is linked to the refactoring plan and includes clear acceptance criteria

---

## ⚙️ Governance Contract

- **Allowed writes:** `.spec/reports/refactoring/`, `.spec/reports/previews/`
- **Forbidden writes:** `.git/`, `.smartspec/`, `src/`
- **--apply required:** To create tasks.md

---

## 🚩 Flags

### Universal flags (must support)

All SmartSpec workflows support these universal flags:

| Flag | Required | Description |
|---|---|---|
| `--config` | No | Path to custom config file (default: `.spec/smartspec.config.yaml`) |
| `--lang` | No | Output language (`th` for Thai, `en` for English, `auto` for automatic detection) |
| `--platform` | No | Platform mode (`cli` for CLI, `kilo` for Kilo Code, `ci` for CI/CD, `other` for custom integrations) |
| `--out` | No | Base output directory for reports and generated files (must pass safety checks) |
| `--json` | No | Output results in JSON format for machine parsing and automation |
| `--quiet` | No | Suppress non-essential output, showing only errors and critical information |

### Workflow-specific flags

Flags specific to `/smartspec_refactor_planner`:

| Flag | Required | Description |
|---|---|---|
| `--run-analysis` | Yes | Run the code smell detection and refactoring analysis |
| `--target` | Yes | Path to code/module to analyze (e.g., `src/api/auth`) |
| `--scope` | No | Limit the analysis to a specific directory or file (overrides --target) |
| `--min-impact` | No | Report only opportunities with a minimum impact level (low, medium, high, critical) |
| `--auto-plan` | No | Automatically generate detailed plans for all high-impact opportunities |
| `--apply` | No | Enable creation of tasks.md with refactoring tasks |
| `--dry-run` | No | Perform analysis and planning without creating any tasks (preview mode) |
| `--help` | No | Show help message and usage examples |
| `--version` | No | Show workflow version information |
| `--verbose` | No | Show detailed analysis output including all code smells detected |

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file
- **Preview-first:** Use `--dry-run` to preview refactoring recommendations before using `--apply`
- **Impact filtering:** Use `--min-impact high` to focus on the most important refactoring opportunities
