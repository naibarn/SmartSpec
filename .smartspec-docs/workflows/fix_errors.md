# `/smartspec_fix_errors`

**Automatically detect and fix compilation errors, type errors, and runtime errors in spec-scoped files.**

---

## 1. Summary

This workflow acts as an intelligent code debugger that automatically finds and fixes errors in your codebase. It focuses only on files related to a specific spec (spec-scoped), making it fast and precise even in large projects.

- **What it solves:** Eliminates tedious manual error fixing by automatically detecting and resolving compilation errors, type errors, and linting issues.
- **When to use it:** After implementation, when `verify_tasks_progress` reports errors, or before running tests.

---

## 2. Usage

```bash
/smartspec_fix_errors <spec_directory> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_directory` | `string` | ✅ Yes | Path to the spec directory | `specs/feature/spec-004-financial-system` |

### **Filtering Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--file` | `string` | All files | Fix errors in specific file only | `--file src/services/credit.service.ts` |
| `--severity` | `string` | All | Fix only errors of specific severity | `--severity critical` |

**Severity levels:**
- `critical` - Compilation errors that prevent build
- `high` - Type errors that may cause runtime errors
- `medium` - Linting errors that should be fixed
- `low` - Warnings and minor issues

### **Execution Options**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--auto-fix` | `flag` | `false` | Auto-fix all errors without asking for confirmation |
| `--dry-run` | `flag` | `false` | Show what would be fixed without actually fixing |
| `--interactive` | `flag` | `true` | Ask for confirmation before each fix |

---

## 4. Examples

### Fix All Errors in Spec

```bash
/smartspec_fix_errors specs/feature/spec-004-financial-system
```

**What happens:**
1. Loads SPEC_INDEX.json to get scoped files
2. Runs TypeScript compiler on scoped files
3. Runs ESLint on scoped files
4. Categorizes errors by severity
5. Proposes fixes for each error
6. Asks for confirmation before fixing

**Output:**
```
🔍 Scanning spec-004-financial-system...
📂 Scoped files: 5 files
  - src/services/credit.service.ts
  - src/services/payment.service.ts
  - src/models/transaction.model.ts
  - src/controllers/credit.controller.ts
  - src/utils/financial-calculator.ts

🔍 Running TypeScript compiler...
⚠️  Found 8 compilation errors

🔍 Running ESLint...
⚠️  Found 3 linting errors

📊 Error Summary:
  CRITICAL: 3 errors
  HIGH: 5 errors
  MEDIUM: 3 errors
  LOW: 0 errors

🔧 Proposed Fixes:

CRITICAL (3):
✗ src/services/credit.service.ts:45
  TS2345: Argument of type 'string' is not assignable to parameter of type 'number'
  Fix: Cast userId to number using parseInt()
  Confidence: 95%
  
  [Show fix] [Skip] [Skip all critical]
  
✗ src/models/transaction.model.ts:12
  TS2304: Cannot find name 'TransactionStatus'
  Fix: Import TransactionStatus from './types'
  Confidence: 100%

HIGH (5):
✗ src/services/payment.service.ts:23
  TS2322: Type 'null' is not assignable to type 'Payment'
  Fix: Change return type to 'Payment | null'
  Confidence: 90%

...

Apply all fixes? [y/n/selective]: y

✅ Fixed 11 errors:
  - 3 critical errors
  - 5 high errors
  - 3 medium errors

📄 Changes made to 4 files:
  - src/services/credit.service.ts (3 fixes)
  - src/models/transaction.model.ts (2 fixes)
  - src/services/payment.service.ts (4 fixes)
  - src/controllers/credit.controller.ts (2 fixes)

🔍 Re-running TypeScript compiler...
✅ No compilation errors!

💡 Next steps:
  - Review the changes
  - Run tests: npm test
  - Commit changes: git add . && git commit -m "fix: Auto-fix errors in spec-004"
```

---

### Fix Specific File Only

```bash
/smartspec_fix_errors specs/feature/spec-004-financial-system --file src/services/credit.service.ts
```

**Use case:** You know errors are in a specific file.

