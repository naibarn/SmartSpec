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
import re

from .security import (
    sanitize_spec_id,
    sanitize_query,
    validate_tasks_path,
    InvalidInputError,
    PathTraversalError
)
from .error_handler import (
    safe_file_read,
    with_error_handling,
    FileNotFoundError,
    SpecNotFoundError,
    ParseError,
    get_user_friendly_error
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
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


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
        """Initialize Status Agent"""
        self.specs_dir = Path("specs")
        self.reports_dir = Path(".spec/reports")
    
    @with_error_handling
    def query(self, spec_id: str, question: str = "") -> StatusResponse:
        """
        Answer status question with comprehensive error handling.
        
        Args:
            spec_id: Spec ID (e.g., "spec-core-001-authentication")
            question: Optional specific question
        
        Returns:
            StatusResponse with all relevant information or error dict
            
        Raises:
            InvalidInputError: If spec_id or question is invalid
            SpecNotFoundError: If spec does not exist
        """
        errors = []
        warnings = []
        
        try:
            # Sanitize inputs
            try:
                spec_id = sanitize_spec_id(spec_id)
            except Exception as e:
                raise InvalidInputError(
                    input_name="spec_id",
                    input_value=spec_id,
                    reason=str(e)
                )
            
            if question:
                try:
                    question = sanitize_query(question)
                except Exception as e:
                    warnings.append(f"Could not sanitize question: {str(e)}")
                    question = ""  # Fallback to default
            
            # Parse tasks.md
            tasks_file = self.specs_dir / spec_id / "tasks.md"
            
            # Validate path to prevent traversal
            try:
                tasks_file = validate_tasks_path(str(tasks_file), ".")
            except PathTraversalError as e:
                raise e
            except Exception as e:
                raise PathTraversalError(
                    path=str(tasks_file),
                    reason=str(e)
                )
            
            # Parse tasks with error handling
            try:
                tasks_info = self._parse_tasks(tasks_file)
            except Exception as e:
                errors.append(f"Failed to parse tasks: {str(e)}")
                # Return default tasks_info
                tasks_info = {
                    "total": 0,
                    "completed": 0,
                    "pending": 0,
                    "completion_rate": 0.0,
                    "tasks": []
                }
            
            # Get pending tasks
            try:
                pending_tasks = [t for t in tasks_info["tasks"] if not t["completed"]]
            except Exception as e:
                errors.append(f"Failed to get pending tasks: {str(e)}")
                pending_tasks = []
            
            # Build progress bar
            try:
                progress_bar = self._build_progress_bar(tasks_info["completion_rate"])
            except Exception as e:
                errors.append(f"Failed to build progress bar: {str(e)}")
                progress_bar = "░" * 20 + " 0%"
            
            # Determine next steps
            try:
                next_steps = self._determine_next_steps(spec_id, tasks_info)
            except Exception as e:
                errors.append(f"Failed to determine next steps: {str(e)}")
                next_steps = ["ไม่สามารถกำหนดขั้นตอนถัดไปได้"]
            
            # Estimate remaining time
            try:
                estimated_time = self._estimate_time(tasks_info)
            except Exception as e:
                errors.append(f"Failed to estimate time: {str(e)}")
                estimated_time = "ไม่ทราบ"
            
            # Check for warnings
            try:
                spec_warnings = self._check_warnings(spec_id, tasks_info)
                warnings.extend(spec_warnings)
            except Exception as e:
                errors.append(f"Failed to check warnings: {str(e)}")
            
            # Build answer based on question
            try:
                answer = self._build_answer(question, spec_id, tasks_info, next_steps)
            except Exception as e:
                errors.append(f"Failed to build answer: {str(e)}")
                answer = f"{tasks_info['completed']} / {tasks_info['total']} tasks เสร็จแล้ว"
            
            return StatusResponse(
                answer=answer,
                progress_bar=progress_bar,
                tasks_completed=tasks_info["completed"],
                tasks_total=tasks_info["total"],
                completion_rate=tasks_info["completion_rate"],
                pending_tasks=pending_tasks,
                next_steps=next_steps,
                estimated_time=estimated_time,
                warnings=warnings,
                errors=errors
            )
        
        except (InvalidInputError, SpecNotFoundError, PathTraversalError) as e:
            # Re-raise known errors
            raise e
        
        except Exception as e:
            # Catch unexpected errors
            raise RuntimeError(f"Unexpected error in query: {str(e)}")
    
    def _parse_tasks(self, tasks_file: Path) -> Dict[str, Any]:
        """
        Parse tasks.md file with error handling.
        
        Args:
            tasks_file: Path to tasks.md
            
        Returns:
            Dict with task information
            
        Raises:
            FileNotFoundError: If tasks file doesn't exist
            ParseError: If parsing fails
        """
        if not tasks_file.exists():
            return {
                "total": 0,
                "completed": 0,
                "pending": 0,
                "completion_rate": 0.0,
                "tasks": []
            }
        
        try:
            # Read file safely
            result = safe_file_read(str(tasks_file))
            
            if result.get("error"):
                raise ParseError(
                    file_path=str(tasks_file),
                    reason=result.get("message", "Unknown error")
                )
            
            content = result["content"]
            
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
        
        except ParseError:
            raise
        
        except Exception as e:
            raise ParseError(
                file_path=str(tasks_file),
                reason=f"Unexpected error: {str(e)}"
            )
    
    def _build_progress_bar(self, completion_rate: float, width: int = 20) -> str:
        """
        Build ASCII progress bar with error handling.
        
        Args:
            completion_rate: Completion rate (0.0 to 1.0)
            width: Width of progress bar
            
        Returns:
            Progress bar string
        """
        try:
            # Clamp completion_rate to [0, 1]
            completion_rate = max(0.0, min(1.0, completion_rate))
            
            filled = int(completion_rate * width)
            empty = width - filled
            return "█" * filled + "░" * empty + f" {completion_rate:.0%}"
        
        except Exception:
            # Fallback to empty progress bar
            return "░" * width + " 0%"
    
    def _determine_next_steps(self, spec_id: str, tasks_info: Dict[str, Any]) -> List[str]:
        """
        Determine next steps with error handling.
        
        Args:
            spec_id: Spec ID
            tasks_info: Task information dict
            
        Returns:
            List of next steps
        """
        try:
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
        
        except Exception:
            return ["ไม่สามารถกำหนดขั้นตอนถัดไปได้"]
    
    def _estimate_time(self, tasks_info: Dict[str, Any]) -> str:
        """
        Estimate remaining time with error handling.
        
        Args:
            tasks_info: Task information dict
            
        Returns:
            Estimated time string
        """
        try:
            if tasks_info["pending"] == 0:
                return "0 นาที (เสร็จแล้ว)"
            
            # Assume 20 minutes per task
            minutes = tasks_info["pending"] * 20
            
            if minutes < 60:
                return f"{minutes} นาที"
            else:
                hours = minutes / 60
                return f"{hours:.1f} ชั่วโมง"
        
        except Exception:
            return "ไม่ทราบ"
    
    def _check_warnings(self, spec_id: str, tasks_info: Dict[str, Any]) -> List[str]:
        """
        Check for warnings with error handling.
        
        Args:
            spec_id: Spec ID
            tasks_info: Task information dict
            
        Returns:
            List of warnings
        """
        warnings = []
        
        try:
            # Check if implementation report exists but completion rate is low
            implement_report = self.reports_dir / "implement-tasks" / spec_id / "summary.json"
            if implement_report.exists() and tasks_info["completion_rate"] < 1.0:
                warnings.append("มี implementation report แต่ tasks ยังไม่เสร็จ - อาจต้อง sync checkboxes")
        except Exception:
            pass  # Ignore errors in warning checks
        
        try:
            # Check if completion rate is high but not 100%
            if 0.8 <= tasks_info["completion_rate"] < 1.0:
                warnings.append("ใกล้เสร็จแล้ว - แนะนำให้ sync checkboxes ก่อนทำ tasks สุดท้าย")
        except Exception:
            pass  # Ignore errors in warning checks
        
        return warnings
    
    def _build_answer(self, question: str, spec_id: str, tasks_info: Dict[str, Any], next_steps: List[str]) -> str:
        """
        Build answer based on question with error handling.
        
        Args:
            question: User question
            spec_id: Spec ID
            tasks_info: Task information dict
            next_steps: List of next steps
            
        Returns:
            Answer string
        """
        try:
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
        
        except Exception:
            # Fallback answer
            return f"{tasks_info.get('completed', 0)} / {tasks_info.get('total', 0)} tasks เสร็จแล้ว"
    
    def format_response(self, response: StatusResponse) -> str:
        """
        Format response as human-readable text with error handling.
        
        Args:
            response: StatusResponse object
            
        Returns:
            Formatted response string
        """
        try:
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
            
            if response.errors:
                lines.append(f"## ❌ ข้อผิดพลาด")
                lines.append(f"")
                for error in response.errors:
                    lines.append(f"- {error}")
                lines.append(f"")
            
            if response.warnings:
                lines.append(f"## ⚠️ คำเตือน")
                lines.append(f"")
                for warning in response.warnings:
                    lines.append(f"- {warning}")
                lines.append(f"")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"Error formatting response: {str(e)}"


# Example usage
if __name__ == "__main__":
    try:
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
                response_result = agent.query(spec_id, question)
                
                # Check if result is an error
                if isinstance(response_result, dict) and response_result.get("error"):
                    print(f"Error: {get_user_friendly_error(response_result)}")
                else:
                    # Extract response
                    if isinstance(response_result, dict) and response_result.get("success"):
                        response = response_result["result"]
                    else:
                        response = response_result
                    
                    print(agent.format_response(response))
            
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
            
            print()
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
