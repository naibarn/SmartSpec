# smartspec_enrich_tasks

Enrich existing tasks.md with detailed specifications, naming conventions, and architectural guidance.

## Purpose

**Problem:** Existing tasks.md files lack detailed specifications, making implementation inconsistent and causing naming issues.

**Solution:** Automatically enrich tasks with:
- Naming convention guidance
- Architectural context
- Implementation notes
- Clear file placement rules

## Usage

```bash
/smartspec_enrich_tasks \
  <tasks.md> \
  [--add-naming-convention] \
  [--add-architecture] \
  [--preview|--apply]
```

## Parameters

- `<tasks.md>`: Path to tasks.md file (required)
- `--add-naming-convention`: Add naming convention guidance (optional, default: yes)
- `--add-architecture`: Add architectural guidance (optional, default: yes)
- `--preview`: Preview mode - show what would be changed (default)
- `--apply`: Apply enrichments to tasks.md

## Examples

### Preview Enrichments (Default)

```bash
/smartspec_enrich_tasks \
  specs/core/spec-core-001-authentication/tasks.md \
  --preview
```

### Apply Enrichments

```bash
/smartspec_enrich_tasks \
  specs/core/spec-core-001-authentication/tasks.md \
  --apply
```

### Add Only Naming Convention

```bash
/smartspec_enrich_tasks \
  specs/core/spec-core-001-authentication/tasks.md \
  --add-naming-convention \
  --apply
```

### Add Only Architecture

```bash
/smartspec_enrich_tasks \
  specs/core/spec-core-001-authentication/tasks.md \
  --add-architecture \
  --apply
```

## What It Does

### 1. **Analyzes Evidence Paths**

Parses tasks.md and extracts evidence paths:

```markdown
### TSK-AUTH-057: Integrate SMS provider

**Evidence:**
- code: packages/auth-lib/src/integrations/sms.provider.ts
```

### 2. **Checks Naming Convention Compliance**

Validates against naming convention standard:
- ✅ kebab-case
- ✅ Correct suffix
- ✅ Correct directory
- ✅ Correct package

### 3. **Adds Architecture Section**

Adds architectural context:

```markdown
**Architecture:**
- **Package:** `auth-lib` (Shared code, utilities, models)
- **Directory:** `providers/` (External integrations)
- **Naming:** `sms-provider.ts` (kebab-case + provider suffix)
```

### 4. **Adds Naming Convention Section**

Adds naming convention guidance:

```markdown
**Naming Convention:**
- ✅ Use kebab-case: `sms-provider.ts` (correct)
- ✅ Use provider suffix: `.provider.ts` for external integrations
- ✅ Place in providers/: External service integrations

**Implementation Notes:**
- Follow naming convention strictly
- Create file at exact path specified
- Do not rename or move files without updating tasks.md
```

### 5. **Generates Report**

Creates detailed report:
- Tasks enriched
- Naming convention compliance
- Suggestions for improvement

## Example Transformation

### Before Enrichment

```markdown
### TSK-AUTH-057: Integrate SMS provider

**Evidence:**
- code: packages/auth-lib/src/integrations/sms.provider.ts
- test: packages/auth-lib/tests/unit/sms.provider.test.ts
```

### After Enrichment

```markdown
### TSK-AUTH-057: Integrate SMS provider

**Architecture:**
- **Package:** `auth-lib` (Shared code, utilities, models)
- **Directory:** `providers/` (External integrations)
- **Naming:** `sms-provider.ts` (kebab-case + provider suffix)

**Naming Convention:**
- ⚠️ Use kebab-case: `sms.provider.ts` should be `sms-provider.ts`
- ✅ Use provider suffix: `.provider.ts` for external integrations
- ⚠️ Place in providers/: Currently in `integrations/`, should be `providers/`

**Implementation Notes:**
- Follow naming convention strictly
- Create file at exact path specified
- Do not rename or move files without updating tasks.md

**Evidence:**
- code: packages/auth-lib/src/providers/sms-provider.ts
- test: packages/auth-lib/tests/unit/providers/sms-provider.test.ts
```

**Note:** The tool also suggests corrections to evidence paths if they don't follow naming convention.

## Output

### Console Output

```
📖 Reading tasks: specs/core/spec-core-001-authentication/tasks.md
📋 Found 152 tasks
🔧 Enriching tasks...
   ✓ Enriched TSK-AUTH-001: Setup authentication module
   ✓ Enriched TSK-AUTH-002: Implement JWT utilities
   ✓ Enriched TSK-AUTH-057: Integrate SMS provider
   ... (149 more)

✅ Enriched 152 tasks
✅ Applied enrichments to specs/core/spec-core-001-authentication/tasks.md

📄 Report saved: .spec/reports/tasks-enrichment/spec-core-001-authentication/enrichment_20251227_143000.md
```

