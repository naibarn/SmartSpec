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
