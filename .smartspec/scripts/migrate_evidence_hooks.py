#!/usr/bin/env python3
"""
SmartSpec Migrate Evidence Hooks (Enhanced - Kilo/Antigravity Compatible)
Converts descriptive evidence to standardized evidence hooks using AI
with file system validation and path correction

This version expects LLM to be called externally (via Kilo/Antigravity)
and reads prompts/responses through a simple interface.
"""

import argparse
import re
import sys
import time
import shutil
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple


class ProjectContext:
    """Scans and indexes project files for evidence validation"""
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.all_files: Set[str] = set()
        self.symbol_index: Dict[str, List[str]] = {}  # symbol -> [file paths]
        self.package_index: Dict[str, List[str]] = {}  # package name -> [file paths]
        self._scan_project()
    
    def _scan_project(self):
        """Scan project for files and build indexes"""
        print("🔍 Scanning project files...")
        
        # Common ignore patterns
        ignore_dirs = {'.git', 'node_modules', '.next', 'dist', 'build', '__pycache__', 
                      '.venv', 'venv', 'coverage', '.spec/reports'}
        
        file_count = 0
        for root, dirs, files in os.walk(self.project_root):
            # Remove ignored directories from search
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                file_path = Path(root) / file
                try:
                    rel_path = file_path.relative_to(self.project_root)
                    self.all_files.add(str(rel_path))
                    file_count += 1
                    
                    # Index source files for symbols and packages
                    if file.endswith(('.ts', '.tsx', '.js', '.jsx', '.py')):
                        self._index_file(file_path, str(rel_path))
                except ValueError:
                    continue
        
        print(f"✅ Indexed {file_count} files")
        print(f"✅ Found {len(self.symbol_index)} unique symbols")
        print(f"✅ Found {len(self.package_index)} package references")
    
    def _index_file(self, file_path: Path, rel_path: str):
        """Index symbols and package imports in a file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Index common symbols (functions, classes, exports)
            # TypeScript/JavaScript
            for match in re.finditer(r'(?:export\s+)?(?:function|class|const|let|var)\s+(\w+)', content):
                symbol = match.group(1)
                if symbol not in self.symbol_index:
                    self.symbol_index[symbol] = []
                self.symbol_index[symbol].append(rel_path)
            
            # Python
            for match in re.finditer(r'(?:def|class)\s+(\w+)', content):
                symbol = match.group(1)
                if symbol not in self.symbol_index:
                    self.symbol_index[symbol] = []
                self.symbol_index[symbol].append(rel_path)
            
            # Index package imports (for bcrypt, JWT, Vault, Redis, BullMQ, Winston, etc.)
            common_packages = {
                'bcrypt', 'bcryptjs', 'jsonwebtoken', 'jwt', 'vault', 'redis', 
                'ioredis', 'bullmq', 'bull', 'winston', 'pino', 'express',
                'fastify', 'prisma', 'drizzle', 'mongoose', 'typeorm'
            }
            
            for pkg in common_packages:
                # TypeScript/JavaScript imports
                if re.search(rf'(?:import|require)\s*.*[\'"]({pkg})[\'"]', content):
                    if pkg not in self.package_index:
                        self.package_index[pkg] = []
                    self.package_index[pkg].append(rel_path)
                
                # Python imports
                if re.search(rf'(?:import|from)\s+({pkg})', content):
                    if pkg not in self.package_index:
                        self.package_index[pkg] = []
                    self.package_index[pkg].append(rel_path)
        except Exception:
            pass
    
    def find_file(self, partial_path: str) -> Optional[str]:
        """Find a file by partial path (supports fuzzy matching)"""
        partial_path = partial_path.strip()
        
        # Exact match
        if partial_path in self.all_files:
            return partial_path
        
        # Try with common extensions
        for ext in ['.ts', '.tsx', '.js', '.jsx', '.py', '.json', '.yaml', '.yml', '.md']:
            if f"{partial_path}{ext}" in self.all_files:
                return f"{partial_path}{ext}"
        
        # Try basename match
        basename = Path(partial_path).name
        for file in self.all_files:
            if Path(file).name == basename:
                return file
        
        return None
    
    def find_symbol_file(self, symbol: str) -> Optional[str]:
        """Find a file containing a specific symbol"""
        if symbol in self.symbol_index:
            return self.symbol_index[symbol][0]  # Return first match
        return None
    
    def find_package_file(self, package: str) -> Optional[str]:
        """Find a file that imports a specific package"""
        package_lower = package.lower()
        for pkg, files in self.package_index.items():
            if pkg.lower() == package_lower:
                return files[0]  # Return first match
        return None
    
    def get_project_summary(self) -> str:
        """Generate a summary of the project for AI context"""
        # Get top-level directories
        top_dirs = set()
        for file in list(self.all_files)[:100]:  # Sample first 100 files
            parts = Path(file).parts
            if len(parts) > 0:
                top_dirs.add(parts[0])
        
        # Get file type distribution
        file_types = {}
        for file in self.all_files:
            ext = Path(file).suffix
            if ext:
                file_types[ext] = file_types.get(ext, 0) + 1
        
        # Get top packages
        top_packages = sorted(self.package_index.keys())[:10]
        
        summary = f"""
