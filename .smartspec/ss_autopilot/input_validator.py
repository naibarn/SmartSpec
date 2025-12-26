"""
Input Validation Module for SmartSpec Autopilot

Provides comprehensive input validation and sanitization:
- File path sanitization
- Path traversal prevention
- Whitelist/blacklist validation
- Input schema validation

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import os
import re
from .error_handler import InvalidInputError, with_error_handling


class PathValidator:
    """Validator for file paths with security checks"""
    
    # Dangerous path patterns
    DANGEROUS_PATTERNS = [
        r'\.\.',           # Parent directory traversal
        r'~',              # Home directory expansion
        r'\$',             # Environment variable expansion
        r'[<>|*?]',        # Wildcards and redirects
        r'[\x00-\x1f]',    # Control characters
        r';',              # Command separator
        r'&',              # Background execution
        r'\|',             # Pipe
        r'`',              # Command substitution
        r'\$\(',           # Command substitution
    ]
    
    # Allowed base directories (whitelist)
    ALLOWED_BASE_DIRS = [
        '.smartspec',
        'specs',
        'workflows',
        'reports',
        'logs',
        'tmp',
        'cache',
    ]
    
    # Forbidden directories (blacklist)
    FORBIDDEN_DIRS = [
        '/etc',
        '/root',
        '/sys',
        '/proc',
        '/dev',
        '/boot',
        '/bin',
        '/sbin',
        '/usr/bin',
        '/usr/sbin',
    ]
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = [
        '.md',
        '.txt',
        '.json',
        '.yaml',
        '.yml',
        '.log',
        '.csv',
        '.html',
        '.css',
        '.js',
    ]
    
    @staticmethod
    def sanitize_path(file_path: str, base_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Sanitize and validate a file path.
        
        Args:
            file_path: Path to sanitize
            base_dir: Optional base directory to restrict to
            
        Returns:
            Dict with 'success' and 'sanitized_path' or 'error'
        """
        try:
            # Check if path is empty
            if not file_path or not file_path.strip():
                raise InvalidInputError(
                    input_name="file_path",
                    input_value=file_path,
                    reason="Path cannot be empty"
                )
            
            # Remove leading/trailing whitespace
            file_path = file_path.strip()
            
            # Check for dangerous patterns
            for pattern in PathValidator.DANGEROUS_PATTERNS:
                if re.search(pattern, file_path):
                    raise InvalidInputError(
                        input_name="file_path",
                        input_value=file_path,
                        reason=f"Path contains dangerous pattern: {pattern}"
                    )
            
            # Convert to Path object
            path = Path(file_path)
            
            # Resolve to absolute path (prevents traversal)
            try:
                resolved_path = path.resolve()
            except Exception as e:
                raise InvalidInputError(
                    input_name="file_path",
                    input_value=file_path,
                    reason=f"Cannot resolve path: {str(e)}"
                )
            
            # Check if path is within base_dir (if specified)
            if base_dir:
                base_path = Path(base_dir).resolve()
                try:
                    resolved_path.relative_to(base_path)
                except ValueError:
                    raise InvalidInputError(
                        input_name="file_path",
                        input_value=file_path,
                        reason=f"Path is outside allowed base directory: {base_dir}"
                    )
            
            # Check against forbidden directories
            path_str = str(resolved_path)
            for forbidden_dir in PathValidator.FORBIDDEN_DIRS:
                if path_str.startswith(forbidden_dir):
                    raise InvalidInputError(
                        input_name="file_path",
                        input_value=file_path,
                        reason=f"Access to {forbidden_dir} is forbidden"
                    )
            
            # Check file extension
            if resolved_path.suffix and resolved_path.suffix not in PathValidator.ALLOWED_EXTENSIONS:
                raise InvalidInputError(
                    input_name="file_path",
                    input_value=file_path,
                    reason=f"File extension {resolved_path.suffix} is not allowed"
                )
            
            return {
                "success": True,
                "sanitized_path": str(resolved_path),
                "original_path": file_path,
                "is_absolute": resolved_path.is_absolute(),
                "extension": resolved_path.suffix
            }
        
        except InvalidInputError as e:
            return e.to_dict()
        
        except Exception as e:
            return {
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": f"Path validation failed: {str(e)}",
                "details": {
                    "file_path": file_path,
                    "exception_type": type(e).__name__
                }
            }
    
    @staticmethod
    def is_safe_path(file_path: str, base_dir: Optional[str] = None) -> bool:
        """
        Quick check if a path is safe.
        
        Args:
            file_path: Path to check
            base_dir: Optional base directory
            
        Returns:
            True if path is safe, False otherwise
        """
        result = PathValidator.sanitize_path(file_path, base_dir)
        return result.get("success", False)
    
    @staticmethod
    def validate_directory_path(dir_path: str) -> Dict[str, Any]:
        """
        Validate a directory path.
        
        Args:
            dir_path: Directory path to validate
            
        Returns:
            Dict with validation result
        """
        try:
            if not dir_path or not dir_path.strip():
                raise InvalidInputError(
                    input_name="dir_path",
                    input_value=dir_path,
                    reason="Directory path cannot be empty"
                )
            
            # Sanitize path
            result = PathValidator.sanitize_path(dir_path)
            if result.get("error"):
                return result
            
            sanitized_path = result["sanitized_path"]
            path = Path(sanitized_path)
            
            # Check if it's a directory (if exists)
            if path.exists() and not path.is_dir():
                raise InvalidInputError(
                    input_name="dir_path",
                    input_value=dir_path,
                    reason="Path exists but is not a directory"
                )
            
            return {
                "success": True,
                "sanitized_path": sanitized_path,
                "exists": path.exists(),
                "is_directory": path.is_dir() if path.exists() else None
            }
        
        except InvalidInputError as e:
            return e.to_dict()
        
        except Exception as e:
            return {
                "error": True,
                "error_code": "VALIDATION_ERROR",
                "message": f"Directory validation failed: {str(e)}",
                "details": {
                    "dir_path": dir_path,
                    "exception_type": type(e).__name__
                }
            }
    
    @staticmethod
    def normalize_path(file_path: str) -> str:
        """
        Normalize a path (resolve .., ., etc).
        
        Args:
            file_path: Path to normalize
            
        Returns:
            Normalized path string
        """
        try:
            return str(Path(file_path).resolve())
        except Exception:
            return file_path


