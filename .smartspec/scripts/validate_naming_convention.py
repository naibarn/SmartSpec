#!/usr/bin/env python3
"""
SmartSpec Naming Convention Validator

Validate naming convention compliance for all files in project.

Usage:
    validate_naming_convention.py [--dir DIR] [--fix] [--json] [--staged-only]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class NamingConventionValidator:
    def __init__(self, repo_root: Path, standard_path: Optional[Path] = None):
        self.repo_root = repo_root
        self.standard_path = standard_path or repo_root / ".smartspec" / "standards" / "naming-convention.md"
        self.standard = self.load_standard()
        self.violations = []
    
    def load_standard(self) -> Dict:
        """Load naming convention standard"""
        if not self.standard_path.exists():
            return self.get_default_standard()
        
        # For now, use hardcoded standard
        # In production, parse markdown file
        return self.get_default_standard()
    
    def get_default_standard(self) -> Dict:
        """Get default naming convention standard"""
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
                'constant': '.constant.ts',
                'type': '.type.ts',
                'interface': '.interface.ts',
                'enum': '.enum.ts',
                'guard': '.guard.ts',
                'decorator': '.decorator.ts',
                'factory': '.factory.ts',
                'repository': '.repository.ts',
                'dto': '.dto.ts',
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
                'constant': 'constants/',
                'type': 'types/',
                'interface': 'interfaces/',
                'enum': 'enums/',
                'guard': 'guards/',
                'decorator': 'decorators/',
                'factory': 'factories/',
                'repository': 'repositories/',
                'dto': 'dto/',
            }
        }
    
    def is_kebab_case(self, filename: str) -> bool:
        """Check if filename follows kebab-case convention"""
        # Remove extension(s)
        name = filename
        while '.' in name:
            name = name.rsplit('.', 1)[0]
        
        # Check kebab-case pattern
        return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))
    
    def to_kebab_case(self, filename: str) -> str:
        """Convert filename to kebab-case"""
        # Extract extension
        parts = filename.split('.')
        name = parts[0]
        extensions = parts[1:] if len(parts) > 1 else []
        
        # Convert to kebab-case
        # camelCase or PascalCase -> kebab-case
        name = re.sub('([a-z0-9])([A-Z])', r'\1-\2', name)
        # snake_case -> kebab-case
        name = name.replace('_', '-')
        # Multiple hyphens -> single hyphen
        name = re.sub(r'-+', '-', name)
        # Lowercase
        name = name.lower()
        
        # Reconstruct filename
        return name + '.' + '.'.join(extensions) if extensions else name
    
    def detect_file_type(self, file_path: Path) -> Optional[str]:
        """Detect file type from filename"""
        filename = file_path.name
        stem = file_path.stem
        suffix = file_path.suffix
        
        if suffix not in ['.ts', '.tsx', '.js', '.jsx']:
            return None
        
        # Check if stem ends with any known type pattern
        for type_name, type_suffix in self.standard['suffixes'].items():
            # Extract type part (e.g., '.service.ts' -> 'service')
            type_part = type_suffix.replace('.ts', '').replace('.js', '').replace('.tsx', '').replace('.jsx', '').lstrip('.')
            
            # Check if stem ends with '-{type_part}'
            if stem.endswith(f'-{type_part}'):
                return type_name
        
        return None
    
    def get_expected_directory(self, file_type: Optional[str]) -> Optional[str]:
        """Get expected directory for file type"""
        if not file_type:
            return None
        return self.standard['directories'].get(file_type)
    
    def is_in_correct_directory(self, file_path: Path, file_type: Optional[str]) -> bool:
        """Check if file is in correct directory"""
        if not file_type:
            return True  # Can't validate without file type
        
        expected_dir = self.get_expected_directory(file_type)
        if not expected_dir:
            return True
        
        # Check if file is in expected directory
        parent_dir = file_path.parent.name + '/'
        return parent_dir == expected_dir.rstrip('/')
    
    def validate_file(self, file_path: Path) -> Dict:
        """Validate a single file"""
        filename = file_path.name
        stem = file_path.stem
        suffix = file_path.suffix
        
        issues = []
        fixes = []
        
        # Skip special files
        if filename in ['index.ts', 'index.js', 'main.ts', 'app.ts', 'server.ts']:
            return {
                'file': str(file_path.relative_to(self.repo_root)),
                'compliant': True,
                'issues': [],
                'fixes': [],
                'skipped': True,
                'reason': 'Framework file'
            }
        
        # Check kebab-case
        if not self.is_kebab_case(filename):
            kebab_filename = self.to_kebab_case(filename)
            issues.append({
                'type': 'case',
                'severity': 'error',
                'message': f'Not kebab-case: {filename}',
                'expected': kebab_filename,
                'actual': filename
            })
            fixes.append({
                'type': 'rename',
                'from': filename,
                'to': kebab_filename
            })
        
        # Detect file type
        file_type = self.detect_file_type(file_path)
        
        # Check suffix
        if suffix in ['.ts', '.tsx', '.js', '.jsx']:
            if not file_type:
                issues.append({
                    'type': 'suffix',
                    'severity': 'warning',
                    'message': f'Missing or invalid suffix: {filename}',
                    'suggestions': list(self.standard['suffixes'].keys())
                })
        
        # Check directory
        if file_type:
            if not self.is_in_correct_directory(file_path, file_type):
                expected_dir = self.get_expected_directory(file_type)
                actual_dir = file_path.parent.name + '/'
                issues.append({
                    'type': 'directory',
                    'severity': 'warning',
                    'message': f'Wrong directory for {file_type}',
                    'expected': expected_dir,
                    'actual': actual_dir
                })
        
        return {
            'file': str(file_path.relative_to(self.repo_root)),
            'compliant': len(issues) == 0,
            'issues': issues,
            'fixes': fixes,
            'file_type': file_type
        }
    
    def get_staged_files(self) -> List[Path]:
        """Get list of staged TypeScript/JavaScript files"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line and re.search(r'\.(ts|tsx|js|jsx)$', line):
                    file_path = self.repo_root / line
                    if file_path.exists():
                        files.append(file_path)
            
            return files
        except subprocess.CalledProcessError:
            return []
    
    def validate_project(self, target_dir: Optional[Path] = None, staged_only: bool = False) -> Dict:
        """Validate entire project or specific directory"""
        if staged_only:
            files = self.get_staged_files()
            if not files:
                return {
                    'total_files': 0,
                    'violations': 0,
                    'compliance_rate': 1.0,
                    'results': [],
                    'staged_only': True
                }
        else:
            target = target_dir or self.repo_root
            
            # Find all TypeScript/JavaScript files
            files = []
            for pattern in ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx']:
                for file_path in target.glob(pattern):
                    # Skip excluded directories
                    if any(x in file_path.parts for x in ['node_modules', 'dist', 'build', '.git', 'coverage']):
                        continue
                    files.append(file_path)
        
        results = []
        for file_path in files:
            result = self.validate_file(file_path)
            if not result.get('skipped') and not result['compliant']:
                results.append(result)
        
        total_files = len(files)
        violations = len(results)
        
        return {
            'total_files': total_files,
            'violations': violations,
            'compliance_rate': (total_files - violations) / total_files if total_files > 0 else 1.0,
            'results': results,
            'staged_only': staged_only
        }
    
    def auto_fix(self, result: Dict) -> bool:
        """Auto-fix naming convention violations"""
        file_path = self.repo_root / result['file']
        
        if not file_path.exists():
            return False
        
        fixed = False
        for fix in result.get('fixes', []):
            if fix['type'] == 'rename':
                new_path = file_path.parent / fix['to']
                try:
                    file_path.rename(new_path)
                    print(f"✅ Fixed: {result['file']} → {fix['to']}")
                    fixed = True
                except Exception as e:
                    print(f"❌ Failed to fix {result['file']}: {e}")
        
        return fixed
    
    def generate_report(self, results: Dict, format: str = 'markdown') -> str:
        """Generate validation report"""
        if format == 'json':
            return json.dumps(results, indent=2)
        
        # Markdown report
        md = "# Naming Convention Validation Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**Total files:** {results['total_files']}\n"
        md += f"**Violations:** {results['violations']}\n"
        md += f"**Compliance rate:** {results['compliance_rate']:.1%}\n"
        
        if results.get('staged_only'):
            md += f"**Scope:** Staged files only\n"
        
        md += "\n"
        
        if results['violations'] > 0:
            md += "## ❌ Violations Found\n\n"
            
            # Group by severity
            errors = [r for r in results['results'] if any(i['severity'] == 'error' for i in r['issues'])]
            warnings = [r for r in results['results'] if all(i['severity'] == 'warning' for i in r['issues'])]
            
            if errors:
                md += f"### Errors ({len(errors)})\n\n"
                for result in errors[:10]:
                    md += f"**{result['file']}**\n"
                    for issue in result['issues']:
                        if issue['severity'] == 'error':
                            md += f"- ❌ **{issue['type']}:** {issue['message']}\n"
                            if 'expected' in issue:
                                md += f"  - Expected: `{issue['expected']}`\n"
                    md += "\n"
                
                if len(errors) > 10:
                    md += f"... and {len(errors) - 10} more errors\n\n"
            
            if warnings:
                md += f"### Warnings ({len(warnings)})\n\n"
                for result in warnings[:10]:
                    md += f"**{result['file']}**\n"
                    for issue in result['issues']:
                        if issue['severity'] == 'warning':
                            md += f"- ⚠️  **{issue['type']}:** {issue['message']}\n"
                            if 'suggestions' in issue:
                                md += f"  - Suggestions: {', '.join(issue['suggestions'][:5])}\n"
                    md += "\n"
                
                if len(warnings) > 10:
                    md += f"... and {len(warnings) - 10} more warnings\n\n"
            
            md += "## 🔧 How to Fix\n\n"
            md += "```bash\n"
            md += "# Auto-fix violations\n"
            md += "/smartspec_validate_naming_convention --fix\n"
            md += "\n"
            md += "# Or fix manually and re-validate\n"
            md += "/smartspec_validate_naming_convention\n"
            md += "```\n\n"
        else:
            md += "## ✅ No Violations Found\n\n"
            md += "All files follow naming convention!\n\n"
        
        return md
    
    def save_report(self, results: Dict, format: str = 'markdown') -> Path:
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.repo_root / ".spec" / "reports" / "naming-convention"
        
        try:
            report_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            report_dir = Path("/tmp") / "smartspec-reports" / "naming-convention"
            report_dir.mkdir(parents=True, exist_ok=True)
        
        ext = 'json' if format == 'json' else 'md'
        report_file = report_dir / f"validation_{timestamp}.{ext}"
        
        report_content = self.generate_report(results, format)
        report_file.write_text(report_content, encoding='utf-8')
        
        return report_file


