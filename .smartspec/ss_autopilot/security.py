"""
Security utilities for SmartSpec Autopilot.

This module provides input sanitization and validation functions to prevent
security vulnerabilities such as command injection, path traversal, and
injection attacks.
"""

import re
import shlex
from pathlib import Path
from typing import Union


class SecurityError(Exception):
    """Base exception for security-related errors."""
    pass


class InvalidInputError(SecurityError):
    """Raised when input validation fails."""
    pass


class PathTraversalError(SecurityError):
    """Raised when path traversal attack is detected."""
    pass


def sanitize_spec_id(spec_id: str) -> str:
    """
    Sanitize spec ID to prevent injection attacks.
    
    Only allows alphanumeric characters, hyphens, and underscores.
    
    Args:
        spec_id: The spec ID to sanitize
        
    Returns:
        The sanitized spec ID
        
    Raises:
        InvalidInputError: If spec ID contains invalid characters
        
    Examples:
        >>> sanitize_spec_id("spec-core-001")
        'spec-core-001'
        >>> sanitize_spec_id("spec_core_001")
        'spec_core_001'
        >>> sanitize_spec_id("spec-001; rm -rf /")
        Traceback (most recent call last):
        ...
        InvalidInputError: Invalid spec ID: spec-001; rm -rf /
    """
    if not spec_id:
        raise InvalidInputError("Spec ID cannot be empty")
    
    if len(spec_id) > 100:
        raise InvalidInputError(f"Spec ID too long: {len(spec_id)} > 100")
    
    # Only allow alphanumeric, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', spec_id):
        raise InvalidInputError(
            f"Invalid spec ID: {spec_id}. "
            "Only alphanumeric characters, hyphens, and underscores are allowed."
        )
    
    return spec_id


def sanitize_workflow_name(workflow: str) -> str:
    """
    Sanitize workflow name to prevent injection attacks.
    
    Only allows alphanumeric characters and underscores.
    
    Args:
        workflow: The workflow name to sanitize
        
    Returns:
        The sanitized workflow name
        
    Raises:
        InvalidInputError: If workflow name contains invalid characters
    """
    if not workflow:
        raise InvalidInputError("Workflow name cannot be empty")
    
    if len(workflow) > 100:
        raise InvalidInputError(f"Workflow name too long: {len(workflow)} > 100")
    
    # Only allow alphanumeric and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', workflow):
        raise InvalidInputError(
            f"Invalid workflow name: {workflow}. "
            "Only alphanumeric characters and underscores are allowed."
        )
    
    return workflow


def sanitize_platform(platform: str) -> str:
    """
    Sanitize platform name.
    
    Only allows known platforms: kilo, antigravity, claude.
    
    Args:
        platform: The platform name to sanitize
        
    Returns:
        The sanitized platform name
        
    Raises:
        InvalidInputError: If platform is not recognized
    """
    if not platform:
        raise InvalidInputError("Platform cannot be empty")
    
    platform = platform.lower().strip()
    
    allowed_platforms = ['kilo', 'antigravity', 'claude']
    if platform not in allowed_platforms:
        raise InvalidInputError(
            f"Invalid platform: {platform}. "
            f"Allowed platforms: {', '.join(allowed_platforms)}"
        )
    
    return platform


def sanitize_path(path: Union[str, Path], base_dir: Union[str, Path]) -> Path:
    """
    Sanitize file path to prevent path traversal attacks.
    
    Ensures that the resolved path is within the base directory.
    
    Args:
        path: The file path to sanitize
        base_dir: The base directory that path must be within
        
    Returns:
        The sanitized absolute path
        
    Raises:
        PathTraversalError: If path is outside base directory
        
    Examples:
        >>> sanitize_path("specs/spec-001.md", "/home/user/project")
        PosixPath('/home/user/project/specs/spec-001.md')
        >>> sanitize_path("../../etc/passwd", "/home/user/project")
        Traceback (most recent call last):
        ...
        PathTraversalError: Path outside base directory
    """
    try:
        # Convert to Path objects and resolve
        path = Path(path).resolve()
        base = Path(base_dir).resolve()
        
        # Check if path is within base directory
        # Use relative_to() which raises ValueError if not relative
        path.relative_to(base)
        
        return path
        
    except ValueError:
        raise PathTraversalError(
            f"Path outside base directory: {path} not in {base}"
        )


