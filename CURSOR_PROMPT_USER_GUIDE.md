# Cursor/Antigravity Prompt Generator - User Guide
## Vibe Coding with SmartSpec

**Version:** 1.0.0  
**Date:** 2025-01-04  
**Workflow:** `smartspec_generate_cursor_prompt.md`

---

## 🎯 What Is This?

แปลง **technical tasks.md** เป็น **user-friendly prompts** สำหรับ Cursor/Antigravity

**Problem:**
- tasks.md เทคนิคเกินไป ❌
- ยากต่อการเข้าใจ ❌
- ไม่เหมาะกับ vibe coding ❌

**Solution:**
- Simple prompts ✅
- Step-by-step instructions ✅
- Perfect for copy-paste ✅

---

## 🚀 Quick Start

### Basic Usage

```bash
# Generate prompt for single task
/smartspec_generate_cursor_prompt tasks.md --task T001

# Output: cursor-prompt-T001.md
# Copy and paste to Cursor!
```

### Common Patterns

```bash
# Single task
/smartspec_generate_cursor_prompt tasks.md --task T001

# Multiple tasks
/smartspec_generate_cursor_prompt tasks.md --task T001,T002,T003

# Task range
/smartspec_generate_cursor_prompt tasks.md --task T001-T010

# Large task with breakdown
/smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown

# Skip completed tasks
/smartspec_generate_cursor_prompt tasks.md --task T001-T020 --skip-completed

# For Antigravity
/smartspec_generate_cursor_prompt tasks.md --task T001 --antigravity
```

---

## 📖 Use Cases

### Use Case 1: Vibe Coding (One Task at a Time)

**Scenario:** ทำทีละ task ด้วย Cursor

```bash
# Step 1: Generate prompt for T001
$ /smartspec_generate_cursor_prompt tasks.md --task T001

# Step 2: Open the generated file
$ open cursor-prompt-T001.md

# Step 3: Copy prompt and paste to Cursor

# Step 4: Implement with Cursor's help

# Step 5: Move to next task
$ /smartspec_generate_cursor_prompt tasks.md --task T002
```

**Benefits:**
- ✅ Focus on one task
- ✅ Clear instructions
- ✅ Easy to understand

---

### Use Case 2: Batch Tasks

**Scenario:** ทำหลาย tasks พร้อมกัน

```bash
# Generate prompt for T001-T005
$ /smartspec_generate_cursor_prompt tasks.md --task T001-T005

# Output: cursor-prompt-T001-T005.md
# Contains all 5 tasks with clear separation
```

**Benefits:**
- ✅ See all tasks together
- ✅ Understand flow
- ✅ Implement in sequence

---

### Use Case 3: Large Task Breakdown

**Scenario:** Task ใหญ่ต้องแบ่งเป็น subtasks

```bash
# T050 is 12 hours (too large!)
$ /smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown

# Output: 4 files
# - cursor-prompt-T050.1.md (3h)
# - cursor-prompt-T050.2.md (3h)
# - cursor-prompt-T050.3.md (3h)
# - cursor-prompt-T050.4.md (3h)
```

**Benefits:**
- ✅ Manageable size
- ✅ Clear scope
- ✅ Better progress tracking

---

### Use Case 4: Hybrid Workflow

**Scenario:** สลับระหว่าง Kilo Code และ Cursor

```bash
# Phase 1: Use Kilo Code (autonomous)
$ kilo code implement tasks.md --task T001-T010
# T001-T010 completed ✅

# Phase 2: Switch to Cursor (manual control)
$ /smartspec_generate_cursor_prompt tasks.md --task T011-T015 --skip-completed
# Only generates prompts for T011-T015
# Knows T001-T010 are done

# Phase 3: Back to Kilo Code
$ kilo code implement tasks.md --task T016-T050 --skip-completed
```

**Benefits:**
- ✅ Flexibility
- ✅ Platform switching
- ✅ Context preserved

---

### Use Case 5: Team Collaboration

**Scenario:** ทีมทำคนละส่วน

```bash
# Dev A: Database layer
$ /smartspec_generate_cursor_prompt tasks.md --task T001-T010

# Dev B: API layer
$ /smartspec_generate_cursor_prompt tasks.md --task T011-T020

# Dev C: Frontend
$ /smartspec_generate_cursor_prompt tasks.md --task T021-T030
```

**Benefits:**
- ✅ Clear boundaries
- ✅ Independent work
- ✅ Easy merging

