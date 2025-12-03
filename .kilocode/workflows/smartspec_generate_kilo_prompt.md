---
description: Generate comprehensive Kilo Code/Claude Code implementation prompt from tasks.md with safety constraints, supporting files integration, and error recovery procedures.
---

## User Input
```text
$ARGUMENTS
```

**Patterns:**
- `specs/feature/spec-004/tasks.md`
- `specs/feature/spec-004/tasks.md --specindex="path"`

## 0. Load Context

Read `.smartspec/` files, parse --specindex → Load SPEC_INDEX into SPEC_REGISTRY

## 1. Resolve Paths

Extract tasks.md path from arguments
Set TASKS_DIR = directory of tasks.md
Set OUTPUT = TASKS_DIR/kilo-prompt.md (or timestamped if exists)

## 2. Read & Parse tasks.md

Parse structure:
- Project metadata
- Phase overview table
- All phases with tasks
- Checkpoints
- Supporting files references

Extract:
- Total phases/tasks
- High-risk phases
- Dependencies
- Validation requirements

## 3. Scan Supporting Files

Detect in TASKS_DIR:
- openapi.yaml / api-spec.yaml
- data-model.md
- README.md
- research.md
- test-plan.md
- Other relevant files

Read content for context integration

## 4. Generate Prompt Header

```markdown
# Kilo Code & Claude Code Implementation: [Project Name]

**Generated:** YYYY-MM-DD HH:mm
**Author:** SmartSpec Architect v4.0
**Source Tasks:** [Path to tasks.md]
**Source SPEC:** [SPEC-ID] v[X.Y.Z]
**SPEC_INDEX:** [Path used]

---

## Project Overview

**Status:** IMPLEMENTATION
**Total Phases:** X
**Total Tasks:** XX
**Estimated Effort:** XX hours
**Technology Stack:** [From tasks.md]

**Supporting Documentation:**
- 📄 SPEC: [Link to spec.md]
- 📋 Tasks: [Link to tasks.md]
- 🔌 API Spec: [Link to openapi.yaml if exists]
- 📊 Data Model: [Link to data-model.md if exists]
- 📖 README: [Link to README.md if exists]

**Related Specs:** (Resolved from SPEC_INDEX)
[For each referenced spec:]
- **[spec-id]** (`[path]`, repo: [repo]) - [Title]

---
```

## 5. Critical Execution Constraints

```markdown
## 🚨 CRITICAL EXECUTION CONSTRAINTS

**THESE RULES ARE NON-NEGOTIABLE**

### Hard Limits (NEVER VIOLATE)
- ❌ Maximum 10 tasks per execution cycle
- ❌ Maximum 5 file edits per task
- ❌ Maximum 50 lines per str_replace operation
- ❌ Maximum 2 retry attempts per failed operation
- ❌ STOP at 3 consecutive errors

### File Size Strategy (MANDATORY)

**SMALL Files (< 200 lines):**
- CREATE: Full file generation is safe
- EDIT: Any method OK (str_replace or full rewrite)
- No special handling needed

**MEDIUM Files (200-500 lines):**
- CREATE: Staged creation preferred
- EDIT: **str_replace ONLY** - NO full file rewrites
- Max 50 lines per str_replace

**LARGE Files (> 500 lines):**
- CREATE: Incremental build required
- EDIT: **Surgical str_replace ONLY**
- Max 50 lines per operation
- Multiple small edits instead of one large edit

### Error Handling Protocol

**Attempt 1:** Identify issue, apply fix, retry
**Attempt 2:** Different approach, verify context, retry
**Attempt 3:** **STOP IMMEDIATELY**
- DO NOT continue
- Report error details
- Request manual guidance

### Context Management

**At 80% token usage:**
- Stop execution
- Create checkpoint
- Report progress: "Completed T001-T0XX"
- Wait for user to restart from next task

**On context overflow:**
- Immediate checkpoint
- Save state
- Report: "Restart from T0XX"

### Validation Requirements (EVERY TASK)

**After EACH task completion:**
```bash
# TypeScript projects
tsc --noEmit

# Import resolution
# (verify no broken imports)

# Tests (if exist)
npm test -- [relevant-test-file]

