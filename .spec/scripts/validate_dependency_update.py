#!/usr/bin/env python3
"""
Validation script for smartspec_dependency_updater workflow outputs.

Usage:
    python3 validate_dependency_update.py <report_path>

Exit codes:
    0 - Validation passed
    1 - Validation failed with errors
"""

import sys
import json
import os
from pathlib import Path

def validate_dependency_report(report_path):
    """Validate dependency update report."""
    errors = []
    warnings = []
    
    if not os.path.exists(report_path):
        errors.append(f"Report file not found: {report_path}")
        return errors, warnings
    
    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {e}")
            return errors, warnings
    
    # Check required fields
    required_fields = ['version', 'timestamp', 'package_manager', 'outdated_dependencies', 'vulnerabilities']
    for field in required_fields:
        if field not in report:
            errors.append(f"Missing required field: {field}")
    
    # Validate outdated dependencies
    if 'outdated_dependencies' in report:
        for dep in report['outdated_dependencies']:
            if 'name' not in dep or 'current_version' not in dep or 'latest_version' not in dep:
                errors.append(f"Invalid dependency entry: {dep}")
    
    # Validate vulnerabilities
    if 'vulnerabilities' in report:
        for vuln in report['vulnerabilities']:
            if 'cve_id' not in vuln or 'severity' not in vuln:
                errors.append(f"Invalid vulnerability entry: {vuln}")
            elif vuln['severity'] in ['high', 'critical']:
                warnings.append(f"High/critical vulnerability found: {vuln.get('cve_id', 'unknown')}")
    
    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_dependency_update.py <report_path>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    errors, warnings = validate_dependency_report(report_path)
    
    if errors:
        print("❌ Validation FAILED")
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors:
        print("✅ Validation PASSED")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
