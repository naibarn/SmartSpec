name: /smartspec_implement_tasks
version: 6.2.0
role: implementation/execution
write_guard: ALLOW-WRITE
purpose: Implement code changes strictly from `tasks.md` (and `spec.md`/`plan.md` when present)
         with SmartSpec v6 governance: tasks-first execution, multi-repo read-only context,
         registry-aware reuse, KiloCode Orchestrator sub-task enforcement, safe write gating,
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

### 0.2 Kilo Orchestrator Sub-Task Invariant (Legacy Rule — DO NOT REMOVE)

When running under Kilo with `--kilocode`:

1. Kilo MUST NOT execute this workflow as a single root job over many tasks
   without sub-task decomposition.
2. Before any implementation begins, Kilo MUST:
   - enable Orchestrator Mode; and
   - create an appropriate set of Kilo sub-tasks that map to the selected
     SmartSpec tasks (typically one sub-task per top-level task, or per
     small batch).
3. This workflow MUST assume that it is running inside a Kilo sub-task
   whenever `--kilocode` is set and Orchestrator is active.
4. If this workflow detects that it is running with `--kilocode` but not
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

### 0.3 Non-Stop Workflow Invariant

To prevent premature stops and half-finished work:

1. Completion of a single task or edit attempt MUST NOT be treated as a
   reason to end the entire workflow if there are remaining selected tasks.
2. When running under `--kilocode`, any single Kilo edit failure (for
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

### 0.4 Orchestrator Recovery Invariant (Legacy Rule — DO NOT REMOVE)

This invariant encodes the legacy rule that implementation runs must not
"die quietly" under Kilo Orchestrator:

1. When running with `--kilocode` and Orchestrator is active, if an
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
   - a hard governance violation (see 0.3) that prevents any safe
     continuation.

The historical rule can be restated as:

> If an implementation run cannot continue under Kilo, you MUST switch back
> into Orchestrator Mode, re-plan, and then continue — you must not simply
> stop and leave tasks half-finished.

These invariants are part of the SmartSpec core governance for this
workflow. Teams may extend them but MUST NOT delete or contradict them.

---

## 1) Summary (and what changed in v6.2.0)

`/smartspec_implement_tasks` performs real implementation changes, but only under explicit write gates.

**Breaking (v6):** Writes to runtime source trees (code/tests/config) are now governed by a two-gate rule:

- `--apply` AND
- `--write-code`

Without both, the workflow MUST run in `--validate-only` mode (no code writes, no `tasks.md` checkbox updates).

This aligns the workflow with v6 governance requiring explicit opt-in for runtime-tree writes.

---

## 2) Where this fits (relationship with other workflows)

Canonical chain context (preferred order):

1) `/smartspec_generate_spec` → `/smartspec_generate_plan` → `/smartspec_generate_tasks`
2) **THIS (implement):** `/smartspec_implement_tasks`
3) **STRICT VERIFY:** `/smartspec_verify_tasks_progress_strict` (recommended immediately after implement)
4) **SYNC CHECKBOXES:** `/smartspec_sync_tasks_checkboxes` (if checkbox sync is separated in your setup)

Optional helpers (non-canonical but commonly useful):

- PROMPTER: `/smartspec_report_implement_prompter` (recommended for large/complex changes before implement)
- Quality gates: `/smartspec_test_suite_runner` → `/smartspec_test_report_analyzer`
- Security audits / threat-model checks (project-specific)
- Release flows (e.g., hotfix/release tagging) should consume verified evidence, not assumptions

This workflow MUST NOT invoke other workflows programmatically; it may only recommend them.

---

## 3) Inputs / Outputs

### 3.1 Primary input (positional-first)

- Positional: `<tasks.md>`

Examples:

- `specs/<category>/<spec-id>/tasks.md`

### 3.2 Optional inputs

- adjacent artifacts (auto-detected from tasks folder when possible):
  - `spec.md` (required)
  - `plan.md` (optional)
  - `ui.json` (optional)

### 3.3 Governance context (read-only)

- `.spec/SPEC_INDEX.json` (canonical)
- `.spec/registry/**` (canonical)
- optional registry roots (read-only)
- multi-repo context via config (`workspace_roots`, `repos_config`)

### 3.4 Outputs

Safe outputs (no `--apply` required):

- `.spec/reports/implement-tasks/<run-id>/report.md`
- `.spec/reports/implement-tasks/<run-id>/summary.json`
- `.spec/reports/implement-tasks/<run-id>/change_plan.md` (always generated when `--apply` is present; generated before any write)

Governed writes (require `--apply`):

- `tasks.md` checkbox changes and implementation notes (governed by spec folder rules)

Runtime-tree writes (require two gates):

- code/tests/config changes in the current repo only (require `--apply --write-code`)

---

## 4) Write model, gates, and constraints

### 4.1 Default behavior

- If `--apply` is absent → MUST behave like `--validate-only`.
- If `--apply` is present but `--write-code` is absent → MAY update governed artifacts only (e.g., `tasks.md`), but MUST NOT write code.
- If both `--apply` and `--write-code` are present → may write code/tests/config **in the current repo only**.

### 4.2 Allowed write scopes

- `.spec/reports/implement-tasks/**` (safe)
- `specs/<category>/<spec-id>/tasks.md` (governed; checkbox + notes only)
- runtime source trees in **current repo only** when gated by `--apply --write-code`

Must never:

- write into sibling repos discovered via multi-repo scanning
- write into `.spec/registry/**` or `.spec/SPEC_INDEX.json`

---

## 5) Flags

### 5.1 Universal flags (must support)

- `--config <path>` (default: `.spec/smartspec.config.yaml`)
- `--lang <th|en>`
- `--platform <cli|kilo|ci|other>`
- `--apply`
- `--out <path>` (report root override; must pass output-root safety checks)
- `--json`
- `--quiet`

