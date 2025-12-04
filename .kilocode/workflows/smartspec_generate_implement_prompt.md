---
description: Generate comprehensive implementation prompt from tasks.md with platform-specific instructions (Kilo Code/Claude Code/Roo Code), safety constraints, supporting files integration, and flexible validation commands.
---

## User Input
```text
$ARGUMENTS
```

**Patterns:**
- `specs/feature/spec-004/tasks.md`
- `specs/feature/spec-004/tasks.md --phase 1`
- `specs/feature/spec-004/tasks.md --phase 1,2,3`
- `specs/feature/spec-004/tasks.md --phase 1-3`
- `specs/feature/spec-004/tasks.md --tasks T001`
- `specs/feature/spec-004/tasks.md --tasks T001,T002,T003`
- `specs/feature/spec-004/tasks.md --tasks T001-T010`
- `specs/feature/spec-004/tasks.md --kilocode`
- `specs/feature/spec-004/tasks.md --claude`
- `specs/feature/spec-004/tasks.md --roocode`
- `specs/feature/spec-004/tasks.md --phase 1-2 --tasks T001-T010 --kilocode`
- `specs/feature/spec-004/tasks.md --specindex=".smartspec/SPEC_INDEX.json"`

**Default Behavior:**
- Platform: `--claude` (most popular, if not specified)
- Phase: all phases (if not specified)
- Tasks: all tasks (if not specified)
- SPEC_INDEX: auto-detect `.smartspec/SPEC_INDEX.json` if exists

## 0. Load Context

**Read `.smartspec/` files:**
- If user provides `--specindex="path"`: Load from specified path
- Else: Auto-detect `.smartspec/SPEC_INDEX.json` in project root
- If found: Parse and load into SPEC_REGISTRY
- If not found: Continue without dependency resolution (log warning)

**Parse Arguments:**
- Extract tasks.md path
- Parse `--phase` parameter (single, comma-separated, or range)
- Parse `--tasks` parameter (single, comma-separated, or range)
- Parse platform flag: `--kilocode`, `--claude`, `--roocode`
- Default platform: `--claude` if none specified

## 1. Resolve Paths

Extract tasks.md path from arguments
Set TASKS_DIR = directory of tasks.md
Extract SPEC_ID from path or tasks.md metadata

**Determine output filename:**
- Pattern: `implement-prompt-<spec-id>-<timestamp>.md`
- Example: `implement-prompt-spec-004-20250104-143022.md`
- If file exists: Use timestamped version
- Output location: TASKS_DIR/

## 2. Read & Parse tasks.md

**Parse YAML frontmatter (if exists):**
```yaml
---
spec_id: spec-004-financial-system
version: 1.0.0
technology_stack: TypeScript, Node.js, PostgreSQL
validation_commands:
  compile: "tsc --noEmit"
  test: "npm test -- {test_file}"
  lint: "npm run lint"
  integration: "npm run test:integration"
---
```

**If frontmatter missing:**
- Use default TypeScript validation commands
- Log warning: "No validation_commands in frontmatter, using TypeScript defaults"

**Parse structure:**
- Project metadata
- Phase overview table
- All phases with tasks
- Checkpoints
- Supporting files references

**Extract:**
- Total phases/tasks
- High-risk phases
- Dependencies
- Validation requirements
- Technology stack

**Validate format:**
- [ ] Has Project Metadata section
- [ ] Has Phase Overview table
- [ ] Tasks use checkbox format `- [ ]`
- [ ] Tasks have IDs (T001, T002, ...)
- [ ] Tasks have time estimates (Xh)
- [ ] Files specify size category (SMALL/MEDIUM/LARGE)

**If validation fails:**
- Stop and report parsing errors
- Example: "Cannot parse tasks.md: missing Phase Overview table"
- Request user to fix format

## 3. Filter Scope (Based on Parameters)

