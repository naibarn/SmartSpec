#!/usr/bin/env python3
"""
Test suite for naming convention integration

Tests all helper functions and integration points.
"""

import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from naming_convention_helper import (
    load_naming_standard,
    is_kebab_case,
    detect_file_type,
    validate_file_path,
    is_compliant,
    get_violations,
    calculate_base_similarity,
    similarity_with_naming,
    find_compliant_matches,
    format_naming_issues,
    get_naming_statistics,
    find_similar_files_with_naming
)


def test_kebab_case():
    """Test kebab-case detection"""
    print("Testing kebab-case detection...")
    
    test_cases = [
        ('user-service.ts', True),
        ('userService.ts', False),
        ('user_service.ts', False),
        ('UserService.ts', False),
        ('user-service-v2.ts', True),
        ('user.service.ts', True),  # Has dots but stem is kebab
        ('123-test.ts', True),
        ('test-123.ts', True),
        ('test--double.ts', False),  # Double dash
        ('-test.ts', False),  # Leading dash
        ('test-.ts', False),  # Trailing dash
    ]
    
    for filename, expected in test_cases:
        result = is_kebab_case(filename)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {filename}: {result} (expected {expected})")
        if result != expected:
            raise AssertionError(f"Failed: {filename}")
    
    print("✅ Kebab-case tests passed\n")


def test_file_type_detection():
    """Test file type detection"""
    print("Testing file type detection...")
    
    standard = load_naming_standard(Path.cwd())
    
    test_cases = [
        ('user-service.ts', 'service'),
        ('sms-provider.ts', 'provider'),
        ('auth-client.ts', 'client'),
        ('user-controller.ts', 'controller'),
        ('auth-middleware.ts', 'middleware'),
        ('jwt-util.ts', 'util'),
        ('user-model.ts', 'model'),
        ('user.ts', None),  # No suffix
        ('index.ts', None),  # Special file
        ('user-service.js', 'service'),  # JavaScript
    ]
    
    for filename, expected in test_cases:
        result = detect_file_type(filename, standard)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {filename}: {result} (expected {expected})")
        if result != expected:
            raise AssertionError(f"Failed: {filename}")
    
    print("✅ File type detection tests passed\n")


def test_validation():
    """Test path validation"""
    print("Testing path validation...")
    
    standard = load_naming_standard(Path.cwd())
    
    test_cases = [
        # (path, expected_compliant, expected_issues_count)
        ('packages/auth-lib/src/services/user-service.ts', True, 0),
        ('packages/auth-lib/src/services/userService.ts', False, 2),  # Not kebab + no suffix
        ('packages/auth-lib/src/providers/sms-provider.ts', True, 0),
        ('packages/auth-lib/src/integrations/sms-provider.ts', False, 1),  # Wrong directory
        ('packages/auth-lib/src/utils/jwt-util.ts', True, 0),
        ('packages/auth-lib/src/utils/jwt_util.ts', False, 2),  # Not kebab + no suffix
        ('packages/auth-lib/src/index.ts', True, 0),  # Special file
    ]
    
    for path, expected_compliant, expected_issues_count in test_cases:
        result = validate_file_path(path, standard)
        status = "✅" if result.compliant == expected_compliant else "❌"
        print(f"  {status} {path}")
        print(f"      Compliant: {result.compliant} (expected {expected_compliant})")
        print(f"      Issues: {len(result.issues)} (expected {expected_issues_count})")
        if result.issues:
            for issue in result.issues:
                print(f"        - {issue}")
        
        if result.compliant != expected_compliant:
            raise AssertionError(f"Failed: {path}")
        if len(result.issues) != expected_issues_count:
            raise AssertionError(f"Failed: {path} - wrong number of issues")
    
    print("✅ Validation tests passed\n")


def test_compliance_check():
    """Test quick compliance check"""
    print("Testing compliance check...")
    
    standard = load_naming_standard(Path.cwd())
    
    test_cases = [
        ('packages/auth-lib/src/services/user-service.ts', True),
        ('packages/auth-lib/src/services/userService.ts', False),
        ('packages/auth-lib/src/providers/sms-provider.ts', True),
    ]
    
    for path, expected in test_cases:
        result = is_compliant(path, standard)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {path}: {result} (expected {expected})")
        if result != expected:
            raise AssertionError(f"Failed: {path}")
    
    print("✅ Compliance check tests passed\n")


def test_similarity():
    """Test similarity calculation"""
    print("Testing similarity calculation...")
    
    standard = load_naming_standard(Path.cwd())
    
    # Test exact match
    sim1 = calculate_base_similarity(
        'packages/auth-lib/src/services/user-service.ts',
        'packages/auth-lib/src/services/user-service.ts'
    )
    print(f"  Exact match: {sim1:.2f} (expected 1.0)")
    assert abs(sim1 - 1.0) < 0.01, "Exact match should be 1.0"
    
    # Test similar paths
    sim2 = calculate_base_similarity(
        'packages/auth-lib/src/services/user-service.ts',
        'packages/auth-lib/src/services/auth-service.ts'
    )
    print(f"  Similar paths: {sim2:.2f} (expected 0.7-0.9)")
    assert 0.7 < sim2 < 0.9, "Similar paths should have high similarity"
    
    # Test different paths
    sim3 = calculate_base_similarity(
        'packages/auth-lib/src/services/user-service.ts',
        'packages/auth-lib/src/providers/sms-provider.ts'
    )
    print(f"  Different paths: {sim3:.2f} (expected 0.4-0.7)")
    assert 0.4 < sim3 < 0.7, "Different paths should have medium similarity"
    
    # Test with naming bonus
    sim4 = similarity_with_naming(
        'packages/auth-lib/src/services/user-service.ts',
        'packages/auth-lib/src/services/user-service.ts',
        standard
    )
    print(f"  With naming bonus (exact): {sim4:.2f} (expected 1.0)")
    assert abs(sim4 - 1.0) < 0.01, "Exact match with bonus should be 1.0"
    
    print("✅ Similarity tests passed\n")


