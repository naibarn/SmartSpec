#!/usr/bin/env python3
"""
UI Spec Validator - Proof of Concept

Validates A2UI-compliant UI specifications for:
- Component structure
- Design system compliance
- Accessibility requirements
- Naming conventions
- Completeness

Version: 1.0.0 (PoC)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re


class UISpecValidator:
    """Validates UI specifications against A2UI standards"""
    
    def __init__(self, spec_path: Path, catalog_path: Optional[Path] = None, apply: bool = False):
        self.spec_path = spec_path
        self.catalog_path = catalog_path or Path(".spec/ui-catalog.json")
        self.apply = apply
        self.issues: List[Dict] = []
        self.fixes: List[Dict] = []
        self.spec_data: Optional[Dict] = None
        self.catalog_data: Optional[Dict] = None
        
    def load_spec(self) -> bool:
        """Load UI spec file"""
        try:
            with open(self.spec_path, 'r', encoding='utf-8') as f:
                self.spec_data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"❌ Error: UI spec not found: {self.spec_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in UI spec: {e}")
            return False
    
    def load_catalog(self) -> bool:
        """Load component catalog"""
        if not self.catalog_path.exists():
            print(f"⚠️  Warning: Component catalog not found: {self.catalog_path}")
            print("   Skipping catalog-based validation")
            return False
        
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                self.catalog_data = json.load(f)
            return True
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON in catalog: {e}")
            return False
    
    def validate_structure(self) -> bool:
        """Validate basic A2UI structure"""
        required_fields = ['version', 'metadata', 'components', 'layout']
        missing_fields = []
        
        for field in required_fields:
            if field not in self.spec_data:
                missing_fields.append(field)
                self.issues.append({
                    'type': 'structure',
                    'severity': 'error',
                    'field': field,
                    'message': f"Missing required field: {field}"
                })
        
        if missing_fields:
            print(f"❌ Structure validation failed: Missing fields: {', '.join(missing_fields)}")
            return False
        
        print("✅ Structure validation passed")
        return True
    
    def validate_version(self) -> bool:
        """Validate A2UI version"""
        version = self.spec_data.get('version', '')
        
        # Check version format (e.g., "0.8", "1.0")
        if not re.match(r'^\d+\.\d+$', version):
            self.issues.append({
                'type': 'version',
                'severity': 'error',
                'message': f"Invalid version format: {version}"
            })
            print(f"❌ Version validation failed: {version}")
            return False
        
        print(f"✅ Version validation passed: {version}")
        return True
    
    def validate_metadata(self) -> bool:
        """Validate metadata section"""
        metadata = self.spec_data.get('metadata', {})
        required_meta = ['name', 'description', 'platform']
        missing_meta = []
        
        for field in required_meta:
            if field not in metadata:
                missing_meta.append(field)
                self.issues.append({
                    'type': 'metadata',
                    'severity': 'warning',
                    'field': field,
                    'message': f"Missing metadata field: {field}"
                })
        
        if missing_meta:
            print(f"⚠️  Metadata incomplete: Missing {', '.join(missing_meta)}")
            return False
        
        print("✅ Metadata validation passed")
        return True
    
    def validate_components(self) -> bool:
        """Validate components section"""
        components = self.spec_data.get('components', [])
        
        if not components:
            self.issues.append({
                'type': 'components',
                'severity': 'error',
                'message': "No components defined"
            })
            print("❌ Components validation failed: No components")
            return False
        
        all_valid = True
        for i, component in enumerate(components):
            if not self._validate_component(component, i):
                all_valid = False
        
        if all_valid:
            print(f"✅ Components validation passed ({len(components)} components)")
        else:
            print(f"⚠️  Components validation completed with issues")
        
        return all_valid
    
    def _validate_component(self, component: Dict, index: int) -> bool:
        """Validate individual component"""
        required_fields = ['id', 'type', 'props']
        missing_fields = []
        
        for field in required_fields:
            if field not in component:
                missing_fields.append(field)
                self.issues.append({
                    'type': 'component',
                    'severity': 'error',
                    'component_index': index,
                    'field': field,
                    'message': f"Component {index}: Missing field: {field}"
                })
        
        if missing_fields:
            return False
        
        # Validate component ID naming (kebab-case)
        component_id = component.get('id', '')
        if not re.match(r'^[a-z][a-z0-9-]*$', component_id):
            self.issues.append({
                'type': 'component',
                'severity': 'warning',
                'component_index': index,
                'field': 'id',
                'message': f"Component {index}: ID should be kebab-case: {component_id}"
            })
            
            # Auto-fix: Convert to kebab-case
            fixed_id = self._to_kebab_case(component_id)
            self.fixes.append({
                'type': 'component_id',
                'component_index': index,
                'old_value': component_id,
                'new_value': fixed_id,
                'message': f"Convert component ID to kebab-case: {component_id} → {fixed_id}"
            })
        
        # Validate component type (if catalog available)
        if self.catalog_data:
            component_type = component.get('type', '')
            valid_types = self.catalog_data.get('components', {}).keys()
            if component_type not in valid_types:
                self.issues.append({
                    'type': 'component',
                    'severity': 'warning',
                    'component_index': index,
                    'field': 'type',
                    'message': f"Component {index}: Unknown type: {component_type}"
                })
        
        return len(missing_fields) == 0
    
    def validate_accessibility(self) -> bool:
        """Validate accessibility requirements"""
        components = self.spec_data.get('components', [])
        issues_found = False
        
        for i, component in enumerate(components):
            props = component.get('props', {})
            component_type = component.get('type', '')
            
            # Check for aria-label on interactive components
            interactive_types = ['button', 'input', 'select', 'checkbox', 'radio']
            if component_type in interactive_types:
                if 'aria-label' not in props and 'label' not in props:
                    self.issues.append({
                        'type': 'accessibility',
                        'severity': 'warning',
                        'component_index': i,
                        'message': f"Component {i} ({component_type}): Missing aria-label or label"
                    })
                    issues_found = True
                    
                    # Auto-fix: Add aria-label
                    component_id = component.get('id', f'component-{i}')
                    suggested_label = component_id.replace('-', ' ').title()
                    self.fixes.append({
                        'type': 'accessibility',
                        'component_index': i,
                        'field': 'aria-label',
                        'value': suggested_label,
                        'message': f"Add aria-label: {suggested_label}"
                    })
        
        if not issues_found:
            print("✅ Accessibility validation passed")
        else:
            print("⚠️  Accessibility validation completed with warnings")
        
        return not issues_found
    
    def validate_layout(self) -> bool:
        """Validate layout section"""
        layout = self.spec_data.get('layout', {})
        
        if not layout:
            self.issues.append({
                'type': 'layout',
                'severity': 'warning',
                'message': "Layout section is empty"
            })
            print("⚠️  Layout validation: Empty layout")
            return False
        
        # Check for required layout fields
        if 'type' not in layout:
            self.issues.append({
                'type': 'layout',
                'severity': 'warning',
                'field': 'type',
                'message': "Layout type not specified"
            })
            return False
        
        print("✅ Layout validation passed")
        return True
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case"""
        # Replace spaces and underscores with hyphens
        text = re.sub(r'[\s_]+', '-', text)
        # Insert hyphen before uppercase letters
        text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
        # Convert to lowercase
        text = text.lower()
        # Remove any non-alphanumeric characters except hyphens
        text = re.sub(r'[^a-z0-9-]', '', text)
        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Remove leading/trailing hyphens
        text = text.strip('-')
        return text
    
    def apply_fixes(self) -> bool:
        """Apply auto-fixes to spec"""
        if not self.fixes:
            print("ℹ️  No fixes to apply")
            return True
        
        if not self.apply:
            print(f"ℹ️  Preview mode: {len(self.fixes)} fix(es) available (use --apply to apply)")
            return False
        
        print(f"\n🔧 Applying {len(self.fixes)} fix(es)...")
        
        for fix in self.fixes:
            fix_type = fix['type']
            
            if fix_type == 'component_id':
                index = fix['component_index']
                new_id = fix['new_value']
                self.spec_data['components'][index]['id'] = new_id
                print(f"  ✅ Fixed component {index} ID: {fix['old_value']} → {new_id}")
            
            elif fix_type == 'accessibility':
                index = fix['component_index']
                field = fix['field']
                value = fix['value']
                if 'props' not in self.spec_data['components'][index]:
                    self.spec_data['components'][index]['props'] = {}
                self.spec_data['components'][index]['props'][field] = value
                print(f"  ✅ Added {field} to component {index}: {value}")
        
        # Save fixed spec
        try:
            with open(self.spec_path, 'w', encoding='utf-8') as f:
                json.dump(self.spec_data, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Applied {len(self.fixes)} fix(es) to {self.spec_path}")
            return True
        except Exception as e:
            print(f"\n❌ Error applying fixes: {e}")
            return False
    
    def generate_report(self) -> str:
        """Generate validation report"""
        report = []
        report.append("=" * 60)
        report.append("UI Spec Validation Report")
        report.append("=" * 60)
        report.append(f"Spec: {self.spec_path}")
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Mode: {'APPLY' if self.apply else 'PREVIEW'}")
        report.append("")
        
        # Summary
        error_count = len([i for i in self.issues if i['severity'] == 'error'])
        warning_count = len([i for i in self.issues if i['severity'] == 'warning'])
        
        report.append(f"Issues Found: {len(self.issues)}")
        report.append(f"  - Errors: {error_count}")
        report.append(f"  - Warnings: {warning_count}")
        report.append(f"Fixes Available: {len(self.fixes)}")
        report.append("")
        
        # Issues
        if self.issues:
            report.append("Issues:")
            report.append("-" * 60)
            for i, issue in enumerate(self.issues, 1):
                severity_icon = "❌" if issue['severity'] == 'error' else "⚠️ "
                report.append(f"{i}. {severity_icon} [{issue['type']}] {issue['message']}")
            report.append("")
        
        # Fixes
        if self.fixes:
            report.append("Available Fixes:")
            report.append("-" * 60)
            for i, fix in enumerate(self.fixes, 1):
                report.append(f"{i}. 🔧 [{fix['type']}] {fix['message']}")
            report.append("")
        
        # Recommendation
        if error_count > 0:
            report.append("❌ Validation FAILED: Fix errors before using this spec")
        elif warning_count > 0:
            report.append("⚠️  Validation PASSED with warnings: Consider fixing warnings")
        else:
            report.append("✅ Validation PASSED: Spec is ready to use")
        
        if self.fixes and not self.apply:
            report.append("")
            report.append("ℹ️  Run with --apply to automatically fix issues")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def validate(self) -> bool:
        """Run all validations"""
        print("\n🔍 Validating UI Spec...\n")
        
        # Load files
        if not self.load_spec():
            return False
        
        self.load_catalog()  # Optional
        
        # Run validations
        validations = [
            self.validate_structure(),
            self.validate_version(),
            self.validate_metadata(),
            self.validate_components(),
            self.validate_accessibility(),
            self.validate_layout(),
        ]
        
        # Apply fixes if requested
        if self.fixes and self.apply:
            self.apply_fixes()
        
        # Generate and print report
        print("\n" + self.generate_report())
        
        # Return overall result
        error_count = len([i for i in self.issues if i['severity'] == 'error'])
        return error_count == 0


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate A2UI-compliant UI specifications'
    )
    parser.add_argument(
        'spec',
        type=Path,
        help='Path to ui-spec.json file'
    )
    parser.add_argument(
        '--catalog',
        type=Path,
        help='Path to component catalog (default: .spec/ui-catalog.json)'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply auto-fixes (default: preview mode)'
    )
    
    args = parser.parse_args()
    
    # Validate
    validator = UISpecValidator(
        spec_path=args.spec,
        catalog_path=args.catalog,
        apply=args.apply
    )
    
    success = validator.validate()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
