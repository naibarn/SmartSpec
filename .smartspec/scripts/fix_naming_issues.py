#!/usr/bin/env python3
"""
SmartSpec Naming Issues Fixer (Enhanced)
Automatically fixes naming issues by updating evidence paths in tasks.md
based on verification report findings.

Enhanced Features:
- Improved fuzzy matching with weighted similarity
- Cross-package search capability
- Multi-candidate selection with confidence levels
- Comprehensive reporting with manual review guidance

Usage:
    python3 fix_naming_issues_enhanced.py <tasks_md> --from-report <report_path> [--apply]
"""

import argparse
from datetime import datetime
import difflib
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set


class EnhancedNamingIssuesFixer:
    # Similarity thresholds
    SIMILARITY_THRESHOLD_HIGH = 0.70  # Auto-fix with high confidence
    SIMILARITY_THRESHOLD_MEDIUM = 0.60  # Auto-fix with medium confidence
    SIMILARITY_THRESHOLD_LOW = 0.50  # Show in report for manual review
    
    # Semantic word groups for better matching
    SEMANTIC_GROUPS = {
        'auth': {'api', 'auth', 'authentication', 'authorize', 'oauth', 'jwt'},
        'middleware': {'handler', 'interceptor', 'guard', 'middleware', 'filter'},
        'service': {'provider', 'manager', 'controller', 'service', 'handler'},
        'test': {'spec', 'test', 'e2e', 'integration', 'unit'},
        'util': {'helper', 'utility', 'utils', 'util', 'tool'},
    }
    
    def __init__(self, tasks_path: Path, report_path: Path, apply: bool = False, repo_root: Optional[Path] = None):
        self.tasks_path = tasks_path
        self.report_path = report_path
        self.apply = apply
        self.repo_root = repo_root or Path.cwd()
        self.changes: List[Dict] = []
        self.naming_issues: List[Dict] = []
        self.auto_fixed: List[Dict] = []
        self.manual_review: List[Dict] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def are_semantically_similar(self, word1: str, word2: str) -> bool:
        """Check if two words are semantically similar"""
        word1_lower = word1.lower()
        word2_lower = word2.lower()
        
        # Exact match
        if word1_lower == word2_lower:
            return True
        
        # Check if both words belong to same semantic group
        for group, words in self.SEMANTIC_GROUPS.items():
            if word1_lower in words and word2_lower in words:
                return True
        
        return False
    
    def extract_keywords(self, path: str) -> Set[str]:
        """Extract keywords from path for similarity matching"""
        # Split by / - . _
        parts = re.split(r'[/\-._]', path.lower())
        # Remove common words and empty strings
        stopwords = {'src', 'lib', 'test', 'tests', 'unit', 'integration', 'packages', 'ts', 'js'}
        keywords = {p for p in parts if p and p not in stopwords and len(p) > 2}
        return keywords
    
    def calculate_similarity(self, expected: str, found: str) -> float:
        """Calculate weighted similarity between two paths with semantic understanding"""
        expected_path = Path(expected)
        found_path = Path(found)
        
        # Special Rule 1: Same base name, different suffix
        # e.g., rate-limit.middleware.ts vs rate-limit.ts
        expected_base = expected_path.stem.replace('.middleware', '').replace('.service', '').replace('.provider', '')
        found_base = found_path.stem.replace('.middleware', '').replace('.service', '').replace('.provider', '')
        
        if expected_base == found_base and expected_path.suffix == found_path.suffix:
            # Same base name, only suffix difference
            return 0.95
        
        # Special Rule 2: Semantic word matching in filename
        expected_words = re.split(r'[-_.]', expected_path.stem.lower())
        found_words = re.split(r'[-_.]', found_path.stem.lower())
        
        semantic_matches = 0
        total_words = max(len(expected_words), len(found_words))
        
        for i in range(min(len(expected_words), len(found_words))):
            if self.are_semantically_similar(expected_words[i], found_words[i]):
                semantic_matches += 1
        
        semantic_filename_sim = semantic_matches / total_words if total_words > 0 else 0.0
        
        # 1. Filename similarity (30% character-based + 20% semantic)
        expected_name = expected_path.stem
        found_name = found_path.stem
        char_filename_sim = difflib.SequenceMatcher(None, expected_name, found_name).ratio()
        filename_sim = char_filename_sim * 0.6 + semantic_filename_sim * 0.4
        
        # 2. Directory similarity (20%)
        expected_dir = str(expected_path.parent)
        found_dir = str(found_path.parent)
        dir_sim = difflib.SequenceMatcher(None, expected_dir, found_dir).ratio()
        
        # 3. Extension similarity (10%)
        ext_sim = 1.0 if expected_path.suffix == found_path.suffix else 0.0
        
        # 4. Keywords similarity (20%)
        expected_keywords = self.extract_keywords(expected)
        found_keywords = self.extract_keywords(found)
        if expected_keywords:
            keyword_sim = len(expected_keywords & found_keywords) / len(expected_keywords)
        else:
            keyword_sim = 0.0
        
        # Weighted average (total 100%)
        total_sim = (
            filename_sim * 0.5 +  # 50% (30% char + 20% semantic)
            dir_sim * 0.2 +       # 20%
            ext_sim * 0.1 +       # 10%
            keyword_sim * 0.2     # 20%
        )
        
        return total_sim
    
    def get_confidence_level(self, similarity: float, location: str) -> str:
        """Get confidence level based on similarity and location"""
        if similarity >= 0.80:
            if location == 'same_package':
                return 'VERY HIGH'
            else:
                return 'HIGH'
        elif similarity >= 0.70:
            return 'HIGH'
        elif similarity >= 0.60:
            return 'MEDIUM'
        elif similarity >= 0.50:
            return 'LOW'
        else:
            return 'VERY LOW'
    
    def find_files_in_directory(self, directory: Path, pattern: str) -> List[Path]:
        """Find files matching pattern in directory"""
        if not directory.exists():
            return []
        
        results = []
        for file_path in directory.rglob(pattern):
            if file_path.is_file():
                results.append(file_path)
        
        return results
    
    def find_similar_files(self, expected_path: str) -> List[Dict]:
        """Find similar files with priority-based search"""
        expected = Path(expected_path)
        results = []
        
        # Extract package name from expected path
        parts = expected.parts
        expected_package = None
        if 'packages' in parts:
            pkg_idx = parts.index('packages')
            if pkg_idx + 1 < len(parts):
                expected_package = parts[pkg_idx + 1]
        
        # Priority 1: Same package
        if expected_package:
            package_dir = self.repo_root / 'packages' / expected_package
            if package_dir.exists():
                for file_path in package_dir.rglob('*.ts'):
                    if file_path.is_file():
                        relative_path = str(file_path.relative_to(self.repo_root))
                        similarity = self.calculate_similarity(expected_path, relative_path)
                        if similarity >= self.SIMILARITY_THRESHOLD_LOW:
                            results.append({
                                'path': relative_path,
                                'similarity': similarity,
                                'location': 'same_package',
                                'confidence': self.get_confidence_level(similarity, 'same_package')
                            })
        
        # Priority 2: Related packages (auth-lib <-> auth-service)
        if expected_package:
            related_packages = []
            if 'lib' in expected_package:
                related_name = expected_package.replace('-lib', '-service')
                related_packages.append(related_name)
            elif 'service' in expected_package:
                related_name = expected_package.replace('-service', '-lib')
                related_packages.append(related_name)
            
            for related_pkg in related_packages:
                related_dir = self.repo_root / 'packages' / related_pkg
                if related_dir.exists():
                    for file_path in related_dir.rglob('*.ts'):
                        if file_path.is_file():
                            relative_path = str(file_path.relative_to(self.repo_root))
                            similarity = self.calculate_similarity(expected_path, relative_path)
                            if similarity >= self.SIMILARITY_THRESHOLD_LOW:
                                results.append({
                                    'path': relative_path,
                                    'similarity': similarity,
                                    'location': 'related_package',
                                    'confidence': self.get_confidence_level(similarity, 'related_package')
                                })
        
        # Priority 3: Entire repository (if not enough results)
        if len(results) < 3:
            packages_dir = self.repo_root / 'packages'
            if packages_dir.exists():
                for file_path in packages_dir.rglob('*.ts'):
                    if file_path.is_file():
                        relative_path = str(file_path.relative_to(self.repo_root))
                        # Skip if already in results
                        if any(r['path'] == relative_path for r in results):
                            continue
                        similarity = self.calculate_similarity(expected_path, relative_path)
                        if similarity >= self.SIMILARITY_THRESHOLD_LOW:
                            results.append({
                                'path': relative_path,
                                'similarity': similarity,
                                'location': 'entire_repo',
                                'confidence': self.get_confidence_level(similarity, 'entire_repo')
                            })
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:5]  # Return top 5 candidates
    
    def read_report(self) -> Dict:
        """Read verification report (JSON or Markdown)"""
        if self.report_path.suffix == '.json':
            with open(self.report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif self.report_path.suffix == '.md':
            return self.parse_markdown_report()
        else:
            raise ValueError(f"Unsupported report format: {self.report_path.suffix}")
    
    def parse_markdown_report(self) -> Dict:
        """Parse markdown report to extract naming issues"""
        with open(self.report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        naming_issues = []
        
        # Pattern: → Update evidence path to: /full/path/to/file.ts
        pattern = r'→ Update evidence path to: (.+?)(?:\n|$)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            full_path = match.group(1).strip()
            # Extract relative path
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
                    suggestions = task.get('suggestions', [])
                    expected_path = None
                    found_path = None
                    
                    for suggestion in suggestions:
                        if '→ Update evidence path to:' in suggestion:
                            match = re.search(r'→ Update evidence path to: (.+?)(?:\n|$)', suggestion)
                            if match:
                                full_path = match.group(1).strip()
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
    
    def process_naming_issues(self, naming_issues: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Process naming issues and categorize into auto-fix and manual review"""
        auto_fix = []
        manual_review = []
        
        for issue in naming_issues:
            expected = issue.get('expected_path')
            found = issue.get('found_path')
            
            if not expected:
                continue
            
            # If found path is provided and has high confidence, use it
            if found:
                similarity = self.calculate_similarity(expected, found)
                confidence = self.get_confidence_level(similarity, 'provided')
                
                if similarity >= self.SIMILARITY_THRESHOLD_MEDIUM:
                    auto_fix.append({
                        **issue,
                        'candidates': [{
                            'path': found,
                            'similarity': similarity,
                            'confidence': confidence,
                            'selected': True
                        }]
                    })
                else:
                    # Low confidence, search for alternatives
                    candidates = self.find_similar_files(expected)
                    if candidates and candidates[0]['similarity'] >= self.SIMILARITY_THRESHOLD_MEDIUM:
                        auto_fix.append({
                            **issue,
                            'found_path': candidates[0]['path'],
                            'candidates': candidates
                        })
                    else:
                        manual_review.append({
                            **issue,
                            'candidates': candidates,
                            'reason': 'Low confidence match'
                        })
            else:
                # No found path, search for candidates
                candidates = self.find_similar_files(expected)
                
                if candidates:
                    if candidates[0]['similarity'] >= self.SIMILARITY_THRESHOLD_HIGH:
                        # High confidence, auto-fix
                        auto_fix.append({
                            **issue,
                            'found_path': candidates[0]['path'],
                            'candidates': candidates
                        })
                    elif candidates[0]['similarity'] >= self.SIMILARITY_THRESHOLD_MEDIUM:
                        # Medium confidence, check if there's a clear winner
                        if len(candidates) == 1 or (candidates[0]['similarity'] - candidates[1]['similarity']) > 0.15:
                            auto_fix.append({
                                **issue,
                                'found_path': candidates[0]['path'],
                                'candidates': candidates
                            })
                        else:
                            manual_review.append({
                                **issue,
                                'candidates': candidates,
                                'reason': 'Multiple similar candidates found'
                            })
                    else:
                        manual_review.append({
                            **issue,
                            'candidates': candidates,
                            'reason': 'Low confidence match'
                        })
                else:
                    manual_review.append({
                        **issue,
                        'candidates': [],
                        'reason': 'No similar files found'
                    })
        
        return auto_fix, manual_review
    
    def read_tasks_md(self) -> str:
        """Read tasks.md content"""
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def update_evidence_path(self, content: str, expected_path: str, found_path: str) -> Tuple[str, int]:
        """Update evidence path in content"""
        lines = content.split('\n')
        updated_count = 0
        
        for i, line in enumerate(lines):
            if 'evidence:' in line and expected_path in line:
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
    
    def generate_report(self) -> str:
        """Generate comprehensive markdown report"""
        md = "# Fix Naming Issues Report (Enhanced)\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Tasks File:** `{self.tasks_path}`\n"
        md += f"**Source Report:** `{self.report_path}`\n"
        md += f"**Status:** {'✅ Applied' if self.apply else '👁️ Preview Only'}\n\n"
        md += "---\n\n"
        
        # Summary
        md += "## Summary\n\n"
        md += f"- **Total naming issues found:** {len(self.naming_issues)}\n"
        md += f"- **Fixed automatically:** {len(self.auto_fixed)} ({len(self.auto_fixed)/max(len(self.naming_issues),1)*100:.0f}%)\n"
        md += f"- **Requires manual review:** {len(self.manual_review)} ({len(self.manual_review)/max(len(self.naming_issues),1)*100:.0f}%)\n"
        md += f"- **Evidence paths updated:** {len(self.changes)}\n"
        md += f"- **Changes applied:** {'Yes' if self.apply else 'No (preview mode)'}\n\n"
        
        # Fixed Automatically
        if self.auto_fixed:
            md += "## ✅ Fixed Automatically\n\n"
            md += f"Successfully fixed {len(self.auto_fixed)} naming issues with high/medium confidence:\n\n"
            
            # Group by type
            test_changes = [c for c in self.auto_fixed if 'test' in c['expected_path'].lower()]
            code_changes = [c for c in self.auto_fixed if 'test' not in c['expected_path'].lower()]
            
            if test_changes:
                md += f"### Test Files ({len(test_changes)} fixes)\n\n"
                for change in test_changes[:10]:
                    candidates = change.get('candidates', [])
                    best = candidates[0] if candidates else {}
                    conf = best.get('confidence', 'UNKNOWN')
                    sim = best.get('similarity', 0) * 100
                    md += f"- `{change['expected_path']}`\n"
                    md += f"  → `{change.get('found_path', 'N/A')}` ({sim:.0f}% - {conf})\n"
                if len(test_changes) > 10:
                    md += f"- ... and {len(test_changes) - 10} more\n"
                md += "\n"
            
            if code_changes:
                md += f"### Code Files ({len(code_changes)} fixes)\n\n"
                for change in code_changes[:10]:
                    candidates = change.get('candidates', [])
                    best = candidates[0] if candidates else {}
                    conf = best.get('confidence', 'UNKNOWN')
                    sim = best.get('similarity', 0) * 100
                    md += f"- `{change['expected_path']}`\n"
                    md += f"  → `{change.get('found_path', 'N/A')}` ({sim:.0f}% - {conf})\n"
                if len(code_changes) > 10:
                    md += f"- ... and {len(code_changes) - 10} more\n"
                md += "\n"
        
        # Requires Manual Review
        if self.manual_review:
            md += "## ⚠️ Requires Manual Review\n\n"
            md += f"Found {len(self.manual_review)} naming issues that need manual review:\n\n"
            
            for i, issue in enumerate(self.manual_review, 1):
                task_id = issue.get('task_id', f'Issue {i}')
                title = issue.get('title', 'Unknown')
                expected = issue.get('expected_path', 'Unknown')
                reason = issue.get('reason', 'Unknown')
                candidates = issue.get('candidates', [])
                
                md += f"### {task_id}: {title}\n\n"
                md += f"**Expected:** `{expected}`\n\n"
                
                if candidates:
                    md += "**Candidates Found:**\n\n"
                    for j, candidate in enumerate(candidates[:3], 1):
                        path = candidate['path']
                        sim = candidate['similarity'] * 100
                        conf = candidate['confidence']
                        md += f"{j}. `{path}` ({sim:.0f}% - {conf})\n"
                    md += "\n"
                else:
                    md += "**Candidates Found:** None\n\n"
                
                md += f"**Reason:** {reason}\n\n"
                md += "**Recommendation:**\n"
                if candidates:
                    md += "- Review the candidate files above\n"
                    md += "- Update evidence in tasks.md to the correct file\n"
                    md += "- Or create new file if none match\n"
                else:
                    md += "- File may not exist yet (not implemented)\n"
                    md += "- Create the file according to evidence path\n"
                    md += "- Or update evidence if file exists elsewhere\n"
                md += "\n---\n\n"
        
        # Next Steps
        md += "## Next Steps\n\n"
        if self.apply:
            md += "### 1. Verify Changes\n\n"
            md += "```bash\n"
            md += f"/smartspec_verify_tasks_progress_strict {self.tasks_path} --json\n"
            md += "```\n\n"
            
            md += "### 2. Review Diff\n\n"
            md += "```bash\n"
            md += f"git diff {self.tasks_path}\n"
            md += "```\n\n"
            
            if self.manual_review:
                md += "### 3. Address Manual Review Items\n\n"
                md += "Review the items in the 'Requires Manual Review' section above and:\n"
                md += "- Update evidence paths manually for items with clear candidates\n"
                md += "- Create missing files for items with no candidates\n\n"
            
            md += "### 4. Commit Changes\n\n"
            md += "```bash\n"
            md += "git add tasks.md\n"
            md += 'git commit -m "fix: Update evidence paths to match actual files"\n'
            md += "```\n\n"
        else:
            md += "This was a preview. To apply changes, run with `--apply` flag.\n\n"
        
        return md
    
    def save_report(self):
        """Save report to file"""
        # Use tasks_path parent if repo_root is not valid
        if not self.repo_root or self.repo_root == Path('/'):
            self.repo_root = self.tasks_path.parent.parent.parent
        
        spec_name = self.tasks_path.parent.name
        report_dir = self.repo_root / ".spec" / "reports" / "fix-naming-issues" / spec_name
        
        try:
            report_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # Fallback to /tmp if can't create in repo
            report_dir = Path("/tmp") / "smartspec-reports" / "fix-naming-issues" / spec_name
            report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"fix_naming_{self.timestamp}.md"
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
            self.naming_issues = naming_issues
            
            if not naming_issues:
                print("❌ No naming issues found in report.")
                return 1
            
            print(f"✅ Found {len(naming_issues)} naming issues\n")
            
            # Process naming issues
            print("🤖 Processing naming issues with enhanced matching...")
            auto_fixed, manual_review = self.process_naming_issues(naming_issues)
            self.auto_fixed = auto_fixed
            self.manual_review = manual_review
            
            print(f"   ✅ Auto-fix: {len(auto_fixed)} issues ({len(auto_fixed)/len(naming_issues)*100:.0f}%)")
            print(f"   ⚠️  Manual review: {len(manual_review)} issues ({len(manual_review)/len(naming_issues)*100:.0f}%)\n")
            
            # Read tasks.md
            print(f"📖 Reading tasks: {self.tasks_path}")
            content = self.read_tasks_md()
            
            # Update evidence paths for auto-fixed issues
            if auto_fixed:
                print("🔧 Updating evidence paths...")
                for issue in auto_fixed:
                    expected = issue.get('expected_path')
                    found = issue.get('found_path')
                    
                    if expected and found:
                        content, count = self.update_evidence_path(content, expected, found)
                        if count > 0:
                            print(f"   ✓ {expected} → {found} ({count} occurrences)")
            
            # Apply or preview
            if self.apply and self.changes:
                self.write_tasks_md(content)
                print(f"\n✅ Applied {len(self.changes)} changes to {self.tasks_path}")
            elif not self.apply:
                print(f"\n👁️  Preview mode: {len(self.changes)} changes ready to apply")
            
            # Generate report
            self.save_report()
            
            # Summary
            print("\n" + "="*80)
            print("SUMMARY")
            print("="*80)
            print(f"Total naming issues: {len(naming_issues)}")
            print(f"Fixed automatically: {len(auto_fixed)} ({len(auto_fixed)/len(naming_issues)*100:.0f}%)")
            print(f"Requires manual review: {len(manual_review)} ({len(manual_review)/len(naming_issues)*100:.0f}%)")
            print(f"Evidence paths updated: {len(self.changes)}")
            print("="*80 + "\n")
            
            if manual_review:
                print("⚠️  Some issues require manual review. See report for details.")
            
            return 0
            
        except Exception as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1


def resolve_latest_report(report_path: Path) -> Path:
    """Resolve wildcard pattern to latest file"""
    path_str = str(report_path)
    
    if '*' not in path_str:
        return report_path
    
    matches = glob.glob(path_str)
    
    if not matches:
        print(f"⚠️  Warning: No files match pattern: {path_str}")
        return report_path
    
    if len(matches) == 1:
        resolved = Path(matches[0])
        print(f"ℹ️  Resolved: {report_path.name} → {resolved.name}")
        return resolved
    
    matches.sort(key=lambda f: os.path.getmtime(f), reverse=True)
    latest = Path(matches[0])
    
    print(f"ℹ️  Found {len(matches)} files, using latest: {latest.name}")
    
    return latest


def main():
    parser = argparse.ArgumentParser(
        description='Fix naming issues with enhanced fuzzy matching',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes
  python3 fix_naming_issues_enhanced.py tasks.md --from-report report.json
  
  # Apply changes
  python3 fix_naming_issues_enhanced.py tasks.md --from-report report.json --apply
  
  # From markdown report with wildcard
  python3 fix_naming_issues_enhanced.py tasks.md --from-report batch_execution_*.md --apply
        """
    )
    
    parser.add_argument('tasks', type=Path, help='Path to tasks.md file')
    parser.add_argument('--from-report', type=Path, required=True, help='Path to verification report')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: preview only)')
    
    args = parser.parse_args()
    
    # Resolve wildcard
    report_path = resolve_latest_report(args.from_report)
    
    # Validate
    if not args.tasks.exists():
        print(f"❌ Error: tasks.md not found: {args.tasks}", file=sys.stderr)
        return 1
    
    if not report_path.exists():
        print(f"❌ Error: report not found: {report_path}", file=sys.stderr)
        return 1
    
    # Detect repo root
    repo_root = Path.cwd()
    for _ in range(3):
        if (repo_root / ".spec").exists() or (repo_root / "packages").exists():
            break
        repo_root = repo_root.parent
    
    # Run fixer
    fixer = EnhancedNamingIssuesFixer(args.tasks, report_path, args.apply, repo_root)
    return fixer.run()


if __name__ == '__main__':
    sys.exit(main())