def sanitize_query(query: str, max_length: int = 1000) -> str:
    """
    Sanitize user query to prevent injection attacks.
    
    Removes control characters and limits length.
    
    Args:
        query: The user query to sanitize
        max_length: Maximum allowed length (default: 1000)
        
    Returns:
        The sanitized query
        
    Raises:
        InvalidInputError: If query is too long
        
    Examples:
        >>> sanitize_query("งานถึงไหนแล้ว?")
        'งานถึงไหนแล้ว?'
        >>> sanitize_query("a" * 2000)
        Traceback (most recent call last):
        ...
        InvalidInputError: Query too long: 2000 > 1000
    """
    if not query:
        raise InvalidInputError("Query cannot be empty")
    
    if len(query) > max_length:
        raise InvalidInputError(
            f"Query too long: {len(query)} > {max_length}"
        )
    
    # Remove control characters (except newlines and tabs)
    query = ''.join(
        c for c in query 
        if c.isprintable() or c in ('\n', '\t', ' ')
    )
    
    return query.strip()


def quote_for_shell(value: str) -> str:
    """
    Quote a string for safe use in shell commands.
    
    Uses shlex.quote() to properly escape special characters.
    
    Args:
        value: The string to quote
        
    Returns:
        The quoted string safe for shell use
        
    Examples:
        >>> quote_for_shell("spec-001")
        'spec-001'
        >>> quote_for_shell("spec-001; rm -rf /")
        "'spec-001; rm -rf /'"
    """
    return shlex.quote(value)


def validate_spec_path(spec_path: str, project_root: str) -> Path:
    """
    Validate and sanitize a spec file path.
    
    Ensures the path:
    - Is within project root
    - Points to a .md file
    - Exists (optionally)
    
    Args:
        spec_path: The spec file path to validate
        project_root: The project root directory
        
    Returns:
        The validated absolute path
        
    Raises:
        InvalidInputError: If path is invalid
        PathTraversalError: If path is outside project root
    """
    # Sanitize path
    path = sanitize_path(spec_path, project_root)
    
    # Check file extension
    if path.suffix != '.md':
        raise InvalidInputError(
            f"Invalid spec file: {path}. Must be a .md file."
        )
    
    return path


def validate_tasks_path(tasks_path: str, project_root: str) -> Path:
    """
    Validate and sanitize a tasks file path.
    
    Similar to validate_spec_path but for tasks.md files.
    
    Args:
        tasks_path: The tasks file path to validate
        project_root: The project root directory
        
    Returns:
        The validated absolute path
        
    Raises:
        InvalidInputError: If path is invalid
        PathTraversalError: If path is outside project root
    """
    # Sanitize path
    path = sanitize_path(tasks_path, project_root)
    
    # Check file extension
    if path.suffix != '.md':
        raise InvalidInputError(
            f"Invalid tasks file: {path}. Must be a .md file."
        )
    
    # Check filename
    if path.name != 'tasks.md':
        raise InvalidInputError(
            f"Invalid tasks file: {path}. Must be named 'tasks.md'."
        )
    
    return path


def validate_report_path(report_path: str, project_root: str) -> Path:
    """
    Validate and sanitize a report output path.
    
    Ensures the path:
    - Is within project root
    - Is within .spec/reports/ directory
    
    Args:
        report_path: The report output path to validate
        project_root: The project root directory
        
    Returns:
        The validated absolute path
        
    Raises:
        InvalidInputError: If path is invalid
        PathTraversalError: If path is outside allowed directory
    """
    # Sanitize path
    path = sanitize_path(report_path, project_root)
    
    # Ensure it's within .spec/reports/
    spec_reports = Path(project_root) / '.spec' / 'reports'
    try:
        path.relative_to(spec_reports)
    except ValueError:
        raise PathTraversalError(
            f"Report path must be within .spec/reports/: {path}"
        )
    
    return path


# Convenience function for common validation
def validate_workflow_params(
    spec_id: str,
    workflow: str,
    platform: str,
    project_root: str = "."
) -> dict:
    """
    Validate all common workflow parameters at once.
    
    Args:
        spec_id: The spec ID
        workflow: The workflow name
        platform: The platform name
        project_root: The project root directory
        
    Returns:
        Dictionary with sanitized values
        
    Raises:
        InvalidInputError: If any parameter is invalid
    """
    return {
        'spec_id': sanitize_spec_id(spec_id),
        'workflow': sanitize_workflow_name(workflow),
        'platform': sanitize_platform(platform),
        'project_root': Path(project_root).resolve()
    }


if __name__ == '__main__':
    # Run doctests
    import doctest
    doctest.testmod()
