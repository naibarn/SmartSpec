#!/usr/bin/env python3
"""
SmartSpec Prompt Pack Validation Script

Validates generated prompt packs for completeness and duplication prevention.
Supports both spec-based and task-based prompt structures.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Tuple


def detect_prompt_type(prompts_path: Path) -> str:
    """
    Detect prompt pack type.
    
    Returns:
        'spec-based' - Traditional spec-based prompts (00_system_and_rules.md, etc.)
        'task-based' - Task-based prompts from verify report (prompt_001_*.md, etc.)
        'custom-priority' - Custom priority-filtered prompts (critical_issues.md, etc.)
        'unknown' - Cannot determine type
    """
    # Check for custom/priority-filtered structure
    custom_indicators = [
        "critical_issues.md",
        "high_priority_issues.md",
        "medium_priority_issues.md",
        "low_priority_issues.md"
    ]
    
    if any((prompts_path / f).exists() for f in custom_indicators) or (prompts_path / "meta").is_dir():
        return 'custom-priority'
    
    # Check for spec-based structure
    spec_based_files = [
        "prompts/00_system_and_rules.md",
        "prompts/10_context.md",
        "prompts/20_plan_of_attack.md"
    ]
    
    spec_based_count = sum(1 for f in spec_based_files if (prompts_path / f).exists())
    
    if spec_based_count >= 2:
        return 'spec-based'
    
    # Check for task-based structure
    prompt_files = list(prompts_path.glob("prompt_*.md"))
    
    if len(prompt_files) > 0:
        return 'task-based'
    
    return 'unknown'


def validate_spec_based_prompts(prompts_path: Path) -> Tuple[List[str], List[str]]:
    """Validate spec-based prompt pack."""
    errors = []
    warnings = []
    
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
    
    return errors, warnings


def validate_custom_priority_prompts(prompts_path: Path) -> Tuple[List[str], List[str]]:
    """Validate custom priority-filtered prompt pack."""
    errors = []
    warnings = []
    
    # Check required files
    readme_path = prompts_path / "README.md"
    
    if not readme_path.exists():
        errors.append("Required file missing: README.md")
    
    # Check for at least one priority file
    priority_files = [
        "critical_issues.md",
        "high_priority_issues.md",
        "medium_priority_issues.md",
        "low_priority_issues.md"
    ]
    
    has_priority_file = any((prompts_path / f).exists() for f in priority_files)
    
    if not has_priority_file:
        errors.append("No priority issue files found (critical_issues.md, etc.)")
    
    # Check README.md content
    if readme_path.exists():
        readme_content = readme_path.read_text()
        
        # Check for key information
        if "priority" not in readme_content.lower():
            warnings.append("README.md missing priority information")
        
        if "issue" not in readme_content.lower() and "task" not in readme_content.lower():
            warnings.append("README.md missing issue/task information")
    
    # Check meta directory (optional)
    meta_dir = prompts_path / "meta"
    if meta_dir.exists() and meta_dir.is_dir():
        # Meta directory is optional, just note it
        pass
    
    return errors, warnings


def validate_task_based_prompts(prompts_path: Path) -> Tuple[List[str], List[str]]:
    """Validate task-based prompt pack (from verify report)."""
    errors = []
    warnings = []
    
    # Check required files
    readme_path = prompts_path / "README.md"
    summary_path = prompts_path / "summary.json"
    
    if not readme_path.exists():
        errors.append("Required file missing: README.md")
    
    if not summary_path.exists():
        warnings.append("Recommended file missing: summary.json")
    
    # Check for prompt files
    prompt_files = list(prompts_path.glob("prompt_*.md"))
    
    if len(prompt_files) == 0:
        errors.append("No prompt files found (prompt_*.md)")
    else:
        # Validate prompt file naming
        for prompt_file in prompt_files:
            # Expected format: prompt_001_TSK-XXX-NNN.md or prompt_001.md
            if not prompt_file.stem.startswith("prompt_"):
                warnings.append(f"Prompt file has non-standard name: {prompt_file.name}")
    
    # Check README.md content
    if readme_path.exists():
        readme_content = readme_path.read_text()
        
        # Check for key information
        if "task" not in readme_content.lower():
            warnings.append("README.md missing task information")
        
        if "category" not in readme_content.lower() and "priority" not in readme_content.lower():
            warnings.append("README.md missing category or priority information")
    
    # Check summary.json content
    if summary_path.exists():
        try:
            summary_data = json.loads(summary_path.read_text())
            
            # Check for required fields
            required_fields = ["workflow", "generated_at", "prompts_count"]
            for field in required_fields:
                if field not in summary_data:
                    warnings.append(f"summary.json missing recommended field: {field}")
        
        except json.JSONDecodeError:
            errors.append("summary.json is not valid JSON")
    
    return errors, warnings


def validate_prompt_pack(prompts_dir, registry_dir, check_duplicates=False, threshold=0.8):
    """Validate a prompt pack directory."""
    errors = []
    warnings = []
    
    prompts_path = Path(prompts_dir)
    
    # Check if directory exists
    if not prompts_path.exists():
        errors.append(f"Prompt pack directory not found: {prompts_dir}")
        return errors, warnings
    
    # Detect prompt type
    prompt_type = detect_prompt_type(prompts_path)
    
    print(f"📦 Detected prompt type: {prompt_type}")
    print()
    
    # Validate based on type
    if prompt_type == 'spec-based':
        errors, warnings = validate_spec_based_prompts(prompts_path)
    elif prompt_type == 'task-based':
        errors, warnings = validate_task_based_prompts(prompts_path)
    elif prompt_type == 'custom-priority':
        errors, warnings = validate_custom_priority_prompts(prompts_path)
    else:
        errors.append("Cannot determine prompt pack type (no recognizable structure found)")
        return errors, warnings
    
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
