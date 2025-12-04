# `/smartspec_generate_tests`

**Automatically generate comprehensive unit tests, integration tests, and e2e tests to increase test coverage.**

---

## 1. Summary

This workflow acts as an expert test engineer that analyzes your code coverage and automatically generates missing tests. It intelligently detects existing test files and **appends** new tests instead of overwriting, preventing test duplication.

- **What it solves:** Eliminates the tedious work of writing boilerplate tests and ensures high code coverage.
- **When to use it:** After implementation, when coverage is low, or before releases.

---

## 2. Usage

```bash
/smartspec_generate_tests <spec_directory> [options...]
```

---

## 3. Parameters & Options

### **Primary Argument**

| Name | Type | Required? | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `spec_directory` | `string` | ✅ Yes | Path to the spec directory | `specs/feature/spec-004-financial-system` |

### **Coverage Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--target-coverage` | `number` | `80` | Target coverage percentage | `--target-coverage 90` |
| `--focus` | `string` | All | Focus on specific area | `--focus uncovered` |

**Focus values:**
- `uncovered` - Only generate tests for uncovered code
- `critical` - Focus on critical paths (error handling, edge cases)
- `integration` - Focus on integration points

### **Filtering Options**

| Option | Type | Default | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `--file` | `string` | All files | Generate tests for specific file only | `--file src/services/credit.service.ts` |
| `--type` | `string` | All types | Generate specific type of tests | `--type unit` |

**Test types:**
- `unit` - Unit tests for individual functions
- `integration` - Integration tests for service interactions
- `e2e` - End-to-end tests for complete workflows

### **Execution Options**

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--append-only` | `flag` | `true` | Append to existing test files (never overwrite) |
| `--dry-run` | `flag` | `false` | Show what tests would be generated |

---

## 4. Examples

### Generate Tests to Reach 80% Coverage

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --target-coverage 80
```

