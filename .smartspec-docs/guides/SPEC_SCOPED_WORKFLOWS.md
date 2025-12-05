# Spec-Scoped Quality Workflows

## Overview

SmartSpec workflows for quality improvement (`fix_errors`, `generate_tests`, `refactor_code`) now operate on a **spec-scoped basis** instead of scanning entire projects. This dramatically improves performance in large projects with hundreds of specs.

## How It Works

### 1. SPEC_INDEX.json Structure

SmartSpec uses `SPEC_INDEX.json` to map specs to their related source files:

```json
{
  "specs": {
    "spec-004-financial-system": {
      "spec_id": "spec-004-financial-system",
      "spec_path": "specs/feature/spec-004-financial-system/spec.md",
      "tasks_path": "specs/feature/spec-004-financial-system/tasks.md",
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts",
        "src/models/transaction.model.ts",
        "src/utils/financial-calculator.ts"
      ],
      "dependencies": ["spec-001-auth", "spec-002-database"]
    }
  }
}
```

### 2. Workflow Scoping Process

When you run a quality workflow:

1. **Load SPEC_INDEX.json** - Read the spec metadata
2. **Extract spec.files[]** - Get the list of files related to this spec
3. **Apply scope** - Only analyze/modify files in the `spec.files[]` array
4. **Execute workflow** - Run tools (TypeScript, ESLint, tests) only on scoped files

### 3. Performance Benefits

**Before (Project-Wide):**
- Scan all 500+ files in project
- Run TypeScript compiler on entire codebase
- Generate tests for all services
- Time: 5-10 minutes per workflow

**After (Spec-Scoped):**
- Scan only 4-8 files related to spec
- Run TypeScript compiler on scoped files only
- Generate tests for scoped services only
- Time: 30-60 seconds per workflow

**Performance Gain:** ~10x faster ⚡

## Usage Examples

### Fix Errors (Spec-Scoped)

```bash
# Fix all errors in spec-004
/smartspec_fix_errors specs/feature/spec-004-financial-system

# Fix errors in specific file within spec
/smartspec_fix_errors specs/feature/spec-004 --file src/services/credit.service.ts

# Fix only critical errors
/smartspec_fix_errors specs/feature/spec-004 --severity critical

# Dry-run to see what would be fixed
/smartspec_fix_errors specs/feature/spec-004 --dry-run
```

**What happens:**
1. Reads `SPEC_INDEX.json` to get files for `spec-004-financial-system`
2. Runs TypeScript compiler only on: `credit.service.ts`, `payment.service.ts`, `transaction.model.ts`, `financial-calculator.ts`
3. Fixes errors only in those 4 files
4. Skips the other 496 files in the project ✅

### Generate Tests (Spec-Scoped)

```bash
# Generate tests to reach 80% coverage for spec-004
/smartspec_generate_tests specs/feature/spec-004-financial-system --target-coverage 80

# Generate tests for specific file
/smartspec_generate_tests specs/feature/spec-004 --file src/services/credit.service.ts

# Generate only unit tests
/smartspec_generate_tests specs/feature/spec-004 --type unit

# Focus on uncovered code only
/smartspec_generate_tests specs/feature/spec-004 --focus uncovered
```

**What happens:**
1. Reads `SPEC_INDEX.json` to get files for `spec-004-financial-system`
2. Runs coverage analysis only on the 4 scoped files
3. Generates tests only for uncovered code in those files
4. Skips test generation for other services ✅

### Refactor Code (Spec-Scoped)

```bash
# Refactor all code in spec-004
/smartspec_refactor_code specs/feature/spec-004-financial-system

# Refactor specific file
/smartspec_refactor_code specs/feature/spec-004 --file src/services/credit.service.ts

# Focus on reducing complexity
/smartspec_refactor_code specs/feature/spec-004 --focus complexity

# Include breaking changes (rename APIs)
/smartspec_refactor_code specs/feature/spec-004 --aggressive

# Dry-run to see what would be refactored
/smartspec_refactor_code specs/feature/spec-004 --dry-run
```

