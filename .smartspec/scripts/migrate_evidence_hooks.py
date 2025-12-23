#!/usr/bin/env python3
"""
SmartSpec Migrate Evidence Hooks (Enhanced)
Converts descriptive evidence to standardized evidence hooks using AI
with file system validation and path correction
"""

import argparse
import re
import sys
import time
import shutil
import os
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple

try:
    from openai import OpenAI, RateLimitError
    client = OpenAI()  # API key from environment
except ImportError:
    print("Error: openai package not installed. Run: pip3 install openai")
    sys.exit(1)


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
            pass  # Skip files that can't be read
    
    def find_file(self, partial_path: str) -> Optional[str]:
        """Find actual file path from partial/incorrect path"""
        # Exact match
        if partial_path in self.all_files:
            return partial_path
        
        # Try with common extensions
        for ext in ['.ts', '.tsx', '.js', '.jsx', '.py', '.md']:
            if f"{partial_path}{ext}" in self.all_files:
                return f"{partial_path}{ext}"
        
        # Try basename match
        basename = Path(partial_path).name
        matches = [f for f in self.all_files if Path(f).name == basename]
        if len(matches) == 1:
            return matches[0]
        
        # Try fuzzy match (contains)
        matches = [f for f in self.all_files if partial_path in f]
        if len(matches) == 1:
            return matches[0]
        
        return None
    
    def find_symbol_file(self, symbol: str) -> Optional[str]:
        """Find file containing a specific symbol"""
        if symbol in self.symbol_index:
            files = self.symbol_index[symbol]
            return files[0] if files else None
        return None
    
    def find_package_file(self, package: str) -> Optional[str]:
        """Find file that imports a specific package"""
        # Normalize package name
        pkg_lower = package.lower()
        for pkg_name, files in self.package_index.items():
            if pkg_lower in pkg_name.lower() or pkg_name.lower() in pkg_lower:
                return files[0] if files else None
        return None
    
    def get_project_summary(self) -> str:
        """Get a summary of project structure for AI context"""
        # Get top-level directories
        top_dirs = set()
        for file in list(self.all_files)[:100]:  # Sample first 100 files
            parts = Path(file).parts
            if parts:
                top_dirs.add(parts[0])
        
        # Get common file patterns
        extensions = {}
        for file in self.all_files:
            ext = Path(file).suffix
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
        
        summary = f"Project structure:\n"
        summary += f"- Top directories: {', '.join(sorted(top_dirs)[:10])}\n"
        summary += f"- Main file types: {', '.join([f'{ext}({count})' for ext, count in sorted(extensions.items(), key=lambda x: -x[1])[:5]])}\n"
        
        # List some key packages found
        if self.package_index:
            summary += f"- Key packages used: {', '.join(list(self.package_index.keys())[:10])}\n"
        
        return summary


class Task:
    """Represents a single task from tasks.md"""
    def __init__(self, task_id: str, title: str, description: str, evidence: str, original_text: str, block_index: int):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.evidence = evidence
        self.original_text = original_text
        self.block_index = block_index
        self.suggested_hook: Optional[str] = None
        self.validation_result: Optional[Dict] = None


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


def parse_evidence_hook(hook: str) -> Optional[Dict]:
    """Parse evidence hook into components"""
    if not hook.startswith('evidence:'):
        return None
    
    parts = hook.split(maxsplit=2)
    if len(parts) < 3:
        return None
    
    hook_type = parts[1]
    params_str = parts[2]
    
    # Parse key=value pairs
    params = {}
    for match in re.finditer(r'(\w+)=([^\s]+)', params_str):
        key = match.group(1)
        value = match.group(2).strip('"\'')
        params[key] = value
    
    return {
        'type': hook_type,
        'params': params
    }


def validate_evidence_hook(hook: str, context: ProjectContext) -> Tuple[bool, str, Optional[str]]:
    """
    Validate evidence hook and suggest corrections if needed
    Returns: (is_valid, reason, corrected_hook)
    """
    parsed = parse_evidence_hook(hook)
    if not parsed:
        return False, "Invalid hook format", None
    
    hook_type = parsed['type']
    params = parsed['params']
    
    # Validate based on type (from smartspec_verify_tasks_progress_strict.md)
    if hook_type == 'code':
        if 'path' not in params:
            return False, "Missing required 'path' parameter", None
        
        # Check if file exists
        actual_path = context.find_file(params['path'])
        if not actual_path:
            # Try to find file by symbol
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


