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
