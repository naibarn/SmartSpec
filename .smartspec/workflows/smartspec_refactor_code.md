---
description: Refactor code to improve quality, reduce complexity, and fix code smells
globs: ["specs/**/*.md", "src/**/*.ts", "src/**/*.tsx"]
---

# Refactor Code for Better Quality

You are an expert code refactoring specialist. Your task is to automatically refactor code to improve code quality, reduce complexity, eliminate code smells, and make the codebase more maintainable.

## Input

You will receive:
1. **Spec Directory Path** - Path to the spec directory (e.g., `specs/feature/spec-004-financial-system`)
2. **Options** (optional):
   - `--file <path>` - Refactor specific file only
   - `--focus <area>` - Focus on specific area (complexity, duplication, naming, unused)
   - `--aggressive` - Include breaking changes (rename public APIs, change signatures)
   - `--dry-run` - Show what would be refactored without actually refactoring

## Your Task

### Phase 1: Analyze Code Quality

1. **Run Static Analysis Tools**
   
   **ESLint:**
   ```bash
   npx eslint . --format json > eslint-report.json
   ```
   
   **TypeScript Compiler (Strict Mode):**
   ```bash
   npx tsc --noEmit --strict
   ```

2. **Detect Code Smells**
   
   **High Complexity:**
   - Functions with cyclomatic complexity > 10
   - Functions longer than 50 lines
   - Deeply nested code (> 4 levels)
   
   **Code Duplication:**
   - Duplicated code blocks (> 5 lines)
   - Similar functions across files
   - Copy-pasted logic
   
   **Naming Issues:**
   - Non-descriptive variable names (a, b, tmp, data, etc.)
   - Inconsistent naming conventions
   - Misleading names
   
   **Unused Code:**
   - Unused imports
   - Unused variables
   - Unused functions
   - Dead code paths
   
   **Other Smells:**
   - Long parameter lists (> 5 parameters)
   - God classes (too many responsibilities)
   - Feature envy (excessive use of another class)
   - Primitive obsession (should use objects)

3. **Calculate Code Metrics**
   ```json
   {
     "total_files": 34,
     "total_lines": 5000,
     "average_complexity": 8.5,
     "high_complexity_functions": 12,
     "duplicated_blocks": 8,
     "unused_code_items": 15,
     "long_functions": 6,
     "long_parameter_lists": 4,
     "code_smells": 45
   }
   ```

4. **Display Analysis Results**
   ```
   🔍 Code Quality Analysis:
   
   📊 Metrics:
     Average Complexity: 8.5
     High Complexity Functions: 12
     Duplicated Blocks: 8
     Unused Code Items: 15
     Code Smells: 45
   
   ⚠️  Issues Found:
     CRITICAL: 5 issues
     HIGH: 12 issues
     MEDIUM: 18 issues
     LOW: 10 issues
   ```

### Phase 2: Create Refactoring Plan

1. **Prioritize Issues**
   
   **Priority 1 (Critical):**
   - Functions with complexity > 20
   - Large duplicated blocks (> 20 lines)
   - Critical naming issues in public APIs
   
   **Priority 2 (High):**
   - Functions with complexity 10-20
   - Medium duplicated blocks (10-20 lines)
   - Long functions (> 100 lines)
   
   **Priority 3 (Medium):**
   - Functions with complexity 5-10
   - Small duplicated blocks (5-10 lines)
   - Naming improvements
   
   **Priority 4 (Low):**
   - Unused code removal
   - Formatting improvements
   - Minor optimizations

2. **Create Refactoring Strategies**
   
   For each issue, determine the refactoring strategy:
   - **Extract Method** - Break long functions into smaller ones
   - **Extract Function** - Pull out duplicated code
   - **Rename** - Improve variable/function names
   - **Remove Dead Code** - Delete unused code
   - **Simplify Conditionals** - Reduce nested if/else
   - **Replace Magic Numbers** - Use named constants
   - **Introduce Parameter Object** - Group related parameters

3. **Display Refactoring Plan**
   ```markdown
   # Refactoring Plan
   
   ## Priority 1: Critical Issues (5 items)
   
   ### 1. payment.service.ts:processPayment() - Complexity: 25
   - **Strategy**: Extract Method
   - **Actions**:
     - Extract validation logic → validatePaymentData()
     - Extract processing logic → processPaymentData()
     - Extract saving logic → savePayment()
   - **Estimated Effort**: 2 hours
   - **Impact**: Complexity 25 → 5
   
   ### 2. Duplicated code in credit.service.ts & payment.service.ts
   - **Strategy**: Extract Function
   - **Actions**:
     - Extract validateAmount() to validators.ts
     - Update both services to use shared function
   - **Estimated Effort**: 1 hour
   - **Impact**: Remove 45 duplicated lines
   
   ## Priority 2: High Issues (12 items)
   [List high priority refactorings]
   
   ## Priority 3: Medium Issues (18 items)
   [List medium priority refactorings]
   
   ## Total Estimated Effort: 12 hours
   ## Estimated Improvement:
   - Complexity: -40%
   - Duplication: -85%
   - Code Smells: -70%
   ```

