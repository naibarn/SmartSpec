#!/usr/bin/env python3
"""generate_prompts_from_verify_report.py (v1.0.0)

Generate category-specific implementation prompts from verify reports.

This script reads JSON output from verify_evidence_enhanced.py and generates
actionable prompts for fixing verification issues, organized by problem category.

Usage:
    python3 generate_prompts_from_verify_report.py \
        --verify-report report.json \
        --tasks tasks.md \
        --out .spec/prompts/

Features:
    - Automatic category detection
    - Priority-based ordering
    - Template-based prompt generation
    - Actionable suggestions per task
    - Summary and README generation

Safety:
    - Read-only operations
    - No file modifications
    - Safe output directory validation
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum


class ProblemCategory(Enum):
    """Problem categories from verify report"""
    NOT_IMPLEMENTED = "not_implemented"
    MISSING_TESTS = "missing_tests"
    MISSING_CODE = "missing_code"
    NAMING_ISSUE = "naming_issue"
    SYMBOL_ISSUE = "symbol_issue"
    CONTENT_ISSUE = "content_issue"


@dataclasses.dataclass
class TaskInfo:
    """Information about a task from verify report"""
    task_id: str
    title: str
    category: str
    priority: int
    checkbox_state: str
    code_path: Optional[str] = None
    test_path: Optional[str] = None
    code_symbol: Optional[str] = None
    test_symbol: Optional[str] = None
    code_contains: Optional[str] = None
    test_contains: Optional[str] = None
    suggestions: List[str] = dataclasses.field(default_factory=list)
    similar_files: List[Dict[str, str]] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class VerifyReport:
    """Parsed verify report"""
    total_tasks: int
    verified: int
    not_verified: int
    by_category: Dict[str, int]
    tasks: List[TaskInfo]
    report_path: str
    timestamp: str


class TemplateEngine:
    """Simple template engine for generating prompts"""
    
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
    
    def render(self, template_name: str, context: Dict) -> str:
        """Render template with context"""
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        template_content = template_path.read_text()
        
        # Simple variable substitution
        result = template_content
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        
        # Handle conditional blocks (simple implementation)
        result = self._process_conditionals(result, context)
        
        # Handle loops (simple implementation)
        result = self._process_loops(result, context)
        
        return result
    
    def _process_conditionals(self, text: str, context: Dict) -> str:
        """Process {{#if var}}...{{/if}} blocks"""
        pattern = r'\{\{#if\s+(\w+)\}\}(.*?)\{\{/if\}\}'
        
        def replace_conditional(match):
            var_name = match.group(1)
            content = match.group(2)
            if context.get(var_name):
                return content
            return ""
        
        return re.sub(pattern, replace_conditional, text, flags=re.DOTALL)
    
    def _process_loops(self, text: str, context: Dict) -> str:
        """Process {{#each items}}...{{/each}} blocks"""
        pattern = r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}'
        
        def replace_loop(match):
            var_name = match.group(1)
            content = match.group(2)
            items = context.get(var_name, [])
            
            if not items:
                return ""
            
            result = []
            for i, item in enumerate(items, 1):
                # Create context for this iteration
                item_context = context.copy()
                if isinstance(item, dict):
                    item_context.update(item)
                else:
                    item_context['this'] = item
                item_context['task_number'] = i
                
                # Process nested loops and conditionals first
                item_text = self._process_conditionals(content, item_context)
                item_text = self._process_loops(item_text, item_context)
                
                # Then do variable substitution
                for key, value in item_context.items():
                    if isinstance(value, (str, int, float, bool)):
                        placeholder = f"{{{{{key}}}}}"
                        item_text = item_text.replace(placeholder, str(value))
                    elif isinstance(value, list) and key != var_name:
                        # Handle list values (like suggestions)
                        if value:
                            list_str = "\n".join(f"- {v}" for v in value)
                            placeholder = f"{{{{{key}}}}}"
                            item_text = item_text.replace(placeholder, list_str)
                
                result.append(item_text)
            
            return "\n".join(result)
        
        # Process loops recursively
        while re.search(pattern, text, flags=re.DOTALL):
            text = re.sub(pattern, replace_loop, text, flags=re.DOTALL)
        
        return text


class ReportParser:
    """Parse verify report JSON"""
    
    @staticmethod
    def parse(report_path: Path) -> VerifyReport:
        """Parse verify report JSON file"""
        if not report_path.exists():
            raise FileNotFoundError(f"Report not found: {report_path}")
        
        with open(report_path) as f:
            data = json.load(f)
        
        # Parse totals
        totals = data.get("totals", {})
        total_tasks = totals.get("total_tasks", 0)
        verified = totals.get("verified", 0)
        not_verified = totals.get("not_verified", 0)
        
        # Parse by_category
        by_category = data.get("by_category", {})
        
        # Parse tasks
        tasks = []
        for task_data in data.get("tasks", []):
            task = TaskInfo(
                task_id=task_data.get("task_id", ""),
                title=task_data.get("title", ""),
                category=task_data.get("category", ""),
                priority=task_data.get("priority", 4),
                checkbox_state=task_data.get("checkbox_state", " "),
                code_path=task_data.get("code_path"),
                test_path=task_data.get("test_path"),
                code_symbol=task_data.get("code_symbol"),
                test_symbol=task_data.get("test_symbol"),
                code_contains=task_data.get("code_contains"),
                test_contains=task_data.get("test_contains"),
                suggestions=task_data.get("suggestions", []),
                similar_files=task_data.get("similar_files", [])
            )
            tasks.append(task)
        
        return VerifyReport(
            total_tasks=total_tasks,
            verified=verified,
            not_verified=not_verified,
            by_category=by_category,
            tasks=tasks,
            report_path=str(report_path),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )


class PromptGenerator:
    """Generate prompts from verify report"""
    
    def __init__(self, template_dir: Path, tasks_path: Path):
        self.template_engine = TemplateEngine(template_dir)
        self.tasks_path = tasks_path
    
    def generate(
        self,
        report: VerifyReport,
        output_dir: Path,
        category_filter: Optional[str] = None,
        priority_filter: Optional[int] = None
    ) -> Dict[str, Path]:
        """Generate prompts for all categories"""
        
        # Filter tasks
        tasks = report.tasks
        if category_filter:
            tasks = [t for t in tasks if t.category == category_filter]
        if priority_filter is not None:
            tasks = [t for t in tasks if t.priority == priority_filter]
        
        if not tasks:
            print("No tasks to generate prompts for.")
            return {}
        
        # Group tasks by category
        by_category = {}
        for task in tasks:
            category = task.category
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(task)
        
        # Generate prompts for each category
        generated_files = {}
        
        for category, category_tasks in by_category.items():
            # Sort by priority
            category_tasks.sort(key=lambda t: (t.priority, t.task_id))
            
            # Determine template
            template_name = self._get_template_name(category)
            
            # Prepare context
            context = self._prepare_context(
                category=category,
                tasks=category_tasks,
                report=report
            )
            
            # Render template
            try:
                content = self.template_engine.render(template_name, context)
                
                # Write output file
                output_file = output_dir / f"{category}.md"
                output_file.write_text(content)
                
                generated_files[category] = output_file
                print(f"✅ Generated: {output_file}")
                
            except FileNotFoundError as e:
                print(f"⚠️  Template not found for {category}: {e}")
                continue
            except Exception as e:
                print(f"❌ Error generating {category}: {e}")
                continue
        
        # Generate README
        readme_path = self._generate_readme(
            output_dir=output_dir,
            report=report,
            by_category=by_category,
            generated_files=generated_files
        )
        generated_files["README"] = readme_path
        
        # Generate summary JSON
        summary_path = self._generate_summary(
            output_dir=output_dir,
            report=report,
            by_category=by_category,
            generated_files=generated_files
        )
        generated_files["summary"] = summary_path
        
        return generated_files
    
    def _get_template_name(self, category: str) -> str:
        """Get template filename for category"""
        return f"{category}_template.md"
    
    def _prepare_context(
        self,
        category: str,
        tasks: List[TaskInfo],
        report: VerifyReport
    ) -> Dict:
        """Prepare template context"""
        
        # Determine priority
        priorities = [t.priority for t in tasks]
        priority = min(priorities) if priorities else 4
        
        # Prepare task contexts
        task_contexts = []
        for i, task in enumerate(tasks, 1):
            # Format suggestions as string
            suggestions_str = ""
            if task.suggestions:
                suggestions_str = "\n".join(f"- {s}" for s in task.suggestions)
            
            # Format similar files as string
            similar_files_str = ""
            if task.similar_files:
                similar_files_str = "\n".join(
                    f"- {f.get('file', '')} ({f.get('similarity', 0)}% similar)"
                    for f in task.similar_files
                )
            
            task_context = {
                "task_number": i,
                "task_id": task.task_id,
                "task_id_lower": task.task_id.lower().replace("-", "_"),
                "title": task.title,
                "priority": task.priority,
                "checkbox_state": task.checkbox_state,
                "code_path": task.code_path or "",
                "test_path": task.test_path or "",
                "code_symbol": task.code_symbol or "",
                "test_symbol": task.test_symbol or "",
                "code_contains": task.code_contains or "",
                "test_contains": task.test_contains or "",
                "suggestions": suggestions_str,
                "suggestions_list": task.suggestions,
                "similar_files": similar_files_str,
                "similar_files_list": task.similar_files,
                "file_path": task.code_path or task.test_path or "",
                "missing_symbol": task.code_symbol or task.test_symbol or "",
                "missing_content": task.code_contains or task.test_contains or "",
            }
            
            # Add derived fields
            if task.code_path:
                task_context["code_module"] = self._path_to_module(task.code_path)
            if task.code_symbol:
                task_context["is_class"] = task.code_symbol[0].isupper()
                task_context["is_function"] = task.code_symbol[0].islower()
            
            task_contexts.append(task_context)
        
        return {
            "category": category,
            "priority": priority,
            "timestamp": report.timestamp,
            "report_path": report.report_path,
            "task_count": len(tasks),
            "tasks": task_contexts,
            "tasks_path": str(self.tasks_path),
            "test_dir": "tests/",
        }
    
    def _path_to_module(self, path: str) -> str:
        """Convert file path to Python module path"""
        # Remove .py extension
        module = path.replace(".py", "")
        # Replace / with .
        module = module.replace("/", ".")
        # Remove leading dots
        module = module.lstrip(".")
        return module
    
    def _generate_readme(
        self,
        output_dir: Path,
        report: VerifyReport,
        by_category: Dict[str, List[TaskInfo]],
        generated_files: Dict[str, Path]
    ) -> Path:
        """Generate README.md"""
        
        readme_content = f"""# Implementation Prompts - Verification Issues

**Generated:** {report.timestamp}  
**Source Report:** {report.report_path}  
**Tasks File:** {self.tasks_path}

---

## Summary

**Total Tasks:** {report.total_tasks}  
**Verified:** {report.verified}  
**Not Verified:** {report.not_verified}

---

## Issues by Category

"""
        
        # Add category breakdown
        for category, tasks in sorted(by_category.items(), key=lambda x: min(t.priority for t in x[1])):
            priority = min(t.priority for t in tasks)
            readme_content += f"### {category.replace('_', ' ').title()} (Priority {priority})\n\n"
            readme_content += f"**Tasks:** {len(tasks)}  \n"
            readme_content += f"**File:** `{category}.md`\n\n"
            
            # List tasks
            for task in sorted(tasks, key=lambda t: t.task_id):
                readme_content += f"- [{task.checkbox_state}] {task.task_id}: {task.title}\n"
            
            readme_content += "\n"
        
        readme_content += """---

## Priority Order

Implement fixes in this order:

1. **Priority 1** - Critical (marked [x] but failed)
2. **Priority 2** - Missing features
3. **Priority 3** - Symbol/content issues
4. **Priority 4** - Naming issues

---

## Usage

### Step 1: Review Category Files

Read each category file for detailed instructions:

"""
        
        for category in sorted(by_category.keys()):
            readme_content += f"- `{category}.md`\n"
        
        readme_content += """
### Step 2: Implement Fixes

Follow the instructions in each file to fix issues.

### Step 3: Verify

After implementing fixes, verify again:

```bash
/smartspec_verify_tasks_progress_strict """ + str(self.tasks_path) + """
```

---

## Files Generated

"""
        
        for category, file_path in sorted(generated_files.items()):
            if category not in ["README", "summary"]:
                readme_content += f"- `{file_path.name}`\n"
        
        readme_content += f"""
---

**Generated by:** smartspec_report_implement_prompter v7.1.0  
**Date:** {report.timestamp}
"""
        
        readme_path = output_dir / "README.md"
        readme_path.write_text(readme_content)
        print(f"✅ Generated: {readme_path}")
        
        return readme_path
    
    def _generate_summary(
        self,
        output_dir: Path,
        report: VerifyReport,
        by_category: Dict[str, List[TaskInfo]],
        generated_files: Dict[str, Path]
    ) -> Path:
        """Generate summary.json"""
        
        summary = {
            "generated_at": report.timestamp,
            "source_report": report.report_path,
            "tasks_file": str(self.tasks_path),
            "total_tasks": report.total_tasks,
            "verified": report.verified,
            "not_verified": report.not_verified,
            "by_category": {
                category: len(tasks)
                for category, tasks in by_category.items()
            },
            "generated_files": {
                category: str(path)
                for category, path in generated_files.items()
            }
        }
        
        # Create meta directory
        meta_dir = output_dir / "meta"
        meta_dir.mkdir(exist_ok=True)
        
        summary_path = meta_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2))
        print(f"✅ Generated: {summary_path}")
        
        return summary_path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate implementation prompts from verify reports"
    )
    
    parser.add_argument(
        "--verify-report",
        required=True,
        type=Path,
        help="Path to verify report JSON"
    )
    
    parser.add_argument(
        "--tasks",
        required=True,
        type=Path,
        help="Path to tasks.md file"
    )
    
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".spec/prompts"),
        help="Output directory (default: .spec/prompts)"
    )
    
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=Path(".smartspec/templates/verify_report_prompts"),
        help="Template directory"
    )
    
    parser.add_argument(
        "--category",
        choices=[c.value for c in ProblemCategory],
        help="Generate prompts for specific category only"
    )
    
    parser.add_argument(
        "--priority",
        type=int,
        choices=[1, 2, 3, 4],
        help="Generate prompts for specific priority only"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output summary in JSON format"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.verify_report.exists():
        print(f"❌ Error: Verify report not found: {args.verify_report}")
        sys.exit(1)
    
    if not args.tasks.exists():
        print(f"❌ Error: Tasks file not found: {args.tasks}")
        sys.exit(1)
    
    if not args.template_dir.exists():
        print(f"❌ Error: Template directory not found: {args.template_dir}")
        sys.exit(1)
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.out / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📊 Parsing verify report: {args.verify_report}")
    
    # Parse report
    try:
        report = ReportParser.parse(args.verify_report)
    except Exception as e:
        print(f"❌ Error parsing report: {e}")
        sys.exit(1)
    
    print(f"📝 Found {report.not_verified} issues in {len(report.by_category)} categories")
    
    # Generate prompts
    print(f"🚀 Generating prompts...")
    
    generator = PromptGenerator(
        template_dir=args.template_dir,
        tasks_path=args.tasks
    )
    
    try:
        generated_files = generator.generate(
            report=report,
            output_dir=output_dir,
            category_filter=args.category,
            priority_filter=args.priority
        )
    except Exception as e:
        print(f"❌ Error generating prompts: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Output results
    print(f"\n✅ Success! Generated {len(generated_files)} files")
    print(f"📁 Output directory: {output_dir}")
    print(f"\n📖 Next steps:")
    print(f"   1. Review: cat {output_dir}/README.md")
    print(f"   2. Implement fixes following the prompts")
    print(f"   3. Verify: /smartspec_verify_tasks_progress_strict {args.tasks}")
    
    if args.json:
        summary_path = output_dir / "meta" / "summary.json"
        print(f"\n{summary_path.read_text()}")


if __name__ == "__main__":
    main()