**What happens:**
1. Reads `SPEC_INDEX.json` to get files for `spec-004-financial-system`
2. Runs ESLint and complexity analysis only on the 4 scoped files
3. Detects code smells only in those files
4. Refactors only the scoped files ✅

## Workflow Comparison

| Aspect | Project-Wide (Old) | Spec-Scoped (New) |
|--------|-------------------|-------------------|
| **Scope** | Entire project (500+ files) | Spec files only (4-8 files) |
| **Performance** | 5-10 minutes | 30-60 seconds |
| **Accuracy** | Finds unrelated issues | Finds spec-related issues only |
| **Usability** | Overwhelming output | Focused, actionable output |
| **Scalability** | Poor (slows down as project grows) | Excellent (constant time per spec) |

## When to Use Each Workflow

### smartspec_fix_errors
- **When:** After implementing tasks, before committing
- **Goal:** Fix TypeScript errors, type errors, linting errors
- **Scope:** Only files in the current spec
- **Output:** Fixed files + error report

### smartspec_generate_tests
- **When:** After implementation is complete
- **Goal:** Increase test coverage to target level (default 80%)
- **Scope:** Only files in the current spec
- **Output:** Generated test files + coverage report

### smartspec_refactor_code
- **When:** After tests pass, before code review
- **Goal:** Improve code quality, reduce complexity
- **Scope:** Only files in the current spec
- **Output:** Refactored files + quality report

## Best Practices

### 1. Keep SPEC_INDEX.json Updated
Always update `SPEC_INDEX.json` when:
- Adding new files to a spec
- Moving files between specs
- Renaming files

### 2. Use Spec Identifiers
Users typically know spec identifiers better than service names:
- ✅ Good: `/smartspec_fix_errors specs/feature/spec-004-financial-system`
- ❌ Avoid: "Fix errors in CreditService" (user may not know which spec it belongs to)

### 3. Workflow Order
Recommended workflow order for quality improvement:

```bash
# 1. Fix errors first
/smartspec_fix_errors specs/feature/spec-004

# 2. Generate tests
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 80

# 3. Refactor code
/smartspec_refactor_code specs/feature/spec-004

# 4. Verify everything works
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

### 4. Use --file for Precision
For even more focused operations:

```bash
# Fix errors in one specific file
/smartspec_fix_errors specs/feature/spec-004 --file src/services/credit.service.ts

# Generate tests for one specific file
/smartspec_generate_tests specs/feature/spec-004 --file src/services/credit.service.ts

# Refactor one specific file
/smartspec_refactor_code specs/feature/spec-004 --file src/services/credit.service.ts
```

## Migration from Project-Wide to Spec-Scoped

If you were using the old project-wide approach:

**Old way (not recommended):**
```bash
# This would scan entire project - very slow!
/smartspec_fix_errors .
```

**New way (recommended):**
```bash
# Specify the spec you're working on
/smartspec_fix_errors specs/feature/spec-004-financial-system
```

## Troubleshooting

### "Cannot find SPEC_INDEX.json"
**Solution:** Make sure you have `.smartspec/SPEC_INDEX.json` in your project root. Run `/smartspec_init` to create it.

### "Spec not found in SPEC_INDEX.json"
**Solution:** The spec may not be registered yet. Add it to `SPEC_INDEX.json`:
```json
{
  "specs": {
    "your-spec-id": {
      "spec_id": "your-spec-id",
      "spec_path": "specs/feature/your-spec-id/spec.md",
      "files": [
        "src/your-service.ts"
      ]
    }
  }
}
```

### "No files in spec.files[]"
**Solution:** Update `SPEC_INDEX.json` to include the files related to your spec.

### "Workflow still scanning entire project"
**Solution:** Make sure you're using the latest version of SmartSpec workflows. Run `git pull` in the SmartSpec repository.

## Technical Details

### File Scoping Implementation

Each workflow now follows this pattern:

```typescript
// 1. Load SPEC_INDEX.json
const specIndex = JSON.parse(fs.readFileSync('.smartspec/SPEC_INDEX.json'));

