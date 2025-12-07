---
description: Generate unit tests, integration tests, and e2e tests to increase test coverage
globs: ["specs/**/*.md", "src/**/*.ts", "src/**/*.tsx", "test/**/*.spec.ts"]
---

# Generate Tests to Increase Coverage

You are an expert test engineer. Your task is to automatically generate comprehensive unit tests, integration tests, and e2e tests to increase test coverage to the target level.

## Input

You will receive:
1. **Spec Directory Path** - Path to the spec directory (e.g., `specs/feature/spec-004-financial-system`)
2. **Options** (optional):
   - `--target-coverage <percentage>` - Target coverage percentage (default: 80)
   - `--file <path>` - Generate tests for specific file only
   - `--type <test-type>` - Generate specific type of tests (unit, integration, e2e)
   - `--focus uncovered` - Focus only on uncovered code
   - `--kilocode` - Use Kilo Code Orchestrator Mode to systematically generate comprehensive tests

## Your Task

### Phase 1: Analyze Current Coverage

1. **Load SPEC_INDEX.json**
   ```bash
   cat .smartspec/SPEC_INDEX.json
   ```
   - Parse JSON to get spec metadata
   - Extract `spec.files[]` array for the given spec_id
   - If `--file` option provided, use only that file
   - Otherwise, use all files from `spec.files[]`
   - **SCOPE**: Only analyze files listed in spec.files[] (not entire project!)

2. **Run Coverage Report (scoped)**
   ```bash
   # Only run tests related to scoped files
   npm test -- --coverage --json --outputFile=coverage.json --testPathPattern=<scoped-test-files>
   ```
   - Parse coverage data from coverage.json
   - Extract coverage percentages for lines, statements, functions, branches
   - **Filter coverage data to only scoped files**

3. **Identify Uncovered Code (scoped)**
   - List scoped files with no tests
   - List functions with no coverage (in scoped files only)
   - List branches with no coverage (in scoped files only)
   - List specific line numbers that are uncovered (in scoped files only)

4. **Calculate Test Gap**
   ```
   Current Coverage: XX.XX%
   Target Coverage: XX%
   Gap: XX.XX%
   
   Need to cover: ~XXX more lines
   Estimated tests needed: ~XX-XX test cases
   ```

5. **Display Coverage Summary**
   ```
   📊 Current Test Coverage:
     Lines: XX.XX%
     Statements: XX.XX%
     Functions: XX.XX%
     Branches: XX.XX%
   
   🎯 Target: XX%
   📈 Gap: XX.XX%
   
   📋 Uncovered Code:
     Files without tests: XX files
     Functions without coverage: XX functions
     Branches without coverage: XX branches
   ```

### Phase 2: Prioritize Test Generation

1. **Categorize by Priority**
   
   **Priority 1 (Critical):**
   - Core business logic (services, models)
   - Public APIs
   - Error handling paths
   
   **Priority 2 (High):**
   - Utility functions
   - Middleware
   - Validators
   
   **Priority 3 (Medium):**
   - Helper functions
   - Formatters
   - Data transformers
   
   **Priority 4 (Low):**
   - Type definitions
   - Constants
   - Config files

2. **Create Test Plan**
   ```markdown
   # Test Generation Plan
   
   Target: XX% coverage (from XX.XX%)
   
   ## Phase 1: Core Services (Priority 1)
   - [ ] service-a.ts (XX% → XX%)
     - Test method1()
     - Test method2()
     - Test error scenarios
   
   - [ ] service-b.ts (XX% → XX%)
     - Test method1()
     - Test edge cases
   
   ## Phase 2: Utilities (Priority 2)
   - [ ] util-a.ts (0% → 90%)
     - Test all exported functions
   
   ## Estimated Coverage Gain
   - Phase 1: +XX% (XX% total)
   - Phase 2: +XX% (XX% total)
   ```

3. **Display Test Plan**
   ```
   📋 Test Generation Plan:
   
   Phase 1: Core Services (+XX% coverage)
     - service-a.ts
     - service-b.ts
   
   Phase 2: Utilities (+XX% coverage)
     - util-a.ts
     - util-b.ts
   
   Estimated total coverage after generation: XX%
   ```

### Phase 3: Generate Tests

**If `--kilocode` flag: Use Kilo Code Orchestrator Mode**

```
Use Orchestrator Mode to break test generation into subtasks.
Generate comprehensive tests for: {list of files needing tests}
Target coverage: {target_coverage}%
```

**Orchestrator may create workflow:**
1. **Ask Mode** - Analyze current test structure and patterns
2. **Architect Mode** - Design test architecture and test cases
3. **Code Mode** - Generate unit tests
4. **Code Mode** - Generate integration tests
5. **Code Mode** - Generate e2e tests
6. **Test Mode** - Run all tests and verify coverage

