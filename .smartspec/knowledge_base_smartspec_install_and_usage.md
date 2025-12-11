# SmartSpec Install & Usage Knowledge Base – v5.7.1 (Rewritten Full Edition)

This is the **complete and modernized SmartSpec Install & Usage Knowledge Base**.  
It fully supports:
- SmartSpec v5.6–v5.7 governance
- KiloCode / Claude Code / Antigravity integration
- The new `/smartspec_fix_errors` capability with `--report=<path>`
- Auto-discovery of implementation reports
- Multi-repo, multi-registry, SPEC_INDEX resolution
- SPEC → PLAN → TASKS → IMPLEMENT → TESTS → QUALITY → RELEASE chain

This file replaces older versions completely while keeping all rules intact.

---

# 1. What SmartSpec Is
SmartSpec is a **specification-driven development system** designed for AI-assisted engineering across multiple environments (local, VSCode/KiloCode, cloud editors, CI pipelines).

SmartSpec enforces:
- clear specification documents (`spec.md`)
- deterministic planning (`generate_plan`)
- deterministic tasks (`generate_tasks`)
- deterministic, reproducible implementation (`implement_tasks`)
- safe error correction (`fix_errors`)
- structured quality gates (`generate_tests`, `ci_quality_gate`)

All workflows must follow the SmartSpec chain:
```
SPEC → PLAN → TASKS → IMPLEMENT → TESTS → QUALITY → RELEASE
```

---

# 2. Installation Overview
SmartSpec can run in three environments:
1. **Local machine**  
2. **KiloCode / Claude Code**  
3. **Cloud-based orchestration (Antigravity)**

Most common usage involves KiloCode, where the LLM has access to project files and runs workflows on your behalf.

SmartSpec workflows live under:
```
.smartspec/workflows/smartspec_<name>.md
```

Manuals live separately (typically under `.smartspec-docs/`).

---

# 3. Calling SmartSpec Workflows
Every workflow follows the convention:
```
/smartspec_<name>.md [flags]
```

Examples:
```
/smartspec_generate_spec_from_prompt "build a billing dashboard"
/smartspec_generate_tasks specs/billing/billing_core/spec.md
/smartspec_implement_tasks specs/billing/billing_core/tasks.md --kilocode
```

## 3.1 Flags
All workflows support:
- `--kilocode` → run with Kilo Orchestrator

Other flags vary per workflow, e.g.:
- `--plan` `--tasks` `--index` `--registry-dir` `--registry-roots`
- `--mode` (`recommend`, `additive-meta`)
- `--safety-mode` (`strict`, `dev`)

Every workflow must document its own flags in its `.md` file.

---

# 4. KiloCode Usage Guide
`--kilocode` activates orchestrator mode:
- SmartSpec splits work into subtasks
- Errors and logs are streamed back to the LLM
- Workflows operate on the same file system as the user

### 4.1 Important Kilo rule
**When you start a new Task in Kilo, runtime context is cleared.**  
This means:
- Previous test output is gone
- Previous compiler errors are gone
- Previous stack traces are gone

Therefore:
> Always use `--report=<path>` with `/smartspec_fix_errors` after running `/smartspec_implement_tasks` if you start a new Task.

---

# 5. The SPEC-First Workflow Chain
### 5.1 /smartspec_generate_spec_from_prompt
Creates starter specs from natural-language prompts.  
Does **not** overwrite existing specs.

### 5.2 /smartspec_generate_spec
Upgrades/refines specs from validated `spec-id`s.

### 5.3 /smartspec_generate_plan
Creates a plan (`plan.md`) from a spec.

### 5.4 /smartspec_generate_tasks
Creates `tasks.md` from a spec or plan.
- If tasks already exist, it creates *additive* sections.

### 5.5 /smartspec_implement_tasks
Implements code for the tasks.
- Writes files in code areas
- Produces **implementation reports**:
  - `.spec/reports/implement-tasks/<scope>-implementation-report.md`
- These reports are now essential for `/smartspec_fix_errors`.