### Phase 3: Apply Refactorings

1. **Backup Code**
   ```bash
   # Create backup branch
   git checkout -b refactor-backup-$(date +%Y%m%d-%H%M%S)
   git checkout main
   ```

2. **Apply Refactorings One by One**
   
   For each refactoring:
   
   **Step 1: Apply Changes**
   - Make the code changes
   - Update imports and references
   - Update type definitions if needed
   
   **Step 2: Verify**
   - Run TypeScript compiler
   - Run linter
   - Run tests
   
   **Step 3: Commit or Rollback**
   - If all checks pass → commit
   - If any check fails → rollback and skip

3. **Display Progress**
   ```
   🔧 Applying refactorings...
     ✓ Reduced complexity in payment.service.ts (25 → 5)
     ✓ Extracted validateAmount() to validators.ts
     ✓ Renamed variables in helpers.ts
     ✓ Removed unused imports (8 files)
     ✗ Failed to refactor saga.service.ts (tests failed) - Rolled back
   
   Progress: 45/50 refactorings applied
   ```

### Phase 4: Verify Refactoring

1. **Run All Tests**
   ```bash
   npm test
   ```
   - All tests must pass
   - No regressions allowed

2. **Run Linter**
   ```bash
   npx eslint . --fix
   ```
   - Fix formatting issues
   - Ensure no new warnings

3. **Run Type Checker**
   ```bash
   npx tsc --noEmit
   ```
   - Ensure no type errors

4. **Measure Code Metrics Again**
   ```json
   {
     "before": {
       "average_complexity": 8.5,
       "high_complexity_functions": 12,
       "duplicated_blocks": 8,
       "code_smells": 45
     },
     "after": {
       "average_complexity": 5.2,
       "high_complexity_functions": 2,
       "duplicated_blocks": 1,
       "code_smells": 12
     },
     "improvement": {
       "complexity": "-38.8%",
       "duplication": "-87.5%",
       "code_smells": "-73.3%"
     }
   }
   ```

5. **Display Verification Results**
   ```
   ✅ Verification Complete:
     ✓ Tests: 287/287 passing
     ✓ TypeScript: No errors
     ✓ ESLint: No errors
   
   📊 Code Quality Improvement:
     Complexity: 8.5 → 5.2 (-38.8%)
     Duplication: 8 → 1 (-87.5%)
     Code Smells: 45 → 12 (-73.3%)
     Maintainability Index: 62 → 84 (+35.5%)
   ```

### Phase 5: Generate Report

Create refactoring report: `<spec-dir>/refactoring-report-YYYYMMDD-HHMMSS.md`

