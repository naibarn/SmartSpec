#!/usr/bin/env python3
"""
Validate Spec From Prompt - SmartSpec Workflow Validator (Refactored)

Validates specifications generated from prompts to ensure:
- Required sections present
- Content completeness
- Proper formatting
- Naming conventions
- Cross-references validity

Auto-fixes common issues when possible.

This is the refactored version using BaseValidator.
"""

import sys
import re
from pathlib import Path
from typing import Tuple
from base_validator import BaseValidator

class SpecFromPromptValidator(BaseValidator):
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
    
    def validate_content(self) -> None:
        """Validate content completeness"""
        # Check requirements section
        if 'requirements' in self.data:
            reqs = str(self.data['requirements'])
            
            # Check for functional requirements
            if 'functional' not in reqs.lower():
                self.issues.append({
                    'type': 'warning',
                    'section': 'requirements',
                    'message': 'No functional requirements found',
                    'fixable': False
                })
            
            # Check for non-functional requirements
            if 'non-functional' not in reqs.lower():
                self.issues.append({
                    'type': 'info',
                    'section': 'requirements',
                    'message': 'No non-functional requirements found',
                    'fixable': False
                })
        
        # Check for user stories
        has_user_stories = any('user_stories' in section or 'user stories' in section 
                              for section in self.data.keys())
        if not has_user_stories:
            self.issues.append({
                'type': 'info',
                'message': 'No user stories section found',
                'fixable': False
            })
        
        # Check for acceptance criteria
        has_acceptance = any('acceptance' in section.lower() 
                           for section in self.data.keys())
        if not has_acceptance:
            self.issues.append({
                'type': 'info',
                'message': 'No acceptance criteria section found',
                'fixable': False
            })
    
    def validate_cross_references(self) -> None:
        """Validate cross-references within spec"""
        # Check for broken internal links
        link_pattern = r'\[([^\]]+)\]\(#([^\)]+)\)'
        
        # Get all section anchors
        anchors = set()
        for section in self.data.keys():
            anchors.add(section.lower().replace(' ', '-'))
        
        for section, content in self.data.items():
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
    
    def validate(self, apply_fixes: bool = False) -> Tuple[bool, str]:
        """
        Run full validation
        
        Args:
            apply_fixes: Whether to apply automatic fixes
        
        Returns:
            (success, report)
        """
        # Load file
        if not self.load_file():
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
                self.save_file()
        
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
    parser.add_argument('spec_file', help='Path to spec file')
    parser.add_argument('--repo-root', help='Repository root directory')
    parser.add_argument('--apply', action='store_true', help='Apply automatic fixes')
    parser.add_argument('--output', help='Output report file')
    
    args = parser.parse_args()
    
    try:
        validator = SpecFromPromptValidator(args.spec_file, args.repo_root)
        success, report = validator.validate(apply_fixes=args.apply)
        
        print(report)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
        
        sys.exit(0 if success else 1)
    
    except (FileNotFoundError, ValueError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