### 5.6 /smartspec_fix_errors — *FULL v5.7.1 SUPPORT*
This workflow now supports structured report ingestion.
```
--report=<path>
```
Example:
```
/smartspec_fix_errors.md --kilocode \
  --report=.spec/reports/implement-tasks/T026-T040-implementation-report.md
```
If no `--report` is specified, SmartSpec will automatically:
1. Look under `.spec/reports/implement-tasks/`
2. Select the newest relevant report
3. Use that structured context for error analysis

This enables **continuity** even when Kilo resets context.

### 5.7 /smartspec_generate_tests
Creates tests aligned with SPEC + tasks.

### 5.8 /smartspec_ci_quality_gate
CI-level checks for spec completeness, test coverage, quality bars.

---

# 6. SPEC_INDEX & Registries
SmartSpec uses `.spec/SPEC_INDEX.json` as the canonical spec registry.
Other fallback locations are allowed (e.g., repo root), but this is the authoritative one.

Registries under `.spec/registry/` define:
- UI components
- design tokens
- shared data models
- version ranges

Workflows must:
- read registries
- never rewrite registries unless allowed by `additive-meta` mode
- validate implementation against canonical definitions

---

# 7. Directory Overview
```
.smartspec/
  workflows/
  system_prompt_smartspec.md
  knowledge_base_smart_spec.md
  knowledge_base_smartspec_install_and_usage.md

.spec/
  SPEC_INDEX.json
  registry/
  reports/
    implement-tasks/
    smartspec_fix_errors/

specs/<category>/<spec-id>/spec.md
```

---

# 8. Using Reports Effectively
Implementation reports are core to SmartSpec v5.7.1.

### 8.1 For implement → fix_errors flow
Typical flow:
```
/smartspec_implement_tasks.md specs/.../tasks.md --kilocode
```
This generates:
```
.spec/reports/implement-tasks/<scope>-implementation-report.md
```
Then fix errors:
```
/smartspec_fix_errors.md --kilocode \
  --report=.spec/reports/implement-tasks/<scope>-implementation-report.md
```

### 8.2 Auto-discovery
If no report is provided, SmartSpec scans:
```
.spec/reports/implement-tasks/
```
And selects the newest matching one.

### 8.3 Why `--report` is crucial
Because Kilo clears runtime logs when you start a new task.
The *only* reliable way to preserve context is:
```
--report=<path>
```

---

# 9. Troubleshooting
### ❌ Problem: `/smartspec_fix_errors` cannot find failing tests
**Cause:** new Kilo task = no logs in memory  
**Solution:**  
```
--report=<path>
```

### ❌ Problem: Missing SPEC ownership
Ensure `.spec/SPEC_INDEX.json` exists.  
Otherwise workflows must guess.

### ❌ Problem: Conflicts between specs
Use:
```
/smartspec_project_copilot --kilocode
```
This reveals cross-spec mismatches.

### ❌ Problem: UI mismatch
Run:
```
/smartspec_ui_validation --kilocode
```
It cross-checks UI JSON, registry, and code.

---

# 10. Best Practices
- Always think SPEC-first.
- Keep SPECs small and modular.
- Preserve `.spec/reports/**` — do not delete them.
- Always use `--report` when using fix_errors across tasks.
- Do not hand-edit SPEC_INDEX unless necessary.
- Use additive modes (`--mode=additive-meta`) cautiously.
- Align UI with design tokens & component registry.

---

# 11. Developer Checklist
Before running SmartSpec workflows:
- SPEC exists? ✔
- Tasks exist? ✔
- SPEC_INDEX is valid? ✔
- Registry entries match implementation? ✔

Before running fix errors:
- Implementation report exists? ✔  
- Pass via `--report` if starting a new Kilo task ✔

---

# 12. Summary
This KB now fully supports SmartSpec v5.7.1 workflows, including the newest behavior:
- **Use `--report` with `/smartspec_fix_errors.md`**  
- **Full auto-discovery under `.spec/reports/implement-tasks/`**  
- **Cross-task continuity for KiloCode users**

All SmartSpec assistants should rely on this file + the governance KB as the unified source of truth for usage patterns.

End of SmartSpec Install & Usage Knowledge Base – v5.7.1.