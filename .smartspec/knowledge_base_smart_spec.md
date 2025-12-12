# Knowledge Base — SmartSpec Governance (Updated With Kilo Code Dual-Command Rules)

> **Version:** 2.3.0  
> **Status:** Stable  
> **Scope of Update:**  
> - Add *dual-command guidance* (CLI + Kilo Code) for every SmartSpec workflow example.  
> - Enforce rule: **When `--kilocode` is present → workflows MUST use `.md` suffix.**

---

# 1. Purpose of SmartSpec
SmartSpec provides a structured, auditable, multi-phase system for:

- Specification design (SPEC)
- Task planning (PLAN → TASKS)
- Implementation (IMPLEMENT)
- Evidence-driven verification (VERIFY)
- Prompted refinement (PROMPTER)

SmartSpec ensures each artifact is:
- Deterministic
- Traceable
- Evidence-first
- AI-tooling-compatible (Kilo Code, Antigravity, Claude Code, etc.)

---

# 2. SmartSpec File System Governance
SmartSpec files must follow the structure:
```
specs/
  feature/
    <spec-id>/
      spec.md
      tasks.md
      design/
      testplan/
.spec/
  reports/
    verify-tasks-progress/
```  

Write guards apply:
- **NO-WRITE** to spec.md, tasks.md, design files, registries unless workflows explicitly allow modification.
- Prompt-only workflows (like implement-prompter) may write only under:
```
.smartspec/prompts/<spec-id>/
```

---

# 3. Core Workflows Index
SmartSpec workflows include:

| Workflow | Purpose |
|----------|---------|
| `/smartspec_generate_spec` | Create SPEC from user intent |
| `/smartspec_generate_plan` | Convert SPEC → PLAN |
| `/smartspec_generate_tasks` | Convert PLAN → TASKS |
| `/smartspec_verify_tasks_progress` | Evidence-based verification |
| `/smartspec_verify_tasks_progress_strict` | **Strict** verification (canonical) |
| `/smartspec_report_implement_prompter` | Generate implementation prompts |
| `/smartspec_sync_tasks_checkboxes` | Sync TASKS checkboxes based on evidence |
| `/smartspec_project_copilot` | High-level guidance engine |

Every workflow must now include **two command variants**:  
1) **CLI Standard**  
2) **Kilo Code (`.md` + `--kilocode`)**

---

# 4. Dual-Command Rule (NEW — Required Everywhere)
SmartSpec now enforces the following:

## 4.1 CLI Standard Mode
- Workflow commands are used **as-is** (no `.md`).
- No `--kilocode` flag.

Example:
```bash
/smartspec_verify_tasks_progress_strict --tasks specs/feature/abc/tasks.md
```

## 4.2 Kilo Code Mode
If the user runs **ANY** workflow with `--kilocode`:
- The workflow name **must end with `.md`**
- The command arguments rendered by the workflow **must also use the `.md` variant**
- The workflow must propagate `--kilocode`

Example:
```bash
/smartspec_verify_tasks_progress_strict.md specs/feature/abc/tasks.md --kilocode
```

This rule applies to:
- strict verifier
- sync checkboxes
- implement-prompter
- any re-run suggestions printed inside prompts or workflow output

> **This prevents users from copying CLI commands that fail inside Kilo Code.**

---

# 5. Detailed Workflow Descriptions (With Dual-Command Examples)

---

# 5.1 `/smartspec_verify_tasks_progress_strict`
**Purpose:** Perform strict, evidence-only verification of all tasks.

### CLI Example
```bash
/smartspec_verify_tasks_progress_strict \
  --tasks specs/feature/spec-001-user/tasks.md \
  --report-format=both \
  --report .spec/reports/verify-tasks-progress/spec-001.json
```

### Kilo Code Example
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-001-user/tasks.md \
  --kilocode \
  --report-format=both \
  --report .spec/reports/verify-tasks-progress/spec-001.json
```

---

# 5.2 `/smartspec_sync_tasks_checkboxes`
**Purpose:** After strict verification, sync checkbox states in tasks.md.

### CLI Example
```bash
/smartspec_sync_tasks_checkboxes --tasks specs/feature/spec-001-user/tasks.md
```

### Kilo Code Example
```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/feature/spec-001-user/tasks.md \
  --kilocode
```

---

# 5.3 `/smartspec_report_implement_prompter` (Updated — Must Output Dual Commands)
**Purpose:** Generate implementation prompts based on strict verification.

### CLI Example
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report user-management-progress-report-strict.json \
  --output .smartspec/prompts/spec-002-user-management
```

### Kilo Code Example
```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report user-management-progress-report-strict.json \
  --output .smartspec/prompts/spec-002-user-management \
  --kilocode
```

### REQUIRED (NEW):  
When invoked with `--kilocode`, all commands embedded in generated prompts must also use:
- workflow name ending in `.md`
- `--kilocode`

Example inside generated prompt:
```bash
/smartspec_verify_tasks_progress_strict.md specs/feature/spec-002-user-management/tasks.md --kilocode --report-format=both
```

---

# 6. Project Copilot Workflow

### CLI Example
```bash
/smartspec_project_copilot --spec specs/feature/spec-900/system/spec.md
```

### Kilo Code Example
```bash
/smartspec_project_copilot.md \
  --spec specs/feature/spec-900/system/spec.md \
  --kilocode
```

---

# 7. Language / Locale Resolution
Language selection follows:
1. Explicit `--language <th|en>`
2. `language:` in SPEC header
3. Body ratio auto-detect
4. Platform default (Kilo Code = Thai)

---

# 8. Write Guards
Workflows may *read* but never *modify*:
- spec.md
- tasks.md
- design/
- ui/
- schema/
- registries

Except for:
- `/smartspec_sync_tasks_checkboxes` which may modify checkboxes only

---

# 9. Evidence Governance Summary
Strict verifier expects evidence from:
- Routes
- Controllers
- Services
- Tests
- Deploy manifests / CI scripts
- Documentation

Prompter must classify tasks:
- unsynced
- simple
- complex (clustered: api/tests/docs/deploy)

---

# 10. Mandatory Rule for Documentation & Examples
Every SmartSpec example **MUST** follow this pattern:

```
# CLI Example
<command>

# Kilo Code Example
<command.md ... --kilocode>
```

Users consistently make mistakes when copying examples from the docs.  
This rule ensures both environments are always represented.

---

# 11. Backward Compatibility
Existing CLI usage is preserved.  
No change to semantics — only **documentation correctness + command rendering rules** updated.

---

# End of SmartSpec Governance KB (Updated v2.3.0)

