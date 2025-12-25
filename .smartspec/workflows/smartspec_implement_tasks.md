---
description: Implement code changes strictly from tasks.md with 100% duplication prevention and SmartSpec v7 governance.
version: 7.0.0
workflow: /smartspec_implement_tasks
---

name: /smartspec_implement_tasks
version: 7.0.0
role: implementation/execution
write_guard: ALLOW-WRITE
purpose: Implement code changes strictly from `tasks.md` with 100% duplication prevention,
         tasks-first execution, multi-repo read-only context, registry-aware reuse,
         KiloCode Orchestrator sub-task enforcement, safe write gating,
         privileged-ops hardening (no-shell/allowlist/timeouts), network deny-by-default,
         and report-first evidence.

---

## 0) Non-Removable Invariants (DO NOT DELETE OR WEAKEN)

> These invariants encode legacy SmartSpec + Kilo behaviour. They MUST NOT
> be removed, renamed, or weakened without an explicit governance KB change
> and a major version bump for this workflow.

### 0.1 Tasks-First Invariant

1. Implementation MUST ALWAYS be driven by `tasks.md`.
   - No code change may be performed that is not traceable to an explicit
     task entry in `tasks.md`.
   - This applies across all environments (CLI, Kilo Code, Claude Code,
     Google Antigravity).
2. This workflow MUST NOT run if:
   - `tasks.md` is missing;
   - `tasks.md` cannot be parsed; or
   - task selection flags resolve to an empty set.
   It MUST instead fail fast with a clear governance error.
3. `tasks.md` is the canonical mechanism for scoping work. This workflow
   MUST NOT:
   - infer new tasks implicitly from diffs or code structure;
   - silently expand scope beyond the selected tasks;
   - modify task numbering or structure (only checkboxes/notes are allowed).

### 0.2 Duplication Prevention Invariant (NEW in v7.0.0)

1. Before implementing any task, the workflow MUST check for existing similar
   components in `.spec/registry/**`.
2. If potential duplicates are found (similarity >= threshold), the workflow MUST:
   - in `strict` safety mode: fail fast and present duplicates to user;
   - in `dev` safety mode: warn prominently but allow continuation with user confirmation.
3. After implementation, the workflow MUST validate that no duplicates were created.
4. This invariant applies to all component types: APIs, data models, UI components (including A2UI),
   services, workflows, and integrations.

### 0.3 Kilo Orchestrator Sub-Task Invariant (Legacy Rule — DO NOT REMOVE)

When running under Kilo with `--platform kilo`:

1. Kilo MUST NOT execute this workflow as a single root job over many tasks
   without sub-task decomposition.
2. Before any implementation begins, Kilo MUST:
   - enable Orchestrator Mode; and
   - create an appropriate set of Kilo sub-tasks that map to the selected
     SmartSpec tasks (typically one sub-task per top-level task, or per
     small batch).
3. This workflow MUST assume that it is running inside a Kilo sub-task
   whenever `--platform kilo` is set and Orchestrator is active.
4. If this workflow detects that it is running with `--platform kilo` but not
   inside a sub-task context (for example, required Kilo sub-task metadata
   is missing), it MUST:
   - in `strict` safety mode: fail fast with a governance error and
     instruct the user/Orchestrator to enable sub-task decomposition;
   - in `dev` safety mode: it MAY either fail fast or run in degraded
     non-Orchestrator mode, but MUST emit a prominent warning and label the
     run as non-compliant with Kilo sub-task governance.
5. Orchestrator must treat sub-task creation as mandatory for complex
   implementations. The legacy rule is explicitly preserved:

   > When switching to Orchestrator Mode under Kilo, you MUST `new subtasks`
   > before implementing tasks.

### 0.4 Non-Stop Workflow Invariant

To prevent premature stops and half-finished work:

1. Completion of a single task or edit attempt MUST NOT be treated as a
   reason to end the entire workflow if there are remaining selected tasks.
2. When running under `--platform kilo`, any single Kilo edit failure (for
   example "Edit Unsuccessful" or similar) MUST be treated as a recoverable
   event:
   - narrow scope (fewer tasks, smaller file ranges);
   - retry where appropriate; and
   - surface clear next-step options.
