# Cursor/Antigravity Prompt Generator Architecture
## Solution Design for Vibe Coding Workflow

**Version:** 1.0.0  
**Date:** 2025-01-04  
**Status:** 🏗️ ARCHITECTURE DESIGN

---

## 🎯 Solution Overview

สร้าง workflow ใหม่ที่แปลง **technical tasks.md** เป็น **user-friendly prompts** สำหรับ Cursor/Antigravity

**Key Features:**
- ✅ Simple prompt generation
- ✅ Task selection (single, multiple, range)
- ✅ Subtask breakdown (auto for >8h)
- ✅ Context preservation
- ✅ Platform-specific optimization
- ✅ Hybrid workflow support

---

## 🏗️ Architecture

### Workflow Name
`smartspec_generate_cursor_prompt.md`

### Command Patterns

```bash
# Single task
/smartspec_generate_cursor_prompt tasks.md --task T001

# Multiple tasks (comma-separated)
/smartspec_generate_cursor_prompt tasks.md --task T001,T002,T003

# Task range
/smartspec_generate_cursor_prompt tasks.md --task T001-T010

# Single task with breakdown
/smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown

# Multiple tasks with specific subtasks
/smartspec_generate_cursor_prompt tasks.md --subtask T050.1,T050.2,T050.3

# Skip completed tasks
/smartspec_generate_cursor_prompt tasks.md --task T011-T020 --skip-completed

# Platform specific
/smartspec_generate_cursor_prompt tasks.md --task T001 --antigravity

# All tasks (generate all prompts)
/smartspec_generate_cursor_prompt tasks.md --all

# Interactive mode
/smartspec_generate_cursor_prompt tasks.md --interactive
```

### Default Behavior
- Platform: `--cursor` (if not specified)
- Task: Must specify (no default)
- Output: Single file `cursor-prompt-<tasks>.md`
- Breakdown: Manual (use --breakdown for auto)

---

## 📥 Input Processing

### 1. Parse Arguments

```
Input: tasks.md --task T001,T002,T003 --cursor
```

**Extract:**
- `tasks_file`: `tasks.md`
- `task_selection`: `T001,T002,T003`
- `platform`: `cursor`
- `breakdown`: `false` (default)
- `skip_completed`: `false` (default)

### 2. Read tasks.md

**Parse:**
- YAML frontmatter (validation commands, tech stack)
- Project metadata
- Phase overview
- All tasks with details

**Extract per task:**
- Task ID (T001, T002, ...)
- Task title
- Task description
- Time estimate
- Files to create/edit
- Dependencies
- Acceptance criteria
- Risks

### 3. Task Selection Logic

**Pattern: Single Task**
```
--task T001
→ Select T001 only
```

**Pattern: Multiple Tasks (Comma)**
```
--task T001,T002,T003
→ Select T001, T002, T003
```

**Pattern: Task Range**
```
--task T001-T010
→ Select T001, T002, ..., T010
```

**Pattern: Subtasks**
```
--subtask T050.1,T050.2
→ Select T050.1, T050.2 only
```

**Pattern: All**
```
--all
→ Select all tasks
→ Generate one prompt per task
```

### 4. Breakdown Logic

**Auto Breakdown (if --breakdown):**
```
IF task.hours > 8:
  → Break into subtasks (2-4h each)
  → T050 (12h) → T050.1 (3h), T050.2 (3h), T050.3 (3h), T050.4 (3h)
ELSE:
  → Keep as single task
```

**Breakdown Algorithm:**
```
1. Calculate subtask count: ceil(task.hours / 3)
2. Distribute hours evenly
3. Analyze task description
4. Split by logical components
5. Assign dependencies between subtasks
6. Generate subtask IDs (T050.1, T050.2, ...)
```

### 5. Context Building

**For Each Selected Task:**
```
Context = {
  previous_tasks: [tasks before this one],
  dependencies: [tasks this depends on],
  dependent_tasks: [tasks that depend on this],
  phase_info: {phase number, phase name, phase goals},
  files_created_before: [files from previous tasks],
  tech_stack: [from frontmatter],
  validation_commands: [from frontmatter]
}
```

---

## 📤 Output Generation

### Output Filename Pattern

**Single Task:**
```
cursor-prompt-T001.md
```

**Multiple Tasks:**
```
cursor-prompt-T001-T003.md
```