def generate_evidence_hook(task: Task, context: ProjectContext, model: str = "gpt-4.1-mini", max_retries: int = 3) -> str:
    """Use AI to generate a standardized evidence hook from descriptive text with project context"""
    
    prompt = f"""You are an expert at converting natural language evidence descriptions into standardized evidence hooks for SmartSpec verification.

PROJECT CONTEXT:
{context.get_project_summary()}

TASK:
ID: {task.task_id}
Title: {task.title}
Description: {task.description}

CURRENT EVIDENCE (descriptive):
{task.evidence}

EVIDENCE HOOK FORMATS (from smartspec_verify_tasks_progress_strict):

1. code: For implementation evidence
   - Required: path (repo-relative, must exist)
   - Optional: symbol (function/class name), contains (code snippet)
   - Example: evidence: code path=src/auth/handler.ts symbol=validateToken
   - Example: evidence: code path=src/config/redis.ts contains="createClient"

2. test: For test evidence
   - Required: path (repo-relative, must exist)
   - Optional: contains (test description)
   - Note: 'command' is NEVER executed by verifier, avoid using it
   - Example: evidence: test path=tests/auth.test.ts contains="validates JWT token"

3. ui: For UI evidence
   - Required: screen (screen name)
   - Optional: route, component, states
   - Example: evidence: ui screen=LoginPage component=LoginForm states=loading,error,success

4. docs: For documentation evidence
   - Required: path (repo-relative, must exist)
   - Optional: heading, contains
   - Example: evidence: docs path=docs/api/auth.md heading="Authentication"

CRITICAL RULES:
1. Use REAL file paths that exist in the project
2. For packages like bcrypt/JWT/Vault/Redis/BullMQ/Winston, find the ACTUAL file that imports them
3. NEVER use placeholder paths like "???" or "TODO"
4. NEVER use 'command' in test evidence (verifier doesn't execute commands)
5. Paths must be repo-relative (no absolute paths, no "../")
6. Use 'contains' for code snippets, not full implementations

INSTRUCTIONS:
1. Analyze the task description and evidence text
2. Identify what needs to be verified (code, test, ui, or docs)
3. Find the most likely file path from the project structure
4. Generate ONE precise evidence hook

RESPONSE FORMAT:
Return ONLY the evidence hook, nothing else:
evidence: <type> <key>=<value> <key>=<value>
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
                max_tokens=150
            )
            
            hook = response.choices[0].message.content.strip()
            
            # Ensure it starts with "evidence:"
            if not hook.startswith('evidence:'):
                hook = f"evidence: {hook}"
            
            return hook
            
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"\n⚠️  Rate limit hit. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Rate limit exceeded for {task.task_id}")
                return f"evidence: code path=RATE_LIMIT_EXCEEDED contains=check_task_{task.task_id}"
        except Exception as e:
            print(f"\n⚠️  Warning: AI generation failed for {task.task_id}: {e}")
            return f"evidence: code path=GENERATION_FAILED contains=check_task_{task.task_id}"
    
    return f"evidence: code path=MAX_RETRIES_EXCEEDED contains=check_task_{task.task_id}"


def preview_changes(tasks: List[Task], file_path: Path, all_tasks: List[Task]):
    """Show a diff-like preview of proposed changes with detailed statistics"""
    
    already_standardized = len([t for t in all_tasks if t.evidence.startswith('evidence:')])
    no_evidence = len([t for t in all_tasks if not t.evidence.strip()])
    
    # Count validation results
    valid_count = 0
    corrected_count = 0
    invalid_count = 0
    
    for task in tasks:
        if task.validation_result:
            if task.validation_result['is_valid']:
                valid_count += 1
            elif task.validation_result['corrected_hook']:
                corrected_count += 1
            else:
                invalid_count += 1
    
    print(f"\n{'='*80}")
    print(f"STATISTICS for {file_path}")
    print(f"{'='*80}")
    print(f"Total tasks: {len(all_tasks)}")
    print(f"Already standardized: {already_standardized}")
    print(f"No evidence: {no_evidence}")
    print(f"Needs migration: {len(tasks)}")
    print(f"\nValidation results:")
    print(f"  ✅ Valid hooks: {valid_count}")
    print(f"  🔧 Auto-corrected: {corrected_count}")
    print(f"  ⚠️  Needs manual review: {invalid_count}")
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
            
            if task.validation_result:
                status = "✅ Valid" if task.validation_result['is_valid'] else \
                        f"🔧 Auto-corrected" if task.validation_result['corrected_hook'] else \
                        f"⚠️  {task.validation_result['reason']}"
                print(f"  Status: {status}")
            
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
        description="Migrate descriptive evidence to standardized evidence hooks with validation"
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
    parser.add_argument(
        '--project-root',
        type=str,
        help='Project root directory (default: auto-detect from tasks.md location)'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    file_path = Path(args.tasks_file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Determine project root
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        # Auto-detect: go up from tasks.md until we find .git or specs/
        project_root = file_path.parent
        while project_root != project_root.parent:
            if (project_root / '.git').exists() or (project_root / 'specs').exists():
                break
            project_root = project_root.parent
    
    print(f"📁 Project root: {project_root}")
    
    # Build project context
    context = ProjectContext(project_root)
    
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
    
    # Generate hooks using AI with project context
    print(f"\n🤖 Generating evidence hooks using {args.model}...")
    for i, task in enumerate(tasks_to_migrate, 1):
        print(f"  [{i}/{len(tasks_to_migrate)}] Processing {task.task_id}...", end='', flush=True)
        task.suggested_hook = generate_evidence_hook(task, context, args.model)
        print(" ✓")
        time.sleep(0.5)  # Rate limiting
    
    # Validate and auto-correct generated hooks
    print(f"\n🔍 Validating generated hooks...")
    for i, task in enumerate(tasks_to_migrate, 1):
        print(f"  [{i}/{len(tasks_to_migrate)}] Validating {task.task_id}...", end='', flush=True)
        is_valid, reason, corrected = validate_evidence_hook(task.suggested_hook, context)
        
        task.validation_result = {
            'is_valid': is_valid,
            'reason': reason,
            'corrected_hook': corrected
        }
        
        # Auto-apply correction if available
        if corrected:
            task.suggested_hook = corrected
            print(f" 🔧 (corrected)")
        elif is_valid:
            print(f" ✅")
        else:
            print(f" ⚠️")
    
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
