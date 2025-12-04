# Platform-Specific Instructions Design
## Optimized for Kilo Code, Claude Code, Roo Code

**Version:** 2.0.0  
**Date:** 2025-01-04  
**Purpose:** ออกแบบ instructions ที่ดึงศักยภาพเต็มที่ของแต่ละ platform

---

## 🎯 Design Principles

### For Kilo Code
1. **Leverage Orchestrator** - ให้ tasks >8h แตกเป็น subtasks อัตโนมัติ
2. **Trust Mode Switching** - ไม่ต้องระบุ mode (automatic)
3. **Structured Tasks** - format ที่ชัดเจนเพื่อ mode detection
4. **Batch Execution** - optimize สำหรับ autonomous execution

### For Claude Code
1. **Setup Sub Agents** - สร้าง specialized agents ตั้งแต่ต้น
2. **Leverage Analysis** - ใช้ deep analysis capabilities
3. **Interactive Flow** - รองรับ user decisions
4. **Domain Separation** - แยก responsibilities ชัดเจน

### For Roo Code
1. **Workflow Phases** - แบ่งเป็น phases ชัดเจน
2. **Preview First** - เน้น preview diffs ก่อน apply
3. **Incremental Changes** - เปลี่ยนแปลงทีละน้อย
4. **Safety Gates** - validation ทุก phase

---

## 🤖 Kilo Code Instructions (Optimized)

### Section 1: Mode Overview

```markdown
## Kilo Code - Multi-Mode Architecture

Kilo Code uses **5 specialized modes** with automatic mode switching and LLM optimization:

### Modes

1. **Architect Mode** - Design, architecture, planning
   - Auto-selected for: design, architecture, schema, plan tasks
   - Optimized LLM: Architecture reasoning model
   - Best for: System design, database schema, API contracts

2. **Code Mode** - Implementation, file creation/editing
   - Auto-selected for: create, implement, build, add tasks
   - Optimized LLM: Code generation model
   - Best for: Feature implementation, code creation

3. **Debug Mode** - Error fixing, troubleshooting
   - Auto-selected for: fix, debug, resolve, troubleshoot tasks
   - Optimized LLM: Debugging model
   - Best for: Bug fixes, test failures, error resolution

4. **Ask Mode** - Clarification, decision support
   - Auto-selected for: ambiguous requirements, multiple options
   - Optimized LLM: Q&A and reasoning model
   - Best for: Requirement clarification, decision making

5. **Orchestrator Mode** - Task coordination, subtask management
   - **Auto-activated for tasks >8h**
   - Optimized LLM: Coordination model
   - Best for: Complex workflows, multi-component tasks

### Auto Subtasks

**Automatic Breakdown:**
- Tasks >8h: Automatically broken into subtasks
- Format: T001.1, T001.2, T001.3, ...
- Each subtask: 2-4h (optimal size)
- Mode assigned per subtask
- Dependencies tracked automatically

**Example:**
```
T050: Implement complete authentication system (12h)
  ↓ Orchestrator Mode activates
  
Subtasks created:
- [ ] T050.1: Design auth database schema (2h) → Architect Mode
- [ ] T050.2: Create User entity model (2h) → Code Mode
- [ ] T050.3: Implement JWT service (3h) → Code Mode
- [ ] T050.4: Create auth endpoints (3h) → Code Mode
- [ ] T050.5: Add auth tests (2h) → Code Mode
```

### Mode Selection (Automatic)

**You don't need to specify modes - they're selected automatically based on:**
- Task title keywords
- Task description content
- Task duration (>8h → Orchestrator)
- File operations (CREATE/EDIT → Code)
- Error patterns (fix/debug → Debug)

### Execution Strategy

**Autonomous Execution:**
1. Read task list
2. For each task:
   - Auto-select appropriate mode
   - If >8h: Orchestrator breaks into subtasks
   - Execute in selected mode
   - Switch modes as needed
   - Validate after completion
3. Track progress automatically

**Trust the System:**
- ✅ Let Orchestrator handle large tasks
- ✅ Trust automatic mode switching
- ✅ Don't manually specify modes
- ✅ Focus on clear task descriptions
```

---

### Section 2: Task Format for Kilo Code

```markdown
## Task Format (Optimized for Mode Detection)

### For Architect Mode Tasks

```markdown
### Task T001: Design user authentication schema (3h)
- [ ] T001: Design user authentication schema (3h)

