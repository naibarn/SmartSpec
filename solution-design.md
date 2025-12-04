# Solution Design: Implement Prompt & Tasks Workflow Improvement

## 📋 สรุปปัญหาที่พบ

### 1. ชื่อและขอบเขตของ Workflow
- ❌ ชื่อ "kilo-prompt" ไม่เป็นกลาง ผูกติดกับ Kilo Code
- ❌ ไม่รองรับหลาย platform (Claude, Roo Code)
- ✅ **Solution:** เปลี่ยนเป็น "implement-prompt" และรองรับหลาย platform

### 2. Parameters ที่ขาดหายไป
- ❌ ไม่มี `--phase` สำหรับเลือก phase ที่ต้องการ
- ❌ ไม่มี `--tasks` สำหรับเลือก tasks เฉพาะ
- ❌ ไม่มี platform selector (`--kilocode`, `--claude`, `--roocode`)
- ✅ **Solution:** เพิ่ม parameters ทั้งหมดพร้อม default behavior

### 3. Format ของ tasks.md ไม่ชัดเจน
- ❌ ไม่มีข้อตกลงร่วมระหว่าง generate_tasks และ generate_implement_prompt
- ❌ Parser อาจพังถ้า format เปลี่ยน
- ✅ **Solution:** กำหนด standard format และ validation rules

### 4. Validation Commands ไม่ยืดหยุ่น
- ❌ Hardcode `tsc --noEmit`, `npm test` (TypeScript only)
- ❌ ไม่รองรับภาษาอื่น (Python, Go, Rust, etc.)
- ✅ **Solution:** อ่าน validation commands จาก tasks.md metadata หรือ spec

### 5. ขาด Workflow สำหรับ Auto Implementation
- ❌ ไม่มี `/smartspec_implement_tasks` สำหรับ run auto
- ❌ ไม่มีระบบติดตาม progress และ resume
- ✅ **Solution:** สร้าง workflow ใหม่สำหรับ auto implement

### 6. Platform-Specific Features ไม่ชัดเจน
- ❌ Kilo Code vs Claude Code แยกไม่ชัด
- ❌ ไม่ได้ใช้ features เฉพาะของแต่ละ platform
- ✅ **Solution:** แยก instruction และใช้ features เต็มที่

### 7. Safety Constraints วางผิดที่
- ❌ Safety rules อยู่ใน prompt generation workflow
- ❌ ควรอยู่ใน implementation workflow
- ✅ **Solution:** แยก concerns ให้ชัดเจน

---

## 🎯 Solution Overview

### Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SmartSpec V5 Workflows                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. /smartspec_generate_spec.md                              │
│     └─> specs/*/spec.md                                      │
│                                                               │
│  2. /smartspec_generate_plan.md                              │
│     └─> specs/*/plan.md                                      │
│                                                               │
│  3. /smartspec_generate_tasks.md                             │
│     └─> specs/*/tasks.md (STANDARD FORMAT)                   │
│                                                               │
│  4. /smartspec_generate_implement_prompt.md (NEW NAME)       │
│     ├─> Input: tasks.md                                      │
│     ├─> Parameters: --phase, --tasks, --platform            │
│     └─> Output: implement-prompt-<spec-id>.md                │
│                                                               │
│  5. /smartspec_implement_tasks.md (NEW WORKFLOW)             │
│     ├─> Input: tasks.md OR implement-prompt.md              │
│     ├─> Parameters: --phase, --tasks, --resume, --validate  │
│     └─> Action: Auto implement with safety constraints       │
│                                                               │
│  6. /smartspec_sync_spec_tasks.md                            │
│  7. /smartspec_verify_tasks_progress.md                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📐 Detailed Solutions

### Solution 1: Rename & Restructure Generate Implement Prompt

**ไฟล์เดิม:** `smartspec_generate_kilo_prompt.md`
**ไฟล์ใหม่:** `smartspec_generate_implement_prompt.md`

**Parameters ใหม่:**

```bash
# Basic usage (default: Claude, all phases, all tasks)
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md

# Select specific phases
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --phase 1
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --phase 1,2,3
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --phase 1-3

# Select specific tasks
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --tasks T001
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --tasks T001,T002,T003
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --tasks T001-T010

# Select platform
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --kilocode
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --claude
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --roocode

# Combine parameters
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --phase 1-2 --tasks T001-T010 --kilocode

# With SPEC_INDEX
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md --specindex=".smartspec/SPEC_INDEX.json"
```

**Default Behavior:**
- Platform: `--claude` (most popular)
- Phase: all phases
- Tasks: all tasks
- SPEC_INDEX: auto-detect `.smartspec/SPEC_INDEX.json` if exists

**Output Filename:**
- Pattern: `implement-prompt-<spec-id>-<timestamp>.md`
- Example: `implement-prompt-spec-004-20250104-143022.md`

---

### Solution 2: Standard tasks.md Format

**กำหนด format ที่ชัดเจนสำหรับ tasks.md:**

```markdown
---
spec_id: spec-004-financial-system
version: 1.0.0
technology_stack: TypeScript, Node.js, PostgreSQL
validation_commands:
  compile: "tsc --noEmit"
  test: "npm test"
  lint: "npm run lint"
  integration: "npm run test:integration"
---

# Tasks: [Project Name]

## Project Metadata
- **SPEC ID:** spec-004-financial-system
- **Version:** 1.0.0
- **Technology Stack:** TypeScript, Node.js, PostgreSQL, Redis
- **Total Phases:** 5
- **Total Tasks:** 45
- **Estimated Effort:** 180 hours

## Phase Overview

| Phase | Name | Tasks | Hours | Risk | Dependencies |
|-------|------|-------|-------|------|--------------|
| 1 | Foundation | T001-T010 | 40h | MEDIUM | None |
| 2 | Core Features | T011-T025 | 60h | HIGH | Phase 1 |
...

## Phase 1: Foundation (T001-T010)

### Task T001: Setup project structure (4h)
- [ ] T001: Setup project structure (4h)

**Description:**
...

**Files:**
- CREATE: `src/index.ts` (~50 lines - SMALL)
- CREATE: `package.json` (~30 lines - SMALL)
...
```

**Validation Rules:**
1. ต้องมี YAML frontmatter พร้อม `validation_commands`
2. ต้องมี Project Metadata section
3. ต้องมี Phase Overview table
4. Tasks ต้องมี checkbox format `- [ ]`
5. Tasks ต้องมี ID (T001, T002, ...)
6. Tasks ต้องมี time estimate (Xh)
7. Files ต้องระบุ size category (SMALL/MEDIUM/LARGE)

---

### Solution 3: Flexible Validation Commands

**อ่านจาก tasks.md frontmatter:**

```yaml
---
validation_commands:
  # TypeScript/Node.js
  compile: "tsc --noEmit"
  test: "npm test -- {test_file}"
  lint: "npm run lint"
  
  # Python
  # compile: "python -m py_compile {file}"
  # test: "pytest {test_file}"
  # lint: "flake8 {file}"
  
  # Go
  # compile: "go build ./..."
  # test: "go test {package}"
  # lint: "golangci-lint run"
  
  # Rust
  # compile: "cargo check"
  # test: "cargo test {test_name}"
  # lint: "cargo clippy"
---
```

**ใน implement prompt จะใช้:**

```markdown
**Validation (After EACH task):**
```bash
# Compilation check
{validation_commands.compile}

# Run relevant tests
{validation_commands.test}

# Linting
{validation_commands.lint}
```

**If validation fails:**
- Fix immediately
- Do NOT proceed to next task
- Re-validate before continuing
```

---

### Solution 4: Platform-Specific Instructions

**Kilo Code Features:**
- ✅ Auto subtasks (รองรับอัตโนมัติ)
- ✅ Multiple modes: Architect, Code, Ask, Debug, Orchestrator
- ✅ Auto mode switching based on task type
- ✅ Multi-LLM support (different LLM per mode)

**Claude Code Features:**
- ✅ Sub agents (สร้าง agents ย่อย)
- ✅ Interactive execution
- ✅ Manual mode control
- ✅ Context management by user

**Roo Code Features:**
- ✅ (ต้องวิจัยเพิ่มเติม)

**Implementation:**

```markdown
## 🤖 PLATFORM-SPECIFIC INSTRUCTIONS

### For Kilo Code

**Auto Subtasks:** ENABLED
- Tasks >8h will auto-break into subtasks
- No manual intervention needed

**Mode Switching:** AUTOMATIC
- **Architect Mode:** For design decisions, architecture planning
- **Code Mode:** For implementation, file editing
- **Debug Mode:** For error fixing, troubleshooting
- **Ask Mode:** For clarification, user input needed
- **Orchestrator Mode:** For coordinating multiple tasks

**Example Task Execution:**
```
T001: Design database schema (Architect Mode)
T002: Create entity models (Code Mode)
T003: Fix migration error (Debug Mode)
T004: Clarify business rule (Ask Mode)
T005: Coordinate API + DB tasks (Orchestrator Mode)
```

**LLM Selection:** Automatic per mode
- Each mode may use different LLM optimized for that task
- No manual configuration needed

---

### For Claude Code

**Sub Agents:** AVAILABLE
- Create specialized agents for different concerns
- Example: DB Agent, API Agent, Test Agent

**Execution:** INTERACTIVE
- Manual task selection
- User-driven validation
- Flexible checkpoint timing

**Mode Control:** MANUAL
- User decides when to switch approaches
- More flexibility, requires more oversight

**Example Workflow:**
```
1. Create DB Agent → Handle all database tasks
2. Create API Agent → Handle all API endpoints
3. Create Test Agent → Handle all testing tasks
4. Coordinate between agents manually
```

---

### For Roo Code

(To be documented based on Roo Code capabilities)

---
```

---

### Solution 5: New Workflow - smartspec_implement_tasks.md

**Purpose:** Auto-implement tasks with safety constraints

**Parameters:**

```bash
# Basic usage (implement all uncompleted tasks)
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md

# Use existing implement prompt
/smartspec_implement_tasks.md specs/feature/spec-004/implement-prompt-spec-004.md

# Auto-detect from spec folder
/smartspec_implement_tasks.md specs/feature/spec-004

# Select specific phases
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --phase 1-2

# Select specific tasks
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --tasks T001-T010

# Resume from checkpoint
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --resume

# Skip completed tasks (default)
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --skip-completed

# Re-implement all (ignore checkboxes)
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --force-all

# Validate only (no implementation)
/smartspec_implement_tasks.md specs/feature/spec-004/tasks.md --validate-only
```

**Workflow Steps:**

1. **Load Context**
   - Read tasks.md or implement-prompt.md
   - Parse task completion status (checkboxes)
   - Load SPEC_INDEX if available
   - Read validation commands

2. **Determine Scope**
   - If `--skip-completed`: filter out checked tasks
   - If `--force-all`: ignore checkboxes
   - If `--phase X`: filter by phase
   - If `--tasks T001-T010`: filter by task range
   - If `--resume`: continue from last checkpoint

3. **Prepare Environment**
   - Validate project setup
   - Check dependencies installed
   - Verify supporting files exist

4. **Execute Tasks**
   - For each task in scope:
     - Read task description
     - Check dependencies completed
     - Implement according to instructions
     - Run validation commands
     - Update checkbox if successful
     - Create checkpoint every 5 tasks

5. **Safety Constraints** (Apply during execution)
   - ❌ Max 10 tasks per cycle
   - ❌ Max 5 file edits per task
   - ❌ Max 50 lines per str_replace
   - ❌ Stop at 3 consecutive errors
   - ✅ Validate after EVERY task
   - ✅ Checkpoint every 5 tasks
   - ✅ Report progress continuously

6. **Error Handling**
   - Validation fails → Fix and retry (max 2 times)
   - 3 consecutive errors → Stop and report
   - Context overflow → Checkpoint and pause
   - Missing dependency → Skip and report

7. **Progress Tracking**
   - Update checkboxes in tasks.md
   - Create checkpoint files
   - Generate progress report

8. **Final Report**
   - Tasks completed: X/Y
   - Tasks failed: Z
   - Validation status
   - Next steps

---

### Solution 6: Separation of Concerns

**Generate Implement Prompt Workflow:**
- ✅ Parse tasks.md
- ✅ Scan supporting files
- ✅ Resolve dependencies from SPEC_INDEX
- ✅ Generate platform-specific instructions
- ✅ Create comprehensive prompt document
- ❌ NO safety constraints (not executing yet)
- ❌ NO validation commands execution

**Implement Tasks Workflow:**
- ✅ Load implement prompt or tasks.md
- ✅ Apply safety constraints
- ✅ Execute validation commands
- ✅ Implement code changes
- ✅ Track progress
- ✅ Handle errors and recovery
- ❌ NO prompt generation (use existing)

---

## 📊 Implementation Priority

### Phase 1: Critical (Do First)
1. ✅ Rename workflow: `smartspec_generate_kilo_prompt.md` → `smartspec_generate_implement_prompt.md`
2. ✅ Add parameters: `--phase`, `--tasks`, `--platform`
3. ✅ Update output filename: `implement-prompt-<spec-id>.md`
4. ✅ Add platform detection and default to `--claude`

### Phase 2: Important (Do Next)
5. ✅ Define standard tasks.md format with validation rules
6. ✅ Add YAML frontmatter support for validation commands
7. ✅ Update generate_tasks workflow to output standard format
8. ✅ Add platform-specific instructions (Kilo Code vs Claude Code)

### Phase 3: Enhancement (Do After)
9. ✅ Create new workflow: `smartspec_implement_tasks.md`
10. ✅ Implement progress tracking with checkboxes
11. ✅ Add resume/checkpoint functionality
12. ✅ Add validation-only mode

### Phase 4: Documentation
13. ✅ Update README with new workflow names and parameters
14. ✅ Add examples for all parameter combinations
15. ✅ Document standard tasks.md format
16. ✅ Document platform-specific features

---

## 🔄 Migration Path

### For Existing Users

**Old Command:**
```bash
/smartspec_generate_kilo_prompt.md specs/feature/spec-004/tasks.md
```

**New Command (Backward Compatible):**
```bash
/smartspec_generate_implement_prompt.md specs/feature/spec-004/tasks.md
```

**Output Change:**
- Old: `kilo-prompt.md`
- New: `implement-prompt-spec-004-<timestamp>.md`

**Breaking Changes:**
- ❌ Workflow filename changed (need to update commands)
- ❌ Output filename changed (need to update references)
- ✅ Content format mostly compatible
- ✅ Can still use with Kilo Code and Claude Code

---

## ✅ Success Criteria

### For Generate Implement Prompt
- [ ] Workflow renamed to `smartspec_generate_implement_prompt.md`
- [ ] All parameters working: `--phase`, `--tasks`, `--platform`
- [ ] Default platform is Claude
- [ ] Output filename follows new pattern
- [ ] Platform-specific instructions included
- [ ] Validation commands read from tasks.md frontmatter
- [ ] SPEC_INDEX auto-detected from `.smartspec/`
- [ ] Supporting files scanned and integrated

### For Implement Tasks
- [ ] New workflow `smartspec_implement_tasks.md` created
- [ ] Can accept tasks.md or implement-prompt.md as input
- [ ] Progress tracking with checkbox updates
- [ ] Resume functionality working
- [ ] Safety constraints enforced
- [ ] Validation commands executed correctly
- [ ] Error handling and recovery working
- [ ] Progress reports generated

### For Documentation
- [ ] README updated with new workflow names
- [ ] All examples use correct syntax
- [ ] Standard tasks.md format documented
- [ ] Platform-specific features documented
- [ ] Migration guide provided

---

## 📝 Notes

### Edge Cases to Handle

1. **Missing SPEC_INDEX:**
   - Behavior: Continue without dependency resolution
   - Warning: "SPEC_INDEX not found, skipping dependency resolution"

2. **Invalid tasks.md format:**
   - Behavior: Stop and report parsing errors
   - Error: "Cannot parse tasks.md: missing Phase Overview table"

3. **Missing validation commands:**
   - Behavior: Use default TypeScript commands
   - Warning: "No validation_commands in frontmatter, using defaults"

4. **Missing supporting files:**
   - Behavior: Generate prompt with notes about missing files
   - Warning: "Referenced openapi.yaml not found"

5. **Platform not specified:**
   - Behavior: Default to Claude
   - Info: "No platform specified, using --claude"

6. **Invalid phase/task range:**
   - Behavior: Stop and report error
   - Error: "Invalid range: --phase 1-10 (only 5 phases exist)"

---

## 🎯 Next Steps

1. **Implement Phase 1** (Critical)
   - Rename workflow file
   - Add parameter parsing
   - Update output filename logic
   - Add platform detection

2. **Test Phase 1**
   - Test all parameter combinations
   - Verify output format
   - Check backward compatibility

3. **Implement Phase 2** (Important)
   - Define standard format
   - Add frontmatter support
   - Update generate_tasks workflow
   - Add platform instructions

4. **Implement Phase 3** (Enhancement)
   - Create implement_tasks workflow
   - Add progress tracking
   - Add resume functionality

5. **Update Documentation**
   - Update README
   - Add examples
   - Document formats

6. **Commit and Push**
   - Commit each phase separately
   - Write clear commit messages
   - Push to GitHub

---

**Document Version:** 1.0.0
**Created:** 2025-01-04
**Author:** SmartSpec Improvement Team
