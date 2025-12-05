# Manual Update Checkboxes Guide

Guide for manually updating checkboxes in tasks.md

---

## 📋 When to Use Manual Update

### When is Manual Update Needed?

1. **`/smartspec_implement_tasks` doesn't mark checkboxes**
   - Workflow completed but checkboxes remain `[ ]`
   - Need manual update to track progress

2. **`/smartspec_verify_tasks_progress` not run yet**
   - Haven't run verify workflow yet
   - Want to mark checkboxes beforehand

3. **Manual Implementation**
   - Working without using workflows
   - Need to mark checkboxes to track progress

4. **Partial Implementation**
   - Some tasks completed
   - Need to mark only completed tasks

---

## 🔧 Method 1: Using sed (Fastest)

### Mark Single Task

```bash
# Mark T001 as complete
sed -i 's/^- \[ \] \(T001:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[x\] T001:" specs/feature/spec-004/tasks.md
```

---

### Mark Multiple Tasks (Range)

```bash
# Mark T001-T010 as complete
sed -i 's/^- \[ \] \(T00[1-9]:\|T010:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[x\] T0[01][0-9]:" specs/feature/spec-004/tasks.md
```

---

### Mark Specific Tasks

```bash
# Mark T001, T003, T005 as complete
sed -i 's/^- \[ \] \(T001:\|T003:\|T005:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[x\] T00[135]:" specs/feature/spec-004/tasks.md
```

---

### Mark All Tasks in a Phase

```bash
# Mark all tasks in Phase 1 (T001-T020)
sed -i 's/^- \[ \] \(T0[01][0-9]:\|T020:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[x\] T0[012][0-9]:" specs/feature/spec-004/tasks.md
```

---

## 🔧 Method 2: Using Bash Script (Flexible)

### Create Script

```bash
cat > /tmp/update_checkboxes.sh << 'SCRIPT_EOF'
#!/bin/bash

# Usage: ./update_checkboxes.sh <tasks.md> <task_ids>
# Example: ./update_checkboxes.sh tasks.md "T001,T002,T003"

TASKS_FILE="$1"
TASK_IDS="$2"

if [ -z "$TASKS_FILE" ] || [ -z "$TASK_IDS" ]; then
  echo "Usage: $0 <tasks.md> <task_ids>"
  echo "Example: $0 tasks.md \"T001,T002,T003\""
  exit 1
fi

# Check file exists
if [ ! -f "$TASKS_FILE" ]; then
  echo "❌ Error: File not found: $TASKS_FILE"
  exit 1
fi

# Convert comma-separated to array
IFS=',' read -ra TASKS <<< "$TASK_IDS"

# Update each task
UPDATED=0
for task in "${TASKS[@]}"; do
  # Remove whitespace
  task=$(echo "$task" | xargs)
  
  # Update checkbox
  if sed -i "s/^- \[ \] \($task:\)/- [x] \1/" "$TASKS_FILE"; then
    echo "✅ Marked $task as complete"
    ((UPDATED++))
  else
    echo "⚠️  Could not update $task (already marked or not found)"
  fi
done

echo ""
echo "✅ Updated $UPDATED tasks"
SCRIPT_EOF

chmod +x /tmp/update_checkboxes.sh
```

---

### Using the Script

```bash
# Mark T001-T010
/tmp/update_checkboxes.sh specs/feature/spec-004/tasks.md "T001,T002,T003,T004,T005,T006,T007,T008,T009,T010"

# Output:
# ✅ Marked T001 as complete
# ✅ Marked T002 as complete
# ...
# ✅ Updated 10 tasks
```

---

## 🔧 Method 3: Using Python Script (Most Accurate)

### Create Script