class InputValidator:
    """General input validator with multiple validation types"""
    
    @staticmethod
    @with_error_handling
    def validate_string(
        value: str,
        field_name: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        allowed_values: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Validate a string input.
        
        Args:
            value: String to validate
            field_name: Name of the field
            min_length: Minimum length
            max_length: Maximum length
            pattern: Regex pattern to match
            allowed_values: List of allowed values
            
        Returns:
            Validation result dict
        """
        # Check if empty
        if not value or not value.strip():
            raise InvalidInputError(
                input_name=field_name,
                input_value=value,
                reason="Value cannot be empty"
            )
        
        value = value.strip()
        
        # Check length
        if min_length and len(value) < min_length:
            raise InvalidInputError(
                input_name=field_name,
                input_value=value,
                reason=f"Value must be at least {min_length} characters"
            )
        
        if max_length and len(value) > max_length:
            raise InvalidInputError(
                input_name=field_name,
                input_value=value,
                reason=f"Value must be at most {max_length} characters"
            )
        
        # Check pattern
        if pattern and not re.match(pattern, value):
            raise InvalidInputError(
                input_name=field_name,
                input_value=value,
                reason=f"Value does not match required pattern"
            )
        
        # Check allowed values
        if allowed_values and value not in allowed_values:
            raise InvalidInputError(
                input_name=field_name,
                input_value=value,
                reason=f"Value must be one of: {', '.join(allowed_values)}"
            )
        
        return {
            "success": True,
            "validated_value": value,
            "field_name": field_name
        }
    
    @staticmethod
    @with_error_handling
    def validate_spec_id(spec_id: str) -> Dict[str, Any]:
        """
        Validate a spec ID format.
        
        Args:
            spec_id: Spec ID to validate
            
        Returns:
            Validation result dict
        """
        # Spec ID format: spec-{category}-{number}-{name}
        # Example: spec-core-001-authentication
        pattern = r'^spec-[a-z]+-\d{3}-[a-z0-9_-]+$'
        
        return InputValidator.validate_string(
            value=spec_id,
            field_name="spec_id",
            min_length=10,
            max_length=100,
            pattern=pattern
        )
    
    @staticmethod
    @with_error_handling
    def validate_workflow_name(workflow_name: str) -> Dict[str, Any]:
        """
        Validate a workflow name format.
        
        Args:
            workflow_name: Workflow name to validate
            
        Returns:
            Validation result dict
        """
        # Workflow name format: lowercase with underscores
        # Example: smartspec_generate_spec
        pattern = r'^[a-z][a-z0-9_]*$'
        
        return InputValidator.validate_string(
            value=workflow_name,
            field_name="workflow_name",
            min_length=3,
            max_length=100,
            pattern=pattern
        )
    
    @staticmethod
    @with_error_handling
    def sanitize_user_input(user_input: str) -> Dict[str, Any]:
        """
        Sanitize user input to prevent injection attacks.
        
        Args:
            user_input: User input to sanitize
            
        Returns:
            Sanitized input dict
        """
        if not user_input:
            return {
                "success": True,
                "sanitized_input": "",
                "original_input": user_input
            }
        
        # Remove control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', user_input)
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '&', '"', "'", '`', '$', '|', ';']
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '')
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return {
            "success": True,
            "sanitized_input": sanitized,
            "original_input": user_input,
            "was_modified": sanitized != user_input
        }


# Export all
__all__ = [
    'PathValidator',
    'InputValidator',
]



class SchemaValidator:
    """Validator for JSON schemas and data structures"""
    
    # Schema definitions
    SPEC_METADATA_SCHEMA = {
        "type": "object",
        "required": ["spec_id", "title", "category", "priority"],
        "properties": {
            "spec_id": {
                "type": "string",
                "pattern": r"^spec-[a-z]+-\d{3}-[a-z0-9_-]+$"
            },
            "title": {
                "type": "string",
                "minLength": 3,
                "maxLength": 200
            },
            "category": {
                "type": "string",
                "enum": ["core", "feature", "integration", "security", "performance"]
            },
            "priority": {
                "type": "string",
                "enum": ["high", "medium", "low"]
            },
            "status": {
                "type": "string",
                "enum": ["draft", "review", "approved", "implemented"]
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
    
    WORKFLOW_CONFIG_SCHEMA = {
        "type": "object",
        "required": ["name", "version", "steps"],
        "properties": {
            "name": {
                "type": "string",
                "pattern": r"^[a-z][a-z0-9_]*$"
            },
            "version": {
                "type": "string",
                "pattern": r"^\d+\.\d+\.\d+$"
            },
            "description": {
                "type": "string",
                "maxLength": 500
            },
            "steps": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["id", "type"],
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "string"},
                        "config": {"type": "object"}
                    }
                }
            },
            "timeout": {
                "type": "integer",
                "minimum": 1,
                "maximum": 3600
            }
        }
    }
    
    @staticmethod
    @with_error_handling
    def validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against a schema.
        
        Args:
            data: Data to validate
            schema: Schema definition
            
        Returns:
            Validation result dict
        """
        errors = []
        
        # Validate type
        if "type" in schema:
            expected_type = schema["type"]
            actual_type = SchemaValidator._get_type(data)
            
            if actual_type != expected_type:
                errors.append(f"Expected type {expected_type}, got {actual_type}")
                return {
                    "success": False,
                    "errors": errors
                }
        
        # For primitive types (string, number, integer), validate directly
        if schema.get("type") in ["string", "integer", "number", "boolean"]:
            result = SchemaValidator._validate_value(data, schema, "value")
            if not result["valid"]:
                return {
                    "success": False,
                    "errors": result["errors"]
                }
        
        # Validate object properties
        elif schema.get("type") == "object":
            # Check required fields
            required = schema.get("required", [])
            for field in required:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate properties
            properties = schema.get("properties", {})
            for key, value in data.items():
                if key in properties:
                    prop_schema = properties[key]
                    result = SchemaValidator._validate_value(value, prop_schema, key)
                    if not result["valid"]:
                        errors.extend(result["errors"])
        
        # Validate array items
        elif schema.get("type") == "array":
            if not isinstance(data, list):
                errors.append("Expected array")
            else:
                # Check minItems
                min_items = schema.get("minItems")
                if min_items and len(data) < min_items:
                    errors.append(f"Array must have at least {min_items} items")
                
                # Check maxItems
                max_items = schema.get("maxItems")
                if max_items and len(data) > max_items:
                    errors.append(f"Array must have at most {max_items} items")
                
                # Validate items
                items_schema = schema.get("items")
                if items_schema:
                    for i, item in enumerate(data):
                        result = SchemaValidator._validate_value(item, items_schema, f"[{i}]")
                        if not result["valid"]:
                            errors.extend(result["errors"])
        
        if errors:
            return {
                "success": False,
                "errors": errors
            }
        
        return {
            "success": True,
            "validated_data": data
        }
    
    @staticmethod
    def _validate_value(value: Any, schema: Dict[str, Any], field_name: str) -> Dict[str, Any]:
        """Validate a single value against schema"""
        errors = []
        
        # Type check
        if "type" in schema:
            expected_type = schema["type"]
            actual_type = SchemaValidator._get_type(value)
            
            if actual_type != expected_type:
                errors.append(f"{field_name}: Expected {expected_type}, got {actual_type}")
                return {"valid": False, "errors": errors}
        
        # String validations
        if isinstance(value, str):
            # minLength
            if "minLength" in schema and len(value) < schema["minLength"]:
                errors.append(f"{field_name}: Must be at least {schema['minLength']} characters")
            
            # maxLength
            if "maxLength" in schema and len(value) > schema["maxLength"]:
                errors.append(f"{field_name}: Must be at most {schema['maxLength']} characters")
            
            # pattern
            if "pattern" in schema and not re.match(schema["pattern"], value):
                errors.append(f"{field_name}: Does not match required pattern")
            
            # enum
            if "enum" in schema and value not in schema["enum"]:
                errors.append(f"{field_name}: Must be one of {schema['enum']}")
        
        # Number validations
        if isinstance(value, (int, float)):
            # minimum
            if "minimum" in schema and value < schema["minimum"]:
                errors.append(f"{field_name}: Must be at least {schema['minimum']}")
            
            # maximum
            if "maximum" in schema and value > schema["maximum"]:
                errors.append(f"{field_name}: Must be at most {schema['maximum']}")
        
        # Array validations
        if isinstance(value, list):
            # minItems
            if "minItems" in schema and len(value) < schema["minItems"]:
                errors.append(f"{field_name}: Must have at least {schema['minItems']} items")
            
            # maxItems
            if "maxItems" in schema and len(value) > schema["maxItems"]:
                errors.append(f"{field_name}: Must have at most {schema['maxItems']} items")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    def _get_type(value: Any) -> str:
        """Get JSON schema type of a value"""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif value is None:
            return "null"
        else:
            return "unknown"
    
    @staticmethod
    @with_error_handling
    def validate_spec_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate spec metadata against schema.
        
        Args:
            metadata: Spec metadata dict
            
        Returns:
            Validation result
        """
        return SchemaValidator.validate_schema(
            metadata,
            SchemaValidator.SPEC_METADATA_SCHEMA
        )
    
    @staticmethod
    @with_error_handling
    def validate_workflow_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate workflow config against schema.
        
        Args:
            config: Workflow config dict
            
        Returns:
            Validation result
        """
        return SchemaValidator.validate_schema(
            config,
            SchemaValidator.WORKFLOW_CONFIG_SCHEMA
        )


# Update exports
__all__ = [
    'PathValidator',
    'InputValidator',
    'SchemaValidator',
]