// 2. Get spec metadata
const specId = extractSpecId(specDirPath); // e.g., "spec-004-financial-system"
const spec = specIndex.specs[specId];

// 3. Extract scoped files
const scopedFiles = spec.files; // e.g., ["src/services/credit.service.ts", ...]

// 4. Run tools only on scoped files
const errors = runTypeScriptCompiler(scopedFiles);
const coverage = runCoverageAnalysis(scopedFiles);
const smells = runCodeAnalysis(scopedFiles);
```

### Scope Filtering

All analysis results are filtered to only include scoped files:

```typescript
// Filter TypeScript errors
const scopedErrors = allErrors.filter(error => 
  scopedFiles.includes(error.fileName)
);

// Filter coverage data
const scopedCoverage = {
  lines: coverage.lines.filter(line => 
    scopedFiles.includes(line.fileName)
  ),
  // ...
};

// Filter code smells
const scopedSmells = allSmells.filter(smell => 
  scopedFiles.includes(smell.fileName)
);
```

## Future Enhancements

Planned improvements for spec-scoped workflows:

1. **Dependency-aware scoping** - Include files from dependent specs
2. **Cross-spec analysis** - Detect issues that span multiple specs
3. **Incremental analysis** - Only analyze changed files since last run
4. **Parallel execution** - Run workflows on multiple specs simultaneously
5. **Smart caching** - Cache analysis results for faster re-runs

## Summary

Spec-scoped workflows make SmartSpec practical for large projects by:

✅ **Focusing** on relevant files only  
✅ **Improving** performance by 10x  
✅ **Reducing** noise and overwhelming output  
✅ **Scaling** linearly with project size  
✅ **Matching** user mental model (specs, not services)  

Use spec identifiers to run workflows efficiently, even in projects with hundreds of specs!
# Updates to SPEC_SCOPED_WORKFLOWS.md

## New Section: Maintaining SPEC_INDEX.json

### Why Re-Indexing is Important

SPEC_INDEX.json can become outdated when:
- New files are added to a spec
- Files are renamed or moved
- Specs are added or removed
- External repositories are integrated
- Dependencies between specs change

**Solution:** Use `/smartspec_reindex_specs` to keep SPEC_INDEX.json accurate.

### Re-Indexing Workflows

#### Re-Index All Specs
```bash
/smartspec_reindex_specs
```

This will:
1. Scan all specs in `specs/` directory
2. Identify new, modified, and removed specs
3. Detect related files using 5 strategies
4. Update SPEC_INDEX.json
5. Generate detailed report

#### Re-Index Specific Spec
```bash
/smartspec_reindex_specs --spec specs/feature/spec-004-financial-system
```

Use this when you've modified a single spec and want to update only its entry.

#### Verify Without Changes
```bash
/smartspec_reindex_specs --verify
```

This checks SPEC_INDEX.json for issues without making changes:
- Missing files
- Outdated entries
- Circular dependencies
- Invalid JSON

#### Include External Repositories
```bash
/smartspec_reindex_specs --external-repo /path/to/shared-repo
```

For projects that share services across multiple repositories:
- Scans external repo for related files
- Adds them to `external_files[]` in SPEC_INDEX.json
- Prefixes with repo identifier (e.g., `@shared/services/auth.service.ts`)

### File Detection Strategies

The re-index workflow uses 5 strategies to find files related to each spec:

1. **Parse spec.md** - Looks for file paths in spec content
2. **Search by spec ID** - Finds files with spec ID in comments
3. **Analyze tasks.md** - Extracts file paths from task descriptions
4. **Service/Model inference** - Infers file paths from service/model names
5. **Git history** - Finds files modified around the same time as spec

### Example SPEC_INDEX.json Structure

```json
{
  "version": "1.0",
  "last_updated": "2024-01-15T10:30:00Z",
  "external_repos": {
    "shared": "/path/to/shared-repo"
  },
  "specs": {
    "spec-004-financial-system": {
      "spec_id": "spec-004-financial-system",
      "title": "Financial System",
      "spec_path": "specs/feature/spec-004-financial-system/spec.md",
      "tasks_path": "specs/feature/spec-004-financial-system/tasks.md",
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts",
        "src/models/transaction.model.ts"
      ],
      "external_files": [
        "@shared/services/common-payment.service.ts"
      ],
      "dependencies": [
        "spec-001-auth",
        "spec-002-database"
      ],
      "last_indexed": "2024-01-15T10:30:00Z",
      "status": "implemented"
    }
  }
}
```

### When to Re-Index

**Recommended times to run re-index:**

1. **After major changes** - When you've added/removed multiple files
2. **Before quality workflows** - To ensure accurate scoping
3. **Weekly maintenance** - Keep index fresh in active projects
4. **After merging** - When merging branches with spec changes
5. **Before releases** - Verify all specs are properly indexed

### Best Practices

1. **Backup automatically** - Re-index workflow backs up before changes
2. **Review the report** - Check what changed in the re-index report
3. **Commit SPEC_INDEX.json** - Track changes in version control
4. **Use --verify first** - Check for issues before making changes
5. **Configure external repos** - Set up `.smartspec/config.json` for external repos

---

## Updated: Test Generation Workflow

### Handling Existing Test Files

The `smartspec_generate_tests` workflow now detects existing test files:

**Before:**
- Always created new test files
- Could overwrite existing tests
- No awareness of current coverage

**After:**
- Checks for existing test files first
- Analyzes current test coverage
- Only generates tests for uncovered parts
- **Appends** new tests (never overwrites!)

### Example Workflow

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --target-coverage 80
```

