"""
Pytest configuration and shared fixtures for SmartSpec Autopilot tests.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def temp_file():
    """Create a temporary file for tests"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_text_content():
    """Sample text content for testing"""
    return "Hello, World!\nThis is a test file.\n"


@pytest.fixture
def sample_json_content():
    """Sample JSON content for testing"""
    return '{"key": "value", "number": 42, "array": [1, 2, 3]}'


@pytest.fixture
def sample_unicode_content():
    """Sample Unicode content for testing"""
    return "สวัสดี 你好 مرحبا Hello"


@pytest.fixture
def mock_spec_id():
    """Mock spec ID for testing"""
    return "spec-core-001-authentication"


@pytest.fixture
def mock_workflow_name():
    """Mock workflow name for testing"""
    return "smartspec_generate_spec"
