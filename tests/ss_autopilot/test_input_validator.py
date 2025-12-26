"""
Comprehensive unit tests for input_validator.py

Tests:
- PathValidator.sanitize_path()
- PathValidator.is_safe_path()
- PathValidator.validate_directory_path()
- InputValidator.validate_string()
- InputValidator.validate_spec_id()
- InputValidator.validate_workflow_name()
- InputValidator.sanitize_user_input()
"""

import pytest
import tempfile
import os
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.input_validator import PathValidator, InputValidator


# ============================================================================
# Test PathValidator.sanitize_path()
# ============================================================================

class TestPathValidatorSanitize:
    """Test PathValidator.sanitize_path() method"""
    
    def test_sanitize_valid_path(self):
        """Test sanitizing a valid path"""
        result = PathValidator.sanitize_path(".smartspec/config.json")
        assert result.get("success") is True
        assert "sanitized_path" in result
    
    def test_sanitize_empty_path(self):
        """Test sanitizing an empty path"""
        result = PathValidator.sanitize_path("")
        assert result.get("error") is True
        assert result.get("error_code") == "INVALID_INPUT"
    
    def test_sanitize_path_with_traversal(self):
        """Test path with parent directory traversal"""
        result = PathValidator.sanitize_path("../../../etc/passwd")
        assert result.get("error") is True
    
    def test_sanitize_path_with_home_expansion(self):
        """Test path with home directory expansion"""
        result = PathValidator.sanitize_path("~/secret/file.txt")
        assert result.get("error") is True
    
    def test_sanitize_path_with_env_var(self):
        """Test path with environment variable"""
        result = PathValidator.sanitize_path("$HOME/file.txt")
        assert result.get("error") is True
    
    def test_sanitize_path_with_wildcards(self):
        """Test path with wildcards"""
        result = PathValidator.sanitize_path("*.txt")
        assert result.get("error") is True
    
    def test_sanitize_path_with_pipe(self):
        """Test path with pipe character"""
        result = PathValidator.sanitize_path("file.txt|cat")
        assert result.get("error") is True
    
    def test_sanitize_forbidden_directory(self):
        """Test access to forbidden directory"""
        result = PathValidator.sanitize_path("/etc/passwd")
        assert result.get("error") is True
    
    def test_sanitize_with_base_dir(self):
        """Test sanitization with base directory restriction"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.txt")
            result = PathValidator.sanitize_path(file_path, base_dir=temp_dir)
            assert result.get("success") is True
    
    def test_sanitize_outside_base_dir(self):
        """Test path outside base directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = PathValidator.sanitize_path("/tmp/other.txt", base_dir=temp_dir)
            assert result.get("error") is True
    
    def test_sanitize_invalid_extension(self):
        """Test file with invalid extension"""
        result = PathValidator.sanitize_path("malicious.exe")
        assert result.get("error") is True
    
    def test_sanitize_allowed_extension(self):
        """Test file with allowed extension"""
        result = PathValidator.sanitize_path(".smartspec/test.json")
        assert result.get("success") is True


# ============================================================================
# Test PathValidator.is_safe_path()
# ============================================================================

class TestPathValidatorIsSafe:
    """Test PathValidator.is_safe_path() method"""
    
    def test_is_safe_valid_path(self):
        """Test safe path returns True"""
        assert PathValidator.is_safe_path(".smartspec/config.json") is True
    
    def test_is_safe_dangerous_path(self):
        """Test dangerous path returns False"""
        assert PathValidator.is_safe_path("../../../etc/passwd") is False
    
    def test_is_safe_empty_path(self):
        """Test empty path returns False"""
        assert PathValidator.is_safe_path("") is False


# ============================================================================
# Test PathValidator.validate_directory_path()
# ============================================================================

