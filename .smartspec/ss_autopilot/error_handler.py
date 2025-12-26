"""
Error Handler Module for SmartSpec Autopilot

Provides comprehensive error handling, recovery mechanisms, and user-friendly error messages.

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

from typing import Dict, Any, Optional, Callable
from functools import wraps
from pathlib import Path
import traceback
import sys


class AutopilotError(Exception):
    """Base exception for all Autopilot errors."""
    
    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for JSON serialization."""
        return {
            "error": True,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "type": self.__class__.__name__
        }


class FileNotFoundError(AutopilotError):
    """Raised when a required file is not found."""
    
    def __init__(self, file_path: str, suggestion: Optional[str] = None):
        details = {"file_path": file_path}
        if suggestion:
            details["suggestion"] = suggestion
        
        super().__init__(
            message=f"File not found: {file_path}",
            error_code="FILE_NOT_FOUND",
            details=details
        )


class PermissionDeniedError(AutopilotError):
    """Raised when permission is denied for file/directory access."""
    
    def __init__(self, path: str, operation: str):
        super().__init__(
            message=f"Permission denied: Cannot {operation} {path}",
            error_code="PERMISSION_DENIED",
            details={"path": path, "operation": operation}
        )


class InvalidInputError(AutopilotError):
    """Raised when input validation fails."""
    
    def __init__(self, input_name: str, input_value: Any, reason: str):
        super().__init__(
            message=f"Invalid {input_name}: {reason}",
            error_code="INVALID_INPUT",
            details={
                "input_name": input_name,
                "input_value": str(input_value),
                "reason": reason
            }
        )


class WorkflowNotFoundError(AutopilotError):
    """Raised when a workflow is not found."""
    
    def __init__(self, workflow_name: str, available_workflows: Optional[list] = None):
        details = {"workflow_name": workflow_name}
        if available_workflows:
            details["available_workflows"] = available_workflows[:5]  # Show first 5
        
        super().__init__(
            message=f"Workflow not found: {workflow_name}",
            error_code="WORKFLOW_NOT_FOUND",
            details=details
        )


class SpecNotFoundError(AutopilotError):
    """Raised when a spec is not found."""
    
    def __init__(self, spec_id: str, suggestion: Optional[str] = None):
        details = {"spec_id": spec_id}
        if suggestion:
            details["suggestion"] = suggestion
        
        super().__init__(
            message=f"Spec not found: {spec_id}",
            error_code="SPEC_NOT_FOUND",
            details=details
        )


class ParseError(AutopilotError):
    """Raised when parsing fails."""
    
    def __init__(self, file_path: str, reason: str):
        super().__init__(
            message=f"Failed to parse {file_path}: {reason}",
            error_code="PARSE_ERROR",
            details={"file_path": file_path, "reason": reason}
        )


class ConfigurationError(AutopilotError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, config_key: str, reason: str):
        super().__init__(
            message=f"Configuration error for '{config_key}': {reason}",
            error_code="CONFIGURATION_ERROR",
            details={"config_key": config_key, "reason": reason}
        )