### 5.2 Inputs

- positional: `<tasks.md>`
- `--tasks-path <path>` (override positional)
- `--spec-path <path>` (override auto-detect)
- `--spec-id <id>` (resolve via SPEC_INDEX; if present)

### 5.3 Task selection

- `--task <n>`
- `--tasks <csv>`
- `--range <a-b>`
- `--from <n>`
- `--start-from <Tnnn>` (legacy alias)

### 5.4 Completion and resume

- `--skip-completed` (default)
- `--force-all`
- `--resume`

### 5.5 Phases (if tasks are phase-tagged)

- `--phase <n>`
- `--phases <csv>`
- `--phase-range <a-b>`

### 5.6 Safety / preview

- `--safety-mode <strict|dev>` (default: strict)
- `--strict` (alias for strict)
- `--validate-only`
- `--dry-run` (alias)

### 5.7 Runtime-tree write gates (v6)

- `--write-code`
  - explicit opt-in to modify runtime source trees in the current repo
  - only takes effect when `--apply` is present

### 5.8 Privileged operations

- `--allow-network`
  - required to perform any action that needs network (dependency fetch, remote git fetch/push, remote APIs)

### 5.9 Kilo / Orchestrator

- `--kilocode`
  - enables Kilo integration semantics when running under Kilo

- `--require-orchestrator`
  - only meaningful with `--kilocode`
  - in strict mode: fail fast if Orchestrator Mode is not clearly active

---

## 6) Security hardening (mandatory)

### 6.1 Path safety

All filesystem paths (inputs and outputs) MUST enforce:

- path normalization; reject traversal (`..`), absolute paths, control chars
- no symlink escape for reads/writes
- output-root safety: `--out` (and report dir) must resolve under an allowlist and not under a denylist

### 6.2 Bounded scanning

- enforce limits (max files/bytes/time) from config
- if limits are hit, record reduced coverage in report

### 6.3 Secret handling

- do not accept secrets as raw CLI flags
- redact secrets and sensitive values from reports
- reports should prefer diffs + short excerpts + hashes; avoid dumping full configs/logs

### 6.4 Privileged execution (if running external commands)

If the workflow executes external commands (tests, linters, package managers), it MUST:

- spawn without a shell (no `sh -c`)
- use a binary allowlist (+ subcommand allowlist where applicable)
- enforce per-command timeouts
- capture outputs with redaction

---

## 7) KiloCode semantics (ties back to Section 0)

When `--kilocode` is present and Kilo is detected:

- Orchestrator-per-task execution is mandatory for complex scopes.
- This workflow MUST assume it runs inside a Kilo sub-task when Orchestrator is active.
- If sub-task context is missing:
  - strict: fail fast with a governance error
  - dev: allow degraded mode with prominent warnings

---

## 8) Report structure

Default report path:

- `.spec/reports/implement-tasks/<run-id>/`

Minimum artifacts:

- `report.md`
- `change_plan.md` (when `--apply` is present; created before any governed/runtime write)
- `summary.json`

### `summary.json` (minimum schema)

```json
{
  "workflow": "smartspec_implement_tasks",
  "version": "6.2.0",
  "run_id": "string",
  "status": "success|failed|blocked",
  "applied": true,
  "write_gates": {
    "apply": true,
    "write_code": true,
    "allow_network": false
  },
  "scope": {
    "tasks_path": "string",
    "spec_path": "string",
    "selected_tasks": ["T001", "T002"],
    "safety_mode": "strict"
  },
  "writes": {
    "reports": ["..."],
    "governed": ["..."],
    "runtime": ["..."]
  },
  "warnings": ["string"],
  "errors": ["string"]
}
```

---

## 9) Weakness & risk check (threats to watch)

This workflow is high-impact. Minimum risks and required mitigations:

- **Scope creep** → enforce tasks-first; fail on empty selection; forbid implicit new tasks.
- **Repo boundary escape** → hard block writes outside current repo; treat other repos as read-only.
- **Path traversal/symlink escape** → normalize paths; refuse unsafe; resolve symlinks before writing.
- **Supply-chain risk (deps install/update)** → require `--allow-network`; prefer lockfile-respecting installs; record changes.
- **Command injection** → no-shell spawning + allowlists.
- **Secret leakage** → redact outputs; never print env values; avoid logging raw prompts or tokens.
- **DoS via scanning** → bounded scanning; record reduced coverage.

---

## 10) Examples (dual-command)

### 10.1 Validate-only (no writes)

CLI:

```bash
/smartspec_implement_tasks \
  specs/<category>/<spec-id>/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks \
  --json
```

Kilo Code:

```bash
/smartspec_implement_tasks.md \
  specs/<category>/<spec-id>/tasks.md \
  --validate-only \
  --out .spec/reports/implement-tasks \
  --json \
  --kilocode
```

### 10.2 Apply + write code (governed + runtime-tree writes)

CLI:

```bash
/smartspec_implement_tasks \
  specs/<category>/<spec-id>/tasks.md \
  --apply \
  --write-code \
  --safety-mode strict \
  --out .spec/reports/implement-tasks \
  --json
```

Kilo Code:

```bash
/smartspec_implement_tasks.md \
  specs/<category>/<spec-id>/tasks.md \
  --apply \
  --write-code \
  --require-orchestrator \
  --safety-mode strict \
  --out .spec/reports/implement-tasks \
  --json \
  --kilocode
```

---

## 11) Exit codes

- `0`: success (or validate-only completed)
- `1`: implementation failed (recoverable errors exhausted)
- `2`: governance/config error (blocked before implementation)

---

# End of workflow doc