Project Structure:
- Total files: {len(self.all_files)}
- Top directories: {', '.join(sorted(top_dirs)[:10])}
- Main file types: {', '.join(f'{ext}({count})' for ext, count in sorted(file_types.items(), key=lambda x: -x[1])[:5])}
- Key packages used: {', '.join(top_packages)}
"""
        return summary.strip()


class Task:
    """Represents a task with evidence"""
    def __init__(self, task_id: str, title: str, description: str, evidence: str, line_num: int):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.evidence = evidence
        self.line_num = line_num
        self.suggested_hook: Optional[str] = None
        self.validation_status: Optional[str] = None
        self.validation_reason: Optional[str] = None


def parse_tasks_file(file_path: Path) -> List[Task]:
    """Parse tasks.md file and extract tasks with descriptive evidence"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    tasks = []
    current_task_id = None
    current_title = None
    current_description = None
    current_evidence = None
    current_line = None
    
    # Pattern to match task lines: - [x] TSK-XXX-NNN Title
    task_pattern = re.compile(r'^\s*-\s*\[[ x]\]\s+(TSK-[\w-]+)\s+(.+?)$')
    # Pattern to match evidence lines that are NOT standardized
    evidence_pattern = re.compile(r'^\s*-\s*\*\*Evidence:\*\*\s+(.+?)$')
    
    for i, line in enumerate(lines, 1):
        # Check for task line
        task_match = task_pattern.match(line)
        if task_match:
            # Save previous task if it had descriptive evidence
            if current_task_id and current_evidence:
                tasks.append(Task(current_task_id, current_title, current_description, current_evidence, current_line))
            
            # Start new task
            current_task_id = task_match.group(1)
            current_title = task_match.group(2).strip()
            current_description = current_title
            current_evidence = None
            current_line = i
            continue
        
        # Check for descriptive evidence
        evidence_match = evidence_pattern.match(line)
        if evidence_match and current_task_id:
            evidence_text = evidence_match.group(1).strip()
            # Only capture if it's NOT already a standardized hook
            if not evidence_text.startswith('evidence:'):
                current_evidence = evidence_text
                current_line = i
    
    # Don't forget the last task
    if current_task_id and current_evidence:
        tasks.append(Task(current_task_id, current_title, current_description, current_evidence, current_line))
    
    return tasks


