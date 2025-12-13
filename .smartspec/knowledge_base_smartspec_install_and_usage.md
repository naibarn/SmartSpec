# knowledge_base_smartspec_install_and_usage.md

# SmartSpec Installation & Usage

> **Version:** 6.1.1  
> **Status:** Production Ready  
> **This document is a thin wrapper.**  
> Canonical governance lives in: `knowledge_base_smartspec_handbook.md`.

---

## 0) What to read first

Read the Canonical Handbook for:

- governance rules, write model, and security
- universal flag contract
- privileged operation policy (no-shell, allowlist, allow-network gate)
- Change Plan requirement
- SPEC_INDEX reuse/de-dup policy
- reference/research requirements
- UI/UX minimum standard
- workflow registry rules

This wrapper focuses on installation, standard execution sequence, and short quickstart commands.

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
- Some governed writes additionally require an explicit opt-in (examples: `--write-docs`, `--write-runtime-config`, `--write-ci-workflow`).

---

## 4) Quickstart (positional-first + dual command examples)

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
  --apply \
  --kilocode
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
  --apply \
  --kilocode
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
  --apply \
  --kilocode
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
  --json \
  --kilocode
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
  --json \
  --kilocode
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
  --apply \
  --kilocode
```

---

## 5) Common patterns for newer workflows (v6.1.x)

This section does not list every workflow (see `.spec/WORKFLOWS_INDEX.yaml`). It documents **common contracts** used by newer workflows.

### 5.1 Platform flag collision avoidance

- `--platform` is universal and reserved for `cli|kilo|ci|other`.
- Workflow-specific platforms must use namespaced flags:
  - `--obs-platform` (observability)
  - `--publish-platform` (docs publishing)

### 5.2 Network gating for publish/tag flows

- Any workflow that fetches/pushes/publishes typically requires `--allow-network`.
- If your environment cannot enforce deny-by-default, expect a warning in reports.

### 5.3 Runtime tree writes require an extra opt-in gate

- Writing into `docs/` or other runtime trees requires BOTH:
  - `--apply`
  - an explicit opt-in such as `--write-docs` / `--write-runtime-config`

### 5.4 Docs generation → publishing (example chain)

Generate docs (preview bundle) and then publish from that bundle.

#### CLI

```bash
/smartspec_docs_generator \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json

/smartspec_docs_publisher \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json
```

#### Kilo Code

```bash
/smartspec_docs_generator.md \
  --mode user-guide \
  --spec specs/<category>/<spec-id>/spec.md \
  --out .spec/reports/docs-generator \
  --json \
  --kilocode

/smartspec_docs_publisher.md \
  --docs-dir .spec/reports/docs-generator/<run-id>/bundle.preview \
  --publish-platform github-pages \
  --version v1.2.3 \
  --remote origin \
  --github-branch gh-pages \
  --allow-network \
  --apply \
  --out .spec/reports/docs-publisher \
  --json \
  --kilocode
```

---

## 6) Universal flags (quick reference)

All workflows share:

- `--config`, `--lang`, `--platform`, `--apply`, `--out`, `--json`, `--quiet`

See the Canonical Handbook for definitions.

---

# End of Thin Wrapper

