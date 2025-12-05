---
description: Fix compilation errors, type errors, and runtime errors automatically
globs: ["specs/**/*.md", "src/**/*.ts", "src/**/*.tsx"]
---

# Fix Compilation and Runtime Errors

You are an expert code debugger and error fixer. Your task is to automatically detect and fix compilation errors, type errors, and runtime errors in the codebase.

## Input

You will receive:
1. **Spec Directory Path** - Path to the spec directory (e.g., `specs/feature/spec-004-financial-system`)
2. **Options** (optional):
   - `--file <path>` - Fix errors in specific file only
   - `--severity <level>` - Fix only errors of specific severity (critical, high, medium, low)
   - `--auto-fix` - Auto-fix all errors without asking
   - `--dry-run` - Show what would be fixed without actually fixing
   - `--kilocode` - Use Kilo Code Orchestrator Mode with Debug Mode for systematic error fixing

## Your Task

### Phase 1: Detect Errors

1. **Load SPEC_INDEX.json**
   ```bash
   cat .smartspec/SPEC_INDEX.json
   ```
   - Parse JSON to get spec metadata
   - Extract `spec.files[]` array for the given spec_id
   - If `--file` option provided, use only that file
   - Otherwise, use all files from `spec.files[]`
   - **SCOPE**: Only scan files listed in spec.files[] (not entire project!)

2. **Read Progress Report**
   - Look for `progress-report-*.md` in the spec directory
   - Extract all reported errors
   - Filter errors to only those in scoped files

3. **Run TypeScript Compiler (scoped)**
   ```bash
   cd <project-root>
   # Only check files in scope
   npx tsc --noEmit --pretty false <file1> <file2> ... 2>&1
   ```
   - Parse compilation errors
   - Extract file paths, line numbers, error codes, and messages
   - **Only process errors from scoped files**

4. **Run ESLint (scoped)**
   ```bash
   # Only lint files in scope
   npx eslint <file1> <file2> ... --format json 2>&1
   ```
   - Parse linting errors
   - Filter only errors (not warnings)
   - **Only process errors from scoped files**

5. **Categorize Errors by Severity**
   - **CRITICAL**: Compilation errors that prevent build
   - **HIGH**: Type errors that may cause runtime errors
   - **MEDIUM**: Linting errors that should be fixed
   - **LOW**: Warnings and minor issues

6. **Display Error Summary**
   ```
   🔍 Found X errors:
     CRITICAL: X errors
     HIGH: X errors
     MEDIUM: X errors
     LOW: X errors
   ```

### Phase 2: Analyze Errors

For each error:

1. **Read Context**
   - Read the file containing the error
   - Extract 10 lines before and after the error line
   - Analyze imports and dependencies

2. **Identify Root Cause**
   - Type mismatch → need type cast or type definition change
   - Missing import → need to add import statement
   - Undefined variable → need to declare variable
   - Wrong function signature → need to fix parameters or return type

3. **Create Fix Strategy**
   - Determine the fix type (type cast, add import, rename, etc.)
   - Calculate confidence level (0-100%)
   - Prepare the exact code changes needed

4. **Display Proposed Fixes**
   ```
   Found X errors to fix:
   
   CRITICAL (X):
   ✗ src/services/example.service.ts:45
     TS2345: Argument type mismatch
     Fix: Cast userId to number using parseInt()
     Confidence: 95%
   
   [Show all proposed fixes]
   ```

### Phase 3: Apply Fixes

**If `--kilocode` flag: Use Kilo Code Debug Mode**

```
Use Debug Mode to analyze and fix all errors systematically.
```

**Debug Mode will:**
- Analyze all errors systematically
- Identify root causes
- Apply fixes one by one
- Verify each fix
- Rollback if fix creates new errors
- Report progress

**If NOT using `--kilocode`:**

1. **Ask User for Confirmation** (unless `--auto-fix`)
   ```
   Fix all errors? (y/n/s)
   y = Yes, fix all
   n = No, skip all  
   s = Select which to fix
   ```

2. **Backup Original Files**
   - Create `.backup` files before making changes
   - Store backup timestamp

3. **Apply Fixes One by One**
   - Make the code changes
   - Verify syntax after each fix
   - If fix creates new errors → rollback immediately

4. **Display Progress**
   ```
   🔧 Fixing errors...
     ✓ Fixed src/services/example.service.ts:45 (TS2345)
     ✗ Failed src/services/other.service.ts:120 (TS2339) - Rolled back
     ✓ Fixed src/utils/helper.ts:23 (unused variable)
   ```

### Phase 4: Verify Fixes

1. **Run TypeScript Compiler Again**
   ```bash
   npx tsc --noEmit
   ```
   - Check if errors are resolved
   - Check for new errors introduced

2. **Run Tests (if available)**
   ```bash
   npm test
   ```
   - Ensure tests still pass
   - If tests fail → rollback and report

3. **Display Verification Results**
   ```
   ✅ Verification:
     ✓ TypeScript compilation: PASS
     ✓ Tests: 25/25 passing
     ✓ No new errors introduced
   ```

### Phase 5: Generate Report

Create a fix report file: `<spec-dir>/fix-report-YYYYMMDD-HHMMSS.md`

