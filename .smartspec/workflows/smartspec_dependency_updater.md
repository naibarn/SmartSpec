# smartspec_dependency_updater

---

## 📝 Frontmatter (YAML)

```yaml
version: 1.0.0
workflow_id: smartspec_dependency_updater
summary: "Automated dependency scanning and update management"
author: Manus AI
license: MIT

# Governance & Safety
safety:
  allow_writes_only_under:
    - ".spec/reports/dependency-updates/"
    - ".spec/reports/previews/"
  deny_writes_under:
    - ".git/"
    - ".smartspec/"
    - "src/"

# AI Agent Configuration
ai_config:
  persona: "Security-conscious dependency manager"
  capabilities:
    - dependency_analysis
    - impact_assessment
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

`/smartspec_dependency_updater` is a proactive workflow designed to automate the process of scanning for outdated dependencies, assessing their impact, and creating tasks for safe updates.

**Key Features:**
- ✅ Scans for outdated dependencies across multiple package managers (npm, pip, Maven, etc.)
- ✅ Assesses security vulnerabilities (CVEs) and breaking changes
- ✅ Generates impact analysis reports
- ✅ Creates tasks for dependency updates with clear instructions
- ✅ Integrates with `smartspec_implement_tasks` for automated updates

---

## 🎯 Behavior

### 1. Scan for Outdated Dependencies
- The agent scans all dependency files (`package.json`, `requirements.txt`, etc.)
- It compares current versions with the latest available versions
- It identifies outdated dependencies and their severity (major, minor, patch)

### 2. Assess Impact
- For each outdated dependency, the agent:
  - Checks for known security vulnerabilities (CVEs)
  - Analyzes changelogs for breaking changes
  - Determines the potential impact on the codebase

### 3. Generate Report
- The agent generates a detailed report in `.spec/reports/dependency-updates/`
- The report includes:
  - List of outdated dependencies
  - Security vulnerabilities found
  - Recommended update actions
  - Impact assessment

### 4. Create Update Tasks (with --apply)
- If `--apply` is used, the agent creates a new `tasks.md` file with tasks for each dependency update
- Each task includes:
  - Dependency name and version
  - Update instructions
  - Verification steps
  - Rollback plan

---

## ⚙️ Governance Contract

- **Allowed writes:** `.spec/reports/dependency-updates/`, `.spec/reports/previews/`
- **Forbidden writes:** `.git/`, `.smartspec/`, `src/`
- **--apply required:** To create tasks.md

---

## 🚩 Flags

- `--run-scan`: **(Required)** Run the dependency scan
- `--package-manager <name>`: Scan only for a specific package manager (e.g., `npm`, `pip`)
- `--security-level <level>`: Report only vulnerabilities above a certain level (e.g., `high`, `critical`)
- `--auto-update-safe`: Automatically create tasks for safe updates (minor and patch versions)
