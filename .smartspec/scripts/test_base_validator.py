#!/usr/bin/env python3
"""
Unit Tests for BaseValidator

Tests security features, validation logic, and auto-fix functionality.
"""

import unittest
import tempfile
import os
from pathlib import Path
from base_validator import BaseValidator

class TestBaseValidator(unittest.TestCase):
    """Test cases for BaseValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = Path(self.test_dir) / "test.md"
        
    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    # Security Tests
    
    def test_file_not_found(self):
        """Test that non-existent file raises FileNotFoundError"""
        with self.assertRaises(FileNotFoundError):
            BaseValidator("/nonexistent/file.md")
    
    def test_invalid_file_type(self):
        """Test that invalid file type raises ValueError"""
        invalid_file = Path(self.test_dir) / "test.txt"
        invalid_file.write_text("test")
        
        with self.assertRaises(ValueError) as cm:
            BaseValidator(str(invalid_file))
        
        self.assertIn("Invalid file type", str(cm.exception))
    
    def test_directory_not_file(self):
        """Test that directory raises ValueError"""
        with self.assertRaises(ValueError) as cm:
            BaseValidator(self.test_dir)
        
        self.assertIn("Not a regular file", str(cm.exception))
    
    def test_file_outside_repo(self):
        """Test that file outside repo raises ValueError"""
        self.test_file.write_text("# Test\n\n## Section\n\nContent")
        
        with self.assertRaises(ValueError) as cm:
            BaseValidator(str(self.test_file), repo_root="/different/path")
        
        self.assertIn("outside repository", str(cm.exception))
    
    def test_file_size_limit(self):
        """Test that large file is rejected"""
        # Create file larger than 10 MB
        large_content = "x" * (11 * 1024 * 1024)  # 11 MB
        self.test_file.write_text(large_content)
        
        validator = BaseValidator(str(self.test_file))
        success = validator.load_file()
        
        self.assertFalse(success)
        self.assertTrue(any('too large' in issue['message'] 
                          for issue in validator.issues))
    
    def test_symlink_resolution(self):
        """Test that symlinks are resolved"""
        self.test_file.write_text("# Test\n\n## Section\n\nContent")
        symlink = Path(self.test_dir) / "link.md"
        symlink.symlink_to(self.test_file)
        
        validator = BaseValidator(str(symlink))
        self.assertEqual(validator.file_path, self.test_file.resolve())
    
    # Parsing Tests
    
    def test_parse_markdown(self):
        """Test markdown parsing"""
        content = """# Title

## Section One

Content for section one.

## Section Two

Content for section two.
"""
        self.test_file.write_text(content)
        
        validator = BaseValidator(str(self.test_file))
        validator.load_file()
        
        self.assertIn('section_one', validator.data)
        self.assertIn('section_two', validator.data)
        self.assertEqual(validator.data['section_one'], 'Content for section one.')
    
    def test_parse_json(self):
        """Test JSON parsing"""
        json_file = Path(self.test_dir) / "test.json"
        json_file.write_text('{"section": "content"}')
        
        validator = BaseValidator(str(json_file))
        validator.load_file()
        
        self.assertEqual(validator.data['section'], 'content')
    
    def test_invalid_json(self):
        """Test invalid JSON handling"""
        json_file = Path(self.test_dir) / "test.json"
        json_file.write_text('{invalid json}')
        
        validator = BaseValidator(str(json_file))
        success = validator.load_file()
        
        self.assertFalse(success)
        self.assertTrue(any('Invalid JSON' in issue['message'] 
                          for issue in validator.issues))
    
    # Validation Tests
    
    def test_validate_structure_missing_sections(self):
        """Test structure validation with missing sections"""
        content = "# Test\n\n## Some Section\n\nContent"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['required_section']
        
        validator = TestValidator(str(self.test_file))
        validator.load_file()
        validator.validate_structure()
        
        errors = [i for i in validator.issues if i['type'] == 'error']
        self.assertEqual(len(errors), 1)
        self.assertIn('required_section', errors[0]['message'])
    
    def test_validate_structure_empty_sections(self):
        """Test structure validation with empty sections"""
        content = "# Test\n\n## Required Section\n\n"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['required_section']
        
        validator = TestValidator(str(self.test_file))
        validator.load_file()
        validator.validate_structure()
        
        warnings = [i for i in validator.issues if i['type'] == 'warning']
        self.assertEqual(len(warnings), 1)
        self.assertIn('empty', warnings[0]['message'])
    
    def test_validate_naming_kebab_case(self):
        """Test naming validation for kebab-case"""
        content = """# Test

