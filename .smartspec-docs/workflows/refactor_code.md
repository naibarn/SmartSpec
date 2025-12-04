# `/smartspec_refactor_code`

**Automatically refactor code to improve quality, reduce complexity, and eliminate code smells.**

---

## 1. Summary

This workflow acts as an expert code refactoring specialist that analyzes code quality issues and automatically applies safe refactorings. It focuses only on files related to a specific spec (spec-scoped), making it practical for large codebases.

- **What it solves:** Eliminates technical debt by reducing complexity, removing duplication, improving naming, and cleaning up unused code.
- **When to use it:** After implementation, when code reviews flag quality issues, or before releases.

---

## 2. Usage

```bash
/smartspec_refactor_code <spec_directory> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_directory` | `string` | ✅ Yes | Path to the spec directory | `specs/feature/spec-004-financial-system` |

### **Focus Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--focus` | `string` | All areas | Focus on specific refactoring area | `--focus complexity` |
| `--file` | `string` | All files | Refactor specific file only | `--file src/services/credit.service.ts` |

**Focus areas:**
- `complexity` - Reduce cyclomatic complexity and nesting
- `duplication` - Remove duplicated code
- `naming` - Improve variable and function names
- `unused` - Remove unused code
- `all` - All refactoring areas (default)

### **Execution Options**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--aggressive` | `flag` | `false` | Include breaking changes (rename public APIs) |
| `--dry-run` | `flag` | `false` | Show what would be refactored without changes |
| `--safe-only` | `flag` | `true` | Only apply safe refactorings (no breaking changes) |

---

## 4. Examples

### Refactor All Code Quality Issues

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system
```

**What happens:**
1. Loads SPEC_INDEX.json to get scoped files
2. Runs static analysis (ESLint, TypeScript)
3. Detects code smells (complexity, duplication, naming, unused)
4. Creates refactoring plan
5. Applies safe refactorings
6. Verifies code still compiles and tests pass

**Output:**
```
🔍 Analyzing code quality for spec-004-financial-system...
📂 Scoped files: 5 files
  - src/services/credit.service.ts
  - src/services/payment.service.ts
  - src/models/transaction.model.ts
  - src/controllers/credit.controller.ts
  - src/utils/financial-calculator.ts

🔍 Running static analysis...
⚠️  Found 23 code quality issues:

📊 Code Quality Report:

High Complexity (8):
  ✗ credit.service.ts:calculateCreditScore() - Complexity: 15 (threshold: 10)
  ✗ payment.service.ts:processPayment() - Complexity: 12
  ✗ financial-calculator.ts:calculateInterest() - 78 lines (threshold: 50)

Code Duplication (5):
  ✗ credit.service.ts:45-60 duplicates payment.service.ts:89-104
  ✗ Similar validation logic in 3 files

Naming Issues (6):
  ✗ credit.service.ts:45 - Variable 'a' is not descriptive
  ✗ payment.service.ts:23 - Function 'doStuff' is not descriptive
  ✗ transaction.model.ts:12 - Inconsistent naming: 'user_id' vs 'userId'

Unused Code (4):
  ✗ credit.service.ts:12 - Unused import 'lodash'
  ✗ payment.service.ts:67 - Unused function 'oldCalculate'
  ✗ financial-calculator.ts:34 - Dead code path

🔧 Refactoring Plan:

Priority 1 - High Complexity (8 issues):
  1. Extract method from calculateCreditScore() (lines 45-78)
  2. Simplify processPayment() using early returns
  3. Split calculateInterest() into smaller functions

Priority 2 - Code Duplication (5 issues):
  4. Extract common validation to shared function
  5. Create base validator class

Priority 3 - Naming (6 issues):
  6. Rename 'a' → 'amount'
  7. Rename 'doStuff' → 'validatePaymentDetails'
  8. Standardize naming: user_id → userId

Priority 4 - Unused Code (4 issues):
  9. Remove unused imports
  10. Remove unused functions
  11. Remove dead code paths

Apply refactorings? [y/n/selective]: y

🔧 Applying refactorings...

✅ credit.service.ts
   - Extracted method: validateUserCredit() (reduced complexity 15 → 8)
   - Renamed variable: a → amount
   - Removed unused import: lodash

✅ payment.service.ts
   - Simplified with early returns (reduced complexity 12 → 7)
   - Renamed function: doStuff → validatePaymentDetails
   - Removed unused function: oldCalculate()

✅ financial-calculator.ts
   - Split into 3 smaller functions (78 lines → 25+20+18 lines)
   - Removed dead code path

