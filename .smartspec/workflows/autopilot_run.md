# Autopilot Run - Next Workflow Recommendation

Get intelligent workflow recommendation from Orchestrator Agent based on current spec state.

## Purpose

This workflow analyzes the current state of a spec and recommends the next workflow to run, along with the exact command to execute.

**What it does:**
- Reads current state (spec, plan, tasks, implementation status)
- Determines development phase (spec → plan → tasks → implement → sync → verify)
- Recommends appropriate workflow
- Builds complete command with correct flags
- Provides tips and warnings

## Usage

```bash
/autopilot_run.md <spec-id> [--auto] --platform <kilo|antigravity|claude>
```

## Parameters

| Parameter | Required | Description | Example |
|:---|:---:|:---|:---|
| `<spec-id>` | Yes | Spec ID to analyze | `spec-core-001-authentication` |
| `--auto` | No | Auto-continue without confirmation | (flag) |
| `--platform` | Yes | Platform (kilo/antigravity/claude) | `kilo` |

## Examples

### Example 1: Get recommendation

```bash
/autopilot_run.md spec-core-001-authentication --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_implement_tasks  
**Reason:** Continue implementation (5/12 tasks completed, 42%)  
**Priority:** high  
**Estimated Time:** 140 minutes

## Current State

- ✅ spec.md exists
- ✅ plan.md exists
- ✅ tasks.md exists (12 tasks)
- ⚠️  Implementation in progress (5/12 completed)

## Next Step

Continue implementing remaining tasks.

## ⚠️  Warnings

- Checkboxes might not match actual code (consider syncing first)

## 💡 Tips

- Run sync_tasks_checkboxes if unsure about progress
- Focus on one task at a time
- Test after each task

## 🚀 Command

```bash
/smartspec_implement_tasks.md \
  specs/spec-core-001-authentication/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-core-001-authentication \
  --json \
  --platform kilo
```

**Run this command?** [y/N]
```

### Example 2: Auto-continue mode

```bash
/autopilot_run.md spec-core-001-authentication --auto --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

Workflow: smartspec_implement_tasks
Reason: Continue implementation

✅ Command ready to execute!

/smartspec_implement_tasks.md \
  specs/spec-core-001-authentication/tasks.md \
  --apply \
  --out .spec/reports/implement-tasks/spec-core-001-authentication \
  --json \
  --platform kilo
```

(Skips confirmation prompt)

### Example 3: Starting from scratch

```bash
/autopilot_run.md spec-core-003-new-feature --platform kilo
```

**Output:**
```
🤖 Orchestrator Agent

## Recommendation

**Workflow:** smartspec_generate_spec  
**Reason:** No spec.md found - need to generate specification first  
**Priority:** critical  
**Estimated Time:** 30 minutes

## Current State

- ❌ spec.md not found
- ❌ plan.md not found
- ❌ tasks.md not found

## Next Step

Generate specification document first.

## 🚀 Command

```bash
/smartspec_generate_spec.md \
  "Create authentication system with JWT tokens" \
  --out specs/spec-core-003-new-feature/spec.md \
  --json \
  --platform kilo
```
```

## Implementation

This workflow calls the Orchestrator Agent which knows all 59 SmartSpec workflows.

### Internal Process

1. **Read current state**
   ```python
   state = {
       "has_spec": exists("specs/<spec-id>/spec.md"),
       "has_plan": exists("specs/<spec-id>/plan.md"),
       "has_tasks": exists("specs/<spec-id>/tasks.md"),
       "tasks_completed": count_completed_tasks(),
       "tasks_total": count_total_tasks(),
       "implementation_status": "NOT_STARTED|IN_PROGRESS|COMPLETED"
   }
   ```

2. **Determine next workflow**
   ```python
   if not state["has_spec"]:
       return "smartspec_generate_spec"
   elif not state["has_plan"]:
       return "smartspec_generate_plan"
   elif not state["has_tasks"]:
       return "smartspec_generate_tasks"
   elif state["implementation_status"] == "IN_PROGRESS":
       if state["needs_sync"]:
           return "smartspec_sync_tasks_checkboxes"
       else:
           return "smartspec_implement_tasks"
   elif state["implementation_status"] == "COMPLETED":
       return "smartspec_verify_implementation"
   ```