def validate_evidence_hook(hook: str, context: ProjectContext) -> Tuple[bool, str, Optional[str]]:
    """
    Validate an evidence hook and suggest corrections if needed
    Returns: (is_valid, reason, corrected_hook)
    """
    # Parse the hook
    hook = hook.strip()
    if not hook.startswith('evidence:'):
        return False, "Hook must start with 'evidence:'", None
    
    # Extract type and parameters
    parts = hook[9:].strip().split(maxsplit=1)
    if not parts:
        return False, "Missing evidence type", None
    
    hook_type = parts[0]
    params_str = parts[1] if len(parts) > 1 else ""
    
    # Parse parameters (key=value format)
    params = {}
    for match in re.finditer(r'(\w+)=([^\s]+(?:\s+[^\s=]+)*?)(?=\s+\w+=|$)', params_str):
        key = match.group(1)
        value = match.group(2).strip().strip('"\'')
        params[key] = value
    
    # Validate based on type
    if hook_type == 'code':
        if 'path' not in params:
            # If no path but has symbol, try to find it
            if 'symbol' in params:
                actual_path = context.find_symbol_file(params['symbol'])
                if actual_path:
                    corrected = f"evidence: code path={actual_path} symbol={params['symbol']}"
                    if 'contains' in params:
                        corrected += f" contains={params['contains']}"
                    return False, f"Added path from symbol lookup: {actual_path}", corrected
            return False, "Missing required 'path' parameter", None
        
        # Check if file exists
        actual_path = context.find_file(params['path'])
        if not actual_path:
            # Try to find by symbol
            if 'symbol' in params:
                actual_path = context.find_symbol_file(params['symbol'])
                if actual_path:
                    corrected = f"evidence: code path={actual_path}"
                    if 'symbol' in params:
                        corrected += f" symbol={params['symbol']}"
                    if 'contains' in params:
                        corrected += f" contains={params['contains']}"
                    return False, f"Path not found, suggested: {actual_path}", corrected
            
            # Try to find file by package name in contains
            if 'contains' in params:
                for pkg in ['bcrypt', 'jwt', 'vault', 'redis', 'bullmq', 'winston']:
                    if pkg.lower() in params['contains'].lower():
                        actual_path = context.find_package_file(pkg)
                        if actual_path:
                            corrected = f"evidence: code path={actual_path} contains={params['contains']}"
                            return False, f"Path not found, suggested file using {pkg}: {actual_path}", corrected
            
            return False, f"File not found: {params['path']}", None
        
        # Path exists but different - suggest correction
        if actual_path != params['path']:
            corrected = f"evidence: code path={actual_path}"
            if 'symbol' in params:
                corrected += f" symbol={params['symbol']}"
            if 'contains' in params:
                corrected += f" contains={params['contains']}"
            return False, f"Path corrected: {params['path']} -> {actual_path}", corrected
        
        return True, "Valid", None
    
    elif hook_type == 'test':
        if 'path' not in params:
            return False, "Missing required 'path' parameter", None
        
        # Check if test file exists
        actual_path = context.find_file(params['path'])
        if not actual_path:
            return False, f"Test file not found: {params['path']}", None
        
        if actual_path != params['path']:
            corrected = f"evidence: test path={actual_path}"
            if 'contains' in params:
                corrected += f" contains={params['contains']}"
            # Note: 'command' is never executed by verifier, just recorded
            if 'command' in params:
                corrected += f" command={params['command']}"
            return False, f"Path corrected: {params['path']} -> {actual_path}", corrected
        
        return True, "Valid", None
    
    elif hook_type == 'ui':
        # UI evidence requires 'screen'
        if 'screen' not in params:
            return False, "Missing required 'screen' parameter", None
        
        # UI verification is often manual, but we can check if component exists
        if 'component' in params:
            actual_path = context.find_symbol_file(params['component'])
            if not actual_path:
                return False, f"Component not found: {params['component']}", None
        
        return True, "Valid (UI may need manual verification)", None
    
    elif hook_type == 'docs':
        if 'path' not in params:
            return False, "Missing required 'path' parameter", None
        
        # Check if docs file exists
        actual_path = context.find_file(params['path'])
        if not actual_path:
            return False, f"Docs file not found: {params['path']}", None
        
        if actual_path != params['path']:
            corrected = f"evidence: docs path={actual_path}"
            if 'heading' in params:
                corrected += f" heading={params['heading']}"
            if 'contains' in params:
                corrected += f" contains={params['contains']}"
            return False, f"Path corrected: {params['path']} -> {actual_path}", corrected
        
        return True, "Valid", None
    
    else:
        return False, f"Unknown evidence type: {hook_type}", None