**Output:**
```
🔍 Scanning credit.service.ts...

⚠️  Found 3 errors:
  CRITICAL: 1 error
  HIGH: 2 errors

✗ src/services/credit.service.ts:45
  TS2345: Argument type mismatch
  Fix: Cast userId to number
  
✗ src/services/credit.service.ts:67
  TS2322: Return type mismatch
  Fix: Add null to return type

✗ src/services/credit.service.ts:89
  TS2339: Property 'score' does not exist
  Fix: Add 'score' to CreditResult interface

Apply fixes? [y/n]: y

✅ Fixed 3 errors in credit.service.ts
```

---

### Fix Only Critical Errors

```bash
/smartspec_fix_errors specs/feature/spec-004-financial-system --severity critical
```

**Use case:** Focus on errors that prevent compilation first.

**Output:**
```
🔍 Filtering for CRITICAL errors only...

⚠️  Found 3 critical errors:

✗ src/services/credit.service.ts:45
  TS2345: Argument type mismatch
  
✗ src/models/transaction.model.ts:12
  TS2304: Cannot find name 'TransactionStatus'
  
✗ src/utils/financial-calculator.ts:34
  TS2554: Expected 2 arguments, but got 1

Apply fixes? [y/n]: y

✅ Fixed 3 critical errors
✅ Build should now succeed

💡 Still have 8 non-critical errors. Run without --severity to fix all.
```

---

### Dry Run (Preview Fixes)

```bash
/smartspec_fix_errors specs/feature/spec-004-financial-system --dry-run
```

**Use case:** See what would be fixed without making changes.

**Output:**
```
🔍 DRY RUN MODE - No changes will be made

📊 Would fix 11 errors:

CRITICAL (3):
✗ src/services/credit.service.ts:45
  TS2345: Argument type mismatch
  Would fix: Cast userId to number using parseInt()
  
✗ src/models/transaction.model.ts:12
  TS2304: Cannot find name 'TransactionStatus'
  Would fix: Add import statement

...

💡 Run without --dry-run to apply these fixes
```

---

### Auto-Fix Without Confirmation

```bash
/smartspec_fix_errors specs/feature/spec-004-financial-system --auto-fix
```

**Use case:** You trust the auto-fixer and want to fix all errors quickly.

**Output:**
```
🔍 AUTO-FIX MODE - Fixing all errors automatically...

✅ Fixed 11 errors in 4 files
✅ No compilation errors remaining

💡 Review changes and run tests
```

---

## 5. How It Works

### Phase 1: Detect Errors (Spec-Scoped)

**1. Load SPEC_INDEX.json (Canonical-first)**

SmartSpec v5.2 resolves the index in this order unless `--index` is provided:

1) `.spec/SPEC_INDEX.json` (canonical)  
2) `SPEC_INDEX.json` at repo root (legacy mirror)  
3) `.smartspec/SPEC_INDEX.json` (deprecated fallback)

```bash
cat .spec/SPEC_INDEX.json
```

Extract scoped files for the spec:
```json
{
  "specs": {
    "spec-004-financial-system": {
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts",
        "src/models/transaction.model.ts",
        "src/controllers/credit.controller.ts",
        "src/utils/financial-calculator.ts"
      ]
    }
  }
}
```

**2. Run TypeScript Compiler (Scoped)**
```bash
npx tsc --noEmit --pretty false \
  src/services/credit.service.ts \
  src/services/payment.service.ts \
  src/models/transaction.model.ts \
  src/controllers/credit.controller.ts \
  src/utils/financial-calculator.ts
```

Only check the 5 scoped files (not entire project).

**3. Run ESLint (Scoped)**
```bash
npx eslint \
  src/services/credit.service.ts \
  src/services/payment.service.ts \
  src/models/transaction.model.ts \
  src/controllers/credit.controller.ts \
  src/utils/financial-calculator.ts \
  --format json
```

**4. Categorize by Severity**
- **CRITICAL**: Compilation errors (TS2xxx codes)
- **HIGH**: Type errors that may cause runtime issues
- **MEDIUM**: ESLint errors
- **LOW**: ESLint warnings

---

### Phase 2: Analyze Errors

For each error:

**1. Read Context**
```typescript
// Read 10 lines before and after error line
// Example: Error at line 45

// Lines 35-44 (context before)
function calculateCreditScore(userId: number): number {
  const user = getUserById(userId);
  if (!user) {
    throw new Error('User not found');
  }
  
  // Line 45 (error line)
  const score = calculateScore(userId);  // ❌ Error: userId is string
  
  // Lines 46-55 (context after)
  return score;
}
```

**2. Identify Root Cause**
- **Type mismatch**: `userId` is `string` but function expects `number`
- **Fix**: Cast to number using `parseInt(userId)`

**3. Calculate Confidence**
- **100%**: Simple fixes (add import, fix typo)
- **90-95%**: Type casts, null checks
- **70-80%**: Complex type changes
- **<70%**: Suggest manual review

---

### Phase 3: Apply Fixes

**1. Generate Fix Code**
```typescript
// Before
const score = calculateScore(userId);

// After
const score = calculateScore(parseInt(userId));
```

**2. Apply Fix**
```bash
# Read file
content = read_file('src/services/credit.service.ts')

# Apply fix at line 45
lines[44] = '  const score = calculateScore(parseInt(userId));'

# Write file
write_file('src/services/credit.service.ts', content)
```

**3. Verify Fix**
```bash
# Re-run TypeScript compiler on fixed file
npx tsc --noEmit src/services/credit.service.ts

# Check if error is gone
if no_errors:
  print("✅ Fix successful")
else:
  print("⚠️ Fix may need manual review")
```

---

## 6. Error Types & Fixes

### Type Mismatch Errors

**Error:**
```
TS2345: Argument of type 'string' is not assignable to parameter of type 'number'
```

**Fix:**
```typescript
// Before
const score = calculateScore(userId);

// After
const score = calculateScore(parseInt(userId));
```

---

### Missing Import Errors

**Error:**
```
TS2304: Cannot find name 'TransactionStatus'
```

**Fix:**
```typescript
// Before
export interface Transaction {
  status: TransactionStatus;
}

// After
import { TransactionStatus } from './types';

export interface Transaction {
  status: TransactionStatus;
}
```

---

### Null/Undefined Errors

**Error:**
```
TS2322: Type 'Payment | null' is not assignable to type 'Payment'
```

**Fix:**
```typescript
// Before
function getPayment(): Payment {
  return null;  // ❌ Error
}

// After
function getPayment(): Payment | null {
  return null;
}
```

---

### Property Not Found Errors

**Error:**
```
TS2339: Property 'score' does not exist on type 'CreditResult'
```

**Fix:**
```typescript
// Before
interface CreditResult {
  userId: string;
}

// After
interface CreditResult {
  userId: string;
  score: number;
}
```

---

### Function Signature Errors

**Error:**
```
TS2554: Expected 2 arguments, but got 1
```

**Fix:**
```typescript
// Before
calculateInterest(amount);

// After
calculateInterest(amount, rate);
```

---

## 7. Confidence Levels

| Confidence | Fix Type | Action |
| :--- | :--- | :--- |
| **100%** | Simple fixes (imports, typos) | Auto-apply |
| **90-95%** | Type casts, null checks | Auto-apply with review |
| **70-80%** | Complex type changes | Ask for confirmation |
| **<70%** | Uncertain fixes | Show suggestion, manual review |

---

## 8. Safety Features

### Backup Before Fixing

Before making any changes, create a backup.

**Default backup location (v5.2):**
```
.spec/backups/
  ├── credit.service.ts.backup-20240115-103000
  ├── payment.service.ts.backup-20240115-103000
  └── ...
```

**Legacy backup location (older versions / transitional projects):**
```
.smartspec/backups/
  ├── credit.service.ts.backup-20240115-103000
  ├── payment.service.ts.backup-20240115-103000
  └── ...
```

**Restore from backup:**
```bash
# v5.2 default
cp .spec/backups/credit.service.ts.backup-20240115-103000 src/services/credit.service.ts

# legacy fallback
cp .smartspec/backups/credit.service.ts.backup-20240115-103000 src/services/credit.service.ts
```

### Verification After Fixing

After each fix:
1. Re-run TypeScript compiler
2. Check if error is gone
3. Check for new errors introduced
4. Report success or failure

