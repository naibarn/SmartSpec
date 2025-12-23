#!/usr/bin/env python3
"""
SmartSpec Migrate Evidence Hooks
Converts descriptive evidence to standardized evidence hooks using AI
"""

import argparse
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

try:
    from openai import OpenAI
    client = OpenAI()  # API key from environment
except ImportError:
    print("Error: openai package not installed. Run: pip3 install openai")
    sys.exit(1)


class Task:
    """Represents a single task from tasks.md"""
    def __init__(self, task_id: str, title: str, description: str, evidence: str, original_text: str):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.evidence = evidence
        self.original_text = original_text
        self.suggested_hook: Optional[str] = None


def parse_tasks_file(file_path: Path) -> List[Task]:
    """Parse tasks.md file and extract all tasks"""
    content = file_path.read_text(encoding='utf-8')
    
    # Split by task separator
    task_blocks = re.split(r'\n-{80,}\n', content)
    
    tasks = []
    for block in task_blocks:
        if not block.strip():
            continue
            
        # Extract task ID, title, description, and evidence
        task_match = re.search(r'\|\s*(\S+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', block)
        if not task_match:
            continue
            
        task_id = task_match.group(1).strip()
        title = task_match.group(2).strip()
        description = task_match.group(3).strip()
        
        # Extract evidence
        evidence_match = re.search(r'\|\s*\*\*Evidence:\*\*\s*(.+?)\s*\|', block, re.DOTALL)
        evidence = evidence_match.group(1).strip() if evidence_match else ""
        
        tasks.append(Task(task_id, title, description, evidence, block))
    
    return tasks


def is_descriptive_evidence(evidence: str) -> bool:
    """Check if evidence is descriptive text rather than a standardized hook"""
    # If it already starts with "evidence:", it's already a hook
    if evidence.strip().startswith('evidence:'):
        return False
    
    # If it's empty, it's not descriptive
    if not evidence.strip():
        return False
    
    # If it contains natural language patterns, it's descriptive
    descriptive_patterns = [
        r'\bshould\b',
        r'\bmust\b',
        r'\bcheck\b',
        r'\bverify\b',
        r'\bensure\b',
        r'\bthe\s+\w+\s+file\b',
        r'\bin\s+the\b',
    ]
    
    for pattern in descriptive_patterns:
        if re.search(pattern, evidence, re.IGNORECASE):
            return True
    
    return False


def generate_evidence_hook(task: Task, model: str = "gpt-4.1-mini") -> str:
    """Use AI to generate a standardized evidence hook from descriptive text"""
    
    prompt = f"""You are an expert at converting natural language evidence descriptions into standardized evidence hooks.

TASK:
ID: {task.task_id}
Title: {task.title}
Description: {task.description}

CURRENT EVIDENCE (descriptive):
{task.evidence}

EVIDENCE HOOK FORMATS:
- evidence: file_exists path=<path>
- evidence: file_contains path=<path> content=<text>
- evidence: api_route method=<GET|POST|PUT|DELETE> path=<route>
- evidence: db_schema table=<table_name>
- evidence: gh_commit repo=<repo> sha=<commit_sha>
- evidence: test_exists path=<test_file> name=<test_name>
- evidence: config_key file=<config_file> key=<key_name>

INSTRUCTIONS:
1. Analyze the descriptive evidence text
2. Determine the most appropriate evidence type
3. Extract the specific file paths, routes, or identifiers mentioned
4. Generate a single, concise evidence hook

RESPONSE FORMAT:
Return ONLY the evidence hook in this exact format:
evidence: <type> <key1>=<value1> <key2>=<value2>

Do not include any explanation, just the hook.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a precise code analysis assistant. Return only the requested format with no additional text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=100
        )
        
        hook = response.choices[0].message.content.strip()
        
        # Validate that it starts with "evidence:"
        if not hook.startswith('evidence:'):
            hook = f"evidence: {hook}"
        
        return hook
        
    except Exception as e:
        print(f"Warning: AI generation failed for {task.task_id}: {e}")
        return f"evidence: file_exists path=MANUAL_REVIEW_REQUIRED"


def preview_changes(tasks: List[Task], file_path: Path):
    """Show a diff-like preview of proposed changes"""
    print(f"\n{'='*80}")
    print(f"PREVIEW: Proposed changes for {file_path}")
    print(f"{'='*80}\n")
    
    changes_count = 0
    for task in tasks:
        if task.suggested_hook:
            changes_count += 1
            print(f"Task: {task.task_id} - {task.title}")
            print(f"{'─'*80}")
            print(f"- OLD: {task.evidence}")
            print(f"+ NEW: {task.suggested_hook}")
            print(f"{'─'*80}\n")
    
    print(f"\nTotal changes proposed: {changes_count}")
    print(f"Total tasks analyzed: {len(tasks)}")
    print(f"\nTo apply these changes, run with --apply flag")


def apply_changes(tasks: List[Task], file_path: Path):
    """Apply the changes to the tasks.md file"""
    content = file_path.read_text(encoding='utf-8')
    
    changes_count = 0
    for task in tasks:
        if task.suggested_hook:
            # Replace the evidence line
            old_pattern = re.escape(f"| **Evidence:** {task.evidence} |")
            new_line = f"| **Evidence:** {task.suggested_hook} |"
            
            content = re.sub(old_pattern, new_line, content)
            changes_count += 1
    
    # Write back to file
    file_path.write_text(content, encoding='utf-8')
    
    print(f"\n✅ Applied {changes_count} changes to {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Migrate descriptive evidence to standardized evidence hooks"
    )
    parser.add_argument(
        '--tasks-file',
        type=str,
        required=True,
        help='Path to the tasks.md file'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes directly to the file (default: preview only)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4.1-mini',
        help='AI model to use for conversion (default: gpt-4.1-mini)'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    file_path = Path(args.tasks_file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    print(f"📖 Reading tasks from: {file_path}")
    
    # Parse tasks
    tasks = parse_tasks_file(file_path)
    print(f"Found {len(tasks)} tasks")
    
    # Identify tasks with descriptive evidence
    tasks_to_migrate = [t for t in tasks if is_descriptive_evidence(t.evidence)]
    print(f"Found {len(tasks_to_migrate)} tasks with descriptive evidence")
    
    if not tasks_to_migrate:
        print("\n✅ No tasks need migration. All evidence is already standardized!")
        return
    
    # Generate hooks using AI
    print(f"\n🤖 Generating evidence hooks using {args.model}...")
    for i, task in enumerate(tasks_to_migrate, 1):
        print(f"  [{i}/{len(tasks_to_migrate)}] Processing {task.task_id}...", end='', flush=True)
        task.suggested_hook = generate_evidence_hook(task, args.model)
        print(" ✓")
        time.sleep(0.5)  # Rate limiting
    
    # Preview or apply
    if args.apply:
        print(f"\n⚠️  APPLYING CHANGES in 5 seconds... (Ctrl+C to cancel)")
        for i in range(5, 0, -1):
            print(f"  {i}...", flush=True)
            time.sleep(1)
        
        apply_changes(tasks_to_migrate, file_path)
    else:
        preview_changes(tasks_to_migrate, file_path)


if __name__ == '__main__':
    main()