def build_prompt(task: Task, context: ProjectContext) -> str:
    """Build the prompt for LLM"""
    return f"""You are an expert at converting natural language evidence descriptions into standardized evidence hooks for SmartSpec verification.

PROJECT CONTEXT:
{context.get_project_summary()}

TASK:
ID: {task.task_id}
Title: {task.title}
Description: {task.description}

CURRENT EVIDENCE (descriptive):
{task.evidence}

EVIDENCE HOOK FORMATS (from smartspec_verify_tasks_progress_strict):

1. code evidence - For implementation/source code:
   evidence: code path=<file-path> [symbol=<function/class>] [contains=<text>]
   Example: evidence: code path=src/auth/login.ts symbol=validatePassword

2. test evidence - For test files:
   evidence: test path=<test-file> [contains=<test-description>]
   Example: evidence: test path=tests/auth.test.ts contains="validates password"
   IMPORTANT: NEVER use 'command' in test evidence (verifier doesn't execute commands)

3. ui evidence - For UI components:
   evidence: ui screen=<screen-name> [route=<path>] [component=<name>] [states=<list>]
   Example: evidence: ui screen=LoginScreen component=PasswordInput

4. docs evidence - For documentation:
   evidence: docs path=<doc-file> [heading=<section>] [contains=<text>]
   Example: evidence: docs path=README.md heading="Authentication"

CRITICAL RULES:
1. Use REAL file paths that exist in the project (see PROJECT CONTEXT above)
2. For packages like bcrypt/JWT/Vault/Redis/BullMQ/Winston, find the ACTUAL file that imports them
3. NEVER use placeholder paths like "???" or "TODO"
4. NEVER use 'command' in test evidence (verifier doesn't execute commands)
5. All paths must be repo-relative (no absolute paths)
6. Choose the most appropriate evidence type based on what's being verified

RESPONSE FORMAT:
Return ONLY the evidence hook, nothing else:
evidence: <type> <key>=<value> <key>=<value>
"""


def generate_evidence_hook_interactive(task: Task, context: ProjectContext) -> str:
    """
    Generate evidence hook by writing prompt to file and waiting for response
    This allows external LLM (Kilo/Antigravity) to process it
    """
    prompt = build_prompt(task, context)
    
    # Write prompt to file
    prompt_file = Path(f"/tmp/evidence_prompt_{task.task_id}.txt")
    response_file = Path(f"/tmp/evidence_response_{task.task_id}.txt")
    
    prompt_file.write_text(prompt)
    
    print(f"\n{'='*80}")
    print(f"PROMPT for {task.task_id}:")
    print(f"{'='*80}")
    print(f"Prompt written to: {prompt_file}")
    print(f"\nPlease:")
    print(f"1. Read the prompt from: {prompt_file}")
    print(f"2. Generate the evidence hook using your LLM")
    print(f"3. Write the response to: {response_file}")
    print(f"4. Press Enter when done...")
    print(f"{'='*80}")
    
    input()  # Wait for user
    
    # Read response
    if response_file.exists():
        hook = response_file.read_text().strip()
        response_file.unlink()  # Clean up
        prompt_file.unlink()
        
        # Ensure it starts with "evidence:"
        if not hook.startswith('evidence:'):
            hook = f"evidence: {hook}"
        
        return hook
    else:
        print(f"⚠️  No response file found, using fallback")
        return f"evidence: code path=MANUAL_INPUT_REQUIRED contains=check_task_{task.task_id}"


