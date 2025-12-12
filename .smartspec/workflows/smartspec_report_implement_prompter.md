# Workflow: /smartspec_report_implement_prompter.md

> **Status:** Revised (Governance-aligned)
> **Purpose:** Generate implementation-ready prompts from **strict verification reports** without polluting engine or project source folders.

---

## 1. Design Intent (What changed & why)
This revision enforces **clear separation of concerns**:

- **Engine code** stays in `scripts/` (versioned, not temporary)
- **Kilo Code registration artifacts** live in `.kilocode/workflows/` (cache-like, deletable)
- **Runtime outputs** are written **only** to `.smartspec/prompts/<spec-id>/`

This prevents:
- Accidental writes to `scripts/`
- Perceived "garbage" accumulation
- Mixing workflow engines with user artifacts

---

## 2. Read / Write Boundaries (Hard Rules)

### Read-only inputs
- `specs/**/spec.md`
- `specs/**/tasks.md`
- strict verification report (`*.json`)

### Allowed write locations (ONLY)
```
.smartspec/prompts/<spec-id>/
```

### Forbidden write locations
- `scripts/`
- `specs/`
- `.spec/`
- `.kilocode/workflows/`

> Any runtime write outside `.smartspec/prompts/` is a **bug**.

---

## 3. Output Directory Resolution (Mandatory)

### Resolution order
1. Explicit `--output`
2. Default: `.smartspec/prompts/<spec-id>`

### Guardrail
If resolved output path:
- contains `/scripts`
- equals project root
- is outside `.smartspec/prompts`

→ **Abort with error**

---

## 4. CLI Usage

```bash
/smartspec_report_implement_prompter \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-strict.json \
  --output .smartspec/prompts/<spec-id>
```

---

## 5. Kilo Code Usage (Required Pattern)

```bash
/smartspec_report_implement_prompter.md \
  --spec specs/feature/<spec-id>/spec.md \
  --tasks specs/feature/<spec-id>/tasks.md \
  --report .spec/reports/verify-tasks-progress/<spec-id>-strict.json \
  --output .smartspec/prompts/<spec-id> \
  --kilocode
```

> `.kilocode/workflows/` artifacts (chmod / symlink) are **registration cache** and may be safely deleted.

---

## 6. Generated Structure

```
.smartspec/prompts/<spec-id>/
  README.md
  api-cluster.md
  tests-cluster.md
  docs-cluster.md
  deploy-cluster.md
```

No other files are generated.

---

## 7. Task Classification Logic (Unchanged)
- **unsynced** → checkbox sync only
- **simple** → inline implementation hints
- **complex** → clustered by domain (API / Tests / Docs / Deploy)

---

## 8. Idempotency & Cleanup

- Re-running the workflow **overwrites prompts** for the same `<spec-id>`
- Safe to delete:
  - `.kilocode/workflows/smartspec_*`
  - `.smartspec/prompts/<spec-id>`

- Never delete:
  - `scripts/`

---

## 9. Non-Goals (Explicit)

This workflow does **NOT**:
- Modify `spec.md` or `tasks.md`
- Sync checkboxes
- Perform verification

Use:
- `/smartspec_verify_tasks_progress_strict`
- `/smartspec_sync_tasks_checkboxes`

---

## 10. Canonical Execution Flow

```
STRICT VERIFY
  ↓
IMPLEMENT PROMPTER (this workflow)
  ↓
CODE CHANGES
  ↓
STRICT VERIFY
  ↓
SYNC CHECKBOXES
```

---

## 11. Compliance Checklist
- [x] CLI-first
- [x] Kilo Code compatible
- [x] No engine pollution
- [x] Output isolated & deletable
- [x] Governance-aligned

---

**End of workflow specification**

