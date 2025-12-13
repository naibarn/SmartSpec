# Workflow Chain Example: Migrating from MUI to Ant Design

This document outlines a complete, end-to-end workflow for migrating a frontend application from Material-UI (MUI) to Ant Design using the SmartSpec v6 workflow suite. This process emphasizes safety, verifiability, and automation.

## Scenario

- **Goal:** Migrate a web application's frontend from MUI to Ant Design.
- **Scope:** Replace all MUI components with their Ant Design equivalents and adopt the new Ant Design-based design tokens.
- **Principle:** The migration must be verifiable at every step, with a clear rollback path in case of issues.

---

## Phase 1: Planning and Initial Audit

**Objective:** Define the scope of the migration and get a baseline understanding of the current implementation.

1.  **Generate Migration Specification (`spec.md`)**
    - **Workflow:** `/smartspec_generate_spec_from_prompt`
    - **Purpose:** Create a formal specification document for the migration project itself. This serves as the source of truth for the migration's goals.
    - **Command:**
      ```bash
      /smartspec_generate_spec_from_prompt \
        --prompt "Create a specification for migrating the project's frontend from MUI to Ant Design. The goal is to replace all MUI components and adopt the new Ant Design theme. The migration should be done incrementally and be verifiable." \
        --spec-id "FE-MUI-to-AntD-Migration"
      ```

2.  **Generate Migration Plan (`plan.md`)**
    - **Workflow:** `/smartspec_generate_plan`
    - **Purpose:** Break down the migration spec into high-level, manageable phases.
    - **Command:**
      ```bash
      /smartspec_generate_plan \
        --spec specs/project/FE-MUI-to-AntD-Migration/spec.md
      ```

3.  **Initial UI Audit (Baseline)**
    - **Workflow:** `/smartspec_ui_component_audit`
    - **Purpose:** Scan the current codebase to identify every instance of an MUI component or a hardcoded value. This report is the primary input for the migration assistant.
    - **Command:**
      ```bash
      /smartspec_ui_component_audit \
        --source-root src \
        --component-library mui \
        --design-tokens design-system/mui-tokens.json \
        --out .spec/reports/ui-audit-baseline
      ```

---

## Phase 2: Pre-Migration Quality & Security Checks

**Objective:** Ensure the application is in a stable and secure state *before* starting major refactoring. This helps isolate any new issues to the migration itself.

1.  **Generate Threat Model (`threats.md`)**
    - **Workflow:** `/smartspec_security_threat_modeler`
    - **Purpose:** Analyze the migration plan for potential security risks (e.g., risks associated with adding a new library).
    - **Command:**
      ```bash
      /smartspec_security_threat_modeler \
        specs/project/FE-MUI-to-AntD-Migration/spec.md
      ```

2.  **Validate API Contracts**
    - **Workflow:** `/smartspec_api_contract_validator`
    - **Purpose:** Ensure the frontend and backend are in sync before changing the UI.
    - **Command:**
      ```bash
      /smartspec_api_contract_validator \
        --contract path/to/openapi.yaml \
        --implementation-root path/to/backend/src
      ```

3.  **Validate Data Models**
    - **Workflow:** `/smartspec_data_model_validator`
    - **Purpose:** Ensure the database schema matches the application's expectations.
    - **Command:**
      ```bash
      /smartspec_data_model_validator \
        specs/project/FE-MUI-to-AntD-Migration/spec.md \
        --schema-files "db/schema.ts"
      ```

---

## Phase 3: Automated Migration and Refactoring

**Objective:** Use the audit results to automatically refactor the codebase.

1.  **Generate Migration Tasks (`tasks.md`)**
    - **Workflow:** `/smartspec_generate_tasks`
    - **Purpose:** Create a detailed, machine-readable list of tasks based on the migration plan and the baseline audit report.
    - **Command:**
      ```bash
      /smartspec_generate_tasks \
        --spec specs/project/FE-MUI-to-AntD-Migration/spec.md \
        --context .spec/reports/ui-audit-baseline/<run-id>/summary.json
      ```

2.  **Run Migration Assistant (Preview Mode)**
    - **Workflow:** `/smartspec_design_system_migration_assistant`
    - **Purpose:** Generate a `migration.diff` file showing all proposed code changes without actually modifying any files. This is a critical review step.
    - **Command:**
      ```bash
      /smartspec_design_system_migration_assistant \
        --audit-report .spec/reports/ui-audit-baseline/<run-id>/summary.json \
        --source-root src
      ```

3.  **Review the Diff File**
    - **Action:** Manually review the generated `migration.diff` file to ensure the proposed changes are correct and logical.

4.  **Run Migration Assistant (Apply Mode)**
    - **Workflow:** `/smartspec_design_system_migration_assistant`
    - **Purpose:** Apply the changes to the source code.
    - **Command:**
      ```bash
      /smartspec_design_system_migration_assistant \
        --audit-report .spec/reports/ui-audit-baseline/<run-id>/summary.json \
        --source-root src \
        --apply
      ```

---

## Phase 4: Post-Migration Verification

**Objective:** Verify that the migration was successful, all tasks are complete, and the new implementation adheres to the new design system.

1.  **Verify Task Completion**
    - **Workflow:** `/smartspec_verify_tasks_progress_strict`
    - **Purpose:** Check the source code for evidence that the migration tasks (e.g., "remove all MUI imports") have been completed.
    - **Command:**
      ```bash
      /smartspec_verify_tasks_progress_strict \
        --tasks specs/project/FE-MUI-to-AntD-Migration/tasks.md
      ```

2.  **Final UI Audit (Ant Design)**
    - **Workflow:** `/smartspec_ui_component_audit`
    - **Purpose:** Run the audit again, but this time configured for Ant Design, to ensure the new code is compliant.
    - **Command:**
      ```bash
      /smartspec_ui_component_audit \
        --source-root src \
        --component-library antd \
        --design-tokens design-system/antd-tokens.json
      ```

3.  **Final Security Audit**
    - **Workflow:** `/smartspec_security_audit_reporter`
    - **Purpose:** Generate a final report confirming that all identified security threats have been addressed.
    - **Command:**
      ```bash
      /smartspec_security_audit_reporter \
        specs/project/FE-MUI-to-AntD-Migration/spec.md
      ```

---

## Phase 5: Emergency Rollback (If Necessary)

**Objective:** Provide a safe exit if the migration introduces critical bugs.

1.  **Run Rollback Assistant (Preview Mode)**
    - **Workflow:** `/smartspec_migration_rollback_assistant`
    - **Purpose:** Perform a dry run to ensure the code can be reverted cleanly.
    - **Command:**
      ```bash
      /smartspec_migration_rollback_assistant \
        --migration-report .spec/reports/ds-migration-assistant/<migration-run-id>/
      ```

2.  **Review Rollback Plan**
    - **Action:** Check the report to confirm which files will be reverted.

3.  **Run Rollback Assistant (Apply Mode)**
    - **Workflow:** `/smartspec_migration_rollback_assistant`
    - **Purpose:** Revert all changes by applying the reverse patch.
    - **Command:**
      ```bash
      /smartspec_migration_rollback_assistant \
        --migration-report .spec/reports/ds-migration-assistant/<migration-run-id>/ \
        --apply
      ```

This comprehensive chain ensures that a complex migration is broken down into verifiable, automated, and safe steps, significantly reducing risk and manual effort.