3. **Build command**
   ```python
   command = build_workflow_command(
       workflow=recommended_workflow,
       spec_id=spec_id,
       platform=platform,
       additional_flags=get_recommended_flags()
   )
   ```

4. **Format output**
   - Show recommendation with reasoning
   - Show current state
   - Show warnings and tips
   - Show exact command to run

5. **Optional: Execute**
   - If `--auto` flag: execute immediately
   - Otherwise: ask for confirmation

### Workflow Knowledge

The Orchestrator Agent knows **all 59 SmartSpec workflows** including:

**Core Development Loop (10 workflows):**
1. `smartspec_generate_spec` - Generate specification
2. `smartspec_generate_plan` - Generate implementation plan
3. `smartspec_generate_tasks` - Generate task list
4. `smartspec_implement_tasks` - Implement tasks
5. `smartspec_sync_tasks_checkboxes` - Sync task progress
6. `smartspec_verify_implementation` - Verify implementation
7. `smartspec_generate_tests` - Generate tests
8. `smartspec_run_tests` - Run tests
9. `smartspec_generate_docs` - Generate documentation
10. `smartspec_deploy` - Deploy to environment

**Plus 49 other workflows** for specific scenarios.

### Decision Logic

The Orchestrator uses a state machine to determine next workflow:

```
START → has_spec? → NO → generate_spec
                 ↓ YES
              has_plan? → NO → generate_plan
                 ↓ YES
              has_tasks? → NO → generate_tasks
                 ↓ YES
           implementation? → NOT_STARTED → implement_tasks
                 ↓ IN_PROGRESS
              needs_sync? → YES → sync_tasks_checkboxes
                 ↓ NO
           completion_rate? → < 100% → implement_tasks
                 ↓ 100%
              has_tests? → NO → generate_tests
                 ↓ YES
           tests_passing? → NO → fix_tests
                 ↓ YES
              has_docs? → NO → generate_docs
                 ↓ YES
              deployed? → NO → deploy
                 ↓ YES
                 DONE
```

## File Paths

**Input files (read):**
- `specs/<spec-id>/spec.md` - Specification
- `specs/<spec-id>/plan.md` - Implementation plan
- `specs/<spec-id>/tasks.md` - Task list
- `.spec/reports/implement-tasks/<spec-id>/` - Implementation reports

**Output files (write):**
- None (output to stdout/IDE chat only)

## Error Handling

**If spec directory not found:**
```
❌ Error: Spec directory 'specs/spec-core-001' not found

**Did you mean:**
- spec-core-001-authentication
- spec-core-002-authorization

**Or create new spec:**
/smartspec_generate_spec.md "your feature description" --platform kilo
```

## Notes

### Requirements

- **Python 3.11+** required
- **Multi-Agent System** installed in `.smartspec/ss_autopilot/`
- **Workflow catalog** loaded (59 workflows)

### Performance

- **Response time:** < 1 second (typical)
- **File reads:** 3-5 files (spec, plan, tasks, reports)
- **No network calls**

### Limitations

- Basic recommendation logic (will be enhanced with LLM in Phase 2)
- Doesn't verify actual code (only reads tasks.md checkboxes)
- No error recovery (Phase 2)
- No workflow history tracking (Phase 2)

### Tips

- Run this whenever you're unsure what to do next
- Use `--auto` for continuous development (be careful!)
- Combine with `/autopilot_status.md` to check progress first
- Trust the recommendation - it knows all 59 workflows!

## Related Workflows

- `/autopilot_status.md` - Check current progress
- `/autopilot_ask.md` - Natural language query
- All 59 SmartSpec workflows (can be recommended)

## Troubleshooting

### Issue: "Spec not found"

**Solution:** Create spec first or check spelling:
```bash
/smartspec_generate_spec.md "your feature" --platform kilo
```

### Issue: "Recommendation doesn't make sense"

**Solution:** Check current state first:
```bash
/autopilot_status.md <spec-id> --platform kilo
```

Then sync checkboxes if needed:
```bash
/smartspec_sync_tasks_checkboxes.md \
  specs/<spec-id>/tasks.md \
  --apply \
  --platform kilo
```

### Issue: "Workflow execution failed"

**Solution:** Check error message and:
1. Verify all input files exist
2. Check file permissions
3. Run with `--validate-only` first
4. Contact support if issue persists

## Version History

- **v2.0** (2025-12-25) - Initial release with Orchestrator Agent
