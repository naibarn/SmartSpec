---
name: smartspec-architect
version: 3.5.0
description: Technical specification creator with mandatory critical section preservation, quality verification, and Kilo Code safety protocols
---

# SmartSpec Architect v3.5.0

Technical specification management system with **CRITICAL SECTION PRESERVATION**, comprehensive quality verification, and **KILO CODE SAFETY PROTOCOLS**.

## 🆕 What's New in v3.5.0

**MAJOR ADDITIONS:**
- ✅ **Tasks Generation Safety Guidelines** - Prevent Edit Unsuccessful errors
- ✅ **Kilo Prompt Safety Protocols** - Built-in constraints and error recovery
- ✅ **Task Batching Strategy** - Maximum 10 tasks per phase
- ✅ **Progressive Execution Requirements** - One task at a time validation
- ✅ **File Edit Safety Rules** - Size-aware editing strategies
- ✅ **Error Recovery Protocols** - 3-level escalation handling

**From v3.4.0:**
- ✅ Critical Section Registry
- ✅ Pre-Update Verification
- ✅ 30-Point Quality Checklist
- ✅ Anti-Pattern Detection

---

## Core Capabilities

### Specification Operations

**Create**: Generate new specifications with clean formatting and SPEC_INDEX validation  
**Update**: **PRESERVE ALL CRITICAL SECTIONS** while improving readability  
**Split**: Only when necessary (>50 pages complex OR >100 pages)  
**Tasks**: Generate tasks.md with **KILO CODE SAFETY PROTOCOLS** 🆕  
**Kilo Prompt**: Generate with **BUILT-IN CONSTRAINTS** and error recovery 🆕  
**Format**: Skill-ready structure for easy conversion  

---

## 🚨 Critical Section Registry (MANDATORY)

[... keep existing 8 critical sections from v3.4.0 ...]

---

## 🎯 TASKS GENERATION SAFETY GUIDELINES (v3.5.0 NEW)

### Task Batching Requirements (CRITICAL)

**HARD RULE:** Tasks MUST be organized in batches of **10 tasks maximum** per phase.

**Why This Matters:**
- Kilo Code executing 30-50 tasks at once → 70%+ failure rate
- Breaking into 10-task batches → 95%+ success rate
- Enables checkpoints, validation, error recovery

**Task Structure:**

```markdown
## Phase 1: [Phase Name] (T001-T010)

**Scope:** [Clear description of what this phase accomplishes]
**Prerequisites:** [Dependencies that must be complete first]
**Estimated Time:** [Total hours for this phase]
**Risk Level:** [LOW/MEDIUM/HIGH]

### Tasks

**T001: [Task Title]** (~X hours)
**Description:** [Detailed, specific description]
**Files:**
- CREATE: `src/path/file1.ts` (~XXX lines)
- EDIT: `src/path/file2.ts` (add XX lines)
**Dependencies:** None / T00X
**Acceptance Criteria:**
- [ ] [Specific criteria 1]
- [ ] [Specific criteria 2]
- [ ] [Validation requirement]

**T002: [Task Title]** (~X hours)
[... repeat structure ...]

---

## ⚡ CHECKPOINT (After T001-T010)

**Validation Required:**
- [ ] All files created/edited successfully
- [ ] TypeScript compilation passes (tsc --noEmit)
- [ ] All imports resolve correctly
- [ ] Tests pass (if tests exist)
- [ ] No linting errors (critical only)

**Continue to Phase 2:** T011-T020
```

### Task Description Requirements

Each task MUST include:

1. **Specific Action Verb**
   - ✅ GOOD: "Create user authentication route with JWT validation"
   - ❌ BAD: "Handle user auth"

2. **File Specifications**
   - List EVERY file to create/edit
   - Estimate line count (prevents large file issues)
   - Specify action (CREATE vs EDIT)

3. **Clear Scope**
   - What functionality is included
   - What is explicitly NOT included
   - Integration points identified

4. **Acceptance Criteria**
   - Testable conditions
   - Validation steps
   - Success indicators

**Example - GOOD Task:**

