#!/usr/bin/env python3
"""
SmartSpec Evidence Type Fixer
Automatically detects and fixes evidence type mismatches in tasks.md

Usage:
    python3 fix_evidence_type.py <tasks_md> <repo_root> [--apply]
    
Examples:
    # Preview fixes
    python3 fix_evidence_type.py specs/core/spec-core-001-authentication/tasks.md /path/to/repo
    
    # Apply fixes
    python3 fix_evidence_type.py specs/core/spec-core-001-authentication/tasks.md /path/to/repo --apply
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class EvidenceTypeFixer:
    """Fix evidence type mismatches in tasks.md"""
    
    def __init__(self, tasks_path: Path, repo_root: Path, apply: bool = False):
        self.tasks_path = tasks_path
        self.repo_root = repo_root
        self.apply = apply
        self.fixes: List[Dict] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def detect_correct_evidence_type(self, file_path: str) -> str:
        """
        Determine correct evidence type based on file path and content
        
        Rules (priority order):
        1. Test files: tests/, .test.ts, .spec.ts, .e2e.ts → test
        2. Documentation files: docs/, .md, .yaml, .yml → docs
        3. UI files: .html, .css, /ui/, /views/ → ui
        4. Everything else → code
        """
        file_path_lower = file_path.lower()
        
        # Test files (highest priority)
        if '/tests/' in file_path_lower or \
           '/test/' in file_path_lower or \
           file_path_lower.endswith('.test.ts') or \
           file_path_lower.endswith('.spec.ts') or \
           file_path_lower.endswith('.e2e.ts') or \
           file_path_lower.endswith('.integration.ts') or \
           file_path_lower.endswith('.unit.ts'):
            return 'test'
        
        # Documentation files (second priority)
        # Check directory first
        if '/docs/' in file_path_lower or \
           '/doc/' in file_path_lower or \
           '/specs/' in file_path_lower:
            # Then check extension for docs types
            if file_path_lower.endswith('.md') or \
               file_path_lower.endswith('.yaml') or \
               file_path_lower.endswith('.yml') or \
               file_path_lower.endswith('.txt'):
                return 'docs'
        
        # Also check extension alone for .md files
        if file_path_lower.endswith('.md') or \
           file_path_lower.endswith('.yaml') or \
           file_path_lower.endswith('.yml'):
            return 'docs'
        
        # UI files (third priority)
        if file_path_lower.endswith('.html') or \
           file_path_lower.endswith('.css') or \
           file_path_lower.endswith('.scss') or \
           file_path_lower.endswith('.sass') or \
           '/ui/' in file_path_lower or \
           '/views/' in file_path_lower or \
           '/components/' in file_path_lower:
            return 'ui'
        
        # Default: code
        return 'code'
    
    def parse_evidence_line(self, line: str) -> Optional[Dict]:
        """Parse evidence line and extract type and path"""
        # Match: evidence: <type> path=<path> [contains=<pattern>] [symbol=<symbol>]
        match = re.match(
            r'\s*evidence:\s+(\w+)\s+path=([^\s]+)(?:\s+contains=([^\s]+))?(?:\s+symbol=([^\s]+))?',
            line
        )
        
        if not match:
            return None
        
        return {
            'type': match.group(1),
            'path': match.group(2),
            'contains': match.group(3),
            'symbol': match.group(4),
            'raw_line': line
        }
    
    def detect_type_mismatch(
        self,
        task_id: str,
        evidence: Dict
    ) -> Optional[Dict]:
        """
        Detect if evidence type is incorrect
        
        Returns:
            Dict with mismatch info or None if no mismatch
        """
        current_type = evidence['type']
        evidence_path = evidence['path']
        
        # Check if file exists
        full_path = self.repo_root / evidence_path
        if not full_path.exists():
            return None
        
        # Determine correct type
        correct_type = self.detect_correct_evidence_type(evidence_path)
        
        # Check for mismatch
        if current_type != correct_type:
            return {
                'task_id': task_id,
                'evidence_path': evidence_path,
                'current_type': current_type,
                'correct_type': correct_type,
                'raw_line': evidence['raw_line'],
                'contains': evidence['contains'],
                'symbol': evidence['symbol']
            }
        
        return None
    
    def fix_evidence_type_in_line(self, line: str, current_type: str, correct_type: str) -> str:
        """Fix evidence type in a single line"""
        # Replace evidence type
        pattern = rf'(evidence:\s+){current_type}(\s+)'
        replacement = rf'\1{correct_type}\2'
        return re.sub(pattern, replacement, line)
    
    def scan_tasks_md(self) -> List[Dict]:
        """Scan tasks.md for evidence type mismatches"""
        mismatches = []
        
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_task_id = None
        
        for i, line in enumerate(lines):
            # Check if this is a task line
            task_match = re.match(r'- \[([ x])\]\s+\*\*([A-Z]+-[A-Z]+-\d+)\*\*', line)
            if task_match:
                current_task_id = task_match.group(2)
                continue
            
            # Check if this is an evidence line
            if current_task_id and 'evidence:' in line:
                evidence = self.parse_evidence_line(line)
                if evidence:
                    mismatch = self.detect_type_mismatch(current_task_id, evidence)
                    if mismatch:
                        mismatch['line_number'] = i + 1
                        mismatches.append(mismatch)
        
        return mismatches
    
    def apply_fixes(self, mismatches: List[Dict]) -> int:
        """Apply fixes to tasks.md"""
        if not mismatches:
            return 0
        
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        fixed_count = 0
        
        for mismatch in mismatches:
            line_idx = mismatch['line_number'] - 1
            if line_idx < len(lines):
                old_line = lines[line_idx]
                new_line = self.fix_evidence_type_in_line(
                    old_line,
                    mismatch['current_type'],
                    mismatch['correct_type']
                )
                
                if old_line != new_line:
                    lines[line_idx] = new_line
                    fixed_count += 1
        
        if fixed_count > 0:
            with open(self.tasks_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        
        return fixed_count
    
    def generate_report(self, mismatches: List[Dict]) -> str:
        """Generate report of evidence type mismatches"""
        report = []
        report.append("=" * 60)
        report.append("Evidence Type Fixer Report")
        report.append("=" * 60)
        report.append(f"Tasks file: {self.tasks_path}")
        report.append(f"Repository: {self.repo_root}")
        report.append(f"Timestamp: {self.timestamp}")
        report.append(f"Mode: {'APPLY' if self.apply else 'PREVIEW'}")
        report.append("")
        
        if not mismatches:
            report.append("✅ No evidence type mismatches found!")
            report.append("")
            return "\n".join(report)
        
        report.append(f"⚠️  Found {len(mismatches)} evidence type mismatch(es)")
        report.append("")
        
        for i, mismatch in enumerate(mismatches, 1):
            report.append(f"{i}. Task: {mismatch['task_id']}")
            report.append(f"   File: {mismatch['evidence_path']}")
            report.append(f"   Line: {mismatch['line_number']}")
            report.append(f"   Current type: {mismatch['current_type']}")
            report.append(f"   Correct type: {mismatch['correct_type']}")
            report.append("")
        
        if self.apply:
            report.append(f"✅ Fixed {len(mismatches)} evidence type mismatch(es)")
        else:
            report.append("ℹ️  Run with --apply to fix these mismatches")
        
        report.append("")
        return "\n".join(report)
    
    def run(self) -> int:
        """Run the evidence type fixer"""
        print(f"Scanning {self.tasks_path}...")
        
        # Scan for mismatches
        mismatches = self.scan_tasks_md()
        
        # Generate report
        report = self.generate_report(mismatches)
        print(report)
        
        # Apply fixes if requested
        if self.apply and mismatches:
            fixed_count = self.apply_fixes(mismatches)
            print(f"\n✅ Applied {fixed_count} fix(es) to {self.tasks_path}")
            return fixed_count
        
        return len(mismatches)


def main():
    parser = argparse.ArgumentParser(
        description='Fix evidence type mismatches in tasks.md'
    )
    parser.add_argument(
        'tasks_md',
        type=Path,
        help='Path to tasks.md file'
    )
    parser.add_argument(
        'repo_root',
        type=Path,
        help='Path to repository root'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply fixes (default: preview only)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not args.tasks_md.exists():
        print(f"Error: tasks.md not found: {args.tasks_md}", file=sys.stderr)
        return 1
    
    if not args.repo_root.exists():
        print(f"Error: repository root not found: {args.repo_root}", file=sys.stderr)
        return 1
    
    # Run fixer
    fixer = EvidenceTypeFixer(args.tasks_md, args.repo_root, args.apply)
    mismatch_count = fixer.run()
    
    return 0 if args.apply or mismatch_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
