#!/usr/bin/env python3
"""
SmartSpec Naming Issues Fixer
Automatically fixes naming issues by updating evidence paths in tasks.md
based on verification report findings.

Usage:
    python3 fix_naming_issues.py <tasks_md> --from-report <report_path> [--apply]
"""

import argparse
from datetime import datetime
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class NamingIssuesFixer:
    def __init__(self, tasks_path: Path, report_path: Path, apply: bool = False, repo_root: Optional[Path] = None):
        self.tasks_path = tasks_path
        self.report_path = report_path
        self.apply = apply
        self.repo_root = repo_root or Path.cwd()
        self.changes: List[Dict] = []
        self.naming_issues: List[Dict] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def read_report(self) -> Dict:
        """Read verification report (JSON or Markdown)"""
        if self.report_path.suffix == '.json':
            with open(self.report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif self.report_path.suffix == '.md':
            # Parse markdown report to extract naming issues
            return self.parse_markdown_report()
        else:
            raise ValueError(f"Unsupported report format: {self.report_path.suffix}")
    
    def parse_markdown_report(self) -> Dict:
        """Parse markdown report to extract naming issues"""
        with open(self.report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract naming issues from markdown
        naming_issues = []
        
        # Pattern: → Update evidence path to: /full/path/to/file.ts
        pattern = r'→ Update evidence path to: (.+?)(?:\n|$)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            full_path = match.group(1).strip()
            # Extract relative path from full path
            # Example: /home/user/project/packages/auth-lib/src/file.ts
            #       -> packages/auth-lib/src/file.ts
            
            # Find "packages/" or "specs/" in path
            if 'packages/' in full_path:
                relative_path = full_path[full_path.index('packages/'):]
            elif 'specs/' in full_path:
                relative_path = full_path[full_path.index('specs/'):]
            else:
                relative_path = full_path
            
            naming_issues.append({
                'found_path': relative_path
            })
        
        # Also extract "OR rename file to match evidence" patterns
        rename_pattern = r'OR rename file to match evidence: (.+?)(?:\n|$)'
        rename_matches = re.finditer(rename_pattern, content)
        
        for i, match in enumerate(rename_matches):
            expected_path = match.group(1).strip()
            if i < len(naming_issues):
                naming_issues[i]['expected_path'] = expected_path
        
        return {'naming_issues': naming_issues}
    
    def extract_naming_issues(self, report: Dict) -> List[Dict]:
        """Extract naming issues from report"""
        naming_issues = []
        
        # Check if report has 'tasks' field (JSON format)
        if 'tasks' in report:
            for task in report['tasks']:
                if task.get('category') == 'naming_issue':
                    # Extract paths from suggestions
                    suggestions = task.get('suggestions', [])
                    expected_path = None
                    found_path = None
                    
                    for suggestion in suggestions:
                        if '→ Update evidence path to:' in suggestion:
                            # Extract path after "to:"
                            match = re.search(r'→ Update evidence path to: (.+?)(?:\n|$)', suggestion)
                            if match:
                                full_path = match.group(1).strip()
                                # Extract relative path
                                if 'packages/' in full_path:
                                    found_path = full_path[full_path.index('packages/'):]
                                elif 'specs/' in full_path:
                                    found_path = full_path[full_path.index('specs/'):]
                        
                        if 'OR rename file to match evidence:' in suggestion:
                            match = re.search(r'OR rename file to match evidence: (.+?)(?:\n|$)', suggestion)
                            if match:
                                expected_path = match.group(1).strip()
                    
                    if expected_path and found_path:
                        naming_issues.append({
                            'task_id': task.get('task_id'),
                            'title': task.get('title'),
                            'expected_path': expected_path,
                            'found_path': found_path
                        })
        
        # Check if report has 'naming_issues' field (parsed markdown)
        elif 'naming_issues' in report:
            naming_issues = report['naming_issues']
        
        # Check if report has 'not_verified' field (simple JSON format)
        elif 'not_verified' in report:
            for item in report['not_verified']:
                if item.get('reason') == 'naming_issue':
                    expected = item.get('expected_path')
                    found = item.get('found_path')
                    if expected and found:
                        naming_issues.append({
                            'task_id': item.get('task'),
                            'title': item.get('task'),
                            'expected_path': expected,
                            'found_path': found
                        })
        
        return naming_issues
    
    def read_tasks_md(self) -> str:
        """Read tasks.md content"""
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def find_evidence_lines(self, content: str, expected_path: str) -> List[Tuple[int, str]]:
        """Find all evidence lines that match the expected path"""
        lines = content.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if 'evidence:' in line and expected_path in line:
                matches.append((i, line))
        
        return matches
    
    def update_evidence_path(self, content: str, expected_path: str, found_path: str) -> Tuple[str, int]:
        """Update evidence path in content"""
        lines = content.split('\n')
        updated_count = 0
        
        for i, line in enumerate(lines):
            if 'evidence:' in line and expected_path in line:
                # Replace expected_path with found_path
                new_line = line.replace(expected_path, found_path)
                lines[i] = new_line
                updated_count += 1
                
                self.changes.append({
                    'line': i + 1,
                    'old': line,
                    'new': new_line,
                    'expected_path': expected_path,
                    'found_path': found_path
                })
        
        return '\n'.join(lines), updated_count
    
    def write_tasks_md(self, content: str):
        """Write updated content to tasks.md"""
        with open(self.tasks_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def print_preview(self):
        """Print preview of changes"""
        print("\n" + "="*80)
        print("PREVIEW: Evidence Path Updates")
        print("="*80 + "\n")
        
        if not self.changes:
            print("❌ No changes to apply.")
            return
        
        for i, change in enumerate(self.changes, 1):
            print(f"{i}. Line {change['line']}:")
            print(f"   Expected: {change['expected_path']}")
            print(f"   Found:    {change['found_path']}")
            print(f"   Old: {change['old'].strip()}")
            print(f"   New: {change['new'].strip()}")
            print()
        
        print("="*80)
        print(f"Total changes: {len(self.changes)}")
        print("="*80 + "\n")
        
        if not self.apply:
            print("ℹ️  This is preview mode. Use --apply to make changes.")
    
    def print_summary(self):
        """Print summary after applying changes"""
        print("\n" + "="*80)
        print("✅ APPLIED: Evidence Path Updates")
        print("="*80 + "\n")
        
        print(f"Total changes applied: {len(self.changes)}")
        print(f"File updated: {self.tasks_path}")
        print()
        
        print("Next steps:")
        print("1. Verify changes:")
        print(f"   /smartspec_verify_tasks_progress_strict {self.tasks_path} --json")
        print()
        print("2. Review diff:")
        print(f"   git diff {self.tasks_path}")
        print()
        print("3. Commit changes:")
        print("   git add tasks.md")
        print('   git commit -m "fix: Update evidence paths to match actual files"')
        print()
        print("="*80 + "\n")
    
    def generate_report(self) -> str:
        """Generate markdown report of changes"""
        md = "# Fix Naming Issues Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Tasks File:** `{self.tasks_path}`\n"
        md += f"**Source Report:** `{self.report_path}`\n"
        md += f"**Status:** {'✅ Applied' if self.apply else '👁️ Preview Only'}\n\n"
        
        md += "---\n\n"
        
        # Summary
        md += "## Summary\n\n"
        md += f"- **Total naming issues found:** {len(self.naming_issues)}\n"
        md += f"- **Evidence paths updated:** {len(self.changes)}\n"
        md += f"- **Changes applied:** {'Yes' if self.apply else 'No (preview mode)'}\n\n"
        
        # Changes Made
        md += "## Changes Made\n\n"
        if self.changes:
            md += "Updated evidence paths to match actual file names:\n\n"
            
            # Group by type
            test_changes = [c for c in self.changes if 'test' in c['expected_path'].lower()]
            code_changes = [c for c in self.changes if 'test' not in c['expected_path'].lower() and not c['expected_path'].endswith('.md')]
            doc_changes = [c for c in self.changes if c['expected_path'].endswith('.md')]
            
            if test_changes:
                md += f"### Test Files ({len(test_changes)} changes)\n\n"
                for change in test_changes[:10]:  # Show first 10
                    md += f"- `{change['expected_path']}` → `{change['found_path']}`\n"
                if len(test_changes) > 10:
                    md += f"- ... and {len(test_changes) - 10} more\n"
                md += "\n"
            
            if code_changes:
                md += f"### Code Files ({len(code_changes)} changes)\n\n"
                for change in code_changes[:10]:
                    md += f"- `{change['expected_path']}` → `{change['found_path']}`\n"
                if len(code_changes) > 10:
                    md += f"- ... and {len(code_changes) - 10} more\n"
                md += "\n"
            
            if doc_changes:
                md += f"### Documentation ({len(doc_changes)} changes)\n\n"
                for change in doc_changes:
                    md += f"- `{change['expected_path']}` → `{change['found_path']}`\n"
                md += "\n"
        else:
            md += "No changes made.\n\n"
        
        # Next Steps
        md += "## Next Steps\n\n"
        if self.apply:
            md += "1. **Verify changes:**\n"
            md += f"   ```bash\n   /smartspec_verify_tasks_progress_strict {self.tasks_path} --json\n   ```\n\n"
            md += "2. **Review diff:**\n"
            md += f"   ```bash\n   git diff {self.tasks_path}\n   ```\n\n"
            md += "3. **Commit changes:**\n"
            md += "   ```bash\n"
            md += "   git add tasks.md\n"
            md += '   git commit -m "fix: Update evidence paths to match actual files"\n'
            md += "   ```\n\n"
        else:
            md += "This was a preview. To apply changes, run with `--apply` flag.\n\n"
        
        return md
    
    def save_report(self):
        """Save report to file"""
        # Determine report directory
        spec_name = self.tasks_path.parent.name
        report_dir = self.repo_root / ".spec" / "reports" / "fix-naming-issues" / spec_name
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate report filename
        report_file = report_dir / f"fix_naming_{self.timestamp}.md"
        
        # Generate and save report
        report_content = self.generate_report()
        report_file.write_text(report_content, encoding='utf-8')
        
        print(f"\n📄 Report saved: {report_file}")
        return report_file
    
    def run(self):
        """Main execution flow"""
        try:
            # Read report
            print(f"📄 Reading report: {self.report_path}")
            report = self.read_report()
            
            # Extract naming issues
            print("🔍 Extracting naming issues...")
            naming_issues = self.extract_naming_issues(report)
            self.naming_issues = naming_issues  # Save for report generation
            
            if not naming_issues:
                print("❌ No naming issues found in report.")
                return 1
            
            print(f"✅ Found {len(naming_issues)} naming issues")
            print()
            
            # Read tasks.md
            print(f"📖 Reading tasks: {self.tasks_path}")
            content = self.read_tasks_md()
            
            # Update evidence paths
            print("🔧 Updating evidence paths...")
            for issue in naming_issues:
                expected = issue.get('expected_path')
                found = issue.get('found_path')
                
                if not expected or not found:
                    continue
                
                content, count = self.update_evidence_path(content, expected, found)
                
                if count > 0:
                    print(f"   ✓ {expected} → {found} ({count} occurrences)")
            
            # Preview or apply
            if self.apply:
                self.write_tasks_md(content)
                self.print_summary()
            else:
                self.print_preview()
            
            # Generate report
            self.save_report()
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1


def resolve_latest_report(report_path: Path) -> Path:
    """
    Resolve wildcard pattern to latest file.
    If path contains wildcard (*), expand and return newest file.
    Otherwise, return path as-is.
    """
    path_str = str(report_path)
    
    # Check if path contains wildcard
    if '*' not in path_str:
        return report_path
    
    # Expand wildcard
    matches = glob.glob(path_str)
    
    if not matches:
        print(f"⚠️  Warning: No files match pattern: {path_str}")
        print(f"   Using original path: {report_path}")
        return report_path
    
    if len(matches) == 1:
        resolved = Path(matches[0])
        print(f"ℹ️  Resolved: {report_path} → {resolved.name}")
        return resolved
    
    # Multiple matches - sort by modification time (newest first)
    matches.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    latest = Path(matches[0])
    
    print(f"ℹ️  Found {len(matches)} files matching pattern: {path_str}")
    print(f"   Using latest: {latest.name} (modified: {os.path.getmtime(str(latest))})")
    print(f"   Other files:")
    for f in matches[1:4]:  # Show up to 3 older files
        print(f"     - {Path(f).name} (modified: {os.path.getmtime(f)})")
    if len(matches) > 4:
        print(f"     ... and {len(matches) - 4} more")
    print()
    
    return latest


def main():
    parser = argparse.ArgumentParser(
        description='Fix naming issues by updating evidence paths in tasks.md',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes
  python3 fix_naming_issues.py tasks.md --from-report report.json
  
  # Apply changes
  python3 fix_naming_issues.py tasks.md --from-report report.json --apply
  
  # From markdown report
  python3 fix_naming_issues.py tasks.md --from-report batch_execution.md --apply
        """
    )
    
    parser.add_argument(
        'tasks',
        type=Path,
        help='Path to tasks.md file'
    )
    
    parser.add_argument(
        '--from-report',
        type=Path,
        required=True,
        help='Path to verification report (JSON or Markdown)'
    )
    
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes (default: preview only)'
    )
    
    args = parser.parse_args()
    
    # Resolve wildcard in report path
    report_path = resolve_latest_report(args.from_report)
    
    # Validate inputs
    if not args.tasks.exists():
        print(f"❌ Error: tasks.md not found: {args.tasks}", file=sys.stderr)
        return 1
    
    if not report_path.exists():
        print(f"❌ Error: report not found: {report_path}", file=sys.stderr)
        return 1
    
    # Detect repo root
    repo_root = Path.cwd()
    if (repo_root / ".spec").exists():
        # Already at repo root
        pass
    elif (repo_root.parent / ".spec").exists():
        repo_root = repo_root.parent
    elif (repo_root.parent.parent / ".spec").exists():
        repo_root = repo_root.parent.parent
    
    # Run fixer
    fixer = NamingIssuesFixer(args.tasks, report_path, args.apply, repo_root)
    return fixer.run()


if __name__ == '__main__':
    sys.exit(main())