**Task Range:**
```
cursor-prompt-T001-T010.md
```

**Subtasks:**
```
cursor-prompt-T050.1-T050.3.md
```

**All Tasks:**
```
cursor-prompt-T001.md
cursor-prompt-T002.md
cursor-prompt-T003.md
...
```

### Output Location
Same directory as tasks.md

---

## 📝 Prompt Template

### Template Structure

```markdown
# [Task Title]

## 🎯 What You'll Build
[Simple description of what this task accomplishes]

## 📋 Context
[Information about previous tasks and dependencies]

## 🔧 Implementation Steps
[Step-by-step instructions]

## 💻 Code Structure
[Example code structure or skeleton]

## 📁 Files
[List of files to create/edit]

## ✅ Validation
[How to validate the implementation]

## ⏱️ Estimated Time
[Time estimate]

## ➡️ Next Steps
[What comes after this task]
```

---

### Template for Single Task

```markdown
# Task T001: Create User Entity

## 🎯 What You'll Build

A User entity model with email and password fields, including validation methods.

## 📋 Context

**Phase:** Phase 1 - Database Layer
**Position:** First task in this phase
**Dependencies:** None (this is the starting point)

**What comes before:**
- Nothing (this is the first task)

**What comes after:**
- T002 will create AuthService that uses this User entity
- T003 will create API endpoints that use this User entity

## 🔧 Implementation Steps

### Step 1: Create the User Entity File

Create a new file: `src/models/User.ts`

### Step 2: Define the User Class

Add a User class with these properties:
- `email`: string (user's email address)
- `password`: string (hashed password)
- `createdAt`: Date (when user was created)
- `updatedAt`: Date (when user was last updated)

### Step 3: Add Validation Methods

Add these methods to validate user data:
- `validateEmail()`: Check if email format is valid
- `validatePassword()`: Check if password meets requirements (min 8 chars, etc.)

### Step 4: Add Helper Methods

Add these helper methods:
- `toJSON()`: Return user data without password (for API responses)
- `comparePassword()`: Compare input password with stored hash

### Step 5: Export the Class

Export the User class so other files can use it.

## 💻 Code Structure

Here's the basic structure your code should follow:

```typescript
// src/models/User.ts

export class User {
  // Properties
  email: string;
  password: string;
  createdAt: Date;
  updatedAt: Date;

  // Constructor
  constructor(email: string, password: string) {
    // Initialize properties
  }

  // Validation methods
  validateEmail(): boolean {
    // Email validation logic
  }

  validatePassword(): boolean {
    // Password validation logic
  }

  // Helper methods
  toJSON(): object {
    // Return user data without password
  }

  async comparePassword(inputPassword: string): Promise<boolean> {
    // Compare passwords
  }
}
```

## 📁 Files

**Create:**
- `src/models/User.ts` (~80 lines)

**Size:** SMALL (less than 100 lines)

## ✅ Validation

After implementing, run these commands to validate:

```bash
# Check TypeScript compilation
tsc --noEmit

# Run tests (if you have tests)
npm test

# Check linting
npm run lint
```

**Expected Results:**
- ✅ No TypeScript errors
- ✅ All tests passing
- ✅ No lint errors

## ⏱️ Estimated Time

**2 hours**

This includes:
- Creating the file (10 min)
- Implementing the class (60 min)
- Adding validation (30 min)
- Testing (20 min)

## ➡️ Next Steps

After completing this task:

1. **Validate your implementation** using the commands above
2. **Commit your changes** to version control
3. **Move to T002**: Create AuthService
   - T002 will import and use this User entity
   - Make sure User is exported correctly

## 💡 Tips

- Use bcrypt for password hashing
- Email validation can use regex or a library like validator.js
- Remember to handle edge cases (empty strings, null values)
- Add JSDoc comments for better documentation

## 🔗 Dependencies

**This task depends on:**
- None (starting point)

**Tasks that depend on this:**
- T002: Create AuthService (uses User entity)
- T003: Create API endpoints (uses User entity)
- T005: Write tests (tests User entity)

---

**Platform:** Cursor
**Generated:** 2025-01-04
**Source:** tasks.md
```

---

### Template for Multiple Tasks

