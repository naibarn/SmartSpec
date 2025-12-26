# Knowledge Base Consolidation Plan

**Date:** 2025-12-26  
**Goal:** Reduce knowledge base files from 19 to 8-10 files

---

## Current State

**Total Files:** 19 markdown files in `.smartspec/`

### Files by Category

#### Workflow Guides (9 files) - **Target: 2 files**
1. AFTER_PROMPT_GENERATION_GUIDE.md (12 KB)
2. BATCH_EXECUTION_GUIDE.md (12 KB)
3. PROMPTER_USAGE_GUIDE.md (12 KB)
4. VERIFICATION_WORKFLOWS_GUIDE.md (16 KB)
5. VERIFY_REPORT_ACTION_GUIDE.md (20 KB)
6. WORKFLOW_PARAMETERS_REFERENCE.md (36 KB)
7. WORKFLOW_SCENARIOS_GUIDE.md (20 KB)
8. PROBLEM_SOLUTION_MATRIX.md (16 KB)
9. TROUBLESHOOTING_DECISION_TREE.md (16 KB)

#### System Knowledge (5 files) - **Target: 2 files**
10. knowledge_base_smartspec_handbook.md (16 KB)
11. knowledge_base_smartspec_install_and_usage.md (48 KB)
12. knowledge_base_autopilot_workflows.md (16 KB)
13. knowledge_base_autopilot_cli_workflows.md (24 KB)
14. knowledge_base_a2ui_workflows.md (16 KB)

#### Core System (3 files) - **Keep as-is**
15. constitution.md (4 KB)
16. kilocode-context.md (28 KB)
17. system_prompt_smartspec.md (8 KB)

#### Reference (2 files) - **Keep as-is**
18. ui-json-formats-comparison.md (8 KB)
19. workflow-selection-guide.md (4 KB)

---

## Consolidation Strategy

### New Structure (10 files total)

#### 1. **SMARTSPEC_COMPLETE_GUIDE.md** (NEW)
**Size:** ~80 KB  
**Consolidates:** 5 files
- VERIFICATION_WORKFLOWS_GUIDE.md
- AFTER_PROMPT_GENERATION_GUIDE.md
- BATCH_EXECUTION_GUIDE.md
- PROMPTER_USAGE_GUIDE.md
- VERIFY_REPORT_ACTION_GUIDE.md

**Content:**
```markdown
# SmartSpec Complete Guide

## 1. Introduction
## 2. Quick Start
## 3. Verification Workflow
   - Running verification
   - Understanding reports
   - What to do with results
## 4. Prompt Generation
   - Using prompter
   - Understanding generated prompts
   - Filtering by category/priority
## 5. After Prompt Generation
   - Decision tree (batch vs manual)
   - Manual execution
   - Batch execution
## 6. Complete Examples
## 7. Best Practices
## 8. FAQ
## 9. Troubleshooting
```

---

#### 2. **WORKFLOW_REFERENCE.md** (NEW)
**Size:** ~60 KB  
**Consolidates:** 4 files
- WORKFLOW_PARAMETERS_REFERENCE.md
- WORKFLOW_SCENARIOS_GUIDE.md
- PROBLEM_SOLUTION_MATRIX.md
- TROUBLESHOOTING_DECISION_TREE.md

**Content:**
```markdown
# Workflow Reference

## 1. Quick Reference
   - Problem → Solution mapping
   - Decision trees
## 2. Workflow Parameters
   - All workflow flags
   - Parameter descriptions
   - Examples
## 3. Common Scenarios
   - Scenario-based guides
   - When to use what
## 4. Troubleshooting
   - Common problems
   - Solutions
   - Decision trees
```

---

#### 3. **SMARTSPEC_HANDBOOK.md** (NEW)
**Size:** ~70 KB  
**Consolidates:** 3 files
- knowledge_base_smartspec_handbook.md
- knowledge_base_smartspec_install_and_usage.md
- workflow-selection-guide.md

**Content:**
```markdown
# SmartSpec Handbook

## 1. Installation & Setup
## 2. Core Concepts
## 3. Workflow Selection
## 4. Usage Patterns
## 5. Configuration
## 6. Best Practices
```

---

#### 4. **AUTOPILOT_GUIDE.md** (NEW)
**Size:** ~50 KB  
**Consolidates:** 2 files
- knowledge_base_autopilot_workflows.md
- knowledge_base_autopilot_cli_workflows.md

**Content:**
```markdown
# Autopilot Guide

## 1. Overview
## 2. Autopilot Workflows
## 3. CLI Workflows
## 4. Usage Examples
## 5. Best Practices
```

---

