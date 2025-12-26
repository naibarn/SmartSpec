"""
Parse tasks.md to extract task information.

This module provides functions to parse tasks.md files and extract:
- Total number of tasks
- Number of completed tasks
- Number of pending tasks
- Completion rate
- List of tasks with their status
"""

import re
from pathlib import Path
from typing import Dict, List, Any

from .error_handler import (
    safe_file_read,
    with_error_handling,
    FileNotFoundError,
    ParseError
)


@with_error_handling
def parse_tasks_file(tasks_file: Path) -> Dict[str, Any]:
    """
    Parse tasks.md to count completed/pending tasks with error handling.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        Dict with task information or error dict:
        {
            "total": 12,
            "completed": 5,
            "pending": 7,
            "completion_rate": 0.42,
            "tasks": [
                {"id": 1, "title": "Login API", "completed": True},
                {"id": 2, "title": "Register API", "completed": True},
                {"id": 3, "title": "Logout API", "completed": False},
                ...
            ],
            "errors": []
        }
    """
    errors = []
    
    # Default return value
    default_result = {
        "total": 0,
        "completed": 0,
        "pending": 0,
        "completion_rate": 0.0,
        "tasks": [],
        "errors": errors
    }
    
    try:
        # Check if file exists
        if not tasks_file.exists():
            errors.append(f"Tasks file not found: {tasks_file}")
            return default_result
        
        # Read file safely
        result = safe_file_read(str(tasks_file))
        
        if result.get("error"):
            raise ParseError(
                file_path=str(tasks_file),
                reason=result.get("message", "Unknown error")
            )
        
        content = result["content"]
        
        # Find all checkboxes
        # Pattern for completed: - [x] or - [X]
        completed_pattern = r'^\s*-\s*\[x\](.+?)$'
        # Pattern for pending: - [ ]
        pending_pattern = r'^\s*-\s*\[\s\](.+?)$'
        
        try:
            completed_matches = re.findall(completed_pattern, content, re.IGNORECASE | re.MULTILINE)
            pending_matches = re.findall(pending_pattern, content, re.MULTILINE)
        except Exception as e:
            raise ParseError(
                file_path=str(tasks_file),
                reason=f"Regex matching failed: {str(e)}"
            )
        
        completed = len(completed_matches)
        pending = len(pending_matches)
        total = completed + pending
        
        # Build task list
        tasks = []
        task_id = 1
        
        try:
            # Add completed tasks
            for match in completed_matches:
                tasks.append({
                    "id": task_id,
                    "title": match.strip(),
                    "completed": True
                })
                task_id += 1
            
            # Add pending tasks
            for match in pending_matches:
                tasks.append({
                    "id": task_id,
                    "title": match.strip(),
                    "completed": False
                })
                task_id += 1
        
        except Exception as e:
            errors.append(f"Failed to build task list: {str(e)}")
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": completed / total if total > 0 else 0.0,
            "tasks": tasks,
            "errors": errors
        }
    
    except ParseError:
        raise
    
    except Exception as e:
        raise ParseError(
            file_path=str(tasks_file),
            reason=f"Unexpected error: {str(e)}"
        )


@with_error_handling
def get_pending_tasks(tasks_file: Path) -> List[Dict[str, Any]]:
    """
    Get list of pending tasks with error handling.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        List of pending tasks or error dict:
        [
            {"id": 3, "title": "Logout API", "completed": False},
            ...
        ]
    """
    try:
        info_result = parse_tasks_file(tasks_file)
        
        # Check if result is an error
        if isinstance(info_result, dict) and info_result.get("error"):
            return []
        
        # Extract info from result
        if isinstance(info_result, dict) and info_result.get("success"):
            info = info_result["result"]
        else:
            info = info_result
        
        return [t for t in info.get("tasks", []) if not t.get("completed", True)]
    
    except Exception:
        return []