```markdown
# Tasks T001-T003: Database Layer

## 🎯 Overview

Build the complete database layer including User entity, AuthService, and database connection.

**Phase:** Phase 1 - Database Layer
**Total Time:** 7 hours
**Tasks:** 3 tasks

---

## Task T001: Create User Entity

### 🎯 What You'll Build
[Same as single task template...]

### 🔧 Implementation Steps
[Same as single task template...]

### 💻 Code Structure
[Same as single task template...]

### 📁 Files
- `src/models/User.ts` (~80 lines)

### ⏱️ Time: 2 hours

---

## Task T002: Create AuthService

### 🎯 What You'll Build

An authentication service that handles user login and registration using the User entity from T001.

### 📋 Context

**Depends on:** T001 (User entity must be completed first)

**Files from T001:**
- `src/models/User.ts` (you created this in T001)

**What this adds:**
- AuthService that uses User entity
- Login and register methods
- JWT token generation

### 🔧 Implementation Steps

[Detailed steps...]

### 💻 Code Structure

```typescript
// src/services/AuthService.ts

import { User } from '../models/User';

export class AuthService {
  async login(email: string, password: string): Promise<string> {
    // 1. Find user by email
    // 2. Compare password
    // 3. Generate JWT token
    // 4. Return token
  }

  async register(email: string, password: string): Promise<User> {
    // 1. Validate email and password
    // 2. Hash password
    // 3. Create new User
    // 4. Save to database
    // 5. Return user
  }
}
```

### 📁 Files

**Create:**
- `src/services/AuthService.ts` (~120 lines)

**Uses:**
- `src/models/User.ts` (from T001)

### ⏱️ Time: 3 hours

---

## Task T003: Setup Database Connection

### 🎯 What You'll Build

[Similar structure...]

---

## ✅ Validation (All Tasks)

After completing all tasks, run:

```bash
tsc --noEmit
npm test
npm run lint
```

## 📊 Progress Tracking

- [ ] T001: Create User Entity (2h)
- [ ] T002: Create AuthService (3h)
- [ ] T003: Setup Database Connection (2h)

**Total:** 7 hours

## ➡️ Next Steps

After completing all 3 tasks:
1. Validate all implementations
2. Commit changes
3. Move to Phase 2: API Layer (T004-T008)

---

**Platform:** Cursor
**Generated:** 2025-01-04
**Source:** tasks.md
```

---

## 🔄 Subtask Breakdown Algorithm

### Input: Large Task

```markdown
- [ ] T050: Implement complete authentication system (12h)
  - **Description:** Build full auth system with login, register, JWT, middleware
  - **Files:** 
    - `src/models/User.ts`
    - `src/services/AuthService.ts`
    - `src/controllers/AuthController.ts`
    - `src/middleware/auth.ts`
    - `tests/auth.test.ts`
```

### Breakdown Process

**Step 1: Calculate Subtask Count**
```
task.hours = 12h
target_hours_per_subtask = 3h
subtask_count = ceil(12 / 3) = 4 subtasks
```

**Step 2: Analyze Components**
```
Components identified:
1. User model (database)
2. AuthService (business logic)
3. AuthController (API endpoints)
4. Auth middleware (request validation)
5. Tests (validation)

Group into 4 subtasks:
- Subtask 1: User model (3h)
- Subtask 2: AuthService (3h)
- Subtask 3: AuthController + routes (3h)
- Subtask 4: Middleware + tests (3h)
```

**Step 3: Generate Subtasks**
```markdown
- [ ] T050.1: Create User model and database schema (3h)
  - Files: src/models/User.ts, prisma/schema.prisma
  - Dependencies: None
  
- [ ] T050.2: Implement AuthService with login/register (3h)
  - Files: src/services/AuthService.ts
  - Dependencies: T050.1
  
- [ ] T050.3: Create AuthController and API endpoints (3h)
  - Files: src/controllers/AuthController.ts, src/routes/auth.ts
  - Dependencies: T050.2
  
- [ ] T050.4: Add auth middleware and tests (3h)
  - Files: src/middleware/auth.ts, tests/auth.test.ts
  - Dependencies: T050.3
```

**Step 4: Generate Prompts**
```
Generate 4 separate prompts:
- cursor-prompt-T050.1.md
- cursor-prompt-T050.2.md
- cursor-prompt-T050.3.md
- cursor-prompt-T050.4.md

Each prompt includes:
- Clear scope
- Dependencies
- Context from previous subtasks
- Validation steps
```

---

## 🔗 Context Preservation Strategy

### Context Types