# Linting (critical only)
npm run lint
```

**If validation fails:**
- Fix immediately
- Do NOT proceed to next task
- Re-validate before continuing

### Supporting Files Integration

**When tasks reference supporting files:**

**openapi.yaml:**
- Use for endpoint definitions
- Reference for request/response schemas
- Validation rules

**data-model.md:**
- Use for entity relationships
- Database schema reference
- Field definitions

**README.md:**
- Setup instructions
- Environment requirements
- Development workflow

**Example task integration:**
```markdown
Task T015: Create GET /api/v1/balance endpoint

Supporting Files:
- openapi.yaml: Line 45-60 defines endpoint spec
- data-model.md: Credit entity schema for queries

Implementation:
1. Read openapi.yaml endpoint definition
2. Use data-model.md Credit schema
3. Implement according to specs
```

---
```

## 6. Progressive Execution Guide

```markdown
## 📖 How to Execute This Project

**CRITICAL: Follow This Exact Pattern**

### Execution Philosophy
🐢 **Slow and steady wins**
✅ **Validate everything**
🛑 **Stop on errors**
📊 **Report progress**

### Step-by-Step Process

**Step 1: Preparation**
- Read this ENTIRE prompt
- Understand all phases
- Note checkpoints
- Review supporting files
- Prepare incremental execution

**Step 2: Start Phase 1**

Execute **ONLY Task T001:**
1. Read complete task description
2. Review supporting files referenced
3. Create/edit specified files
4. Use appropriate strategy (SMALL/MEDIUM/LARGE)
5. Validate immediately:
   ```bash
   tsc --noEmit
   npm test -- <relevant-test>
   ```
6. **If PASS:** Continue to T002
7. **If FAIL:** Fix, re-validate, then continue

**Step 3: Continue Through Phase 1**

For T002-T010:
- ONE task at a time
- Validate after EACH task
- Stop at mini-checkpoint (T005)
- Validate mini-checkpoint
- Continue to T006-T010
- Stop at major checkpoint (T010)

**Step 4: Major Checkpoint (End of Phase)**

Run comprehensive validation:
```bash
# Full compilation
tsc --noEmit

# All tests
npm test

# Linting
npm run lint

# Integration check
# (verify phase goals met)
```

**If ALL pass:**
- Generate checkpoint report
- Get user confirmation
- Proceed to Phase 2

**If ANY fail:**
- **STOP**
- Fix all issues
- Re-validate
- Do not continue until 100% pass

**Step 5: Repeat for Remaining Phases**

Continue pattern for Phase 2, 3, 4...
- One task at a time
- Validate everything
- Stop at checkpoints
- Fix before continuing

### Token/Context Management

**Monitor usage continuously:**

**At 80% tokens:**
- Stop current task
- Complete validation
- Report: "Phase X, completed T001-T0YY"
- Instructions: "Restart from T0YY+1"

**On overflow:**
- Immediate stop
- Checkpoint state
- Report current position

### Supporting Files Workflow

**Before starting each task:**
1. Check if task references supporting files
2. Read referenced sections
3. Use information in implementation
4. Verify alignment with supporting docs

**Example:**
```
Task T020: Implement user authentication

References:
- openapi.yaml: /auth/login endpoint (line 120)
- data-model.md: User entity (section 3)

Steps:
1. Read openapi.yaml lines 120-140
2. Read data-model.md section 3
3. Implement per specifications
4. Validate against schemas
```

---
```

## 7. Error Recovery Procedures

```markdown
## 🛡️ ERROR RECOVERY PROCEDURES

### str_replace Failures

**Attempt 1: Context Review**
```typescript
// If str_replace fails:
1. view('file.ts', view_range=[start-10, end+10])
2. Find EXACT text match (including whitespace)
3. Retry str_replace with precise match
```

**Attempt 2: Expand Context**
```typescript
// If still fails:
1. view('file.ts', view_range=[start-50, end+50])
2. Include more surrounding context
3. Adjust match pattern
4. Retry with expanded pattern
```

**Attempt 3: STOP**
```
❌ DO NOT RETRY AGAIN

Report:
- File: [path]
- Operation: str_replace
- Attempts: 3
- Last error: [message]
- Context: [show relevant lines]