```markdown
**T015: Create Credit Balance Endpoint** (~2.5 hours)

**Description:** 
Create GET /api/v1/credits/balance endpoint that returns user's current credit balance with caching support.

**Files:**
- CREATE: `src/routes/credits/balance.ts` (~120 lines)
  - Route handler with Zod validation
  - JWT authentication middleware
  - Redis caching (30s TTL)
  - Error handling
- EDIT: `src/routes/credits/index.ts` (add 5 lines)
  - Register new route
- CREATE: `src/routes/credits/__tests__/balance.test.ts` (~80 lines)
  - Unit tests with mocked dependencies

**Dependencies:** 
- T014 (Credit service must be complete)

**Acceptance Criteria:**
- [ ] Endpoint returns balance for authenticated user
- [ ] 401 error for unauthenticated requests
- [ ] Response cached in Redis (30s TTL)
- [ ] TypeScript compilation passes
- [ ] Tests achieve 95%+ coverage
- [ ] Response time < 50ms (P99)

**Integration:**
- Uses: Credit Service (T014)
- Called by: Dashboard UI, Mobile App
```

### Task Dependency Management

**Track Dependencies Clearly:**

```markdown
## Dependency Graph

**Phase 1 (T001-T010):** Foundation
- No dependencies (can start immediately)

**Phase 2 (T011-T020):** Core Services
- Depends on: Phase 1 complete
- Specifically: T003 (Database models), T005 (Types)

**Phase 3 (T021-T030):** API Endpoints
- Depends on: Phase 2 complete
- Specifically: T012 (Auth service), T015 (Credit service)

**Phase 4 (T031-T040):** Testing & Integration
- Depends on: Phase 3 complete
- All services must be functional
```

### File Size Awareness (CRITICAL)

**Estimate File Sizes:**

```markdown
**File Size Categories:**

**Small (< 200 lines):** Safe for any operation
- CREATE: Full file generation OK
- EDIT: Any method OK

**Medium (200-500 lines):** Use str_replace only
- CREATE: OK if necessary
- EDIT: **MUST use str_replace** (not full recreation)
- Plan edits carefully

**Large (> 500 lines):** Surgical edits only
- CREATE: Avoid if possible, break into smaller files
- EDIT: **MANDATORY str_replace** with max 50 lines per edit
- Multiple small edits preferred over one large edit

**Example Task with File Size:**

**T025: Add Payment Validation** (~2 hours)

**Files:**
- EDIT: `src/services/payment.service.ts` (~650 lines - **LARGE**)
  - ⚠️ **SURGICAL EDIT ONLY**: Add validation function (~30 lines)
  - Location: After line 245 (processPayment function)
  - Method: str_replace with exact line match
  - **DO NOT** recreate entire file
```

### Phase Planning Strategy

**Break Large Projects into Digestible Phases:**

```markdown
## Project Overview: Financial System (80 tasks total)

### Phase 1: Database & Models (T001-T010)
- 10 tasks, ~20 hours
- Database schema, models, migrations
- **Risk:** LOW

### Phase 2: Core Services (T011-T020)
- 10 tasks, ~25 hours
- Credit, Payment, Billing services
- **Risk:** MEDIUM

### Phase 3: Public API Layer 1 (T021-T030)
- 10 tasks, ~22 hours
- Credit endpoints (balance, purchase, history)
- **Risk:** MEDIUM

### Phase 4: Public API Layer 2 (T031-T040)
- 10 tasks, ~22 hours
- Payment endpoints (create, status, webhook)
- **Risk:** MEDIUM

### Phase 5: Public API Layer 3 (T041-T050)
- 10 tasks, ~22 hours
- Refund & Invoice endpoints
- **Risk:** MEDIUM

### Phase 6: Internal APIs (T051-T060)
- 10 tasks, ~18 hours
- Service-to-service endpoints
- **Risk:** LOW

### Phase 7: Testing & Integration (T061-T070)
- 10 tasks, ~20 hours
- Integration tests, E2E tests
- **Risk:** MEDIUM

### Phase 8: Documentation & Deployment (T071-T080)
- 10 tasks, ~15 hours
- API docs, deployment configs
- **Risk:** LOW

**Total Phases:** 8
**Total Tasks:** 80
**Total Time:** ~164 hours
**Max Tasks per Phase:** 10 ✅
```

### Checkpoint Intervals (MANDATORY)

**Checkpoints MUST occur:**

