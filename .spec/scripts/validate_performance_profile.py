#!/usr/bin/env python3
"""
Validation script for smartspec_performance_profiler workflow outputs.

Usage:
    python3 validate_performance_profile.py <report_path>

Exit codes:
    0 - Validation passed
    1 - Validation failed with errors
"""

import sys
import json
import os

def validate_performance_report(report_path):
    """Validate performance profiling report."""
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
    required_fields = ['version', 'timestamp', 'profiler', 'scenario', 'bottlenecks', 'optimization_opportunities']
    for field in required_fields:
        if field not in report:
            errors.append(f"Missing required field: {field}")
    
    # Validate bottlenecks
    if 'bottlenecks' in report:
        for bottleneck in report['bottlenecks']:
            if 'type' not in bottleneck or 'location' not in bottleneck or 'severity' not in bottleneck:
                errors.append(f"Invalid bottleneck entry: {bottleneck}")
    
    # Validate optimization opportunities
    if 'optimization_opportunities' in report:
        for opportunity in report['optimization_opportunities']:
            required = ['title', 'description', 'expected_gain', 'effort']
            for field in required:
                if field not in opportunity:
                    errors.append(f"Optimization opportunity missing field '{field}': {opportunity.get('title', 'unknown')}")
    
    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_performance_profile.py <report_path>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    errors, warnings = validate_performance_report(report_path)
    
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
