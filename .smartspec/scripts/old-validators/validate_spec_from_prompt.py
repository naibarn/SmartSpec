#!/usr/bin/env python3
"""
Validate Spec From Prompt - SmartSpec Workflow Validator

Validates specifications generated from prompts to ensure:
- Required sections present
- Content completeness
- Proper formatting
- Naming conventions
- Cross-references validity

Auto-fixes common issues when possible.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

class SpecFromPromptValidator:
    """Validator for spec-from-prompt workflow output"""
    
    # Required sections in a spec
    REQUIRED_SECTIONS = [
        "problem",
        "solution",
        "requirements",
        "architecture",
        "implementation"
    ]
    
    # Optional but recommended sections
    RECOMMENDED_SECTIONS = [
        "assumptions",
        "constraints",
        "risks",
        "alternatives"
    ]
    
    def __init__(self, spec_file: Path, repo_root: Optional[Path] = None):
        """
        Initialize validator
        
        Args:
            spec_file: Path to spec JSON/MD file
            repo_root: Repository root for validating paths
        """
        self.spec_file = Path(spec_file)
        self.repo_root = Path(repo_root) if repo_root else self.spec_file.parent
        self.issues = []
        self.fixes_applied = []
        self.spec_data = None
        
    def load_spec(self) -> bool:
        """Load spec file"""
        try:
            if self.spec_file.suffix == '.json':
                with open(self.spec_file, 'r', encoding='utf-8') as f:
                    self.spec_data = json.load(f)
            elif self.spec_file.suffix == '.md':
                self.spec_data = self._parse_markdown()
            else:
                self.issues.append({
                    'type': 'error',
                    'message': f'Unsupported file type: {self.spec_file.suffix}',
                    'fixable': False
                })
                return False
            return True
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'message': f'Failed to load spec: {str(e)}',
                'fixable': False
            })
            return False
    
    def _parse_markdown(self) -> Dict[str, Any]:
        """Parse markdown spec into structured data"""
        with open(self.spec_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        spec = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Check for section headers (## Section Name)
            if line.startswith('## '):
                if current_section:
                    spec[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip().lower().replace(' ', '_')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add last section
        if current_section:
            spec[current_section] = '\n'.join(current_content).strip()
        
        return spec
    
    def validate_structure(self) -> None:
        """Validate spec structure"""
        if not isinstance(self.spec_data, dict):
            self.issues.append({
                'type': 'error',
                'message': 'Spec must be a dictionary/object',
                'fixable': False
            })
            return
        
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self.spec_data:
                self.issues.append({
                    'type': 'error',
                    'section': section,
                    'message': f'Missing required section: {section}',
                    'fixable': True,
                    'fix': 'add_section'
                })
            elif not self.spec_data[section] or not str(self.spec_data[section]).strip():
                self.issues.append({
                    'type': 'warning',
                    'section': section,
                    'message': f'Section "{section}" is empty',
                    'fixable': True,
                    'fix': 'add_placeholder'
                })
        
        # Check recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if section not in self.spec_data:
                self.issues.append({
                    'type': 'info',
                    'section': section,
                    'message': f'Recommended section missing: {section}',
                    'fixable': True,
                    'fix': 'add_section'
                })
    
    def validate_content(self) -> None:
        """Validate content completeness"""
        # Check problem section
        if 'problem' in self.spec_data:
            problem = str(self.spec_data['problem'])
            if len(problem) < 50:
                self.issues.append({
                    'type': 'warning',
                    'section': 'problem',
                    'message': 'Problem description too short (< 50 chars)',
                    'fixable': False
                })
        
        # Check solution section
        if 'solution' in self.spec_data:
            solution = str(self.spec_data['solution'])
            if len(solution) < 100:
                self.issues.append({
                    'type': 'warning',
                    'section': 'solution',
                    'message': 'Solution description too short (< 100 chars)',
                    'fixable': False
                })
        
        # Check requirements
        if 'requirements' in self.spec_data:
            reqs = self.spec_data['requirements']
            if isinstance(reqs, str):
                # Count bullet points or numbered items
                req_items = len(re.findall(r'^[-*\d]+\.?\s+', reqs, re.MULTILINE))
                if req_items < 3:
                    self.issues.append({
                        'type': 'warning',
                        'section': 'requirements',
                        'message': f'Only {req_items} requirements found (recommend 3+)',
                        'fixable': False
                    })
            elif isinstance(reqs, list):
                if len(reqs) < 3:
                    self.issues.append({
                        'type': 'warning',
                        'section': 'requirements',
                        'message': f'Only {len(reqs)} requirements (recommend 3+)',
                        'fixable': False
                    })
    
    def validate_naming(self) -> None:
        """Validate naming conventions in file paths"""
        # Check for file paths in spec
        path_pattern = r'`([^`]+\.(ts|js|py|java|go|rs|md|json|yaml|yml))`'
        
        for section, content in self.spec_data.items():
            if not isinstance(content, str):
                continue
            
            paths = re.findall(path_pattern, content)
            for path, ext in paths:
                # Check kebab-case
                filename = Path(path).name
                stem = filename.rsplit('.', 1)[0]
                
                if not self._is_kebab_case(stem):
                    self.issues.append({
                        'type': 'warning',
                        'section': section,
                        'path': path,
                        'message': f'File path not in kebab-case: {path}',
                        'fixable': True,
                        'fix': 'convert_kebab_case'
                    })
    
    def _is_kebab_case(self, name: str) -> bool:
        """Check if name is in kebab-case"""
        # Allow kebab-case: lowercase with hyphens
        # Allow dots for extensions
        return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)*$', name))
    
    def validate_cross_references(self) -> None:
        """Validate cross-references within spec"""
        # Check for broken internal links
        link_pattern = r'\[([^\]]+)\]\(#([^\)]+)\)'
        
        # Get all section anchors
        anchors = set()
        for section in self.spec_data.keys():
            anchors.add(section.lower().replace(' ', '-'))
        
        for section, content in self.spec_data.items():
            if not isinstance(content, str):
                continue
            
            links = re.findall(link_pattern, content)
            for text, anchor in links:
                if anchor not in anchors:
                    self.issues.append({
                        'type': 'warning',
                        'section': section,
                        'link': f'[{text}](#{anchor})',
                        'message': f'Broken internal link: #{anchor}',
                        'fixable': False
                    })
    
    def auto_fix(self) -> None:
        """Apply automatic fixes"""
        for issue in self.issues:
            if not issue.get('fixable'):
                continue
            
            fix_type = issue.get('fix')
            
            if fix_type == 'add_section':
                section = issue.get('section')
                if section and section not in self.spec_data:
                    self.spec_data[section] = f'[TODO: Add {section} section]'
                    self.fixes_applied.append(f'Added section: {section}')
            
            elif fix_type == 'add_placeholder':
                section = issue.get('section')
                if section and not str(self.spec_data.get(section, '')).strip():
                    self.spec_data[section] = f'[TODO: Complete {section} section]'
                    self.fixes_applied.append(f'Added placeholder for: {section}')
            
            elif fix_type == 'convert_kebab_case':
                # This would require content modification
                # For now, just log it
                path = issue.get('path')
                if path:
                    self.fixes_applied.append(f'Flagged for kebab-case: {path}')
    
    def save_spec(self) -> None:
        """Save fixed spec"""
        if self.spec_file.suffix == '.json':
            with open(self.spec_file, 'w', encoding='utf-8') as f:
                json.dump(self.spec_data, f, indent=2, ensure_ascii=False)
        elif self.spec_file.suffix == '.md':
            self._save_markdown()
    
    def _save_markdown(self) -> None:
        """Save spec as markdown"""
        lines = []
        lines.append(f'# Specification\n')
        
        for section in self.REQUIRED_SECTIONS + self.RECOMMENDED_SECTIONS:
            if section in self.spec_data:
                title = section.replace('_', ' ').title()
                lines.append(f'## {title}\n')
                lines.append(f'{self.spec_data[section]}\n')
        
        # Add any other sections
        for section, content in self.spec_data.items():
            if section not in self.REQUIRED_SECTIONS + self.RECOMMENDED_SECTIONS:
                title = section.replace('_', ' ').title()
                lines.append(f'## {title}\n')
                lines.append(f'{content}\n')
        
        with open(self.spec_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_report(self) -> str:
        """Generate validation report"""
        lines = []
        lines.append('# Spec From Prompt Validation Report\n')
        lines.append(f'**File:** `{self.spec_file}`\n')
        
        # Summary
        errors = [i for i in self.issues if i['type'] == 'error']
        warnings = [i for i in self.issues if i['type'] == 'warning']
        infos = [i for i in self.issues if i['type'] == 'info']
        
        lines.append(f'## Summary\n')
        lines.append(f'- **Errors:** {len(errors)}')
        lines.append(f'- **Warnings:** {len(warnings)}')
        lines.append(f'- **Info:** {len(infos)}')
        lines.append(f'- **Fixes Applied:** {len(self.fixes_applied)}\n')
        
        # Issues
        if errors:
            lines.append(f'## Errors\n')
            for issue in errors:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        if warnings:
            lines.append(f'## Warnings\n')
            for issue in warnings:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        if infos:
            lines.append(f'## Recommendations\n')
            for issue in infos:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        # Fixes
        if self.fixes_applied:
            lines.append(f'## Fixes Applied\n')
            for fix in self.fixes_applied:
                lines.append(f'- {fix}')
            lines.append('')
        
        return '\n'.join(lines)
    
    def validate(self, apply_fixes: bool = False) -> Tuple[bool, str]:
        """
        Run full validation
        
        Args:
            apply_fixes: Whether to apply automatic fixes
        
        Returns:
            (success, report)
        """
        # Load spec
        if not self.load_spec():
            return False, self.generate_report()
        
        # Run validations
        self.validate_structure()
        self.validate_content()
        self.validate_naming()
        self.validate_cross_references()
        
        # Apply fixes if requested
        if apply_fixes:
            self.auto_fix()
            if self.fixes_applied:
                self.save_spec()
        
        # Generate report
        report = self.generate_report()
        
        # Success if no errors
        errors = [i for i in self.issues if i['type'] == 'error']
        success = len(errors) == 0
        
        return success, report


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate spec-from-prompt workflow output'
    )
    parser.add_argument('spec_file', help='Path to spec file (.json or .md)')
    parser.add_argument('--repo-root', help='Repository root directory')
    parser.add_argument('--apply', action='store_true', 
                       help='Apply automatic fixes')
    parser.add_argument('--output', help='Output report file')
    
    args = parser.parse_args()
    
    # Validate
    validator = SpecFromPromptValidator(args.spec_file, args.repo_root)
    success, report = validator.validate(apply_fixes=args.apply)
    
    # Print report
    print(report)
    
    # Save report if requested
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
    
    # Exit code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