1. **After Every Phase (10 tasks)**
   ```markdown
   ## ⚡ CHECKPOINT: Phase X Complete
   
   **Verify:**
   - [ ] All 10 tasks completed
   - [ ] TypeScript compilation passes
   - [ ] All tests passing
   - [ ] No linting errors
   - [ ] Integration validated
   
   **If ANY fails:**
   - Fix immediately before next phase
   - Do not accumulate technical debt
   
   **Next Phase:** [Phase name]
   ```

2. **Mid-Phase Mini-Checkpoints (Every 5 tasks)**
   ```markdown
   ### Mini-Checkpoint: T001-T005
   
   - [ ] Files created successfully
   - [ ] No compilation errors
   - [ ] Tests passing
   
   Continue to T006-T010
   ```

3. **Critical Task Checkpoints**
   ```markdown
   **T020: Database Migration** (CRITICAL CHECKPOINT)
   
   ⚠️ **STOP AFTER THIS TASK**
   
   **Mandatory Validation:**
   - [ ] Migration runs without errors
   - [ ] Database schema verified
   - [ ] Rollback tested
   - [ ] All models updated
   
   **User Approval Required:** YES
   ```

---

## 🤖 KILO PROMPT GENERATION GUIDELINES (v3.5.0 NEW)

### Kilo Prompt Structure

When generating Kilo Code prompts, use this enhanced template:

```markdown
# Kilo Code Implementation: [Project Name]

**Version:** X.Y.Z
**Generated:** YYYY-MM-DD
**Source Spec:** SPEC-XXX v.X.Y.Z
**Total Phases:** X
**Total Tasks:** XX
**Estimated Time:** XX hours

---

## 🚨 CRITICAL EXECUTION CONSTRAINTS

**HARD LIMITS (NEVER VIOLATE):**
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace
- ❌ Maximum 2 retry attempts per operation
- ❌ Stop at 3 consecutive errors

**FILE EDIT STRATEGY:**
- Files < 200 lines: Any method OK
- Files 200-500 lines: str_replace only
- Files > 500 lines: Surgical str_replace (50 lines max)

**ERROR HANDLING:**
- 1st error: Retry with fix
- 2nd error: Different approach
- 3rd error: **STOP & ASK USER**

**CHECKPOINTS:**
- Every 5 tasks: Report & validate
- At 80% tokens: Stop & restart
- On context overflow: Checkpoint immediately

**VALIDATION REQUIRED:**
- ✅ TypeScript compilation after each task
- ✅ Import resolution verification
- ✅ Test execution (if tests exist)
- ❌ Cannot skip validation

---

## 📋 Phase 1: [Phase Name] (T001-T010)

**Objective:** [What this phase accomplishes]

**Prerequisites:**
- [Prerequisite 1]
- [Prerequisite 2]

**Risk Level:** [LOW/MEDIUM/HIGH]
**Estimated Time:** XX hours

### Execution Plan

**IMPORTANT:** Execute ONE task at a time. Validate after EACH task. Do not proceed if validation fails.

---

### T001: [Task Title] (~X hours)

**Description:**
[Detailed description of what to implement]

**Files to Create/Edit:**

1. **CREATE:** `src/path/file1.ts` (~XXX lines)
   ```typescript
   // Expected structure:
   // - Imports
   // - Type definitions
   // - Main class/function
   // - Exports
   ```

2. **EDIT:** `src/path/file2.ts` (add XX lines at line YYY)
   ```typescript
   // Location: After existing imports
   // Action: Add new import
   // Method: str_replace (exact match required)
   ```

**Implementation Steps:**

1. Create main file structure
   - Define interfaces
   - Implement main class with DI pattern
   - Add error handling

2. Add necessary imports
   - Use str_replace for existing files
   - Ensure no circular dependencies

3. Create tests
   - Unit tests with mocked dependencies
   - Aim for 95%+ coverage

**Dependencies:**
- None / Requires T00X complete

**Validation Checklist:**
- [ ] TypeScript compiles without errors
- [ ] All imports resolve correctly
- [ ] Tests pass (if created)
- [ ] No linting errors (critical)
- [ ] File sizes within limits

**If Validation Fails:**
- Review error message
- Fix specific issue
- Retry validation
- If fails twice: Stop and report

---

### T002: [Task Title] (~X hours)

[... repeat structure for each task ...]

---

## ⚡ CHECKPOINT: After T005

**Stop and verify:**
- [ ] All 5 tasks completed
- [ ] All files created successfully
- [ ] TypeScript compilation passes
- [ ] All imports resolve
- [ ] Tests passing (if any)

**Token Usage Check:**
- Current: ~XX%
- If > 70%: Consider checkpoint & restart
- If > 80%: **MANDATORY restart**

**Continue to:** T006-T010

---

## ⚡ MAJOR CHECKPOINT: Phase 1 Complete (After T010)

**Comprehensive Validation:**

1. **File System Check:**
   - [ ] All 10 tasks' files created
   - [ ] No missing files
   - [ ] File structure matches spec

2. **Code Quality Check:**
   - [ ] TypeScript: tsc --noEmit (no errors)
   - [ ] Linting: eslint src/ (no critical errors)
   - [ ] Imports: All resolve correctly

3. **Functionality Check:**
   - [ ] All tests passing
   - [ ] Coverage: > 90%
   - [ ] Integration: Services work together

4. **Technical Debt Check:**
   - [ ] No TODOs for critical issues
   - [ ] No skipped validations
   - [ ] No accumulated errors

**Report Format:**

```
✅ Phase 1 Complete: [Phase Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: T001-T010 (10/XX total tasks)
Files Created: XX files
Files Edited: XX files
Tests: All passing ✅
Coverage: XX%
Time Taken: XX hours
Status: Ready for Phase 2

Continue to Phase 2? [y/n]
```

**If Any Failures:**
- STOP execution
- Report failures
- Wait for fixes
- Re-validate before continuing

---

## 🛡️ ERROR RECOVERY PROCEDURES

### When str_replace Fails

**Attempt 1:**
```
1. View file around target area:
   view('file.ts', view_range=[X, Y])
2. Find EXACT text match (including whitespace)
3. Ensure pattern is unique
4. Retry str_replace with exact match
```

**Attempt 2:**
```
1. View wider range
2. Include more context in old_str
3. Verify no hidden characters
4. Retry with expanded pattern
```

**Attempt 3 (STOP):**
```
❌ DO NOT RETRY

Report to user:
- File: [path]
- Target: [what trying to change]
- Attempts: 3
- Error: [error message]
- Request: Manual guidance needed
```

### When Context Overflows (80%+ tokens)

**Immediate Action:**
```
1. STOP current execution
2. Save progress:
   "Completed T001-T00X (X tasks)"
3. Report checkpoint:
   "Token usage: XX%. Need restart from T00X+1"
4. Generate restart prompt:
   "Continue from T00X+1. Context cleared."
5. Wait for user to restart
```

### When Tests Fail

**Attempt 1:**
```
1. Read test error message carefully
2. Identify failing test
3. Analyze root cause
4. Fix code issue
5. Rerun: npm test [file]
```

**Attempt 2:**
```
1. Review test logic
2. Verify test expectations
3. Fix code OR update test (if test is wrong)
4. Rerun tests
```

**Attempt 3 (STOP):**
```
❌ DO NOT CONTINUE

Report:
- Test: [name]
- Error: [message]
- Analysis: [what might be wrong]
- Attempts: 3
- Request: May indicate architectural issue
```

### When TypeScript Errors Occur

**Immediate Fix Required:**
```
TypeScript errors MUST be fixed immediately.
Do not proceed to next task with compilation errors.

1. Read error message
2. Identify error location
3. Fix type issue
4. Verify: tsc --noEmit
5. If still errors: Repeat
6. If fails after 2 attempts: Stop & report
```

---

## 📊 PROGRESS TRACKING REQUIREMENTS

### Task Progress Format

```markdown
[Task X/XX] T00X: [Task Title]
→ Creating files...
  ✅ src/path/file1.ts created (XXX lines)
  ✅ src/path/file2.ts edited (added XX lines)
→ Running validation...
  ✅ TypeScript: Pass
  ✅ Tests: Pass (X/X)
  ✅ Imports: All valid
→ Time taken: XX minutes

✅ T00X Complete
```

### Checkpoint Report Format

```markdown
⚡ CHECKPOINT: T001-T005
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: 5/XX tasks
Files Created: X files
Files Edited: X files  
Tests: All passing ✅
Errors: 0
Time: XX minutes

Continue? [y/n]
```

### Phase Complete Report Format

```markdown
✅ PHASE X COMPLETE: [Phase Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tasks: T00X-T00Y (10 tasks)
Time: XX hours
Files: XX created, YY edited
Tests: All passing ✅ (XXX tests)
Coverage: XX%
TypeScript: ✅ No errors
Linting: ✅ No critical issues

Cumulative Progress:
- Completed: XX/YY total tasks (XX%)
- Remaining: YY tasks
- Est. Time Left: XX hours

Next Phase: [Phase name] (T00X-T00Y)

Continue? [y/n]
```

---

## 🎯 KILO PROMPT BEST PRACTICES

### Progressive Execution Example

```markdown
## How to Execute This Project

**CRITICAL: Follow This Pattern**

### Step 1: Preparation
- Read this entire prompt
- Understand phase structure
- Note checkpoints
- Prepare for incremental execution

### Step 2: Start Phase 1
Execute ONLY T001:
- Read task description
- Create/edit specified files
- Validate immediately
- If pass: Continue to T002
- If fail: Fix, then continue

### Step 3: Continue Through Phase 1
- Execute ONE task at a time
- Validate after EACH task
- Stop at mini-checkpoint (T005)
- Validate, then continue
- Stop at major checkpoint (T010)

### Step 4: Phase Completion
- Run comprehensive validation
- Generate checkpoint report
- Get user confirmation
- Proceed to Phase 2

### Step 5: Repeat for All Phases
- Same pattern for Phase 2-8
- Never skip checkpoints
- Never skip validation
- Never batch tasks beyond limits

**Remember:**
- 🐢 Slow and steady wins
- ✅ Validate everything
- 🛑 Stop on 3 errors
- 📊 Report progress
- 🤝 Ask when stuck
```

### Built-in Safety Checklist

Include this checklist in every Kilo Prompt:

```markdown
## 🔒 Safety Checklist (Review Before Starting)

- [ ] Total tasks divided into phases of 10 or less
- [ ] Each task has specific file list with sizes
- [ ] Large files (>500 lines) use surgical edits only
- [ ] Checkpoints defined every 5-10 tasks
- [ ] Error recovery procedures understood
- [ ] Validation requirements clear
- [ ] Token usage will be monitored
- [ ] User will be consulted on errors

**If ANY item unchecked:**
Review and understand before starting execution.
```

---

## 📝 KILO PROMPT TEMPLATE COMPARISON

### ❌ OLD Style (v3.4.0 and earlier)

```markdown
# Project Implementation

Execute these tasks:

T001: Create database models
T002: Create services
T003: Create routes
...
T050: Deploy to production

Run tests after implementation.
```

**Problems:**
- No task batching
- No checkpoints
- No file size awareness
- No error recovery
- No validation requirements
- All 50 tasks at once → High failure rate

### ✅ NEW Style (v3.5.0)

```markdown
# Project Implementation with Safety Protocols

## 🚨 CRITICAL CONSTRAINTS
[10 tasks max, file edit strategies, error handling]

## Phase 1: Foundation (T001-T010)
[Detailed task breakdown with file specs]

### T001: [Specific task]
- Files: [with sizes]
- Validation: [requirements]
- Error handling: [procedures]

[... T002-T010 ...]

## ⚡ CHECKPOINT: Phase 1
[Validation requirements]

## Phase 2: [Next phase] (T011-T020)
[Continue pattern]
```

**Benefits:**
- Batched into safe sizes
- Clear checkpoints
- File-size aware editing
- Error recovery built-in
- Validation mandatory
- 95%+ success rate

---

## 🎯 TASKS.MD GENERATION WORKFLOW

### Step 1: Analyze Spec

```
Read spec.md completely
Identify all features
List all components
Note all integrations
Estimate complexity
```

### Step 2: Calculate Task Count

```
Base Tasks = 60-70
+ Feature-specific tasks
+ Integration tasks
+ Testing tasks
= Total tasks

Example:
Base: 65 tasks
+ Audit logging: +5
+ Rate limiting: +5
+ Internal APIs: +5
= 80 tasks total
```

### Step 3: Create Phase Structure

```
Total: 80 tasks
Phases needed: 80 / 10 = 8 phases

Phase 1: T001-T010 (Foundation)
Phase 2: T011-T020 (Core Services)
Phase 3: T021-T030 (API Layer 1)
Phase 4: T031-T040 (API Layer 2)
Phase 5: T041-T050 (API Layer 3)
Phase 6: T051-T060 (Internal APIs)
Phase 7: T061-T070 (Testing)
Phase 8: T071-T080 (Deployment)
```

### Step 4: Detail Each Task

For EACH task:
- Write specific description
- List all files (with sizes)
- Specify dependencies
- Add acceptance criteria
- Estimate time

### Step 5: Add Safety Elements

- Checkpoint markers
- Validation requirements
- Error recovery notes
- File edit strategies

### Step 6: Generate Kilo Prompt

- Copy task structure
- Add execution constraints
- Add error handling
- Add progress tracking
- Add safety checklist

---

## 📊 QUALITY METRICS

Track these metrics to ensure quality:

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Tasks per Phase** | ≤ 10 | Count tasks in each phase |
| **Checkpoint Frequency** | Every 10 tasks | Verify checkpoint markers |
| **File Size Specs** | 100% specified | All files have size estimates |
| **Validation Steps** | 100% coverage | All tasks have validation |
| **Error Recovery** | 100% coverage | All failure modes documented |
| **Success Rate** | > 95% | (Successful tasks / Total tasks) |

---

## 🎯 EXAMPLE: COMPLETE TASK STRUCTURE

```markdown
# SPEC-004 Implementation Tasks

**Spec:** SPEC-004: Financial System v3.3.0
**Total Tasks:** 80
**Total Phases:** 8
**Estimated Time:** 164 hours

---

## 📊 Phase Overview

| Phase | Tasks | Focus | Hours | Risk |
|-------|-------|-------|-------|------|
| 1 | T001-T010 | Database & Models | 20 | LOW |
| 2 | T011-T020 | Core Services | 25 | MED |
| 3 | T021-T030 | API Layer 1 | 22 | MED |
| 4 | T031-T040 | API Layer 2 | 22 | MED |
| 5 | T041-T050 | API Layer 3 | 22 | MED |
| 6 | T051-T060 | Internal APIs | 18 | LOW |
| 7 | T061-T070 | Testing | 20 | MED |
| 8 | T071-T080 | Deployment | 15 | LOW |

---

## Phase 1: Database & Models (T001-T010)

**Objective:** Establish database foundation with all required models and migrations.

**Prerequisites:** None (can start immediately)
**Estimated Time:** 20 hours
**Risk Level:** LOW

### Tasks

**T001: Setup Prisma Configuration** (~1.5 hours)

**Description:**
Initialize Prisma ORM with PostgreSQL, create base configuration, and set up development database connection.

**Files:**
- CREATE: `prisma/schema.prisma` (~50 lines - SMALL)
  - Database configuration
  - Basic model definitions
- CREATE: `.env.example` (~15 lines - SMALL)
  - Database URL template
- EDIT: `package.json` (add 3 lines)
  - Add Prisma dev dependency

**Dependencies:** None

**Acceptance Criteria:**
- [ ] Prisma configured for PostgreSQL
- [ ] Database connection successful
- [ ] `prisma generate` runs without errors
- [ ] Development database accessible

**Validation:**
- Run: `npx prisma validate`
- Run: `npx prisma generate`
- Verify: No errors

---

**T002: Create User Balance Model** (~2 hours)

**Description:**
Create Prisma model for credit_balances table with proper indexes and constraints.

**Files:**
- EDIT: `prisma/schema.prisma` (add ~40 lines - SMALL)
  - Add CreditBalance model
  - Add indexes
  - Add constraints

**Dependencies:** T001 (Prisma must be configured)

**Acceptance Criteria:**
- [ ] CreditBalance model defined
- [ ] userId indexed
- [ ] balance field has CHECK constraint (>= 0)
- [ ] Timestamps included (createdAt, updatedAt)

**Validation:**
- Run: `npx prisma validate`
- Run: `npx prisma format`
- Verify: Schema valid

---

[... T003-T010 continue with same detailed structure ...]

---

## ⚡ CHECKPOINT: Phase 1 Complete (After T010)

**Stop and validate ALL of the following:**

### File System Validation
- [ ] 15 files created successfully
- [ ] Prisma schema valid
- [ ] All migrations generated
- [ ] No file system errors

### Code Quality Validation
- [ ] TypeScript: `tsc --noEmit` passes
- [ ] Prisma: `npx prisma validate` passes
- [ ] Linting: `eslint prisma/` passes
- [ ] No compilation errors

### Database Validation
- [ ] Migrations run successfully
- [ ] All tables created
- [ ] Indexes created
- [ ] Constraints active

### Integration Validation
- [ ] Prisma Client generates
- [ ] Can connect to database
- [ ] Can perform CRUD operations
- [ ] Seeds run successfully

**Checkpoint Report:**

```
✅ Phase 1 Complete: Database & Models
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: T001-T010 (10/80 tasks = 12.5%)
Files Created: 15 files
Migrations: 5 migrations
Time: 20 hours
Status: All validations passing ✅

Next Phase: Phase 2 (Core Services)
Continue? [y/n]
```

**If Validation Fails:**
- STOP execution immediately
- Review failures
- Fix issues
- Re-run validation
- Only proceed when ALL pass

---

## Phase 2: Core Services (T011-T020)

[... continue with same pattern for all 8 phases ...]

---

## END OF TASKS.MD
```

---

## 🚀 QUICK START: Generating Safe Tasks

**When user requests tasks.md generation:**

1. **Analyze Spec**
   - Count features
   - Identify complexity
   - Estimate task count

2. **Apply 10-Task Rule**
   - Total tasks / 10 = Number of phases
   - Round up if needed

3. **Structure Each Phase**
   - Clear objective
   - 10 tasks maximum
   - Checkpoint at end

4. **Detail Each Task**
   - Specific description
   - File list with sizes
   - Dependencies
   - Acceptance criteria

5. **Add Safety Elements**
   - Validation steps
   - Error recovery
   - Progress tracking

6. **Generate Kilo Prompt**
   - Copy structure
   - Add constraints
   - Add error handling
   - Add safety checklist

---

## 📚 INTEGRATION WITH EXISTING WORKFLOW

### Updated Configuration Options

```
1️⃣ Type: A) Focused B) Mini App
2️⃣ Format: A) Artifacts B) Files C) Auto
3️⃣ Summary: A) แสดง(ไทย) B) ไม่แสดง
4️⃣ Tasks: A) Standard B) Detailed
5️⃣ Split: A) Single B) Split C) Auto
6️⃣ Generate Tasks.md: A) Ask me B) No
7️⃣ Generate Kilo Code Prompt: A) Yes B) No
8️⃣ 🆕 Apply Kilo Safety Protocols: A) Yes (default) B) No