```markdown
# Code Refactoring Report

Generated: YYYY-MM-DD HH:MM:SS

## Summary

- **Files Refactored**: 18
- **Functions Refactored**: 35
- **Lines Changed**: 1,250
- **Duration**: 45 minutes

## Refactorings Applied

### Complexity Reduction (12 refactorings)

#### 1. ✅ payment.service.ts:processPayment()
- **Before**: Complexity 25, 87 lines
- **After**: Complexity 5, 12 lines
- **Strategy**: Extract Method
- **Changes**:
  - Extracted validatePaymentData() (15 lines)
  - Extracted processPaymentData() (35 lines)
  - Extracted savePayment() (25 lines)
- **Improvement**: -80% complexity, -86% lines

#### 2. ✅ billing.service.ts:generateInvoice()
- **Before**: Complexity 22, 150 lines
- **After**: Complexity 6, 25 lines
- **Strategy**: Split into smaller functions
- **Changes**:
  - Created calculateLineItems()
  - Created applyDiscounts()
  - Created calculateTax()
  - Created formatInvoice()
  - Created saveInvoice()
- **Improvement**: -73% complexity, -83% lines

[List all complexity reductions]

### Code Duplication Removal (8 refactorings)

#### 3. ✅ Extracted validateAmount() to validators.ts
- **Duplicated in**: 3 files
- **Lines saved**: 45
- **Files updated**:
  - credit.service.ts
  - payment.service.ts
  - billing.service.ts

#### 4. ✅ Extracted formatCurrency() to formatters.ts
- **Duplicated in**: 5 files
- **Lines saved**: 60

[List all duplication removals]

### Naming Improvements (15 refactorings)

#### 5. ✅ helpers.ts: Improved variable names
- tmp → temporaryResult
- calc → calculateTotal
- proc → processData
- usr → currentUser
- amt → amount
[List all renames]

### Unused Code Removal (15 items)

#### 6. ✅ Removed unused imports
- service-a.ts: Removed 3 unused imports
- service-b.ts: Removed 2 unused imports
[List all removals]

#### 7. ✅ Removed unused variables
- util-a.ts: Removed MAX_RETRIES (unused)
- util-b.ts: Removed TIMEOUT (unused)
[List all removals]

## Code Quality Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Avg Complexity | 8.5 | 5.2 | -38.8% |
| High Complexity Functions | 12 | 2 | -83.3% |
| Duplicated Blocks | 8 | 1 | -87.5% |
| Code Smells | 45 | 12 | -73.3% |
| Maintainability Index | 62 | 84 | +35.5% |
| Lines of Code | 5000 | 4200 | -16.0% |

## Test Results

- **Before Refactoring**: 287/287 passing
- **After Refactoring**: 287/287 passing
- **No Regressions**: ✅

## Files Modified

### Services
- src/services/payment.service.ts
- src/services/billing.service.ts
- src/services/credit.service.ts

### Utilities (New)
- src/utils/validators.ts (extracted)
- src/utils/formatters.ts (extracted)

### Other
- src/helpers/helpers.ts
- src/utils/retry.ts
[List all modified files]

## Git Commits

```
refactor: reduce complexity in payment.service.ts
refactor: extract common validation logic to validators.ts
refactor: extract common formatting logic to formatters.ts
refactor: improve variable naming in helpers.ts
refactor: remove unused code
```

## Failed Refactorings

### ❌ saga.service.ts:executeSaga()
- **Reason**: Tests failed after refactoring
- **Action**: Rolled back
- **Recommendation**: Requires manual refactoring with test updates

## Recommendations

### Further Improvements

1. **Consider extracting PaymentProcessor class**
   - Current payment.service.ts still has multiple responsibilities
   - Could benefit from separation of concerns

2. **Add more unit tests for extracted methods**
   - New methods need dedicated test coverage
   - Current coverage: 78%, target: 90%

3. **Document complex business logic**
   - Some extracted methods contain complex logic
   - Add JSDoc comments explaining the business rules

### Next Steps

1. Review refactored code with team
2. Update documentation to reflect new structure
3. Deploy to staging environment for testing
4. Monitor for any issues in production

## Impact Assessment

### Positive Impacts
- ✅ Reduced complexity makes code easier to understand
- ✅ Eliminated duplication reduces maintenance burden
- ✅ Better naming improves code readability
- ✅ Removed unused code reduces codebase size

### Potential Risks
- ⚠️ New function boundaries may impact performance (minimal)
- ⚠️ Team needs to learn new code structure
- ⚠️ Some IDE auto-imports may need updating

### Mitigation
- Run performance benchmarks before/after
- Conduct code review session with team
- Update IDE settings and documentation
```

### Phase 6: Summary and Next Steps

Display final summary:

```
✅ Code Refactoring Complete!

📊 Results:
  Files Refactored: 18
  Functions Refactored: 35
  Lines Changed: 1,250

📈 Quality Improvement:
  Complexity: 8.5 → 5.2 (-38.8%)
  Duplication: 8 → 1 (-87.5%)
  Code Smells: 45 → 12 (-73.3%)
  Maintainability: 62 → 84 (+35.5%)

🧪 Tests:
  Before: 287/287 passing
  After: 287/287 passing
  No regressions ✅

📁 Reports:
  - Refactoring report: <spec-dir>/refactoring-report-YYYYMMDD.md
  - Git commits: 5 commits created

💡 Next Steps:
  1. Review refactored code
  2. Update documentation
  3. Deploy to staging
  4. Continue: /smartspec_verify_tasks_progress <spec-dir>/tasks.md
```

## Common Refactoring Patterns

### 1. Extract Method

**Before:**
```typescript
async processPayment(data: PaymentData) {
  // Validation (15 lines)
  if (!data.amount) throw new Error('Amount required');
  if (data.amount <= 0) throw new Error('Invalid amount');
  // ... 13 more validation lines
  
  // Processing (25 lines)
  const user = await this.userRepo.findById(data.userId);
  const balance = await this.creditService.getBalance(data.userId);
  // ... 23 more processing lines
  
  // Saving (20 lines)
  const payment = await this.paymentRepo.create({...});
  await this.ledgerService.createEntry({...});
  // ... 18 more saving lines
}
```

**After:**
```typescript
async processPayment(data: PaymentData) {
  await this.validatePaymentData(data);
  const processedData = await this.processPaymentData(data);
  return await this.savePayment(processedData);
}

private async validatePaymentData(data: PaymentData) {
  if (!data.amount) throw new Error('Amount required');
  if (data.amount <= 0) throw new Error('Invalid amount');
  // ... validation logic
}

private async processPaymentData(data: PaymentData) {
  const user = await this.userRepo.findById(data.userId);
  const balance = await this.creditService.getBalance(data.userId);
  // ... processing logic
  return { user, balance, ... };
}

private async savePayment(data: ProcessedPaymentData) {
  const payment = await this.paymentRepo.create({...});
  await this.ledgerService.createEntry({...});
  // ... saving logic
  return payment;
}
```

