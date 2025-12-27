# smartspec_validate_naming_convention

Validate naming convention compliance for all files in project.

## Purpose

**Problem:** No automated way to check if files follow naming convention standard.

**Solution:** Automated validation tool that:
- Scans all TypeScript/JavaScript files
- Checks naming convention compliance
- Reports violations with clear guidance
- Auto-fixes common violations
- Integrates with Git pre-commit hooks

## Usage

```bash
/smartspec_validate_naming_convention [--dir DIR] [--fix] [--json] [--staged-only]
```

## Parameters

- `--dir DIR`: Validate specific directory only (optional, default: entire project)
- `--fix`: Auto-fix violations (optional)
- `--json`: Output JSON format (optional, default: markdown)
- `--staged-only`: Validate staged files only (optional, for pre-commit hook)
- `--save-report`: Save report to file (optional)

## Examples

### Validate Entire Project

```bash
/smartspec_validate_naming_convention
```

**Output:**
```
🔍 Validating naming convention...

# Naming Convention Validation Report

**Generated:** 2025-12-27 14:30:00
**Total files:** 245
**Violations:** 12
**Compliance rate:** 95.1%

## ❌ Violations Found

### Errors (8)

**packages/auth-lib/src/services/userService.ts**
- ❌ **case:** Not kebab-case: userService.ts
  - Expected: `user-service.ts`

... (more violations)

## 🔧 How to Fix

```bash
# Auto-fix violations
/smartspec_validate_naming_convention --fix
```
```

### Validate Specific Directory

```bash
/smartspec_validate_naming_convention --dir packages/auth-lib
```

### Auto-fix Violations

```bash
/smartspec_validate_naming_convention --fix
```

**Output:**
```
🔍 Validating naming convention...

🔧 Auto-fixing 12 violations...
✅ Fixed: packages/auth-lib/src/services/userService.ts → user-service.ts
✅ Fixed: packages/auth-lib/src/providers/smsProvider.ts → sms-provider.ts
... (more fixes)
✅ Fixed 12/12 violations

🔍 Re-validating...

✅ No violations found!
```

### Validate Staged Files (Pre-commit)

```bash
/smartspec_validate_naming_convention --staged-only
```

**Output:**
```
✅ All 5 staged files follow naming convention
```

Or if violations found:
```
❌ Found 2 naming convention violation(s) in staged files:

  packages/auth-lib/src/services/userService.ts
    - Not kebab-case: userService.ts

To fix: /smartspec_validate_naming_convention --fix
```

### Generate JSON Report

```bash
/smartspec_validate_naming_convention --json
```

**Output:**
```json
{
  "total_files": 245,
  "violations": 12,
  "compliance_rate": 0.951,
  "results": [
    {
      "file": "packages/auth-lib/src/services/userService.ts",
      "compliant": false,
      "issues": [
        {
          "type": "case",
          "severity": "error",
          "message": "Not kebab-case: userService.ts",
          "expected": "user-service.ts",
          "actual": "userService.ts"
        }
      ],
      "fixes": [
        {
          "type": "rename",
          "from": "userService.ts",
          "to": "user-service.ts"
        }
      ],
      "file_type": "service"
    }
  ]
}
```

## What It Checks

### 1. **Case Convention**

**Rule:** Files must use kebab-case

**Examples:**
```
✅ PASS:
- user-service.ts
- sms-provider.ts
- jwt-util.ts

❌ FAIL:
- userService.ts (camelCase)
- SMSProvider.ts (PascalCase)
- user_service.ts (snake_case)
```

### 2. **File Suffixes**

**Rule:** Files must have appropriate suffixes

**Examples:**
```
✅ PASS:
- user-service.ts (.service.ts)
- sms-provider.ts (.provider.ts)
- jwt-util.ts (.util.ts)

⚠️  WARNING:
- user.ts (no suffix)
- sms.ts (no suffix)
```

### 3. **Directory Placement**

**Rule:** Files should be in correct directories

**Examples:**
```
✅ PASS:
- services/user-service.ts
- providers/sms-provider.ts
- utils/jwt-util.ts

⚠️  WARNING:
- integrations/sms-provider.ts (should be providers/)
- lib/jwt-util.ts (should be utils/)
```

## Validation Rules

### Severity Levels

| Severity | Description | Action |
|:---------|:------------|:-------|
| **error** | Must be fixed | Blocks commit (pre-commit hook) |
| **warning** | Should be fixed | Allows commit but reports |

### Auto-fix Support