---

## 🎨 Command Reference

### Basic Commands

#### Single Task

```bash
/smartspec_generate_cursor_prompt tasks.md --task T001
```

**Output:**
- File: `cursor-prompt-T001.md`
- Content: Detailed instructions for T001

---

#### Multiple Tasks (Comma-Separated)

```bash
/smartspec_generate_cursor_prompt tasks.md --task T001,T002,T003
```

**Output:**
- File: `cursor-prompt-T001-T003.md`
- Content: Combined instructions for 3 tasks

---

#### Task Range

```bash
/smartspec_generate_cursor_prompt tasks.md --task T001-T010
```

**Output:**
- File: `cursor-prompt-T001-T010.md`
- Content: Instructions for T001 through T010

---

### Advanced Commands

#### Breakdown Large Task

```bash
/smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown
```

**What it does:**
- Analyzes T050 (e.g., 12 hours)
- Breaks into subtasks (T050.1, T050.2, ...)
- Each subtask 2-4 hours
- Generates separate prompt for each

**Output:**
- `cursor-prompt-T050.1.md`
- `cursor-prompt-T050.2.md`
- `cursor-prompt-T050.3.md`
- `cursor-prompt-T050.4.md`

---

#### Skip Completed Tasks

```bash
/smartspec_generate_cursor_prompt tasks.md --task T001-T020 --skip-completed
```

**What it does:**
- Reads tasks.md checkbox status
- Skips tasks marked `[x]`
- Only generates prompts for `[ ]` tasks
- Includes context from completed tasks

**Example:**
```markdown
# tasks.md
- [x] T001: Done
- [x] T002: Done
- [ ] T003: Not done
- [ ] T004: Not done
```

**Result:**
- Only generates prompt for T003, T004
- Includes context from T001, T002

---

#### Platform-Specific

```bash
# For Cursor (default)
/smartspec_generate_cursor_prompt tasks.md --task T001

# For Antigravity
/smartspec_generate_cursor_prompt tasks.md --task T001 --antigravity
```

**Differences:**
- Different tips and tricks
- Different workflow suggestions
- Optimized for each platform

---

#### Specific Subtasks

```bash
/smartspec_generate_cursor_prompt tasks.md --subtask T050.1,T050.2
```

**What it does:**
- Generates prompt for specific subtasks only
- Useful if subtasks already exist in tasks.md

---

#### All Tasks

```bash
/smartspec_generate_cursor_prompt tasks.md --all
```

**What it does:**
- Generates one prompt file per task
- Creates multiple files
- Useful for batch generation

**Output:**
- `cursor-prompt-T001.md`
- `cursor-prompt-T002.md`
- `cursor-prompt-T003.md`
- ...

---

## 📝 Prompt Structure

### What's in a Prompt?

Every generated prompt includes:

#### 1. 🎯 What You'll Build
Simple, non-technical description

**Example:**
```markdown
## 🎯 What You'll Build

A User entity model with email and password fields.

This model will be used throughout the authentication system
to represent user data and handle validation.
```

---

#### 2. 📋 Context
Previous tasks, dependencies, files

**Example:**
```markdown
## 📋 Context

**Phase:** Phase 1 - Database Layer
**Position:** First task in this phase
**Dependencies:** None

**What comes after:**
- T002 will create AuthService that uses this User entity
- T003 will create API endpoints that use this User entity
```

---

#### 3. 🔧 Implementation Steps
Step-by-step instructions

**Example:**
```markdown
## 🔧 Implementation Steps

### Step 1: Create the User Entity File
Create a new file: `src/models/User.ts`

### Step 2: Define the User Class
Add a User class with these properties:
- `email`: string
- `password`: string
- `createdAt`: Date
- `updatedAt`: Date

### Step 3: Add Validation Methods
Add `validateEmail()` and `validatePassword()` methods

### Step 4: Export the Class
Export the User class for use in other files
```

---

#### 4. 💻 Code Structure
Example code skeleton

**Example:**
```markdown
## 💻 Code Structure

```typescript
// src/models/User.ts

export class User {
  email: string;
  password: string;
  createdAt: Date;
  updatedAt: Date;

  constructor(email: string, password: string) {
    // Initialize
  }

  validateEmail(): boolean {
    // Validation logic
  }

  validatePassword(): boolean {
    // Validation logic
  }
}
```
```

---

#### 5. 📁 Files
What to create/edit/use