Request: Manual guidance needed
```

### Compilation Errors

**Error Detected:**
```bash
$ tsc --noEmit
error TS2304: Cannot find name 'User'
```

**Response:**
1. **DO NOT** continue to next task
2. Identify root cause
3. Fix error (import, type definition, etc.)
4. Re-compile
5. Verify fix successful
6. **THEN** continue

**If cannot fix after 2 attempts:**
- STOP
- Report error details
- Request guidance

### Test Failures

**Attempt 1: Fix Implementation**
```typescript
// Test fails:
1. Read test code
2. Understand expectation
3. Fix implementation
4. Re-run test
```

**Attempt 2: Verify Test Logic**
```typescript
// If still fails:
1. Review test logic
2. Check if test or code is wrong
3. Fix appropriate side
4. Re-run
```

**Attempt 3: STOP**
```
Report:
- Test: [name]
- Failure: [message]
- Attempts: 3
- Request: Manual review
```

### Context Overflow

**When approaching limit:**
```markdown
🛑 TOKEN USAGE: 85%

STOPPING EXECUTION

Progress Report:
- Completed: Phase 1 (T001-T010) ✅
- Completed: Phase 2 (T011-T018) ✅
- Current: Phase 2, Task T019 (in progress)

Validation:
- Compilation: ✅ PASS
- Tests: ✅ PASS (95% coverage)
- Linting: ✅ PASS

Next Steps:
1. Resume from Task T019
2. Provide prompt: "Continue Phase 2 from T019"
3. I will pick up exactly where I left off

Files Modified This Session:
- [list of files with changes]

State saved. Ready for continuation.
```

### Integration Issues

**If integration with existing code breaks:**
1. Identify breaking change
2. Review affected components
3. Fix backward compatibility
4. Re-validate integration
5. Update tests if needed

**If cannot resolve:**
- STOP
- Report:
  - What broke
  - Which components affected
  - Attempted fixes
- Request architecture review

---
```

## 8. Phase & Task Details

For each phase from tasks.md:

```markdown
## 📋 Phase [X]: [Phase Name] (T00A–T00B)

**Objective:** [Phase goal from tasks.md]

**Focus Areas:**
- [Area 1]
- [Area 2]

**Risk Level:** [LOW/MEDIUM/HIGH/CRITICAL]
**Estimated Effort:** [XX hours]

**Supporting Files for This Phase:**
- [List relevant supporting files]

---

### Task T00X: [Task Title] (~X.X hours)

**Description:**
[From tasks.md - concrete implementation details]

**Files:**

**CREATE: `[path/to/file.ts]`** (~XXX lines - SMALL)
- Purpose: [What this file does]
- Key functions: [List]
- Strategy: Full creation safe
- Supporting file reference: [If any]

**EDIT: `[path/to/existing.ts]`** (add XX lines - MEDIUM)
- Location: [Where to edit]
- Change: [What to change]
- Strategy: **str_replace ONLY** (MEDIUM file - no full rewrite)
- Max lines per change: 50
- Supporting file reference: [If any]

**Dependencies:**
- T00Y: [Reason]
- Related Spec: **[spec-id]** (`[path]`, repo: [repo])

**Validation:**
```bash
tsc --noEmit
npm test -- path/to/test.test.ts
```

**Expected Outcome:**
[What should work after this task]

**Supporting Files Integration:**
- `openapi.yaml` (lines XX-YY): Endpoint definition for this feature
- `data-model.md` (section Z): Entity schema to use

---

[Continue for all tasks in phase...]

### 🔍 Mini-Checkpoint: T00X-T00Y

**Validation:**
- [ ] Files created as expected
- [ ] No compilation errors
- [ ] Tests passing
- [ ] No critical lint issues

**If any fails:** Fix before continuing

---

[At end of phase:]

## ⚡ CHECKPOINT: Phase [X] Complete

**Comprehensive Validation:**

**Code Quality:**
- [ ] TypeScript compilation passes
- [ ] All tests passing
- [ ] No critical lint errors
- [ ] Code coverage ≥ [target]%

**Functionality:**
- [ ] All [X] tasks completed
- [ ] Acceptance criteria met
- [ ] Integration verified
- [ ] Supporting files alignment confirmed

**Documentation:**
- [ ] Code comments present
- [ ] README updated (if needed)

**Performance:**
- [ ] No obvious bottlenecks
- [ ] Response times acceptable

**Security:**
- [ ] No vulnerabilities introduced
- [ ] Auth/authz working

**Integration:**
- [ ] Works with existing system
- [ ] No breaking changes

**⚠️ CRITICAL:**
- If ANY validation fails: **STOP**
- Fix ALL issues before Phase [X+1]
- Do not accumulate technical debt

**Next Steps:**
Continue to Phase [X+1]: [Phase name]

---
```