**What happens:**
1. Loads SPEC_INDEX.json to get scoped files
2. Runs coverage report on scoped files
3. **Detects existing test files** (won't overwrite!)
4. Identifies uncovered code
5. Generates tests to reach 80% coverage
6. **Appends** new tests to existing files or creates new files

**Output:**
```
🔍 Analyzing test coverage for spec-004-financial-system...
📂 Scoped files: 5 files
  - src/services/credit.service.ts
  - src/services/payment.service.ts
  - src/models/transaction.model.ts
  - src/controllers/credit.controller.ts
  - src/utils/financial-calculator.ts

📊 Current Test Coverage:
  Lines: 62.5%
  Statements: 65.0%
  Functions: 58.3%
  Branches: 50.0%

🎯 Target: 80%
📈 Gap: 17.5%

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
  
  ❌ credit.controller.spec.ts - NOT FOUND
     Action: Create new file with 10 test cases
  
  ✅ financial-calculator.spec.ts - EXISTS
     Current: 5 test cases, 45% coverage
     Missing: calculateTax(), edge cases
     Action: Append 8 new test cases

🔧 Generating tests...

✅ credit.service.spec.ts
   Appended 5 new test cases:
   - ✅ should handle invalid user ID
   - ✅ should calculate interest correctly
   - ✅ should throw error when amount is negative
   - ✅ should handle edge case: zero amount
   - ✅ should validate interest rate range

✅ payment.service.spec.ts (NEW FILE)
   Created with 15 test cases:
   - ✅ should process payment successfully
   - ✅ should handle payment failure
   - ✅ should refund payment
   - ... (12 more)

✅ financial-calculator.spec.ts
   Appended 8 new test cases:
   - ✅ should calculate tax correctly
   - ✅ should handle zero tax rate
   - ... (6 more)

📊 New Coverage (estimated):
  Lines: 82.3% (+19.8%)
  Statements: 83.5% (+18.5%)
  Functions: 81.7% (+23.4%)
  Branches: 75.0% (+25.0%)

✅ Target coverage reached!

💡 Next steps:
  - Run tests: npm test
  - Review generated tests
  - Adjust edge cases if needed
  - Commit: git add . && git commit -m "test: Add tests for spec-004"
```

---

### Generate Tests for Specific File

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --file src/services/credit.service.ts
```

**Use case:** You want to focus on testing a specific service.

**Output:**
```
🔍 Analyzing credit.service.ts...

📊 Current Coverage:
  Lines: 65%
  Functions: 58.3%

📝 Existing test file: credit.service.spec.ts
  Current: 12 test cases
  Missing coverage:
    - errorHandler() - 0%
    - calculateInterest() - 0%
    - Edge cases for calculateCreditScore()

🔧 Generating 5 new test cases...

✅ Appended to credit.service.spec.ts:
  - ✅ should handle invalid user ID
  - ✅ should calculate interest correctly
  - ✅ should throw error when amount is negative
  - ✅ should handle edge case: zero amount
  - ✅ should validate interest rate range

📊 New Coverage: 85% (+20%)
```

---

### Generate Only Unit Tests

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --type unit
```

**Use case:** You want to focus on unit tests first.

**Output:**
```
🔍 Generating UNIT tests only...

✅ Generated 23 unit test cases across 4 files:
  - credit.service.spec.ts: 8 tests
  - payment.service.spec.ts: 10 tests
  - financial-calculator.spec.ts: 5 tests

💡 Consider adding integration tests later:
  /smartspec_generate_tests specs/feature/spec-004 --type integration
```

---

### Focus on Uncovered Code Only

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --focus uncovered --target-coverage 90
```

**Use case:** You already have good coverage and want to fill gaps.

**Output:**
```
🔍 Focusing on UNCOVERED code only...

📊 Current Coverage: 75%
🎯 Target: 90%

📝 Uncovered Functions:
  - credit.service.ts: errorHandler() (0%)
  - payment.service.ts: handleRefund() (0%)
  - financial-calculator.ts: calculateTax() (0%)

📝 Uncovered Branches:
  - credit.service.ts:45 - error path
  - payment.service.ts:67 - null check

🔧 Generating tests for uncovered code only...

✅ Generated 8 test cases:
  - 3 tests for uncovered functions
  - 5 tests for uncovered branches

📊 New Coverage: 91% (+16%)
```

---

### Dry Run (Preview Tests)

```bash
/smartspec_generate_tests specs/feature/spec-004-financial-system --dry-run
```

**Use case:** See what tests would be generated without creating them.

**Output:**
```
🔍 DRY RUN MODE - No tests will be created

📝 Would generate:

credit.service.spec.ts (APPEND):
  describe('CreditService', () => {
    describe('errorHandler', () => {
      it('should handle invalid user ID', () => {
        // Test implementation
      });
      
      it('should throw error when amount is negative', () => {
        // Test implementation
      });
    });
  });

payment.service.spec.ts (NEW FILE):
  describe('PaymentService', () => {
    describe('processPayment', () => {
      it('should process payment successfully', () => {
        // Test implementation
      });
      
      it('should handle payment failure', () => {
        // Test implementation
      });
    });
  });

...

💡 Run without --dry-run to create these tests
```

---

## 5. How It Works

### Phase 1: Analyze Current Coverage (Spec-Scoped)

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

**2. Check for Existing Test Files**

For each scoped file, check common test file patterns:
- `src/services/credit.service.spec.ts` (same directory)
- `src/services/__tests__/credit.service.test.ts` (Jest convention)
- `test/unit/services/credit.service.spec.ts` (separate test directory)
- `tests/services/credit.service.test.ts` (alternative)

**3. Analyze Existing Tests**

If test file exists:
```typescript
// credit.service.spec.ts
describe('CreditService', () => {
  describe('calculateCreditScore', () => {
    it('should calculate score correctly', () => { });
    it('should handle missing user', () => { });
  });
  // Missing: errorHandler(), calculateInterest()
});
```

**Result:**
```
✅ credit.service.spec.ts - EXISTS
   Current: 12 test cases, 65% coverage
   Missing: errorHandler(), calculateInterest()
   Action: Append 5 new test cases
```

**4. Run Coverage Report (Scoped)**
```bash
npm test -- --coverage --json \
  --testPathPattern="(credit|payment|transaction)" \
  --outputFile=coverage.json
```

Only run tests for scoped files.

---

### Phase 2: Detect Existing Tests (No Duplication!)

**Key Feature:** The workflow **detects existing test files** and **appends** new tests instead of overwriting.

**Detection Process:**

1. **Find test file**
   ```bash
   # Check common patterns
   ls src/services/credit.service.spec.ts
   ls src/services/__tests__/credit.service.test.ts
   ls test/unit/services/credit.service.spec.ts
   ```

2. **Parse existing tests**
   ```typescript
   // Extract test structure
   - describe('CreditService')
     - describe('calculateCreditScore')
       - it('should calculate score correctly')
       - it('should handle missing user')
     - describe('calculateInterest')  // ❌ Missing!
   ```

3. **Identify missing tests**
   ```
   Missing functions:
   - errorHandler() - no tests
   - calculateInterest() - no tests
   
   Missing edge cases:
   - calculateCreditScore() - no test for negative amount
   - calculateCreditScore() - no test for zero amount
   ```

4. **Generate only missing tests**
   ```typescript
   // Append to existing file
   describe('CreditService', () => {
     // ... existing tests ...
     
     // ✅ NEW: Appended tests
     describe('errorHandler', () => {
       it('should handle invalid user ID', () => { });
       it('should log error details', () => { });
     });
     
     describe('calculateInterest', () => {
       it('should calculate interest correctly', () => { });
       it('should handle zero rate', () => { });
     });
   });
   ```

**Result:** No duplicate tests, existing tests preserved!

---

### Phase 3: Generate Tests

**1. Prioritize by Coverage Gap**
- Functions with 0% coverage first
- Branches with low coverage
- Edge cases and error paths

**2. Generate Test Structure**
```typescript
describe('CreditService', () => {
  let service: CreditService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  
  beforeEach(() => {
    mockUserRepo = {
      findById: jest.fn(),
    } as any;
    service = new CreditService(mockUserRepo);
  });
  
  describe('calculateCreditScore', () => {
    it('should calculate score correctly', () => {
      // Arrange
      const userId = '123';
      mockUserRepo.findById.mockResolvedValue({ id: '123', name: 'John' });
      
      // Act
      const result = service.calculateCreditScore(userId);
      
      // Assert
      expect(result).toBe(750);
    });
    
    it('should handle invalid user ID', () => {
      // Arrange
      const userId = 'invalid';
      mockUserRepo.findById.mockResolvedValue(null);
      
      // Act & Assert
      expect(() => service.calculateCreditScore(userId)).toThrow('User not found');
    });
  });
});
```

**3. Append or Create File**

If test file exists:
```typescript
// Read existing file
const content = readFile('credit.service.spec.ts');

// Append new tests before closing brace
const newContent = content.replace(
  /}\);[\s]*$/,  // Last closing brace
  `  // ✅ Generated tests\n${newTests}\n});`
);

