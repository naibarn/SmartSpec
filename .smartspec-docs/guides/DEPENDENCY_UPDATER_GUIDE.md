# Guide: smartspec_dependency_updater

## 📚 Overview

`/smartspec_dependency_updater` is a proactive workflow designed to automate the process of scanning for outdated dependencies, assessing their impact, and creating tasks for safe updates.

**Key Features:**
- ✅ Scans for outdated dependencies across multiple package managers (npm, pip, Maven, etc.)
- ✅ Assesses security vulnerabilities (CVEs) and breaking changes
- ✅ Generates impact analysis reports
- ✅ Creates tasks for dependency updates with clear instructions
- ✅ Integrates with `smartspec_implement_tasks` for automated updates

---

## 🎯 Basic Usage

This workflow is typically run on a schedule (e.g., weekly) as a background process.

### Running the Scanner

```bash
/smartspec_dependency_updater --run-scan
```

**Behavior:**
1.  Scans all dependency files in the repository.
2.  Generates a report in `.spec/reports/dependency-updates/`.
3.  Does not create tasks unless `--apply` is used.

### Creating Update Tasks

```bash
/smartspec_dependency_updater --run-scan --apply --auto-update-safe
```

**Behavior:**
1.  Runs the scan.
2.  Generates a report.
3.  Creates a `tasks.md` file with tasks for all safe updates (minor and patch versions).

---

## ⚙️ Workflow Cycle

1.  **Scan:** The workflow scans for outdated dependencies.
2.  **Assess:** It checks for security vulnerabilities and breaking changes.
3.  **Report:** A detailed report is generated.
4.  **Plan:** With `--apply`, it creates a `tasks.md` file.
5.  **Implement:** `smartspec_implement_tasks` can be used to automatically perform the updates.
6.  **Verify:** The implementation workflow runs tests to verify the updates.

---

## 🚩 Flags

- `--run-scan`: **(Required)** Run the dependency scan.
- `--package-manager <name>`: Scan only for a specific package manager (e.g., `npm`, `pip`).
- `--security-level <level>`: Report only vulnerabilities above a certain level (e.g., `high`, `critical`).
- `--auto-update-safe`: Automatically create tasks for safe updates (minor and patch versions).
- `--apply`: Create a `tasks.md` file with update tasks.
