"""
Comprehensive unit tests for error_handler.py

Tests:
- All 7 custom exception classes
- safe_file_read() function
- safe_file_write() function
- @with_error_handling decorator
- get_user_friendly_error() function
"""

import pytest
import tempfile
import os
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.error_handler import (
    AutopilotError,
    FileNotFoundError,
    PermissionDeniedError,
    InvalidInputError,
    WorkflowNotFoundError,
    SpecNotFoundError,
    ParseError,
    ConfigurationError,
    safe_file_read,
    safe_file_write,
    with_error_handling,
    get_user_friendly_error
)


# ============================================================================
# Test Custom Exception Classes
# ============================================================================

class TestCustomExceptions:
    """Test all custom exception classes"""
    
    def test_autopilot_error_base(self):
        """Test AutopilotError base class"""
        error = AutopilotError("Test error", "TEST_ERROR")
        assert str(error) == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert isinstance(error, Exception)
        
        error_dict = error.to_dict()
        assert error_dict["error"] is True
        assert error_dict["error_code"] == "TEST_ERROR"
    
    def test_file_not_found_error(self):
        """Test FileNotFoundError"""
        error = FileNotFoundError("/path/to/file.txt")
        assert "file.txt" in str(error)
        assert error.error_code == "FILE_NOT_FOUND"
        
        error_dict = error.to_dict()
        assert error_dict["details"]["file_path"] == "/path/to/file.txt"
    
    def test_permission_denied_error(self):
        """Test PermissionDeniedError"""
        error = PermissionDeniedError("/path/to/file.txt", "write")
        assert "Permission denied" in str(error)
        assert error.error_code == "PERMISSION_DENIED"
        
        error_dict = error.to_dict()
        assert error_dict["details"]["path"] == "/path/to/file.txt"
        assert error_dict["details"]["operation"] == "write"
    
    def test_invalid_input_error(self):
        """Test InvalidInputError"""
        error = InvalidInputError("user_input", "test", "empty string")
        assert "Invalid" in str(error)
        assert error.error_code == "INVALID_INPUT"
    
    def test_workflow_not_found_error(self):
        """Test WorkflowNotFoundError"""
        error = WorkflowNotFoundError("my_workflow")
        assert "my_workflow" in str(error)
        assert error.error_code == "WORKFLOW_NOT_FOUND"
    
    def test_spec_not_found_error(self):
        """Test SpecNotFoundError"""
        error = SpecNotFoundError("spec-001")
        assert "spec-001" in str(error)
        assert error.error_code == "SPEC_NOT_FOUND"
    
    def test_parse_error(self):
        """Test ParseError"""
        error = ParseError("/path/to/file.json", "Invalid JSON")
        assert "Parse" in str(error) or "parse" in str(error)
        assert error.error_code == "PARSE_ERROR"
    
    def test_configuration_error(self):
        """Test ConfigurationError"""
        error = ConfigurationError("api_key", "API key not found")
        assert "Configuration" in str(error) or "configuration" in str(error)
        assert error.error_code == "CONFIGURATION_ERROR"


# ============================================================================
# Test safe_file_read()
# ============================================================================

