# smartspec_fix_naming_issues

Fix naming issues by automatically updating evidence paths in tasks.md based on verification report findings.

## Usage

```bash
/smartspec_fix_naming_issues \
  <tasks.md> \
  --from-report <report_path> \
  [--apply]
```

## Parameters

- `<tasks.md>`: Path to tasks.md file (required)
- `--from-report`: Path to verification report (JSON or Markdown) (required)
- `--apply`: Apply changes immediately (optional, default: preview only)

## Examples

### Preview Changes

```bash
/smartspec_fix_naming_issues \
  specs/core/spec-core-001-authentication/tasks.md \
  --from-report .spec/reports/batch-execution/batch_execution_20251226_174500.md
```

### Apply Changes

```bash
/smartspec_fix_naming_issues \
  specs/core/spec-core-001-authentication/tasks.md \
  --from-report .spec/reports/batch-execution/batch_execution_20251226_174500.md \
  --apply
```

### From JSON Report

```bash
/smartspec_fix_naming_issues \
  specs/core/spec-core-001-authentication/tasks.md \
  --from-report .spec/reports/verify-tasks-progress/spec-core-001-authentication/summary.json \
  --apply
```

## What It Does

1. **Reads verification report** (JSON or Markdown format)
2. **Extracts naming issues** with expected vs found paths
3. **Updates evidence paths** in tasks.md to match actual files
4. **Preview mode** (default): Shows what would be changed
5. **Apply mode** (`--apply`): Makes actual changes to tasks.md

## Output

### Preview Mode (Default)

```
================================================================================
PREVIEW: Evidence Path Updates
================================================================================

1. Line 123:
   Expected: packages/auth-lib/src/crypto/password.util.ts
   Found:    packages/auth-lib/src/crypto/password.ts
   Old: evidence: code path=packages/auth-lib/src/crypto/password.util.ts
   New: evidence: code path=packages/auth-lib/src/crypto/password.ts

2. Line 456:
   Expected: packages/auth-lib/tests/unit/jwt.util.test.ts
   Found:    packages/auth-lib/tests/unit/edge-cases/jwt.util.edge-cases.test.ts
   Old: evidence: test path=packages/auth-lib/tests/unit/jwt.util.test.ts
   New: evidence: test path=packages/auth-lib/tests/unit/edge-cases/jwt.util.edge-cases.test.ts

================================================================================
Total changes: 52
================================================================================

ℹ️  This is preview mode. Use --apply to make changes.
```

### Apply Mode (`--apply`)

```
================================================================================
✅ APPLIED: Evidence Path Updates
================================================================================

Total changes applied: 52
File updated: specs/core/spec-core-001-authentication/tasks.md

Next steps:
1. Verify changes:
   /smartspec_verify_tasks_progress_strict specs/core/spec-core-001-authentication/tasks.md --json

2. Review diff:
   git diff specs/core/spec-core-001-authentication/tasks.md

3. Commit changes:
   git add tasks.md
   git commit -m "fix: Update evidence paths to match actual files"

================================================================================
```

## When to Use

Use this workflow when:

1. **After batch execution** - Many naming issues remain
2. **After refactoring** - Files were renamed or moved
3. **After verification** - Evidence paths don't match actual files
4. **Bulk updates needed** - 10+ naming issues to fix

## Workflow Integration

### Typical Flow

```bash
# Step 1: Generate prompts for critical issues
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify-tasks-progress/spec-core-001-authentication/summary.json \
  --tasks specs/core/spec-core-001-authentication/tasks.md \
  --priority 1 \
  --out .spec/prompts/spec-core-001-authentication/critical

# Step 2: Execute prompts in batch
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/spec-core-001-authentication/critical/20251226_164500/ \
  --tasks specs/core/spec-core-001-authentication/tasks.md \
  --checkpoint

# Step 3: Fix remaining naming issues
/smartspec_fix_naming_issues \
  specs/core/spec-core-001-authentication/tasks.md \
  --from-report .spec/reports/batch-execution/batch_execution_20251226_174500.md \
  --apply

# Step 4: Verify all fixes
/smartspec_verify_tasks_progress_strict \
  specs/core/spec-core-001-authentication/tasks.md \
  --json
```

## Safety Features

1. **Preview by default** - Must explicitly use `--apply`
2. **Line-by-line changes** - Shows exactly what will change
3. **No data loss** - Only updates evidence paths, doesn't delete anything
4. **Git-friendly** - Changes are easy to review with `git diff`

## Limitations

- Only fixes naming issues (evidence path mismatches)
- Doesn't create missing files
- Doesn't fix implementation issues
- Requires verification report as input

## Related Workflows

- `/smartspec_verify_tasks_progress_strict` - Generate verification report
- `/smartspec_execute_prompts_batch` - Execute implementation prompts
- `/smartspec_report_implement_prompter` - Generate prompts from verification

## Notes

- Always review changes before committing
- Use preview mode first to check what will be changed
- Naming issues are governance problems, not implementation problems
- This workflow is safe - it only updates text in tasks.md

## Implementation

**Script:** `.smartspec/scripts/fix_naming_issues.py`  
**Language:** Python 3.11+  
**Dependencies:** None (uses only standard library)

## Version

**Version:** 1.0.0  
**Created:** 2025-12-27  
**Status:** Stable
