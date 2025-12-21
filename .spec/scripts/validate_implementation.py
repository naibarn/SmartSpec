#!/usr/bin/env python3
"""
SmartSpec Implementation Validation Script

Validates implementation changes against tasks.md and spec.md,
with duplication prevention checks.
"""

import sys
import os
import json
import argparse
import re
from pathlib import Path

def parse_tasks(tasks_path):
    """Parse tasks.md to extract task IDs and requirements."""
    tasks = []
    
    with open(tasks_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract task items (e.g., "- [ ] TSK-AUTH-001: ...")
    task_pattern = r'-\s*\[([ x])\]\s*(TSK-[A-Z]+-\d+):\s*(.+?)(?=\n-|\n\n|$)'
    matches = re.finditer(task_pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        checked = match.group(1) == 'x'
        task_id = match.group(2)
        description = match.group(3).strip()
        
        tasks.append({
            'id': task_id,
            'checked': checked,
            'description': description
        })
    
    return tasks

def parse_spec(spec_path):
    """Parse spec.md to extract requirements."""
    requirements = []
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract SEC requirements
    sec_pattern = r'(SEC-\d+):\s*(.+?)(?=\n\n|SEC-\d+:|$)'
    matches = re.finditer(sec_pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        req_id = match.group(1)
        description = match.group(2).strip()
        
        requirements.append({
            'id': req_id,
            'description': description
        })
    
    return requirements

def validate_implementation(tasks_path, spec_path, registry_dir, check_duplicates=False, threshold=0.8):
    """Validate implementation against tasks and spec."""
    errors = []
    warnings = []
    
    # Check if files exist
    if not os.path.exists(tasks_path):
        errors.append(f"tasks.md not found: {tasks_path}")
        return errors, warnings
    
    if not os.path.exists(spec_path):
        errors.append(f"spec.md not found: {spec_path}")
        return errors, warnings
    
    # Parse tasks and spec
    tasks = parse_tasks(tasks_path)
    requirements = parse_spec(spec_path)
    
    # Check if any tasks are checked
    checked_tasks = [t for t in tasks if t['checked']]
    if not checked_tasks:
        warnings.append("No tasks are marked as completed")
    
    # Check for duplication if requested
    if check_duplicates and registry_dir:
        if not os.path.exists(registry_dir):
            warnings.append(f"Registry directory not found: {registry_dir}")
        else:
            # Call detect_duplicates.py
            import subprocess
            result = subprocess.run([
                sys.executable,
                os.path.join(os.path.dirname(__file__), 'detect_duplicates.py'),
                '--registry-dir', registry_dir,
                '--threshold', str(threshold)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                errors.append("Duplicate components detected. See output above.")
                print(result.stdout)
    
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Validate SmartSpec implementation")
    parser.add_argument("--tasks", required=True, help="Path to tasks.md")
    parser.add_argument("--spec", required=True, help="Path to spec.md")
    parser.add_argument("--registry", help="Path to registry directory")
    parser.add_argument("--check-duplicates", action="store_true", help="Check for duplicates")
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold (0.0-1.0)")
    
    args = parser.parse_args()
    
    # Run validation
    errors, warnings = validate_implementation(
        args.tasks,
        args.spec,
        args.registry,
        args.check_duplicates,
        args.threshold
    )
    
    # Print results
    print("=" * 60)
    print("IMPLEMENTATION VALIDATION RESULTS")
    print("=" * 60)
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    if not errors and not warnings:
        print("\n✅ Implementation is valid and complete!")
    elif not errors:
        print("\n⚠️  Validation passed with warnings")
    else:
        print("\n❌ Validation failed")
    
    # Exit code
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