## 9. Alternative: Claude Code Instructions

```markdown
## 🔧 CLAUDE CODE COMPATIBILITY

This prompt is designed for both Kilo Code and Claude Code.

### Claude Code Specific Notes

**Terminal Commands:**
Same bash commands work in Claude Code terminal.

**File Operations:**
- Use Claude Code's file editing capabilities
- Apply same size-based strategies (SMALL/MEDIUM/LARGE)
- Same validation requirements

**Context Management:**
Claude Code has different token management:
- Monitor context in Claude Code interface
- Apply same checkpoint patterns
- Stop and restart as needed

**Execution Pattern:**
Same incremental execution:
1. One task at a time
2. Validate after each
3. Stop at checkpoints
4. Continue after validation

### Key Differences

| Aspect | Kilo Code | Claude Code |
|--------|-----------|-------------|
| Execution | Automated | Interactive |
| Context | Auto-managed | User-monitored |
| Validation | Must command | Can suggest |
| Recovery | Explicit protocol | Flexible |

**Bottom Line:** Core workflow identical, execution environment differs.

---
```

## 10. Safety Checklist

```markdown
## 🔒 SAFETY CHECKLIST

**Before Starting Implementation:**

**I understand and accept:**
- [ ] Maximum 10 tasks per execution cycle
- [ ] File size strategies (SMALL/MEDIUM/LARGE)
- [ ] str_replace-only for MEDIUM/LARGE files
- [ ] Maximum 50 lines per str_replace
- [ ] Stop at 3 consecutive errors
- [ ] Validation after EVERY task
- [ ] Checkpoints are mandatory
- [ ] Progress reporting required
- [ ] Supporting files must be referenced
- [ ] Spec alignment must be verified

**I will:**
- [ ] Execute ONE task at a time
- [ ] Validate after EACH task
- [ ] Stop on validation failure
- [ ] Report progress at checkpoints
- [ ] Use supporting files appropriately
- [ ] Follow error recovery procedures
- [ ] Respect token/context limits
- [ ] Not skip any safety steps

**I will NOT:**
- [ ] Skip tasks or rush ahead
- [ ] Ignore validation failures
- [ ] Rewrite MEDIUM/LARGE files entirely
- [ ] Exceed str_replace line limits
- [ ] Continue after 3 errors
- [ ] Modify supporting files unless instructed

---

✅ All checks confirmed
🚀 Ready to begin implementation

---
```

## 11. Write Prompt File

Determine output path (non-conflicting)
Write complete prompt to file

## 12. Report (Thai)

```
✅ สร้าง Implementation Prompt เรียบร้อยแล้ว

📁 ไฟล์: [Path to kilo-prompt.md]
📊 Structure:
- Phases: X
- Tasks: XX
- Hours: YY estimated

🔒 Safety Features:
- File size strategies: ✅
- Error recovery: ✅
- Checkpoints: X points
- Validation: After every task

📄 Supporting Files Integrated:
- openapi.yaml: API specs
- data-model.md: Data schemas
- README.md: Setup guide
- [Other files if any]

🔗 Spec References Resolved: X specs

💡 วิธีใช้:

**สำหรับ Kilo Code:**
```bash
kilo code implement kilo-prompt.md
```

**สำหรับ Claude Code:**
1. เปิด Claude Code
2. Load prompt file
3. Execute ทีละ task
4. Follow checkpoint pattern

⚠️ Important:
- Execute ONE task at a time
- Validate after EACH task
- Stop at checkpoints
- Use supporting files

🔄 ต่อไป:
1. Review prompt
2. Prepare environment
3. Start Phase 1, Task T001
4. Execute incrementally
```

---

Context: $ARGUMENTS
