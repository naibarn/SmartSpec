# SmartSpec v4.0 Complete Package - Manifest

**Package Version:** 4.0.0
**Generated:** December 3, 2025
**Total Files:** 14
**Total Size:** ~162KB

---

## Core Workflows (6 files)

### 1. smartspec_generate_spec_v4.md (16KB, 676 lines)
**Purpose:** Generate or update specifications with critical section preservation
**Features:**
- ✅ EDIT mode with critical section preservation
- ✅ NEW mode with auto-included critical sections
- ✅ Spec reference resolution (path + repo)
- ✅ Author tracking (SmartSpec v4.0)
- ✅ --nogenerate flag (dry run)
- ✅ --specindex support
**Usage:** `"Create SPEC for..." OR "specs/path/spec.md" [--flags]`

### 2. smartspec_generate_tasks_v4.md (27KB, 1113 lines)
**Purpose:** Generate implementation tasks with auto-generated supporting files
**Features:**
- ✅ Auto-detect existing supporting files
- ✅ Auto-generate missing files (README, data-model, openapi, test-plan)
- ✅ Phase planning (10-task max per phase)
- ✅ File-size-aware strategies (SMALL/MEDIUM/LARGE)
- ✅ Checkpoint insertion
- ✅ Spec reference resolution
- ✅ --nogenerate flag
- ✅ --specindex support
**Usage:** `"specs/path/spec.md" [--flags]`

### 3. smartspec_generate_kilo_prompt_v4.md (15KB, 725 lines)
**Purpose:** Create implementation prompts for Kilo Code/Claude Code
**Features:**
- ✅ Kilo Code + Claude Code compatibility
- ✅ Safety constraints built-in
- ✅ Error recovery procedures
- ✅ Supporting files integration
- ✅ Context management guidelines
- ✅ File-size strategies
- ✅ --specindex support
**Usage:** `"specs/path/tasks.md" [--flags]`

### 4. smartspec_generate_plan.md (4.3KB, 230 lines)
**Purpose:** Generate project roadmap and planning documents
**Features:**
- ✅ Milestone generation with dates
- ✅ Phase breakdown with durations
- ✅ Resource requirements
- ✅ Risk assessment
- ✅ Dependency tracking
- ✅ Quality gates
- ✅ --nogenerate flag
- ✅ --output flag (custom filename)
**Usage:** `"specs/path/spec.md" [--flags]`

### 5. smartspec_verify_tasks_progress.md (5.8KB, 269 lines)
**Purpose:** Track implementation progress and mark completed tasks
**Features:**
- ✅ File existence checking
- ✅ Implementation verification
- ✅ Automatic status marking (✅/🟦/⬜/❌)
- ✅ Progress percentage calculation
- ✅ Blocker identification
**Usage:** `"specs/path/tasks.md"`

### 6. smartspec_sync_spec_tasks.md (8.5KB, 350 lines)
**Purpose:** Synchronize spec.md and tasks.md
**Features:**
- ✅ Spec vs tasks comparison
- ✅ Inconsistency detection
- ✅ Auto-update tasks.md
- ✅ Change reporting
- ✅ --check-only flag
**Usage:** `"specs/path/spec.md" [--check-only]`

---

## Documentation & Guides (8 files)