**Example:**
```markdown
## 📁 Files

**Create:**
- `src/models/User.ts` (~80 lines, SMALL)

**Edit:**
- None

**Use:**
- None (this is the first task)
```

---

#### 6. ✅ Validation
How to verify

**Example:**
```markdown
## ✅ Validation

After implementing, run:

```bash
tsc --noEmit
npm test
npm run lint
```

**Expected Results:**
- ✅ No TypeScript errors
- ✅ All tests passing
- ✅ No lint errors
```

---

#### 7. ⏱️ Estimated Time
Time estimate with breakdown

**Example:**
```markdown
## ⏱️ Estimated Time

**2 hours**

This includes:
- Creating the file (10 min)
- Implementing the class (60 min)
- Adding validation (30 min)
- Testing (20 min)
```

---

#### 8. ➡️ Next Steps
What comes after

**Example:**
```markdown
## ➡️ Next Steps

After completing this task:

1. Validate your implementation
2. Mark task as complete: `- [x] T001`
3. Commit your changes
4. Move to T002: Create AuthService
```

---

#### 9. 💡 Tips
Platform-specific tips

**Example:**
```markdown
## 💡 Tips

**Cursor Tips:**
- Use `Cmd+K` to ask Cursor for help
- Use Tab to accept suggestions
- Use `Cmd+L` to select code and ask questions

**Cursor Workflow:**
1. Create `src/models/User.ts`
2. Type `class User` and let Cursor suggest
3. Accept with Tab
4. Ask: "Add email validation"
5. Review and accept
```

---

#### 10. 🔗 Dependencies
What depends on what

**Example:**
```markdown
## 🔗 Dependencies

**This task depends on:**
- None (starting point)

**Tasks that depend on this:**
- T002: Create AuthService
- T003: Create API endpoints
```

---

## 🎯 Best Practices

### 1. Start Small

**Do:**
```bash
# Start with one task
/smartspec_generate_cursor_prompt tasks.md --task T001
```

**Don't:**
```bash
# Don't start with all tasks
/smartspec_generate_cursor_prompt tasks.md --all
```

**Why:** Start small to understand the flow

---

### 2. Follow Sequence

**Do:**
```bash
# T001 → T002 → T003
/smartspec_generate_cursor_prompt tasks.md --task T001
# Complete T001
/smartspec_generate_cursor_prompt tasks.md --task T002
# Complete T002
/smartspec_generate_cursor_prompt tasks.md --task T003
```

**Don't:**
```bash
# Don't jump around
/smartspec_generate_cursor_prompt tasks.md --task T005
# T001-T004 not done yet!
```

**Why:** Dependencies matter

---

### 3. Break Large Tasks

**Do:**
```bash
# T050 is 12h (too large)
/smartspec_generate_cursor_prompt tasks.md --task T050 --breakdown
# Get 4 smaller tasks (3h each)
```

**Don't:**
```bash
# Don't try to do 12h task at once
/smartspec_generate_cursor_prompt tasks.md --task T050
```

**Why:** Smaller tasks are more manageable

---

### 4. Mark Completed

**Do:**
```markdown
# After completing T001, mark it in tasks.md
- [x] T001: Create User entity
```

**Why:** Enables --skip-completed feature

---

### 5. Use Context

**Do:**
- Read the Context section
- Understand dependencies
- Know what came before

**Don't:**
- Skip the Context section
- Ignore dependencies

**Why:** Context helps you understand the big picture

---

## 🔄 Workflow Examples

### Example 1: Solo Developer

```bash
# Day 1: Database layer
$ /smartspec_generate_cursor_prompt tasks.md --task T001
# Implement T001 with Cursor
$ /smartspec_generate_cursor_prompt tasks.md --task T002
# Implement T002 with Cursor
$ /smartspec_generate_cursor_prompt tasks.md --task T003
# Implement T003 with Cursor

# Day 2: API layer
$ /smartspec_generate_cursor_prompt tasks.md --task T004-T008
# Implement all 5 tasks together

# Day 3: Frontend
$ /smartspec_generate_cursor_prompt tasks.md --task T009-T015
# Implement frontend tasks
```

---

### Example 2: Team of 3

```bash
# Dev A: Database (T001-T010)
$ /smartspec_generate_cursor_prompt tasks.md --task T001-T010
# Works on database layer

# Dev B: API (T011-T020)
$ /smartspec_generate_cursor_prompt tasks.md --task T011-T020
# Works on API layer

# Dev C: Frontend (T021-T030)
$ /smartspec_generate_cursor_prompt tasks.md --task T021-T030
# Works on frontend
```