**Apply phase filter:**
- If `--phase 1`: Include only Phase 1
- If `--phase 1,2,3`: Include Phases 1, 2, 3
- If `--phase 1-3`: Include Phases 1 through 3
- If no `--phase`: Include all phases

**Apply task filter:**
- If `--tasks T001`: Include only T001
- If `--tasks T001,T002,T003`: Include T001, T002, T003
- If `--tasks T001-T010`: Include T001 through T010
- If no `--tasks`: Include all tasks (within selected phases)

**Validate ranges:**
- Check phase numbers exist in tasks.md
- Check task IDs exist in tasks.md
- If invalid: Stop and report error
- Example: "Invalid range: --phase 1-10 (only 5 phases exist)"

**Result:**
- FILTERED_PHASES: List of phases to include
- FILTERED_TASKS: List of tasks to include
- TOTAL_FILTERED_HOURS: Sum of hours for filtered tasks

## 4. Scan Supporting Files

**Detect in TASKS_DIR and subdirectories:**
- openapi.yaml / api-spec.yaml
- data-model.md
- README.md
- research.md
- test-plan.md
- architecture.md
- security-requirements.md
- performance-requirements.md
- Other relevant files

**Read content for context integration**

**If referenced file not found:**
- Log warning: "Referenced openapi.yaml not found in TASKS_DIR"
- Continue with note in prompt about missing file

## 5. Generate Prompt Header

```markdown
# Implementation Prompt: [Project Name]

**Generated:** YYYY-MM-DD HH:mm:ss
**Author:** SmartSpec Architect v5.0
**Source Tasks:** [Path to tasks.md]
**Source SPEC:** [SPEC-ID] v[X.Y.Z]
**SPEC_INDEX:** [Path used or "Not found"]
**Platform:** [Kilo Code / Claude Code / Roo Code]

---

## Project Overview

**Status:** IMPLEMENTATION
**Total Phases:** X (Filtered: Y phases)
**Total Tasks:** XX (Filtered: YY tasks)
**Estimated Effort:** XX hours (Filtered: YY hours)
**Technology Stack:** [From tasks.md frontmatter or metadata]

**Scope:**
- **Phases:** [List of included phases, e.g., "1, 2, 3" or "All"]
- **Tasks:** [List of included tasks, e.g., "T001-T010" or "All"]
- **Reason:** [User-specified filter or "Full implementation"]

**Supporting Documentation:**
- 📄 SPEC: [Link to spec.md]
- 📋 Tasks: [Link to tasks.md]
- 🔌 API Spec: [Link to openapi.yaml if exists, else "Not found"]
- 📊 Data Model: [Link to data-model.md if exists, else "Not found"]
- 📖 README: [Link to README.md if exists, else "Not found"]
- 🔬 Research: [Link to research.md if exists]
- 🏗️ Architecture: [Link to architecture.md if exists]

**Related Specs:** (Resolved from SPEC_INDEX)
[For each referenced spec:]
- **[spec-id]** (`[path]`, repo: [repo]) - [Title]

[If SPEC_INDEX not found:]
- ⚠️ SPEC_INDEX not found, dependency resolution skipped

---
```

## 6. Platform-Specific Instructions

**Based on detected platform flag:**

### For --kilocode

