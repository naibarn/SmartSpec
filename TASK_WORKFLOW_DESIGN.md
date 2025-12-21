# `tasks.md` Enhancement Design

This document outlines the design for templates and validation requirements to improve the `smartspec_generate_tasks` workflow.

---

## 1. `tasks.md` Structure and Templates

The generated `tasks.md` file MUST follow this structure and use the provided templates.

### 1.1 Header

A markdown table header is required.

```markdown
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| `<spec-id>` | `spec.md` | `smartspec_generate_tasks:6.0.3` | `<ISO_DATETIME>` |
```

### 1.2 Readiness Checklist

A new mandatory section to ensure the task list is production-ready.

```markdown
## Readiness Checklist

- [ ] All tasks have a stable, unique ID (`TSK-<spec-id>-NNN`).
- [ ] All tasks have at least one specific evidence hook.
- [ ] All `TBD` evidence items are listed in the 'Open Questions' section.
- [ ] All acceptance criteria are verifiable.
- [ ] No secrets or sensitive data are present in the tasks.
```

### 1.3 Tasks Section

Each task item MUST follow this template.

```markdown
### Tasks

- [ ] **TSK-<spec-id>-001: Setup initial project structure**
  - **Acceptance Criteria:**
    - [ ] A new directory is created for the project.
    - [ ] `package.json` is initialized.
    - [ ] Basic folder structure (`src`, `tests`, `docs`) is present.
  - **Evidence Hooks:**
    - **Code:** `package.json`, `src/`, `tests/`
    - **Verification:** Run `ls -lR` and check for directory structure.
```

### 1.4 Evidence Mapping Section

This section maps task IDs to the specific artifacts that prove completion.

```markdown
## Evidence Mapping

| Task ID | Status | Evidence Artifacts | Verification Report |
|---|---|---|---|
| TSK-<spec-id>-001 | `[ ] Open` | `package.json`, `src/` | `TBD` |
| TSK-<spec-id>-002 | `[x] Done` | `src/api/auth.js` | `.spec/reports/verify/run-123.md` |
```

### 1.5 Open Questions / TBD Evidence

This section lists all tasks where evidence is not yet clearly defined.

```markdown
## Open Questions & TBD Evidence

| Task ID | Question / TBD Item |
|---|---|
| TSK-<spec-id>-003 | What is the exact API endpoint for the payment gateway? |
| TSK-<spec-id>-004 | Evidence for UI component rendering needs to be defined. |
```

---

## 2. Validation Script Requirements (`validate_tasks.py`)

The validation script will check for the following:

1.  **Header Presence:** The markdown table header with required fields (`spec-id`, `source`, `generated_by`, `updated_at`) must exist.
2.  **Readiness Checklist:** The `Readiness Checklist` section must exist and contain the required checklist items.
3.  **Required Sections:** The script must verify the presence of `## Tasks`, `## Evidence Mapping`, and `## Open Questions & TBD Evidence` sections.
4.  **Task Item Format:** For each task under `## Tasks`:
    - It must start with a checkbox (`- [ ]` or `- [x]`).
    - It must have a valid and unique Task ID (`TSK-<spec-id>-NNN`).
    - It must contain `**Acceptance Criteria:**`.
    - It must contain `**Evidence Hooks:**`.
5.  **Evidence Hook Specificity:** Under `**Evidence Hooks:**`, there must be at least one specific evidence type (`Code:`, `Test:`, `UI:`, `Docs:`, `Verification:`).
6.  **Evidence Mapping Consistency:**
    - Every Task ID from the `## Tasks` section must exist in the `## Evidence Mapping` table.
    - The status in the `Evidence Mapping` table should reflect the checkbox state.
7.  **TBD Consistency:** If a task has `TBD` in its evidence hook, it must be listed in the `## Open Questions & TBD Evidence` section.
8.  **No Secrets:** The script should scan for patterns that look like secrets and flag them.

This design will be used to create the `validate_tasks.py` script and update the `smartspec_generate_tasks.md` workflow documentation.