```python
#!/usr/bin/env python3
"""
Update checkboxes in tasks.md for completed tasks.

Usage:
    python3 update_checkboxes.py <tasks.md> <task_ids>

Examples:
    python3 update_checkboxes.py tasks.md "T001,T002,T003"
    python3 update_checkboxes.py tasks.md "T001-T010"
"""

import sys
import re
from pathlib import Path


def parse_task_range(task_range):
    """Parse task range like 'T001-T010' into list of task IDs."""
    if '-' not in task_range:
        return [task_range]
    
    start, end = task_range.split('-')
    start_num = int(start[1:])  # Remove 'T' prefix
    end_num = int(end[1:])
    
    return [f"T{i:03d}" for i in range(start_num, end_num + 1)]


def parse_task_ids(task_ids_str):
    """Parse comma-separated task IDs or ranges."""
    task_ids = []
    for part in task_ids_str.split(','):
        part = part.strip()
        if '-' in part:
            task_ids.extend(parse_task_range(part))
        else:
            task_ids.append(part)
    return task_ids


def update_checkboxes(tasks_file, task_ids):
    """Update checkboxes in tasks.md for specified tasks."""
    
    # Read tasks.md
    tasks_path = Path(tasks_file)
    if not tasks_path.exists():
        print(f"❌ Error: File not found: {tasks_file}")
        return 1
    
    content = tasks_path.read_text(encoding='utf-8')
    
    # Update each task
    updated_count = 0
    for task_id in task_ids:
        pattern = rf'^- \[ \] ({re.escape(task_id)}:)'
        replacement = rf'- [x] \1'
        
        new_content, count = re.subn(
            pattern, replacement, content, flags=re.MULTILINE
        )
        
        if count > 0:
            content = new_content
            updated_count += count
            print(f"✅ Marked {task_id} as complete")
        else:
            # Check if already marked
            already_marked = re.search(
                rf'^- \[x\] ({re.escape(task_id)}:)',
                content,
                flags=re.MULTILINE
            )
            if already_marked:
                print(f"⚠️  {task_id} is already marked as complete")
            else:
                print(f"⚠️  {task_id} not found in tasks.md")
    
    # Write back
    if updated_count > 0:
        tasks_path.write_text(content, encoding='utf-8')
        print(f"\n✅ Updated {updated_count} tasks in {tasks_file}")
    else:
        print(f"\n⚠️  No tasks were updated")
    
    return 0


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 update_checkboxes.py <tasks.md> <task_ids>")
        print("")
        print("Examples:")
        print("  python3 update_checkboxes.py tasks.md \"T001,T002,T003\"")
        print("  python3 update_checkboxes.py tasks.md \"T001-T010\"")
        print("  python3 update_checkboxes.py tasks.md \"T001-T010,T015,T020\"")
        return 1
    
    tasks_file = sys.argv[1]
    task_ids_str = sys.argv[2]
    
    task_ids = parse_task_ids(task_ids_str)
    
    return update_checkboxes(tasks_file, task_ids)


if __name__ == '__main__':
    sys.exit(main())
```

---

### Save the Script

```bash
# Save to file
cat > /tmp/update_checkboxes.py << 'PYTHON_SCRIPT'
[... paste script above ...]
PYTHON_SCRIPT

chmod +x /tmp/update_checkboxes.py
```

---

### Using the Script

```bash
# Mark T001-T010
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010"

# Output:
# ✅ Marked T001 as complete
# ✅ Marked T002 as complete
# ...
# ✅ Updated 10 tasks in specs/feature/spec-004/tasks.md
```

```bash
# Mark specific tasks
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001,T003,T005"

# Output:
# ✅ Marked T001 as complete
# ✅ Marked T003 as complete
# ✅ Marked T005 as complete
# ✅ Updated 3 tasks in specs/feature/spec-004/tasks.md
```

```bash
# Mark range + specific
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010,T015,T020"

# Output:
# ✅ Marked T001 as complete
# ...
# ✅ Marked T010 as complete
# ✅ Marked T015 as complete
# ✅ Marked T020 as complete
# ✅ Updated 12 tasks in specs/feature/spec-004/tasks.md
```

---

## 🔧 Method 4: Using Text Editor (Manual)

### Visual Studio Code

1. Open `tasks.md`
2. Press `Ctrl+H` (Find and Replace)
3. Find: `- [ ] T001:`
4. Replace: `- [x] T001:`
5. Click "Replace All" or "Replace" one by one

---

### Vim

```bash
# Open file
vim specs/feature/spec-004/tasks.md

# Replace T001
:%s/^- \[ \] \(T001:\)/- [x] \1/

# Replace T001-T010
:%s/^- \[ \] \(T00[1-9]:\|T010:\)/- [x] \1/

# Save and exit
:wq
```

---

### Nano

