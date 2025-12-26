"""
Enhanced status writer for user-friendly ai_specs/status.md output.

This module generates human-readable status files that guide non-dev users
through the SmartSpec workflow process.
"""

from __future__ import annotations

from typing import Dict, Any
from pathlib import Path
from datetime import datetime

from .error_handler import safe_file_write, with_error_handling


class StatusWriter:
    """Write user-friendly status.md files"""
    
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
    
    def __init__(self, ai_specs_dir: str = "ai_specs"):
        """
        Initialize Status Writer.
        
        Args:
            ai_specs_dir: Path to ai_specs directory
        """
        self.ai_specs_dir = Path(ai_specs_dir)
        try:
            self.ai_specs_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass  # Ignore mkdir errors
    
    @with_error_handling
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
        Write user-friendly status.md file with error handling.
        
        Args:
            spec_id: Spec ID (e.g., "spec-core-001-authentication")
            current_step: Current step (e.g., "IMPLEMENT")
            command: Command to run
            completed_steps: List of completed steps
            errors: List of errors (if any)
            platform: Platform name (kilo, antigravity, claude)
            
        Returns:
            Success dict or error dict
        """
        try:
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
                errors=errors or [],
                platform=platform
            )
            
            # Write file safely
            result = safe_file_write(str(status_file), content)
            
            if result.get("error"):
                raise RuntimeError(f"Failed to write status file: {result.get('message')}")
            
            return {"success": True, "file": str(status_file)}
        
        except Exception as e:
            raise RuntimeError(f"Failed to write status: {str(e)}")
    
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
        """Build status.md content with error handling"""
        
        try:
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
        
        except Exception as e:
            # Return minimal content on error
            return f"""# ❌ Error

Failed to generate status: {str(e)}

**Spec ID:** {spec_id}
**Platform:** {platform}
"""
    
    def _get_timestamp(self) -> str:
        """Get current timestamp with error handling"""
        try:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return "Unknown"
    
    @with_error_handling
    def write_complete_status(self, spec_id: str, platform: str = "kilo"):
        """Write status for completed spec with error handling"""
        return self.write_status(
            spec_id=spec_id,
            current_step="COMPLETE",
            command="",
            completed_steps=["SPEC", "PLAN", "TASKS", "IMPLEMENT", "SYNC_TASKS", "TEST_SUITE", "QUALITY_GATE"],
            errors=[],
            platform=platform
        )