**What happens:**

1. **Load scope** from SPEC_INDEX.json:
   - `src/services/credit.service.ts`
   - `src/services/payment.service.ts`
   - `src/models/transaction.model.ts`

2. **Check for existing tests:**
   ```
   📝 Test File Analysis:
     ✅ credit.service.spec.ts - EXISTS
        Current: 12 test cases, 65% coverage
        Missing: errorHandler(), calculateInterest()
        Action: Append 5 new test cases
     
     ❌ payment.service.spec.ts - NOT FOUND
        Action: Create new file with 15 test cases
     
     ✅ transaction.model.spec.ts - EXISTS
        Current: 8 test cases, 90% coverage
        Action: No new tests needed (already above target)
   ```

3. **Generate only missing tests:**
   - Append 5 test cases to `credit.service.spec.ts`
   - Create new `payment.service.spec.ts` with 15 test cases
   - Skip `transaction.model.spec.ts` (already has good coverage)

4. **Result:**
   - No duplicate tests
   - Existing tests preserved
   - Coverage increased from 65% to 82%

### Test File Patterns Detected

The workflow checks common test file patterns:
- `src/services/credit.service.spec.ts` (same directory)
- `src/services/__tests__/credit.service.test.ts` (Jest convention)
- `test/unit/services/credit.service.spec.ts` (separate test directory)
- `tests/services/credit.service.test.ts` (alternative test directory)

---

## Summary of New Features

### 1. ✅ Test Generation Improvements
- Detects existing test files
- Analyzes current coverage
- Appends instead of overwrites
- Avoids duplicate tests

### 2. ✅ Re-Index Workflow
- Keeps SPEC_INDEX.json accurate
- Supports external repositories
- Uses 5 file detection strategies
- Generates detailed reports
- Validates and backs up automatically

### 3. ✅ Total Workflows: 14
- 10 core workflows
- 4 quality improvement workflows (including reindex)

### 4. ✅ Performance
- Spec-scoped operations: ~10x faster
- Smart test generation: No duplicates
- Accurate indexing: Better scoping