**Description:**
Design PostgreSQL database schema for user authentication system.
Include users table, sessions table, and necessary indexes.

**Requirements:**
- User credentials storage
- Session management
- Password hashing support
- Email verification support

**Expected Outcome:**
- Complete schema design
- ER diagram
- Migration plan

**Files:**
- CREATE: `docs/database-schema.md` (~100 lines - SMALL)
- CREATE: `migrations/001_create_users.sql` (~50 lines - SMALL)
```

**Mode Detection:** "Design" + "schema" → Architect Mode

---

### For Code Mode Tasks

```markdown
### Task T020: Create User entity model (2h)
- [ ] T020: Create User entity model (2h)

**Description:**
Implement User entity model with Prisma ORM.
Include all fields, relations, and validation.

**Requirements:**
- User fields: id, email, password, createdAt, updatedAt
- Relations: sessions, profile
- Validation: email format, password strength

**Expected Outcome:**
- Working User model
- Type definitions
- Basic CRUD operations

**Files:**
- CREATE: `src/models/User.ts` (~150 lines - SMALL)
- CREATE: `src/types/user.types.ts` (~50 lines - SMALL)
```

**Mode Detection:** "Create" + "implement" → Code Mode

---

### For Debug Mode Tasks

```markdown
### Task T025: Fix TypeScript compilation errors (1h)
- [ ] T025: Fix TypeScript compilation errors (1h)

**Description:**
Resolve TypeScript compilation errors in auth module.
Errors related to type mismatches and missing imports.

**Error Messages:**
```
src/auth/service.ts:15:20 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
src/auth/controller.ts:8:1 - error TS2304: Cannot find name 'UserService'.
```

**Expected Outcome:**
- All compilation errors fixed
- Type safety maintained
- No new errors introduced

**Files:**
- EDIT: `src/auth/service.ts` (fix type issues)
- EDIT: `src/auth/controller.ts` (add imports)
```

**Mode Detection:** "Fix" + "errors" → Debug Mode

---

### For Orchestrator Mode Tasks (>8h)

```markdown
### Task T050: Implement complete authentication system (12h)
- [ ] T050: Implement complete authentication system (12h)

**Description:**
Implement full authentication system including:
- Database schema and models
- JWT token service
- Auth endpoints (login, register, logout)
- Password hashing and validation
- Session management
- Comprehensive tests

**Requirements:**
- Secure password storage (bcrypt)
- JWT token generation and validation
- Session persistence
- Email verification
- Password reset flow
- Rate limiting

**Expected Outcome:**
- Working authentication system
- All endpoints tested
- Security best practices applied
- Documentation complete

**Components:**
1. Database layer (schema, models)
2. Service layer (JWT, password, session)
3. API layer (endpoints, middleware)
4. Testing layer (unit, integration)
5. Documentation

**Files:** (Will be determined by subtasks)
```

**Mode Detection:** >8h → Orchestrator Mode (auto-creates subtasks)

**Orchestrator Will Create:**
```
T050.1: Design auth database schema (2h) → Architect
T050.2: Create User entity model (2h) → Code
T050.3: Implement JWT service (3h) → Code
T050.4: Create auth endpoints (3h) → Code
T050.5: Add comprehensive tests (2h) → Code
```
```

---

### Section 3: Execution Instructions

```markdown
## Execution Instructions for Kilo Code

### Autonomous Batch Processing

**Kilo Code excels at autonomous execution. Follow this approach:**

1. **Read All Tasks**
   - Parse tasks.md completely
   - Identify task boundaries
   - Note dependencies

2. **Let Orchestrator Work**
   - Tasks >8h: Wait for Orchestrator to create subtasks
   - Don't manually break down large tasks
   - Trust automatic breakdown

3. **Execute Sequentially**
   - Process tasks in order (T001, T002, T003, ...)
   - Respect dependencies
   - Skip if dependency not met

4. **Mode Switching**
   - Don't manually specify modes
   - Let system auto-select based on task
   - Trust mode transitions

5. **Validate After Each Task**
   - Run validation commands
   - Check compilation
   - Run relevant tests
   - Verify changes

6. **Track Progress**
   - Update checkboxes: `- [ ]` → `- [x]`
   - Log completed tasks
   - Note any failures

### Safety Constraints

**Hard Limits:**
- Maximum 10 tasks per execution cycle
- Maximum 5 file edits per task
- Maximum 50 lines per str_replace
- Stop at 3 consecutive errors

**Validation:**
- Compile after every task
- Test after every task
- Lint after every task

### Error Handling

**On Error:**
1. Switch to Debug Mode automatically
2. Analyze error
3. Attempt fix (max 2 attempts)
4. If still failing: Stop and report

**On 3 Consecutive Errors:**
- STOP execution immediately
- Create checkpoint
- Report errors
- Request manual intervention

### Checkpoint System

**Every 5 Tasks:**
- Create checkpoint file
- Save progress
- Run comprehensive validation
- Report status

**On Context Limit:**
- Immediate checkpoint
- Save state
- Pause execution
- Provide resume command
```