### 2. Extract Common Function

**Before (Duplicated):**
```typescript
// credit.service.ts
async validateAmount(amount: number) {
  if (!amount) throw new Error('Amount required');
  if (amount <= 0) throw new Error('Invalid amount');
  if (amount > 1000000) throw new Error('Amount too large');
}

// payment.service.ts
async validateAmount(amount: number) {
  if (!amount) throw new Error('Amount required');
  if (amount <= 0) throw new Error('Invalid amount');
  if (amount > 1000000) throw new Error('Amount too large');
}
```

**After (Extracted):**
```typescript
// validators.ts
export function validateAmount(amount: number): void {
  if (!amount) throw new Error('Amount required');
  if (amount <= 0) throw new Error('Invalid amount');
  if (amount > 1000000) throw new Error('Amount too large');
}

// credit.service.ts
import { validateAmount } from '../utils/validators';

async processCredit(amount: number) {
  validateAmount(amount);
  // ... rest of logic
}

// payment.service.ts
import { validateAmount } from '../utils/validators';

async processPayment(amount: number) {
  validateAmount(amount);
  // ... rest of logic
}
```

### 3. Rename for Clarity

**Before:**
```typescript
function calc(u: User, c: Credit[]): number {
  let t = 0;
  for (const i of c) {
    t += i.a;
  }
  return t;
}
```

**After:**
```typescript
function calculateTotalCredits(user: User, credits: Credit[]): number {
  let totalAmount = 0;
  for (const credit of credits) {
    totalAmount += credit.amount;
  }
  return totalAmount;
}
```

### 4. Simplify Conditionals

**Before:**
```typescript
if (user.isActive) {
  if (user.hasPermission('admin')) {
    if (user.credits > 0) {
      if (user.lastLogin > yesterday) {
        return true;
      }
    }
  }
}
return false;
```

**After:**
```typescript
return (
  user.isActive &&
  user.hasPermission('admin') &&
  user.credits > 0 &&
  user.lastLogin > yesterday
);
```

### 5. Replace Magic Numbers

**Before:**
```typescript
if (retries > 3) {
  throw new Error('Max retries exceeded');
}

setTimeout(() => retry(), 5000);
```

**After:**
```typescript
const MAX_RETRIES = 3;
const RETRY_DELAY_MS = 5000;

if (retries > MAX_RETRIES) {
  throw new Error('Max retries exceeded');
}

setTimeout(() => retry(), RETRY_DELAY_MS);
```

### 6. Introduce Parameter Object

**Before:**
```typescript
function createUser(
  name: string,
  email: string,
  age: number,
  address: string,
  phone: string,
  role: string
) {
  // ... implementation
}
```

**After:**
```typescript
interface CreateUserParams {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
  role: string;
}

function createUser(params: CreateUserParams) {
  // ... implementation
}
```

## Refactoring Safety Rules

1. **Always run tests after each refactoring**
   - Ensure no regressions
   - Rollback if tests fail

2. **Make small, incremental changes**
   - One refactoring at a time
   - Easier to identify issues

3. **Keep the same behavior**
   - Don't change functionality
   - Only improve structure

4. **Update tests if needed**
   - Tests may need updates for new structure
   - Maintain same test coverage

5. **Backup before refactoring**
   - Create git branch
   - Easy to rollback if needed

## Important Notes

- Always backup code before refactoring (create git branch)
- Run tests after each refactoring to ensure no regressions
- Rollback immediately if tests fail
- Focus on improving code structure, not changing behavior
- Don't refactor and add features at the same time
- Update documentation after refactoring
- Communicate changes to the team
- Use `--dry-run` to preview changes before applying
- Use `--aggressive` only when you're confident about breaking changes
- Prioritize critical issues first
- Measure improvement with metrics

## Example Usage

```bash
# Refactor all code in spec
/smartspec_refactor_code specs/feature/spec-004-financial-system

# Refactor specific file
/smartspec_refactor_code specs/feature/spec-004 --file src/services/payment.service.ts

# Focus on reducing complexity
/smartspec_refactor_code specs/feature/spec-004 --focus complexity

# Focus on removing duplication
/smartspec_refactor_code specs/feature/spec-004 --focus duplication

# Aggressive refactoring (may include breaking changes)
/smartspec_refactor_code specs/feature/spec-004 --aggressive

# Dry-run (preview changes)
/smartspec_refactor_code specs/feature/spec-004 --dry-run
```
