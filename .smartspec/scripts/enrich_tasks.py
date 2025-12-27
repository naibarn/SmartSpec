#!/usr/bin/env python3
"""
SmartSpec Tasks Enrichment Tool
Enrich existing tasks.md with detailed specifications, naming conventions, and architectural guidance.

Usage:
    python3 enrich_tasks.py <tasks_md> [--add-naming-convention] [--add-architecture] [--preview]
"""

import argparse
from datetime import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TasksEnricher:
    def __init__(self, tasks_path: Path, preview: bool = True, repo_root: Optional[Path] = None):
        self.tasks_path = tasks_path
        self.preview = preview
        self.repo_root = repo_root or Path.cwd()
        self.enrichments: List[Dict] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load naming convention standard
        self.naming_standard = self.load_naming_standard()
    
    def load_naming_standard(self) -> Dict:
        """Load naming convention standard"""
        standard_path = self.repo_root / ".smartspec" / "standards" / "naming-convention.md"
        if not standard_path.exists():
            return {}
        
        # Parse standard (simplified - in production, parse markdown properly)
        return {
            'case': 'kebab-case',
            'suffixes': {
                'service': '.service.ts',
                'provider': '.provider.ts',
                'client': '.client.ts',
                'controller': '.controller.ts',
                'middleware': '.middleware.ts',
                'util': '.util.ts',
                'helper': '.helper.ts',
                'model': '.model.ts',
                'schema': '.schema.ts',
                'config': '.config.ts',
            },
            'directories': {
                'service': 'services/',
                'provider': 'providers/',
                'client': 'clients/',
                'controller': 'controllers/',
                'middleware': 'middleware/',
                'util': 'utils/',
                'helper': 'helpers/',
                'model': 'models/',
                'schema': 'schemas/',
                'config': 'config/',
            }
        }
    
    def read_tasks_md(self) -> str:
        """Read tasks.md content"""
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def write_tasks_md(self, content: str):
        """Write updated content to tasks.md"""
        with open(self.tasks_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def parse_tasks(self, content: str) -> List[Dict]:
        """Parse tasks from tasks.md"""
        tasks = []
        
        # Pattern: ### TSK-XXX-NNN: Title
        task_pattern = r'###\s+(TSK-[A-Z]+-\d+):\s+(.+?)(?=\n###|\Z)'
        
        for match in re.finditer(task_pattern, content, re.DOTALL):
            task_id = match.group(1)
            task_content = match.group(0)
            
            # Extract title
            title_match = re.search(r'###\s+TSK-[A-Z]+-\d+:\s+(.+)', task_content)
            title = title_match.group(1).strip() if title_match else "Unknown"
            
            # Extract evidence paths
            evidence_paths = []
            # Pattern 1: inline format (evidence: code path=...)
            evidence_pattern1 = r'evidence:\s+(\w+)\s+path=(.+?)(?:\n|$)'
            # Pattern 2: bullet format (- code: path)
            evidence_pattern2 = r'-\s+(\w+):\s+(.+?)(?:\n|$)'
            
            for ev_match in re.finditer(evidence_pattern1, task_content):
                ev_type = ev_match.group(1)
                ev_path = ev_match.group(2).strip()
                evidence_paths.append({
                    'type': ev_type,
                    'path': ev_path
                })
            
            # If no inline format found, try bullet format
            if not evidence_paths:
                # Look for evidence section first
                if '**Evidence:**' in task_content or '**evidence:**' in task_content:
                    for ev_match in re.finditer(evidence_pattern2, task_content):
                        ev_type = ev_match.group(1)
                        ev_path = ev_match.group(2).strip()
                        evidence_paths.append({
                            'type': ev_type,
                            'path': ev_path
                        })
            
            # Check if already enriched
            has_naming_convention = '**Naming Convention:**' in task_content
            has_architecture = '**Architecture:**' in task_content
            
            tasks.append({
                'task_id': task_id,
                'title': title,
                'content': task_content,
                'evidence_paths': evidence_paths,
                'has_naming_convention': has_naming_convention,
                'has_architecture': has_architecture,
                'start_pos': match.start(),
                'end_pos': match.end()
            })
        
        return tasks
    
    def analyze_evidence_path(self, path: str) -> Dict:
        """Analyze evidence path and suggest improvements"""
        parts = Path(path).parts
        filename = Path(path).name
        stem = Path(path).stem
        suffix = Path(path).suffix
        
        # Determine package
        package = None
        if 'packages' in parts:
            pkg_idx = parts.index('packages')
            if pkg_idx + 1 < len(parts):
                package = parts[pkg_idx + 1]
        
        # Determine directory
        directory = None
        if len(parts) > 2:
            directory = parts[-2]
        
        # Determine file type from filename
        file_type = None
        if suffix in ['.ts', '.js', '.tsx', '.jsx']:
            for type_name, type_suffix in self.naming_standard.get('suffixes', {}).items():
                # Extract type part from suffix (e.g., '.service.ts' -> 'service')
                type_part = type_suffix.replace('.ts', '').replace('.js', '').replace('.tsx', '').replace('.jsx', '').lstrip('.')
                # Check if stem ends with '-{type_part}' (e.g., 'user-service')
                if stem.endswith(f'-{type_part}'):
                    file_type = type_name
                    break
        
        # Check naming convention compliance
        is_kebab_case = re.match(r'^[a-z0-9]+(-[a-z0-9]+)*\.[a-z]+(\.[a-z]+)?$', filename) is not None
        has_suffix = file_type is not None
        
        # Suggest improvements
        suggestions = []
        if not is_kebab_case:
            suggestions.append("Use kebab-case for filename")
        if not has_suffix:
            suggestions.append("Add appropriate suffix (e.g., .service.ts, .provider.ts)")
        if not directory:
            suggestions.append("Place file in appropriate directory")
        
        return {
            'path': path,
            'package': package,
            'directory': directory,
            'filename': filename,
            'file_type': file_type,
            'is_kebab_case': is_kebab_case,
            'has_suffix': has_suffix,
            'compliant': is_kebab_case and has_suffix,
            'suggestions': suggestions
        }
    
    def generate_naming_convention_section(self, evidence_path: str, analysis: Dict) -> str:
        """Generate naming convention section for task"""
        file_type = analysis.get('file_type', 'unknown')
        filename = analysis.get('filename', '')
        
        section = "\n**Naming Convention:**\n"
        
        # Case convention
        if analysis.get('is_kebab_case'):
            section += f"- ✅ Use kebab-case: `{filename}` (correct)\n"
        else:
            section += f"- ❌ Use kebab-case: `{filename}` should be kebab-case\n"
        
        # Suffix
        if analysis.get('has_suffix'):
            suffix = self.naming_standard.get('suffixes', {}).get(file_type, '')
            section += f"- ✅ Use {file_type} suffix: `{suffix}` (correct)\n"
        else:
            section += f"- ❌ Add appropriate suffix (e.g., .service.ts, .provider.ts, .util.ts)\n"
        
        # Directory
        directory = analysis.get('directory', '')
        if directory:
            expected_dir = self.naming_standard.get('directories', {}).get(file_type, '')
            if expected_dir and directory + '/' == expected_dir:
                section += f"- ✅ Place in {expected_dir}: Correct directory\n"
            else:
                section += f"- ⚠️ Place in appropriate directory: Currently in `{directory}/`\n"
        else:
            section += f"- ❌ Place in appropriate directory (e.g., services/, providers/, utils/)\n"
        
        # Implementation note
        section += "\n**Implementation Notes:**\n"
        section += "- Follow naming convention strictly\n"
        section += "- Create file at exact path specified\n"
        section += "- Do not rename or move files without updating tasks.md\n"
        
        return section
    
    def generate_architecture_section(self, evidence_path: str, analysis: Dict) -> str:
        """Generate architecture section for task"""
        package = analysis.get('package', 'unknown')
        directory = analysis.get('directory', 'unknown')
        filename = analysis.get('filename', 'unknown')
        file_type = analysis.get('file_type', 'unknown')
        
        section = "\n**Architecture:**\n"
        
        # Package
        package_type = 'lib' if '-lib' in package else 'service' if '-service' in package else 'unknown'
        package_purpose = {
            'lib': 'Shared code, utilities, models',
            'service': 'Business logic, APIs, controllers',
            'client': 'Client libraries, SDKs'
        }.get(package_type, 'Unknown')
        
        section += f"- **Package:** `{package}` ({package_purpose})\n"
        
        # Directory
        dir_purpose = {
            'services': 'Business logic services',
            'providers': 'External integrations',
            'clients': 'API clients',
            'controllers': 'HTTP controllers',
            'middleware': 'Express middleware',
            'utils': 'Utility functions',
            'helpers': 'Helper functions',
            'models': 'Data models',
            'schemas': 'Validation schemas',
            'config': 'Configuration'
        }.get(directory, 'Unknown')
        
        section += f"- **Directory:** `{directory}/` ({dir_purpose})\n"
        
        # Naming
        section += f"- **Naming:** `{filename}` (kebab-case + {file_type} suffix)\n"
        
        return section
    
    def enrich_task(self, task: Dict, add_naming: bool = True, add_architecture: bool = True) -> Optional[str]:
        """Enrich a single task with additional information"""
        if not task['evidence_paths']:
            return None
        
        # Skip if already enriched
        if add_naming and task['has_naming_convention']:
            return None
        if add_architecture and task['has_architecture']:
            return None
        
        # Analyze first evidence path (usually code)
        first_evidence = task['evidence_paths'][0]
        analysis = self.analyze_evidence_path(first_evidence['path'])
        
        # Generate enrichment sections
        enrichment = ""
        
        if add_architecture and not task['has_architecture']:
            enrichment += self.generate_architecture_section(first_evidence['path'], analysis)
        
        if add_naming and not task['has_naming_convention']:
            enrichment += self.generate_naming_convention_section(first_evidence['path'], analysis)
        
        if not enrichment:
            return None
        
        # Find insertion point (after title, before evidence)
        content = task['content']
        
        # Insert after title line
        lines = content.split('\n')
        title_line_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('###'):
                title_line_idx = i
                break
        
        # Find evidence section
        evidence_line_idx = len(lines)
        for i, line in enumerate(lines):
            if 'evidence:' in line.lower():
                evidence_line_idx = i
                break
        
        # Insert enrichment before evidence
        insert_idx = evidence_line_idx
        
        # If there's already a description, insert after it
        if title_line_idx + 1 < evidence_line_idx:
            # There's content between title and evidence
            insert_idx = evidence_line_idx
        else:
            # No content, insert right after title
            insert_idx = title_line_idx + 1
        
        enriched_lines = lines[:insert_idx] + [enrichment] + lines[insert_idx:]
        enriched_content = '\n'.join(enriched_lines)
        
        self.enrichments.append({
            'task_id': task['task_id'],
            'title': task['title'],
            'evidence_path': first_evidence['path'],
            'analysis': analysis,
            'enrichment': enrichment
        })
        
        return enriched_content
    
    def enrich_all_tasks(self, content: str, add_naming: bool = True, add_architecture: bool = True) -> str:
        """Enrich all tasks in tasks.md"""
        tasks = self.parse_tasks(content)
        
        print(f"📋 Found {len(tasks)} tasks")
        
        enriched_content = content
        offset = 0
        
        for task in tasks:
            enriched_task = self.enrich_task(task, add_naming, add_architecture)
            
            if enriched_task:
                # Replace task content
                start = task['start_pos'] + offset
                end = task['end_pos'] + offset
                
                enriched_content = (
                    enriched_content[:start] +
                    enriched_task +
                    enriched_content[end:]
                )
                
                # Update offset
                offset += len(enriched_task) - len(task['content'])
                
                print(f"   ✓ Enriched {task['task_id']}: {task['title']}")
        
        return enriched_content
    
    def generate_report(self, add_naming: bool, add_architecture: bool) -> str:
        """Generate markdown report of enrichments"""
        md = "# Tasks Enrichment Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Tasks File:** `{self.tasks_path}`\n"
        md += f"**Status:** {'✅ Applied' if not self.preview else '👁️ Preview Only'}\n\n"
        md += "---\n\n"
        
        # Summary
        md += "## Summary\n\n"
        md += f"- **Total tasks enriched:** {len(self.enrichments)}\n"
        md += f"- **Added naming convention:** {'Yes' if add_naming else 'No'}\n"
        md += f"- **Added architecture:** {'Yes' if add_architecture else 'No'}\n"
        md += f"- **Changes applied:** {'Yes' if not self.preview else 'No (preview mode)'}\n\n"
        
        # Enrichments
        if self.enrichments:
            md += "## Enrichments Made\n\n"
            
            for enrichment in self.enrichments[:10]:
                task_id = enrichment['task_id']
                title = enrichment['title']
                evidence_path = enrichment['evidence_path']
                analysis = enrichment['analysis']
                
                md += f"### {task_id}: {title}\n\n"
                md += f"**Evidence:** `{evidence_path}`\n\n"
                
                if analysis.get('compliant'):
                    md += "**Status:** ✅ Compliant with naming convention\n\n"
                else:
                    md += "**Status:** ⚠️ Needs attention\n\n"
                    if analysis.get('suggestions'):
                        md += "**Suggestions:**\n"
                        for suggestion in analysis['suggestions']:
                            md += f"- {suggestion}\n"
                        md += "\n"
            
            if len(self.enrichments) > 10:
                md += f"... and {len(self.enrichments) - 10} more\n\n"
        else:
            md += "No enrichments made (all tasks already enriched).\n\n"
        
        # Next Steps
        md += "## Next Steps\n\n"
        if self.preview:
            md += "This was a preview. To apply enrichments, run with `--apply` flag.\n\n"
        else:
            md += "1. **Review enriched tasks:**\n"
            md += f"   ```bash\n   cat {self.tasks_path}\n   ```\n\n"
            md += "2. **Verify changes:**\n"
            md += f"   ```bash\n   git diff {self.tasks_path}\n   ```\n\n"
            md += "3. **Commit changes:**\n"
            md += "   ```bash\n"
            md += "   git add tasks.md\n"
            md += '   git commit -m "docs: Enrich tasks with naming convention and architecture"\n'
            md += "   ```\n\n"
        
        return md
    
    def save_report(self):
        """Save report to file"""
        # Use tasks_path parent if repo_root is not valid
        if not self.repo_root or self.repo_root == Path('/'):
            self.repo_root = self.tasks_path.parent.parent.parent
        
        spec_name = self.tasks_path.parent.name
        report_dir = self.repo_root / ".spec" / "reports" / "tasks-enrichment" / spec_name
        
        try:
            report_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # Fallback to /tmp
            report_dir = Path("/tmp") / "smartspec-reports" / "tasks-enrichment" / spec_name
            report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"enrichment_{self.timestamp}.md"
        report_content = self.generate_report(True, True)
        report_file.write_text(report_content, encoding='utf-8')
        
        print(f"\n📄 Report saved: {report_file}")
        return report_file
    
    def run(self, add_naming: bool = True, add_architecture: bool = True):
        """Main execution flow"""
        try:
            # Read tasks.md
            print(f"📖 Reading tasks: {self.tasks_path}")
            content = self.read_tasks_md()
            
            # Enrich tasks
            print("🔧 Enriching tasks...")
            enriched_content = self.enrich_all_tasks(content, add_naming, add_architecture)
            
            if not self.enrichments:
                print("ℹ️  No tasks to enrich (all tasks already enriched)")
                return 0
            
            print(f"\n✅ Enriched {len(self.enrichments)} tasks")
            
            # Apply or preview
            if not self.preview:
                self.write_tasks_md(enriched_content)
                print(f"✅ Applied enrichments to {self.tasks_path}")
            else:
                print(f"👁️  Preview mode: {len(self.enrichments)} enrichments ready to apply")
            
            # Generate report
            self.save_report()
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1


def main():
    parser = argparse.ArgumentParser(
        description='Enrich tasks.md with naming convention and architectural guidance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview enrichments
  python3 enrich_tasks.py tasks.md --preview
  
  # Apply enrichments
  python3 enrich_tasks.py tasks.md --apply
  
  # Add only naming convention
  python3 enrich_tasks.py tasks.md --add-naming-convention --apply
  
  # Add only architecture
  python3 enrich_tasks.py tasks.md --add-architecture --apply
        """
    )
    
    parser.add_argument('tasks', type=Path, help='Path to tasks.md file')
    parser.add_argument('--add-naming-convention', action='store_true', help='Add naming convention guidance')
    parser.add_argument('--add-architecture', action='store_true', help='Add architectural guidance')
    parser.add_argument('--preview', action='store_true', help='Preview mode (default: apply)')
    parser.add_argument('--apply', action='store_true', help='Apply enrichments')
    
    args = parser.parse_args()
    
    # Default: add both if neither specified
    add_naming = args.add_naming_convention or not args.add_architecture
    add_architecture = args.add_architecture or not args.add_naming_convention
    
    # Default: preview unless --apply specified
    preview = not args.apply
    
    # Validate input
    if not args.tasks.exists():
        print(f"❌ Error: tasks.md not found: {args.tasks}", file=sys.stderr)
        return 1
    
    # Detect repo root
    repo_root = Path.cwd()
    for _ in range(3):
        if (repo_root / ".smartspec").exists() or (repo_root / "packages").exists():
            break
        repo_root = repo_root.parent
    
    # Run enricher
    enricher = TasksEnricher(args.tasks, preview, repo_root)
    return enricher.run(add_naming, add_architecture)


if __name__ == '__main__':
    sys.exit(main())