---

## 🧠 Claude Code Instructions (Optimized)

### Section 1: Sub Agents Setup

```markdown
## Claude Code - Sub Agents Architecture

Claude Code uses **user-created sub agents** for specialized expertise.

### Step 1: Create Sub Agents (Do This First!)

**Before starting implementation, create specialized sub agents:**

#### Database Agent

"Create a sub agent specialized in database operations.

**Focus Areas:**
- PostgreSQL database design
- Prisma ORM
- Database migrations
- Query optimization
- Indexing strategies

**Expertise:**
- Schema design and normalization
- Entity relationships
- Data integrity constraints
- Performance optimization
- Migration safety

**Responsibilities:**
All database-related tasks (T001-T015):
- T001: Design database schema
- T002: Create entity models
- T003: Setup Prisma client
- T004: Create migrations
- T005: Add indexes
- ... (all DB tasks)

**Context:**
- Project uses PostgreSQL 14
- ORM: Prisma 5.x
- Migration strategy: Incremental
- Performance target: <100ms queries"

---

#### API Agent

"Create a sub agent specialized in API development.

**Focus Areas:**
- Express.js REST APIs
- Request validation
- Error handling
- Middleware
- Authentication/Authorization

**Expertise:**
- RESTful API design
- Input validation (Zod)
- Error handling patterns
- Security best practices
- API documentation

**Responsibilities:**
All API-related tasks (T016-T030):
- T016: Setup Express server
- T017: Create user endpoints
- T018: Add validation middleware
- T019: Implement error handling
- T020: Add authentication
- ... (all API tasks)

**Context:**
- Framework: Express.js 4.x
- Validation: Zod
- Auth: JWT
- Error handling: Centralized
- Documentation: OpenAPI 3.0"

---

#### Test Agent

"Create a sub agent specialized in testing.

**Focus Areas:**
- Jest unit testing
- Integration testing
- Test coverage
- Mocking strategies
- E2E testing

**Expertise:**
- Test design and structure
- Mocking and stubbing
- Coverage optimization
- Test performance
- CI/CD integration

**Responsibilities:**
All testing tasks (T031-T045):
- T031: Setup Jest
- T032: Write unit tests
- T033: Write integration tests
- T034: Add E2E tests
- T035: Achieve 80% coverage
- ... (all test tasks)

**Context:**
- Framework: Jest 29.x
- Coverage target: 80%
- E2E: Supertest
- Mocking: jest.mock
- CI: GitHub Actions"

---

### Step 2: Execution Strategy

**Agent-Based Workflow:**

1. **Phase 1: Database (DB Agent)**
   - DB Agent handles T001-T015
   - Complete all database tasks
   - Validate schema and migrations
   - Hand off to API Agent

2. **Phase 2: API (API Agent)**
   - API Agent handles T016-T030
   - Implement all endpoints
   - Validate API contracts
   - Hand off to Test Agent

3. **Phase 3: Testing (Test Agent)**
   - Test Agent handles T031-T045
   - Write all tests
   - Achieve coverage targets
   - Report final status

4. **Phase 4: Integration (Main Agent)**
   - Main agent coordinates
   - Integration testing
   - Final validation
   - Documentation

**Benefits:**
- ✅ Specialized expertise per domain
- ✅ Clear responsibility boundaries
- ✅ Context isolation
- ✅ Parallel conceptual work
```

---

### Section 2: Task Format for Claude Code

```markdown
## Task Format (Optimized for Sub Agents)

### Database Tasks (for DB Agent)

```markdown
## Phase 1: Database Layer (T001-T015)
**Assigned to:** Database Agent

