"""
Enhanced status writer for user-friendly ai_specs/status.md output.

This module generates human-readable status files that guide non-dev users
through the SmartSpec workflow process.
"""

from __future__ import annotations

from typing import Dict, Any
from pathlib import Path
from datetime import datetime


class StatusWriter:
    """Write user-friendly status.md files"""
    
    def __init__(self, ai_specs_dir: str = "ai_specs"):
        self.ai_specs_dir = ai_specs_dir
        Path(ai_specs_dir).mkdir(exist_ok=True)
    
    # Step metadata
    STEP_INFO = {
        "SPEC": {
            "title": "สร้าง Specification",
            "description": "สร้างเอกสาร spec.md ที่อธิบายรายละเอียดของ feature",
            "time_estimate": "5-10 นาที",
            "what_it_does": [
                "วิเคราะห์ requirements",
                "สร้างเอกสาร spec.md",
                "กำหนด scope และ constraints"
            ]
        },
        "PLAN": {
            "title": "สร้าง Implementation Plan",
            "description": "สร้างแผนการพัฒนา (plan.md) ที่ระบุขั้นตอนการทำงาน",
            "time_estimate": "5-10 นาที",
            "what_it_does": [
                "วิเคราะห์ spec.md",
                "สร้างแผนการพัฒนา",
                "กำหนด architecture และ design decisions"
            ]
        },
        "TASKS": {
            "title": "สร้าง Task List",
            "description": "แยก implementation plan เป็น tasks ย่อย ๆ (tasks.md)",
            "time_estimate": "3-5 นาที",
            "what_it_does": [
                "แยก plan เป็น tasks ย่อย",
                "สร้าง checklist",
                "กำหนดลำดับความสำคัญ"
            ]
        },
        "IMPLEMENT": {
            "title": "เขียนโค้ดตาม Tasks",
            "description": "เขียนโค้ดตาม tasks ที่กำหนดไว้",
            "time_estimate": "10-30 นาที",
            "what_it_does": [
                "อ่าน tasks จาก tasks.md",
                "เขียนโค้ดตาม tasks",
                "สร้าง report บอกว่าเขียนอะไรไปบ้าง"
            ]
        },
        "SYNC_TASKS": {
            "title": "Sync Task Checkboxes",
            "description": "อัปเดต checkboxes ใน tasks.md ตามความคืบหน้า",
            "time_estimate": "1-2 นาที",
            "what_it_does": [
                "ตรวจสอบ tasks ที่เสร็จแล้ว",
                "อัปเดต checkboxes",
                "สร้าง progress report"
            ]
        },
        "TEST_SUITE": {
            "title": "รัน Test Suite",
            "description": "รัน automated tests เพื่อตรวจสอบว่าโค้ดทำงานถูกต้อง",
            "time_estimate": "5-15 นาที",
            "what_it_does": [
                "รัน unit tests",
                "รัน integration tests",
                "สร้าง test report"
            ]
        },
        "QUALITY_GATE": {
            "title": "Quality Gate Check",
            "description": "ตรวจสอบคุณภาพโค้ดและ compliance",
            "time_estimate": "3-5 นาที",
            "what_it_does": [
                "ตรวจสอบ code quality",
                "ตรวจสอบ test coverage",
                "ตรวจสอบ compliance"
            ]
        },
        "COMPLETE": {
            "title": "เสร็จสมบูรณ์",
            "description": "ทุกขั้นตอนเสร็จสิ้นแล้ว",
            "time_estimate": "N/A",
            "what_it_does": []
        }
    }
    
    def __init__(self, ai_specs_dir: str):
        self.ai_specs_dir = Path(ai_specs_dir)
        self.ai_specs_dir.mkdir(parents=True, exist_ok=True)
    
    def write_status(
        self,
        spec_id: str,
        current_step: str,
        command: str,
        completed_steps: list[str],
        errors: list[str] = None,
        platform: str = "kilo"
    ):
        """
        Write user-friendly status.md file.
        
        Args:
            spec_id: Spec ID (e.g., "spec-core-001-authentication")
            current_step: Current step (e.g., "IMPLEMENT")
            command: Command to run
            completed_steps: List of completed steps
            errors: List of errors (if any)
            platform: Platform name (kilo, antigravity, claude)
        """
        status_file = self.ai_specs_dir / "status.md"
        
        # Get step info
        step_info = self.STEP_INFO.get(current_step, {})
        
        # Build content
        content = self._build_status_content(
            spec_id=spec_id,
            current_step=current_step,
            step_info=step_info,
            command=command,
            completed_steps=completed_steps,
            errors=errors,
            platform=platform
        )
        
        # Write file
        with open(status_file, "w", encoding="utf-8") as f:
            f.write(content)
    
    def _build_status_content(
        self,
        spec_id: str,
        current_step: str,
        step_info: dict,
        command: str,
        completed_steps: list[str],
        errors: list[str],
        platform: str
    ) -> str:
        """Build status.md content"""
        
        # Header
        lines = [
            f"# 🎯 สถานะปัจจุบัน: {step_info.get('title', current_step)}",
            "",
            f"**Spec ID:** `{spec_id}`",
            f"**Platform:** {platform.title()}",
            f"**Last Updated:** {self._get_timestamp()}",
            "",
            "---",
            ""
        ]
        
        # Completed steps
        if completed_steps:
            lines.extend([
                "## ✅ ที่ทำเสร็จแล้ว",
                ""
            ])
            for step in self.STEP_INFO.keys():
                if step in completed_steps:
                    step_title = self.STEP_INFO[step]["title"]
                    lines.append(f"- [x] {step_title}")
                elif step == "COMPLETE":
                    continue
                else:
                    step_title = self.STEP_INFO[step]["title"]
                    lines.append(f"- [ ] {step_title}")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # Current step
        if current_step != "COMPLETE":
            lines.extend([
                f"## 🚀 ขั้นตอนถัดไป: {step_info.get('title', current_step)}",
                "",
                f"**คำอธิบาย:** {step_info.get('description', '')}",
                "",
                "### คำสั่งที่ต้องรัน",
                "",
                "```bash",
                command,
                "```",
                "",
                "### 📝 คำสั่งนี้จะทำอะไร",
                ""
            ])
            
            what_it_does = step_info.get("what_it_does", [])
            for item in what_it_does:
                lines.append(f"- {item}")
            
            lines.extend([
                "",
                f"### ⏱️ เวลาโดยประมาณ: {step_info.get('time_estimate', 'N/A')}",
                "",
                "### 🔄 หลังจากรันเสร็จ",
                "",
                "รันคำสั่งนี้อีกครั้งเพื่อดูขั้นตอนถัดไป:",
                "",
                "```bash",
                f"ss-autopilot run --spec-id {spec_id}",
                "```",
                ""
            ])
        else:
            lines.extend([
                "## 🎉 เสร็จสมบูรณ์!",
                "",
                "ทุกขั้นตอนเสร็จสิ้นแล้ว คุณสามารถ:",
                "",
                "- ✅ ตรวจสอบโค้ดที่สร้างขึ้น",
                "- ✅ รัน tests เพื่อ verify",
                "- ✅ Deploy ไปยัง production",
                "- ✅ เริ่ม spec ใหม่",
                ""
            ])
        
        # Errors (if any)
        if errors:
            lines.extend([
                "---",
                "",
                "## ❌ ปัญหาที่พบ",
                ""
            ])
            for error in errors:
                lines.append(f"- {error}")
            lines.append("")
        
        # Troubleshooting
        if current_step != "COMPLETE":
            lines.extend([
                "---",
                "",
                "## ❓ ถ้ามีปัญหา",
                "",
                "### Workflow ไม่ทำงาน",
                "- ตรวจสอบว่า SmartSpec ถูก install แล้ว",
                "- ตรวจสอบว่าอยู่ใน project directory ที่ถูกต้อง",
                "- ตรวจสอบว่ามี `.smartspec/` directory",
                "",
                "### Workflow fail",
                f"- ดู error message ใน `.spec/reports/{current_step.lower()}/{spec_id}/`",
                "- ตรวจสอบ logs",
                "- ถาม AI หรือ senior dev",
                "",
                "### ผลลัพธ์ไม่ถูกต้อง",
                "- รัน workflow อีกครั้ง",
                "- ตรวจสอบ input files",
                "- แก้ไข spec/plan/tasks ถ้าจำเป็น",
                ""
            ])
        
        # Footer
        lines.extend([
            "---",
            "",
            f"**Generated by:** SmartSpec Autopilot v1.0",
            f"**Platform:** {platform.title()}",
            ""
        ])
        
        return "\n".join(lines)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def write_complete_status(self, spec_id: str, platform: str = "kilo"):
        """Write status for completed spec"""
        self.write_status(
            spec_id=spec_id,
            current_step="COMPLETE",
            command="",
            completed_steps=["SPEC", "PLAN", "TASKS", "IMPLEMENT", "SYNC_TASKS", "TEST_SUITE", "QUALITY_GATE"],
            errors=[],
            platform=platform
        )

    
    def write_status_with_progress(
        self,
        spec_id: str,
        current_step: str,
        command: str,
        completed_steps: list[str],
        errors: list[str],
        platform: str,
        # New parameters for progress
        tasks_total: int = 0,
        tasks_completed: int = 0,
        tasks_completion_rate: float = 0.0,
        needs_sync: bool = False,
        recommendation: Dict[str, Any] = None
    ):
        """
        Write status.md with progress information.
        
        This enhanced version shows:
        - Progress bar
        - Completion rate
        - Recommendations
        - Warnings
        """
        from .tasks_parser import build_progress_bar
        
        # Get step info
        step_info = self.STEP_INFO.get(current_step, {})
        step_title = step_info.get("title", current_step)
        
        # Build progress section
        progress_section = ""
        if tasks_total > 0:
            progress_bar = build_progress_bar(tasks_completion_rate)
            tasks_pending = tasks_total - tasks_completed
            
            progress_section = f"""
## 📊 ความคืบหน้า

**Tasks ที่เสร็จแล้ว:** {tasks_completed} / {tasks_total} ({tasks_completion_rate:.0%})

```
{progress_bar}
```

**Tasks ที่เหลือ:** {tasks_pending} tasks
"""
        
        # Build recommendation section
        recommendation_section = ""
        if recommendation:
            warnings = recommendation.get("warnings", [])
            tips = recommendation.get("tips", [])
            
            if warnings or tips:
                recommendation_section = "\n### 💡 คำแนะนำ\n\n"
                
                if warnings:
                    recommendation_section += "**⚠️ คำเตือน:**\n"
                    for warning in warnings:
                        recommendation_section += f"- {warning}\n"
                    recommendation_section += "\n"
                
                if tips:
                    recommendation_section += "**✨ เคล็ดลับ:**\n"
                    for tip in tips:
                        recommendation_section += f"- {tip}\n"
        
        # Build sync recommendation
        sync_section = ""
        if needs_sync and current_step != "SYNC_TASKS":
            sync_section = f"""
### ⚠️ แนะนำให้ Sync ก่อน

ตรวจพบว่า tasks.md อาจไม่ตรงกับโค้ดจริง

**แนะนำ:** รัน sync_tasks_checkboxes ก่อน เพื่อให้ checkboxes ตรงกับโค้ดจริง

```bash
/smartspec_sync_tasks_checkboxes.md \\
  specs/{spec_id}/tasks.md \\
  --out .spec/reports/sync-tasks/{spec_id} \\
  --json \\
  --apply \\
  --platform {platform}
```

**คำสั่งนี้จะ:**
- ตรวจสอบโค้ดที่เขียนไปแล้ว
- อัปเดต checkboxes ให้ตรงกับโค้ดจริง
- สร้าง report บอกว่าอะไรเสร็จแล้ว อะไรยังไม่เสร็จ

หลังจาก sync เสร็จ รันคำสั่ง Autopilot อีกครั้ง:

```bash
ss-autopilot run --spec-id {spec_id}
```
"""
        
        # Build error section
        error_section = ""
        if errors:
            error_section = "\n## ❌ ข้อผิดพลาด\n\n"
            for error in errors:
                error_section += f"- {error}\n"
        
        # Build completed steps section
        completed_section = "## ✅ ที่ทำเสร็จแล้ว\n\n"
        if not completed_steps:
            completed_section += "ยังไม่มีขั้นตอนที่เสร็จ\n"
        else:
            for step in completed_steps:
                step_name = self.STEP_INFO.get(step, {}).get("title", step)
                if step == "IMPLEMENT" and tasks_total > 0:
                    completed_section += f"- [x] {step_name} (กำลังดำเนินการ {tasks_completion_rate:.0%})\n"
                else:
                    completed_section += f"- [x] {step_name}\n"
        
        # Build main content
        content = f"""# 🎯 สถานะปัจจุบัน: {step_title}

**Spec ID:** `{spec_id}`
**Platform:** {platform.title()}
**Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
{progress_section}
---

{completed_section}

---

## 🚀 ขั้นตอนถัดไป: {step_title}

**คำอธิบาย:** {step_info.get('description', 'ไม่มีคำอธิบาย')}

### คำสั่งที่ต้องรัน

```bash
{command}
```

### 📝 คำสั่งนี้จะทำอะไร

"""
        
        # Add what it does
        what_it_does = step_info.get("what_it_does", [])
        for item in what_it_does:
            content += f"- {item}\n"
        
        content += f"\n### ⏱️ เวลาโดยประมาณ\n\n{step_info.get('time_estimate', 'ไม่ทราบ')}\n"
        
        # Add recommendation
        content += recommendation_section
        
        # Add sync recommendation
        content += sync_section
        
        # Add errors
        content += error_section
        
        # Add footer
        content += f"""
---

## 🔄 หลังจากรันเสร็จ

รันคำสั่งนี้อีกครั้งเพื่อดูความคืบหน้า:

```bash
ss-autopilot run --spec-id {spec_id}
```

---

## ❓ ถ้ามีปัญหา

1. **ตรวจสอบ error message** ใน terminal
2. **ดู logs** ใน `.spec/reports/{current_step.lower().replace('_', '-')}/{spec_id}/`
3. **ถามใน Slack/Discord** หรือติดต่อทีมพัฒนา
4. **อ่านเอกสาร** ใน `.smartspec/` directory

---

*Generated by SmartSpec Autopilot v1.1*
"""
        
        # Write to file
        status_file = Path(self.ai_specs_dir) / "status.md"
        with open(status_file, "w", encoding='utf-8') as f:
            f.write(content)
    
    
    def write_complete_status(self, spec_id: str, platform: str):
        """Write status when all steps are complete."""
        content = f"""# ✅ เสร็จสมบูรณ์!

**Spec ID:** `{spec_id}`
**Platform:** {platform.title()}
**Completed:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 🎉 ขั้นตอนทั้งหมดเสร็จสมบูรณ์แล้ว!

**ที่ทำเสร็จ:**

- [x] SPEC - สร้าง Specification
- [x] PLAN - สร้าง Implementation Plan
- [x] TASKS - สร้าง Task List
- [x] IMPLEMENT - เขียนโค้ดตาม Tasks
- [x] SYNC_TASKS - Sync Task Checkboxes
- [x] TEST_SUITE - รัน Test Suite (ถ้ามี)
- [x] QUALITY_GATE - Quality Gate Check (ถ้ามี)

---

## 🚀 ขั้นตอนถัดไป

1. **Review โค้ด** ที่เขียนไว้
2. **Test manually** เพื่อให้แน่ใจว่าทำงานถูกต้อง
3. **Commit และ Push** ไป Git repository
4. **Deploy** ไป staging/production (ถ้าพร้อม)

---

## 📁 ไฟล์ที่สร้างขึ้น

- `specs/{spec_id}/spec.md` - Specification
- `specs/{spec_id}/plan.md` - Implementation Plan
- `specs/{spec_id}/tasks.md` - Task List
- `.spec/reports/` - Reports จาก workflows

---

## 📊 สถิติ

รันคำสั่งนี้เพื่อดูสถิติ:

```bash
ss-autopilot status --spec-id {spec_id}
```

---

*Generated by SmartSpec Autopilot v1.1*
"""
        
        # Write to file
        status_file = Path(self.ai_specs_dir) / "status.md"
        with open(status_file, "w", encoding='utf-8') as f:
            f.write(content)