```markdown
# Error Fix Report

Generated: YYYY-MM-DD HH:MM:SS

## Summary

- Total errors detected: X
- Fixed successfully: X
- Failed to fix: X
- Skipped: X

## Fixed Errors

### ✅ src/services/example.service.ts:45
- **Error**: TS2345 - Argument type mismatch
- **Fix Applied**: Cast userId to number using parseInt()
- **Status**: Success
- **Before**:
  ```typescript
  this.calculateBalance(userId)
  ```
- **After**:
  ```typescript
  this.calculateBalance(parseInt(userId))
  ```

### ❌ src/services/other.service.ts:120
- **Error**: TS2339 - Property 'amount' does not exist
- **Fix Attempted**: Add amount property to interface
- **Status**: Failed - Created new error TS2322
- **Action**: Rolled back
- **Recommendation**: Manual fix required

## Errors Requiring Manual Fix

1. src/services/other.service.ts:120 - Complex interface issue
2. [List other errors that couldn't be auto-fixed]

## Verification Results

- TypeScript Compilation: ✅ PASS
- ESLint: ✅ PASS
- Tests: ✅ 25/25 passing
- New Errors: ❌ None

## Backup Files

- src/services/example.service.ts.backup-YYYYMMDD-HHMMSS
- src/utils/helper.ts.backup-YYYYMMDD-HHMMSS

## Recommendations

- Review fixed code before committing
- Add tests for edge cases
- Consider refactoring complex functions

## Next Steps

1. Review the fixes in the modified files
2. Run full test suite
3. Commit changes if satisfied
4. Continue with task implementation
```

### Phase 6: Update Progress Report

1. **Update the progress report** with:
   - Reduced error count
   - Fix timestamp
   - Link to fix report

2. **Suggest Next Action**
   ```
   ✅ Fixed X/Y errors successfully!
   
   📊 Results:
     Fixed: X errors (XX%)
     Failed: X errors (requires manual fix)
   
   📁 Reports:
     - Fix report: <spec-dir>/fix-report-YYYYMMDD.md
     - Updated progress: <spec-dir>/progress-report-YYYYMMDD.md
   
   💡 Next Steps:
     1. Review fixed code
     2. Fix remaining errors manually (if any)
     3. Run tests: npm test
     4. Commit changes: git add . && git commit -m "fix: Auto-fix errors in spec-XXX"
   
   🔧 Suggested Workflows:
   
   ✅ Errors fixed! Consider these next actions:
   
   1. Generate tests for fixed code:
      /smartspec_generate_tests <spec-dir> --target-coverage 80
   
   2. Check code quality:
      /smartspec_refactor_code <spec-dir>
   
   3. Verify overall progress:
      /smartspec_verify_tasks_progress <spec-dir>/tasks.md
   
   4. Continue implementation:
      /smartspec_implement_tasks <spec-dir>/tasks.md --skip-completed
   ```

## Common Fix Patterns

### Type Mismatch Errors

**Pattern**: Argument of type 'X' is not assignable to parameter of type 'Y'

**Fixes**:
- Add type cast: `value as Type` or `<Type>value`
- Use conversion function: `parseInt()`, `parseFloat()`, `String()`, etc.
- Fix the type definition in interface/type

### Missing Import Errors

**Pattern**: Cannot find name 'X'

**Fixes**:
- Add import statement: `import { X } from './path'`
- Check if X is exported from the module
- Install missing package if it's from node_modules

### Undefined Variable Errors

**Pattern**: Variable 'X' is used before being assigned

**Fixes**:
- Add variable declaration: `let X: Type;` or `const X = value;`
- Initialize variable with default value
- Check if variable should be a parameter

### Property Does Not Exist Errors

**Pattern**: Property 'X' does not exist on type 'Y'

**Fixes**:
- Add property to interface/type definition
- Use optional chaining: `obj?.property`
- Add type guard to narrow type

### Unused Variable/Import Errors

**Pattern**: 'X' is declared but its value is never read

**Fixes**:
- Remove unused variable/import
- Prefix with underscore if intentionally unused: `_variable`
- Use the variable if it should be used

## Error Handling

### If Fix Creates New Errors
1. Rollback the fix immediately
2. Mark as "Failed" in report
3. Add to "Requires Manual Fix" list
4. Continue with other fixes

### If Tests Fail After Fix
1. Rollback all fixes in that file
2. Mark file as "Requires Manual Fix"
3. Continue with other files

### If Confidence < 80%
1. Skip auto-fix
2. Add to "Requires Manual Fix" list
3. Provide detailed analysis for manual fixing

## Output Format

Always provide:
1. ✅ **Summary** of what was fixed
2. 📊 **Statistics** (fixed/failed/skipped)
3. 📁 **Report file path**
4. 💡 **Next steps** recommendation

## Important Notes

- Always backup files before making changes
- Verify each fix doesn't introduce new errors
- Rollback immediately if fix fails
- Prioritize critical errors over minor issues
- Don't fix errors with confidence < 80% automatically
- Always run tests after fixing to ensure no regressions
- Create detailed reports for audit trail
- Suggest manual fixes for complex errors

## Example Usage

```bash
# Fix all errors in spec
/smartspec_fix_errors specs/feature/spec-004-financial-system

# Fix errors in specific file
/smartspec_fix_errors specs/feature/spec-004 --file src/services/credit.service.ts

# Fix only critical errors
/smartspec_fix_errors specs/feature/spec-004 --severity critical

# Auto-fix without asking
/smartspec_fix_errors specs/feature/spec-004 --auto-fix

# Dry-run (show what would be fixed)
/smartspec_fix_errors specs/feature/spec-004 --dry-run
```