def main():
    parser = argparse.ArgumentParser(
        description='Validate naming convention compliance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate entire project
  python3 validate_naming_convention.py
  
  # Validate specific directory
  python3 validate_naming_convention.py --dir packages/auth-lib
  
  # Validate staged files only (for pre-commit hook)
  python3 validate_naming_convention.py --staged-only
  
  # Auto-fix violations
  python3 validate_naming_convention.py --fix
  
  # Generate JSON report
  python3 validate_naming_convention.py --json
        """
    )
    
    parser.add_argument('--dir', type=Path, help='Directory to validate (default: entire project)')
    parser.add_argument('--fix', action='store_true', help='Auto-fix violations')
    parser.add_argument('--json', action='store_true', help='Output JSON format')
    parser.add_argument('--staged-only', action='store_true', help='Validate staged files only')
    parser.add_argument('--save-report', action='store_true', help='Save report to file')
    
    args = parser.parse_args()
    
    # Detect repo root
    repo_root = Path.cwd()
    while not (repo_root / '.smartspec').exists() and repo_root != repo_root.parent:
        repo_root = repo_root.parent
    
    if not (repo_root / '.smartspec').exists():
        print("❌ Error: Not in a SmartSpec project (no .smartspec directory found)", file=sys.stderr)
        return 1
    
    # Validate
    validator = NamingConventionValidator(repo_root)
    
    if not args.staged_only:
        print(f"🔍 Validating naming convention...")
        if args.dir:
            print(f"   Directory: {args.dir}")
    
    results = validator.validate_project(args.dir, args.staged_only)
    
    # Auto-fix if requested
    if args.fix and results['violations'] > 0:
        print(f"\n🔧 Auto-fixing {results['violations']} violations...")
        fixed_count = 0
        for result in results['results']:
            if validator.auto_fix(result):
                fixed_count += 1
        print(f"✅ Fixed {fixed_count}/{results['violations']} violations")
        
        # Re-validate
        print(f"\n🔍 Re-validating...")
        results = validator.validate_project(args.dir, args.staged_only)
    
    # Generate and display report
    report = validator.generate_report(results, 'json' if args.json else 'markdown')
    
    if args.json:
        print(report)
    else:
        if not args.staged_only:
            print(f"\n{report}")
        else:
            # For staged-only (pre-commit), show concise output
            if results['violations'] > 0:
                print(f"\n❌ Found {results['violations']} naming convention violation(s) in staged files:\n")
                for result in results['results']:
                    print(f"  {result['file']}")
                    for issue in result['issues']:
                        print(f"    - {issue['message']}")
                print(f"\nTo fix: /smartspec_validate_naming_convention --fix")
            else:
                if results['total_files'] > 0:
                    print(f"✅ All {results['total_files']} staged files follow naming convention")
    
    # Save report if requested
    if args.save_report:
        report_file = validator.save_report(results, 'json' if args.json else 'markdown')
        print(f"\n📄 Report saved: {report_file}")
    
    # Exit code
    return 0 if results['violations'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