✅ common/validators.ts (NEW)
   - Extracted shared validation logic

📊 Quality Improvement:

Before:
  Average Complexity: 12.3
  Code Duplication: 15%
  Naming Issues: 6
  Unused Code: 4 items

After:
  Average Complexity: 6.8 (-45%)
  Code Duplication: 3% (-80%)
  Naming Issues: 0 (-100%)
  Unused Code: 0 (-100%)

✅ All tests still passing!

💡 Next steps:
  - Review refactored code
  - Run full test suite: npm test
  - Commit: git add . && git commit -m "refactor: Improve code quality in spec-004"
```

---

### Focus on Reducing Complexity

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system --focus complexity
```

**Use case:** You have complex functions that need simplification.

**Output:**
```
🔍 Focusing on COMPLEXITY only...

⚠️  Found 8 high complexity issues:

✗ credit.service.ts:calculateCreditScore()
  Complexity: 15 (threshold: 10)
  Lines: 65 (threshold: 50)
  Nesting: 5 levels (threshold: 4)
  
  Suggested refactorings:
  1. Extract validation logic → validateUserCredit()
  2. Extract calculation logic → computeScoreValue()
  3. Use early returns to reduce nesting

✗ payment.service.ts:processPayment()
  Complexity: 12
  
  Suggested refactorings:
  1. Use early returns for error cases
  2. Extract payment validation → validatePayment()

Apply refactorings? [y/n]: y

✅ Reduced complexity:
  - calculateCreditScore: 15 → 8 (-47%)
  - processPayment: 12 → 7 (-42%)

📊 Average complexity: 12.3 → 6.8 (-45%)
```

---

### Remove Code Duplication

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system --focus duplication
```

**Use case:** You have copy-pasted code that should be shared.

**Output:**
```
🔍 Focusing on DUPLICATION only...

⚠️  Found 5 duplication issues:

✗ Duplicated code (15 lines):
  credit.service.ts:45-60
  payment.service.ts:89-104
  
  Similarity: 95%
  
  Suggested refactoring:
  Extract to: src/common/validators.ts:validateAmount()

✗ Similar validation logic in 3 files:
  credit.service.ts:validateUser()
  payment.service.ts:validateUser()
  transaction.model.ts:validateUser()
  
  Suggested refactoring:
  Create base validator: src/common/user-validator.ts

Apply refactorings? [y/n]: y

✅ Removed duplication:
  - Created src/common/validators.ts
  - Created src/common/user-validator.ts
  - Updated 5 files to use shared code

📊 Code duplication: 15% → 3% (-80%)
```

---

### Improve Naming

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system --focus naming
```

**Use case:** Your code has unclear or inconsistent names.

**Output:**
```
🔍 Focusing on NAMING only...

⚠️  Found 6 naming issues:

✗ credit.service.ts:45
  Variable 'a' is not descriptive
  Suggested: 'amount' (based on usage context)

✗ payment.service.ts:23
  Function 'doStuff' is not descriptive
  Suggested: 'validatePaymentDetails' (based on function body)

✗ transaction.model.ts:12
  Inconsistent naming: 'user_id' (snake_case)
  Should be: 'userId' (camelCase, project standard)

Apply refactorings? [y/n]: y

✅ Improved naming:
  - Renamed 6 variables/functions
  - Standardized naming convention
  - Updated all references

📊 Naming issues: 6 → 0 (-100%)
```

---

### Remove Unused Code

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system --focus unused
```

**Use case:** Clean up unused imports, variables, and functions.

**Output:**
```
🔍 Focusing on UNUSED CODE only...

⚠️  Found 4 unused code items:

✗ credit.service.ts:12
  Unused import: 'lodash'

✗ payment.service.ts:67
  Unused function: oldCalculate()
  Last used: 3 months ago (git history)

✗ financial-calculator.ts:34
  Dead code path: if (false) { ... }

Apply refactorings? [y/n]: y

✅ Removed unused code:
  - Removed 2 unused imports
  - Removed 1 unused function
  - Removed 1 dead code path

📊 Unused code: 4 items → 0 (-100%)
```

---

### Dry Run (Preview Refactorings)

```bash
/smartspec_refactor_code specs/feature/spec-004-financial-system --dry-run
```

**Use case:** See what would be refactored without making changes.

**Output:**
```
🔍 DRY RUN MODE - No changes will be made

📊 Would apply 23 refactorings:

High Complexity (8):
  1. credit.service.ts:calculateCreditScore()
     Would extract method: validateUserCredit()
     
     Before:
       function calculateCreditScore(userId: string): number {
         if (!userId) throw new Error('Invalid user');
         const user = getUserById(userId);
         if (!user) throw new Error('User not found');
         if (!user.isActive) throw new Error('User inactive');
         // ... 60 more lines
       }
     
     After:
       function calculateCreditScore(userId: string): number {
         validateUserCredit(userId);
         const score = computeScoreValue(userId);
         return score;
       }
       
       function validateUserCredit(userId: string): void {
         if (!userId) throw new Error('Invalid user');
         const user = getUserById(userId);
         if (!user) throw new Error('User not found');
         if (!user.isActive) throw new Error('User inactive');
       }

...

💡 Run without --dry-run to apply these refactorings
```

---

## 5. How It Works

### Phase 1: Analyze Code Quality (Spec-Scoped)

**1. Load SPEC_INDEX.json**
```json
{
  "specs": {
    "spec-004-financial-system": {
      "files": [
        "src/services/credit.service.ts",
        "src/services/payment.service.ts",
        "src/models/transaction.model.ts"
      ]
    }
  }
}
```

**2. Run Static Analysis (Scoped)**
```bash
# ESLint on scoped files only
npx eslint \
  src/services/credit.service.ts \
  src/services/payment.service.ts \
  src/models/transaction.model.ts \
  --format json

# TypeScript strict mode on scoped files only
npx tsc --noEmit --strict \
  src/services/credit.service.ts \
  src/services/payment.service.ts \
  src/models/transaction.model.ts
```

**3. Detect Code Smells (Scoped)**

Only analyze code smells in scoped files:
- High complexity functions
- Duplicated code within scoped files
- Naming issues in scoped files
- Unused code in scoped files

---

### Phase 2: Create Refactoring Plan

**1. Categorize by Priority**

| Priority | Category | Impact | Risk |
|----------|----------|--------|------|
| 1 | High Complexity | High | Low |
| 2 | Code Duplication | High | Medium |
| 3 | Naming Issues | Medium | Low |
| 4 | Unused Code | Low | Low |

**2. Generate Refactoring Steps**

For each issue:
```
Issue: calculateCreditScore() has complexity 15

Refactoring steps:
1. Extract validation → validateUserCredit()
2. Extract calculation → computeScoreValue()
3. Use early returns
4. Reduce nesting

Estimated impact:
- Complexity: 15 → 8 (-47%)
- Lines: 65 → 25 (-62%)
- Nesting: 5 → 2 (-60%)

Risk: Low (safe refactoring)
```

---

### Phase 3: Apply Refactorings

**1. Extract Method**

Before:
```typescript
function calculateCreditScore(userId: string): number {
  if (!userId) throw new Error('Invalid user');
  const user = getUserById(userId);
  if (!user) throw new Error('User not found');
  if (!user.isActive) throw new Error('User inactive');
  
  let score = 700;
  if (user.paymentHistory.length > 0) {
    score += user.paymentHistory.filter(p => p.onTime).length * 10;
  }
  if (user.creditHistory.length > 0) {
    score += user.creditHistory.filter(c => c.good).length * 5;
  }
  
  return score;
}
```

After:
```typescript
function calculateCreditScore(userId: string): number {
  validateUserCredit(userId);
  const score = computeScoreValue(userId);
  return score;
}

function validateUserCredit(userId: string): void {
  if (!userId) throw new Error('Invalid user');
  const user = getUserById(userId);
  if (!user) throw new Error('User not found');
  if (!user.isActive) throw new Error('User inactive');
}

function computeScoreValue(userId: string): number {
  const user = getUserById(userId);
  let score = 700;
  score += calculatePaymentScore(user);
  score += calculateCreditHistoryScore(user);
  return score;
}
```

**2. Remove Duplication**

Before:
```typescript
// credit.service.ts
if (!amount || amount <= 0) {
  throw new Error('Invalid amount');
}

// payment.service.ts
if (!amount || amount <= 0) {
  throw new Error('Invalid amount');
}
```

After:
```typescript
// common/validators.ts
export function validateAmount(amount: number): void {
  if (!amount || amount <= 0) {
    throw new Error('Invalid amount');
  }
}

// credit.service.ts
import { validateAmount } from '../common/validators';
validateAmount(amount);