| Issue Type | Auto-fix | Description |
|:-----------|:---------|:------------|
| **case** | ✅ Yes | Rename to kebab-case |
| **suffix** | ❌ No | Manual decision required |
| **directory** | ❌ No | Manual decision required |

### Skipped Files

**Framework files are skipped:**
- `index.ts`, `index.js`
- `main.ts`, `app.ts`
- `server.ts`

**Directories are excluded:**
- `node_modules/`
- `dist/`, `build/`
- `.git/`
- `coverage/`

## Integration with Git

### Pre-commit Hook

**Install:**
```bash
bash .smartspec/scripts/install_hooks.sh
```

**What it does:**
1. Validates staged files before commit
2. Blocks commit if violations found
3. Shows clear error messages
4. Suggests how to fix

**Bypass (not recommended):**
```bash
git commit --no-verify
```

### Typical Workflow

```bash
# 1. Make changes
vim packages/auth-lib/src/services/user-service.ts

# 2. Stage files
git add packages/auth-lib/src/services/user-service.ts

# 3. Commit (hook runs automatically)
git commit -m "feat: Add user service"

# If violations found:
🔍 Validating naming convention for staged files...
❌ Found 1 naming convention violation(s) in staged files:
  packages/auth-lib/src/services/userService.ts
    - Not kebab-case: userService.ts

# 4. Fix violations
/smartspec_validate_naming_convention --fix

# 5. Stage fixes and commit again
git add packages/auth-lib/src/services/user-service.ts
git commit -m "feat: Add user service"

# Success!
🔍 Validating naming convention for staged files...
✅ All 1 staged files follow naming convention
```

## Output Formats

### Markdown (Default)

Human-readable report with:
- Summary statistics
- Violations grouped by severity
- Clear fix instructions

**Use when:**
- Running manually
- Reviewing violations
- Sharing with team

### JSON

Machine-readable format with:
- Structured data
- All violation details
- Programmatic access

**Use when:**
- CI/CD integration
- Automated processing
- Metrics collection

## Reports

### Save Report

```bash
/smartspec_validate_naming_convention --save-report
```

**Location:** `.spec/reports/naming-convention/validation_YYYYMMDD_HHMMSS.md`

**Contents:**
- Validation results
- All violations
- Fix suggestions
- Compliance rate

## When to Use

### Use This Workflow When:

1. **Before Committing**
   - Validate staged files
   - Ensure compliance
   - Fix violations

2. **During Code Review**
   - Check PR compliance
   - Validate new files
   - Enforce standards

3. **Project Audit**
   - Check entire project
   - Measure compliance rate
   - Identify problem areas

4. **After Refactoring**
   - Validate renamed files
   - Ensure consistency
   - Fix bulk violations

5. **CI/CD Pipeline**
   - Automated validation
   - Block non-compliant PRs
   - Track compliance metrics

## Benefits

### 1. **Prevention**

- Catch violations before commit
- Enforce standards automatically
- Reduce manual review time

### 2. **Consistency**

- All files follow same convention
- Clear, unambiguous rules
- Automated enforcement

### 3. **Automation**

- No manual checking needed
- Auto-fix common violations
- Integrate with Git workflow

### 4. **Visibility**

- Clear compliance metrics
- Detailed violation reports
- Track improvements over time

## Limitations

- Only validates file names and locations
- Cannot validate file contents
- Auto-fix limited to case conversion
- Requires manual review for ambiguous cases

## Related Workflows

- `/smartspec_enrich_tasks` - Add naming convention to tasks
- `/smartspec_fix_naming_issues` - Fix naming issues in evidence paths
- `/smartspec_verify_tasks_progress_strict` - Verify task completion

## Implementation

**Script:** `.smartspec/scripts/validate_naming_convention.py`  
**Hook:** `.smartspec/hooks/pre-commit-naming-convention`  
**Install:** `.smartspec/scripts/install_hooks.sh`  
**Language:** Python 3.11+  
**Dependencies:** None (uses only standard library)

## Version

**Version:** 1.0.0  
**Created:** 2025-12-27  
**Status:** Stable

## Notes

- Fast execution (<5 seconds for typical project)
- Safe to run multiple times
- Non-destructive without `--fix` flag
- Git-friendly (works with staged files)

## Future Enhancements

- [ ] Support for custom naming rules
- [ ] IDE integration (ESLint plugin)
- [ ] Auto-fix for directory placement
- [ ] Suggest appropriate suffixes
- [ ] Learning from user corrections
- [ ] Metrics dashboard