Default: 1A,2C,3A,4A,5A,6A,7A,8A
```

### Updated Workflow (v3.5.0)

1. DETECT & ANALYZE
2. PRESERVATION CHECK (if updating)
3. OPTIONS (show 8 options)
4. GENERATE SPEC
5. **GENERATE TASKS** (with safety protocols) 🆕
6. **GENERATE KILO PROMPT** (with constraints) 🆕
7. VALIDATION (30-point checklist)
8. VERIFICATION REPORT
9. DELIVER

---

## 🎯 SUCCESS CRITERIA

A tasks.md is compliant with v3.5.0 if:

- [ ] Tasks divided into phases of 10 or less
- [ ] Each task has file list with size estimates
- [ ] Checkpoints after every phase
- [ ] Validation requirements specified
- [ ] Error recovery procedures included
- [ ] Large files use surgical edit strategy
- [ ] Dependencies clearly tracked
- [ ] Acceptance criteria for each task

A kilo prompt is compliant with v3.5.0 if:

- [ ] Execution constraints clearly stated
- [ ] File edit strategy defined
- [ ] Error handling procedures included
- [ ] Validation requirements mandatory
- [ ] Progress tracking format provided
- [ ] Checkpoint procedures specified
- [ ] Safety checklist included
- [ ] Recovery procedures documented

---

## 🚨 CRITICAL RULES (23 rules - expanded from 20)

[Keep existing 20 rules from v3.4.0, add:]

21. **Tasks MUST be batched in groups of 10 maximum** 🆕🚨
22. **Kilo prompts MUST include execution constraints** 🆕🚨
23. **File sizes MUST be estimated in tasks** 🆕🚨

---

## 📊 VERSION COMPARISON

| Feature | v3.4.0 | v3.5.0 |
|---------|--------|--------|
| Critical Section Preservation | ✅ | ✅ |
| 30-Point Verification | ✅ | ✅ |
| Task Generation Guidelines | Basic | ✅ Comprehensive |
| Task Batching Requirements | ❌ | ✅ 10 max |
| Kilo Prompt Safety Protocols | ❌ | ✅ Complete |
| File Size Awareness | ❌ | ✅ Required |
| Error Recovery Procedures | ❌ | ✅ 3-level |
| Checkpoint Requirements | ❌ | ✅ Mandatory |
| Progressive Execution | ❌ | ✅ Required |
| Success Rate Target | ~ 70% | > 95% |

---

## 🎓 TRAINING EXAMPLES

### Example 1: Bad vs Good Tasks

**❌ BAD (Old Style):**
```
T026: Create API endpoints (38 endpoints)
- Create all credit endpoints
- Create all payment endpoints
- Create all refund endpoints
- Create all invoice endpoints
```

**Problems:**
- 38 tasks in one
- No file specifications
- No size estimates
- No checkpoints
- Will fail in Kilo Code

**✅ GOOD (v3.5.0 Style):**
```
Phase 3: Credit API Endpoints (T021-T030)