@with_error_handling
def get_completed_tasks(tasks_file: Path) -> List[Dict[str, Any]]:
    """
    Get list of completed tasks with error handling.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        List of completed tasks or error dict:
        [
            {"id": 1, "title": "Login API", "completed": True},
            ...
        ]
    """
    try:
        info_result = parse_tasks_file(tasks_file)
        
        # Check if result is an error
        if isinstance(info_result, dict) and info_result.get("error"):
            return []
        
        # Extract info from result
        if isinstance(info_result, dict) and info_result.get("success"):
            info = info_result["result"]
        else:
            info = info_result
        
        return [t for t in info.get("tasks", []) if t.get("completed", False)]
    
    except Exception:
        return []


@with_error_handling
def get_completion_summary(tasks_file: Path) -> str:
    """
    Get human-readable completion summary with error handling.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        Summary string like "5 / 12 tasks completed (42%)" or error dict
    """
    try:
        info_result = parse_tasks_file(tasks_file)
        
        # Check if result is an error
        if isinstance(info_result, dict) and info_result.get("error"):
            return "Error: Could not parse tasks file"
        
        # Extract info from result
        if isinstance(info_result, dict) and info_result.get("success"):
            info = info_result["result"]
        else:
            info = info_result
        
        if info.get("total", 0) == 0:
            return "No tasks found"
        
        return f"{info['completed']} / {info['total']} tasks completed ({info['completion_rate']:.0%})"
    
    except Exception:
        return "Error: Could not generate summary"


def build_progress_bar(completion_rate: float, width: int = 20) -> str:
    """
    Build ASCII progress bar with error handling.
    
    Args:
        completion_rate: Completion rate (0.0 to 1.0)
        width: Width of progress bar in characters
    
    Returns:
        Progress bar string like "████████░░░░░░░░░░░░ 42%"
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


# Example usage
if __name__ == "__main__":
    try:
        # Test with example tasks.md
        example_content = """
# Tasks

## Phase 1: Authentication

- [x] Task 1: Implement login API
- [x] Task 2: Implement register API
- [ ] Task 3: Implement logout API
- [ ] Task 4: Implement password reset

## Phase 2: User Management

- [x] Task 5: Get user profile
- [ ] Task 6: Update user profile
- [ ] Task 7: Delete user account
"""
        
        # Create temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(example_content)
            temp_file = Path(f.name)
        
        try:
            # Parse
            info_result = parse_tasks_file(temp_file)
            
            # Check if result is an error
            if isinstance(info_result, dict) and info_result.get("error"):
                print(f"Error: {info_result.get('message')}")
            else:
                # Extract info from result
                if isinstance(info_result, dict) and info_result.get("success"):
                    info = info_result["result"]
                else:
                    info = info_result
                
                print("Tasks Info:")
                print(f"  Total: {info['total']}")
                print(f"  Completed: {info['completed']}")
                print(f"  Pending: {info['pending']}")
                print(f"  Completion Rate: {info['completion_rate']:.0%}")
                
                if info.get('errors'):
                    print(f"  Errors: {len(info['errors'])}")
                    for error in info['errors']:
                        print(f"    - {error}")
                
                print()
                
                print("Progress Bar:")
                print(f"  {build_progress_bar(info['completion_rate'])}")
                print()
                
                print("Summary:")
                summary_result = get_completion_summary(temp_file)
                if isinstance(summary_result, dict) and summary_result.get("success"):
                    summary = summary_result["result"]
                else:
                    summary = summary_result
                print(f"  {summary}")
                print()
                
                print("Completed Tasks:")
                completed_result = get_completed_tasks(temp_file)
                if isinstance(completed_result, dict) and completed_result.get("success"):
                    completed_tasks = completed_result["result"]
                else:
                    completed_tasks = completed_result
                
                for task in completed_tasks:
                    print(f"  ✅ {task['title']}")
                print()
                
                print("Pending Tasks:")
                pending_result = get_pending_tasks(temp_file)
                if isinstance(pending_result, dict) and pending_result.get("success"):
                    pending_tasks = pending_result["result"]
                else:
                    pending_tasks = pending_result
                
                for task in pending_tasks:
                    print(f"  ⏳ {task['title']}")
        
        finally:
            # Clean up
            temp_file.unlink()
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