#### 5-10. **Keep As-Is** (6 files)
5. constitution.md (4 KB)
6. kilocode-context.md (28 KB)
7. system_prompt_smartspec.md (8 KB)
8. ui-json-formats-comparison.md (8 KB)
9. knowledge_base_a2ui_workflows.md (16 KB) - specific feature
10. (Reserved for future)

---

## Implementation Plan

### Phase 1: Create Consolidated Files ✅

#### Step 1.1: Create SMARTSPEC_COMPLETE_GUIDE.md
```bash
# Merge 5 workflow guides into one comprehensive guide
cat VERIFICATION_WORKFLOWS_GUIDE.md \
    AFTER_PROMPT_GENERATION_GUIDE.md \
    BATCH_EXECUTION_GUIDE.md \
    PROMPTER_USAGE_GUIDE.md \
    VERIFY_REPORT_ACTION_GUIDE.md \
    > /tmp/combined.md

# Restructure and create final guide
# (Manual editing required for proper structure)
```

#### Step 1.2: Create WORKFLOW_REFERENCE.md
```bash
# Merge 4 reference guides
cat WORKFLOW_PARAMETERS_REFERENCE.md \
    WORKFLOW_SCENARIOS_GUIDE.md \
    PROBLEM_SOLUTION_MATRIX.md \
    TROUBLESHOOTING_DECISION_TREE.md \
    > /tmp/workflow_ref.md
```

#### Step 1.3: Create SMARTSPEC_HANDBOOK.md
```bash
# Merge handbook files
cat knowledge_base_smartspec_handbook.md \
    knowledge_base_smartspec_install_and_usage.md \
    workflow-selection-guide.md \
    > /tmp/handbook.md
```

#### Step 1.4: Create AUTOPILOT_GUIDE.md
```bash
# Merge autopilot files
cat knowledge_base_autopilot_workflows.md \
    knowledge_base_autopilot_cli_workflows.md \
    > /tmp/autopilot.md
```

---

### Phase 2: Move Old Files to Archive
```bash
mkdir -p .smartspec/archive/pre-consolidation-2025-12-26

# Move old workflow guides
mv .smartspec/VERIFICATION_WORKFLOWS_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/AFTER_PROMPT_GENERATION_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/BATCH_EXECUTION_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/PROMPTER_USAGE_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/VERIFY_REPORT_ACTION_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/

# Move old reference guides
mv .smartspec/WORKFLOW_PARAMETERS_REFERENCE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/WORKFLOW_SCENARIOS_GUIDE.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/PROBLEM_SOLUTION_MATRIX.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/TROUBLESHOOTING_DECISION_TREE.md .smartspec/archive/pre-consolidation-2025-12-26/

# Move old handbook files
mv .smartspec/knowledge_base_smartspec_handbook.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/knowledge_base_smartspec_install_and_usage.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/workflow-selection-guide.md .smartspec/archive/pre-consolidation-2025-12-26/

# Move old autopilot files
mv .smartspec/knowledge_base_autopilot_workflows.md .smartspec/archive/pre-consolidation-2025-12-26/
mv .smartspec/knowledge_base_autopilot_cli_workflows.md .smartspec/archive/pre-consolidation-2025-12-26/
```

---

### Phase 3: Update References
Update all references in:
- system_prompt_smartspec.md
- Other remaining files
- Workflows
- Scripts

---

## Benefits

### Before
- ❌ 19 files
- ❌ Scattered information
- ❌ Hard to find
- ❌ Duplicate content
- ❌ Inconsistent structure

### After
- ✅ 10 files (-47%)
- ✅ Organized by purpose
- ✅ Easy to navigate
- ✅ No duplication
- ✅ Consistent structure

---

## File Reduction Summary

| Category | Before | After | Reduction |
|:---|:---:|:---:|:---:|
| Workflow Guides | 9 | 2 | -78% |
| System Knowledge | 5 | 2 | -60% |
| Core System | 3 | 3 | 0% |
| Reference | 2 | 2 | 0% |
| A2UI (keep) | 0 | 1 | - |
| **Total** | **19** | **10** | **-47%** |

---

## Next Steps

1. ✅ Create consolidation plan (this document)
2. ⏳ Create SMARTSPEC_COMPLETE_GUIDE.md
3. ⏳ Create WORKFLOW_REFERENCE.md
4. ⏳ Create SMARTSPEC_HANDBOOK.md
5. ⏳ Create AUTOPILOT_GUIDE.md
6. ⏳ Move old files to archive
7. ⏳ Update all references
8. ⏳ Test workflows
9. ⏳ Commit and push

---

**Status:** Plan Created  
**Ready for:** Implementation