def apply_changes(file_path: Path, tasks: List[Task]):
    """Apply the suggested evidence hooks to the tasks file"""
    # Create backup
    backup_path = file_path.with_suffix('.md.backup')
    shutil.copy2(file_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Build a map of line numbers to new evidence
        replacements = {}
        for task in tasks:
            if task.suggested_hook:
                replacements[task.line_num] = task.suggested_hook
        
        # Apply replacements
        modified_lines = []
        for i, line in enumerate(lines, 1):
            if i in replacements:
                # Replace the evidence line
                indent = len(line) - len(line.lstrip())
                new_line = ' ' * indent + f"- {replacements[i]}\n"
                modified_lines.append(new_line)
            else:
                modified_lines.append(line)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        print(f"✅ Applied {len(replacements)} changes to {file_path}")
        print(f"✅ Backup available at: {backup_path}")
        
    except Exception as e:
        # Restore from backup on error
        print(f"❌ Error applying changes: {e}")
        print(f"🔄 Restoring from backup...")
        shutil.copy2(backup_path, file_path)
        print(f"✅ File restored from backup")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Migrate descriptive evidence to standardized evidence hooks"
    )
    parser.add_argument(
        "--tasks-file",
        required=True,
        help="Path to tasks.md file"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory for file validation (default: current directory)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to the file (default: preview only)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode: write prompts to files for external LLM processing"
    )
    
    args = parser.parse_args()
    
    tasks_file = Path(args.tasks_file)
    project_root = Path(args.project_root).resolve()
    
    if not tasks_file.exists():
        print(f"❌ Error: File not found: {tasks_file}")
        sys.exit(1)
    
    if not project_root.exists():
        print(f"❌ Error: Project root not found: {project_root}")
        sys.exit(1)
    
    print(f"📁 Project root: {project_root}")
    
    # Build project context
    context = ProjectContext(project_root)
    
    # Parse tasks file
    print(f"📖 Reading tasks from: {tasks_file}")
    tasks = parse_tasks_file(tasks_file)
    
    if not tasks:
        print("✅ No tasks with descriptive evidence found. All evidence is already standardized!")
        sys.exit(0)
    
    print(f"Found {len(tasks)} tasks with descriptive evidence")
    
    # Generate evidence hooks
    if args.interactive:
        print("\n🤖 Interactive mode: You will be prompted to provide LLM responses")
        for i, task in enumerate(tasks, 1):
            print(f"\n[{i}/{len(tasks)}] Processing {task.task_id}...")
            task.suggested_hook = generate_evidence_hook_interactive(task, context)
    else:
        print("\n⚠️  This script requires --interactive mode in Kilo/Antigravity environment")
        print("Or you need to have OpenAI API key configured.")
        print("\nRun with: --interactive flag")
        sys.exit(1)
    
    # Validate generated hooks
    print(f"\n🔍 Validating generated hooks...")
    valid_count = 0
    corrected_count = 0
    manual_count = 0
    
    for i, task in enumerate(tasks, 1):
        print(f"  [{i}/{len(tasks)}] Validating {task.task_id}...", end=" ")
        is_valid, reason, corrected = validate_evidence_hook(task.suggested_hook, context)
        
        task.validation_status = "valid" if is_valid else "needs_review"
        task.validation_reason = reason
        
        if is_valid:
            print("✅")
            valid_count += 1
        elif corrected:
            print("🔧")
            task.suggested_hook = corrected
            task.validation_status = "corrected"
            corrected_count += 1
        else:
            print("⚠️")
            manual_count += 1
    
    # Print statistics
    print("\n" + "="*80)
    print(f"STATISTICS for {tasks_file.name}")
    print("="*80)
    print(f"Total tasks with descriptive evidence: {len(tasks)}")
    print(f"\nValidation results:")
    print(f"  ✅ Valid hooks: {valid_count}")
    print(f"  🔧 Auto-corrected: {corrected_count}")
    print(f"  ⚠️  Needs manual review: {manual_count}")
    print("="*80)
    
    # Preview changes
    print("\n" + "="*80)
    print(f"PREVIEW: Proposed changes for {tasks_file.name}")
    print("="*80)
    
    for task in tasks:
        print(f"\nTask: {task.task_id} - {task.title}")
        print("─" * 80)
        print(f"- OLD: {task.evidence}")
        print(f"+ NEW: {task.suggested_hook}")
        if task.validation_status != "valid":
            print(f"  Status: {task.validation_status.upper()} - {task.validation_reason}")
        print("─" * 80)
    
    print(f"\nTotal changes proposed: {len(tasks)}")
    
    # Apply changes if requested
    if args.apply:
        print("\n⚠️  You are about to modify the file!")
        print("Countdown: ", end="", flush=True)
        for i in range(3, 0, -1):
            print(f"{i}...", end="", flush=True)
            time.sleep(1)
        print("GO!")
        
        apply_changes(tasks_file, tasks)
        print("\n✅ Done! Changes applied.")
    else:
        print("\nTo apply these changes, run with --apply flag")


if __name__ == "__main__":
    main()