### Task T001: Design user authentication schema (3h)
- [ ] T001: Design user authentication schema (3h)

**Agent:** Database Agent
**Focus:** Schema design, normalization, indexes

**Description:**
Design PostgreSQL schema for user authentication.
Include users, sessions, and necessary relations.

**Requirements:**
- Users table with credentials
- Sessions table for JWT tokens
- Proper indexes for performance
- Foreign key constraints

**Expected Outcome:**
- Schema design document
- Prisma schema file
- Migration files

**Files:**
- CREATE: `prisma/schema.prisma` (~200 lines - MEDIUM)
- CREATE: `docs/database-design.md` (~100 lines - SMALL)

**Validation:**
- Schema compiles
- Migrations generate correctly
- No circular dependencies
```

---

### API Tasks (for API Agent)

```markdown
## Phase 2: API Layer (T016-T030)
**Assigned to:** API Agent

### Task T016: Create user registration endpoint (2h)
- [ ] T016: Create user registration endpoint (2h)

**Agent:** API Agent
**Focus:** Endpoint implementation, validation, error handling

**Description:**
Implement POST /api/auth/register endpoint.
Include validation, password hashing, and error handling.

**Requirements:**
- Input validation (email, password)
- Password strength requirements
- Duplicate email check
- Error responses

**Expected Outcome:**
- Working registration endpoint
- Proper validation
- Error handling
- API documentation

**Files:**
- CREATE: `src/api/auth/register.controller.ts` (~150 lines - SMALL)
- CREATE: `src/api/auth/register.validation.ts` (~50 lines - SMALL)
- EDIT: `src/api/auth/routes.ts` (add route)

**Validation:**
- Endpoint responds correctly
- Validation works
- Errors handled properly
- Tests pass
```

---

### Test Tasks (for Test Agent)

```markdown
## Phase 3: Testing Layer (T031-T045)
**Assigned to:** Test Agent

### Task T031: Write unit tests for auth service (3h)
- [ ] T031: Write unit tests for auth service (3h)

**Agent:** Test Agent
**Focus:** Unit testing, mocking, coverage

**Description:**
Write comprehensive unit tests for authentication service.
Mock database and external dependencies.

**Requirements:**
- Test all public methods
- Mock database calls
- Test error scenarios
- Achieve 90% coverage

**Expected Outcome:**
- Complete test suite
- All tests passing
- 90%+ coverage
- Clear test documentation

**Files:**
- CREATE: `src/auth/__tests__/auth.service.test.ts` (~300 lines - MEDIUM)
- CREATE: `src/auth/__tests__/mocks.ts` (~100 lines - SMALL)

**Validation:**
- All tests pass
- Coverage >90%
- No flaky tests
- Fast execution (<5s)
```
```

---

### Section 3: Execution Instructions

```markdown
## Execution Instructions for Claude Code

### Interactive Agent-Based Execution

**Claude Code excels at interactive development with specialized agents:**

### Phase-by-Phase Execution

**Phase 1: Database Agent**

1. **Activate Database Agent**
   - Switch to DB Agent context
   - Load database-specific knowledge
   - Review all DB tasks (T001-T015)

2. **Execute DB Tasks**
   - T001: Design schema
   - T002: Create models
   - T003: Setup Prisma
   - ... (all DB tasks)

3. **Validate DB Phase**
   - Schema compiles
   - Migrations work
   - Models tested
   - Hand off to API Agent

---

**Phase 2: API Agent**

1. **Activate API Agent**
   - Switch to API Agent context
   - Load API-specific knowledge
   - Review all API tasks (T016-T030)

2. **Execute API Tasks**
   - T016: Create endpoints
   - T017: Add validation
   - T018: Error handling
   - ... (all API tasks)

3. **Validate API Phase**
   - Endpoints work
   - Validation correct
   - Errors handled
   - Hand off to Test Agent

---

**Phase 3: Test Agent**

1. **Activate Test Agent**
   - Switch to Test Agent context
   - Load testing knowledge
   - Review all test tasks (T031-T045)

2. **Execute Test Tasks**
   - T031: Unit tests
   - T032: Integration tests
   - T033: E2E tests
   - ... (all test tasks)

3. **Validate Test Phase**
   - All tests pass
   - Coverage targets met
   - No flaky tests
   - Hand off to Main Agent

---

**Phase 4: Main Agent Integration**

1. **Coordinate Integration**
   - Review all phases
   - Integration testing
   - End-to-end validation

2. **Final Validation**
   - All components working
   - System integration verified
   - Documentation complete

### Interactive Decision Making

**When to Ask User:**
- Ambiguous requirements
- Multiple valid approaches
- Architecture decisions
- Trade-off analysis
- Missing information

**How to Ask:**
```
"I see two approaches for implementing authentication:

Option 1: JWT with refresh tokens
  Pros: Stateless, scalable
  Cons: Token revocation complexity

Option 2: Session-based with Redis
  Pros: Easy revocation, server control
  Cons: Stateful, Redis dependency

Which approach do you prefer?"
```

### Deep Analysis Usage

**Leverage Repo-wide Reasoning:**

1. **Before Starting:**
   - Analyze entire codebase
   - Understand architecture
   - Identify patterns
   - Map dependencies

2. **During Implementation:**
   - Check for similar code
   - Reuse existing patterns
   - Maintain consistency
   - Avoid duplication

3. **Before Refactoring:**
   - Impact analysis
   - Dependency mapping
   - Risk assessment
   - Migration planning

**Example Analysis:**
```
"Analyze this codebase and identify:
1. All authentication-related code
2. Current security patterns
3. Database access patterns
4. Error handling approaches
5. Testing strategies

Use this analysis to guide implementation."
```

### Safety and Validation

**Per-Agent Validation:**
- DB Agent: Schema validation, migration testing
- API Agent: Endpoint testing, contract validation
- Test Agent: Coverage verification, test quality

**Phase Validation:**
- After each phase: Comprehensive validation
- Integration testing between phases
- Regression testing

**Final Validation:**
- All tests passing
- Coverage targets met
- Integration verified
- Documentation complete
```

---

## 🦘 Roo Code Instructions (Optimized)

### Section 1: Workflow Overview

```markdown
## Roo Code - Workflow-Driven Development

Roo Code uses **structured workflow phases** with emphasis on safety and preview.

### Workflow Phases

1. **Plan Mode** - Task planning and breakdown
2. **Implement Mode** - Code implementation with preview
3. **Review Mode** - Comprehensive diff review
4. **Execute Mode** - Testing and validation
5. **Explain Mode** - Documentation and explanation

### Safety-First Approach

**Key Features:**
- ✅ **Full diff preview** before any changes
- ✅ **Approval gates** at each phase
- ✅ **Incremental changes** (small, safe edits)
- ✅ **Easy rollback** if issues found
- ✅ **Validation gates** before proceeding

### Workflow Structure

```
For each Phase:
  1. Plan Mode: Break down into steps
  2. Implement Mode: Generate changes
  3. Review Mode: Preview all diffs
  4. User Approval: Review and approve
  5. Apply Changes: Execute approved changes
  6. Execute Mode: Run tests and validate
  7. Confirm or Rollback: Verify success
```
```

---

### Section 2: Task Format for Roo Code

```markdown
## Task Format (Optimized for Workflow)

### Phase Structure

```markdown
## Phase 1: Database Setup

**Workflow:** Plan → Implement → Review → Execute

### Step 1: Plan Mode

**Tasks in this phase:**
- T001: Design database schema (3h)
- T002: Create entity models (2h)
- T003: Setup Prisma client (1h)

**Plan:**
1. Design schema structure
2. Create Prisma schema file
3. Generate migration files
4. Setup Prisma client

**Dependencies:**
- None (first phase)

**Estimated Duration:** 6 hours

---

### Step 2: Implement Mode

#### Task T001: Design database schema (3h)

**Implementation Steps:**
1. Create `prisma/schema.prisma`
2. Define User model
3. Define Session model
4. Add relations and indexes

**Files to Create:**
- `prisma/schema.prisma` (~200 lines - MEDIUM)
- `docs/database-design.md` (~100 lines - SMALL)

**Implementation:**
```prisma
// prisma/schema.prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  sessions  Session[]
}

model Session {
  id        String   @id @default(uuid())
  userId    String
  token     String   @unique
  expiresAt DateTime
  user      User     @relation(fields: [userId], references: [id])
}
```

---

### Step 3: Review Mode

**Preview Diffs:**

