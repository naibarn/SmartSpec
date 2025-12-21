#!/usr/bin/env python3
"""
Enhanced spec validation with comprehensive registry and cross-spec checks.

Usage:
    python3 validate_spec_enhanced.py --spec path/to/spec.md --registry path/to/registry/

Exit codes:
    0: Validation passed
    1: Validation failed (errors found)
    2: Usage error
"""

import argparse
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Enhanced spec and registry validation")
    parser.add_argument("--spec", required=True, help="Path to spec.md file")
    parser.add_argument("--registry", required=True, help="Path to registry directory")
    parser.add_argument("--check-duplicates", action="store_true", help="Run duplicate detection")
    parser.add_argument("--threshold", type=float, default=0.8, help="Duplicate detection threshold")
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
    pattern = r'(GET|POST|PUT|DELETE|PATCH)\s+(/[^\s\n]+)'
    matches = re.findall(pattern, spec_content, re.IGNORECASE)
    
    for method, path in matches:
        endpoints.append({"method": method.upper(), "path": path})
    
    return endpoints


def extract_data_models(spec_content):
    """Extract data model names from spec.md."""
    models = []
    patterns = [
        r'###\s+(\w+)\s+Model',
        r'##\s+Data Model:\s+(\w+)',
        r'\*\*(\w+)\*\*\s+entity',
        r'class\s+(\w+)\s*[:{]',
        r'interface\s+(\w+)\s*[{]',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        models.extend(matches)
    
    return list(set(models))


def extract_ui_components(spec_content):
    """Extract UI component names from spec.md."""
    components = []
    patterns = [
        r'###\s+(\w+)\s+Component',
        r'##\s+UI Component:\s+(\w+)',
        r'<(\w+)\s+',  # JSX/HTML tags
        r'component:\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        components.extend(matches)
    
    # Filter out common HTML tags
    common_tags = {'div', 'span', 'p', 'a', 'button', 'input', 'form', 'table', 'tr', 'td', 'th'}
    components = [c for c in components if c.lower() not in common_tags]
    
    return list(set(components))


def extract_services(spec_content):
    """Extract service names from spec.md."""
    services = []
    patterns = [
        r'###\s+(\w+Service)',
        r'##\s+Service:\s+(\w+)',
        r'class\s+(\w+Service)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        services.extend(matches)
    
    return list(set(services))


def extract_workflows(spec_content):
    """Extract workflow names from spec.md."""
    workflows = []
    patterns = [
        r'###\s+(\w+)\s+(Flow|Workflow|Process)',
        r'##\s+(Flow|Workflow|Process):\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, spec_content)
        if matches:
            workflows.extend([m if isinstance(m, str) else ' '.join(m) for m in matches])
    
    return list(set(workflows))


def validate_api_registry(spec_content, spec_id, registry_data):
    """Validate API endpoints."""
    errors = []
    warnings = []
    
    if not registry_data:
        errors.append("api-registry.json is missing or invalid")
        return errors, warnings
    
    spec_endpoints = extract_api_endpoints(spec_content)
    registry_endpoints = [
        ep for ep in registry_data.get("endpoints", [])
        if ep.get("owner_spec") == spec_id
    ]
    
    spec_paths = {(ep["method"], ep["path"]) for ep in spec_endpoints}
    registry_paths = {(ep.get("method"), ep.get("path")) for ep in registry_endpoints}
    
    missing = spec_paths - registry_paths
    if missing:
        for method, path in missing:
            warnings.append(f"API endpoint not in registry: {method} {path}")
    
    orphaned = registry_paths - spec_paths
    if orphaned:
        for method, path in orphaned:
            warnings.append(f"Registry has orphaned endpoint: {method} {path}")
    
    return errors, warnings


def validate_data_model_registry(spec_content, spec_id, registry_data):
    """Validate data models."""
    errors = []
    warnings = []
    
    if not registry_data:
        errors.append("data-model-registry.json is missing or invalid")
        return errors, warnings
    
    spec_models = extract_data_models(spec_content)
    registry_models = [
        model.get("name") for model in registry_data.get("models", [])
        if model.get("owner_spec") == spec_id
    ]
    
    missing = set(spec_models) - set(registry_models)
    if missing:
        for model in missing:
            warnings.append(f"Data model not in registry: {model}")
    
    orphaned = set(registry_models) - set(spec_models)
    if orphaned:
        for model in orphaned:
            warnings.append(f"Registry has orphaned model: {model}")
    
    return errors, warnings


def validate_ui_components_registry(spec_content, spec_id, registry_data):
    """Validate UI components."""
    errors = []
    warnings = []
    
    if not registry_data:
        warnings.append("ui-components-registry.json is missing")
        return errors, warnings
    
    spec_components = extract_ui_components(spec_content)
    registry_components = [
        comp.get("name") for comp in registry_data.get("components", [])
        if comp.get("owner_spec") == spec_id
    ]
    
    missing = set(spec_components) - set(registry_components)
    if missing:
        for comp in missing:
            warnings.append(f"UI component not in registry: {comp}")
    
    return errors, warnings


def validate_services_registry(spec_content, spec_id, registry_data):
    """Validate services."""
    errors = []
    warnings = []
    
    if not registry_data:
        warnings.append("services-registry.json is missing")
        return errors, warnings
    
    spec_services = extract_services(spec_content)
    registry_services = [
        svc.get("name") for svc in registry_data.get("services", [])
        if svc.get("owner_spec") == spec_id
    ]
    
    missing = set(spec_services) - set(registry_services)
    if missing:
        for svc in missing:
            warnings.append(f"Service not in registry: {svc}")
    
    return errors, warnings


def validate_workflows_registry(spec_content, spec_id, registry_data):
    """Validate workflows."""
    errors = []
    warnings = []
    
    if not registry_data:
        warnings.append("workflows-registry.json is missing")
        return errors, warnings
    
    spec_workflows = extract_workflows(spec_content)
    registry_workflows = [
        wf.get("name") for wf in registry_data.get("workflows", [])
        if wf.get("owner_spec") == spec_id
    ]
    
    missing = set(spec_workflows) - set(registry_workflows)
    if missing:
        for wf in missing:
            warnings.append(f"Workflow not in registry: {wf}")
    
    return errors, warnings


def validate_cross_spec_consistency(registry_dir):
    """Validate consistency across specs."""
    errors = []
    warnings = []
    
    # Load data model registry
    data_model_registry, _ = load_registry_file(registry_dir, "data-model-registry.json")
    if not data_model_registry:
        return errors, warnings
    
    # Group models by name
    models_by_name = {}
    for model in data_model_registry.get("models", []):
        name = model.get("name")
        if name not in models_by_name:
            models_by_name[name] = []
        models_by_name[name].append(model)
    
    # Check for inconsistencies
    for name, models in models_by_name.items():
        if len(models) > 1:
            # Compare fields
            fields_sets = [set(m.get("fields", [])) for m in models]
            if not all(f == fields_sets[0] for f in fields_sets):
                specs = [m.get("owner_spec") for m in models]
                warnings.append(
                    f"Model '{name}' has inconsistent fields across specs: {', '.join(specs)}"
                )
    
    return errors, warnings



def validate_registry_schema(registry_path, schema_path):
    """Validate registry JSON against schema."""
    if not HAS_JSONSCHEMA:
        return []  # Skip validation if jsonschema not installed
    
    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        jsonschema.validate(registry, schema)
        return []
    except jsonschema.ValidationError as e:
        return [f"Schema validation error: {e.message}"]
    except Exception as e:
        return [f"Validation error: {str(e)}"]

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
    
    print(f"🔍 Enhanced Spec Validation")
    print(f"📄 Spec: {spec_id}")
    print(f"📁 Registry: {args.registry}")
    print()
    
    all_errors = []
    all_warnings = []
    
    # Validate each registry
    validators = [
        ("api-registry.json", validate_api_registry),
        ("data-model-registry.json", validate_data_model_registry),
        ("ui-components-registry.json", validate_ui_components_registry),
        ("services-registry.json", validate_services_registry),
        ("workflows-registry.json", validate_workflows_registry),
    ]
    
    for filename, validator in validators:
        registry_data, error = load_registry_file(args.registry, filename)
        if error and "ui-components" not in filename and "services" not in filename and "workflows" not in filename:
            all_errors.append(error)
            continue
        
        errors, warnings = validator(spec_content, spec_id, registry_data)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
    
    # Cross-spec consistency validation
    errors, warnings = validate_cross_spec_consistency(args.registry)
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Run duplicate detection if requested
    if args.check_duplicates:
        print("🔍 Running duplicate detection...")
        import subprocess
        result = subprocess.run(
            ["python3", os.path.join(os.path.dirname(__file__), "detect_duplicates.py"),
             "--registry-dir", args.registry,
             "--threshold", str(args.threshold)],
            capture_output=True,
            text=True
        )
        if result.returncode == 1:
            all_warnings.append("Potential duplicates detected (see duplicate detection output above)")
        print()
    
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