---

### Example 3: Hybrid Approach

```bash
# Use Kilo Code for routine tasks
$ kilo code implement tasks.md --task T001-T010
# Autonomous execution

# Switch to Cursor for complex tasks
$ /smartspec_generate_cursor_prompt tasks.md --task T011-T015 --skip-completed
# Manual control for complex logic

# Back to Kilo Code for remaining tasks
$ kilo code implement tasks.md --task T016-T050 --skip-completed
# Autonomous execution
```

---

## 🚨 Troubleshooting

### Issue: "Task not found"

**Error:**
```
❌ Error: Task not found
Task ID "T999" does not exist
```

**Solution:**
- Check task ID spelling
- Verify task exists in tasks.md
- Use correct format (T001, not t001 or Task001)

---

### Issue: "Unmet dependencies"

**Warning:**
```
⚠️ Warning: Unmet dependencies
Task T003 depends on T001, T002 (not completed)
```

**Solution:**
- Complete T001 and T002 first, OR
- Generate prompt for T001-T003 together, OR
- Ignore warning if you know what you're doing

---

### Issue: "Invalid task range"

**Error:**
```
❌ Error: Invalid task range
Range "T010-T001" is invalid
```

**Solution:**
- Use correct order: T001-T010 (not T010-T001)
- Start must be before end

---

### Issue: Prompt too technical

**Problem:** Generated prompt still too technical

**Solution:**
- This is a bug - please report
- Workflow should generate simple prompts
- Check if you're using the right workflow

---

## 💡 Tips & Tricks

### Tip 1: Use with Cursor Composer

```bash
# Generate prompt
$ /smartspec_generate_cursor_prompt tasks.md --task T001

# Open in Cursor Composer
# Paste the entire prompt
# Let Cursor implement everything
```

---

### Tip 2: Combine with Git Branches

```bash
# Create branch per task
$ git checkout -b feature/T001

# Generate and implement
$ /smartspec_generate_cursor_prompt tasks.md --task T001
# Implement with Cursor

# Commit and merge
$ git commit -am "Implement T001"
$ git checkout main
$ git merge feature/T001
```

---

### Tip 3: Use for Code Review

```bash
# Generate prompt for completed task
$ /smartspec_generate_cursor_prompt tasks.md --task T001

# Use prompt as checklist for code review
# Verify all steps were completed
# Check all files were created
# Validate acceptance criteria
```

---

### Tip 4: Batch Generate for Planning

```bash
# Generate all prompts at once
$ /smartspec_generate_cursor_prompt tasks.md --all

# Review all prompts
# Understand full scope
# Plan your approach
```

---

## 📚 Related Workflows

### Generate Implement Prompt

```bash
# For AI agents (Kilo Code, Claude Code)
/smartspec_generate_implement_prompt tasks.md --kilocode
```

**Use when:** You want autonomous execution

---

### Implement Tasks

```bash
# Auto-implement with tracking
/smartspec_implement_tasks tasks.md --task T001-T010
```

**Use when:** You want fully automated implementation

---

### Generate Tasks

```bash
# Generate tasks.md from spec
/smartspec_generate_tasks spec.md
```

**Use when:** You need to create tasks.md first

---

## 🎉 Success Stories

### Story 1: Solo Developer

> "I used to struggle with technical tasks.md. Now I generate simple prompts and use Cursor to implement. So much easier!"

---

### Story 2: Team Lead

> "My team uses this for all new features. Each developer gets clear prompts. No more confusion about what to build."

---

### Story 3: Hybrid User

> "I use Kilo Code for routine tasks and Cursor for complex logic. This workflow makes switching seamless."

---

## 📞 Support

**Documentation:**
- Analysis: `CURSOR_ANTIGRAVITY_ANALYSIS.md`
- Architecture: `CURSOR_PROMPT_ARCHITECTURE.md`
- This guide: `CURSOR_PROMPT_USER_GUIDE.md`

**Issues:**
- Check troubleshooting section
- Review examples
- Read architecture docs

**Feedback:**
- Report bugs
- Suggest improvements
- Share success stories

---

## 🚀 Next Steps

1. **Try it out:**
   ```bash
   /smartspec_generate_cursor_prompt tasks.md --task T001
   ```

2. **Read generated prompt**

3. **Copy to Cursor**

4. **Start coding!**

---

**Happy Vibe Coding! 🎨**
