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


def parse_tasks_file(tasks_file: Path) -> Dict[str, Any]:
    """
    Parse tasks.md to count completed/pending tasks.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
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
            ]
        }
    """
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
    
    # Find all checkboxes
    # Pattern for completed: - [x] or - [X]
    completed_pattern = r'^\s*-\s*\[x\](.+?)$'
    # Pattern for pending: - [ ]
    pending_pattern = r'^\s*-\s*\[\s\](.+?)$'
    
    completed_matches = re.findall(completed_pattern, content, re.IGNORECASE | re.MULTILINE)
    pending_matches = re.findall(pending_pattern, content, re.MULTILINE)
    
    completed = len(completed_matches)
    pending = len(pending_matches)
    total = completed + pending
    
    # Build task list
    tasks = []
    task_id = 1
    
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
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": completed / total if total > 0 else 0.0,
        "tasks": tasks
    }


def get_pending_tasks(tasks_file: Path) -> List[Dict[str, Any]]:
    """
    Get list of pending tasks.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        List of pending tasks:
        [
            {"id": 3, "title": "Logout API", "completed": False},
            ...
        ]
    """
    info = parse_tasks_file(tasks_file)
    return [t for t in info["tasks"] if not t["completed"]]


def get_completed_tasks(tasks_file: Path) -> List[Dict[str, Any]]:
    """
    Get list of completed tasks.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        List of completed tasks:
        [
            {"id": 1, "title": "Login API", "completed": True},
            ...
        ]
    """
    info = parse_tasks_file(tasks_file)
    return [t for t in info["tasks"] if t["completed"]]


def get_completion_summary(tasks_file: Path) -> str:
    """
    Get human-readable completion summary.
    
    Args:
        tasks_file: Path to tasks.md
    
    Returns:
        Summary string like "5 / 12 tasks completed (42%)"
    """
    info = parse_tasks_file(tasks_file)
    
    if info["total"] == 0:
        return "No tasks found"
    
    return f"{info['completed']} / {info['total']} tasks completed ({info['completion_rate']:.0%})"


def build_progress_bar(completion_rate: float, width: int = 20) -> str:
    """
    Build ASCII progress bar.
    
    Args:
        completion_rate: Completion rate (0.0 to 1.0)
        width: Width of progress bar in characters
    
    Returns:
        Progress bar string like "████████░░░░░░░░░░░░ 42%"
    """
    filled = int(completion_rate * width)
    empty = width - filled
    return "█" * filled + "░" * empty + f" {completion_rate:.0%}"


# Example usage
if __name__ == "__main__":
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
        info = parse_tasks_file(temp_file)
        
        print("Tasks Info:")
        print(f"  Total: {info['total']}")
        print(f"  Completed: {info['completed']}")
        print(f"  Pending: {info['pending']}")
        print(f"  Completion Rate: {info['completion_rate']:.0%}")
        print()
        
        print("Progress Bar:")
        print(f"  {build_progress_bar(info['completion_rate'])}")
        print()
        
        print("Summary:")
        print(f"  {get_completion_summary(temp_file)}")
        print()
        
        print("Completed Tasks:")
        for task in get_completed_tasks(temp_file):
            print(f"  ✅ {task['title']}")
        print()
        
        print("Pending Tasks:")
        for task in get_pending_tasks(temp_file):
            print(f"  ⏳ {task['title']}")
    
    finally:
        # Clean up
        temp_file.unlink()