def safe_file_read(file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Safely read a file with comprehensive error handling.
    
    Args:
        file_path: Path to file to read
        encoding: File encoding (default: utf-8)
    
    Returns:
        Dict with 'success', 'content', or 'error' keys
    """
    try:
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(
                file_path=file_path,
                suggestion=f"Check if the file exists or create it first"
            )
        
        # Check if it's a file (not directory)
        if not path.is_file():
            raise InvalidInputError(
                input_name="file_path",
                input_value=file_path,
                reason="Path is a directory, not a file"
            )
        
        # Try to read file
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "file_path": file_path,
            "size": len(content)
        }
    
    except FileNotFoundError as e:
        return e.to_dict()
    
    except PermissionError:
        error = PermissionDeniedError(path=file_path, operation="read")
        return error.to_dict()
    
    except UnicodeDecodeError as e:
        error = ParseError(
            file_path=file_path,
            reason=f"Invalid encoding (expected {encoding}): {str(e)}"
        )
        return error.to_dict()
    
    except Exception as e:
        return {
            "error": True,
            "error_code": "UNKNOWN_ERROR",
            "message": f"Unexpected error reading file: {str(e)}",
            "details": {
                "file_path": file_path,
                "exception_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        }


def safe_file_write(file_path: str, content: str, encoding: str = 'utf-8', 
                   create_dirs: bool = True) -> Dict[str, Any]:
    """
    Safely write content to a file with comprehensive error handling.
    
    Args:
        file_path: Path to file to write
        content: Content to write
        encoding: File encoding (default: utf-8)
        create_dirs: Create parent directories if they don't exist
    
    Returns:
        Dict with 'success' or 'error' keys
    """
    try:
        path = Path(file_path)
        
        # Create parent directories if needed
        if create_dirs and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check write permission on parent directory
        if not path.parent.exists():
            raise PermissionDeniedError(
                path=str(path.parent),
                operation="create directory"
            )
        
        # Write file
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": file_path,
            "bytes_written": len(content.encode(encoding))
        }
    
    except PermissionError:
        error = PermissionDeniedError(path=file_path, operation="write")
        return error.to_dict()
    
    except OSError as e:
        return {
            "error": True,
            "error_code": "OS_ERROR",
            "message": f"OS error writing file: {str(e)}",
            "details": {
                "file_path": file_path,
                "exception_type": type(e).__name__
            }
        }
    
    except Exception as e:
        return {
            "error": True,
            "error_code": "UNKNOWN_ERROR",
            "message": f"Unexpected error writing file: {str(e)}",
            "details": {
                "file_path": file_path,
                "exception_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        }


def safe_execute(func: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Safely execute a function with comprehensive error handling.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        **kwargs: Keyword arguments
    
    Returns:
        Dict with 'success', 'result', or 'error' keys
    """
    try:
        result = func(*args, **kwargs)
        return {
            "success": True,
            "result": result
        }
    
    except AutopilotError as e:
        return e.to_dict()
    
    except Exception as e:
        return {
            "error": True,
            "error_code": "EXECUTION_ERROR",
            "message": f"Error executing {func.__name__}: {str(e)}",
            "details": {
                "function": func.__name__,
                "exception_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        }


def with_error_handling(func: Callable) -> Callable:
    """
    Decorator to add comprehensive error handling to any function.
    
    Usage:
        @with_error_handling
        def my_function(arg1, arg2):
            # Your code here
            pass
    
    Returns:
        Dict with 'success', 'result', or 'error' keys
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            result = func(*args, **kwargs)
            
            # If result is already a dict with error/success, return as-is
            if isinstance(result, dict) and ('error' in result or 'success' in result):
                return result
            
            # Otherwise wrap in success dict
            return {
                "success": True,
                "result": result
            }
        
        except AutopilotError as e:
            return e.to_dict()
        
        except Exception as e:
            return {
                "error": True,
                "error_code": "EXECUTION_ERROR",
                "message": f"Error in {func.__name__}: {str(e)}",
                "details": {
                    "function": func.__name__,
                    "exception_type": type(e).__name__,
                    "traceback": traceback.format_exc()
                }
            }
    
    return wrapper


def handle_errors(default_return: Any = None):
    """
    Decorator to handle errors and return a default value on failure.
    
    Usage:
        @handle_errors(default_return=[])
        def my_function():
            # Your code here
            pass
    
    Args:
        default_return: Value to return on error
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}", file=sys.stderr)
                return default_return
        return wrapper
    return decorator


def get_user_friendly_error(error_dict: Dict[str, Any]) -> str:
    """
    Convert error dict to user-friendly error message.
    
    Args:
        error_dict: Error dictionary from safe_* functions
    
    Returns:
        User-friendly error message
    """
    if not error_dict.get("error"):
        return "No error"
    
    error_code = error_dict.get("error_code", "UNKNOWN")
    message = error_dict.get("message", "Unknown error")
    details = error_dict.get("details", {})
    
    # Customize messages based on error code
    if error_code == "FILE_NOT_FOUND":
        file_path = details.get("file_path", "unknown")
        suggestion = details.get("suggestion", "")
        return f"❌ ไม่พบไฟล์: {file_path}\n💡 {suggestion}" if suggestion else f"❌ ไม่พบไฟล์: {file_path}"
    
    elif error_code == "PERMISSION_DENIED":
        path = details.get("path", "unknown")
        operation = details.get("operation", "access")
        return f"❌ ไม่มีสิทธิ์ {operation}: {path}\n💡 ตรวจสอบ file permissions หรือรันด้วย sudo"
    
    elif error_code == "INVALID_INPUT":
        input_name = details.get("input_name", "input")
        reason = details.get("reason", "invalid")
        return f"❌ {input_name} ไม่ถูกต้อง: {reason}"
    
    elif error_code == "WORKFLOW_NOT_FOUND":
        workflow_name = details.get("workflow_name", "unknown")
        available = details.get("available_workflows", [])
        msg = f"❌ ไม่พบ workflow: {workflow_name}"
        if available:
            msg += f"\n💡 workflows ที่มี: {', '.join(available[:3])}..."
        return msg
    
    elif error_code == "SPEC_NOT_FOUND":
        spec_id = details.get("spec_id", "unknown")
        suggestion = details.get("suggestion", "")
        msg = f"❌ ไม่พบ spec: {spec_id}"
        if suggestion:
            msg += f"\n💡 {suggestion}"
        return msg
    
    else:
        return f"❌ {message}"


# Export all
__all__ = [
    'AutopilotError',
    'FileNotFoundError',
    'PermissionDeniedError',
    'InvalidInputError',
    'WorkflowNotFoundError',
    'SpecNotFoundError',
    'ParseError',
    'ConfigurationError',
    'safe_file_read',
    'safe_file_write',
    'safe_execute',
    'with_error_handling',
    'handle_errors',
    'get_user_friendly_error',
]
