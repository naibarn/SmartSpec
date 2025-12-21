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

Flags specific to `/smartspec_dependency_updater`:

| Flag | Required | Description |
|---|---|---|
| `--run-scan` | Yes | Run the dependency scan across all package managers |
| `--package-manager` | No | Scan only for a specific package manager (npm, pip, maven, gradle, composer, etc.) |
| `--security-level` | No | Report only vulnerabilities above a certain level (low, medium, high, critical) |
| `--auto-update-safe` | No | Automatically create tasks for safe updates (minor and patch versions only) |
| `--apply` | No | Enable creation of tasks.md with update instructions |
| `--dry-run` | No | Perform scan and analysis without creating any tasks (preview mode) |
| `--help` | No | Show help message and usage examples |
| `--version` | No | Show workflow version information |
| `--verbose` | No | Show detailed output including all scanned dependencies |

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file
- **Preview-first:** Use `--dry-run` to preview changes before using `--apply`
- **Security focus:** Use `--security-level high` or `--security-level critical` in CI/CD to fail on serious vulnerabilities
