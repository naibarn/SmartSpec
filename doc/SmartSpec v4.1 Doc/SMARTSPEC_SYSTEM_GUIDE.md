# SmartSpec v4.0 Complete System Guide

**Version:** 4.0.0
**Updated:** December 3, 2025
**Purpose:** Comprehensive guide to the SmartSpec workflow ecosystem

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Workflow Catalog](#workflow-catalog)
3. [Integration Patterns](#integration-patterns)
4. [Best Practices](#best-practices)
5. [Troubleshooting](#troubleshooting)

---

## System Overview

### What is SmartSpec?

SmartSpec is a comprehensive system for managing software specifications, project planning, and implementation workflows. It provides:

**Core Capabilities:**
- ✅ **Specification Management** - Create and maintain technical specs
- ✅ **Project Planning** - Generate roadmaps and milestones
- ✅ **Task Generation** - Break specs into implementable tasks
- ✅ **Implementation Prompts** - Ready-to-use prompts for Kilo Code/Claude Code
- ✅ **Progress Tracking** - Monitor implementation status
- ✅ **Synchronization** - Keep specs and tasks aligned

### System Architecture

```
┌─────────────────────────────────────────────────┐
│                   SmartSpec v4.0                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐     ┌──────────────┐        │
│  │ Specification │────▶│   Planning   │        │
│  │  Generation   │     │  Generation  │        │
│  └──────────────┘     └──────────────┘        │
│         │                    │                  │
│         ▼                    ▼                  │
│  ┌──────────────┐     ┌──────────────┐        │
│  │     Task     │────▶│ Kilo Prompt  │        │
│  │  Generation  │     │  Generation  │        │
│  └──────────────┘     └──────────────┘        │
│         │                    │                  │
│         ▼                    ▼                  │
│  ┌──────────────┐     ┌──────────────┐        │
│  │   Progress   │     │  Spec/Task   │        │
│  │   Tracking   │     │     Sync     │        │
│  └──────────────┘     └──────────────┘        │
│                                                 │
└─────────────────────────────────────────────────┘
         │                                │
         ▼                                ▼
  ┌─────────────┐                 ┌─────────────┐
  │  Kilo Code  │                 │ Claude Code │
  │   Executor  │                 │   Executor  │
  └─────────────┘                 └─────────────┘
```

### Key Components

**1. Knowledge Base (`.smartspec/`)**
- `system_prompt.md` - Core behavior and rules
- `Knowledge-Base.md` - Patterns and best practices
- `constitution.md` - Non-negotiable constraints
- `kilocode-context.md` - Execution guidelines
- `SPEC_INDEX.json` - Registry of all specs

**2. Workflows (6 workflows)**
- Specification generation
- Project planning
- Task generation
- Kilo prompt generation
- Progress verification
- Spec/task synchronization

**3. Supporting Files**
- `openapi.yaml` - API specifications
- `data-model.md` - Data schemas
- `README.md` - Implementation guides
- `test-plan.md` - Testing strategies

---

## Workflow Catalog

### 1. smartspec_generate_spec_v4

**Purpose:** Create or update technical specifications

**Use Cases:**
- Creating new SPEC from requirements
- Updating existing SPEC with enhancements
- Preserving critical sections during updates
- Resolving spec references

**Features:**
- ✅ Critical section preservation (STRIDE, configs, DI patterns)
- ✅ Spec reference resolution with paths + repos
- ✅ Author tracking with version
- ✅ Dry-run mode (--nogenerate)
- ✅ Custom SPEC_INDEX support (--specindex)

**Usage:**
```bash
# NEW spec
"Create SPEC for payment system with Stripe integration..."

# EDIT spec
specs/feature/spec-004-financial/spec.md

# With flags
specs/feature/spec-004/spec.md --specindex="path" --nogenerate
```

**Outputs:**
- `spec.md` (or spec.backup-*.md for edits)
- Includes: Header, Overview, Architecture, Implementation, Examples, Critical Sections

---

### 2. smartspec_generate_plan

**Purpose:** Generate project roadmap and planning documents

**Use Cases:**
- Creating project timeline
- Resource allocation planning
- Risk assessment
- Milestone tracking

**Features:**
- ✅ Milestone generation with dates
- ✅ Phase breakdown with durations
- ✅ Resource requirements
- ✅ Risk assessment
- ✅ Dependency tracking
- ✅ Quality gates

**Usage:**
```bash
# Generate plan from spec
specs/feature/spec-004/spec.md

# Custom output name
specs/feature/spec-004/spec.md --output=roadmap.md

# Dry run
specs/feature/spec-004/spec.md --nogenerate
```

**Outputs:**
- `plan.md` (or custom name)
- Includes: Milestones, phases, resources, risks, timeline, quality gates

---

### 3. smartspec_generate_tasks_v4

**Purpose:** Generate implementation tasks from specifications

**Use Cases:**
- Breaking spec into implementable chunks
- Creating phase-based task structure
- Auto-generating supporting files
- Setting up implementation workflow

**Features:**
- ✅ Auto-detection of supporting files
- ✅ Auto-generation of missing files (README, data-model, openapi.yaml)
- ✅ Phase planning (10-task maximum per phase)
- ✅ File-size-aware strategies
- ✅ Checkpoint insertion
- ✅ Spec reference resolution

**Usage:**
```bash
# Generate tasks
specs/feature/spec-004/spec.md

# With custom SPEC_INDEX
specs/feature/spec-004/spec.md --specindex="custom/index.json"

# Dry run (see plan without creating)
specs/feature/spec-004/spec.md --nogenerate
```

**Outputs:**
- `tasks.md` - Complete task breakdown
- `README.md` - Implementation guide (if missing)
- `data-model.md` - Data schemas (if needed)
- `openapi.yaml` - API spec (if needed)
- `test-plan.md` - Testing strategy (if needed)

---

### 4. smartspec_generate_kilo_prompt_v4

**Purpose:** Create implementation prompts for Kilo Code/Claude Code

**Use Cases:**
- Preparing for implementation
- Setting up safety constraints
- Integrating supporting files
- Creating executable prompts

**Features:**
- ✅ Kilo Code + Claude Code compatibility
- ✅ Safety constraints built-in
- ✅ Error recovery procedures
- ✅ Supporting files integration
- ✅ Context management guidelines
- ✅ File-size strategies

**Usage:**
```bash
# Generate prompt from tasks
specs/feature/spec-004/tasks.md

# With custom SPEC_INDEX
specs/feature/spec-004/tasks.md --specindex="path"
```

**Outputs:**
- `kilo-prompt.md` (or timestamped if exists)
- Ready to use with Kilo Code or Claude Code
- Includes: Constraints, execution guide, phases, tasks, checkpoints

---

### 5. smartspec_verify_tasks_progress

**Purpose:** Track implementation progress and mark completed tasks

**Use Cases:**
- Checking what's been implemented
- Marking tasks as complete
- Identifying blockers
- Generating progress reports

**Features:**
- ✅ File existence checking
- ✅ Implementation verification
- ✅ Automatic task marking (✅/🟦/⬜/❌)
- ✅ Progress percentage calculation
- ✅ Blocker identification

**Usage:**
```bash
# Verify progress
specs/feature/spec-004/tasks.md

# With detailed report
specs/feature/spec-004/tasks.md --detailed
```

**Outputs:**
- Updated `tasks.md` with status markers
- Progress report
- Blocker list
- Completion percentage

---

### 6. smartspec_sync_spec_tasks

**Purpose:** Keep spec.md and tasks.md synchronized

**Use Cases:**
- After updating SPEC
- Detecting outdated tasks
- Ensuring consistency
- Auto-updating tasks

**Features:**
- ✅ Spec vs tasks comparison
- ✅ Inconsistency detection
- ✅ Auto-update tasks.md
- ✅ Change reporting
- ✅ Validation

**Usage:**
```bash
# Sync check and update
specs/feature/spec-004/spec.md specs/feature/spec-004/tasks.md

# Check only (no update)
specs/feature/spec-004/spec.md specs/feature/spec-004/tasks.md --check-only
```

**Outputs:**
- Updated `tasks.md` (if needed)
- Sync report
- List of changes
- Inconsistencies found

---

## Integration Patterns

### Pattern 1: Complete New Project

**Workflow:**
```
1. Generate SPEC
   ↓
2. Generate Plan (optional)
   ↓
3. Generate Tasks
   ↓
4. Generate Kilo Prompt
   ↓
5. Implement (Kilo/Claude Code)
   ↓
6. Verify Progress
```

**Commands:**
```bash
# Step 1: Create SPEC
"Create SPEC for e-commerce cart system with Redis caching..."

# Step 2: Generate plan (optional)
specs/feature/spec-005-cart/spec.md

# Step 3: Generate tasks
specs/feature/spec-005-cart/spec.md

# Step 4: Generate prompt
specs/feature/spec-005-cart/tasks.md

# Step 5: Implement
kilo code implement specs/feature/spec-005-cart/kilo-prompt.md

# Step 6: Track progress
specs/feature/spec-005-cart/tasks.md
```

---

### Pattern 2: Update Existing Project

**Workflow:**
```
1. Update SPEC (with preservation)
   ↓
2. Sync Tasks (auto-update)
   ↓
3. Regenerate Kilo Prompt
   ↓
4. Continue Implementation
   ↓
5. Verify Progress
```

**Commands:**
```bash
# Step 1: Update SPEC
specs/feature/spec-004/spec.md

# Step 2: Sync tasks
specs/feature/spec-004/spec.md specs/feature/spec-004/tasks.md

# Step 3: Regenerate prompt
specs/feature/spec-004/tasks.md

# Step 4: Continue implementation
kilo code implement specs/feature/spec-004/kilo-prompt-YYYYMMDD.md

# Step 5: Track progress
specs/feature/spec-004/tasks.md
```

---

### Pattern 3: Dry-Run Validation

**Workflow:**
```
1. Dry-run SPEC generation
   ↓
2. Review plan
   ↓
3. Dry-run tasks generation
   ↓
4. Review task structure
   ↓
5. Generate actual files
```

**Commands:**
```bash
# Step 1: Dry-run SPEC
"Create payment SPEC..." --nogenerate

# Step 2: Review output, adjust requirements

# Step 3: Dry-run tasks
specs/feature/spec-006-payment/spec.md --nogenerate

# Step 4: Review task structure

# Step 5: Generate for real
specs/feature/spec-006-payment/spec.md
```

---

## Best Practices

### Specification Management

**DO:**
- ✅ Use --nogenerate for review before creating
- ✅ Include comprehensive examples
- ✅ Define Non-Goals explicitly
- ✅ Reference related specs
- ✅ Include security considerations
- ✅ Add configuration schemas
- ✅ Document DI patterns

**DON'T:**
- ❌ Skip critical sections
- ❌ Leave spec references unresolved
- ❌ Forget to update author field
- ❌ Ignore Non-Goals section
- ❌ Skip validation steps

---

### Task Generation

**DO:**
- ✅ Review auto-generated supporting files
- ✅ Verify file-size strategies
- ✅ Check phase boundaries (10-task max)
- ✅ Ensure checkpoint presence
- ✅ Validate dependencies
- ✅ Use specific acceptance criteria

**DON'T:**
- ❌ Ignore supporting files
- ❌ Skip checkpoints
- ❌ Create phases > 10 tasks
- ❌ Use vague acceptance criteria
- ❌ Forget validation commands

---

### Implementation

**DO:**
- ✅ Execute one task at a time
- ✅ Validate after each task
- ✅ Stop at checkpoints
- ✅ Reference supporting files
- ✅ Follow file-size strategies
- ✅ Report progress regularly

**DON'T:**
- ❌ Rush through multiple tasks
- ❌ Skip validation
- ❌ Ignore checkpoints
- ❌ Forget supporting files
- ❌ Exceed str_replace limits
- ❌ Continue after 3 errors

---

### Progress Tracking

**DO:**
- ✅ Run verification regularly
- ✅ Mark tasks as complete
- ✅ Track blockers
- ✅ Update status in tasks.md
- ✅ Generate progress reports

**DON'T:**
- ❌ Forget to update tasks.md
- ❌ Ignore blockers
- ❌ Skip progress reports
- ❌ Let tasks.md get stale

---

### Synchronization

**DO:**
- ✅ Sync after SPEC updates
- ✅ Review changes before applying
- ✅ Keep tasks aligned with spec
- ✅ Document why changes needed

**DON'T:**
- ❌ Let spec and tasks diverge
- ❌ Auto-update without review
- ❌ Ignore inconsistencies
- ❌ Skip validation

---

## Troubleshooting

### SPEC Generation Issues

**Problem:** Critical sections missing after EDIT
**Solution:** Check CRITICAL_REGISTRY, ensure preservation rules followed

**Problem:** Spec references not resolved
**Solution:** Verify SPEC_INDEX loaded, check spec IDs exist in index

**Problem:** Author field not updated
**Solution:** Check workflow completed step 5, verify v4.0 author

---

### Task Generation Issues

**Problem:** Supporting files not detected
**Solution:** Check file naming patterns, ensure files in SPEC_DIR

**Problem:** Auto-generation not working
**Solution:** Verify SPEC has required indicators (API endpoints, schemas)

**Problem:** Phases > 10 tasks
**Solution:** Review phase planning logic, may need manual adjustment

---

### Kilo Prompt Issues

**Problem:** Supporting files not integrated
**Solution:** Check tasks.md references, ensure files detected

**Problem:** Constraints not appearing
**Solution:** Verify workflow step 5 completed, check constraint template

**Problem:** Spec references missing paths
**Solution:** Ensure SPEC_INDEX loaded, check resolution logic

---

### Progress Tracking Issues

**Problem:** Tasks not being marked
**Solution:** Check file existence, verify task ID matching

**Problem:** Progress percentage wrong
**Solution:** Review task completion criteria, recount manually

**Problem:** Blockers not detected
**Solution:** Check blocker detection logic, may need manual entry

---

### Synchronization Issues

**Problem:** Changes not detected
**Solution:** Compare spec vs tasks manually, check diff logic

**Problem:** Auto-update breaking tasks
**Solution:** Use --check-only first, review changes before applying

**Problem:** False positives
**Solution:** Refine comparison logic, may need threshold adjustment

---

## Version History

**v4.0.0 (Current)**
- Complete workflow system
- Full supporting files integration
- Comprehensive safety features
- Kilo + Claude Code compatibility

**v3.5.0**
- Critical section preservation
- Spec reference resolution
- Enhanced validation

**v3.0.0**
- Auto-replace with backup
- Custom SPEC_INDEX support
- Dry-run mode

**v2.1.0**
- Basic SPEC generation
- Task breakdown
- Simple prompts

---

## Additional Resources

- **Knowledge Base:** `.smartspec/Knowledge-Base.md`
- **System Prompt:** `.smartspec/system_prompt.md`
- **Constitution:** `.smartspec/constitution.md`
- **Kilo Context:** `.smartspec/kilocode-context.md`
- **SPEC Index:** `.smartspec/SPEC_INDEX.json`

---

**For questions or issues:** Refer to individual workflow documentation or contact SmartSpec maintainers.
