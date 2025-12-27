#!/usr/bin/env python3
"""
Batch Prompts Execution Script

Execute all generated prompts in a single batch run with automatic priority
ordering, progress tracking, and error handling.

Usage:
    python3 execute_prompts_batch.py \
        --prompts-dir .spec/prompts/20251226_083000/ \
        --tasks tasks.md

Features:
    - Automatic priority ordering
    - Progress tracking
    - Error handling
    - Checkpoint support
    - Dry run mode
    - Category filtering
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set
from enum import Enum

# Import naming convention helper
sys.path.insert(0, str(Path(__file__).parent))
from naming_convention_helper import (
    load_naming_standard,
    validate_file_path,
    is_compliant,
    get_naming_statistics
)


class ProblemCategory(Enum):
    """Problem categories matching verify_evidence_enhanced.py"""
    NOT_IMPLEMENTED = "not_implemented"
    MISSING_TESTS = "missing_tests"
    MISSING_CODE = "missing_code"
    NAMING_ISSUE = "naming_issue"
    SYMBOL_ISSUE = "symbol_issue"
    CONTENT_ISSUE = "content_issue"


@dataclass
class Task:
    """Task to be executed"""
    task_id: str
    title: str
    category: ProblemCategory
    priority: int
    code_file: Optional[str] = None
    test_file: Optional[str] = None
    code_content: Optional[str] = None
    test_content: Optional[str] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []


@dataclass
class ExecutionResult:
    """Result of task execution"""
    task_id: str
    success: bool
    error: Optional[str] = None
    files_created: List[str] = None
    files_modified: List[str] = None
    
    def __post_init__(self):
        if self.files_created is None:
            self.files_created = []
        if self.files_modified is None:
            self.files_modified = []


@dataclass
class BatchExecutionSummary:
    """Summary of batch execution"""
    started: str
    completed: str
    duration_seconds: float
    total_tasks: int
    successful: int
    failed: int
    results: List[ExecutionResult]
    verification_before: Optional[Dict] = None
    verification_after: Optional[Dict] = None
    naming_statistics: Optional[Dict] = None


class PromptsParser:
    """Parse generated prompts directory"""
    
    def __init__(self, prompts_dir: Path):
        self.prompts_dir = prompts_dir
        self.tasks: List[Task] = []
        
    def parse(self) -> List[Task]:
        """Parse all prompt files and extract tasks"""
        
        # Read summary.json if exists
        summary_file = self.prompts_dir / "meta" / "summary.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
                print(f"📊 Summary: {summary.get('total_tasks', 0)} tasks across {summary.get('total_categories', 0)} categories")
        
        # Parse each category file
        for category in ProblemCategory:
            category_file = self.prompts_dir / f"{category.value}.md"
            if category_file.exists():
                self._parse_category_file(category_file, category)
        
        # Sort by priority
        self.tasks.sort(key=lambda t: (t.priority, t.task_id))
        
        return self.tasks
    
    def _parse_category_file(self, file_path: Path, category: ProblemCategory):
        """Parse a single category file"""
        content = file_path.read_text()
        
        # Split by task headers (## Task: TASK-XXX)
        task_sections = re.split(r'\n## Task: (TASK-\d+)', content)
        
        # Skip first section (header)
        for i in range(1, len(task_sections), 2):
            if i + 1 < len(task_sections):
                task_id = task_sections[i]
                task_content = task_sections[i + 1]
                
                task = self._parse_task(task_id, task_content, category)
                if task:
                    self.tasks.append(task)
    
    def _parse_task(self, task_id: str, content: str, category: ProblemCategory) -> Optional[Task]:
        """Parse a single task from content"""
        
        # Extract title
        title_match = re.search(r'^(.+?)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # Extract priority
        priority_match = re.search(r'Priority:\s*(\d+)', content)
        priority = int(priority_match.group(1)) if priority_match else 2
        
        # Extract code file
        code_file_match = re.search(r'Code file:\s*`([^`]+)`', content)
        code_file = code_file_match.group(1) if code_file_match else None
        
        # Extract test file
        test_file_match = re.search(r'Test file:\s*`([^`]+)`', content)
        test_file = test_file_match.group(1) if test_file_match else None
        
        # Extract code content
        code_content = None
        code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
        if code_match:
            code_content = code_match.group(1)
        
        # Extract test content
        test_content = None
        test_match = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        if len(test_match) > 1:
            test_content = test_match[1]
        
        # Extract suggestions
        suggestions = []
        suggestions_section = re.search(r'### Suggestions\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
        if suggestions_section:
            suggestion_lines = suggestions_section.group(1).strip().split('\n')
            suggestions = [line.strip('- ').strip() for line in suggestion_lines if line.strip().startswith('-')]
        
        return Task(
            task_id=task_id,
            title=title,
            category=category,
            priority=priority,
            code_file=code_file,
            test_file=test_file,
            code_content=code_content,
            test_content=test_content,
            suggestions=suggestions
        )


class BatchExecutor:
    """Execute batch of tasks"""
    
    def __init__(self, 
                 tasks: List[Task],
                 repo_root: Path,
                 dry_run: bool = False,
                 max_failures: int = 3,
                 checkpoint_enabled: bool = False):
        self.tasks = tasks
        self.repo_root = repo_root
        self.dry_run = dry_run
        self.max_failures = max_failures
        self.checkpoint_enabled = checkpoint_enabled
        self.results: List[ExecutionResult] = []
        self.failures = 0
        self.naming_standard = load_naming_standard(repo_root)
        self.naming_violations: List[Dict] = []
        
    def execute(self) -> List[ExecutionResult]:
        """Execute all tasks"""
        
        print(f"\n🚀 Starting batch execution: {len(self.tasks)} tasks")
        print(f"   Dry run: {self.dry_run}")
        print(f"   Max failures: {self.max_failures}")
        print(f"   Checkpoint: {self.checkpoint_enabled}\n")
        
        for idx, task in enumerate(self.tasks, 1):
            print(f"[{idx}/{len(self.tasks)}] {task.task_id}: {task.title}")
            
            if self.dry_run:
                print(f"   Would create: {task.code_file}")
                if task.test_file:
                    print(f"   Would create: {task.test_file}")
                continue
            
            result = self._execute_task(task)
            self.results.append(result)
            
            if result.success:
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed: {result.error}")
                self.failures += 1
                
                if self.failures >= self.max_failures:
                    print(f"\n⚠️  Max failures ({self.max_failures}) reached. Stopping.")
                    if self.checkpoint_enabled:
                        self._save_checkpoint(idx)
                    break
            
            if self.checkpoint_enabled and idx % 5 == 0:
                self._save_checkpoint(idx)
        
        return self.results
    
    def _execute_task(self, task: Task) -> ExecutionResult:
        """Execute a single task"""
        
        files_created = []
        files_modified = []
        
        try:
            # Create code file
            if task.code_file and task.code_content:
                # Validate naming convention
                self._validate_naming_convention(task.code_file)
                
                code_path = self.repo_root / task.code_file
                
                if code_path.exists():
                    files_modified.append(task.code_file)
                else:
                    files_created.append(task.code_file)
                
                code_path.parent.mkdir(parents=True, exist_ok=True)
                code_path.write_text(task.code_content)
            
            # Create test file
            if task.test_file and task.test_content:
                # Validate naming convention
                self._validate_naming_convention(task.test_file)
                
                test_path = self.repo_root / task.test_file
                
                if test_path.exists():
                    files_modified.append(task.test_file)
                else:
                    files_created.append(task.test_file)
                
                test_path.parent.mkdir(parents=True, exist_ok=True)
                test_path.write_text(task.test_content)
            
            return ExecutionResult(
                task_id=task.task_id,
                success=True,
                files_created=files_created,
                files_modified=files_modified
            )
            
        except Exception as e:
            return ExecutionResult(
                task_id=task.task_id,
                success=False,
                error=str(e)
            )
    
    def _validate_naming_convention(self, file_path: str):
        """Validate file path against naming convention"""
        result = validate_file_path(file_path, self.naming_standard)
        
        if not result.compliant:
            # Log violation but don't fail (warning only)
            self.naming_violations.append({
                'file': file_path,
                'issues': result.issues
            })
            print(f"   ⚠️  Naming convention warning: {file_path}")
            for issue in result.issues:
                print(f"       - {issue}")
        else:
            print(f"   ✅ Naming convention OK: {file_path}")
    
    def _save_checkpoint(self, current_idx: int):
        """Save checkpoint"""
        checkpoint_dir = self.repo_root / ".spec" / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        checkpoint_file = checkpoint_dir / f"batch_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        checkpoint_data = {
            "timestamp": datetime.now().isoformat(),
            "current_task_index": current_idx,
            "total_tasks": len(self.tasks),
            "failures": self.failures,
            "completed_tasks": [r.task_id for r in self.results if r.success],
            "failed_tasks": [r.task_id for r in self.results if not r.success]
        }
        
        checkpoint_file.write_text(json.dumps(checkpoint_data, indent=2))
        print(f"   💾 Checkpoint saved: {checkpoint_file}")


class ReportGenerator:
    """Generate execution summary report"""
    
    def __init__(self, summary: BatchExecutionSummary, output_dir: Path):
        self.summary = summary
        self.output_dir = output_dir
        
    def generate(self) -> Path:
        """Generate markdown report"""
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f"batch_execution_{timestamp}.md"
        
        content = self._generate_markdown()
        report_file.write_text(content)
        
        # Also save JSON
        json_file = self.output_dir / f"batch_execution_{timestamp}.json"
        json_file.write_text(json.dumps(asdict(self.summary), indent=2))
        
        return report_file
    
    def _generate_markdown(self) -> str:
        """Generate markdown content"""
        
        success_rate = (self.summary.successful / self.summary.total_tasks * 100) if self.summary.total_tasks > 0 else 0
        
        md = f"""# Batch Execution Summary