**1. Previous Tasks Context**
```markdown
## 📋 Context

**What you've built so far:**

In T001, you created:
- User entity model (`src/models/User.ts`)
- Email and password validation
- Helper methods for user data

In T002, you created:
- AuthService (`src/services/AuthService.ts`)
- Login method that uses User entity
- Register method that creates new users
- JWT token generation

**Now in T003, you'll build on top of these:**
- Use AuthService for authentication
- Create API endpoints that call AuthService methods
- Handle HTTP requests and responses
```

**2. Dependencies Context**
```markdown
## 🔗 Dependencies

**This task depends on:**
- ✅ T001: User entity (completed)
- ✅ T002: AuthService (completed)

**Files you'll use:**
- `src/models/User.ts` (from T001)
- `src/services/AuthService.ts` (from T002)

**Make sure these are completed before starting this task.**
```

**3. Files Created Context**
```markdown
## 📁 Existing Files

**Files created in previous tasks:**
- `src/models/User.ts` (T001) - User entity model
- `src/services/AuthService.ts` (T002) - Authentication service

**Files you'll create in this task:**
- `src/controllers/AuthController.ts` (NEW)
- `src/routes/auth.ts` (NEW)

**Files you'll edit in this task:**
- `src/app.ts` (add auth routes)
```

**4. Phase Context**
```markdown
## 📊 Phase Progress

**Phase 1: Database Layer**
- ✅ T001: User entity (completed)
- ✅ T002: AuthService (completed)
- 🔄 T003: Database connection (current task)
- ⏳ T004: Migrations (next)

**You are:** 3 of 4 tasks in Phase 1
**Progress:** 75% of Phase 1 complete
```

---

## 🎨 Platform-Specific Optimizations

### Cursor Optimizations

**Features to leverage:**
- Tab completion
- Inline suggestions
- Multi-file editing
- Command palette

**Prompt Optimizations:**
```markdown
## 💡 Cursor Tips

- Use `Cmd+K` to ask Cursor for help
- Use `Cmd+L` to select code and ask questions
- Use Tab to accept inline suggestions
- Use `Cmd+Shift+P` for command palette

## 🔧 Cursor Workflow

1. Create file: `src/models/User.ts`
2. Type `class User` and let Cursor suggest
3. Accept suggestions with Tab
4. Ask Cursor: "Add email validation method"
5. Review and accept suggestions
```

---

### Antigravity Optimizations

**Features to leverage:**
- AI pair programming
- Code review
- Refactoring suggestions
- Test generation

**Prompt Optimizations:**
```markdown
## 💡 Antigravity Tips

- Use AI pair programming mode
- Ask for code review after implementation
- Request refactoring suggestions
- Generate tests automatically

## 🔧 Antigravity Workflow

1. Start pair programming session
2. Describe what you want to build
3. Review AI suggestions
4. Accept or modify
5. Ask for code review
6. Request test generation
```

---

## 📊 Completed Task Tracking

### Mechanism

**Read tasks.md:**
```markdown
- [x] T001: Create User entity (completed)
- [x] T002: Create AuthService (completed)
- [ ] T003: Setup database (not completed)
- [ ] T004: Create endpoints (not completed)
```

**With --skip-completed:**
```
User requests: --task T001-T004 --skip-completed

Filter:
- T001: ✅ Completed → Skip
- T002: ✅ Completed → Skip
- T003: ❌ Not completed → Include
- T004: ❌ Not completed → Include

Generate prompt for: T003, T004 only
```

**Context Preservation:**
```markdown
## 📋 Context

**Completed tasks:**
- ✅ T001: User entity (completed)
- ✅ T002: AuthService (completed)

**Files already created:**
- `src/models/User.ts` (T001)
- `src/services/AuthService.ts` (T002)

**Current task:**
- 🔄 T003: Setup database connection

**You can use:**
- User entity from T001
- AuthService from T002
```

---

## 🔄 Hybrid Workflow Support

### Scenario: Kilo Code → Cursor → Kilo Code

**Phase 1: Kilo Code (T001-T010)**
```bash
$ kilo code implement tasks.md --task T001-T010
# Autonomous execution
# T001-T010 completed ✅
```

