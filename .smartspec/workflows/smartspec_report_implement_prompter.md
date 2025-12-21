---
description: Generate implementation prompt packs with 100% duplication prevention.
version: 7.0.0
workflow: /smartspec_report_implement_prompter
---

# smartspec_report_implement_prompter

> **Canonical path:** `.smartspec/workflows/smartspec_report_implement_prompter.md`  
> **Version:** 7.0.0  
> **Status:** Production Ready  
> **Category:** prompter

## Purpose

Generate **implementation prompt packs** from a spec and tasks, with **100% duplication prevention** and **reuse-first** governance.

This workflow replaces legacy prompt generators and ensures that all generated prompts are aware of existing components, preventing the creation of duplicates.

It produces **prompts only** (safe outputs) and never modifies governed artifacts or runtime source trees.

---

## Governance contract

This workflow MUST follow:

- `knowledge_base_smartspec_handbook.md` (v6)
- `.spec/smartspec.config.yaml`

### Write scopes (enforced)

Allowed writes (safe outputs only):

- Prompts: `.smartspec/prompts/**`

Forbidden writes (must hard-fail):

- Any path outside allowlist from config
- Any governed artifact (e.g., `specs/**`, `.spec/SPEC_INDEX.json`, `.spec/WORKFLOWS_INDEX.yaml`)
- Reports output (this workflow does not write to `.spec/reports/**`)
- Any runtime source tree modifications

### `--apply` behavior (universal flag)

- Accepted for compatibility with the universal flag contract.
- Must have **no effect** on write scopes.
- If provided, the workflow MUST note in the prompt pack header and JSON summary that `--apply` was ignored.

---

## Flags

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

Flags specific to `/smartspec_report_implement_prompter`:

| Flag | Required | Description |
|---|---|---|
| `--spec` | Yes | Path to the spec.md file (e.g., `specs/feature/spec-001/spec.md`) |
| `--tasks` | Yes | Path to the tasks.md file (e.g., `specs/feature/spec-001/tasks.md`) |
| `--apply` | No | Accepted for compatibility but has no effect (prompts are safe outputs) |
| `--skip-duplication-check` | No | Skip pre-generation duplication validation (not recommended) |
| `--registry-roots` | No | Additional registry directories to check for duplicates (comma-separated) |
| `--prompt-style` | No | Style of generated prompts (detailed|concise|structured, default: detailed) |

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file
- **Duplication prevention:** Never use `--skip-duplication-check` unless explicitly instructed
- **Safe outputs:** This workflow only writes to `.smartspec/prompts/**`, no `--apply` gate needed

---

## Behavior

### 1) Pre-Generation Validation (MANDATORY)

Before generating prompts, the AI agent **MUST** check for existing similar components.

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
    a) Reuse existing components
    b) Justify creating new components
    c) Cancel and review existing specs
  - **MUST NOT** proceed until the user confirms.

### 2) Generate prompt pack

- Generate implementation prompt packs from a spec and tasks, optionally augmented by strict verification reports.

### 3) Post-Generation Validation (MANDATORY)

After generating the prompt pack, the AI agent **MUST** validate the generated prompts.

**Validation Command:**
```bash
python3 .spec/scripts/validate_prompts.py \
  --prompts .smartspec/prompts/<spec-id>/<target>/<run-id>/ \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** The prompt pack is valid.
- **Exit Code `1` (Failure):** The prompt pack is invalid. The agent **MUST NOT** use the generated prompts.
- The full output from the validation script **MUST** be included in the `README.md` of the prompt pack.

---

## Output structure

### Output root selection

To prevent accidental overwrites, outputs are always written under a run folder.

- If `--out` is provided, treat it as a **base output root** and write under:
  - `<out>/<target>/<run-id>/README.md`
  - `<out>/<target>/<run-id>/prompts/*.md`
  - `<out>/<target>/<run-id>/meta/summary.json` (if `--json`)

- If `--out` is not provided, default to:
  - `.smartspec/prompts/<spec-id>/<target>/<run-id>/...`

---

# End of workflow doc
