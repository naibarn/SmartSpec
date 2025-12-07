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
   - `--kilocode` - Use Kilo Code Orchestrator Mode with Ask/Architect/Code workflow for systematic refactoring

## Your Task

### Phase 1: Analyze Code Quality

1. **Load SPEC_INDEX.json**
   ```bash
   cat .smartspec/SPEC_INDEX.json
   ```
   - Parse JSON to get spec metadata
   - Extract `spec.files[]` array for the given spec_id
   - If `--file` option provided, use only that file
   - Otherwise, use all files from `spec.files[]`
   - **SCOPE**: Only analyze files listed in spec.files[] (not entire project!)

2. **Run Static Analysis Tools (scoped)**
   
   **ESLint (scoped):**
   ```bash
   # Only lint files in scope
   npx eslint <file1> <file2> ... --format json > eslint-report.json
   ```
   
   **TypeScript Compiler (Strict Mode, scoped):**
   ```bash
   # Only check files in scope
   npx tsc --noEmit --strict <file1> <file2> ...
   ```

3. **Detect Code Smells (scoped)**
   
   **High Complexity:**
   - Functions with cyclomatic complexity > 10 (in scoped files only)
   - Functions longer than 50 lines (in scoped files only)
   - Deeply nested code (> 4 levels) (in scoped files only)
   
   **Code Duplication:**
   - Duplicated code blocks (> 5 lines) (within scoped files)
   - Similar functions across scoped files
   - Copy-pasted logic (within scoped files)
   
   **Naming Issues:**
   - Non-descriptive variable names (a, b, tmp, data, etc.) (in scoped files)
   - Inconsistent naming conventions (in scoped files)
   - Misleading names (in scoped files)
   
   **Unused Code:**
   - Unused imports (in scoped files)
   - Unused variables (in scoped files)
   - Unused functions (in scoped files)
   - Dead code paths (in scoped files)
   
   **Other Smells:**
   - Long parameter lists (> 5 parameters) (in scoped files)
   - God classes (too many responsibilities) (in scoped files)
   - Feature envy (excessive use of another class) (in scoped files)
   - Primitive obsession (should use objects) (in scoped files)

4. **Calculate Code Metrics (scoped)**

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

**If `--kilocode` flag: Use Kilo Code Orchestrator Mode**

```
Use Orchestrator Mode to break this refactoring into subtasks.
Refactor code to improve quality: {summary of refactorings needed}
```

**Orchestrator may create workflow:**
1. **Ask Mode** - Analyze current code structure and refactoring impact
2. **Architect Mode** - Design refactored architecture and structure
3. **Code Mode** - Apply refactorings one by one
4. **Debug Mode** - Fix any issues introduced
5. **Test Mode** - Validate all tests pass

**If NOT using `--kilocode`:**

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
  2. Run tests: npm test
  3. Update documentation (if needed)
  4. Commit: git add . && git commit -m "refactor: Improve code quality in spec-XXX"
  
  🔧 Suggested Workflows:
  
  ✅ Refactoring complete! Consider these next actions:
  
  1. Ensure tests still pass:
     npm test
     # If failures found:
     /smartspec_fix_errors <spec-dir>
  
  2. Check test coverage:
     /smartspec_generate_tests <spec-dir> --target-coverage 80
  
  3. Verify overall progress:
     /smartspec_verify_tasks_progress <spec-dir>/tasks.md
  
  4. Continue implementation:
     /smartspec_implement_tasks <spec-dir>/tasks.md --skip-completed
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

---

# UI Centralization Addendum (Penpot-first)

เอกสารนี้เป็นส่วนเสริมของ **SmartSpec Centralization Contract**  
เพื่อรองรับ **SPEC ประเภท UI** ที่มีข้อกำหนดพิเศษ:

- **UI design source of truth เป็น JSON** (เพื่อใช้กับ Penpot)
- ทีม UI ต้องสามารถแก้ UI ได้ตรงจากไฟล์นี้
- งานของทีม dev ต้องผูกกับ component/logic โดยไม่ทำให้ไฟล์ UI JSON ปน logic

ใช้ addendum นี้วางต่อท้าย contract ในทุก workflow ที่แตะ UI:
- generate-spec
- generate-plan
- generate-tasks
- implement-tasks
- verify-tasks-progress
- generate-tests
- refactor-code
- reverse-to-spec
- reindex-specs
- validate-index
- sync-spec-tasks
- fix-errors
- generate-implement-prompt / generate-cursor-prompt (ในส่วน canonical constraints)

---

## 1) UI File Model

สำหรับ UI spec ให้ถือว่าในโฟลเดอร์ spec มีไฟล์หลัก 2 ชั้น:

1) `spec.md`  
   - narrative, scope, non-goals, UX rules, accessibility, performance targets  
   - อ้างอิงไฟล์ UI JSON เป็น design artifact

