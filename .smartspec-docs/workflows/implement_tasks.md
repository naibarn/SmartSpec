# SmartSpec Manual — /smartspec_implement_tasks (English, v5.7.2 Enforced Edition)

This manual reflects the **full enforcement version** of `/smartspec_implement_tasks` where:
- `--require-orchestrator` is strictly honored.
- Orchestrator Mode **must** be explicitly active when using `--kilocode --require-orchestrator`.
- Missing/false/unknown Orchestrator signals → treated as **not active**.
- `strict` safety mode triggers **fail-fast**.
- `dev` mode warns loudly and may optionally continue.

These rules match the updated workflow file.

---

# 1. Overview

`/smartspec_implement_tasks` performs *real implementation work* based on `tasks.md` while enforcing:
- SPEC_INDEX governance
- Registry & multi-repo ownership boundaries
- UI governance (design tokens, App components, ui.json)
- Web-stack guardrails
- AI/data-sensitivity rules
- KiloCode + Orchestrator Mode integration

This is the **strict, enforced version** aligned with workflow v5.7.2.

---

# 2. What Changed in v5.7.2 (Enforced)

## 2.1 Hard enforcement of `--require-orchestrator`
When passed together with `--kilocode`, the rule is:

> **If Orchestrator Mode is not explicitly reported as active, the workflow MUST treat it as inactive and fail (strict mode).**

Explicitly active means:
```
env.orchestrator_active = true
```
(or an equivalent integration flag from Kilo.)

### If Orchestrator is missing / false / unknown:
- `strict` → **FAIL immediately** with a clear error message
- `dev` → warn loudly; may stop or continue in degraded mode

No silent fallback is allowed.

## 2.2 Non-auto-switching rule
Kilo Code will **not** auto-switch into Orchestrator Mode.
Users must activate Orchestrator Mode manually in the Kilo UI before running the workflow.

## 2.3 Updated Step 1.a in workflow
The workflow now checks Orchestrator Mode **before any implementation step**.

---

# 3. Inputs & Outputs

## Inputs
- Required: `tasks.md`
- Optional: `spec.md`, `plan.md`, `ui.json`
- Governance: SPEC_INDEX, registries, multi-repo config

## Outputs
- Code updates in the current repo
- Updated tasks.md checkboxes
- Implementation summary / optional report

---

# 4. Flags (Updated)

### Orchestrator Flags
```
--kilocode
--require-orchestrator
```

### Safety
```
--safety-mode=strict | dev
--strict
```

### Validation
```
--validate-only
--dry-run
```

### Task selection
```
--task
--tasks
--range
--from
--skip-completed
--resume
```

### Multi-repo
```
--workspace-roots
--repos-config
--registry-dir
--registry-roots
```

---

# 5. Orchestrator Behavior (Fully Enforced)

## 5.1 Using `--kilocode` only
- Workflow attempts Orchestrator support
- If Orchestrator is not active → workflow may continue in linear mode with warnings

## 5.2 Using `--kilocode --require-orchestrator`
**This is the enforced behavior:**

If Orchestrator Active signal is:
- **missing**
- **false**
- **unknown**

→ Treat as **NOT active**.

### strict mode:
- Hard fail
- Error message example:
  > "Orchestrator Mode is required (`--require-orchestrator`) but not active. Please enable Orchestrator Mode in Kilo and re-run."

### dev mode:
- Loud warning
- Workflow may stop or continue in degraded non-Orchestrator mode

No silent fallback is allowed.

---

# 6. Example Commands

## Strongly recommended (inside Kilo):
```
/smartspec_implement_tasks specs/.../tasks.md \
  --kilocode --require-orchestrator --safety-mode=strict
```

## Validate only:
```
/smartspec_implement_tasks specs/.../tasks.md --validate-only
```

## With limited tasks (using task IDs like T001/T002):
```
/smartspec_implement_tasks specs/.../tasks.md --task=T003 \
  --kilocode --require-orchestrator
```

---
# 6.1 Full Use Case Examples (Expanded)
Below are the **complete patterns** normally included in the full SmartSpec Implement Tasks manual.

## ✔ Use Case 1 — Implement a single task
```
--task=T002
```
Runs exactly task T002.

## ✔ Use Case 2 — Implement multiple tasks
```
--tasks=T001,T004,T009
```
Order follows the order in tasks.md.

## ✔ Use Case 3 — Implement a continuous range
```
--range=T003-T010
```
Runs from task T003 to T010 inclusive.

## ✔ Use Case 4 — Open-ended range
```
--from=T005
```
Runs T005 through the last task.

## ✔ Use Case 5 — Mixed selection
```
--tasks=T002,T007 --range=T010-T015
```
Useful when combining related tasks.

## ✔ Use Case 6 — Skip completed tasks
```
--skip-completed
```
Even if selected, tasks already marked ✓ will be skipped.

## ✔ Use Case 7 — Resume workflow
```
--resume
```
Continues from the last incomplete task in tasks.md.

---
# 6.2 Phase-Based Use Cases
Phases may appear as:
```
## Phase: 1 (setup)
## Phase: 2 (api)
## Phase: 3 (ui)
```

## ✔ Use Case 8 — Run a single phase
```
--phase="Phase 2"
```
Runs all tasks under Phase 2.

## ✔ Use Case 9 — Run multiple phases
```
--phases="Phase 1","Phase 3"
```

## ✔ Use Case 10 — Combine phases + ranges
```
--phase="Phase 2" --from=T006
```

---
# 6.3 Advanced Kilo Use Cases

## ✔ Use Case 11 — Strict Kilo Orchestrator enforcement
```
--kilocode --require-orchestrator --safety-mode=strict
```
If Orchestrator Mode is not active → **FAIL immediately**.

## ✔ Use Case 12 — Resume inside Kilo with enforced Orchestrator
```
--resume --kilocode --require-orchestrator
```

## ✔ Use Case 13 — Validate large edit sequences
```
--validate-only
```
No file changes — useful for previewing multi-file impact.

---
# 6.4 Special Patterns

## ✔ Use Case 14 — Implement only newly added tasks (metadata-based)
If tasks.md includes metadata banners:
```
--from=Tlast
```

## ✔ Use Case 15 — Implement by category tags
If tasks include tags (`[api]`, `[ui]`, etc.):
```
--tag=api
```
(If supported by your tasks.md variant.)

## ✔ Use Case 16 — Implement only failing tasks from previous run
```
--resume --skip-completed
```

---
# 7. Troubleshooting

### ❗ Orchestrator not active
This workflow will stop (strict mode):
> "Orchestrator Mode is required (`--require-orchestrator`) but not active. Please enable Orchestrator Mode in Kilo and re-run."

Fix:
1. Open Kilo UI
2. Switch to **Orchestrator Mode** manually
3. Run again

### ❗ Kilo edit failure
- Workflow will narrow scope
- Suggest retries or split tasks

---

# 8. Best Practices

### ⭐ For Kilo users:
```
--kilocode --require-orchestrator --safety-mode=strict
```

### ⭐ Always activate Orchestrator Mode *before* running
Kilo will not auto-switch even if the workflow requests it.

### ⭐ Keep tasks small and explicit
### ⭐ Use validate-only first on large repos

---

# END OF ENGLISH MANUAL