### 7. SMARTSPEC_SYSTEM_GUIDE.md (15KB, 611 lines)
**Purpose:** Complete system overview and integration guide
**Contents:**
- System architecture
- Workflow catalog with detailed descriptions
- Integration patterns (3 common patterns)
- Best practices (DO/DON'T lists)
- Troubleshooting guide

### 8. WORKFLOW_DECISION_TREE.md (6.7KB)
**Purpose:** Decision flowchart for choosing workflows
**Contents:**
- When to use which workflow
- Decision criteria
- Common scenarios
- Quick reference chart

### 9. QUICK_START_GUIDE_TH.md (7.6KB)
**Purpose:** Thai language quick start guide
**Contents:**
- การเริ่มต้นใช้งาน
- Use cases พื้นฐาน
- ตัวอย่างการใช้งาน
- การแก้ไขปัญหา

### 10. SUPPORTING_FILES_GUIDE.md (11KB)
**Purpose:** Guide to supporting files system
**Contents:**
- What are supporting files
- Auto-detection patterns
- Auto-generation rules
- File templates
- Integration examples

### 11. SPEC_INDEX_GUIDE.md (11KB)
**Purpose:** SPEC_INDEX format and usage
**Contents:**
- JSON structure
- How to create/maintain
- Resolution mechanism
- Best practices
- Examples

### 12. TESTING_WORKFLOWS_GUIDE.md (11KB)
**Purpose:** How to test each workflow
**Contents:**
- Test scenarios per workflow
- Expected outputs
- Validation criteria
- Edge cases
- Troubleshooting

### 13. COMPLETE_EXAMPLE.md (17KB)
**Purpose:** End-to-end project walkthrough
**Contents:**
- Full project from start to finish
- spec.md → plan.md → tasks.md → kilo-prompt.md → implementation → verification
- Real-world example with actual commands
- Expected outputs at each step

### 14. PACKAGE_README.md (7.7KB)
**Purpose:** Package overview and navigation
**Contents:**
- Quick overview
- File descriptions
- Getting started
- Where to find what
- Version information

---

## Key Features by Version

### v4.0.0 (Current - December 2025)
**Major Features:**
- ✅ Complete workflow ecosystem (6 workflows)
- ✅ Supporting files auto-detection & generation
- ✅ Kilo Code + Claude Code compatibility
- ✅ Comprehensive safety features
- ✅ Full SPEC_INDEX integration
- ✅ Dry-run mode for all generation workflows
- ✅ Progress tracking & synchronization
- ✅ Critical section preservation (from v3)
- ✅ Spec reference resolution (from v3)

### v3.5.0 (November 2025)
- Critical section preservation
- Spec reference resolution with paths + repos
- Author field with version tracking
- Enhanced validation

### v3.0.0 (Earlier)
- Auto-replace with backup
- Custom SPEC_INDEX support
- --no-replace flag

---

## Usage Patterns

### Pattern 1: Complete New Project
```bash
# 1. Generate SPEC
"Create SPEC for e-commerce platform..."

# 2. Optional: Generate plan
specs/ecommerce/spec-001/spec.md

# 3. Generate tasks
specs/ecommerce/spec-001/spec.md

# 4. Generate implementation prompt
specs/ecommerce/spec-001/tasks.md

# 5. Implement
kilo code implement specs/ecommerce/spec-001/kilo-prompt.md

# 6. Track progress
specs/ecommerce/spec-001/tasks.md
```

### Pattern 2: Update Existing
```bash
# 1. Update SPEC
specs/existing/spec-004/spec.md

# 2. Sync tasks
specs/existing/spec-004/spec.md

# 3. Regenerate prompt
specs/existing/spec-004/tasks.md

# 4. Continue implementation
kilo code implement specs/existing/spec-004/kilo-prompt-YYYYMMDD.md
```

### Pattern 3: Dry-Run Review
```bash
# 1. Dry-run SPEC
"Create payment SPEC..." --nogenerate

# 2. Review, adjust

# 3. Dry-run tasks
specs/payment/spec-006/spec.md --nogenerate

# 4. Review, adjust

# 5. Generate for real
specs/payment/spec-006/spec.md
```

---

## Quick Reference

### Common Flags
- `--specindex="path"` - Use custom SPEC_INDEX
- `--nogenerate` - Dry run (show plan without creating)
- `--output="name.md"` - Custom output filename (plan only)
- `--check-only` - Check without updating (sync only)
- `--detailed` - Detailed report (verify only)

### File Conventions
- `spec.md` - Technical specification
- `plan.md` - Project roadmap
- `tasks.md` - Implementation tasks
- `kilo-prompt.md` - Implementation prompt
- `README.md` - Implementation guide
- `data-model.md` - Data schemas
- `openapi.yaml` - API specification
- `test-plan.md` - Testing strategy

### Status Markers
- ⬜ Pending
- 🟦 In Progress
- ✅ Complete
- ❌ Blocked

---

## System Requirements

**Prerequisites:**
- `.smartspec/` directory with knowledge base files
- `SPEC_INDEX.json` (or custom path)
- Node.js/TypeScript project (for validation)
- Git (recommended)

**Optional:**
- Kilo Code (for automated implementation)
- Claude Code (alternative executor)

---

## Support & Troubleshooting

### Common Issues

**Issue:** SPEC_INDEX not found
**Solution:** Create `.smartspec/SPEC_INDEX.json` or specify path with --specindex

**Issue:** Critical sections lost during EDIT
**Solution:** Check preservation logic, verify CRITICAL_REGISTRY loaded

**Issue:** Supporting files not detected
**Solution:** Check file naming conventions, ensure files in SPEC_DIR

**Issue:** Phases exceed 10 tasks
**Solution:** Review phase boundaries, may need manual adjustment

---

## Version Compatibility

**Backward Compatibility:**
- ✅ v4.0 workflows compatible with v3.5+ knowledge base
- ✅ v3.x SPECs work with v4.0 workflows
- ⚠️ v2.x SPECs may need minor updates

**Migration Path:**
- v2.x → v3.x: Update SPEC headers, add mandatory sections
- v3.x → v4.0: No changes needed, new features automatically available

---

## License & Attribution

**Author:** SmartSpec Architect System
**Version:** 4.0.0
**Release Date:** December 3, 2025
**License:** Internal Use

---

## Change Log

**v4.0.0 (December 3, 2025):**
- NEW: smartspec_generate_plan workflow
- NEW: smartspec_verify_tasks_progress workflow
- NEW: smartspec_sync_spec_tasks workflow
- ENHANCED: All workflows support --specindex
- ENHANCED: spec/tasks workflows support --nogenerate
- ENHANCED: Supporting files auto-detection & generation
- ENHANCED: Kilo + Claude Code compatibility
- ENHANCED: Comprehensive documentation (8 guides)
- UPDATED: All workflows to v4.0 standards
- UPDATED: Author field format (SmartSpec Architect v4.0)
- UPDATED: Spec reference resolution with paths + repos

**v3.5.0 (November 2025):**
- Critical section preservation
- Spec reference resolution
- Enhanced validation

**v3.0.0:**
- Auto-replace with backup
- Custom SPEC_INDEX support

---

**For detailed usage of each workflow, refer to individual workflow files.**