class TestPathValidatorDirectory:
    """Test PathValidator.validate_directory_path() method"""
    
    def test_validate_existing_directory(self):
        """Test validating an existing directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = PathValidator.validate_directory_path(temp_dir)
            assert result.get("success") is True
            assert result.get("exists") is True
            assert result.get("is_directory") is True
    
    def test_validate_nonexistent_directory(self):
        """Test validating a non-existent directory"""
        result = PathValidator.validate_directory_path(".smartspec/nonexistent")
        assert result.get("success") is True
        assert result.get("exists") is False
    
    def test_validate_file_as_directory(self):
        """Test validating a file path as directory"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as f:
            temp_path = f.name
        
        try:
            result = PathValidator.validate_directory_path(temp_path)
            assert result.get("error") is True
        finally:
            os.unlink(temp_path)
    
    def test_validate_empty_directory_path(self):
        """Test validating empty directory path"""
        result = PathValidator.validate_directory_path("")
        assert result.get("error") is True


# ============================================================================
# Test InputValidator.validate_string()
# ============================================================================

class TestInputValidatorString:
    """Test InputValidator.validate_string() method"""
    
    def test_validate_valid_string(self):
        """Test validating a valid string"""
        result = InputValidator.validate_string("test", "field_name")
        assert result.get("success") is True
        assert result.get("validated_value") == "test"
    
    def test_validate_empty_string(self):
        """Test validating an empty string"""
        result = InputValidator.validate_string("", "field_name")
        assert result.get("error") is True
    
    def test_validate_string_min_length(self):
        """Test string minimum length validation"""
        result = InputValidator.validate_string("ab", "field_name", min_length=3)
        assert result.get("error") is True
    
    def test_validate_string_max_length(self):
        """Test string maximum length validation"""
        result = InputValidator.validate_string("toolong", "field_name", max_length=5)
        assert result.get("error") is True
    
    def test_validate_string_pattern(self):
        """Test string pattern validation"""
        result = InputValidator.validate_string(
            "test123",
            "field_name",
            pattern=r'^[a-z]+$'
        )
        assert result.get("error") is True
    
    def test_validate_string_allowed_values(self):
        """Test string allowed values validation"""
        result = InputValidator.validate_string(
            "invalid",
            "field_name",
            allowed_values=["valid1", "valid2"]
        )
        assert result.get("error") is True
    
    def test_validate_string_with_whitespace(self):
        """Test string with leading/trailing whitespace"""
        result = InputValidator.validate_string("  test  ", "field_name")
        assert result.get("success") is True
        assert result.get("validated_value") == "test"


# ============================================================================
# Test InputValidator.validate_spec_id()
# ============================================================================

class TestInputValidatorSpecId:
    """Test InputValidator.validate_spec_id() method"""
    
    def test_validate_valid_spec_id(self):
        """Test validating a valid spec ID"""
        result = InputValidator.validate_spec_id("spec-core-001-authentication")
        assert result.get("success") is True
    
    def test_validate_invalid_spec_id_format(self):
        """Test invalid spec ID format"""
        result = InputValidator.validate_spec_id("invalid-spec-id")
        assert result.get("error") is True
    
    def test_validate_spec_id_uppercase(self):
        """Test spec ID with uppercase (should fail)"""
        result = InputValidator.validate_spec_id("spec-CORE-001-auth")
        assert result.get("error") is True
    
    def test_validate_spec_id_no_number(self):
        """Test spec ID without number"""
        result = InputValidator.validate_spec_id("spec-core-auth")
        assert result.get("error") is True
    
    def test_validate_spec_id_too_short(self):
        """Test spec ID that is too short"""
        result = InputValidator.validate_spec_id("spec-c-1")
        assert result.get("error") is True


# ============================================================================
# Test InputValidator.validate_workflow_name()
# ============================================================================