### Report Contents

```markdown
# Tasks Enrichment Report

**Generated:** 2025-12-27 14:30:00
**Tasks File:** `specs/core/spec-core-001-authentication/tasks.md`
**Status:** ✅ Applied

---

## Summary

- **Total tasks enriched:** 152
- **Added naming convention:** Yes
- **Added architecture:** Yes
- **Changes applied:** Yes

## Enrichments Made

### TSK-AUTH-057: Integrate SMS provider

**Evidence:** `packages/auth-lib/src/integrations/sms.provider.ts`

**Status:** ⚠️ Needs attention

**Suggestions:**
- Use kebab-case for filename
- Place in providers/ directory instead of integrations/

---

... (more tasks)

## Next Steps

1. **Review enriched tasks:**
   ```bash
   cat specs/core/spec-core-001-authentication/tasks.md
   ```

2. **Verify changes:**
   ```bash
   git diff specs/core/spec-core-001-authentication/tasks.md
   ```

3. **Commit changes:**
   ```bash
   git add tasks.md
   git commit -m "docs: Enrich tasks with naming convention and architecture"
   ```
```

## When to Use

### Use This Workflow When:

1. **Migrating Existing Projects**
   - Have existing tasks.md without detailed specs
   - Want to add naming convention guidance
   - Need architectural context

2. **After Creating New Spec**
   - Generated tasks.md with basic structure
   - Want to add detailed specifications
   - Prepare for implementation

3. **Before Batch Execution**
   - Ensure clear guidance for implementers
   - Reduce naming issues
   - Improve consistency

4. **Updating Old Tasks**
   - Tasks created before naming convention standard
   - Need to bring up to current standards
   - Want to improve clarity

### Don't Use When:

1. **Tasks Already Enriched**
   - Tool skips already enriched tasks
   - No need to run again

2. **Custom Task Format**
   - Tasks don't follow standard format
   - May not parse correctly

## Benefits

### 1. **Consistency**

- All tasks follow same format
- Clear guidance for implementers
- Reduced ambiguity

### 2. **Prevention**

- Prevent naming issues at source
- Clear rules before implementation
- Reduce verification failures

### 3. **Documentation**

- Self-documenting tasks
- Architectural context included
- Easy to understand purpose

### 4. **Automation**

- Automated enrichment process
- Batch processing of all tasks
- Consistent results

## Integration with Other Workflows

### Typical Flow

```bash
# Step 1: Generate or update tasks
/smartspec_generate_tasks \
  --spec specs/core/spec-core-001-authentication/spec.md \
  --out specs/core/spec-core-001-authentication/tasks.md

# Step 2: Enrich tasks with naming convention
/smartspec_enrich_tasks \
  specs/core/spec-core-001-authentication/tasks.md \
  --apply

# Step 3: Generate implementation prompts
/smartspec_report_implement_prompter \
  --verify-report .spec/reports/verify-tasks-progress/latest/summary.json \
  --tasks specs/core/spec-core-001-authentication/tasks.md

# Step 4: Execute prompts
/smartspec_execute_prompts_batch \
  --prompts-dir .spec/prompts/latest/ \
  --tasks specs/core/spec-core-001-authentication/tasks.md

# Step 5: Verify
/smartspec_verify_tasks_progress_strict \
  specs/core/spec-core-001-authentication/tasks.md \
  --json
```

## Safety Features

1. **Preview by Default** - Must explicitly use `--apply`
2. **Skip Already Enriched** - Won't duplicate enrichments
3. **Non-Destructive** - Only adds information, doesn't remove
4. **Git-Friendly** - Changes are easy to review with `git diff`
5. **Report Generation** - Detailed report of all changes

## Limitations

- Only enriches tasks with evidence paths
- Assumes standard task format
- Requires naming convention standard to be present
- May need manual adjustment for edge cases

## Related Workflows

- `/smartspec_generate_tasks` - Generate tasks from spec
- `/smartspec_verify_tasks_progress_strict` - Verify task completion
- `/smartspec_fix_naming_issues` - Fix naming issues in evidence paths

## Implementation

**Script:** `.smartspec/scripts/enrich_tasks.py`  
**Language:** Python 3.11+  
**Dependencies:** None (uses only standard library)

## Version

**Version:** 1.0.0  
**Created:** 2025-12-27  
**Status:** Stable

## Notes

- Always preview first to check what will be changed
- Review enrichments before committing
- Can be run multiple times safely (skips already enriched)
- Integrates with naming convention standard

## Future Enhancements

- [ ] Add examples to tasks
- [ ] Add related tasks links
- [ ] Add implementation complexity estimates
- [ ] Add dependency information
- [ ] Interactive mode for ambiguous cases
