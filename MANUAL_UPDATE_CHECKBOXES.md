# Manual Update Checkboxes Guide

คู่มือการ update checkboxes ใน tasks.md ด้วยตัวเอง

---

## 📋 สถานการณ์ที่ต้องใช้

### เมื่อไหร่ต้อง Manual Update?

1. **`/smartspec_implement_tasks` ไม่ mark checkboxes**
   - Workflow เสร็จแล้ว แต่ checkboxes ยังเป็น `[ ]`
   - ต้อง manual update เพื่อ track progress

2. **`/smartspec_verify_tasks_progress` ยังไม่รัน**
   - ยังไม่ได้รัน verify workflow
   - ต้องการ mark checkboxes ก่อน

3. **Manual Implementation**
   - ทำงานเองโดยไม่ใช้ workflows
   - ต้อง mark checkboxes เพื่อ track progress

4. **Partial Implementation**
   - ทำงานบางส่วนเสร็จแล้ว
   - ต้อง mark เฉพาะ tasks ที่เสร็จ

---

## 🔧 วิธีที่ 1: ใช้ sed (เร็วที่สุด)

### Mark Task เดียว

```bash
# Mark T001 เสร็จ
sed -i 's/^- \[ \] \(T001:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# ตรวจสอบ
grep "^- \[x\] T001:" specs/feature/spec-004/tasks.md
```

---

### Mark หลาย Tasks (Range)

```bash
# Mark T001-T010 เสร็จ
sed -i 's/^- \[ \] \(T00[1-9]:\|T010:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# ตรวจสอบ
grep "^- \[x\] T0[01][0-9]:" specs/feature/spec-004/tasks.md
```

---

### Mark Tasks เฉพาะเจาะจง

```bash
# Mark T001, T003, T005 เสร็จ
sed -i 's/^- \[ \] \(T001:\|T003:\|T005:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# ตรวจสอบ
grep "^- \[x\] T00[135]:" specs/feature/spec-004/tasks.md
```

---

### Mark ทุก Tasks ใน Phase

```bash
# Mark ทุก tasks ใน Phase 1 (T001-T020)
sed -i 's/^- \[ \] \(T0[01][0-9]:\|T020:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# ตรวจสอบ
grep "^- \[x\] T0[012][0-9]:" specs/feature/spec-004/tasks.md
```

---

## 🔧 วิธีที่ 2: ใช้ Bash Script (ยืดหยุ่น)

### สร้าง Script

```bash
cat > /tmp/update_checkboxes.sh << 'EOF'
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
EOF

chmod +x /tmp/update_checkboxes.sh
```

---

### ใช้งาน Script

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

## 🔧 วิธีที่ 3: ใช้ Python Script (แม่นยำที่สุด)

### สร้าง Script

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

### บันทึก Script

```bash
cat > /tmp/update_checkboxes.py << 'PYTHON_SCRIPT'
[... paste script above ...]
PYTHON_SCRIPT

chmod +x /tmp/update_checkboxes.py
```

---

### ใช้งาน Script

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

## 🔧 วิธีที่ 4: ใช้ Text Editor (Manual)

### Visual Studio Code

1. เปิด `tasks.md`
2. กด `Ctrl+H` (Find and Replace)
3. Find: `- [ ] T001:`
4. Replace: `- [x] T001:`
5. กด "Replace All" หรือ "Replace" ทีละตัว

---

### Vim

```bash
# เปิดไฟล์
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
# เปิดไฟล์
nano specs/feature/spec-004/tasks.md

# กด Ctrl+\ (Replace)
# Search for: - [ ] T001:
# Replace with: - [x] T001:
# กด A (Replace All)

# Save and exit
# Ctrl+O (Save)
# Ctrl+X (Exit)
```

---

## 📊 ตัวอย่างการใช้งาน

### Scenario 1: Mark Tasks หลัง Implementation

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
# คุณทำ T001, T003, T005 เสร็จแล้ว
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001,T003,T005"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### Scenario 3: Mark Entire Phase

```bash
# Phase 1 (T001-T020) เสร็จแล้ว
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T020"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### Scenario 4: Unmark Tasks (Rollback)

```bash
# Unmark T001-T010 (ถ้าต้องการทำใหม่)
sed -i 's/^- \[x\] \(T00[1-9]:\|T010:\)/- [ ] \1/' specs/feature/spec-004/tasks.md

