#!/usr/bin/env python3
"""
Path sanitization and validation utilities for SmartSpec.

Prevents path traversal, symlink escape, and other path-based attacks.
"""

import os
import sys
from pathlib import Path


def sanitize_path(path_str, base_dir=None, allow_absolute=False):
    """
    Sanitize and validate a file path.
    
    Args:
        path_str: Path string to sanitize
        base_dir: Base directory that path must be under (optional)
        allow_absolute: Whether to allow absolute paths
    
    Returns:
        Sanitized absolute path
    
    Raises:
        ValueError: If path is invalid or unsafe
    """
    if not path_str:
        raise ValueError("Path cannot be empty")
    
    # Convert to Path object
    path = Path(path_str)
    
    # Check for path traversal attempts
    if ".." in path.parts:
        raise ValueError(f"Path traversal not allowed: {path_str}")
    
    # Check for absolute paths if not allowed
    if not allow_absolute and path.is_absolute():
        raise ValueError(f"Absolute paths not allowed: {path_str}")
    
    # Resolve to absolute path
    if base_dir:
        abs_path = (Path(base_dir) / path).resolve()
        base_resolved = Path(base_dir).resolve()
        
        # Check if path escapes base directory
        try:
            abs_path.relative_to(base_resolved)
        except ValueError:
            raise ValueError(f"Path escapes base directory: {path_str}")
    else:
        abs_path = path.resolve()
    
    # Check for symlink escape
    if abs_path.is_symlink():
        target = abs_path.readlink()
        if target.is_absolute():
            raise ValueError(f"Symlink to absolute path not allowed: {path_str}")
        
        # Recursively check symlink target
        return sanitize_path(str(target), base_dir, allow_absolute)
    
    return str(abs_path)


def validate_registry_path(path_str):
    """Validate that path is under .spec/registry/."""
    try:
        sanitized = sanitize_path(path_str, base_dir=".spec/registry")
        return sanitized
    except ValueError as e:
        raise ValueError(f"Invalid registry path: {e}")


def validate_spec_path(path_str):
    """Validate that path is under specs/."""
    try:
        sanitized = sanitize_path(path_str, base_dir="specs")
        return sanitized
    except ValueError as e:
        raise ValueError(f"Invalid spec path: {e}")


def validate_report_path(path_str):
    """Validate that path is under .spec/reports/."""
    try:
        sanitized = sanitize_path(path_str, base_dir=".spec/reports")
        return sanitized
    except ValueError as e:
        raise ValueError(f"Invalid report path: {e}")


def redact_secrets(text, patterns=None):
    """
    Redact secrets from text.
    
    Args:
        text: Text to redact
        patterns: List of regex patterns to redact (optional)
    
    Returns:
        Redacted text
    """
    import re
    
    if patterns is None:
        # Default patterns
        patterns = [
            r'[A-Za-z0-9]{32,}',  # API keys (long alphanumeric strings)
            r'sk-[A-Za-z0-9]{32,}',  # OpenAI API keys
            r'ghp_[A-Za-z0-9]{36}',  # GitHub personal access tokens
            r'gho_[A-Za-z0-9]{36}',  # GitHub OAuth tokens
            r'Bearer [A-Za-z0-9._-]+',  # Bearer tokens
            r'password["\']?\s*[:=]\s*["\']?[^"\'\s]+',  # Passwords
            r'token["\']?\s*[:=]\s*["\']?[^"\'\s]+',  # Tokens
        ]
    
    redacted = text
    for pattern in patterns:
        redacted = re.sub(pattern, '[REDACTED]', redacted, flags=re.IGNORECASE)
    
    return redacted


if __name__ == "__main__":
    # Test
    try:
        print("Testing path sanitization...")
        
        # Valid paths
        print(f"✅ {sanitize_path('test.md', base_dir='specs')}")
        print(f"✅ {sanitize_path('specs/core/test.md', base_dir='specs')}")
        
        # Invalid paths
        try:
            sanitize_path('../etc/passwd', base_dir='specs')
            print("❌ Path traversal should have been blocked")
        except ValueError as e:
            print(f"✅ Path traversal blocked: {e}")
        
        # Redaction test
        text = "API key: sk-1234567890abcdef1234567890abcdef password=secret123"
        redacted = redact_secrets(text)
        print(f"✅ Redacted: {redacted}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
