"""
Test Helpers - Utility functions for integration tests

Author: SmartSpec Team
Date: 2025-12-26
"""

from typing import Any, Dict


def unwrap_result(result: Any) -> Any:
    """
    Unwrap result from @with_error_handling decorator.
    
    The decorator wraps results in:
    {"success": True, "result": actual_value}
    
    This function extracts the actual_value.
    
    Args:
        result: Wrapped or unwrapped result
        
    Returns:
        Unwrapped result
    """
    if isinstance(result, dict):
        if "success" in result and "result" in result:
            if result["success"]:
                # Recursively unwrap in case of double-wrapping
                return unwrap_result(result["result"])
            else:
                # Error case - return the error dict
                return result
    
    # Already unwrapped or not a dict
    return result


def is_error_result(result: Any) -> bool:
    """
    Check if result is an error from @with_error_handling.
    
    Args:
        result: Result to check
        
    Returns:
        True if error, False otherwise
    """
    if isinstance(result, dict):
        return result.get("success") == False or result.get("error") == True
    
    return False


def get_error_message(result: Dict) -> str:
    """
    Extract error message from error result.
    
    Args:
        result: Error result dict
        
    Returns:
        Error message
    """
    if isinstance(result, dict):
        return result.get("message", "Unknown error")
    
    return str(result)


__all__ = [
    'unwrap_result',
    'is_error_result',
    'get_error_message',
]