def test_compliant_matches():
    """Test finding compliant matches"""
    print("Testing compliant matches...")
    
    standard = load_naming_standard(Path.cwd())
    
    expected = 'packages/auth-lib/src/services/user-service.ts'
    candidates = [
        'packages/auth-lib/src/services/user-service.ts',  # Exact match (compliant)
        'packages/auth-lib/src/services/userService.ts',   # Non-compliant
        'packages/auth-lib/src/services/auth-service.ts',  # Compliant but different
        'packages/auth-lib/src/providers/sms-provider.ts', # Compliant but very different
    ]
    
    matches = find_compliant_matches(expected, candidates, standard, threshold=0.5)
    
    print(f"  Found {len(matches)} compliant matches")
    for path, similarity in matches:
        print(f"    - {path}: {similarity:.2f}")
    
    # Should find at least exact match and similar compliant file
    assert len(matches) >= 2, f"Expected at least 2 matches, got {len(matches)}"
    
    # First match should be exact
    assert matches[0][0] == expected, "First match should be exact"
    assert matches[0][1] >= 0.95, "Exact match should have very high similarity"
    
    print("✅ Compliant matches tests passed\n")


def test_statistics():
    """Test statistics calculation"""
    print("Testing statistics calculation...")
    
    standard = load_naming_standard(Path.cwd())
    
    files = [
        'packages/auth-lib/src/services/user-service.ts',  # Compliant
        'packages/auth-lib/src/services/userService.ts',   # Non-compliant
        'packages/auth-lib/src/providers/sms-provider.ts', # Compliant
        'packages/auth-lib/src/utils/jwt-util.ts',         # Compliant
        'packages/auth-lib/src/utils/jwt_util.ts',         # Non-compliant
    ]
    
    stats = get_naming_statistics(files, standard)
    
    print(f"  Total files: {stats['total_files']} (expected 5)")
    print(f"  Compliant: {stats['compliant_files']} (expected 3)")
    print(f"  Non-compliant: {stats['non_compliant_files']} (expected 2)")
    print(f"  Compliance rate: {stats['compliance_rate']:.1%} (expected 60%)")
    
    assert stats['total_files'] == 5, "Total should be 5"
    assert stats['compliant_files'] == 3, "Compliant should be 3"
    assert stats['non_compliant_files'] == 2, "Non-compliant should be 2"
    assert abs(stats['compliance_rate'] - 0.6) < 0.01, "Compliance rate should be 60%"
    
    print("✅ Statistics tests passed\n")


def test_similar_files_separation():
    """Test separating similar files by compliance"""
    print("Testing similar files separation...")
    
    standard = load_naming_standard(Path.cwd())
    
    expected = 'packages/auth-lib/src/services/user-service.ts'
    all_files = [
        'packages/auth-lib/src/services/user-service.ts',  # Exact (compliant)
        'packages/auth-lib/src/services/userService.ts',   # Similar (non-compliant)
        'packages/auth-lib/src/services/auth-service.ts',  # Similar (compliant)
        'packages/auth-lib/src/providers/sms-provider.ts', # Different (compliant)
    ]
    
    compliant, non_compliant = find_similar_files_with_naming(
        expected, all_files, standard, threshold=0.6
    )
    
    print(f"  Compliant matches: {len(compliant)}")
    for path, similarity in compliant:
        print(f"    - {path}: {similarity:.2f}")
    
    print(f"  Non-compliant matches: {len(non_compliant)}")
    for path, similarity in non_compliant:
        print(f"    - {path}: {similarity:.2f}")
    
    assert len(compliant) >= 2, "Should find at least 2 compliant matches"
    assert len(non_compliant) >= 1, "Should find at least 1 non-compliant match"
    
    print("✅ Similar files separation tests passed\n")


def test_format_issues():
    """Test formatting issues"""
    print("Testing issue formatting...")
    
    # No issues
    formatted1 = format_naming_issues([])
    print(f"  No issues: {formatted1}")
    assert "✅" in formatted1, "Should show success for no issues"
    
    # With issues
    issues = [
        "Not kebab-case: userService.ts",
        "Wrong directory: expected services/, got integrations/"
    ]
    formatted2 = format_naming_issues(issues)
    print(f"  With issues:\n{formatted2}")
    assert "⚠️" in formatted2, "Should show warning for issues"
    assert all(issue in formatted2 for issue in issues), "Should include all issues"
    
    print("✅ Issue formatting tests passed\n")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Running Naming Convention Integration Tests")
    print("=" * 60)
    print()
    
    try:
        test_kebab_case()
        test_file_type_detection()
        test_validation()
        test_compliance_check()
        test_similarity()
        test_compliant_matches()
        test_statistics()
        test_similar_files_separation()
        test_format_issues()
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