class TestInputValidatorWorkflowName:
    """Test InputValidator.validate_workflow_name() method"""
    
    def test_validate_valid_workflow_name(self):
        """Test validating a valid workflow name"""
        result = InputValidator.validate_workflow_name("smartspec_generate_spec")
        assert result.get("success") is True
    
    def test_validate_workflow_name_uppercase(self):
        """Test workflow name with uppercase (should fail)"""
        result = InputValidator.validate_workflow_name("SmartSpec_Generate")
        assert result.get("error") is True
    
    def test_validate_workflow_name_with_dash(self):
        """Test workflow name with dash (should fail)"""
        result = InputValidator.validate_workflow_name("smartspec-generate")
        assert result.get("error") is True
    
    def test_validate_workflow_name_too_short(self):
        """Test workflow name that is too short"""
        result = InputValidator.validate_workflow_name("ab")
        assert result.get("error") is True
    
    def test_validate_workflow_name_starts_with_number(self):
        """Test workflow name starting with number (should fail)"""
        result = InputValidator.validate_workflow_name("1_workflow")
        assert result.get("error") is True


# ============================================================================
# Test InputValidator.sanitize_user_input()
# ============================================================================

class TestInputValidatorSanitize:
    """Test InputValidator.sanitize_user_input() method"""
    
    def test_sanitize_clean_input(self):
        """Test sanitizing clean input"""
        result = InputValidator.sanitize_user_input("Hello World")
        assert result.get("success") is True
        assert result.get("sanitized_input") == "Hello World"
        assert result.get("was_modified") is False
    
    def test_sanitize_input_with_html(self):
        """Test sanitizing input with HTML tags"""
        result = InputValidator.sanitize_user_input("<script>alert('xss')</script>")
        assert result.get("success") is True
        assert "<" not in result.get("sanitized_input")
        assert ">" not in result.get("sanitized_input")
        assert result.get("was_modified") is True
    
    def test_sanitize_input_with_sql(self):
        """Test sanitizing input with SQL injection attempt"""
        result = InputValidator.sanitize_user_input("'; DROP TABLE users; --")
        assert result.get("success") is True
        assert ";" not in result.get("sanitized_input")
        assert result.get("was_modified") is True
    
    def test_sanitize_input_with_command(self):
        """Test sanitizing input with command injection attempt"""
        result = InputValidator.sanitize_user_input("test | cat /etc/passwd")
        assert result.get("success") is True
        assert "|" not in result.get("sanitized_input")
        assert result.get("was_modified") is True
    
    def test_sanitize_empty_input(self):
        """Test sanitizing empty input"""
        result = InputValidator.sanitize_user_input("")
        assert result.get("success") is True
        assert result.get("sanitized_input") == ""
    
    def test_sanitize_input_with_control_chars(self):
        """Test sanitizing input with control characters"""
        result = InputValidator.sanitize_user_input("test\x00\x01\x02")
        assert result.get("success") is True
        assert "\x00" not in result.get("sanitized_input")
        assert result.get("was_modified") is True


# ============================================================================
# Integration Tests
# ============================================================================

class TestInputValidatorIntegration:
    """Integration tests for input_validator module"""
    
    def test_validate_and_sanitize_path(self):
        """Test validating and sanitizing a path"""
        # First sanitize
        path_result = PathValidator.sanitize_path(".smartspec/test.json")
        assert path_result.get("success") is True
        
        # Then validate as safe
        assert PathValidator.is_safe_path(".smartspec/test.json") is True
    
    def test_validate_spec_id_and_path(self):
        """Test validating spec ID and constructing safe path"""
        # Validate spec ID
        spec_result = InputValidator.validate_spec_id("spec-core-001-auth")
        assert spec_result.get("success") is True
        
        # Construct path from spec ID
        spec_id = spec_result.get("validated_value")
        spec_path = f"specs/{spec_id}.md"
        
        # Validate path
        path_result = PathValidator.sanitize_path(spec_path)
        assert path_result.get("success") is True
    
    def test_sanitize_user_input_then_validate(self):
        """Test sanitizing user input then validating"""
        # Sanitize
        sanitize_result = InputValidator.sanitize_user_input("  Test Input  ")
        assert sanitize_result.get("success") is True
        
        # Validate
        sanitized = sanitize_result.get("sanitized_input")
        validate_result = InputValidator.validate_string(
            sanitized,
            "user_input",
            min_length=5
        )
        assert validate_result.get("success") is True


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
