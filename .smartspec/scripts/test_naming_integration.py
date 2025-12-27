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


def test_camel_to_kebab():
    """Test camelCase to kebab-case conversion"""
    print("Testing camel_to_kebab...")
    
    from naming_convention_helper import camel_to_kebab
    
    test_cases = [
        ('userService', 'user-service'),
        ('SMSProvider', 'sms-provider'),
        ('jwtUtil', 'jwt-util'),
        ('APIClient', 'api-client'),
        ('user-service', 'user-service'),  # Already kebab-case
        ('', ''),  # Empty string
    ]
    
    for input_val, expected in test_cases:
        result = camel_to_kebab(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} camel_to_kebab('{input_val}') = '{result}' (expected '{expected}')")
        if result != expected:
            raise AssertionError(f"Failed: {input_val}")
    
    print("✅ camel_to_kebab tests passed\n")


def test_infer_type():
    """Test file type inference"""
    print("Testing infer_type_from_name...")
    
    from naming_convention_helper import infer_type_from_name
    
    test_cases = [
        ('user-service', 'service'),
        ('sms-provider', 'provider'),
        ('jwt-util', 'util'),
        ('auth-middleware', 'middleware'),
        ('user-model', 'model'),
        ('api-client', 'client'),
        ('random-file', None),  # Cannot infer
    ]
    
    for input_val, expected in test_cases:
        result = infer_type_from_name(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} infer_type_from_name('{input_val}') = {result} (expected {expected})")
        if result != expected:
            raise AssertionError(f"Failed: {input_val}")
    
    print("✅ infer_type_from_name tests passed\n")


def test_auto_correct():
    """Test auto-correction"""
    print("Testing auto_correct_path...")
    
    from naming_convention_helper import auto_correct_path
    standard = load_naming_standard(Path.cwd())
    
    # Test kebab-case correction
    print("  Testing kebab-case correction...")
    path1 = "packages/auth-service/src/services/userService.ts"
    corrected1, changes1 = auto_correct_path(path1, standard)
    assert corrected1 == "packages/auth-service/src/services/user-service.ts", f"Expected user-service.ts, got {corrected1}"
    assert len(changes1) > 0, "Expected changes to be recorded"
    print(f"    ✅ {path1}")
    print(f"       → {corrected1}")
    
    # Test directory correction
    print("  Testing directory correction...")
    path2 = "packages/auth-lib/src/integrations/sms-provider.ts"
    corrected2, changes2 = auto_correct_path(path2, standard)
    assert corrected2 == "packages/auth-lib/src/providers/sms-provider.ts", f"Expected providers/, got {corrected2}"
    assert len(changes2) > 0, "Expected changes to be recorded"
    print(f"    ✅ {path2}")
    print(f"       → {corrected2}")
    
    # Test complex correction
    print("  Testing complex correction...")
    path3 = "packages/auth-lib/src/integrations/smsProvider.ts"
    corrected3, changes3 = auto_correct_path(path3, standard)
    assert corrected3 == "packages/auth-lib/src/providers/sms-provider.ts", f"Expected providers/sms-provider.ts, got {corrected3}"
    assert len(changes3) >= 2, f"Expected multiple changes, got {len(changes3)}"
    print(f"    ✅ {path3}")
    print(f"       → {corrected3}")
    
    # Test already compliant
    print("  Testing already compliant...")
    path4 = "packages/auth-service/src/services/user-service.ts"
    corrected4, changes4 = auto_correct_path(path4, standard)
    assert corrected4 == path4, f"Expected no change, got {corrected4}"
    assert len(changes4) == 0, f"Expected no changes, got {changes4}"
    print(f"    ✅ {path4} (no changes needed)")
    
    print("✅ auto_correct_path tests passed\n")


def test_batch_correction():
    """Test batch auto-correction"""
    print("Testing auto_correct_paths_batch...")
    
    from naming_convention_helper import auto_correct_paths_batch
    standard = load_naming_standard(Path.cwd())
    
    paths = [
        "packages/auth-service/src/services/userService.ts",
        "packages/auth-service/src/services/user-service.ts",  # Already compliant
        "packages/auth-lib/src/integrations/sms-provider.ts",
    ]
    
    result = auto_correct_paths_batch(paths, standard)
    
    print(f"  Total: {result['statistics']['total']} (expected 3)")
    print(f"  Corrected: {result['statistics']['corrected']} (expected 2)")
    print(f"  Unchanged: {result['statistics']['unchanged']} (expected 1)")
    print(f"  Compliance rate: {result['statistics']['compliance_rate']:.0%} (expected 100%)")
    
    assert result['statistics']['total'] == 3, "Expected 3 total paths"
    assert result['statistics']['corrected'] == 2, "Expected 2 corrections"
    assert result['statistics']['unchanged'] == 1, "Expected 1 unchanged"
    assert result['statistics']['compliance_rate'] == 1.0, "Expected 100% compliance"
    
    print("✅ auto_correct_paths_batch tests passed\n")


def test_correction_report():
    """Test correction report formatting"""
    print("Testing format_correction_report...")
    
    from naming_convention_helper import format_correction_report
    
    corrections = [
        {
            'original': 'packages/auth-service/src/services/userService.ts',
            'corrected': 'packages/auth-service/src/services/user-service.ts',
            'changes': ['Changed userService to user-service (kebab-case)']
        }
    ]
    
    report = format_correction_report(corrections)
    assert '## Auto-Corrections Made' in report, "Expected report header"
    assert 'userService.ts' in report, "Expected filename in report"
    print(f"  ✅ Report generated ({len(report)} chars)")
    
    # Test empty corrections
    empty_report = format_correction_report([])
    assert 'No corrections needed' in empty_report, "Expected no corrections message"
    print(f"  ✅ Empty report handled")
    
    print("✅ format_correction_report tests passed\n")


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
        
        # Phase 4 tests
        print("=" * 60)
        print("Phase 4: Auto-Correction Tests")
        print("=" * 60)
        print()
        test_camel_to_kebab()
        test_infer_type()
        test_auto_correct()
        test_batch_correction()
        test_correction_report()
        
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
