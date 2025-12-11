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

## With limited tasks:
```
/smartspec_implement_tasks specs/.../tasks.md --task=3 \
  --kilocode --require-orchestrator
```

---

# 7. Troubleshooting

### ❗ Orchestrator not active
This workflow will stop (strict mode):
> "Orchestrator Mode is required (`--require-orchestrator`) but not active."

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