3. The workflow MAY stop early only when:
   - a hard governance violation occurs (for example missing SPEC_INDEX,
     registry corruption, forbidden write target);
   - Orchestrator requirement is not satisfied while `--require-orchestrator`
     is present; or
   - the user/Orchestrator explicitly cancels.
4. Under Kilo, finishing a sub-task MUST:
   - return a clear per-task report;
   - hand control back to Orchestrator so it can decide the next sub-task;
   - not terminate the entire project run unless Orchestrator decides so.

### 0.5 Orchestrator Recovery Invariant (Legacy Rule — DO NOT REMOVE)

This invariant encodes the legacy rule that implementation runs must not
"die quietly" under Kilo Orchestrator:

1. When running with `--platform kilo` and Orchestrator is active, if an
   implementation attempt:
   - stalls or makes no forward progress;
   - fails repeatedly with non-fatal edit errors; or
   - encounters partial completion where some, but not all, selected
     tasks are done;
   then this workflow MUST hand control back to Orchestrator Mode to
   re-plan and continue, rather than terminating silently.
2. The correct behaviour is:
   - detect the stalled/partial state;
   - summarise what has been completed and what remains;
   - explicitly request Orchestrator to re-enter planning for the
     remaining work (narrowing scope if needed);
   - return a structured report so Orchestrator can:
     - update its task/sub-task view; and
     - decide whether to retry, split tasks further, or escalate.
3. This workflow MUST NOT treat a non-fatal implementation issue as a
   terminal success state. If progress cannot be made within the current
   sub-task, it MUST:
   - surface a clear governance/completion status back to Orchestrator; and
   - allow Orchestrator to resume control and plan the next steps.
4. Under Kilo, a valid stop condition is either:
   - Orchestrator explicitly decides the project is complete or cancelled; or
   - a hard governance violation (see 0.4) that prevents any safe
     continuation.

The historical rule can be restated as:

> If an implementation run cannot continue under Kilo, you MUST switch back
> into Orchestrator Mode, re-plan, and then continue — you must not simply
> stop and leave tasks half-finished.

These invariants are part of the SmartSpec core governance for this
workflow. Teams may extend them but MUST NOT delete or contradict them.

---


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

### Flag usage notes

- **Config-first approach:** Prefer setting defaults in `.spec/smartspec.config.yaml` to minimize command-line flags
- **Positional arguments:** When supported, use positional arguments for primary inputs (e.g., spec path) instead of flags
- **Boolean flags:** Flags without values are boolean (presence = true, absence = false)
- **Path safety:** All path arguments must pass safety validation (no directory traversal, symlink escape, or absolute paths outside project)
- **Secret handling:** Never pass secrets as flag values; use `env:VAR_NAME` references or config file

## 1) Behavior

### 1) Pre-Implementation Validation (MANDATORY)

Before implementing any task, the AI agent **MUST** check for existing similar components.

**Validation Command:**
```bash
python3 .smartspec/scripts/detect_duplicates.py \
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

### 2) Implement tasks

- Implement code changes strictly from `tasks.md`.
- Ensure every task has verifiable outputs (evidence hooks).

### 3) Preview & report (always)

Write:

- `.spec/reports/implement-tasks/<run-id>/report.md`
- `.spec/reports/implement-tasks/<run-id>/summary.json`
- `.spec/reports/implement-tasks/<run-id>/change_plan.md` (always generated when `--apply` is present; generated before any write)

### 4) Post-Implementation Validation (MANDATORY)

After implementing tasks and before applying changes, the AI agent **MUST** validate the changes.

**Validation Command:**
```bash
python3 .smartspec/scripts/validate_implementation.py \
  --tasks specs/<category>/<spec-id>/tasks.md \
  --spec specs/<category>/<spec-id>/spec.md \
  --registry .spec/registry/ \
  --check-duplicates --threshold 0.8
```

**Validation Rules:**
- **Exit Code `0` (Success):** The implementation is valid. The agent may proceed with `--apply`.
- **Exit Code `1` (Failure):** The implementation is invalid. The agent **MUST NOT** use `--apply`.
- The full output from the validation script **MUST** be included in `report.md`.

### 5) Apply (only with `--apply` and if validation passes)

- Update `specs/<category>/<spec-id>/tasks.md`.
- Apply code changes.

---

# End of workflow doc
