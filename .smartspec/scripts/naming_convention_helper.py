#!/usr/bin/env python3
"""
Naming Convention Integration Helper

Shared helper functions for integrating naming convention validation
across SmartSpec workflows.

Usage:
    from naming_convention_helper import (
        load_naming_standard,
        validate_file_path,
        is_compliant,
        find_compliant_matches,
        get_naming_statistics
    )
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


class ValidationResult:
    """Result of naming convention validation"""
    
    def __init__(self, compliant: bool, issues: List[str] = None, file_type: Optional[str] = None):
        self.compliant = compliant
        self.issues = issues or []
        self.file_type = file_type
    
    def __repr__(self):
        return f"ValidationResult(compliant={self.compliant}, issues={self.issues}, file_type={self.file_type})"


def load_naming_standard(repo_root: Path) -> Dict:
    """
    Load naming convention standard from repository.
    
    Returns a dictionary with naming rules:
    - case: 'kebab-case'
    - suffixes: Dict of file type to suffix mapping
    - directories: Dict of file type to directory mapping
    """
    # Define standard (can be loaded from file in the future)
    return {
        'case': 'kebab-case',
        'suffixes': {
            'service': '.service.ts',
            'provider': '.provider.ts',
            'client': '.client.ts',
            'controller': '.controller.ts',
            'middleware': '.middleware.ts',
            'util': '.util.ts',
            'helper': '.helper.ts',
            'model': '.model.ts',
            'schema': '.schema.ts',
            'type': '.type.ts',
            'interface': '.interface.ts',
            'enum': '.enum.ts',
            'constant': '.constant.ts',
            'config': '.config.ts',
            'guard': '.guard.ts',
            'interceptor': '.interceptor.ts',
            'decorator': '.decorator.ts',
            'pipe': '.pipe.ts',
            'filter': '.filter.ts',
            'gateway': '.gateway.ts',
            'adapter': '.adapter.ts',
            'factory': '.factory.ts',
            'builder': '.builder.ts',
            'strategy': '.strategy.ts',
            'repository': '.repository.ts',
            'dao': '.dao.ts',
            'dto': '.dto.ts',
            'entity': '.entity.ts',
            'validator': '.validator.ts',
            'parser': '.parser.ts',
            'serializer': '.serializer.ts',
            'transformer': '.transformer.ts',
            'mapper': '.mapper.ts',
        },
        'directories': {
            'service': 'services',
            'provider': 'providers',
            'client': 'clients',
            'controller': 'controllers',
            'middleware': 'middleware',
            'util': 'utils',
            'helper': 'helpers',
            'model': 'models',
            'schema': 'schemas',
            'type': 'types',
            'interface': 'interfaces',
            'enum': 'enums',
            'constant': 'constants',
            'config': 'config',
            'guard': 'guards',
            'interceptor': 'interceptors',
            'decorator': 'decorators',
            'pipe': 'pipes',
            'filter': 'filters',
            'gateway': 'gateways',
            'adapter': 'adapters',
            'factory': 'factories',
            'builder': 'builders',
            'strategy': 'strategies',
            'repository': 'repositories',
            'dao': 'dao',
            'dto': 'dto',
            'entity': 'entities',
            'validator': 'validators',
            'parser': 'parsers',
            'serializer': 'serializers',
            'transformer': 'transformers',
            'mapper': 'mappers',
        }
    }


def is_kebab_case(filename: str) -> bool:
    """
    Check if filename follows kebab-case convention.
    
    Examples:
        user-service.ts -> True
        userService.ts -> False
        user_service.ts -> False
    """
    # Remove all extensions
    name = filename
    while '.' in name:
        name = name.rsplit('.', 1)[0]
    
    # Check kebab-case pattern
    return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))


def detect_file_type(filename: str, standard: Dict) -> Optional[str]:
    """
    Detect file type from filename based on suffix.
    
    Examples:
        user-service.ts -> 'service'
        sms-provider.ts -> 'provider'
        user.ts -> None
    """
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    
    # Only check TypeScript/JavaScript files
    if suffix not in ['.ts', '.tsx', '.js', '.jsx']:
        return None
    
    # Check each known suffix
    for type_name, type_suffix in standard['suffixes'].items():
        # Extract the type part from suffix (e.g., '.service.ts' -> 'service')
        type_part = type_suffix.replace('.ts', '').replace('.tsx', '').replace('.js', '').replace('.jsx', '').lstrip('.')
        
        # Check if stem ends with -<type>
        if stem.endswith(f'-{type_part}'):
            return type_name
    
    return None


def validate_file_path(path: str, standard: Dict) -> ValidationResult:
    """
    Validate a file path against naming convention standard.
    
    Returns ValidationResult with:
    - compliant: True if path follows all rules
    - issues: List of violation messages
    - file_type: Detected file type (if any)
    """
    file_path = Path(path)
    filename = file_path.name
    
    issues = []
    
    # Check kebab-case
    if not is_kebab_case(filename):
        issues.append(f"Not kebab-case: {filename}")
    
    # Detect file type
    file_type = detect_file_type(filename, standard)
    
    # Check suffix for TypeScript/JavaScript files
    if file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
        if not file_type:
            # Check if it's a special case (index, main, app, etc.)
            stem = file_path.stem
            if stem not in ['index', 'main', 'app', 'server', 'client']:
                issues.append(f"Missing or invalid suffix: {filename}")
    
    # Check directory placement
    if file_type:
        expected_dir = standard['directories'].get(file_type, '').rstrip('/')
        if expected_dir:
            # Get the parent directory name
            actual_dir = file_path.parent.name
            
            # Allow both singular and plural forms
            if actual_dir != expected_dir and actual_dir != expected_dir.rstrip('s'):
                issues.append(f"Wrong directory: expected {expected_dir}/, got {actual_dir}/")
    
    return ValidationResult(
        compliant=len(issues) == 0,
        issues=issues,
        file_type=file_type
    )


def is_compliant(path: str, standard: Dict) -> bool:
    """
    Quick check if path is compliant with naming convention.
    
    Returns True if compliant, False otherwise.
    """
    result = validate_file_path(path, standard)
    return result.compliant


def get_violations(path: str, standard: Dict) -> List[str]:
    """
    Get list of naming convention violations for a path.
    
    Returns list of violation messages.
    """
    result = validate_file_path(path, standard)
    return result.issues


def calculate_base_similarity(path1: str, path2: str) -> float:
    """
    Calculate base similarity between two paths using sequence matching.
    
    Returns similarity score (0.0 to 1.0).
    """
    from difflib import SequenceMatcher
    
    # Compare full paths
    full_similarity = SequenceMatcher(None, path1, path2).ratio()
    
    # Compare filenames
    filename1 = Path(path1).name
    filename2 = Path(path2).name
    filename_similarity = SequenceMatcher(None, filename1, filename2).ratio()
    
    # Compare stems (without extension)
    stem1 = Path(path1).stem
    stem2 = Path(path2).stem
    stem_similarity = SequenceMatcher(None, stem1, stem2).ratio()
    
    # Weighted average (filename matters most)
    return (
        full_similarity * 0.3 +
        filename_similarity * 0.4 +
        stem_similarity * 0.3
    )


def similarity_with_naming(path1: str, path2: str, standard: Dict) -> float:
    """
    Calculate similarity between two paths, with bonus for naming convention compliance.
    
    Returns similarity score (0.0 to 1.0).
    """
    # Base similarity
    base_similarity = calculate_base_similarity(path1, path2)
    
    # Naming convention bonus
    result1 = validate_file_path(path1, standard)
    result2 = validate_file_path(path2, standard)
    
    naming_bonus = 0.0
    if result1.compliant and result2.compliant:
        naming_bonus = 0.1  # 10% bonus for both being compliant
    
    return min(1.0, base_similarity + naming_bonus)


def find_compliant_matches(
    expected: str,
    candidates: List[str],
    standard: Dict,
    threshold: float = 0.8
) -> List[Tuple[str, float]]:
    """
    Find compliant files that match expected path.
    
    Args:
        expected: Expected file path
        candidates: List of candidate file paths
        standard: Naming convention standard
        threshold: Minimum similarity threshold (0.0 to 1.0)
    
    Returns:
        List of (path, similarity) tuples, sorted by similarity (descending)
    """
    matches = []
    
    for candidate in candidates:
        # Check if candidate is compliant
        result = validate_file_path(candidate, standard)
        if not result.compliant:
            continue
        
        # Calculate similarity
        similarity = similarity_with_naming(expected, candidate, standard)
        if similarity >= threshold:
            matches.append((candidate, similarity))
    
    # Sort by similarity (descending)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches


def format_naming_issues(issues: List[str]) -> str:
    """
    Format naming issues for display.
    
    Returns formatted string with emoji indicators.
    """
    if not issues:
        return "✅ No naming issues"
    
    formatted = "⚠️ Naming issues:\n"
    for issue in issues:
        formatted += f"  - {issue}\n"
    
    return formatted.rstrip()


def get_naming_statistics(files: List[str], standard: Dict) -> Dict:
    """
    Get naming convention statistics for a list of files.
    
    Args:
        files: List of file paths
        standard: Naming convention standard
    
    Returns:
        Dictionary with statistics:
        - total_files: Total number of files
        - compliant_files: Number of compliant files
        - non_compliant_files: Number of non-compliant files
        - compliance_rate: Compliance rate (0.0 to 1.0)
        - violations: List of violations with details
    """
    total = len(files)
    compliant = 0
    violations = []
    
    for file_path in files:
        result = validate_file_path(file_path, standard)
        if result.compliant:
            compliant += 1
        else:
            violations.append({
                'file': file_path,
                'issues': result.issues,
                'file_type': result.file_type
            })
    
    return {
        'total_files': total,
        'compliant_files': compliant,
        'non_compliant_files': total - compliant,
        'compliance_rate': compliant / total if total > 0 else 1.0,
        'violations': violations
    }


def find_similar_files_with_naming(
    expected: str,
    all_files: List[str],
    standard: Dict,
    threshold: float = 0.6
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    Find similar files, separated into compliant and non-compliant.
    
    Args:
        expected: Expected file path
        all_files: List of all file paths to search
        standard: Naming convention standard
        threshold: Minimum similarity threshold
    
    Returns:
        Tuple of (compliant_matches, non_compliant_matches)
        Each is a list of (path, similarity) tuples sorted by similarity
    """
    compliant_matches = []
    non_compliant_matches = []
    
    for file_path in all_files:
        # Calculate similarity
        similarity = calculate_base_similarity(expected, file_path)
        if similarity < threshold:
            continue
        
        # Check compliance
        result = validate_file_path(file_path, standard)
        
        if result.compliant:
            compliant_matches.append((file_path, similarity))
        else:
            non_compliant_matches.append((file_path, similarity))
    
    # Sort both lists by similarity (descending)
    compliant_matches.sort(key=lambda x: x[1], reverse=True)
    non_compliant_matches.sort(key=lambda x: x[1], reverse=True)
    
    return compliant_matches, non_compliant_matches


# Convenience function for testing
def test_validation():
    """Test validation functions with sample paths"""
    standard = load_naming_standard(Path.cwd())
    
    test_cases = [
        ('packages/auth-lib/src/services/user-service.ts', True),
        ('packages/auth-lib/src/services/userService.ts', False),
        ('packages/auth-lib/src/providers/sms-provider.ts', True),
        ('packages/auth-lib/src/integrations/sms.provider.ts', False),
        ('packages/auth-lib/src/utils/jwt-util.ts', True),
        ('packages/auth-lib/src/utils/jwt_util.ts', False),
    ]
    
    print("Testing validation:")
    for path, expected_compliant in test_cases:
        result = validate_file_path(path, standard)
        status = "✅" if result.compliant == expected_compliant else "❌"
        print(f"{status} {path}: {result.compliant} (expected {expected_compliant})")
        if result.issues:
            for issue in result.issues:
                print(f"    - {issue}")


if __name__ == '__main__':
    # Run tests when executed directly
    test_validation()
