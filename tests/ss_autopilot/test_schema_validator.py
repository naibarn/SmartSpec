"""
Unit tests for SchemaValidator

Tests:
- validate_schema() with various schemas
- validate_spec_metadata()
- validate_workflow_config()
- Type validation
- String validation (length, pattern, enum)
- Number validation (min, max)
- Array validation (minItems, maxItems)
"""

import pytest
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.input_validator import SchemaValidator


# ============================================================================
# Test validate_schema() - Basic Types
# ============================================================================

class TestSchemaValidatorBasicTypes:
    """Test basic type validation"""
    
    def test_validate_string_type(self):
        """Test validating string type"""
        schema = {"type": "string"}
        result = SchemaValidator.validate_schema("test", schema)
        assert result.get("success") is True
    
    def test_validate_integer_type(self):
        """Test validating integer type"""
        schema = {"type": "integer"}
        result = SchemaValidator.validate_schema(42, schema)
        assert result.get("success") is True
    
    def test_validate_wrong_type(self):
        """Test validation fails for wrong type"""
        schema = {"type": "string"}
        result = SchemaValidator.validate_schema(42, schema)
        assert result.get("success") is False
        assert "errors" in result


# ============================================================================
# Test validate_schema() - String Validations
# ============================================================================

class TestSchemaValidatorString:
    """Test string validation"""
    
    def test_validate_string_min_length(self):
        """Test string minimum length"""
        schema = {"type": "string", "minLength": 5}
        
        # Valid
        result = SchemaValidator.validate_schema("hello", schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema("hi", schema)
        assert result.get("success") is False
    
    def test_validate_string_max_length(self):
        """Test string maximum length"""
        schema = {"type": "string", "maxLength": 10}
        
        # Valid
        result = SchemaValidator.validate_schema("hello", schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema("this is too long", schema)
        assert result.get("success") is False
    
    def test_validate_string_pattern(self):
        """Test string pattern validation"""
        schema = {"type": "string", "pattern": r"^[a-z]+$"}
        
        # Valid
        result = SchemaValidator.validate_schema("hello", schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema("Hello123", schema)
        assert result.get("success") is False
    
    def test_validate_string_enum(self):
        """Test string enum validation"""
        schema = {"type": "string", "enum": ["red", "green", "blue"]}
        
        # Valid
        result = SchemaValidator.validate_schema("red", schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema("yellow", schema)
        assert result.get("success") is False


# ============================================================================
# Test validate_schema() - Number Validations
# ============================================================================

class TestSchemaValidatorNumber:
    """Test number validation"""
    
    def test_validate_number_minimum(self):
        """Test number minimum value"""
        schema = {"type": "integer", "minimum": 10}
        
        # Valid
        result = SchemaValidator.validate_schema(15, schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema(5, schema)
        assert result.get("success") is False
    
    def test_validate_number_maximum(self):
        """Test number maximum value"""
        schema = {"type": "integer", "maximum": 100}
        
        # Valid
        result = SchemaValidator.validate_schema(50, schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema(150, schema)
        assert result.get("success") is False


# ============================================================================
# Test validate_schema() - Array Validations
# ============================================================================

class TestSchemaValidatorArray:
    """Test array validation"""
    
    def test_validate_array_type(self):
        """Test array type validation"""
        schema = {"type": "array"}
        result = SchemaValidator.validate_schema([1, 2, 3], schema)
        assert result.get("success") is True
    
    def test_validate_array_min_items(self):
        """Test array minimum items"""
        schema = {"type": "array", "minItems": 2}
        
        # Valid
        result = SchemaValidator.validate_schema([1, 2], schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema([1], schema)
        assert result.get("success") is False
    
    def test_validate_array_max_items(self):
        """Test array maximum items"""
        schema = {"type": "array", "maxItems": 3}
        
        # Valid
        result = SchemaValidator.validate_schema([1, 2], schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema([1, 2, 3, 4], schema)
        assert result.get("success") is False
    
    def test_validate_array_items_schema(self):
        """Test array items schema validation"""
        schema = {
            "type": "array",
            "items": {"type": "string"}
        }
        
        # Valid
        result = SchemaValidator.validate_schema(["a", "b", "c"], schema)
        assert result.get("success") is True
        
        # Invalid
        result = SchemaValidator.validate_schema(["a", 2, "c"], schema)
        assert result.get("success") is False


# ============================================================================
# Test validate_schema() - Object Validations
# ============================================================================

class TestSchemaValidatorObject:
    """Test object validation"""
    
    def test_validate_object_required_fields(self):
        """Test object required fields"""
        schema = {
            "type": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"}
            }
        }
        
        # Valid
        result = SchemaValidator.validate_schema(
            {"name": "John", "age": 30},
            schema
        )
        assert result.get("success") is True
        
        # Invalid - missing field
        result = SchemaValidator.validate_schema(
            {"name": "John"},
            schema
        )
        assert result.get("success") is False
    
    def test_validate_object_properties(self):
        """Test object properties validation"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3},
                "age": {"type": "integer", "minimum": 0}
            }
        }
        
        # Valid
        result = SchemaValidator.validate_schema(
            {"name": "John", "age": 30},
            schema
        )
        assert result.get("success") is True
        
        # Invalid - name too short
        result = SchemaValidator.validate_schema(
            {"name": "Jo", "age": 30},
            schema
        )
        assert result.get("success") is False


# ============================================================================
# Test validate_spec_metadata()
# ============================================================================

class TestSchemaValidatorSpecMetadata:
    """Test spec metadata validation"""
    
    def test_validate_valid_spec_metadata(self):
        """Test validating valid spec metadata"""
        metadata = {
            "spec_id": "spec-core-001-authentication",
            "title": "User Authentication System",
            "category": "core",
            "priority": "high",
            "status": "approved",
            "tags": ["auth", "security"]
        }
        
        result = SchemaValidator.validate_spec_metadata(metadata)
        assert result.get("success") is True
    
    def test_validate_spec_metadata_missing_required(self):
        """Test spec metadata with missing required field"""
        metadata = {
            "spec_id": "spec-core-001-authentication",
            "title": "User Authentication System",
            "category": "core"
            # Missing priority
        }
        
        result = SchemaValidator.validate_spec_metadata(metadata)
        assert result.get("success") is False
    
    def test_validate_spec_metadata_invalid_spec_id(self):
        """Test spec metadata with invalid spec_id format"""
        metadata = {
            "spec_id": "invalid-spec-id",
            "title": "Test",
            "category": "core",
            "priority": "high"
        }
        
        result = SchemaValidator.validate_spec_metadata(metadata)
        assert result.get("success") is False
    
    def test_validate_spec_metadata_invalid_category(self):
        """Test spec metadata with invalid category"""
        metadata = {
            "spec_id": "spec-core-001-test",
            "title": "Test",
            "category": "invalid",
            "priority": "high"
        }
        
        result = SchemaValidator.validate_spec_metadata(metadata)
        assert result.get("success") is False
    
    def test_validate_spec_metadata_invalid_priority(self):
        """Test spec metadata with invalid priority"""
        metadata = {
            "spec_id": "spec-core-001-test",
            "title": "Test",
            "category": "core",
            "priority": "urgent"  # Not in enum
        }
        
        result = SchemaValidator.validate_spec_metadata(metadata)
        assert result.get("success") is False


# ============================================================================
# Test validate_workflow_config()
# ============================================================================

class TestSchemaValidatorWorkflowConfig:
    """Test workflow config validation"""
    
    def test_validate_valid_workflow_config(self):
        """Test validating valid workflow config"""
        config = {
            "name": "smartspec_generate_spec",
            "version": "1.0.0",
            "description": "Generate spec from requirements",
            "steps": [
                {
                    "id": "parse_input",
                    "type": "parser",
                    "config": {}
                },
                {
                    "id": "generate_spec",
                    "type": "generator",
                    "config": {}
                }
            ],
            "timeout": 300
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is True
    
    def test_validate_workflow_config_missing_required(self):
        """Test workflow config with missing required field"""
        config = {
            "name": "test_workflow",
            "version": "1.0.0"
            # Missing steps
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is False
    
    def test_validate_workflow_config_invalid_name(self):
        """Test workflow config with invalid name format"""
        config = {
            "name": "Invalid-Workflow-Name",
            "version": "1.0.0",
            "steps": [{"id": "step1", "type": "test"}]
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is False
    
    def test_validate_workflow_config_invalid_version(self):
        """Test workflow config with invalid version format"""
        config = {
            "name": "test_workflow",
            "version": "1.0",  # Should be x.y.z
            "steps": [{"id": "step1", "type": "test"}]
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is False
    
    def test_validate_workflow_config_empty_steps(self):
        """Test workflow config with empty steps array"""
        config = {
            "name": "test_workflow",
            "version": "1.0.0",
            "steps": []
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is False
    
    def test_validate_workflow_config_invalid_timeout(self):
        """Test workflow config with invalid timeout"""
        config = {
            "name": "test_workflow",
            "version": "1.0.0",
            "steps": [{"id": "step1", "type": "test"}],
            "timeout": 5000  # Exceeds maximum
        }
        
        result = SchemaValidator.validate_workflow_config(config)
        assert result.get("success") is False


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
