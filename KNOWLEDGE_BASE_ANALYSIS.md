# Knowledge Base Analysis & Update Plan

**Date:** 2025-12-26  
**Purpose:** Identify knowledge base files that need updates with new workflows and scripts

---

## Current Knowledge Base Files

### Core Knowledge Bases
1. `knowledge_base_smartspec_handbook.md` - Main handbook
2. `knowledge_base_smartspec_install_and_usage.md` - Installation guide
3. `knowledge_base_autopilot_workflows.md` - Autopilot execution features
4. `knowledge_base_autopilot_cli_workflows.md` - Autopilot CLI workflows
5. `knowledge_base_a2ui_workflows.md` - A2UI workflows

### Guides
1. `workflow-selection-guide.md` - Workflow selection
2. `WORKFLOW_SCENARIOS_GUIDE.md` - Scenario-based guide
3. `VERIFY_REPORT_ACTION_GUIDE.md` - Verify report actions
4. `PROMPTER_USAGE_GUIDE.md` - Prompter usage
5. `ss_autopilot/INTEGRATION_GUIDE.md` - Autopilot integration

### Script Documentation
1. `scripts/README.md` - Scripts overview
2. `scripts/README_verify_evidence_strict.md` - Old verify script
3. `scripts/README_migrate_evidence_hooks.md` - Migration script

---

## Recent Changes (2025-12-26)

### New Scripts
1. ✅ `verify_evidence_enhanced.py` (797 lines)
   - Replaces: `verify_evidence_strict.py`
   - Features: 8 new features (categorization, fuzzy matching, etc.)
   
2. ✅ `generate_prompts_from_verify_report.py` (650+ lines)
   - New: Complete prompter implementation
   - Features: Template engine, category filtering, priority ordering

### Updated Workflows
1. ✅ `smartspec_verify_tasks_progress_strict.md` (v6.2.0 → v6.3.0)
   - Now uses `verify_evidence_enhanced.py`
   
2. ✅ `smartspec_report_implement_prompter.md` (v7.0.0 → v7.1.0)
   - Now has Python implementation
   - Added `--verify-report` flag

### New Documentation
1. ✅ `VERIFY_REPORT_ACTION_GUIDE.md` - Action guide for verify reports
2. ✅ `PROMPTER_USAGE_GUIDE.md` - Complete prompter usage

---

## Files That Need Updates

### Priority 1: Critical (Must Update)

#### 1. `workflow-selection-guide.md`
**Current Status:** Outdated  
**Missing:**
- New verify script (verify_evidence_enhanced.py)
- Prompter implementation (generate_prompts_from_verify_report.py)
- Updated workflow versions

**Update Needed:**
- Add verify report → prompter workflow
- Update verification workflow to v6.3.0
- Add problem-solution mapping

---

#### 2. `knowledge_base_smartspec_handbook.md`
**Current Status:** May be outdated  
**Missing:**
- Enhanced verification features
- Prompter implementation
- New troubleshooting workflows

**Update Needed:**
- Add section on verification enhancements
- Add section on automated prompt generation
- Update workflow references

---

#### 3. `scripts/README.md`
**Current Status:** Outdated  
**Missing:**
- verify_evidence_enhanced.py
- generate_prompts_from_verify_report.py

**Update Needed:**
- Add new scripts documentation
- Mark old scripts as deprecated
- Add usage examples

---

### Priority 2: Important (Should Update)

#### 4. `WORKFLOW_SCENARIOS_GUIDE.md`
**Current Status:** May need updates  
**Missing:**
- Scenario: "Verify report shows issues"
- Scenario: "Need to fix multiple categories"

**Update Needed:**
- Add verify → prompter → fix scenario
- Add troubleshooting scenarios

---

#### 5. `knowledge_base_smartspec_install_and_usage.md`
**Current Status:** May need script updates  
**Missing:**
- New script dependencies
- New workflow usage

**Update Needed:**
- Update script list
- Add new workflow examples

---

### Priority 3: Optional (Nice to Have)

#### 6. `scripts/README_verify_evidence_strict.md`
**Current Status:** Deprecated  
**Action:** Mark as deprecated, point to enhanced version