```diff
File: prisma/schema.prisma (NEW FILE)

+ generator client {
+   provider = "prisma-client-js"
+ }
+
+ datasource db {
+   provider = "postgresql"
+   url      = env("DATABASE_URL")
+ }
+
+ model User {
+   id        String   @id @default(uuid())
+   email     String   @unique
+   password  String
+   createdAt DateTime @default(now())
+   updatedAt DateTime @updatedAt
+   sessions  Session[]
+ }
+
+ model Session {
+   id        String   @id @default(uuid())
+   userId    String
+   token     String   @unique
+   expiresAt DateTime
+   user      User     @relation(fields: [userId], references: [id])
+ }

File: docs/database-design.md (NEW FILE)

+ # Database Design
+
+ ## User Table
+ - id: UUID primary key
+ - email: Unique email address
+ - password: Hashed password
+ - timestamps: Created/updated
+
+ ## Session Table
+ - id: UUID primary key
+ - userId: Foreign key to User
+ - token: Unique JWT token
+ - expiresAt: Expiration timestamp
```

**Review Checklist:**
- [ ] Schema structure correct
- [ ] Relations defined properly
- [ ] Indexes added
- [ ] No syntax errors
- [ ] Documentation complete

**[APPROVAL REQUIRED]**
Do you approve these changes? (y/n)

---

### Step 4: Execute Mode

**After approval, execute:**

1. **Apply Changes**
   ```bash
   # Create files
   create prisma/schema.prisma
   create docs/database-design.md
   ```

2. **Validate**
   ```bash
   # Generate Prisma client
   npx prisma generate
   
   # Check for errors
   npx prisma validate
   ```

3. **Test**
   ```bash
   # Run schema tests
   npm test -- schema.test.ts
   ```

**Validation Results:**
```
✅ Prisma client generated successfully
✅ Schema validation passed
✅ Tests passed (3/3)
```

**[CONFIRMATION]**
Changes applied successfully. Proceed to next task? (y/n)

---

### Step 5: Rollback (If Needed)

**If validation fails:**

```bash
# Rollback changes
git restore prisma/schema.prisma
git restore docs/database-design.md

# Report error
echo "Rollback completed. Review errors and retry."
```

**Error Report:**
- What failed: [error description]
- Why it failed: [root cause]
- How to fix: [suggested fix]
- Retry command: [command to retry]
```
```

---

### Section 3: Execution Instructions

```markdown
## Execution Instructions for Roo Code

### Workflow-Based Execution

**Roo Code requires structured phase-by-phase execution:**

### Phase Execution Template

**For Each Phase:**

#### 1. Plan Mode

```markdown
## Phase X: [Phase Name]

### Planning

**Tasks:**
- List all tasks in this phase
- Estimate duration
- Identify dependencies

**Steps:**
1. Step 1 description
2. Step 2 description
3. Step 3 description

**Files:**
- File 1 to create/edit
- File 2 to create/edit

**Dependencies:**
- Dependency 1
- Dependency 2

**Estimated Duration:** X hours
```

---

#### 2. Implement Mode

```markdown
### Implementation

**For each task:**

1. **Generate Changes**
   - Create/edit files
   - Implement logic
   - Add documentation

2. **Generate Diffs**
   - Show all changes
   - Line-by-line diffs
   - New files marked

3. **Prepare Preview**
   - Format diffs clearly
   - Add context
   - Highlight important changes
```

---

#### 3. Review Mode

```markdown
### Review

**Preview All Changes:**

```diff
File: path/to/file1.ts

- old line
+ new line
  unchanged line
+ new line

File: path/to/file2.ts (NEW FILE)

+ entire new file content
+ line by line
```

**Review Checklist:**
- [ ] Changes match requirements
- [ ] No unintended modifications
- [ ] Code quality acceptable
- [ ] Documentation included
- [ ] Tests added/updated

**Safety Check:**
- [ ] No breaking changes
- [ ] Backward compatible
- [ ] No security issues
- [ ] Performance acceptable

**[APPROVAL REQUIRED]**
Review complete. Approve changes? (y/n)
```

---

#### 4. Execute Mode

```markdown
### Execution

**After Approval:**

1. **Apply Changes**
   ```bash
   # List files to be modified
   - create: path/to/new/file.ts
   - edit: path/to/existing/file.ts
   - delete: path/to/old/file.ts
   ```

