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

- `--run-analysis`: **(Required)** Run the code analysis
- `--scope <path>`: Limit the analysis to a specific directory or file
- `--min-impact <level>`: Report only opportunities with a minimum impact level (e.g., `medium`, `high`)
- `--auto-plan`: Automatically generate plans for all high-impact opportunities