2) `ui.json` (หรือชื่อที่ทีมกำหนดใน config)  
   - **Penpot-editable**  
   - เก็บ layout, components mapping, design tokens references  
   - **ห้าม** ใส่ business logic หรือ API behaviour ในไฟล์นี้

> ถ้าทีมต้องการชื่อไฟล์เฉพาะ ให้กำหนดใน config:
```json
{
  "ui_spec": {
    "ui_json_name": "ui.json",
    "component_registry": "ui-component-registry.json"
  }
}
```

---

## 2) Registry เพิ่มเติมสำหรับ UI (แนะนำ)

เพิ่มไฟล์ registry ใหม่แบบ optional:

- `.spec/registry/ui-component-registry.json`

โครงสร้างขั้นต่ำแนะนำ:
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601",
  "components": [
    {
      "canonical_name": "UserAvatar",
      "penpot_component_id": "penpot:component:xxx",
      "code_component_path": "src/components/user/UserAvatar.tsx",
      "owned_by_spec": "spec-XXX",
      "aliases": []
    }
  ]
}
```

**กติกา:**
- ชื่อ component ใน tasks/implementation ต้องอ้าง `canonical_name` เป็นค่า default
- ถ้าพบชื่อใหม่:
  - generate-spec / generate-tasks สามารถเพิ่ม entry ใหม่ได้
  - implement / verify ต้องอ่านอย่างเดียว

---

## 3) UI Naming & Separation Rules (MUST)

### 3.1 Separation of Concerns

- `ui.json` = design + structure + bindings
- business logic / data fetching / permissions  
  ต้องอยู่ใน:
  - code components
  - service layer
  - hooks/store
  - หรือ spec.md ในส่วน logic description

### 3.2 Canonical-first

เมื่อ workflow ต้องเสนอชื่อ component:
1) เช็ค `ui-component-registry.json` (ถ้ามี)
2) เช็ค glossary (คำเรียกหน้าจอ/ฟีเจอร์)
3) ถ้ายังไม่มี:
   - เสนอชื่อใหม่แบบ `Proposed`
   - สร้าง task ให้ลงทะเบียน

---

## 4) Workflow-specific Enforcement

### 4.1 generate-spec (UI category)

ต้อง:
- ตรวจ/สร้าง `ui.json` template ขั้นต่ำ (ถ้ายังไม่มี)
- เพิ่ม `ui.json` ลงใน SPEC_INDEX `files` (ถ้าสคีมารองรับ)
- ระบุใน spec.md ว่า:
  - design source-of-truth = ui.json
  - logic อยู่ที่ code layer

### 4.2 generate-tasks

สำหรับ UI spec:
- สร้าง 3 กลุ่มงานแยกกันชัดเจน:

1) **Design tasks (UI team)**
   - ปรับ layout/flow ใน `ui.json` ผ่าน Penpot

2) **Component binding tasks**
   - map Penpot component → code component
   - อัปเดต `ui-component-registry.json` (ถ้าจำเป็น)

3) **Logic tasks (Dev team)**
   - สร้าง/แก้ hooks/services/state
   - ห้ามใส่ logic ใหม่ใน `ui.json`

### 4.3 implement-tasks / refactor-code

- Treat `ui.json` เป็น **design-owned**
- แก้ไขได้เฉพาะเมื่อ tasks ระบุชัดเจน
- ถ้าพบว่า logic ถูกฝังใน ui.json:
  - สร้าง refactor task เพื่อย้าย logic ออก

### 4.4 generate-tests

- อ้าง component canonical names
- สนับสนุนแนวทาง:
  - component tests
  - accessibility checks
  - visual regression (ถ้าทีมใช้)

---

## 5) Index & Validation Rules

### 5.1 SPEC_INDEX

สำหรับ UI spec:
- แนะนำให้มี field เสริมใน entry (ถ้าทีมอนุญาตแบบ additive):
```json
{
  "ui_artifacts": {
    "ui_json_path": "specs/ui/spec-123/ui.json",
    "penpot_project": "optional-string"
  }
}
```

ถ้าไม่เพิ่ม schema:
- ให้ใช้ `files` list แทน

### 5.2 validate-index / global-registry-audit

ต้องตรวจอย่างน้อย:
- UI spec ที่ category=ui ต้องมี `ui.json`
- ชื่อ component ที่ spec/tasks อ้าง ต้องสอดคล้องกับ registry

---

## 6) ผลลัพธ์ที่ต้องการ

- ทีม UI แก้ UI ได้โดยไม่ชนกับ dev logic
- ลดการแตกชื่อ component ซ้ำซ้อน
- UI specs กลายเป็นส่วนหนึ่งของ centralization ไม่ใช่โลกคู่ขนาน