// Write back
writeFile('credit.service.spec.ts', newContent);
```

If test file doesn't exist:
```typescript
// Create new file
writeFile('credit.service.spec.ts', fullTestContent);
```

---

## 6. Test Types Generated

### Unit Tests

**Focus:** Individual functions in isolation

**Example:**
```typescript
describe('calculateInterest', () => {
  it('should calculate simple interest correctly', () => {
    const result = calculateInterest(1000, 0.05, 1);
    expect(result).toBe(50);
  });
  
  it('should handle zero principal', () => {
    const result = calculateInterest(0, 0.05, 1);
    expect(result).toBe(0);
  });
  
  it('should throw error for negative rate', () => {
    expect(() => calculateInterest(1000, -0.05, 1)).toThrow();
  });
});
```

---

### Integration Tests

**Focus:** Service interactions and dependencies

**Example:**
```typescript
describe('CreditService Integration', () => {
  let service: CreditService;
  let userRepo: UserRepository;
  let paymentService: PaymentService;
  
  beforeEach(() => {
    userRepo = new UserRepository();
    paymentService = new PaymentService();
    service = new CreditService(userRepo, paymentService);
  });
  
  it('should calculate credit score with payment history', async () => {
    const userId = '123';
    const user = await userRepo.findById(userId);
    const payments = await paymentService.getPaymentHistory(userId);
    
    const score = service.calculateCreditScore(userId);
    
    expect(score).toBeGreaterThan(700);
  });
});
```

---

### E2E Tests

**Focus:** Complete workflows from API to database

**Example:**
```typescript
describe('Credit API E2E', () => {
  it('should calculate credit score via API', async () => {
    const response = await request(app)
      .post('/api/credit/calculate')
      .send({ userId: '123' })
      .expect(200);
    
    expect(response.body).toMatchObject({
      userId: '123',
      score: expect.any(Number),
      rating: expect.stringMatching(/^(A|B|C|D|F)$/),
    });
  });
});
```

---

## 7. Coverage Metrics

### What Gets Measured

| Metric | Description | Target |
|--------|-------------|--------|
| **Lines** | % of code lines executed | 80%+ |
| **Statements** | % of statements executed | 80%+ |
| **Functions** | % of functions called | 80%+ |
| **Branches** | % of if/else paths taken | 70%+ |

### Coverage Report Example

```
📊 Coverage Report:

