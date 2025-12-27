#!/usr/bin/env python3
"""
Base Validator - SmartSpec Validators Base Class

Provides common functionality for all SmartSpec validators:
- Secure file loading with path validation
- File size limits
- Markdown parsing
- Structure validation
- Naming convention checks
- Auto-fix capabilities
- Report generation

Security features:
- Path traversal prevention
- File size limits (DoS protection)
- File type validation
- Permission checks
"""

import json
import sys
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

class BaseValidator:
    """Base class for all SmartSpec validators"""
    
    # Override in subclasses
    REQUIRED_SECTIONS: List[str] = []
    RECOMMENDED_SECTIONS: List[str] = []
    
    # Security settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = ['.md', '.json']
    
    def __init__(self, file_path: str, repo_root: Optional[str] = None):
        """
        Initialize validator with security checks
        
        Args:
            file_path: Path to file to validate
            repo_root: Repository root for path validation
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or outside repo
            PermissionError: If file is not readable
        """
        # Convert to absolute path and resolve symlinks
        self.file_path = Path(file_path).resolve()
        
        # Security: Check file exists
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Security: Check it's a regular file (not directory, device, etc.)
        if not self.file_path.is_file():
            raise ValueError(f"Not a regular file: {file_path}")
        
        # Security: Check file is readable
        if not os.access(self.file_path, os.R_OK):
            raise PermissionError(f"File not readable: {file_path}")
        
        # Security: Validate file extension
        if self.file_path.suffix not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Invalid file type: {self.file_path.suffix}. "
                f"Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        
        # Security: If repo_root specified, ensure file is within repo
        if repo_root:
            self.repo_root = Path(repo_root).resolve()
            try:
                self.file_path.relative_to(self.repo_root)
            except ValueError:
                raise ValueError(
                    f"Security: File outside repository. "
                    f"File: {self.file_path}, Repo: {self.repo_root}"
                )
        else:
            self.repo_root = self.file_path.parent
        
        # Initialize state
        self.issues: List[Dict[str, Any]] = []
        self.fixes_applied: List[str] = []
        self.data: Optional[Dict[str, Any]] = None
    
    def load_file(self) -> bool:
        """
        Load file with security checks
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # Security: Check file size
            file_size = self.file_path.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                self.issues.append({
                    'type': 'error',
                    'message': (
                        f'File too large: {file_size:,} bytes '
                        f'(max {self.MAX_FILE_SIZE:,} bytes = {self.MAX_FILE_SIZE // (1024*1024)} MB)'
                    ),
                    'fixable': False
                })
                return False
            
            # Security: Check file hasn't been modified during validation (TOCTOU protection)
            initial_mtime = self.file_path.stat().st_mtime
            
            # Load based on file type
            if self.file_path.suffix == '.json':
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            elif self.file_path.suffix == '.md':
                self.data = self._parse_markdown()
            
            # Security: Check mtime hasn't changed
            if self.file_path.stat().st_mtime != initial_mtime:
                self.issues.append({
                    'type': 'error',
                    'message': 'Security: File was modified during validation',
                    'fixable': False
                })
                return False
            
            return True
            
        except json.JSONDecodeError as e:
            self.issues.append({
                'type': 'error',
                'message': f'Invalid JSON: {str(e)}',
                'fixable': False
            })
            return False
        except UnicodeDecodeError as e:
            self.issues.append({
                'type': 'error',
                'message': f'Invalid file encoding (expected UTF-8): {str(e)}',
                'fixable': False
            })
            return False
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'message': f'Failed to load file: {str(e)}',
                'fixable': False
            })
            return False
    
    def _parse_markdown(self) -> Dict[str, Any]:
        """
        Parse markdown file into structured data
        
        Returns:
            Dictionary with section names as keys and content as values
        """
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            # Check for section headers (## Section Name)
            if line.startswith('## '):
                # Save previous section
                if current_section:
                    data[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line[3:].strip().lower().replace(' ', '_')
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            data[current_section] = '\n'.join(current_content).strip()
        
        return data
    
    def validate_structure(self) -> None:
        """Validate file structure"""
        if not isinstance(self.data, dict):
            self.issues.append({
                'type': 'error',
                'message': 'File must contain sections',
                'fixable': False
            })
            return
        
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self.data:
                self.issues.append({
                    'type': 'error',
                    'section': section,
                    'message': f'Missing required section: {section}',
                    'fixable': True,
                    'fix': 'add_section'
                })
            elif not self.data[section] or not str(self.data[section]).strip():
                self.issues.append({
                    'type': 'warning',
                    'section': section,
                    'message': f'Section "{section}" is empty',
                    'fixable': True,
                    'fix': 'add_placeholder'
                })
        
        # Check recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if section not in self.data:
                self.issues.append({
                    'type': 'info',
                    'section': section,
                    'message': f'Recommended section missing: {section}',
                    'fixable': True,
                    'fix': 'add_section'
                })
    
    def validate_naming(self) -> None:
        """Validate naming conventions"""
        # Pattern to find file paths in backticks
        path_pattern = r'`([^`]+\.(ts|js|py|java|go|rs|md|json|yaml|yml))`'
        
        for section, content in self.data.items():
            if not isinstance(content, str):
                continue
            
            paths = re.findall(path_pattern, content)
            for path, ext in paths:
                filename = Path(path).name
                stem = filename.rsplit('.', 1)[0]
                
                if not self._is_kebab_case(stem):
                    self.issues.append({
                        'type': 'warning',
                        'section': section,
                        'path': path,
                        'message': f'File path not in kebab-case: {path}',
                        'fixable': False
                    })
    
    def _is_kebab_case(self, name: str) -> bool:
        """
        Check if name is in kebab-case
        
        Args:
            name: Name to check
        
        Returns:
            True if name is in kebab-case, False otherwise
        """
        # Allow kebab-case: lowercase with hyphens
        # Allow dots for extensions
        return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+)*$', name))
    
    def auto_fix(self) -> None:
        """Apply automatic fixes"""
        for issue in self.issues:
            if not issue.get('fixable'):
                continue
            
            fix_type = issue.get('fix')
            
            if fix_type == 'add_section':
                section = issue.get('section')
                if section and section not in self.data:
                    self.data[section] = f'[TODO: Add {section} section]'
                    self.fixes_applied.append(f'Added section: {section}')
            
            elif fix_type == 'add_placeholder':
                section = issue.get('section')
                if section and not str(self.data.get(section, '')).strip():
                    self.data[section] = f'[TODO: Complete {section} section]'
                    self.fixes_applied.append(f'Added placeholder for: {section}')
    
    def save_file(self) -> None:
        """Save fixed file"""
        try:
            if self.file_path.suffix == '.json':
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=2, ensure_ascii=False)
            elif self.file_path.suffix == '.md':
                self._save_markdown()
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'message': f'Failed to save file: {str(e)}',
                'fixable': False
            })
    
    def _save_markdown(self) -> None:
        """Save data as markdown file"""
        lines = []
        
        # Add title if not present
        if 'title' not in self.data:
            lines.append('# Document\n')
        
        # Add required sections first
        for section in self.REQUIRED_SECTIONS:
            if section in self.data:
                title = section.replace('_', ' ').title()
                lines.append(f'## {title}\n')
                lines.append(f'{self.data[section]}\n')
        
        # Add recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if section in self.data:
                title = section.replace('_', ' ').title()
                lines.append(f'## {title}\n')
                lines.append(f'{self.data[section]}\n')
        
        # Add other sections
        for section, content in self.data.items():
            if section not in self.REQUIRED_SECTIONS + self.RECOMMENDED_SECTIONS:
                title = section.replace('_', ' ').title()
                lines.append(f'## {title}\n')
                lines.append(f'{content}\n')
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def generate_report(self) -> str:
        """Generate validation report"""
        lines = [
            '# Validation Report\n',
            f'**File:** `{self.file_path}`\n'
        ]
        
        # Categorize issues
        errors = [i for i in self.issues if i['type'] == 'error']
        warnings = [i for i in self.issues if i['type'] == 'warning']
        infos = [i for i in self.issues if i['type'] == 'info']
        
        # Summary
        lines.append('## Summary\n')
        lines.append(f'- **Errors:** {len(errors)}')
        lines.append(f'- **Warnings:** {len(warnings)}')
        lines.append(f'- **Info:** {len(infos)}')
        lines.append(f'- **Fixes Applied:** {len(self.fixes_applied)}\n')
        
        # Errors
        if errors:
            lines.append('## Errors\n')
            for issue in errors:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        # Warnings
        if warnings:
            lines.append('## Warnings\n')
            for issue in warnings:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        # Info/Recommendations
        if infos:
            lines.append('## Recommendations\n')
            for issue in infos:
                lines.append(f'- {issue["message"]}')
            lines.append('')
        
        # Fixes applied
        if self.fixes_applied:
            lines.append('## Fixes Applied\n')
            for fix in self.fixes_applied:
                lines.append(f'- {fix}')
            lines.append('')
        
        return '\n'.join(lines)
    
    def validate(self, apply_fixes: bool = False) -> Tuple[bool, str]:
        """
        Run validation (override in subclasses to add specific validations)
        
        Args:
            apply_fixes: Whether to apply automatic fixes
        
        Returns:
            Tuple of (success, report)
        """
        # Load file
        if not self.load_file():
            return False, self.generate_report()
        
        # Run validations
        self.validate_structure()
        self.validate_naming()
        
        # Apply fixes if requested - ✅ FIXED LOGIC
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
