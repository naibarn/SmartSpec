# Knowledge Base — SmartSpec Installation & Usage (Updated for Dual CLI + Kilo Code Commands)
> **Version:** 2.3.0  
> **Status:** Stable  
> **Scope of Update:**  
> - Add **dual command examples** (CLI + Kilo Code) for all workflows.  
> - Enforce rule: **When `--kilocode` is used → workflow names MUST use `.md`.**  
> - Improve clarity of strict verification workflow usage.

---

# 1. Installation Overview
SmartSpec tools are distributed as a workflow suite installable into:
- CLI environments  
- Kilo Code  
- Claude Code / Antigravity  
- Custom CI

Installation provides:
- Workflow executables  
- Kilo Code-compatible orchestrator (`.md` workflows)

---

# 2. Core Components Installed
This installation delivers:

```
/smartspec_generate_spec
/smartspec_generate_plan
/smartspec_generate_tasks
/smartspec_verify_tasks_progress
/smartspec_verify_tasks_progress_strict
/smartspec_sync_tasks_checkboxes
/smartspec_report_implement_prompter
/smartspec_project_copilot
```

And their orchestrated Kilo Code `.md` versions:
```
/smartspec_generate_spec.md
/smartspec_generate_plan.md
/smartspec_generate_tasks.md
/smartspec_verify_tasks_progress.md
/smartspec_verify_tasks_progress_strict.md
/smartspec_sync_tasks_checkboxes.md
/smartspec_report_implement_prompter.md
/smartspec_project_copilot.md
```

---

# 3. IMPORTANT RULE: Dual Example Pattern
Every example in this KB **must include both**:

### **CLI Form** (no `.md`, no `--kilocode`)
### **Kilo Code Form** (`.md` + `--kilocode`)

This guarantees users cannot mistakenly copy a command that fails in Kilo Code.

---

# 4. Running Strict Verification (Canonical Step)
Strict verification is always required before advanced workflows such as implement-prompter.

---

## 4.1 CLI Example
```bash
/smartspec_verify_tasks_progress_strict \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report-format=both \
  --report user-management-progress-report-strict.json
```

## 4.2 Kilo Code Example
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-002-user-management/tasks.md \
  --kilocode \
  --report-format=both \
  --report user-management-progress-report-strict.json
```

---

# 5. Generating Implementation Prompts (smartspec_report_implement_prompter)
This workflow analyzes:
- `spec.md`  
- `tasks.md`  
- strict verification report

Then generates:
- API prompts
- Test prompts
- Documentation prompts
- Deployment prompts

---

## 5.1 CLI Example
```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report user-management-progress-report-strict.json \
  --output .smartspec/prompts/spec-002-user-management
```

## 5.2 Kilo Code Example  (MUST use .md + --kilocode)
```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/spec-002-user-management/spec.md \
  --tasks specs/feature/spec-002-user-management/tasks.md \
  --report user-management-progress-report-strict.json \
  --output .smartspec/prompts/spec-002-user-management \
  --kilocode
```

> When invoked with `--kilocode`, the prompter MUST also render `.md` forms of commands **inside generated prompts**.

Example inside generated prompt:
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/spec-002-user-management/tasks.md \
  --kilocode --report-format=both
```

---

# 6. Sync Task Checkboxes
After running strict verification, use this workflow to sync checkbox states in tasks.md.

## 6.1 CLI Example
```bash
/smartspec_sync_tasks_checkboxes \
  --tasks specs/feature/spec-002-user-management/tasks.md
```

## 6.2 Kilo Code Example
```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/feature/spec-002-user-management/tasks.md \
  --kilocode
```

---

# 7. Project Copilot
High-level guidance workflow.

## 7.1 CLI Example
```bash
/smartspec_project_copilot \
  --spec specs/feature/spec-900/system/spec.md
```

## 7.2 Kilo Code Example
```bash
/smartspec_project_copilot.md \
  --spec specs/feature/spec-900/system/spec.md \
  --kilocode
```

---

# 8. Workflow Execution Sequence
Standard SmartSpec sequence:
```
/spec → /plan → /tasks → /strict-verify → /implement-prompter → code changes → /strict-verify → /sync-checkboxes
```

Kilo Code examples must always use `.md` + `--kilocode`.

---

# 9. Language Handling
Locale =  
1. `--language th|en`
2. SPEC header
3. auto-detect
4. platform default (Kilo Code = TH)

Prompts must follow locale rules.

---

# 10. Multi-Repo Support
Most workflows accept:
```
--workspace-roots <paths>
--repos-config <path>
```
Examples must be duplicated into CLI + Kilo Code formats:

## CLI
```bash
/smartspec_verify_tasks_progress_strict \
  --tasks specs/feature/a/tasks.md \
  --repos-config repos.json \
  --workspace-roots repo1,repo2
```

## Kilo Code
```bash
/smartspec_verify_tasks_progress_strict.md \
  specs/feature/a/tasks.md \
  --kilocode \
  --repos-config repos.json \
  --workspace-roots repo1,repo2
```

---

# 11. Evidence Governance Summary
Strict verifier evaluates:
- Source files
- Routes & controllers
- Services
- Tests
- Docs
- Deployment

Prompter classifies tasks:
- unsynced
- simple
- complex → api/tests/docs/deploy clusters

---

# 12. Mandatory Documentation Rule
From now on, every workflow example must be shown as **two variants**:
```
CLI
Kilo Code (.md + --kilocode)
```
This resolves confusion where users copy CLI commands into Kilo Code and receive `not found` errors.

---

# 13. Backward Compatibility
All CLI examples still work.  
Kilo Code examples simply clarify orchestration and do not break older behavior.

---

# End of SmartSpec Installation and Usage KB (Updated v2.3.0)
