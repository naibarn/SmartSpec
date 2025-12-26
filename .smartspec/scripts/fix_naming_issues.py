#!/usr/bin/env python3
"""
SmartSpec Naming Issues Fixer
Automatically fixes naming issues by updating evidence paths in tasks.md
based on verification report findings.

Usage:
    python3 fix_naming_issues.py <tasks_md> --from-report <report_path> [--apply]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class NamingIssuesFixer:
    def __init__(self, tasks_path: Path, report_path: Path, apply: bool = False):
        self.tasks_path = tasks_path
        self.report_path = report_path
        self.apply = apply
        self.changes: List[Dict] = []
        
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
    
    def run(self):
        """Main execution flow"""
        try:
            # Read report
            print(f"📄 Reading report: {self.report_path}")
            report = self.read_report()
            
            # Extract naming issues
            print("🔍 Extracting naming issues...")
            naming_issues = self.extract_naming_issues(report)
            
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
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1


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
    
    # Validate inputs
    if not args.tasks.exists():
        print(f"❌ Error: tasks.md not found: {args.tasks}", file=sys.stderr)
        return 1
    
    if not args.from_report.exists():
        print(f"❌ Error: report not found: {args.from_report}", file=sys.stderr)
        return 1
    
    # Run fixer
    fixer = NamingIssuesFixer(args.tasks, args.from_report, args.apply)
    return fixer.run()


if __name__ == '__main__':
    sys.exit(main())