### Rollback on Failure

If a fix creates new errors:
1. Rollback the fix immediately
2. Mark as "Failed" in report
3. Add to "Requires Manual Fix" list
4. Continue with other fixes

---

## 9. Performance

### Execution Time

Typical performance (spec-scoped):
- **Small spec (1-5 files):** 5-15 seconds
- **Medium spec (6-20 files):** 15-45 seconds
- **Large spec (20+ files):** 45-120 seconds

Performance depends on:
- Language tooling (TypeScript, ESLint)
- Project size
- Machine resources

---

## 10. Best Practices

### 1. Fix Critical Errors First

```bash
# Fix critical errors first
/smartspec_fix_errors specs/feature/spec-004 --severity critical

# Then fix high severity
/smartspec_fix_errors specs/feature/spec-004 --severity high

# Finally fix medium/low
/smartspec_fix_errors specs/feature/spec-004
```

### 2. Use Dry Run for Complex Specs

```bash
# Preview fixes first
/smartspec_fix_errors specs/critical/payment-gateway --dry-run
```

### 3. Verify After Fixing

```bash
# Fix errors
/smartspec_fix_errors specs/feature/spec-004

# Verify no errors remain
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

### 4. Commit After Fixing

```bash
# Fix errors
/smartspec_fix_errors specs/feature/spec-004

# Review changes
/git diff

# Commit
/git add . && git commit -m "fix: resolve errors for spec-004"
```

### 5. Respect UI JSON Ownership (UI Specs)

If your spec is categorized as **UI** and uses `ui.json` as the design source of truth:

- Treat `ui.json` as **design-owned**.
- `smartspec_fix_errors` should focus on code files listed in the SPEC_INDEX entry.
- Do **not** auto-edit `ui.json` unless the tasks explicitly instruct a change that belongs to the engineering side (rare).
- If errors are caused by UI-to-component mismatches, prefer:
  1) updating the UI component registry, or  
  2) adding a dedicated binding/refactor task.

This keeps the Penpot-driven workflow stable while still allowing engineering to resolve runtime and type errors safely.

---

## 11. Troubleshooting

### Issue: Too many false positive fixes

**Cause:** The workflow may misinterpret complex architectural patterns with limited context.

**Solution:**
1. Re-run with `--interactive` (default) to review each fix.
2. Use `--file` to limit scope.
3. Consider adding clarifying comments or types in the code.

### Issue: Fix introduces new errors

**Cause:** The proposed fix may be correct locally but breaks related code.

**Solution:**
1. Use backups to rollback.
2. Re-run with `--severity critical` first.
3. Consider manual fix for this case.

### Issue: SPEC_INDEX.json outdated

**Cause:** Index may not reflect current file list.

**Solution:**
1. Run reindex for the spec:
   ```bash
   /smartspec_reindex_specs --spec specs/feature/spec-004
   ```
2. Re-run fix:
   ```bash
   /smartspec_fix_errors specs/feature/spec-004
   ```

---

## 12. Related Workflows

Before fixing errors:
- **`/smartspec_reindex_specs`** - Ensure the file registry is accurate
- **`/smartspec_verify_tasks_progress`** - Identify failing tasks and error scope

After fixing errors:
- **`/smartspec_generate_tests`** - Add missing tests
- **`/smartspec_refactor_code`** - Improve code quality
- **`/smartspec_implement_tasks`** - Continue implementing remaining tasks

---

## 13. Summary

The `smartspec_fix_errors` workflow is a spec-scoped auto-debugger that finds and resolves compilation, type, and linting errors safely. It is designed to keep large projects moving without losing control of architecture or spec boundaries.

**Key Benefits:**
- ✅ Spec-scoped error detection
- ✅ Severity-based prioritization
- ✅ Safe fix generation with confidence scoring
- ✅ Safety features (backups + rollback)
- ✅ Works smoothly with centralization and UI addendum rules

**Next Steps:**
1. Reindex if required: `/smartspec_reindex_specs --spec <spec_dir>`
2. Fix errors: `/smartspec_fix_errors <spec_dir>`
3. Verify progress: `/smartspec_verify_tasks_progress <tasks.md>`
4. Generate tests or refactor as needed