File                          | Lines  | Statements | Functions | Branches
------------------------------|--------|------------|-----------|----------
credit.service.ts             | 85.2%  | 87.5%      | 83.3%     | 75.0%
payment.service.ts            | 78.9%  | 80.0%      | 75.0%     | 70.0%
transaction.model.ts          | 95.0%  | 95.0%      | 100%      | 90.0%
credit.controller.ts          | 72.5%  | 75.0%      | 66.7%     | 60.0%
financial-calculator.ts       | 68.0%  | 70.0%      | 60.0%     | 55.0%
------------------------------|--------|------------|-----------|----------
Total                         | 79.9%  | 81.5%      | 77.0%     | 70.0%

🎯 Target: 80%
📈 Gap: 0.1% (almost there!)
```

---

## 8. Performance

### Execution Time

| Project Size | Files in Spec | Tests Generated | Time |
|-------------|---------------|-----------------|------|
| Small | 5 files | 20 tests | 30-60s |
| Medium | 10 files | 50 tests | 1-2 min |
| Large | 20 files | 100+ tests | 2-4 min |

**Why so fast?**
- Only analyzes files in spec scope
- Parallel test generation
- Reuses existing test structure

---

## 9. Best Practices

### 1. Start with Unit Tests

```bash
# Generate unit tests first
/smartspec_generate_tests specs/feature/spec-004 --type unit

# Then integration tests
/smartspec_generate_tests specs/feature/spec-004 --type integration

# Finally e2e tests
/smartspec_generate_tests specs/feature/spec-004 --type e2e
```

### 2. Incremental Coverage Increase

```bash
# Start with 70%
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 70

# Review and adjust tests

# Increase to 80%
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 80

# Finally aim for 90%
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 90
```

### 3. Review Generated Tests

```bash
# Generate tests
/smartspec_generate_tests specs/feature/spec-004

# Review
git diff

# Adjust edge cases manually
# Then run tests
npm test
```

### 4. Verify Coverage

```bash
# Generate tests
/smartspec_generate_tests specs/feature/spec-004 --target-coverage 80

# Run tests with coverage
npm test -- --coverage

# Verify target reached
```

---

## 10. Troubleshooting

### Issue: Tests not appending correctly

**Solution:** Check test file format. Workflow expects standard Jest/Mocha structure:
```typescript
describe('ServiceName', () => {
  // tests here
});
```

### Issue: Coverage not increasing

**Solution:** Run tests to verify they pass:
```bash
npm test
```

### Issue: Duplicate tests generated

**Solution:** This shouldn't happen! If it does, re-index first:
```bash
/smartspec_reindex_specs --spec specs/feature/spec-004
/smartspec_generate_tests specs/feature/spec-004
```

---

## 11. Related Workflows

Before generating tests:
- **`/smartspec_fix_errors`** - Fix errors first
- **`/smartspec_reindex_specs`** - Ensure accurate file list

After generating tests:
- **`/smartspec_refactor_code`** - Improve code quality
- **`/smartspec_verify_tasks_progress`** - Verify coverage target reached

---

## 12. Summary

The `smartspec_generate_tests` workflow is an intelligent test generator that analyzes coverage gaps and automatically creates missing tests. It **detects existing test files** and **appends** new tests instead of overwriting, preventing duplication.

**Key Benefits:**
- ✅ Spec-scoped for speed
- ✅ Detects existing tests (no duplication!)
- ✅ Appends instead of overwrites
- ✅ Generates unit, integration, and e2e tests
- ✅ Focuses on uncovered code
- ✅ Reaches target coverage automatically

**Next Steps:**
1. Run `/smartspec_generate_tests <spec_directory> --target-coverage 80`
2. Review generated tests
3. Run `npm test` to verify
4. Adjust edge cases if needed
5. Commit changes