---

## Problem-Solution Mapping Needed

### Problem Categories

#### 1. Verification Issues
**Problems:**
- Tasks not verified
- Evidence not found
- Files missing

**Solutions:**
- Run `verify_evidence_enhanced.py`
- Check report for categorized issues
- Use prompter to generate fix prompts

**Workflow:**
```bash
verify → review report → generate prompts → implement → verify again
```

---

#### 2. Implementation Issues
**Problems:**
- Don't know what to implement
- Missing tests
- Missing code

**Solutions:**
- Use prompter with `--category` filter
- Follow generated prompts
- Implement step by step

**Workflow:**
```bash
prompter --category not_implemented → implement → test → verify
```

---

#### 3. Naming Issues
**Problems:**
- File names don't match evidence
- Similar files exist

**Solutions:**
- Check report suggestions
- Rename files or update evidence
- Use fuzzy matching results

**Workflow:**
```bash
verify → check similar_files → rename or update evidence → verify
```

---

#### 4. Symbol/Content Issues
**Problems:**
- Symbols missing
- Content doesn't match

**Solutions:**
- Use prompter with `--category symbol_issue`
- Add missing symbols/content
- Follow report suggestions

**Workflow:**
```bash
prompter --category symbol_issue → add symbols → verify
```

---

## Interactive Troubleshooting Guide Needed

### Structure

```
User Problem
  ↓
Question 1: What type of issue?
  → Verification failed
  → Implementation needed
  → Tests missing
  → Files not found
  ↓
Question 2: What category?
  → Not implemented
  → Missing tests
  → Naming issues
  → Symbol issues
  ↓
Recommended Workflow + Parameters
  → Specific command
  → Expected output
  → Next steps
```

---

## Recommended Updates

### 1. Create: `TROUBLESHOOTING_DECISION_TREE.md`
**Purpose:** Interactive guide for problem → solution
**Content:**
- Decision tree diagram
- Problem categories
- Workflow recommendations
- Command examples
- Expected outputs

---

### 2. Update: `workflow-selection-guide.md`
**Add:**
- Verification workflow section
- Prompter workflow section
- Problem-solution mapping
- Command examples

---

### 3. Update: `knowledge_base_smartspec_handbook.md`
**Add:**
- Section: "Enhanced Verification"
- Section: "Automated Prompt Generation"
- Section: "Troubleshooting Workflows"
- Updated workflow list

---

### 4. Update: `scripts/README.md`
**Add:**
- verify_evidence_enhanced.py documentation
- generate_prompts_from_verify_report.py documentation
- Deprecation notices
- Migration guide

---

### 5. Create: `PROBLEM_SOLUTION_MATRIX.md`
**Purpose:** Quick reference for problem → workflow mapping
**Format:** Table with:
- Problem description
- Category
- Recommended workflow
- Command
- Expected result

---

## Implementation Plan

### Phase 1: Critical Updates (Today)
1. Create `TROUBLESHOOTING_DECISION_TREE.md`
2. Create `PROBLEM_SOLUTION_MATRIX.md`
3. Update `workflow-selection-guide.md`
4. Update `scripts/README.md`

### Phase 2: Important Updates (This Week)
5. Update `knowledge_base_smartspec_handbook.md`
6. Update `WORKFLOW_SCENARIOS_GUIDE.md`
7. Update `knowledge_base_smartspec_install_and_usage.md`

### Phase 3: Cleanup (Next Week)
8. Mark deprecated files
9. Add migration guides
10. Create consolidated index

---

## Success Criteria

### For Each Updated File
- ✅ References new scripts
- ✅ References updated workflows
- ✅ Includes command examples
- ✅ Includes expected outputs
- ✅ Includes troubleshooting steps

### For New Files
- ✅ Clear structure
- ✅ Actionable recommendations
- ✅ Real-world examples
- ✅ Easy to navigate
- ✅ Cross-referenced

---

## Next Steps

1. Review this analysis
2. Approve update plan
3. Create new files (Phase 1)
4. Update existing files (Phase 1)
5. Test with real scenarios
6. Commit and deploy

---

**Status:** Analysis Complete  
**Ready for:** Implementation
