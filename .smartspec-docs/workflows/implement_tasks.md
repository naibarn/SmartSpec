# SmartSpec Manual — /smartspec_implement_tasks (English, v5.7.2)

This is the **English-only manual**, updated to align with the latest workflow changes, including:
- `--require-orchestrator`
- Updated KiloCode semantics
- Updated fallback/strict behavior
- Updated troubleshooting and examples.

---

## 1. Overview

`/smartspec_implement_tasks` implements code from `tasks.md` while enforcing SmartSpec governance:
- SPEC_INDEX + registries
- multi-repo boundaries
- UI governance
- web/AI/data guardrails
- Kilo Orchestrator support (`--kilocode`)
- strict mode enforcement

v5.7.2 introduces the ability to **require Orchestrator Mode** using `--require-orchestrator`.

---

## 2. What’s new in v5.7.2

### 2.1 New flag: `--require-orchestrator`

This new flag is **additive** and works only when paired with `--kilocode`:

> “If Orchestrator Mode is not active, **stop immediately** (in strict mode).”

Behavior:
- Under Kilo:
  - Orchestrator active → proceed
  - inactive →
    - strict → **error + stop**
    - dev → strong warning; may continue or stop

- Not under Kilo → record a harmless note.

### 2.2 Improved Kilo edit failure handling
- Do not hard-stop on first error
- Narrow scope
- Suggest retries
- Prefer per-task edits over mega-edits

### 2.3 Updated workflow steps
A new **Step 1.a** checks Orchestrator **before** implementation begins.

---

## 3. Inputs and Outputs

### Inputs
- Required: path to `tasks.md`
- Optional: spec.md, plan.md, ui.json, registries, SPEC_INDEX, multi-repo config.

### Outputs
- Code changes
- Updated tasks.md checkboxes
- Summary
- Optional implementation report

---

## 4. Updated Flags

### Orchestrator flags
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

### Multi-repo / registry
```
--workspace-roots
--repos-config
--registry-dir
--registry-roots
```

---

## 5. Orchestrator behavior

### 5.1 With `--kilocode`
- Attempt Orchestrator activation
- If unavailable → fallback with warning

### 5.2 With `--kilocode --require-orchestrator`
- Orchestrator MUST be active
- If not:
  - strict → error + stop
  - dev → warn loudly; possible fallback or stop

### 5.3 Kilo edit failures
- Do not stop immediately
- Reduce scope, retry, and propose next actions

---

## 6. Examples

### Require Orchestrator
```
/smartspec_implement_tasks specs/core/spec-001/tasks.md \
  --kilocode --require-orchestrator --safety-mode=strict
```

### Allow fallback
```
/smartspec_implement_tasks specs/core/spec-001/tasks.md --kilocode
```

### Validate-only for safety
```
/smartspec_implement_tasks specs/core/spec-001/tasks.md --validate-only
```

---

## 7. Troubleshooting (updated)

### Orchestrator not active
Error example:
> "Orchestrator Mode is required (`--require-orchestrator`) but not active. Please enable Orchestrator in Kilo and re-run."

### Why enforce Orchestrator?
Large edits without Orchestrator typically cause:
- context loss
- ambiguous edits
- inconsistent task execution

---

# End of English Manual