2. **Validate**
   ```bash
   # Compilation
   npm run build
   
   # Linting
   npm run lint
   
   # Type checking
   npm run type-check
   ```

3. **Test**
   ```bash
   # Unit tests
   npm test -- affected
   
   # Integration tests
   npm run test:integration
   ```

**Validation Results:**
```
✅ Compilation: PASS
✅ Linting: PASS
✅ Type Check: PASS
✅ Unit Tests: PASS (15/15)
✅ Integration Tests: PASS (5/5)
```

**[CONFIRMATION]**
All validations passed. Proceed? (y/n)
```

---

#### 5. Rollback (If Needed)

```markdown
### Rollback Procedure

**If Any Validation Fails:**

1. **Identify Failure**
   - Which validation failed
   - Error messages
   - Root cause

2. **Rollback Changes**
   ```bash
   git restore .
   # or
   git reset --hard HEAD
   ```

3. **Report Error**
   ```
   ❌ Validation Failed: [validation type]
   
   Error: [error message]
   
   Root Cause: [analysis]
   
   Suggested Fix: [fix description]
   
   Retry: [y/n]
   ```

4. **Fix and Retry**
   - Apply suggested fix
   - Re-run from Implement Mode
   - Preview changes again
```

---

### Incremental Changes Strategy

**For Large Changes:**

1. **Break into Smaller Steps**
   ```
   Large Task: Implement auth system (12h)
   
   Break into phases:
   - Phase 1: Database (2h)
   - Phase 2: Models (2h)
   - Phase 3: Service (3h)
   - Phase 4: Endpoints (3h)
   - Phase 5: Tests (2h)
   ```

2. **Execute Phase by Phase**
   - Complete Phase 1
   - Validate Phase 1
   - Commit Phase 1
   - Proceed to Phase 2

3. **Validate After Each Phase**
   - Compilation
   - Tests
   - Integration
   - Commit

**Benefits:**
- ✅ Smaller, safer changes
- ✅ Easier to review
- ✅ Easier to rollback
- ✅ Clear progress tracking

---

### Safety Gates

**Mandatory Gates:**

1. **Before Apply:**
   - Preview all diffs
   - User approval required

2. **After Apply:**
   - Compilation check
   - Test execution
   - Lint check

3. **Before Proceed:**
   - All validations pass
   - User confirmation

**Gate Failure:**
- Automatic rollback
- Error report
- Fix suggestions
- Retry option

---

### Frontend-Specific Optimizations

**For React/Vue/Angular:**

1. **Component-Based Workflow**
   ```
   Phase 1: Component structure
   Phase 2: Component logic
   Phase 3: Component styles
   Phase 4: Component tests
   ```

2. **Preview in Browser**
   - Start dev server
   - Preview changes live
   - Visual verification

3. **Hot Reload Testing**
   - Make changes
   - Preview immediately
   - Validate visually

**For Node.js:**

1. **Module-Based Workflow**
   ```
   Phase 1: Module structure
   Phase 2: Module logic
   Phase 3: Module tests
   Phase 4: Module integration
   ```

2. **API Testing**
   - Start server
   - Test endpoints
   - Validate responses
```

---

## 📊 Comparison of Instructions

| Aspect | Kilo Code | Claude Code | Roo Code |
|--------|-----------|-------------|----------|
| **Setup Overhead** | Low (automatic) | High (create agents) | Medium (plan phases) |
| **Execution Style** | Autonomous | Interactive | Structured |
| **User Involvement** | Minimal | High | Medium-High |
| **Safety Level** | Medium | High | Very High |
| **Speed** | Fast | Medium | Slow |
| **Best For** | Large batches | Analysis & decisions | Safe edits |

---

## ✅ Recommendations

### Choose Instructions Based On:

**Kilo Code Instructions:**
- ✅ Large projects (>100 tasks)
- ✅ Need autonomous execution
- ✅ Tasks >8h (leverage Orchestrator)
- ✅ Minimal user oversight

**Claude Code Instructions:**
- ✅ Complex analysis needed
- ✅ Multiple specialized domains
- ✅ Interactive development
- ✅ Decision-heavy projects

**Roo Code Instructions:**
- ✅ Frontend projects
- ✅ Need high safety
- ✅ Learning/onboarding
- ✅ Incremental changes

---

**Document Version:** 2.0.0  
**Last Updated:** 2025-01-04  
**Next Review:** After workflow testing