```markdown
## 🤖 KILO CODE PLATFORM INSTRUCTIONS

**Auto Subtasks:** ENABLED
- Tasks >8h will automatically break into subtasks
- No manual intervention needed
- Subtask format: T001.1, T001.2, etc.

**Mode Switching:** AUTOMATIC
Kilo Code will automatically switch between modes based on task type:

| Mode | Purpose | When Used | LLM |
|------|---------|-----------|-----|
| **Architect** | Design decisions, architecture planning | Design tasks, system planning | Optimized for architecture |
| **Code** | Implementation, file editing, coding | Most implementation tasks | Optimized for code generation |
| **Debug** | Error fixing, troubleshooting | When validation fails, errors occur | Optimized for debugging |
| **Ask** | Clarification, user input needed | Ambiguous requirements, decisions | Optimized for Q&A |
| **Orchestrator** | Coordinating multiple tasks, workflow | Complex multi-step operations | Optimized for coordination |

**Mode Selection Examples:**
```
T001: Design database schema → Architect Mode
T002: Create entity models → Code Mode
T003: Fix migration error → Debug Mode
T004: Clarify business rule → Ask Mode
T005: Coordinate API + DB tasks → Orchestrator Mode
```

**LLM Selection:** AUTOMATIC
- Each mode uses a different LLM optimized for that specific task type
- No manual configuration needed
- Kilo Code handles LLM selection transparently

**Execution Pattern:**
1. Kilo Code reads full prompt
2. Analyzes each task
3. Selects appropriate mode automatically
4. Switches LLM as needed
5. Executes with optimal configuration

**Validation:**
- Automatic after each task
- Uses validation commands from tasks.md
- Retries on failure (max 2 attempts)

**Checkpoints:**
- Automatic every 5 tasks
- Manual checkpoint on user request
- Auto-save on context limit

---
```

### For --claude

```markdown
## 🤖 CLAUDE CODE PLATFORM INSTRUCTIONS

**Sub Agents:** AVAILABLE
You can create specialized agents for different concerns:

**Recommended Agent Structure:**
```
1. DB Agent → Handle all database-related tasks
2. API Agent → Handle all API endpoint tasks
3. Test Agent → Handle all testing tasks
4. Integration Agent → Handle integration and coordination
```

**Creating Sub Agents:**
```typescript
// Example: Create DB Agent
"Create a sub agent specialized in database operations.
Focus: PostgreSQL, migrations, entity models, queries.
Responsibilities: T001-T010 (database tasks)"

// Example: Create API Agent
"Create a sub agent specialized in API development.
Focus: Express.js, endpoints, validation, error handling.
Responsibilities: T011-T025 (API tasks)"
```

**Execution:** INTERACTIVE
- Manual task selection
- User-driven validation
- Flexible checkpoint timing
- More control, requires more oversight

**Mode Control:** MANUAL
- You decide when to switch approaches
- Can pause and resume anytime
- More flexibility in execution order

**Validation:**
- Run validation commands manually after each task
- Check output and decide whether to continue
- Fix errors before proceeding

**Checkpoints:**
- Create checkpoints manually at logical points
- Recommended: After each phase
- Can checkpoint anytime for safety

**Workflow Example:**
```
1. Read full prompt
2. Create specialized sub agents (optional)
3. Start with Phase 1, Task T001
4. Implement task
5. Run validation commands manually
6. If pass: Continue to T002
7. If fail: Debug and fix
8. Checkpoint after Phase 1 complete
9. Continue to Phase 2
```

---
```

### For --roocode

```markdown
## 🤖 ROO CODE PLATFORM INSTRUCTIONS

(To be documented based on Roo Code capabilities)

**Execution Pattern:**
- Follow similar incremental approach
- One task at a time
- Validate after each task
- Stop at checkpoints

**Validation:**
- Use validation commands from tasks.md
- Verify after each task completion

**Checkpoints:**
- Create checkpoints at phase boundaries
- Save progress regularly

---
```

## 7. Critical Execution Constraints

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
# Use commands from tasks.md frontmatter
{validation_commands.compile}
{validation_commands.test}
{validation_commands.lint}
```

**Default (if no frontmatter):**
```bash
# TypeScript projects
tsc --noEmit

# Tests (if exist)
npm test -- [relevant-test-file]

# Linting (critical only)
npm run lint
```

**For other languages:**
```bash
# Python
python -m py_compile {file}
pytest {test_file}
flake8 {file}

# Go
go build ./...
go test {package}
golangci-lint run

# Rust
cargo check
cargo test {test_name}
cargo clippy
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

## 8. Progressive Execution Guide

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
   {validation_commands.compile}
   {validation_commands.test}
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
{validation_commands.compile}

# All tests
{validation_commands.test}

# Linting
{validation_commands.lint}