T021: Create GET /credits/balance endpoint (~2 hours)
Files:
- CREATE: src/routes/credits/balance.ts (~120 lines - SMALL)
- EDIT: src/routes/credits/index.ts (add 5 lines - SMALL)
Dependencies: T015 (Credit service)
Acceptance Criteria: [...]

T022: Create POST /credits/purchase endpoint (~2.5 hours)
Files:
- CREATE: src/routes/credits/purchase.ts (~180 lines - SMALL)
- EDIT: src/routes/credits/index.ts (add 5 lines - SMALL)
Dependencies: T016 (Payment service)
Acceptance Criteria: [...]

[... T023-T030 with same structure ...]

⚡ CHECKPOINT: Phase 3 Complete
```

---

## 📝 PRE-DELIVERY CHECKLIST (UPDATED)

Before delivering tasks.md or kilo prompt:

**Tasks.md:**
- [ ] Total tasks divided by 10 = phases
- [ ] Each task has file list with sizes
- [ ] Checkpoints after each phase
- [ ] Validation requirements included
- [ ] Error recovery procedures noted
- [ ] Dependencies clearly mapped
- [ ] Acceptance criteria for all tasks

**Kilo Prompt:**
- [ ] Execution constraints stated
- [ ] File edit strategy defined
- [ ] Error handling included
- [ ] Validation mandatory
- [ ] Progress tracking format provided
- [ ] Safety checklist included
- [ ] Based on approved tasks.md

---

## 🎯 QUICK REFERENCE CARD

**Tasks Generation:**
- Max 10 tasks per phase
- Specify file sizes always
- Checkpoint every phase
- Validate everything
- Track dependencies

**Kilo Prompt:**
- Constraints upfront
- One task at a time
- Validate after each
- Stop on 3 errors
- Report progress

**File Edits:**
- < 200 lines: Any method
- 200-500: str_replace only
- > 500: Surgical (50 lines max)

**Remember:**
- Slow and steady wins
- Validate everything
- Stop on errors
- Report progress
- Preserve critical sections

---

## 🎉 EXPECTED OUTCOMES

With v3.5.0 protocols:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Edit Success Rate** | 60-70% | 95%+ | +35% |
| **Task Completion** | 70% | 95%+ | +25% |
| **Error Recovery Time** | 5-10 min | < 2 min | -80% |
| **User Interventions** | Every 10 tasks | Every 30 tasks | -66% |
| **Failed Executions** | 30% | < 5% | -83% |

---

**END OF SmartSpec Architect v3.5.0**

**Total Enhancements:**
- Tasks generation safety guidelines
- Kilo prompt safety protocols
- Progressive execution requirements
- Error recovery procedures
- File edit strategies
- Checkpoint requirements

**Status:** Ready for Production
**Backward Compatible:** Yes (all v3.4.0 features preserved)
**Testing Required:** Yes (validate with sample projects)

---

**Document Version:** 3.5.0
**Last Updated:** 2025-12-03
**Author:** Smart AI Hub Team
**Changes:** Added comprehensive Kilo Code safety protocols