// payment.service.ts
import { validateAmount } from '../common/validators';
validateAmount(amount);
```

**3. Improve Naming**

Before:
```typescript
function doStuff(a: number, b: string): number {
  const x = getUserById(b);
  return a * x.rate;
}
```

After:
```typescript
function calculateInterest(amount: number, userId: string): number {
  const user = getUserById(userId);
  return amount * user.interestRate;
}
```

**4. Remove Unused Code**

Before:
```typescript
import { lodash } from 'lodash';  // ❌ Unused
import { getUserById } from './user.repo';

function oldCalculate() {  // ❌ Unused
  // ...
}

function calculateScore(userId: string): number {
  if (false) {  // ❌ Dead code
    return 0;
  }
  return getUserById(userId).score;
}
```

After:
```typescript
import { getUserById } from './user.repo';

function calculateScore(userId: string): number {
  return getUserById(userId).score;
}
```

---

## 6. Code Quality Metrics

### Cyclomatic Complexity

| Complexity | Rating | Action |
|-----------|--------|--------|
| 1-5 | ✅ Simple | No action needed |
| 6-10 | ⚠️ Moderate | Consider simplifying |
| 11-20 | ❌ Complex | Refactor recommended |
| 21+ | 🚨 Very Complex | Refactor required |

### Code Duplication

| Duplication | Rating | Action |
|------------|--------|--------|
| 0-5% | ✅ Excellent | No action needed |
| 6-10% | ⚠️ Good | Monitor |
| 11-20% | ❌ Poor | Refactor recommended |
| 21%+ | 🚨 Very Poor | Refactor required |

---

## 7. Safety Features

### Backup Before Refactoring

```
.smartspec/backups/
  ├── credit.service.ts.backup-20240115-103000
  ├── payment.service.ts.backup-20240115-103000
  └── ...
```

### Verification After Refactoring

After each refactoring:
1. Re-run TypeScript compiler
2. Run tests
3. Check for breaking changes
4. Rollback if issues detected

### Rollback on Failure

```
⚠️  Refactoring caused test failures:
  - credit.service.spec.ts: 2 tests failed

Rolling back changes...
✅ Rolled back to previous state
💡 Manual review needed
```

---

## 8. Performance

### Execution Time

| Project Size | Files in Spec | Refactorings | Time |
|-------------|---------------|--------------|------|
| Small | 5 files | 10 refactorings | 30-60s |
| Medium | 10 files | 30 refactorings | 1-2 min |
| Large | 20 files | 50+ refactorings | 2-4 min |

---

## 9. Best Practices

### 1. Focus on One Area at a Time

```bash
# Fix complexity first
/smartspec_refactor_code specs/feature/spec-004 --focus complexity

# Then remove duplication
/smartspec_refactor_code specs/feature/spec-004 --focus duplication

# Finally clean up naming and unused code
/smartspec_refactor_code specs/feature/spec-004 --focus naming
/smartspec_refactor_code specs/feature/spec-004 --focus unused
```

### 2. Use Dry Run for Large Refactorings

```bash
# Preview first
/smartspec_refactor_code specs/feature/spec-004 --dry-run

# Review proposed changes, then apply
/smartspec_refactor_code specs/feature/spec-004
```

### 3. Verify After Refactoring

```bash
# Refactor
/smartspec_refactor_code specs/feature/spec-004

# Run tests
npm test

# Verify quality improved
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

## 10. Troubleshooting

### Issue: Refactoring breaks tests

**Solution:** Workflow automatically rolls back. Review manually:
```
⚠️  Refactoring caused test failures - rolled back
💡 Use --dry-run to preview changes first
```

### Issue: Too aggressive refactorings

**Solution:** Use `--safe-only` flag:
```bash
/smartspec_refactor_code specs/feature/spec-004 --safe-only
```

---

## 11. Related Workflows

Before refactoring:
- **`/smartspec_fix_errors`** - Fix errors first
- **`/smartspec_generate_tests`** - Ensure good test coverage

After refactoring:
- **`/smartspec_verify_tasks_progress`** - Verify quality improved
- **`/smartspec_generate_tests`** - Add tests for refactored code

---

## 12. Summary

The `smartspec_refactor_code` workflow automatically improves code quality by reducing complexity, removing duplication, improving naming, and cleaning up unused code. It operates on spec-scoped files for speed and safety.

**Key Benefits:**
- ✅ Spec-scoped for speed
- ✅ Reduces complexity by 40-50%
- ✅ Removes 80%+ code duplication
- ✅ Improves naming and readability
- ✅ Cleans up unused code
- ✅ Safe refactorings with automatic rollback

**Next Steps:**
1. Run `/smartspec_refactor_code <spec_directory>`
2. Review proposed refactorings
3. Run tests to verify
4. Commit changes
