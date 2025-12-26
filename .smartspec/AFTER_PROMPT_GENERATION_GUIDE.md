# After Prompt Generation - What's Next?

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Purpose:** Guide for using generated prompts effectively

---

## 📍 You Are Here

```
✅ Verified tasks (verify_evidence_enhanced.py)
✅ Generated prompts (generate_prompts_from_verify_report.py)
👉 YOU ARE HERE - What to do with the prompts?
```

---

## 🎯 Quick Decision

### Got 1-4 Prompts? → Manual Execution
**Time:** 5-15 minutes  
**Best for:** Small fixes, quick tasks

[Skip to Manual Execution](#manual-execution)

### Got 5+ Prompts? → Batch Execution  
**Time:** 5-10 minutes  
**Best for:** Multiple tasks, large projects

[Skip to Batch Execution](#batch-execution)

---

## 📂 Understanding Your Prompts Directory

After running `generate_prompts_from_verify_report.py`, you get:

```
.spec/prompts/YYYYMMDD_HHMMSS/
├── README.md                    # 📖 START HERE
├── 01-not_implemented.md        # Priority 2
├── 02-missing_tests.md          # Priority 2
├── 03-missing_code.md           # Priority 2
├── 04-symbol_issues.md          # Priority 3
├── 05-content_issues.md         # Priority 3
├── 06-naming_issues.md          # Priority 4
└── meta/
    └── summary.json             # Metadata
```

### File Naming Convention

```
NN-category_name.md
│  │
│  └─ Category name
└──── Priority order (01 = highest)
```

---

## 📖 Step 1: Read README.md (ALWAYS!)

```bash
cat .spec/prompts/latest/README.md
```

**README contains:**
- 📊 Summary statistics
- 📋 Priority order
- 📁 File list
- ⚡ Quick start commands
- 🎯 Recommended approach

**Example README:**

```markdown
# Generated Prompts Summary

**Total Tasks:** 12
**Categories:** 4

## Priority Order

1. **Priority 2: Not Implemented** (5 tasks)
   File: 01-not_implemented.md

2. **Priority 2: Missing Tests** (4 tasks)
   File: 02-missing_tests.md

3. **Priority 3: Symbol Issues** (2 tasks)
   File: 04-symbol_issues.md

4. **Priority 4: Naming Issues** (1 task)
   File: 06-naming_issues.md

## Recommended Approach

For 12 tasks, we recommend **Batch Execution**:

```bash
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint
```
```

---

## 🚀 Option 1: Batch Execution (Recommended for 5+)

### When to Use
- ✅ 5+ prompt files
- ✅ Multiple categories
- ✅ Want automation
- ✅ Want progress tracking
- ✅ Want checkpoint support

### Quick Start

```bash
# 1. Preview execution plan (optional)
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run

# 2. Execute all prompts
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# 3. Verify results
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

### What Happens

```
📖 Parsing prompts directory...
   Found 12 tasks in 4 categories

📋 Execution Plan:

not_implemented (Priority 2): 5 tasks
missing_tests (Priority 2): 4 tasks
symbol_issues (Priority 3): 2 tasks
naming_issues (Priority 4): 1 task

🚀 Starting batch execution...

[1/12] TASK-001: Add user authentication
   ✅ Success (3.2s)
[2/12] TASK-002: Add payment processing
   ✅ Success (2.8s)
...
[12/12] TASK-012: Fix naming issue
   ✅ Success (0.5s)

✅ Batch execution complete!
   Successful: 12/12 (100%)
   Failed: 0/12 (0%)
   Duration: 45.3s

📊 Report saved: .spec/reports/batch_execution_20251226_090000.md
```

### Advanced Options

```bash
# Execute only high priority
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --only-category not_implemented,missing_tests

# Skip low priority
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --skip-category naming_issues

# Verify after each category
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint \
  --verify-after-each
```

### See Full Guide
📚 `.smartspec/BATCH_EXECUTION_GUIDE.md`

---

## 📝 Option 2: Manual Execution

### When to Use
- ✅ 1-4 prompt files
- ✅ Simple fixes
- ✅ Want full control
- ✅ Learning the system

### Step-by-Step

#### Step 1: Read Priority Order

```bash
cat .spec/prompts/latest/README.md
```

#### Step 2: Start with Highest Priority

```bash
# Example: Priority 2 - Not Implemented
cat .spec/prompts/latest/01-not_implemented.md
```

#### Step 3: Follow Each Prompt

Each prompt contains:

```markdown
## Task 1: TASK-001 - Add user authentication

### Description
Implement user authentication with JWT tokens

### Files to Create
1. src/auth/user_auth.py
2. tests/auth/test_user_auth.py

### Implementation

#### File: src/auth/user_auth.py
```python
# EVIDENCE_HOOK: TASK-001
class UserAuth:
    def __init__(self):
        pass
    
    def authenticate(self, username, password):
        # Implementation here
        pass
```

#### File: tests/auth/test_user_auth.py
```python
from src.auth.user_auth import UserAuth

def test_user_auth():
    auth = UserAuth()
    assert auth.authenticate("user", "pass") == True
```

### Verification
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```
```

#### Step 4: Implement

1. **Create files** as specified
2. **Copy code** from prompts
3. **Customize** as needed
4. **Add evidence hooks** (already in code)

#### Step 5: Verify After Each Category

```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

#### Step 6: Move to Next Category

```bash
# Next category
cat .spec/prompts/latest/02-missing_tests.md
```

#### Step 7: Repeat Until Done

Continue until all categories are complete

---

## 🎯 Recommended Workflow by Task Count

| Tasks | Method | Time | Command |
|:---|:---|:---|:---|
| 1-2 | Manual | 5-10 min | Read prompts, implement |
| 3-4 | Manual | 10-20 min | Read prompts, implement |
| 5-10 | **Batch** | 5-10 min | `execute_prompts_batch.py` |
| 11-20 | **Batch** | 10-20 min | `execute_prompts_batch.py` |
| 21+ | **Batch** | 20+ min | `execute_prompts_batch.py --checkpoint` |

---

## 📊 Complete Example

### Scenario: 8 Tasks Generated

```bash
# 1. Check what was generated
cat .spec/prompts/latest/README.md

# Output:
# Total: 8 tasks
# Categories: 3
# - not_implemented (3 tasks)
# - missing_tests (4 tasks)
# - naming_issues (1 task)
# Recommended: Batch Execution

# 2. Preview batch execution
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run

# Output:
# 📋 Execution Plan:
# not_implemented: 3 tasks
# missing_tests: 4 tasks
# naming_issues: 1 task
# Total: 8 tasks
# Estimated time: 8-12 minutes

# 3. Execute batch
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint

# Output:
# 🚀 Executing 8 tasks...
# [1/8] ✅ Success
# [2/8] ✅ Success
# ...
# [8/8] ✅ Success
# ✅ Complete! (100%)

# 4. Verify all
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Output:
# ✅ All tasks verified!
# Total: 20 tasks
# Verified: 20 (100%)

# 5. Commit
git add -A
git commit -m "feat: Implement tasks from batch execution"
```

---

## 🔄 What If Something Fails?

### During Batch Execution

```bash
# Execution stops at task 5
[5/8] ❌ Failed: TASK-005
⚠️  Max failures reached. Stopping.

# Check what failed
cat .spec/reports/batch_execution_latest.md

# Fix the issue manually
vim src/problematic_file.py

# Resume from checkpoint
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --checkpoint \
  --resume
```

### During Manual Execution

```bash
# Verify to see what's wrong
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md

# Re-generate prompts for failed tasks only
python3 .smartspec/scripts/generate_prompts_from_verify_report.py \
  --verify-report .spec/reports/latest/summary.json \
  --tasks tasks.md

# Try again
```

---

## 💡 Pro Tips

### Tip 1: Always Read README First
```bash
cat .spec/prompts/latest/README.md
```

### Tip 2: Use Dry-Run for Large Batches
```bash
python3 .smartspec/scripts/execute_prompts_batch.py \
  --prompts-dir .spec/prompts/latest/ \
  --tasks tasks.md \
  --dry-run
```

### Tip 3: Enable Checkpoint for 10+ Tasks
```bash
--checkpoint
```

### Tip 4: Focus on High Priority First
```bash
--only-category not_implemented,missing_tests
```

### Tip 5: Verify Incrementally
```bash
--verify-after-each
```

### Tip 6: Commit After Each Category
```bash
# After not_implemented
git add -A
git commit -m "feat: Implement not_implemented tasks"

# After missing_tests
git add -A
git commit -m "test: Add missing tests"
```

---

## 🎓 Best Practices

### 1. Follow Priority Order
Always implement in priority order (1 → 4)

### 2. Verify After Each Category
```bash
python3 .smartspec/scripts/verify_evidence_enhanced.py tasks.md
```

### 3. Use Batch for 5+ Tasks
Saves 70-80% time

### 4. Keep Evidence Hooks
Don't remove `# EVIDENCE_HOOK: TASK-XXX` comments

### 5. Test Before Committing
```bash
pytest tests/ -v
```

### 6. Commit Incrementally
Don't wait until everything is done

---

## 📚 Related Guides

- **Batch Execution:** `.smartspec/BATCH_EXECUTION_GUIDE.md`
- **Verification:** `.smartspec/VERIFICATION_WORKFLOWS_GUIDE.md`
- **Troubleshooting:** `.smartspec/TROUBLESHOOTING_DECISION_TREE.md`
- **Problem-Solution:** `.smartspec/PROBLEM_SOLUTION_MATRIX.md`

---

## 🔗 Complete Workflow

```
1. Verify
   ↓
2. Generate Prompts
   ↓
3. Read README ← YOU ARE HERE
   ↓
4. Choose Method (Batch or Manual)
   ↓
5. Execute
   ↓
6. Verify Again
   ↓
7. Commit
   ↓
8. Done!
```

---

## ❓ FAQ

### Q: Which method should I use?

**A:** 
- 1-4 tasks → Manual
- 5+ tasks → Batch

### Q: Can I mix batch and manual?

**A:** Yes! Use batch for bulk, manual for specific fixes.

### Q: What if batch fails midway?

**A:** Use `--checkpoint` flag to enable resume.

### Q: Can I skip categories?

**A:** Yes! Use `--skip-category` or `--only-category`.

### Q: How do I know what failed?

**A:** Check `.spec/reports/batch_execution_latest.md`

### Q: Can I customize prompts?

**A:** Yes! Edit prompt files before execution.

---

## 🎯 Summary

**After generating prompts:**

1. **Read README.md** (always!)
2. **Choose method:**
   - 1-4 tasks → Manual
   - 5+ tasks → Batch
3. **Execute prompts**
4. **Verify results**
5. **Commit changes**

**Time savings with batch:**
- 70-80% faster
- 90% fewer errors
- Automatic progress tracking

---

**Version:** 1.0.0  
**Date:** 2025-12-26  
**Status:** Production Ready

**🚀 Now you know what to do with your generated prompts! 🚀**
