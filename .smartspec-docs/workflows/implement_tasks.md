# Implement Tasks Workflow

Auto-implement tasks from `tasks.md` with safety constraints, progress tracking, checkpoint/resume functionality, and validation.

---

## Summary

The `smartspec_implement_tasks` workflow automatically implements tasks defined in `tasks.md` or `implement-prompt.md`. It respects checkbox status, validates after each task, and supports incremental development.

**Key Features:**
- ✅ Automatic task implementation
- ✅ Checkbox-aware (skip completed tasks by default)
- ✅ Checkpoint/resume functionality
- ✅ Validation after each task (compile, test, lint)
- ✅ Automatic rollback on validation failure
- ✅ Progress tracking and reporting

---

## Usage

### Basic Usage

```bash
/smartspec_implement_tasks <path-to-tasks.md> [options]
```

### Path Formats

```bash
# Direct path to tasks.md
/smartspec_implement_tasks specs/feature/spec-004-financial-system/tasks.md

# Directory (will look for tasks.md inside)
/smartspec_implement_tasks specs/feature/spec-004-financial-system

# Implement prompt file
/smartspec_implement_tasks specs/feature/spec-004-financial-system/implement-prompt-spec-004.md
```

---

## Options

### Mode Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-completed` | Skip tasks with checkbox `[x]` | ✅ Yes (default) |
| `--force-all` | Re-implement all tasks, ignore checkboxes | No |
| `--validate-only` | Validate only, no implementation | No |

### Scope Options

| Option | Description | Example |
|--------|-------------|---------|
| `--phase <n>` | Implement specific phase(s) | `--phase 1` or `--phase 1,2,3` or `--phase 1-3` |
| `--tasks <id>` | Implement specific task(s) | `--tasks T001` or `--tasks T001,T002` or `--tasks T001-T010` |

### Resume Options

| Option | Description |
|--------|-------------|
| `--resume` | Resume from last checkpoint |

---

## Examples

See [IMPLEMENT_TASKS_DETAILED_GUIDE.md](../../IMPLEMENT_TASKS_DETAILED_GUIDE.md) for comprehensive examples and use cases.

### Quick Examples

**Implement all pending tasks (default):**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md
```

**Force re-implement all:**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --force-all
```

**Implement specific phase:**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 2
```

**Resume from checkpoint:**
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume
```

---

## How `--skip-completed` Works

### Default Behavior

By default, the workflow uses `--skip-completed` mode:

**tasks.md:**
```markdown
- [x] T001: Setup project (4h)     ← Completed - SKIP
- [x] T002: Configure TypeScript (2h) ← Completed - SKIP
- [ ] T003: Setup database (3h)    ← Pending - IMPLEMENT
- [ ] T004: Create models (4h)     ← Pending - IMPLEMENT
```

**Result:**
- Skip: T001, T002 (already completed)
- Implement: T003, T004 (pending)

### Benefits

1. ✅ **Save time** - Don't re-implement completed tasks
2. ✅ **Continue work** - Stop and resume anytime
3. ✅ **Incremental development** - Add new tasks without affecting old ones
4. ✅ **Parallel work** - Multiple developers can work together
5. ✅ **Safe to re-run** - Run workflow multiple times safely

---

## Validation

After implementing each task, the workflow runs validation commands:

1. **TypeScript compiler:** `tsc --noEmit`
2. **Tests:** `npm test -- {test_file}`
3. **Linter:** `npm run lint`

If validation fails:
- ❌ Rollback changes
- ❌ Mark task as failed
- ❌ Stop or continue based on settings

---

## Checkpoint & Resume

The workflow saves progress to `.smartspec-checkpoint.json`:

```json
{
  "timestamp": "2025-01-04T14:30:22Z",
  "last_completed_task": "T015",
  "next_task": "T016",
  "completed_tasks": ["T001", ..., "T015"],
  "failed_tasks": ["T010"]
}
```

Resume from checkpoint:
```bash
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --resume
```

---

## Best Practices

1. ✅ Use `--skip-completed` as default
2. ✅ Check tasks immediately after implementation
3. ✅ Use `--resume` when workflow stops
4. ✅ Use `--phase` for incremental development
5. ✅ Use `--force-all` only when necessary
6. ✅ Validate before commit

---

## Related Workflows

- **[Generate Tasks](./generate_tasks.md)** - Create tasks.md from spec.md
- **[Verify Tasks Progress](./verify_tasks_progress.md)** - Check implementation progress
- **[Fix Errors](./fix_errors.md)** - Auto-fix compilation/type errors
- **[Generate Tests](./generate_tests.md)** - Generate test files
- **[Refactor Code](./refactor_code.md)** - Improve code quality

---

## Full Documentation

For detailed explanation, examples, and use cases, see:
📚 **[IMPLEMENT_TASKS_DETAILED_GUIDE.md](../../IMPLEMENT_TASKS_DETAILED_GUIDE.md)**
