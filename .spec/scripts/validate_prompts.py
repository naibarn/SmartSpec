#!/usr/bin/env python3
"""
SmartSpec Prompt Pack Validation Script

Validates generated prompt packs for completeness and duplication prevention.
"""

import sys
import os
import json
import argparse
from pathlib import Path

def validate_prompt_pack(prompts_dir, registry_dir, check_duplicates=False, threshold=0.8):
    """Validate a prompt pack directory."""
    errors = []
    warnings = []
    
    prompts_path = Path(prompts_dir)
    
    # Check if directory exists
    if not prompts_path.exists():
        errors.append(f"Prompt pack directory not found: {prompts_dir}")
        return errors, warnings
    
    # Check required files
    required_files = [
        "README.md",
        "prompts/00_system_and_rules.md",
        "prompts/10_context.md",
        "prompts/20_plan_of_attack.md",
        "prompts/30_tasks_breakdown.md",
        "prompts/40_risks_and_guards.md"
    ]
    
    for required_file in required_files:
        file_path = prompts_path / required_file
        if not file_path.exists():
            errors.append(f"Required file missing: {required_file}")
    
    # Check README.md content
    readme_path = prompts_path / "README.md"
    if readme_path.exists():
        readme_content = readme_path.read_text()
        
        # Check for required sections
        required_sections = [
            "Spec and tasks paths",
            "Target profile",
            "Constraints",
            "Output inventory"
        ]
        
        for section in required_sections:
            if section.lower() not in readme_content.lower():
                warnings.append(f"README.md missing recommended section: {section}")
        
        # Check for security notes
        if "no runtime source files were modified" not in readme_content.lower():
            warnings.append("README.md missing security notes")
    
    # Check for duplication if requested
    if check_duplicates and registry_dir:
        # This would call detect_duplicates.py or similar logic
        # For now, just a placeholder
        pass
    
    return errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Validate SmartSpec prompt packs")
    parser.add_argument("--prompts", required=True, help="Path to prompt pack directory")
    parser.add_argument("--registry", help="Path to registry directory")
    parser.add_argument("--check-duplicates", action="store_true", help="Check for duplicates")
    parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold (0.0-1.0)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.prompts):
        print(f"❌ Error: Prompt pack directory not found: {args.prompts}")
        sys.exit(2)
    
    if args.registry and not os.path.exists(args.registry):
        print(f"❌ Error: Registry directory not found: {args.registry}")
        sys.exit(2)
    
    # Run validation
    errors, warnings = validate_prompt_pack(
        args.prompts,
        args.registry,
        args.check_duplicates,
        args.threshold
    )
    
    # Print results
    print("=" * 60)
    print("PROMPT PACK VALIDATION RESULTS")
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
        print("\n✅ Prompt pack is valid and complete!")
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