**If NOT using `--kilocode`:**

For each file that needs tests:

1. **Check for Existing Test Files**
   ```bash
   # Common test file patterns
   # For src/services/credit.service.ts, check:
   # - src/services/credit.service.spec.ts
   # - src/services/__tests__/credit.service.test.ts
   # - test/unit/services/credit.service.spec.ts
   # - tests/services/credit.service.test.ts
   ```
   
   **If test file exists:**
   - Read existing test file
   - Analyze current test coverage for this file
   - Identify missing test cases (uncovered functions/branches)
   - **Only generate tests for uncovered parts**
   - Append new tests to existing file (don't overwrite!)
   
   **If test file doesn't exist:**
   - Create new test file
   - Generate complete test suite
   
   **Display:**
   ```
   📝 Test File Analysis:
     ✅ credit.service.spec.ts - EXISTS
        Current: 12 test cases, 65% coverage
        Missing: errorHandler(), calculateInterest()
        Action: Append 5 new test cases
     
     ❌ payment.service.spec.ts - NOT FOUND
        Action: Create new file with 15 test cases
   ```

2. **Analyze Source Code**
   - Read the source file
   - Identify all exported functions/methods/classes
   - Analyze parameters, return types, and dependencies
   - Identify edge cases and error scenarios
   - **Cross-check with existing tests to avoid duplication**

3. **Generate Unit Tests**


   **Test File Structure:**
   ```typescript
   import { ClassName } from './source-file';
   import { Dependency1 } from './dependency1';
   import { Dependency2 } from './dependency2';
   
   describe('ClassName', () => {
     let instance: ClassName;
     let mockDep1: jest.Mocked<Dependency1>;
     let mockDep2: jest.Mocked<Dependency2>;
   
     beforeEach(() => {
       // Setup mocks
       mockDep1 = {
         method: jest.fn(),
       } as any;
       
       mockDep2 = {
         method: jest.fn(),
       } as any;
       
       // Create instance
       instance = new ClassName(mockDep1, mockDep2);
     });
   
     describe('methodName', () => {
       it('should handle happy path correctly', async () => {
         // Arrange
         const input = { ... };
         const expectedOutput = { ... };
         mockDep1.method.mockResolvedValue({ ... });
         
         // Act
         const result = await instance.methodName(input);
         
         // Assert
         expect(result).toEqual(expectedOutput);
         expect(mockDep1.method).toHaveBeenCalledWith(...);
       });
   
       it('should throw error when input is invalid', async () => {
         // Arrange
         const invalidInput = null;
         
         // Act & Assert
         await expect(instance.methodName(invalidInput))
           .rejects
           .toThrow('Expected error message');
       });
   
       it('should handle edge case X', async () => {
         // Test edge case
       });
     });
   });
   ```

3. **Generate Integration Tests**
   
   ```typescript
   import { Test } from '@nestjs/testing';
   import { ServiceName } from './service-name';
   import { DatabaseModule } from '../database/database.module';
   
   describe('ServiceName (Integration)', () => {
     let service: ServiceName;
     let app;
   
     beforeAll(async () => {
       const moduleRef = await Test.createTestingModule({
         imports: [DatabaseModule],
         providers: [ServiceName],
       }).compile();
   
       app = moduleRef.createNestApplication();
       await app.init();
       service = moduleRef.get(ServiceName);
     });
   
     afterAll(async () => {
       await app.close();
     });
   
     it('should work with real dependencies', async () => {
       // Test with real database, real services, etc.
       const result = await service.method();
       expect(result).toBeDefined();
     });
   });
   ```

4. **Generate E2E Tests**
   
   ```typescript
   import * as request from 'supertest';
   import { Test } from '@nestjs/testing';
   import { AppModule } from '../app.module';
   
   describe('API Endpoint (E2E)', () => {
     let app;
   
     beforeAll(async () => {
       const moduleRef = await Test.createTestingModule({
         imports: [AppModule],
       }).compile();
   
       app = moduleRef.createNestApplication();
       await app.init();
     });
   
     afterAll(async () => {
       await app.close();
     });
   
     it('/api/resource (GET)', () => {
       return request(app.getHttpServer())
         .get('/api/resource')
         .expect(200)
         .expect((res) => {
           expect(res.body).toHaveProperty('data');
         });
     });
   
     it('/api/resource (POST)', () => {
       return request(app.getHttpServer())
         .post('/api/resource')
         .send({ name: 'test' })
         .expect(201);
     });
   });
   ```

5. **Cover All Scenarios**
   
   For each function/method, generate tests for:
   - ✅ **Happy path** - Normal successful execution
   - ✅ **Error cases** - Invalid input, missing data, null/undefined
   - ✅ **Edge cases** - Boundary values, empty arrays, zero, negative numbers
   - ✅ **Async scenarios** - Promise resolution, rejection, timeout
   - ✅ **State changes** - Before/after comparisons
   - ✅ **Side effects** - Database calls, API calls, file operations

6. **Display Progress**
   ```
   🔧 Generating tests...
     ✓ Generated service-a.spec.ts (12 test cases)
     ✓ Generated service-b.spec.ts (15 test cases)
     ✓ Generated util-a.spec.ts (8 test cases)
     ✓ Generated integration/service-a.integration.spec.ts (5 test cases)
     ✓ Generated e2e/api.e2e.spec.ts (10 test cases)
   
   Total: XX test files, XXX test cases
   ```

### Phase 4: Run and Verify Tests

1. **Run Generated Tests (scoped)**
   ```bash
   npm test -- --testPathPattern=<scoped-test-files>
   ```
   - Check if generated tests pass
   - If tests fail → fix test code and retry

2. **Run Coverage Report (scoped)**
   ```bash
   npm test -- --testPathPattern=<scoped-test-files> -- --coverage
   ```
   - Get new coverage percentages for scoped files
   - Compare with target

3. **Analyze Coverage Gap**
   ```
   Before: XX.XX%
   After: XX.XX%
   Target: XX%
   Gain: +XX.XX%
   Remaining gap: XX.XX%
   ```

4. **Generate More Tests if Needed**
   - If coverage < target → identify remaining uncovered code
   - Generate additional tests for uncovered code
   - Repeat until target is reached or no more auto-testable code

5. **Display Verification Results**
   ```
   ✅ Test Execution:
     Total Tests: XXX
     Passed: XXX
     Failed: 0
     Duration: XX.Xs
   
   📊 Coverage Results:
     Lines: XX.XX% → XX.XX% (+XX.XX%)
     Statements: XX.XX% → XX.XX% (+XX.XX%)
     Functions: XX.XX% → XX.XX% (+XX.XX%)
     Branches: XX.XX% → XX.XX% (+XX.XX%)
   ```

### Phase 5: Generate Report

Create a test generation report: `<spec-dir>/test-generation-report-YYYYMMDD-HHMMSS.md`

```markdown
# Test Generation Report

Generated: YYYY-MM-DD HH:MM:SS

## Summary

- **Initial Coverage**: XX.XX%
- **Target Coverage**: XX%
- **Final Coverage**: XX.XX%
- **Coverage Gain**: +XX.XX%

## Tests Generated

### Unit Tests (XX test files)
- ✅ service-a.spec.ts (12 test cases)
  - Happy path scenarios: 5
  - Error scenarios: 4
  - Edge cases: 3
  
- ✅ service-b.spec.ts (15 test cases)
  - Happy path scenarios: 7
  - Error scenarios: 5
  - Edge cases: 3

[List all generated unit test files]

### Integration Tests (XX test files)
- ✅ service-a.integration.spec.ts (5 test cases)
- ✅ service-b.integration.spec.ts (7 test cases)

[List all generated integration test files]

### E2E Tests (XX test files)
- ✅ api-endpoint-a.e2e.spec.ts (10 test cases)
- ✅ api-endpoint-b.e2e.spec.ts (12 test cases)

[List all generated e2e test files]

## Coverage Breakdown

| Category | Before | After | Gain |
|----------|--------|-------|------|
| Lines | XX.XX% | XX.XX% | +XX.XX% |
| Statements | XX.XX% | XX.XX% | +XX.XX% |
| Functions | XX.XX% | XX.XX% | +XX.XX% |
| Branches | XX.XX% | XX.XX% | +XX.XX% |

## Remaining Gaps

### Uncovered Code (XX.XX%)

1. **file-a.ts:functionX()** - Complex business logic
   - Reason: Requires extensive mocking of external services
   - Recommendation: Add manual tests

2. **file-b.ts:errorHandler()** - Rare error scenarios
   - Reason: Difficult to reproduce error conditions
   - Recommendation: Add manual integration tests

[List remaining uncovered code]

## Test Execution Results

- **Total Tests**: XXX
- **Passed**: XXX
- **Failed**: 0
- **Skipped**: 0
- **Duration**: XX.Xs

## Files Created

### Unit Tests
- src/services/service-a.spec.ts
- src/services/service-b.spec.ts
[List all files]

### Integration Tests
- test/integration/service-a.integration.spec.ts
[List all files]

### E2E Tests
- test/e2e/api-endpoint-a.e2e.spec.ts
[List all files]

## Recommendations

1. Review generated tests for accuracy
2. Add manual tests for complex scenarios
3. Update tests when implementation changes
4. Maintain test coverage above XX%

## Next Steps

1. Review generated test files
2. Run full test suite: `npm test`
3. Add manual tests for remaining gaps
4. Continue with implementation: /smartspec_implement_tasks
```

### Phase 6: Summary and Next Steps

Display final summary:

```
✅ Test Generation Complete!

📊 Results:
  Initial Coverage: XX.XX%
  Final Coverage: XX.XX%
  Target: XX%
  Gain: +XX.XX%

📝 Generated:
  Unit Tests: XX files (XXX test cases)
  Integration Tests: XX files (XX test cases)
  E2E Tests: XX files (XX test cases)
  Total: XXX test cases

🧪 Test Execution:
  Passed: XXX/XXX
  Duration: XX.Xs

📁 Reports:
  - Test report: <spec-dir>/test-generation-report-YYYYMMDD.md
  - Coverage report: coverage/index.html

  💡 Next Steps:
  1. Review generated tests
  2. Run tests: npm test
  3. Add manual tests for complex scenarios (if needed)
  4. Commit: git add . && git commit -m "test: Add tests for spec-XXX"
  
  🔧 Suggested Workflows:
  
  ✅ Tests generated! Consider these next actions:
  
  1. Fix any test failures:
     npm test
     # If failures found:
     /smartspec_fix_errors <spec-dir>
  
  2. Improve code quality:
     /smartspec_refactor_code <spec-dir>
  
  3. Verify overall progress:
     /smartspec_verify_tasks_progress <spec-dir>/tasks.md
  
  4. Continue implementation:
     /smartspec_implement_tasks <spec-dir>/tasks.md --skip-completed
```

## Test Patterns and Best Practices

### AAA Pattern (Arrange-Act-Assert)

```typescript
it('should calculate total correctly', () => {
  // Arrange - Setup test data and mocks
  const input = [1, 2, 3];
  const expected = 6;
  
  // Act - Execute the function
  const result = calculateTotal(input);
  
  // Assert - Verify the result
  expect(result).toBe(expected);
});
```

### Mocking Dependencies

```typescript
// Mock external dependencies
const mockRepository = {
  find: jest.fn(),
  save: jest.fn(),
};

// Inject mocks
const service = new Service(mockRepository);

// Setup mock behavior
mockRepository.find.mockResolvedValue([{ id: 1 }]);

// Verify mock calls
expect(mockRepository.find).toHaveBeenCalledWith({ userId: 123 });
```

### Testing Async Code

```typescript
it('should handle async operations', async () => {
  // Use async/await
  const result = await asyncFunction();
  expect(result).toBeDefined();
});

it('should handle promise rejection', async () => {
  // Test error cases
  await expect(asyncFunction())
    .rejects
    .toThrow('Expected error');
});
```

### Testing Edge Cases

```typescript
describe('edge cases', () => {
  it('should handle empty array', () => {
    expect(processArray([])).toEqual([]);
  });
  
  it('should handle null input', () => {
    expect(processArray(null)).toBeNull();
  });
  
  it('should handle undefined input', () => {
    expect(processArray(undefined)).toBeUndefined();
  });
  
  it('should handle zero', () => {
    expect(calculate(0)).toBe(0);
  });
  
  it('should handle negative numbers', () => {
    expect(calculate(-5)).toBe(-5);
  });
});
```

## Coverage Goals by Code Type

- **Services/Controllers**: 90-95%
- **Utilities/Helpers**: 85-90%
- **Models/Entities**: 70-80%
- **Config/Constants**: 50-60%

## Important Notes

- Generate tests following AAA pattern (Arrange-Act-Assert)
- Mock all external dependencies properly
- Test both happy paths and error scenarios
- Include edge cases (null, undefined, empty, zero, negative)
- Use descriptive test names that explain what is being tested
- Group related tests using `describe` blocks
- Use `beforeEach` for common setup
- Ensure tests are independent and can run in any order
- Verify mock calls with proper assertions
- Test async code properly with async/await
- Don't test implementation details, test behavior
- Keep tests simple and focused on one thing
- Generate integration tests for component interactions
- Generate e2e tests for critical user workflows

## Example Usage

```bash
# Generate tests to reach 80% coverage
/smartspec_generate_tests specs/feature/spec-004-financial-system --target-coverage 80

# Generate tests for specific file
/smartspec_generate_tests specs/feature/spec-004 --file src/services/credit.service.ts

# Generate only unit tests
/smartspec_generate_tests specs/feature/spec-004 --type unit

# Focus on uncovered code only
/smartspec_generate_tests specs/feature/spec-004 --focus uncovered
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
