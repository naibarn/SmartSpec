title: SmartSpec Install & Usage Knowledge Base
version: 5.6
role: Shared KB for installation, platform usage, and core workflow commands
scope: Complements `knowledge_base_smart_spec.md` (governance) and is used
       together with `system_prompt_smartspec_v5.6`.
---

# 1. Purpose & Scope

This knowledge base collects **practical installation and usage rules** for
SmartSpec v5.6, so answers about:

- how to install/update SmartSpec,
- how to run workflows on different platforms (Kilo Code, Claude Code,
  Google Antigravity, Gemini CLI, Roo, Cursor/VSCode),
- how core commands like `/smartspec_generate_tasks`,
  `/smartspec_implement_tasks`, and `/smartspec_verify_tasks_progress` work,

are consistent with the repository (`README.md`), the installer manual, and
workflow manuals.

It is **not** a replacement for `knowledge_base_smart_spec.md` (governance).
When the two overlap, the governance KB is authoritative for policies such as:

- canonical folders (`.spec/`, `.smartspec/`, `.spec/registry`, `.spec/reports`),
- `--kilocode` and write-guard rules,
- security and dependency guardrails,
- manual header format and EN/TH manual split.

---

# 2. High-Level Overview (What SmartSpec Is)

SmartSpec is a **structured, production-grade framework** for AI-assisted
software development. It turns initial ideas into production-ready code through
an orchestrated chain:

> **SPEC → PLAN → TASKS → PROMPT → IMPLEMENT (+ TESTS, QUALITY, RELEASE)**

Core characteristics:

- Integrates with multiple AI coding platforms: Kilo Code, Claude Code,
  Google Antigravity, Gemini CLI, Cursor/VSCode, Roo, etc.
- Uses **workflow files** (`/smartspec_*`) under `.smartspec/workflows/` as the
  master source of truth.
- Uses **manuals** in `.smartspec-docs/workflows/` to explain each command.
- Provides project-level orchestration via `/smartspec_project_copilot`.

---

# 3. Supported Platforms & Conceptual Usage

SmartSpec workflows are designed to be **tool-agnostic**. The same workflow
spec lives under `.smartspec/workflows/` and is then copied/linked into
platform-specific locations by the installer.

Typical platform targets:

- **Kilo Code**: `.kilocode/workflows/`
- **Claude Code**: `.claude/commands/`
- **Google Antigravity**: `.agent/workflows/`
- **Gemini CLI**: `.gemini/commands/` (with auto-conversion to TOML where
  required)
- **Roo Code**: `.roo/commands/`
- **Cursor / VSCode**: used as a reference for prompts and context
  (especially via `/smartspec_generate_cursor_prompt`).

The **canonical workflow name** is `/smartspec_<name>`. The underlying
Markdown workflow file is `smartspec_<name>.md` in `.smartspec/workflows/` and
in platform-specific workflow folders.


## 3.1 Command naming & `.md` rules

To keep manuals and examples consistent, use this convention:

- **Non-Kilo / generic CLI examples**
  - Use the canonical command name **without** `.md`:

    ```bash
    /smartspec_generate_tasks ...
    /smartspec_implement_tasks ...
    ```

- **Kilo Code examples**
  - Use the workflow filename form **with** `.md` and `--kilocode`:

    ```bash
    /smartspec_generate_tasks.md --kilocode ...
    /smartspec_implement_tasks.md --kilocode ...
    ```

In manuals:

- Always prefix commands with `/`.
- Include a short note in Quick Start sections explaining:
  - "Use `.md` form with `--kilocode` when running in Kilo Code."
  - "Use the non-`.md` form for other tools/CLIs."

This KB assumes the manuals follow those conventions.

---

# 4. Installation & Update (Project-Local)

SmartSpec is installed **per project**. There are two common patterns:

1. **Remote one-liner install (recommended for quick start)**.
2. **Local installer scripts (`install.sh` / `install.ps1`) for controlled,
   internal distribution**.

## 4.1 Quick start install (Unix/macOS/Linux)

From your project root:

```bash
curl -fsSL https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.sh | bash
```

This will:
- download and run the latest installer script from GitHub;
- fetch the SmartSpec distribution repo;
- create/update `.smartspec/` and `.smartspec-docs/` in your project;
- sync workflows into platform-specific folders.

## 4.2 Quick start install (Windows, PowerShell)

From your project root in PowerShell:

```powershell
irm https://raw.githubusercontent.com/naibarn/SmartSpec/main/.smartspec/scripts/install.ps1 | iex
```

The script performs the same actions as the Unix installer, adapted for
Windows tools.


## 4.3 Using local installer scripts (enterprise / forked repos)

Platform/architecture teams may prefer to vendor the installer scripts inside
internal repos. In that case:

- Place `install.sh` (Linux/macOS) or `install.ps1` (Windows) in the project
  root.
- Optionally set environment variables to point to your distribution repo
  (see 4.4).
- Run `./install.sh` or `./install.ps1` from the project root.

The local scripts perform the same high-level work as the GitHub one-liners:

1. Download the SmartSpec distribution repo.
2. Copy `.smartspec/` and `.smartspec-docs/` into the project.
3. Ensure core files exist:
   - `.smartspec/system_prompt_smartspec.md`
   - `.smartspec/knowledge_base_smart_spec.md`
   - `.smartspec/knowledge_base_smartspec_install_and_usage.md`
4. Sync workflows from `.smartspec/workflows/` into platform-specific
   folders.


## 4.4 Configurable distribution repo

By default, installers pull from a specific distribution repo/branch
(typically the public GitHub repo). Enterprise environments can override this
via environment variables before running the installer.

- **Unix/macOS (`install.sh`)**:

  - `SMARTSPEC_REPO_URL` (default: upstream SmartSpec repo URL)
  - `SMARTSPEC_REPO_BRANCH` (default: `main`)

- **Windows (`install.ps1`)**:

  - `$env:SMARTSPEC_REPO_URL`
  - `$env:SMARTSPEC_REPO_BRANCH`

Example (Unix/macOS):

```bash
export SMARTSPEC_REPO_URL="https://git.company.local/platform/SmartSpec.git"
export SMARTSPEC_REPO_BRANCH="release-5.6"
./install.sh
```

Example (Windows, PowerShell):

```powershell
$env:SMARTSPEC_REPO_URL    = 'https://git.company.local/platform/SmartSpec.git'
$env:SMARTSPEC_REPO_BRANCH = 'release-5.6'
./install.ps1
```


## 4.5 Directory layout after installation

A typical project after installation looks like:

```text
.
├─ .smartspec/
│  ├─ system_prompt_smartspec.md
│  ├─ knowledge_base_smart_spec.md
│  ├─ knowledge_base_smartspec_install_and_usage.md
│  └─ workflows/
│     ├─ smartspec_project_copilot.md
│     ├─ smartspec_generate_spec.md
│     ├─ smartspec_generate_plan.md
│     ├─ smartspec_generate_tasks.md
│     ├─ smartspec_implement_tasks.md
│     ├─ smartspec_generate_tests.md
│     ├─ smartspec_verify_tasks_progress.md
│     └─ ... (other workflows)
├─ .smartspec-docs/
│  └─ workflows/
│     ├─ smartspec_project_copilot/
│     │  ├─ manual_en.md
│     │  ├─ manual_th.md
│     │  └─ ...
│     ├─ smartspec_generate_spec/
│     └─ ... (other manuals)
├─ .kilocode/workflows/
├─ .roo/commands/
├─ .claude/commands/
├─ .agent/workflows/
└─ .gemini/commands/
```

Notes:

- `.smartspec/` is the **master source of truth** for workflows and global
  prompts/KBs.
- `.smartspec-docs/` contains manuals and guides; workflows should never try
  to write into it.
- `.spec/` (indexes, registries, reports) is **project-owned** and not created
  by the installer.


## 4.6 Updating SmartSpec

To update SmartSpec in an existing project:

1. Platform team updates the distribution repo (`.smartspec`,
   `.smartspec-docs`, workflows, KBs).
2. Each project reruns the installer (one-liner or local script).
3. Installer may backup existing `.smartspec/` and `.smartspec-docs/` before
   replacing them.

**Important:** Avoid editing core workflows under `.smartspec/workflows/`
inside a project. Instead, introduce project-specific overlays or separate
workflows to avoid conflicts during updates.

---

# 5. Entry Point & Typical Development Flow

After installation, the recommended entry point is:

## 5.1 `/smartspec_project_copilot`

`/smartspec_project_copilot` is a **project-level navigator**. It helps you:

- understand the current project state (specs, plans, tasks, registries);
- choose which workflow(s) to run next (generate_spec, generate_plan,
  generate_tasks, implement_tasks, generate_tests, ci_quality_gate,
  release_readiness, etc.);
- onboard new contributors by explaining how the project is wired.

Use it when you are unsure which command to run next, or when entering a new
project for the first time.


## 5.2 Core SPEC → PLAN → TASKS → IMPLEMENT loop

A typical end-to-end flow for a new feature might look like:

```bash
# 1) Generate or update the spec
/smartspec_generate_spec --spec-ids=my_feature_service

# 2) Generate or update the plan
/smartspec_generate_plan --spec-ids=my_feature_service

# 3) Generate tasks from the spec
/smartspec_generate_tasks specs/feature/spec-005-promo-system/spec.md

# 4) Implement tasks (phased)
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md --phase 1

# 5) Verify progress (read-only)
/smartspec_verify_tasks_progress specs/feature/spec-005-promo-system/tasks.md

# 6) Generate/extend tests
/smartspec_generate_tests --spec-ids=my_feature_service

# 7) Run quality gate & release readiness workflows
/smartspec_ci_quality_gate --spec-ids=my_feature_service
/smartspec_release_readiness --spec-ids=my_feature_service
```

- In **Kilo Code** examples, these would typically appear as
  `/smartspec_generate_spec.md`, `/smartspec_implement_tasks.md`, etc., with
  `--kilocode` enabled.
- For other tools, the non-`.md` forms above are preferred.

---

# 6. Core Workflow Semantics (Tasks & Implementation)

This section consolidates behaviour for three core workflows so answers are
consistent across manuals and tools.

## 6.1 `/smartspec_generate_tasks`

**Purpose**

Generate a developer-ready `tasks.md` from a `spec.md`, using project artefacts
(spec, schemas, OpenAPI, data models) as the source of truth.

**Canonical usage (non-Kilo)**

```bash
/smartspec_generate_tasks <spec_path> [options]
```

**Kilo usage**

```bash
/smartspec_generate_tasks.md <spec_path> --kilocode [options]
```

**Key options**

- `spec_path` (positional, required): path to the source `spec.md`.
- `--specindex <path>`: custom SPEC index path (override auto-detection).
- `--nogenerate`: dry-run; analyze but do not write files.

**SPEC index detection**

If `--specindex` is not provided, the workflow should auto-detect
`SPEC_INDEX.json` using the canonical order:

1. `.spec/SPEC_INDEX.json` (canonical)
2. `SPEC_INDEX.json` at repo root (legacy mirror)
3. `.smartspec/SPEC_INDEX.json` (deprecated)
4. `specs/SPEC_INDEX.json` (legacy layouts)

If no index is found:

- Emit a clear warning.
- Allow continuing without an index (local-only behaviour) if the user
  chooses.
- Optionally suggest where to create one (`.spec/SPEC_INDEX.json`).

**Source-of-truth priority**

When generating tasks, prefer concrete artefacts over prose when available:

1. Prisma schema(s) and similar typed schemas.
2. Existing OpenAPI specs.
3. Approved data model docs.
4. Spec text itself.

**Output**

- `tasks.md` in the same folder as the `spec.md`.
- Optional supporting files (OpenAPI/data models) when triggered by spec
  content and allowed by governance rules.


## 6.2 `/smartspec_implement_tasks`

**Purpose**

Implement tasks from `tasks.md` safely and incrementally, tracking progress and
producing a per-run summary.

**Canonical usage (non-Kilo)**

```bash
/smartspec_implement_tasks <tasks_path | spec_folder | implement-prompt.md> [options]
```

**Kilo usage**

```bash
/smartspec_implement_tasks.md <tasks_path | spec_folder | implement-prompt.md> --kilocode [options]
```

**Accepted path formats**

```bash
# Direct tasks file
/smartspec_implement_tasks specs/feature/spec-005-promo-system/tasks.md

# Directory (auto-resolve tasks.md inside)
/smartspec_implement_tasks specs/feature/spec-005-promo-system

# Implement prompt file
/smartspec_implement_tasks specs/feature/spec-005-promo-system/implement-prompt-spec-005.md
```

**Mode & safety options**

- `--skip-completed` (default): skip tasks already `[x]`.
- `--force-all`: re-implement all tasks regardless of checkbox state.
- `--validate-only`: run validations without writing code.

**Scope options**

- `--phase <n | n,m | n-m>`: select phases.
- `--tasks <T001 | T001,T002 | T001-T010>`: select tasks.
- `--start-from <Txxx>`: start from a specific task and continue to end.
- `--resume`: resume from last checkpoint.

**Execution options**

- `--architect`: force an architecture step before edits.
- `--kilocode`: may enable Orchestrator Mode (see below).

**Orchestrator safety rule**

- Orchestrator Mode is allowed **only when `--kilocode` is set**.
- Without `--kilocode`, the workflow must not silently switch to
  Orchestrator or mention it as an automatic fallback.

**Spec & evidence resolution**

For integration-sensitive tasks:

1. Read referenced spec files and supporting docs.
2. Resolve spec IDs via the SPEC index detection order (Section 6.1).
3. Inspect the codebase for concrete evidence before making assumptions.

If evidence is missing:

- Ask the user (or mark as unclear), rather than auto-selecting defaults.

**Validation & checkbox rules**

- After each task, run validation commands defined in `tasks.md` (if any); or
  use sensible defaults for the stack.
- Mark a task `[x]` only when implementation and validations for that task
  pass.

**Required per-run summary**

At the end of a run, output a summary including:

- tasks in scope;
- completed / failed / skipped counts;
- files created/edited;
- validation outcomes;
- suggested next commands (e.g., rerun with `--start-from`, run
  `/smartspec_verify_tasks_progress`, etc.).


## 6.3 `/smartspec_verify_tasks_progress`

**Purpose**

Read-only (or optional checkbox-updating) verification of implementation
progress relative to `tasks.md`. It should **never fix code**.

**Canonical usage (non-Kilo)**

```bash
/smartspec_verify_tasks_progress <tasks_path> [options]
```

**Kilo usage**

```bash
/smartspec_verify_tasks_progress.md <tasks_path> --kilocode [options]
```

**Scope options**

- `--tasks <range>` / `--task <range>` (alias).
- `--start-from <Txxx>`.
- `--phase <name_or_id>`.

**Update behaviour**

- Default: verification-only (no checkbox updates).
- If supported, an explicit `--update` flag may update `[ ]` → `[x]` when
  completion is verified.
- If `--no-update` exists, treat it as a hard guardrail (read-only).

**Safety rules**

- Must **not** invoke Orchestrator Mode.
- If `--kilocode` is present, it may be treated as a no-op or used only to
  adapt output formatting, but must not change write behaviour.

**Completion criteria**

A task can be considered complete when:

- expected files exist and have relevant changes;
- acceptance criteria and validations (tests, linters, etc.) pass;
- in strict modes, all configured validations pass.

**Output**

- A progress report (e.g., markdown/JSON) near `tasks.md`.
- Optionally, a backup of `tasks.md` if checkbox updates occur.

---

# 7. Other Important Workflows (Brief Overview)

For quick reference (full details in `.smartspec-docs/workflows/`):

- `/smartspec_generate_spec_from_prompt` – generate `spec.md` from user prompt/user requirements.
- `/smartspec_generate_spec` – generate/update `spec.md` from ideas/requirements.
- `/smartspec_generate_plan` – create/refresh `plan.md` from specs.
- `/smartspec_generate_implement_prompt` – agent-focused implementation prompts
  for Kilo/Roo/Claude.
- `/smartspec_generate_cursor_prompt` – human-guided prompts for Cursor and
  similar tools.
- `/smartspec_generate_tests` – create/extend test suites from specs.
- `/smartspec_fix_errors` – focused error/bug fixing guided by specs.
- `/smartspec_refactor_code` – refactoring aligned with specs and patterns.
- `/smartspec_ci_quality_gate` – CI quality governance per spec/service.
- `/smartspec_release_readiness` – final readiness checks combining other
  signals (UI, security, NFR, CI).
- `/smartspec_ui_validation` – UI validation governance.
- `/smartspec_ui_consistency_audit` – UI style & design-system consistency.
- `/smartspec_security_evidence_audit` – security evidence collection.
- `/smartspec_nfr_perf_planner` / `/smartspec_nfr_perf_verifier` –
  performance/NFR planning & verification.
- `/smartspec_validate_index` / `/smartspec_reindex_specs` – index validation
  and rebuilding.
- `/smartspec_sync_spec_tasks` – sync specs and tasks.
- `/smartspec_reverse_to_spec` – reverse-engineer specs from existing code.

---

# 8. Troubleshooting & FAQ (Install & Usage)

**Q1. The installer ran but `.smartspec/` is missing.**

- Check installer output for errors.
- Verify the distribution repo actually contains `.smartspec/`.
- Ensure you have write permissions to the project directory.

**Q2. Workflows appear in Kilo but not in other tools.**

- Confirm installer synced `.smartspec/workflows/` into `.roo/commands`,
  `.claude/commands`, `.agent/workflows`, `.gemini/commands`, etc.
- Some tools may require a refresh/reload to detect new workflows.

**Q3. Which command should I run first in a new project?**

- Use `/smartspec_project_copilot` for project-level guidance.
- It will typically recommend a SPEC/PLAN/TASKS sequence appropriate for the
  current project state.

**Q4. Should I edit workflows under `.smartspec/workflows/`?**

- Prefer editing workflows only in the distribution repo.
- For project-specific behaviour, use separate overlay workflows or
  parameters; avoid forking core workflows per project.

**Q5. Why are some examples using `.md` and others not?**

- `.md` forms correspond to Kilo Code workflow filenames (e.g.
  `/smartspec_generate_tasks.md`).
- Non-`.md` forms are canonical command names used in generic CLI examples or
  other tools.
- Manuals should clearly state which environment each example targets.

---

This install & usage KB is intended to be read **together with**
`knowledge_base_smart_spec.md` and used by system prompts like
`system_prompt_smartspec v5.6 – SPEC-first miniapp aware` so that installation
steps, directory layout, command syntax, and core workflow behaviour are
answered consistently for users across all supported platforms.
