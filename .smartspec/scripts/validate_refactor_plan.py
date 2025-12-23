#!/usr/bin/env python3
"""
Validation script for smartspec_refactor_planner workflow outputs.

Usage:
    python3 validate_refactor_plan.py <report_path>

Exit codes:
    0 - Validation passed
    1 - Validation failed with errors
"""

import sys
import json
import os

def validate_refactor_report(report_path):
    """Validate refactoring plan report."""
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
    required_fields = ['version', 'timestamp', 'code_smells', 'refactoring_opportunities']
    for field in required_fields:
        if field not in report:
            errors.append(f"Missing required field: {field}")
    
    # Validate code smells
    if 'code_smells' in report:
        for smell in report['code_smells']:
            if 'type' not in smell or 'location' not in smell or 'severity' not in smell:
                errors.append(f"Invalid code smell entry: {smell}")
    
    # Validate refactoring opportunities
    if 'refactoring_opportunities' in report:
        for opportunity in report['refactoring_opportunities']:
            required = ['title', 'description', 'impact', 'effort']
            for field in required:
                if field not in opportunity:
                    errors.append(f"Refactoring opportunity missing field '{field}': {opportunity.get('title', 'unknown')}")
    
    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_refactor_plan.py <report_path>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    errors, warnings = validate_refactor_report(report_path)
    
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