```bash
# Open file
nano specs/feature/spec-004/tasks.md

# Press Ctrl+\ (Replace)
# Search for: - [ ] T001:
# Replace with: - [x] T001:
# Press A (Replace All)

# Save and exit
# Ctrl+O (Save)
# Ctrl+X (Exit)
```

---

## 📊 Usage Examples

### Scenario 1: Mark Tasks After Implementation

```bash
# 1. Implement tasks
/smartspec_implement_tasks specs/feature/spec-004/tasks.md --phase 1

# 2. Check if checkboxes were marked
grep "^- \[x\] T[0-9]" specs/feature/spec-004/tasks.md

# 3. If not marked → Manual update
sed -i 's/^- \[ \] \(T0[01][0-9]:\|T020:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# 4. Verify
grep "^- \[x\] T0[012][0-9]:" specs/feature/spec-004/tasks.md
```

---

### Scenario 2: Mark Specific Tasks

```bash
# You completed T001, T003, T005
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001,T003,T005"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### Scenario 3: Mark Entire Phase

```bash
# Phase 1 (T001-T020) completed
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T020"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### Scenario 4: Unmark Tasks (Rollback)

```bash
# Unmark T001-T010 (if need to redo)
sed -i 's/^- \[x\] \(T00[1-9]:\|T010:\)/- [ ] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[ \] T0[01][0-9]:" specs/feature/spec-004/tasks.md
```

---

## ✅ Best Practices

### 1. Check Before Update

```bash
# See incomplete tasks
grep "^- \[ \] T[0-9]" specs/feature/spec-004/tasks.md

# See completed tasks
grep "^- \[x\] T[0-9]" specs/feature/spec-004/tasks.md
```

---

### 2. Backup Before Update

```bash
# Backup tasks.md
cp specs/feature/spec-004/tasks.md specs/feature/spec-004/tasks.md.backup

# Update
sed -i 's/^- \[ \] \(T001:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# If mistake → Restore
cp specs/feature/spec-004/tasks.md.backup specs/feature/spec-004/tasks.md
```

---

### 3. Verify After Update

```bash
# Update
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### 4. Commit After Update

```bash
# Update checkboxes
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010"

# Commit
git add specs/feature/spec-004/tasks.md
git commit -m "chore: Mark T001-T010 as complete"
```

---

## 🚨 Troubleshooting

### Issue: sed doesn't work (macOS)

**Cause:** macOS uses BSD sed which requires backup extension

**Solution:**
```bash
# macOS
sed -i.bak 's/^- \[ \] \(T001:\)/- [x] \1/' tasks.md

# Or install GNU sed
brew install gnu-sed
gsed -i 's/^- \[ \] \(T001:\)/- [x] \1/' tasks.md
```

---

### Issue: Updated Wrong Task

**Cause:** Pattern doesn't match

**Solution:**
```bash
# Check pattern first
grep "^- \[ \] T001:" tasks.md

# If not found → Check actual format
grep "T001" tasks.md

# Fix pattern to match
```

---

### Issue: Script Doesn't Run

**Cause:** No execute permission

**Solution:**
```bash
chmod +x /tmp/update_checkboxes.sh
chmod +x /tmp/update_checkboxes.py
```

---

## 📚 Related Workflows

### Better Alternative to Manual Update

```bash
# Better: Use verify_tasks_progress
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md

# This workflow will:
# 1. Check completed tasks
# 2. Mark checkboxes automatically
# 3. Generate progress report
```

---

## ✅ Summary

### Which Method to Use?

| Method | Speed | Accuracy | Flexibility | Recommended For |
|--------|-------|----------|-------------|-----------------|
| **sed** | ⚡⚡⚡ | ⭐⭐ | ⭐⭐ | Quick updates |
| **Bash Script** | ⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ | Multiple tasks |
| **Python Script** | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Complex updates |
| **Text Editor** | ⚡ | ⭐⭐⭐⭐ | ⭐ | Single task |

---

### Recommendations:

1. **Use sed** → For quick updates (1-2 tasks)
2. **Use Python Script** → For bulk updates (10+ tasks)
3. **Use verify_tasks_progress** → Best! (auto-detect + mark)

---

**This file is part of SmartSpec Documentation**  
**Repository:** https://github.com/naibarn/SmartSpec