**Started:** {self.summary.started}
**Completed:** {self.summary.completed}
**Duration:** {self.summary.duration_seconds:.1f} seconds

## Results

**Total Tasks:** {self.summary.total_tasks}
**Successful:** {self.summary.successful} ({success_rate:.1f}%)
**Failed:** {self.summary.failed} ({100-success_rate:.1f}%)

## Task Details

"""
        
        for result in self.summary.results:
            status = "✅" if result.success else "❌"
            md += f"### {status} {result.task_id}\n\n"
            
            if result.success:
                if result.files_created:
                    md += f"**Created:**\n"
                    for f in result.files_created:
                        md += f"- `{f}`\n"
                
                if result.files_modified:
                    md += f"**Modified:**\n"
                    for f in result.files_modified:
                        md += f"- `{f}`\n"
            else:
                md += f"**Error:** {result.error}\n"
            
            md += "\n"
        
        if self.summary.failed > 0:
            md += "## Failed Tasks\n\n"
            for result in self.summary.results:
                if not result.success:
                    md += f"- **{result.task_id}:** {result.error}\n"
            md += "\n"
        
        # Add naming convention section
        if self.summary.naming_statistics:
            stats = self.summary.naming_statistics
            md += "## Naming Convention Compliance\n\n"
            md += f"**Compliance Rate:** {stats['compliance_rate']:.1%}\n"
            md += f"**Compliant Files:** {stats['compliant_files']}/{stats['total_files']}\n\n"
            
            if stats['non_compliant_files'] > 0:
                md += "### Violations\n\n"
                for violation in stats['violations']:
                    md += f"**{violation['file']}**\n"
                    for issue in violation['issues']:
                        md += f"- {issue}\n"
                    md += "\n"
                
                md += "### Recommendations\n\n"
                md += "1. Run naming convention validator:\n"
                md += "   ```bash\n"
                md += "   python3 .smartspec/scripts/validate_naming_convention.py --fix\n"
                md += "   ```\n\n"
                md += "2. Update tasks.md with corrected paths\n\n"
                md += "3. Re-run verification\n\n"
        
        md += "## Next Steps\n\n"
        if self.summary.failed > 0:
            md += "1. **Fix failed tasks manually**\n"
            md += "2. **Run verification** to confirm all fixes:\n"
            md += "   ```bash\n"
            md += "   /smartspec_verify_tasks_progress_strict <tasks.md> --json\n"
            md += "   ```\n"
            md += "3. **Commit changes** after verification passes:\n"
            md += "   ```bash\n"
            md += "   git add -A\n"
            md += "   git commit -m \"fix: Resolve issues from batch execution\"\n"
            md += "   ```\n"
        else:
            md += "1. **Run verification** to confirm all fixes:\n"
            md += "   ```bash\n"
            md += "   /smartspec_verify_tasks_progress_strict <tasks.md> --json\n"
            md += "   ```\n"
            md += "2. **Commit changes** after verification passes:\n"
            md += "   ```bash\n"
            md += "   git add -A\n"
            md += "   git commit -m \"fix: Complete batch execution fixes\"\n"
            md += "   ```\n"
        
        return md


def main():
    parser = argparse.ArgumentParser(
        description="Execute all generated prompts in batch",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--prompts-dir",
        type=Path,
        required=True,
        help="Directory containing generated prompts"
    )
    
    parser.add_argument(
        "--tasks",
        type=Path,
        required=True,
        help="Path to tasks.md file"
    )
    
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root directory"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview execution plan without making changes"
    )
    
    parser.add_argument(
        "--checkpoint",
        action="store_true",
        help="Enable checkpointing"
    )
    
    parser.add_argument(
        "--max-failures",
        type=int,
        default=3,
        help="Maximum failures before stopping"
    )
    
    parser.add_argument(
        "--skip-category",
        type=str,
        help="Skip categories (comma-separated)"
    )
    
    parser.add_argument(
        "--only-category",
        type=str,
        help="Execute only these categories (comma-separated)"
    )
    
    parser.add_argument(
        "--verify-after-each",
        action="store_true",
        help="Verify after each category"
    )
    
    parser.add_argument(
        "--verify-at-end",
        action="store_true",
        default=True,
        help="Verify at the end"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.prompts_dir.exists():
        print(f"❌ Error: Prompts directory not found: {args.prompts_dir}")
        return 1
    
    if not args.tasks.exists():
        print(f"❌ Error: tasks.md not found: {args.tasks}")
        return 1
    
    # Parse prompts
    print("📖 Parsing prompts directory...")
    parser_obj = PromptsParser(args.prompts_dir)
    tasks = parser_obj.parse()
    
    if not tasks:
        print("⚠️  No tasks found in prompts directory")
        return 0
    
    # Filter categories if requested
    if args.skip_category:
        skip_cats = set(args.skip_category.split(','))
        tasks = [t for t in tasks if t.category.value not in skip_cats]
        print(f"   Skipping categories: {skip_cats}")
    
    if args.only_category:
        only_cats = set(args.only_category.split(','))
        tasks = [t for t in tasks if t.category.value in only_cats]
        print(f"   Only executing categories: {only_cats}")
    
    print(f"   Found {len(tasks)} tasks to execute\n")
    
    # Show execution plan
    print("📋 Execution Plan:\n")
    current_category = None
    for idx, task in enumerate(tasks, 1):
        if task.category != current_category:
            current_category = task.category
            print(f"\n{current_category.value} (Priority {task.priority}):")
        print(f"  {idx}. {task.task_id}: {task.title}")
    
    if args.dry_run:
        print("\n✅ Dry run complete. No changes made.")
        return 0
    
    # Execute batch
    start_time = datetime.now()
    
    executor = BatchExecutor(
        tasks=tasks,
        repo_root=args.repo_root,
        dry_run=args.dry_run,
        max_failures=args.max_failures,
        checkpoint_enabled=args.checkpoint
    )
    
    results = executor.execute()
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Generate summary
    successful = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)
    
    # Collect all created/modified files
    all_files = []
    for result in results:
        all_files.extend(result.files_created)
        all_files.extend(result.files_modified)
    
    # Get naming statistics
    naming_stats = get_naming_statistics(all_files, executor.naming_standard) if all_files else None
    
    summary = BatchExecutionSummary(
        started=start_time.isoformat(),
        completed=end_time.isoformat(),
        duration_seconds=duration,
        total_tasks=len(tasks),
        successful=successful,
        failed=failed,
        results=results,
        naming_statistics=naming_stats
    )
    
    # Generate report
    report_dir = args.repo_root / ".spec" / "reports" / "batch-execution"
    report_gen = ReportGenerator(summary, report_dir)
    report_file = report_gen.generate()
    
    print(f"\n📊 Report saved: {report_file}")
    print(f"\n✅ Batch execution complete!")
    print(f"   Successful: {successful}/{len(tasks)}")
    print(f"   Failed: {failed}/{len(tasks)}")
    print(f"   Duration: {duration:.1f}s")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
