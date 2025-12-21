---
description: Convert spec.md (or plan.md) → tasks.md with 100% duplication prevention.
version: 7.0.0
workflow: /smartspec_generate_tasks
---

# smartspec_generate_tasks

> **Canonical path:** `.smartspec/workflows/smartspec_generate_tasks.md`  
> **Version:** 7.0.0  
> **Status:** Production Ready  
> **Category:** core

## Purpose

Generate or refine `tasks.md` from `spec.md` (or `plan.md`) with **100% duplication prevention** and **reuse-first** governance.

This workflow is the canonical source for creating tasks that downstream workflows can trust:

- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_report_implement_prompter`
- `/smartspec_quality_gate`

It is **safe-by-default** and writes governed artifacts only when explicitly applied.

---

## File Locations (Important for AI Agents)

**All SmartSpec configuration and registry files are located in the `.spec/` folder:**

- **Config:** `.spec/smartspec.config.yaml`
- **Spec Index:** `.spec/SPEC_INDEX.json`
- **Registry:** `.spec/registry/` (component registry, reuse index)
- **Reports:** `.spec/reports/` (workflow outputs, previews, diffs)
- **Scripts:** `.spec/scripts/` (automation scripts)

**When searching for these files, ALWAYS use the `.spec/` prefix from project root.**

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes:

- Governed specs: `specs/**` (**requires** `--apply`)
- Safe outputs (previews/reports): `.spec/reports/generate-tasks/**` (no `--apply` required)

Forbidden writes (must hard-fail):

- Any path outside config `safety.allow_writes_only_under`
- Any path under config `safety.deny_writes_under` (e.g., `.spec/registry/**`, `.spec/cache/**`)
- Any runtime source tree modifications

### `--apply` behavior

- Without `--apply`:
  - MUST NOT modify `specs/**/tasks.md`.
  - MUST write a deterministic preview bundle to `.spec/reports/`.
- With `--apply`:
  - MAY update or create `specs/**/tasks.md`.
  - MUST NOT modify any other files.

---

## Behavior

### 1) Pre-Generation Validation (MANDATORY)

Before generating tasks, the AI agent **MUST** check for existing similar tasks in other specs.

**Validation Command:**
```bash
python3 .spec/scripts/detect_duplicates.py \
  --registry-dir .spec/registry/ \
  --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** No duplicates found. The agent may proceed.
- **Exit Code `1` (Failure):** Potential duplicates found. The agent **MUST**:
  - Present the duplicates to the user.
  - Ask the user to:
    a) Reuse existing components/tasks
    b) Justify creating new tasks
    c) Cancel and review existing specs
  - **MUST NOT** proceed until the user confirms.

### 2) Produce task graph

- Convert scope into milestones + tasks.
- Ensure every milestone has verifiable outputs (evidence hooks).

### 3) Preview & report (always)

Write:

- `.spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md`
- `.spec/reports/generate-tasks/<run-id>/diff/<spec-id>.patch` (best-effort)
- `.spec/reports/generate-tasks/<run-id>/report.md`
- `.spec/reports/generate-tasks/<run-id>/summary.json` (if `--json`)

### 4) Post-Generation Validation (MANDATORY)

After generating the preview and before applying, the AI agent **MUST** validate the generated task list.

**Validation Command:**
```bash
python3 .spec/scripts/validate_tasks_enhanced.py \
  --tasks .spec/reports/generate-tasks/<run-id>/preview/<spec-id>/tasks.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** The tasks file is valid and complete. The agent may proceed with `--apply`.
- **Exit Code `1` (Failure):** The tasks file is invalid or incomplete. The agent **MUST NOT** use `--apply`.
- The full output from the validation script **MUST** be included in `report.md`.

### 5) Apply (only with `--apply` and if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.

---

## 10) `tasks.md` Content Templates (For AI Agent Implementation)

To ensure consistent and complete output, the AI agent executing this workflow MUST use the following templates when generating `tasks.md`.

### 10.1 Header Template

```markdown
| spec-id | source | generated_by | updated_at |
|---|---|---|---|
| `<spec-id>` | `spec.md` | `smartspec_generate_tasks:7.0.0` | `<ISO_DATETIME>` |
```

### 10.2 Task Item Template

Each task item under the `## Tasks` section MUST follow this template.

```markdown
- [ ] **TSK-<spec-id>-001: Setup initial project structure**
  - **Implements:** Feature - Project Scaffolding
  - **T-Reference:** T001 (Project Setup)
  - **Acceptance Criteria:**
    - [ ] A new directory is created for the project.
    - [ ] `package.json` is initialized.
    - [ ] Basic folder structure (`src`, `tests`, `docs`) is present.
  - **Evidence Hooks:**
    - **Code:** `package.json`, `src/`, `tests/`
    - **Verification:** Run `ls -lR` and check for directory structure.
```

### 10.3 Requirement Traceability Matrix (RTM) Template

```markdown
## Requirement Traceability Matrix

### Security Requirements Coverage

| Requirement ID | Description | Implementing Tasks | Coverage Status |
|---|---|---|---|
| SEC-001 | Password Hashing (bcrypt, cost 12) | TSK-AUTH-025 | ✅ Complete |
| SEC-002 | JWT Algorithm (RS256, JWKS endpoint) | TSK-AUTH-030, TSK-AUTH-031, TSK-AUTH-032 | ✅ Complete |

### Functional Requirements Coverage

| T-ID | Description | TSK-ID | Coverage Status |
|---|---|---|---|
| T001 | User Model (Prisma schema) | TSK-AUTH-020 | ✅ Complete |
| T010 | JWT Token Management (RS256) | TSK-AUTH-030 | ✅ Complete |
```

---

# End of workflow doc
