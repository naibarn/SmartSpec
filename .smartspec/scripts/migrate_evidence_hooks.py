#!/usr/bin/env python3
"""
SmartSpec Migrate Evidence Hooks
Converts descriptive evidence to standardized evidence hooks using AI
"""

import argparse
import re
import sys
import time
import shutil
from pathlib import Path
from typing import List, Dict, Optional

try:
    from openai import OpenAI, RateLimitError
    client = OpenAI()  # API key from environment
except ImportError:
    print("Error: openai package not installed. Run: pip3 install openai")
    sys.exit(1)


class Task:
    """Represents a single task from tasks.md"""
    def __init__(self, task_id: str, title: str, description: str, evidence: str, original_text: str, block_index: int):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.evidence = evidence
        self.original_text = original_text
        self.block_index = block_index  # Track position in file
        self.suggested_hook: Optional[str] = None


def parse_tasks_file(file_path: Path) -> List[Task]:
    """Parse tasks.md file and extract all tasks"""
    content = file_path.read_text(encoding='utf-8')
    
    # More flexible separator pattern (70+ dashes instead of exactly 80)
    task_blocks = re.split(r'\n-{70,}\n', content)
    
    tasks = []
    for idx, block in enumerate(task_blocks):
        if not block.strip():
            continue
            
        # Extract task ID, title, description, and evidence
        task_match = re.search(r'\|\s*(\S+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|', block)
        if not task_match:
            continue
            
        task_id = task_match.group(1).strip()
        title = task_match.group(2).strip()
        description = task_match.group(3).strip()
        
        # Extract evidence (handle multi-line by collapsing whitespace)
        evidence_match = re.search(r'\|\s*\*\*Evidence:\*\*\s*(.+?)\s*\|', block, re.DOTALL)
        if evidence_match:
            evidence = evidence_match.group(1).strip()
            # Normalize multi-line evidence to single line
            evidence = ' '.join(evidence.split())
        else:
            evidence = ""
        
        tasks.append(Task(task_id, title, description, evidence, block, idx))
    
    return tasks


def is_descriptive_evidence(evidence: str) -> bool:
    """Check if evidence is descriptive text rather than a standardized hook"""
    # If it already starts with "evidence:", it's already a hook
    if evidence.strip().startswith('evidence:'):
        return False
    
    # If it's empty, it's not descriptive
    if not evidence.strip():
        return False
    
    # If it contains "TODO", it needs migration
    if 'TODO' in evidence.upper():
        return True
    
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


def validate_evidence_hook(hook: str) -> bool:
    """Validate that the hook follows the correct format"""
    if not hook.startswith('evidence:'):
        return False
    
    # Check for known types
    known_types = ['file_exists', 'file_contains', 'api_route', 'db_schema', 
                   'gh_commit', 'test_exists', 'config_key', 'code']
    
    parts = hook.split(maxsplit=2)
    if len(parts) < 3:
        return False
    
    hook_type = parts[1]
    if hook_type not in known_types:
        return False
    
    # Check for key=value format
    params = parts[2]
    if '=' not in params:
        return False
    
    return True


def generate_evidence_hook(task: Task, model: str = "gpt-4.1-mini", max_retries: int = 3) -> str:
    """Use AI to generate a standardized evidence hook from descriptive text with retry logic"""
    
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
- evidence: code path=<file_path> contains=<code_snippet>

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

    for attempt in range(max_retries):
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
            
            # Validate the hook format
            if not validate_evidence_hook(hook):
                print(f"\n⚠️  Warning: Invalid hook format for {task.task_id}: {hook}")
                return f"evidence: code path=INVALID_FORMAT_MANUAL_REVIEW_REQUIRED contains=check_task_{task.task_id}"
            
            return hook
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"\n⚠️  Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Rate limit exceeded for {task.task_id}")
                return f"evidence: code path=RATE_LIMIT_EXCEEDED_MANUAL_REVIEW_REQUIRED contains=check_task_{task.task_id}"
        except Exception as e:
            print(f"\n⚠️  Warning: AI generation failed for {task.task_id}: {e}")
            return f"evidence: code path=GENERATION_FAILED_MANUAL_REVIEW_REQUIRED contains=check_task_{task.task_id}"
    
    return f"evidence: code path=MAX_RETRIES_EXCEEDED_MANUAL_REVIEW_REQUIRED contains=check_task_{task.task_id}"


def preview_changes(tasks: List[Task], file_path: Path, all_tasks: List[Task]):
    """Show a diff-like preview of proposed changes with detailed statistics"""
    
    already_standardized = len([t for t in all_tasks if t.evidence.startswith('evidence:')])
    no_evidence = len([t for t in all_tasks if not t.evidence.strip()])
    failed_generation = len([t for t in tasks if t.suggested_hook and 'MANUAL_REVIEW' in t.suggested_hook])
    
    print(f"\n{'='*80}")
    print(f"STATISTICS for {file_path}")
    print(f"{'='*80}")
    print(f"Total tasks: {len(all_tasks)}")
    print(f"Already standardized: {already_standardized}")
    print(f"No evidence: {no_evidence}")
    print(f"Needs migration: {len(tasks)}")
    print(f"Failed AI generation: {failed_generation}")
    print(f"{'='*80}\n")
    
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
    print(f"\nTo apply these changes, run with --apply flag")


def apply_changes(tasks: List[Task], file_path: Path):
    """Apply the changes to the tasks.md file with backup"""
    
    # Create backup first
    backup_path = file_path.with_suffix('.md.backup')
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        changes_count = 0
        # Sort tasks by block_index in reverse order to avoid offset issues
        sorted_tasks = sorted(tasks, key=lambda t: t.block_index, reverse=True)
        
        for task in sorted_tasks:
            if task.suggested_hook:
                # Use the original block text to ensure we replace the right occurrence
                old_evidence_line = f"| **Evidence:** {task.evidence} |"
                new_evidence_line = f"| **Evidence:** {task.suggested_hook} |"
                
                # Replace within the specific task block
                if task.original_text in content:
                    updated_block = task.original_text.replace(old_evidence_line, new_evidence_line, 1)
                    content = content.replace(task.original_text, updated_block, 1)
                    changes_count += 1
                else:
                    print(f"⚠️  Warning: Could not find task block for {task.task_id}")
        
        # Write back to file
        file_path.write_text(content, encoding='utf-8')
        
        print(f"\n✅ Applied {changes_count} changes to {file_path}")
        print(f"✅ Original file backed up to: {backup_path}")
        
    except Exception as e:
        # Restore from backup on error
        print(f"\n❌ Error occurred: {e}")
        print(f"🔄 Restoring from backup...")
        shutil.copy2(backup_path, file_path)
        print(f"✅ File restored from backup")
        raise


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
        preview_changes(tasks_to_migrate, file_path, tasks)


if __name__ == '__main__':
    main()