class TestSafeFileRead:
    """Test safe_file_read() function"""
    
    def test_read_existing_file(self):
        """Test reading an existing file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello, World!")
            temp_path = f.name
        
        try:
            result = safe_file_read(temp_path)
            assert result.get("success") is True
            assert result.get("content") == "Hello, World!"
            assert "error" not in result or result.get("error") is not True
        finally:
            os.unlink(temp_path)
    
    def test_read_nonexistent_file(self):
        """Test reading a non-existent file"""
        result = safe_file_read("/nonexistent/file.txt")
        assert result.get("error") is True
        assert result.get("error_code") == "FILE_NOT_FOUND"
    
    def test_read_empty_file(self):
        """Test reading an empty file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_path = f.name
        
        try:
            result = safe_file_read(temp_path)
            assert result.get("success") is True
            assert result.get("content") == ""
        finally:
            os.unlink(temp_path)
    
    def test_read_unicode_file(self):
        """Test reading a file with Unicode content"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            f.write("สวัสดี 你好 مرحبا")
            temp_path = f.name
        
        try:
            result = safe_file_read(temp_path)
            assert result.get("success") is True
            assert "สวัสดี" in result.get("content", "")
        finally:
            os.unlink(temp_path)


# ============================================================================
# Test safe_file_write()
# ============================================================================

class TestSafeFileWrite:
    """Test safe_file_write() function"""
    
    def test_write_new_file(self):
        """Test writing to a new file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.txt")
            result = safe_file_write(file_path, "Hello, World!")
            
            assert result.get("success") is True
            assert os.path.exists(file_path)
            
            with open(file_path, 'r') as f:
                assert f.read() == "Hello, World!"
    
    def test_overwrite_existing_file(self):
        """Test overwriting an existing file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Old content")
            temp_path = f.name
        
        try:
            result = safe_file_write(temp_path, "New content")
            assert result.get("success") is True
            
            with open(temp_path, 'r') as f:
                assert f.read() == "New content"
        finally:
            os.unlink(temp_path)
    
    def test_write_unicode_content(self):
        """Test writing Unicode content"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "unicode.txt")
            content = "สวัสดี 你好 مرحبا"
            result = safe_file_write(file_path, content)
            
            assert result.get("success") is True
            
            with open(file_path, 'r', encoding='utf-8') as f:
                assert f.read() == content
    
    def test_write_creates_directories(self):
        """Test that write creates parent directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "subdir1", "subdir2", "test.txt")
            result = safe_file_write(file_path, "Content")
            
            assert result.get("success") is True
            assert os.path.exists(file_path)


# ============================================================================
# Test @with_error_handling decorator
# ============================================================================

class TestWithErrorHandlingDecorator:
    """Test @with_error_handling decorator"""
    
    def test_decorator_on_successful_function(self):
        """Test decorator on a function that succeeds"""
        @with_error_handling
        def successful_function(x, y):
            return x + y
        
        result = successful_function(2, 3)
        assert result.get("success") is True
        assert result.get("result") == 5
    
    def test_decorator_on_failing_function(self):
        """Test decorator on a function that raises an exception"""
        @with_error_handling
        def failing_function():
            raise ValueError("Test error")
        
        result = failing_function()
        assert result.get("error") is True
        assert result.get("error_code") == "EXECUTION_ERROR"
    
    def test_decorator_with_custom_exception(self):
        """Test decorator with custom AutopilotError"""
        @with_error_handling
        def custom_error_function():
            raise FileNotFoundError("/path/to/file.txt")
        
        result = custom_error_function()
        assert result.get("error") is True
        assert result.get("error_code") == "FILE_NOT_FOUND"
    
    def test_decorator_preserves_dict_with_error(self):
        """Test that decorator preserves dict with error key"""
        @with_error_handling
        def return_error_dict():
            return {"error": True, "message": "Custom error"}
        
        result = return_error_dict()
        assert result.get("error") is True
        assert result.get("message") == "Custom error"
    
    def test_decorator_with_arguments(self):
        """Test decorator with function arguments"""
        @with_error_handling
        def function_with_args(a, b, c=None):
            if c is None:
                return a + b
            return a + b + c
        
        result1 = function_with_args(1, 2)
        assert result1.get("success") is True
        assert result1.get("result") == 3
        
        result2 = function_with_args(1, 2, c=3)
        assert result2.get("success") is True
        assert result2.get("result") == 6


# ============================================================================
# Test get_user_friendly_error()
# ============================================================================

class TestGetUserFriendlyError:
    """Test get_user_friendly_error() function"""
    
    def test_file_not_found_error_message(self):
        """Test user-friendly message for FileNotFoundError"""
        error_dict = {
            "error": True,
            "error_code": "FILE_NOT_FOUND",
            "message": "File not found: /path/to/file.txt",
            "details": {"file_path": "/path/to/file.txt"}
        }
        
        message = get_user_friendly_error(error_dict)
        assert "ไม่พบไฟล์" in message
        assert "/path/to/file.txt" in message
    
    def test_permission_denied_error_message(self):
        """Test user-friendly message for PermissionDeniedError"""
        error_dict = {
            "error": True,
            "error_code": "PERMISSION_DENIED",
            "message": "Permission denied",
            "details": {"path": "/path/to/file.txt", "operation": "write"}
        }
        
        message = get_user_friendly_error(error_dict)
        assert "ไม่มีสิทธิ์" in message
    
    def test_generic_error_message(self):
        """Test user-friendly message for generic error"""
        error_dict = {
            "error": True,
            "error_code": "UNKNOWN_ERROR",
            "message": "Invalid value",
            "details": {}
        }
        
        message = get_user_friendly_error(error_dict)
        assert "❌" in message
        assert "Invalid value" in message


# ============================================================================
# Integration Tests
# ============================================================================

class TestErrorHandlerIntegration:
    """Integration tests for error_handler module"""
    
    def test_read_write_cycle(self):
        """Test complete read-write cycle"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.txt")
            
            # Write
            write_result = safe_file_write(file_path, "Test content")
            assert write_result.get("success") is True
            
            # Read
            read_result = safe_file_read(file_path)
            assert read_result.get("success") is True
            assert read_result.get("content") == "Test content"
    
    def test_decorator_with_safe_file_operations(self):
        """Test decorator combined with safe file operations"""
        @with_error_handling
        def read_and_process(file_path):
            result = safe_file_read(file_path)
            if result.get("error"):
                raise FileNotFoundError(file_path)
            return result.get("content", "").upper()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("hello world")
            temp_path = f.name
        
        try:
            result = read_and_process(temp_path)
            assert result.get("success") is True
            assert result.get("result") == "HELLO WORLD"
        finally:
            os.unlink(temp_path)
    
    def test_error_propagation(self):
        """Test error propagation through decorator"""
        @with_error_handling
        def nested_function():
            raise FileNotFoundError("/nonexistent/file.txt")
        
        result = nested_function()
        assert result.get("error") is True
        assert result.get("error_code") == "FILE_NOT_FOUND"


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
