# SmartSpec Installation & Usage (Thin Wrapper)

> **Version:** 4.0.0  
> **Status:** Production Ready  
> **This document is a thin wrapper.**  
> Canonical governance lives in: `knowledge_base_smartspec_handbook.md`.

---

## 0) What to read first

Read the Canonical Handbook for:

- governance rules, write model, and security
- universal flag contract (minimal)
- SPEC_INDEX reuse/de-dup policy
- reference/research requirements
- UI/UX minimum standard
- workflow registry rules

This wrapper focuses only on installation, standard execution sequence, and short quickstart commands.

---

## 1) Installation overview

Install the SmartSpec workflow suite into your environment (CLI/Kilo/CI) using your platform’s standard method.

After installation, verify these directories exist:

- `.smartspec/workflows/`
- `.spec/` (contains `SPEC_INDEX.json`, `WORKFLOWS_INDEX.yaml`, `smartspec.config.yaml`)

---

## 2) What’s included

### 2.1 Core chain (most-used)

```text
/smartspec_generate_spec
/smartspec_generate_plan
/smartspec_generate_tasks
/smartspec_verify_tasks_progress_strict
/smartspec_report_implement_prompter
/smartspec_sync_tasks_checkboxes
/smartspec_project_copilot
```

### 2.2 Full listing

The complete list of workflows, aliases, write scopes, and supported platforms is stored in:

- `.spec/WORKFLOWS_INDEX.yaml`

---

## 3) Standard execution sequence

```text
SPEC → PLAN → TASKS → STRICT VERIFY → PROMPTER → implement → STRICT VERIFY → SYNC CHECKBOXES
```

Notes:

- **Governed artifacts** (anything under `specs/**` and registry files) require `--apply`.
- **Safe outputs** (reports/prompts/scripts) may be written without `--apply`.
- Workflow-generated helper scripts must be placed under **`.smartspec/generated-scripts/**`**.

---

## 4) Quickstart (positional-first)

> Replace paths with your own spec folder.

### 4.1 Generate / refine SPEC (governed → needs apply)

#### CLI

```bash
/smartspec_generate_spec \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_spec.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --apply
```

### 4.2 Generate PLAN (governed → needs apply)

#### CLI

```bash
/smartspec_generate_plan \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_plan.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

### 4.3 Generate TASKS (governed → needs apply)

#### CLI

```bash
/smartspec_generate_tasks \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_generate_tasks.md \
  specs/feature/spec-002-user-management/spec.md \
  --apply
```

### 4.4 Strict verify (safe output → no apply)

#### CLI

```bash
/smartspec_verify_tasks_progress_strict \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json
```

#### Kilo Code

```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-002-user-management/tasks.md \
  --out .spec/reports/verify-tasks-progress/spec-002 \
  --json
```

### 4.5 Implementation prompter (safe output → no apply)

#### CLI

```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --out .smartspec/prompts/spec-002-user-management \
  --json
```

#### Kilo Code

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --out .smartspec/prompts/spec-002-user-management \
  --json
```

### 4.6 Sync tasks checkboxes (governed → needs apply)

#### CLI

```bash
/smartspec_sync_tasks_checkboxes \
  specs/feature/spec-002-user-management/tasks.md \
  --apply
```

#### Kilo Code

```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/feature/spec-002-user-management/tasks.md \
  --apply
```

---

## 5) Universal flags (quick reference)

All workflows share:

- `--config`, `--lang`, `--platform`, `--apply`, `--out`, `--json`, `--quiet`

See the Canonical Handbook for definitions.

---

# End of Thin Wrapper