**Phase 2: Cursor (T011-T015)**
```bash
$ /smartspec_generate_cursor_prompt tasks.md --task T011-T015 --skip-completed

# Output: cursor-prompt-T011-T015.md

# Prompt includes:
- Context from T001-T010 (completed by Kilo Code)
- Files created in T001-T010
- Dependencies satisfied by T001-T010
```

**Phase 3: Kilo Code (T016-T050)**
```bash
$ kilo code implement tasks.md --task T016-T050 --skip-completed

# Kilo Code knows:
- T001-T010 completed
- T011-T015 completed (by Cursor)
- Start from T016
```

---

## 🎯 Success Criteria

### Prompt Quality

**Must Have:**
- ✅ Easy to understand (non-technical language)
- ✅ Clear steps (step-by-step instructions)
- ✅ Example code (code structure/skeleton)
- ✅ Validation steps (how to verify)

**Should Have:**
- ✅ Context preservation (previous tasks)
- ✅ Dependencies (what's needed)
- ✅ Files list (what to create/edit)
- ✅ Time estimate (how long)

**Nice to Have:**
- ✅ Tips and tricks (platform-specific)
- ✅ Common pitfalls (what to avoid)
- ✅ Next steps (what comes after)

### Functionality

**Must Have:**
- ✅ Task selection (single, multiple, range)
- ✅ Prompt generation (user-friendly)
- ✅ Context preservation (dependencies)

**Should Have:**
- ✅ Subtask breakdown (auto for >8h)
- ✅ Completed task tracking (--skip-completed)
- ✅ Platform-specific (--cursor, --antigravity)

**Nice to Have:**
- ✅ Interactive mode (ask user)
- ✅ Batch generation (all tasks)
- ✅ Progress tracking (mark completed)

---

## 📝 Implementation Plan

### Phase 3: Workflow Implementation

**Step 1: Create Workflow File**
- File: `.kilocode/workflows/smartspec_generate_cursor_prompt.md`
- Structure: Arguments parsing, task selection, prompt generation

**Step 2: Implement Core Logic**
- Parse arguments
- Read tasks.md
- Select tasks
- Build context
- Generate prompts

**Step 3: Implement Advanced Features**
- Subtask breakdown
- Completed task tracking
- Platform-specific optimizations

**Step 4: Testing**
- Test with real tasks.md
- Verify prompt quality
- Test all command patterns

---

## 🎉 Expected Output Examples

### Example 1: Single Task

**Command:**
```bash
/smartspec_generate_cursor_prompt tasks.md --task T001
```

**Output:**
```
✅ Prompt generated successfully!

📁 File: cursor-prompt-T001.md
📊 Tasks: 1 (T001)
⏱️ Time: 2 hours
🎯 Platform: Cursor

💡 Next steps:
1. Open cursor-prompt-T001.md
2. Copy the prompt
3. Paste into Cursor
4. Start coding!
```

---

### Example 2: Multiple Tasks

**Command:**
```bash
/smartspec_generate_cursor_prompt tasks.md --task T001-T005
```

**Output:**
```
✅ Prompt generated successfully!

📁 File: cursor-prompt-T001-T005.md
📊 Tasks: 5 (T001, T002, T003, T004, T005)
⏱️ Time: 12 hours
🎯 Platform: Cursor

📋 Tasks included:
- T001: Create User entity (2h)
- T002: Create AuthService (3h)
- T003: Setup database (2h)
- T004: Create endpoints (3h)
- T005: Write tests (2h)

💡 Next steps:
1. Open cursor-prompt-T001-T005.md
2. Copy the prompt
3. Paste into Cursor
4. Implement all 5 tasks
```

---

### Example 3: Subtask Breakdown

**Command:**
```bash
/smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown
```

**Output:**
```
✅ Task breakdown completed!

🔄 T050 (12h) broken down into 4 subtasks:

📁 Files generated:
- cursor-prompt-T050.1.md (3h)
- cursor-prompt-T050.2.md (3h)
- cursor-prompt-T050.3.md (3h)
- cursor-prompt-T050.4.md (3h)

📋 Subtasks:
- T050.1: Create User model (3h)
- T050.2: Implement AuthService (3h)
- T050.3: Create API endpoints (3h)
- T050.4: Add middleware and tests (3h)

💡 Next steps:
1. Start with cursor-prompt-T050.1.md
2. Complete T050.1 first
3. Then move to T050.2
4. Continue sequentially
```

---

**Status:** 🏗️ Architecture Complete
**Next:** 💻 Implementation