# Verify
grep "^- \[ \] T0[01][0-9]:" specs/feature/spec-004/tasks.md
```

---

## ✅ Best Practices

### 1. ตรวจสอบก่อน Update

```bash
# ดู tasks ที่ยังไม่เสร็จ
grep "^- \[ \] T[0-9]" specs/feature/spec-004/tasks.md

# ดู tasks ที่เสร็จแล้ว
grep "^- \[x\] T[0-9]" specs/feature/spec-004/tasks.md
```

---

### 2. Backup ก่อน Update

```bash
# Backup tasks.md
cp specs/feature/spec-004/tasks.md specs/feature/spec-004/tasks.md.backup

# Update
sed -i 's/^- \[ \] \(T001:\)/- [x] \1/' specs/feature/spec-004/tasks.md

# ถ้าผิดพลาด → Restore
cp specs/feature/spec-004/tasks.md.backup specs/feature/spec-004/tasks.md
```

---

### 3. Verify หลัง Update

```bash
# Update
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010"

# Verify
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md
```

---

### 4. Commit หลัง Update

```bash
# Update checkboxes
python3 /tmp/update_checkboxes.py specs/feature/spec-004/tasks.md "T001-T010"

# Commit
git add specs/feature/spec-004/tasks.md
git commit -m "chore: Mark T001-T010 as complete"
```

---

## 🚨 Troubleshooting

### ปัญหา: sed ไม่ทำงาน (macOS)

**สาเหตุ:** macOS ใช้ BSD sed ต้องระบุ backup extension

**วิธีแก้:**
```bash
# macOS
sed -i.bak 's/^- \[ \] \(T001:\)/- [x] \1/' tasks.md

# หรือติดตั้ง GNU sed
brew install gnu-sed
gsed -i 's/^- \[ \] \(T001:\)/- [x] \1/' tasks.md
```

---

### ปัญหา: Update ผิด Task

**สาเหตุ:** Pattern ไม่ตรง

**วิธีแก้:**
```bash
# ตรวจสอบ pattern ก่อน
grep "^- \[ \] T001:" tasks.md

# ถ้าไม่เจอ → ดู format จริง
grep "T001" tasks.md

# แก้ไข pattern ให้ตรง
```

---

### ปัญหา: Script ไม่ทำงาน

**สาเหตุ:** ไม่มี execute permission

**วิธีแก้:**
```bash
chmod +x /tmp/update_checkboxes.sh
chmod +x /tmp/update_checkboxes.py
```

---

## 📚 Related Workflows

### แทนที่ Manual Update

```bash
# วิธีที่ดีกว่า: ใช้ verify_tasks_progress
/smartspec_verify_tasks_progress specs/feature/spec-004/tasks.md

# Workflow จะ:
# 1. ตรวจสอบ tasks ที่เสร็จแล้ว
# 2. Mark checkboxes อัตโนมัติ
# 3. สร้าง progress report
```

---

## ✅ สรุป

### เลือกวิธีไหนดี?

| วิธี | ความเร็ว | ความแม่นยำ | ความยืดหยุ่น | แนะนำสำหรับ |
|------|---------|-----------|-------------|------------|
| **sed** | ⚡⚡⚡ | ⭐⭐ | ⭐⭐ | Quick updates |
| **Bash Script** | ⚡⚡ | ⭐⭐⭐ | ⭐⭐⭐ | Multiple tasks |
| **Python Script** | ⚡⚡ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Complex updates |
| **Text Editor** | ⚡ | ⭐⭐⭐⭐ | ⭐ | Single task |

---

### คำแนะนำ:

1. **ใช้ sed** → สำหรับ quick updates (1-2 tasks)
2. **ใช้ Python Script** → สำหรับ bulk updates (10+ tasks)
3. **ใช้ verify_tasks_progress** → ดีที่สุด! (auto-detect + mark)

---

**ไฟล์นี้เป็นส่วนหนึ่งของ SmartSpec Documentation**  
**Repository:** https://github.com/naibarn/SmartSpec
