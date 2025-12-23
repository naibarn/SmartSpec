#!/usr/bin/env python3
"""
Validate spec.md and registry files for completeness and consistency.

Usage:
    python3 validate_spec.py --spec path/to/spec.md --registry path/to/registry/

Exit codes:
    0: Validation passed
    1: Validation failed (errors found)
    2: Usage error
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Validate spec.md and registry files")
    parser.add_argument("--spec", required=True, help="Path to spec.md file")
    parser.add_argument("--registry", required=True, help="Path to registry directory")
    return parser.parse_args()


def load_spec(spec_path):
    """Load and parse spec.md file."""
    if not os.path.exists(spec_path):
        return None, f"Spec file not found: {spec_path}"
    
    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return content, None


def extract_spec_id(spec_path):
    """Extract spec ID from spec.md path."""
    # Assuming path is specs/<category>/<spec-id>/spec.md
    parts = Path(spec_path).parts
    if len(parts) >= 2 and parts[-1] == "spec.md":
        return parts[-2]
    return None


def load_registry_file(registry_path, filename):
    """Load a registry JSON file."""
    filepath = os.path.join(registry_path, filename)
    if not os.path.exists(filepath):
        return None, f"Registry file not found: {filename}"
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in {filename}: {e}"


def extract_api_endpoints(spec_content):
    """Extract API endpoints from spec.md."""
    endpoints = []
    
    # Look for API endpoint patterns like:
    # POST /api/v1/auth/register
    # GET /api/v1/users/:id
    pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s\n]+)'
    matches = re.findall(pattern, spec_content, re.IGNORECASE)
    
    for method, path in matches:
        endpoints.append({
            "method": method.upper(),
            "path": path
        })
    
    return endpoints


def extract_data_models(spec_content):
    """Extract data model names from spec.md."""
    models = []
    
    # Look for model definitions like:
    # ### User Model
    # ## Data Model: User
    # **User** entity
    patterns = [
        r'###\s+(\w+)\s+Model',
        r'##\s+Data Model:\s+(\w+)',
        r'\*\*(\w+)\*\*\s+entity'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        models.extend(matches)
    
    # Remove duplicates
    return list(set(models))


def extract_terms(spec_content):
    """Extract terminology from spec.md."""
    terms = []
    
    # Look for term definitions like:
    # **JWT**: JSON Web Token
    # - **MFA**: Multi-Factor Authentication
    patterns = [
        r'\*\*([A-Z]{2,})\*\*:\s+([^\n]+)',
        r'-\s+\*\*([A-Z]{2,})\*\*:\s+([^\n]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        for term, definition in matches:
            terms.append(term)
    
    return list(set(terms))


def validate_api_registry(spec_content, spec_id, registry_data):
    """Validate that API endpoints from spec are in registry."""
    errors = []
    warnings = []
    
    if not registry_data:
        errors.append("api-registry.json is missing or invalid")
        return errors, warnings
    
    # Extract endpoints from spec
    spec_endpoints = extract_api_endpoints(spec_content)
    
    # Get endpoints from registry for this spec
    registry_endpoints = [
        ep for ep in registry_data.get("endpoints", [])
        if ep.get("owner_spec") == spec_id
    ]
    
    # Check if all spec endpoints are in registry
    spec_paths = {(ep["method"], ep["path"]) for ep in spec_endpoints}
    registry_paths = {(ep.get("method"), ep.get("path")) for ep in registry_endpoints}
    
    missing = spec_paths - registry_paths
    if missing:
        for method, path in missing:
            warnings.append(f"API endpoint not in registry: {method} {path}")
    
    # Check for orphaned entries (in registry but not in spec)
    orphaned = registry_paths - spec_paths
    if orphaned:
        for method, path in orphaned:
            warnings.append(f"Registry has orphaned endpoint: {method} {path}")
    
    return errors, warnings


def validate_data_model_registry(spec_content, spec_id, registry_data):
    """Validate that data models from spec are in registry."""
    errors = []
    warnings = []
    
    if not registry_data:
        errors.append("data-model-registry.json is missing or invalid")
        return errors, warnings
    
    # Extract models from spec
    spec_models = extract_data_models(spec_content)
    
    # Get models from registry for this spec
    registry_models = [
        model.get("name") for model in registry_data.get("models", [])
        if model.get("owner_spec") == spec_id
    ]
    
    # Check if all spec models are in registry
    missing = set(spec_models) - set(registry_models)
    if missing:
        for model in missing:
            warnings.append(f"Data model not in registry: {model}")
    
    # Check for orphaned entries
    orphaned = set(registry_models) - set(spec_models)
    if orphaned:
        for model in orphaned:
            warnings.append(f"Registry has orphaned model: {model}")
    
    return errors, warnings


def validate_glossary(spec_content, spec_id, registry_data):
    """Validate that terms from spec are in glossary."""
    errors = []
    warnings = []
    
    if not registry_data:
        errors.append("glossary.json is missing or invalid")
        return errors, warnings
    
    # Extract terms from spec
    spec_terms = extract_terms(spec_content)
    
    # Get terms from glossary for this spec
    glossary_terms = [
        term.get("term") for term in registry_data.get("terms", [])
        if term.get("owner_spec") == spec_id
    ]
    
    # Check if all spec terms are in glossary
    missing = set(spec_terms) - set(glossary_terms)
    if missing:
        for term in missing:
            warnings.append(f"Term not in glossary: {term}")
    
    return errors, warnings


def validate_critical_sections(spec_id, registry_data):
    """Validate critical sections registry."""
    errors = []
    warnings = []
    
    if not registry_data:
        warnings.append("critical-sections-registry.json is missing")
        return errors, warnings
    
    # Get critical sections for this spec
    sections = [
        section for section in registry_data.get("sections", [])
        if section.get("spec_id") == spec_id
    ]
    
    if not sections:
        warnings.append("No critical sections defined for this spec")
    
    return errors, warnings


def main():
    args = parse_args()
    
    # Load spec
    spec_content, error = load_spec(args.spec)
    if error:
        print(f"❌ Error: {error}")
        return 2
    
    # Extract spec ID
    spec_id = extract_spec_id(args.spec)
    if not spec_id:
        print(f"❌ Error: Could not extract spec ID from path: {args.spec}")
        return 2
    
    print(f"🔍 Validating spec: {spec_id}")
    print(f"📄 Spec file: {args.spec}")
    print(f"📁 Registry directory: {args.registry}")
    print()
    
    all_errors = []
    all_warnings = []
    
    # Load and validate each registry file
    registry_files = [
        ("api-registry.json", validate_api_registry),
        ("data-model-registry.json", validate_data_model_registry),
        ("glossary.json", validate_glossary),
    ]
    
    for filename, validator in registry_files:
        registry_data, error = load_registry_file(args.registry, filename)
        if error:
            all_errors.append(error)
            continue
        
        if validator == validate_api_registry:
            errors, warnings = validator(spec_content, spec_id, registry_data)
        elif validator == validate_data_model_registry:
            errors, warnings = validator(spec_content, spec_id, registry_data)
        elif validator == validate_glossary:
            errors, warnings = validator(spec_content, spec_id, registry_data)
        
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Validate critical sections (doesn't need spec content)
    critical_data, error = load_registry_file(args.registry, "critical-sections-registry.json")
    if not error:
        errors, warnings = validate_critical_sections(spec_id, critical_data)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Print results
    print("=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    print()
    
    if all_errors:
        print(f"❌ Errors ({len(all_errors)}):")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        print()
    
    if all_warnings:
        print(f"⚠️  Warnings ({len(all_warnings)}):")
        for i, warning in enumerate(all_warnings, 1):
            print(f"  {i}. {warning}")
        print()
    
    if not all_errors and not all_warnings:
        print("✅ Spec and registry files are VALID and complete!")
        print()
        return 0
    elif all_errors:
        print("❌ Validation FAILED with errors")
        print()
        return 1
    else:
        print("⚠️  Validation passed with warnings")
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