## Section

File: `my-file.py`
File: `MyFile.py`
"""
        self.test_file.write_text(content)
        
        validator = BaseValidator(str(self.test_file))
        validator.load_file()
        validator.validate_naming()
        
        warnings = [i for i in validator.issues if i['type'] == 'warning']
        self.assertEqual(len(warnings), 1)
        self.assertIn('MyFile.py', warnings[0]['message'])
    
    def test_is_kebab_case(self):
        """Test kebab-case validation"""
        validator = BaseValidator.__new__(BaseValidator)
        
        self.assertTrue(validator._is_kebab_case('my-file'))
        self.assertTrue(validator._is_kebab_case('my-file-name'))
        self.assertTrue(validator._is_kebab_case('file123'))
        self.assertFalse(validator._is_kebab_case('MyFile'))
        self.assertFalse(validator._is_kebab_case('my_file'))
        self.assertFalse(validator._is_kebab_case('my file'))
    
    # Auto-fix Tests
    
    def test_auto_fix_add_section(self):
        """Test auto-fix adds missing sections"""
        content = "# Test\n\n## Existing\n\nContent"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['missing_section']
        
        validator = TestValidator(str(self.test_file))
        validator.load_file()
        validator.validate_structure()
        validator.auto_fix()
        
        self.assertIn('missing_section', validator.data)
        self.assertIn('TODO', validator.data['missing_section'])
        self.assertEqual(len(validator.fixes_applied), 1)
    
    def test_auto_fix_add_placeholder(self):
        """Test auto-fix adds placeholder for empty sections"""
        content = "# Test\n\n## Empty Section\n\n"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['empty_section']
        
        validator = TestValidator(str(self.test_file))
        validator.load_file()
        validator.validate_structure()
        validator.auto_fix()
        
        self.assertIn('TODO', validator.data['empty_section'])
        self.assertEqual(len(validator.fixes_applied), 1)
    
    def test_save_and_load_markdown(self):
        """Test saving and loading markdown"""
        content = "# Test\n\n## Section\n\nContent"
        self.test_file.write_text(content)
        
        validator = BaseValidator(str(self.test_file))
        validator.load_file()
        validator.data['new_section'] = 'New content'
        validator.save_file()
        
        # Load again and verify
        validator2 = BaseValidator(str(self.test_file))
        validator2.load_file()
        self.assertIn('new_section', validator2.data)
    
    # Report Tests
    
    def test_generate_report(self):
        """Test report generation"""
        content = "# Test\n\n## Section\n\nContent"
        self.test_file.write_text(content)
        
        validator = BaseValidator(str(self.test_file))
        validator.load_file()
        validator.issues.append({
            'type': 'error',
            'message': 'Test error'
        })
        validator.issues.append({
            'type': 'warning',
            'message': 'Test warning'
        })
        validator.fixes_applied.append('Test fix')
        
        report = validator.generate_report()
        
        self.assertIn('Validation Report', report)
        self.assertIn('**Errors:** 1', report)
        self.assertIn('**Warnings:** 1', report)
        self.assertIn('Test error', report)
        self.assertIn('Test warning', report)
        self.assertIn('Test fix', report)
    
    # Integration Tests
    
    def test_full_validation_workflow(self):
        """Test complete validation workflow"""
        content = "# Test\n\n## Existing\n\nContent"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['required']
            RECOMMENDED_SECTIONS = ['recommended']
        
        validator = TestValidator(str(self.test_file))
        success, report = validator.validate(apply_fixes=True)
        
        self.assertFalse(success)  # Has errors
        self.assertIn('required', validator.data)  # Fixed
        self.assertIn('recommended', validator.data)  # Fixed
        self.assertEqual(len(validator.fixes_applied), 2)
    
    def test_validation_without_fixes(self):
        """Test validation without applying fixes"""
        content = "# Test\n\n## Existing\n\nContent"
        self.test_file.write_text(content)
        
        class TestValidator(BaseValidator):
            REQUIRED_SECTIONS = ['required']
        
        validator = TestValidator(str(self.test_file))
        success, report = validator.validate(apply_fixes=False)
        
        self.assertFalse(success)
        self.assertNotIn('required', validator.data)  # Not fixed
        self.assertEqual(len(validator.fixes_applied), 0)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
