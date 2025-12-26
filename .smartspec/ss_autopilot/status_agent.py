"""
Status Agent - Answer progress and status questions.

This agent answers questions like:
- "งานถึงไหนแล้ว?"
- "เหลืออะไรบ้าง?"
- "ต้องทำอะไรต่อ?"
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from .security import (
    sanitize_spec_id,
    sanitize_query,
    validate_tasks_path,
    InvalidInputError,
    PathTraversalError
)


@dataclass
class StatusResponse:
    """Response from Status Agent"""
    answer: str
    progress_bar: str
    tasks_completed: int
    tasks_total: int
    completion_rate: float
    pending_tasks: List[Dict[str, Any]]
    next_steps: List[str]
    estimated_time: str
    warnings: List[str]


class StatusAgent:
    """
    Status Agent - Answer progress questions.
    
    Capabilities:
    - Parse tasks.md to count progress
    - Check implementation reports
    - Analyze test results
    - Generate progress summaries
    - Recommend next steps
    """
    
    def __init__(self):
        self.specs_dir = Path("specs")
        self.reports_dir = Path(".spec/reports")
    
    def query(self, spec_id: str, question: str = "") -> StatusResponse:
        """
        Answer status question.
        
        Args:
            spec_id: Spec ID (e.g., "spec-core-001-authentication")
            question: Optional specific question
        
        Returns:
            StatusResponse with all relevant information
            
        Raises:
            InvalidInputError: If spec_id or question is invalid
            PathTraversalError: If path is outside project
        """
        # Sanitize inputs
        spec_id = sanitize_spec_id(spec_id)
        if question:
            question = sanitize_query(question)
        
        # Parse tasks.md
        tasks_file = self.specs_dir / spec_id / "tasks.md"
        # Validate path to prevent traversal
        tasks_file = validate_tasks_path(str(tasks_file), ".")
        tasks_info = self._parse_tasks(tasks_file)
        
        # Get pending tasks
        pending_tasks = [t for t in tasks_info["tasks"] if not t["completed"]]
        
        # Build progress bar
        progress_bar = self._build_progress_bar(tasks_info["completion_rate"])
        
        # Determine next steps
        next_steps = self._determine_next_steps(spec_id, tasks_info)
        
        # Estimate remaining time
        estimated_time = self._estimate_time(tasks_info)
        
        # Check for warnings
        warnings = self._check_warnings(spec_id, tasks_info)
        
        # Build answer based on question
        answer = self._build_answer(question, spec_id, tasks_info, next_steps)
        
        return StatusResponse(
            answer=answer,
            progress_bar=progress_bar,
            tasks_completed=tasks_info["completed"],
            tasks_total=tasks_info["total"],
            completion_rate=tasks_info["completion_rate"],
            pending_tasks=pending_tasks,
            next_steps=next_steps,
            estimated_time=estimated_time,
            warnings=warnings
        )
    
    def _parse_tasks(self, tasks_file: Path) -> Dict[str, Any]:
        """Parse tasks.md file"""
        if not tasks_file.exists():
            return {
                "total": 0,
                "completed": 0,
                "pending": 0,
                "completion_rate": 0.0,
                "tasks": []
            }
        
        with open(tasks_file, encoding='utf-8') as f:
            content = f.read()
        
        import re
        
        # Find all checkboxes
        completed_pattern = r'^\s*-\s*\[x\](.+?)$'
        pending_pattern = r'^\s*-\s*\[\s\](.+?)$'
        
        completed_matches = re.findall(completed_pattern, content, re.IGNORECASE | re.MULTILINE)
        pending_matches = re.findall(pending_pattern, content, re.MULTILINE)
        
        completed = len(completed_matches)
        pending = len(pending_matches)
        total = completed + pending
        
        # Build task list
        tasks = []
        task_id = 1
        
        for match in completed_matches:
            tasks.append({
                "id": task_id,
                "title": match.strip(),
                "completed": True
            })
            task_id += 1
        
        for match in pending_matches:
            tasks.append({
                "id": task_id,
                "title": match.strip(),
                "completed": False
            })
            task_id += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completed / total if total > 0 else 0.0,
            "tasks": tasks
        }
    
    def _build_progress_bar(self, completion_rate: float, width: int = 20) -> str:
        """Build ASCII progress bar"""
        filled = int(completion_rate * width)
        empty = width - filled
        return "█" * filled + "░" * empty + f" {completion_rate:.0%}"
    
    def _determine_next_steps(self, spec_id: str, tasks_info: Dict[str, Any]) -> List[str]:
        """Determine next steps"""
        steps = []
        
        if tasks_info["total"] == 0:
            steps.append("สร้าง tasks.md ก่อน")
            return steps
        
        if tasks_info["completed"] == 0:
            steps.append("เริ่มทำ tasks แรก")
        elif tasks_info["completed"] < tasks_info["total"]:
            steps.append(f"ทำ tasks ที่เหลืออีก {tasks_info['pending']} tasks")
            
            if tasks_info["completion_rate"] >= 0.5:
                steps.append("แนะนำให้ sync checkboxes ก่อนทำต่อ")
        else:
            steps.append("Tasks เสร็จหมดแล้ว")
            steps.append("ขั้นตอนถัดไป: สร้าง tests")
        
        return steps
    
    def _estimate_time(self, tasks_info: Dict[str, Any]) -> str:
        """Estimate remaining time"""
        if tasks_info["pending"] == 0:
            return "0 นาที (เสร็จแล้ว)"
        
        # Assume 20 minutes per task
        minutes = tasks_info["pending"] * 20
        
        if minutes < 60:
            return f"{minutes} นาที"
        else:
            hours = minutes / 60
            return f"{hours:.1f} ชั่วโมง"
    
    def _check_warnings(self, spec_id: str, tasks_info: Dict[str, Any]) -> List[str]:
        """Check for warnings"""
        warnings = []
        
        # Check if implementation report exists but completion rate is low
        implement_report = self.reports_dir / "implement-tasks" / spec_id / "summary.json"
        if implement_report.exists() and tasks_info["completion_rate"] < 1.0:
            warnings.append("มี implementation report แต่ tasks ยังไม่เสร็จ - อาจต้อง sync checkboxes")
        
        # Check if completion rate is high but not 100%
        if 0.8 <= tasks_info["completion_rate"] < 1.0:
            warnings.append("ใกล้เสร็จแล้ว - แนะนำให้ sync checkboxes ก่อนทำ tasks สุดท้าย")
        
        return warnings
    
    def _build_answer(self, question: str, spec_id: str, tasks_info: Dict[str, Any], next_steps: List[str]) -> str:
        """Build answer based on question"""
        question_lower = question.lower()
        
        # "งานถึงไหนแล้ว?" or "progress?"
        if "ถึงไหน" in question_lower or "progress" in question_lower or not question:
            return f"{tasks_info['completed']} / {tasks_info['total']} tasks เสร็จแล้ว ({tasks_info['completion_rate']:.0%})"
        
        # "เหลืออะไรบ้าง?" or "what's left?"
        elif "เหลือ" in question_lower or "left" in question_lower or "remaining" in question_lower:
            if tasks_info["pending"] == 0:
                return "ไม่เหลืออะไรแล้ว - เสร็จหมดแล้ว!"
            else:
                return f"เหลืออีก {tasks_info['pending']} tasks"
        
        # "ต้องทำอะไรต่อ?" or "what's next?"
        elif "ทำอะไรต่อ" in question_lower or "next" in question_lower:
            return " → ".join(next_steps)
        
        # "มีปัญหาไหม?" or "any issues?"
        elif "ปัญหา" in question_lower or "issue" in question_lower or "error" in question_lower:
            warnings = self._check_warnings(spec_id, tasks_info)
            if warnings:
                return f"พบ {len(warnings)} ปัญหา: " + "; ".join(warnings)
            else:
                return "ไม่มีปัญหา"
        
        # "เมื่อไหร่เสร็จ?" or "when done?"
        elif "เมื่อไหร่" in question_lower or "when" in question_lower or "eta" in question_lower:
            estimated_time = self._estimate_time(tasks_info)
            return f"คาดว่าจะเสร็จใน {estimated_time}"
        
        # Default
        else:
            return f"{tasks_info['completed']} / {tasks_info['total']} tasks เสร็จแล้ว ({tasks_info['completion_rate']:.0%})"
    
    def format_response(self, response: StatusResponse) -> str:
        """Format response as human-readable text"""
        lines = [
            f"# สถานะ",
            f"",
            f"## ความคืบหน้า",
            f"",
            f"**Tasks ที่เสร็จแล้ว:** {response.tasks_completed} / {response.tasks_total} ({response.completion_rate:.0%})",
            f"",
            f"```",
            f"{response.progress_bar}",
            f"```",
            f"",
            f"**คำตอบ:** {response.answer}",
            f""
        ]
        
        if response.pending_tasks:
            lines.append(f"## Tasks ที่เหลือ")
            lines.append(f"")
            for task in response.pending_tasks[:5]:  # Show first 5
                lines.append(f"- {task['title']}")
            
            if len(response.pending_tasks) > 5:
                lines.append(f"- ... และอีก {len(response.pending_tasks) - 5} tasks")
            lines.append(f"")
        
        if response.next_steps:
            lines.append(f"## ขั้นตอนถัดไป")
            lines.append(f"")
            for i, step in enumerate(response.next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append(f"")
        
        if response.estimated_time:
            lines.append(f"## เวลาโดยประมาณ")
            lines.append(f"")
            lines.append(f"{response.estimated_time}")
            lines.append(f"")
        
        if response.warnings:
            lines.append(f"## ⚠️ คำเตือน")
            lines.append(f"")
            for warning in response.warnings:
                lines.append(f"- {warning}")
            lines.append(f"")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Create agent
    agent = StatusAgent()
    
    # Test with example spec
    spec_id = "spec-core-001-authentication"
    
    print(f"Status Agent Test")
    print("=" * 50)
    print()
    
    # Test different questions
    questions = [
        "",  # Default
        "งานถึงไหนแล้ว?",
        "เหลืออะไรบ้าง?",
        "ต้องทำอะไรต่อ?",
        "มีปัญหาไหม?",
        "เมื่อไหร่เสร็จ?"
    ]
    
    for question in questions:
        print(f"Question: {question if question else '(default)'}")
        print("-" * 50)
        
        try:
            response = agent.query(spec_id, question)
            print(agent.format_response(response))
        except Exception as e:
            print(f"Error: {e}")
        
        print()