# Integration check (if defined)
{validation_commands.integration}
```

**If ALL pass:**
- Generate checkpoint report
- Get user confirmation (if interactive)
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

## 9. Error Recovery Procedures

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
$ {validation_commands.compile}
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

### Missing Dependencies

**If task depends on incomplete task:**
1. Check dependency status
2. If dependency not complete: **SKIP task**
3. Log: "Skipped T0XX: depends on incomplete T0YY"
4. Continue to next task
5. Return to skipped tasks later

**If spec dependency not implemented:**
1. Check SPEC_INDEX for dependency info
2. If dependency spec not implemented: **SKIP task**
3. Log: "Skipped T0XX: depends on unimplemented spec-YYY"
4. Continue to next task
5. Note in final report

---
```

## 10. Phase & Task Details

For each phase in FILTERED_PHASES:

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
{validation_commands.compile}
{validation_commands.test}
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
- [ ] Compilation passes
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

## 11. Safety Checklist

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

## 12. Write Prompt File

Determine output path:
- Pattern: `implement-prompt-<spec-id>-<timestamp>.md`
- Location: TASKS_DIR/
- If exists: Add timestamp suffix

Write complete prompt to file with all sections:
1. Header with project overview
2. Platform-specific instructions
3. Critical execution constraints
4. Progressive execution guide
5. Error recovery procedures
6. Phase & task details (filtered)
7. Safety checklist

## 13. Report (Thai)

```
✅ สร้าง Implementation Prompt เรียบร้อยแล้ว

📁 ไฟล์: [Path to implement-prompt-<spec-id>-<timestamp>.md]
🎯 Platform: [Kilo Code / Claude Code / Roo Code]

📊 Structure:
- Phases: X (Filtered: Y phases - [list])
- Tasks: XX (Filtered: YY tasks - [range])
- Hours: ZZ estimated (Filtered: WW hours)

🔧 Technology Stack: [From tasks.md]

🔒 Safety Features:
- File size strategies: ✅
- Error recovery: ✅
- Checkpoints: X points
- Validation: After every task

📄 Supporting Files Integrated:
- openapi.yaml: [✅ Found / ⚠️ Not found]
- data-model.md: [✅ Found / ⚠️ Not found]
- README.md: [✅ Found / ⚠️ Not found]
- [Other files if any]

🔗 Spec References Resolved: X specs
[If SPEC_INDEX not found: ⚠️ SPEC_INDEX not found, dependency resolution skipped]

✅ Validation Commands:
- Compile: {validation_commands.compile}
- Test: {validation_commands.test}
- Lint: {validation_commands.lint}
[If from frontmatter: ✅ From tasks.md frontmatter]
[If default: ⚠️ Using TypeScript defaults (no frontmatter found)]

💡 วิธีใช้:

**สำหรับ Kilo Code:**
```bash
kilo code implement implement-prompt-<spec-id>-<timestamp>.md
```
- Auto subtasks: ✅ Enabled
- Mode switching: ✅ Automatic
- LLM selection: ✅ Automatic

**สำหรับ Claude Code:**
1. เปิด Claude Code
2. Load prompt file
3. (Optional) Create sub agents for specialized tasks
4. Execute ทีละ task
5. Follow checkpoint pattern
- Sub agents: ✅ Available
- Execution: Interactive
- Mode control: Manual

**สำหรับ Roo Code:**
1. เปิด Roo Code
2. Load prompt file
3. Execute ทีละ task
4. Follow checkpoint pattern

⚠️ Important:
- Execute ONE task at a time
- Validate after EACH task
- Stop at checkpoints
- Use supporting files
- Follow platform-specific instructions

🔄 ต่อไป:
1. Review prompt
2. Prepare environment
3. Start Phase 1, Task T001
4. Execute incrementally

---

**Note:** This prompt generator creates implementation instructions only.
For auto-implementation, use: /smartspec_implement_tasks.md
```

---

Context: $ARGUMENTS
