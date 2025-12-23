#!/usr/bin/env python3
"""
SmartSpec Golden Test Validator
Validates A2UI JSON against golden test cases
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class GoldenTestValidator:
    """Validates A2UI JSON against golden tests"""
    
    def __init__(self, theme_file: str = ".spec/theme.json"):
        self.theme_file = Path(theme_file)
        self.theme: Dict[str, Any] = {}
        self.test_results: List[Dict[str, Any]] = []
        
    def load_theme(self) -> None:
        """Load theme for token validation"""
        if self.theme_file.exists():
            with open(self.theme_file, 'r', encoding='utf-8') as f:
                self.theme = json.load(f)
    
    def load_golden_tests(self, test_dir: str = ".spec/golden_tests") -> List[Dict[str, Any]]:
        """Load all golden test cases"""
        test_path = Path(test_dir)
        tests = []
        
        if not test_path.exists():
            raise FileNotFoundError(f"Golden tests directory not found: {test_dir}")
        
        for test_file in sorted(test_path.glob("*.json")):
            if test_file.name == "README.md":
                continue
            
            with open(test_file, 'r', encoding='utf-8') as f:
                test = json.load(f)
                test['_file'] = str(test_file)
                tests.append(test)
        
        return tests
    
    def filter_tests(self, tests: List[Dict[str, Any]], test_id: str = None, 
                    category: str = None) -> List[Dict[str, Any]]:
        """Filter tests by ID or category"""
        filtered = tests
        
        if test_id:
            filtered = [t for t in filtered if t.get('test_id') == test_id]
        
        if category:
            filtered = [t for t in filtered if t.get('category') == category]
        
        return filtered
    
    def run_tests(self, tests: List[Dict[str, Any]], fail_fast: bool = False, 
                 verbose: bool = False) -> List[Dict[str, Any]]:
        """Run all tests"""
        self.test_results = []
        
        for test in tests:
            result = self.run_single_test(test, verbose)
            self.test_results.append(result)
            
            if fail_fast and result['status'] == 'FAIL':
                break
        
        return self.test_results
    
    def run_single_test(self, test: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """Run a single test"""
        test_id = test.get('test_id', 'unknown')
        expected_valid = test.get('expected_valid', True)
        
        result = {
            'test_id': test_id,
            'name': test.get('name', ''),
            'category': test.get('category', ''),
            'status': 'PASS',
            'errors': [],
            'warnings': []
        }
        
        # Get expected output
        expected_output = test.get('expected_output', {})
        
        # Run validation rules
        validation_rules = test.get('validation_rules', [])
        
        for rule in validation_rules:
            rule_name = rule.get('rule')
            should_fail = rule.get('should_fail', False)
            
            is_valid, error_msg = self.validate_rule(rule_name, expected_output, test)
            
            if should_fail:
                # This rule should fail
                if is_valid:
                    result['errors'].append(f"Rule '{rule_name}' should have failed but passed")
                    result['status'] = 'FAIL'
            else:
                # This rule should pass
                if not is_valid:
                    if expected_valid:
                        result['errors'].append(f"Rule '{rule_name}': {error_msg}")
                        result['status'] = 'FAIL'
                    else:
                        # Expected to fail
                        result['warnings'].append(f"Rule '{rule_name}': {error_msg} (expected)")
        
        # Check expected errors for invalid tests
        if not expected_valid:
            expected_errors = test.get('expected_errors', [])
            if len(result['errors']) == 0 and len(expected_errors) > 0:
                result['warnings'].append("Test expected to fail but no errors were found")
        
        # Set final status
        if result['status'] == 'PASS' and len(result['warnings']) > 0:
            result['status'] = 'WARN'
        
        if verbose:
            self._print_test_result(result)
        
        return result
    
    def validate_rule(self, rule_name: str, output: Dict[str, Any], 
                     test: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate a specific rule"""
        
        if rule_name == "has_version":
            if "version" not in output:
                return False, "Missing 'version' field"
            return True, ""
        
        elif rule_name == "has_type":
            if "type" not in output:
                return False, "Missing 'type' field"
            return True, ""
        
        elif rule_name == "has_component":
            if "component" not in output:
                return False, "Missing 'component' object"
            return True, ""
        
        elif rule_name == "has_accessibility":
            component = output.get("component", {})
            if "accessibility" not in component:
                return False, "Missing 'accessibility' object in component"
            return True, ""
        
        elif rule_name == "has_theme_references":
            has_refs = self._has_theme_references(output)
            if not has_refs:
                return False, "No theme token references found"
            return True, ""
        
        elif rule_name == "valid_theme_tokens":
            invalid_tokens = self._find_invalid_theme_tokens(output)
            if invalid_tokens:
                return False, f"Invalid theme tokens: {', '.join(invalid_tokens)}"
            return True, ""
        
        elif rule_name == "has_image_alt":
            missing_alt = self._find_missing_alt_text(output)
            if missing_alt:
                return False, f"Images missing alt text: {', '.join(missing_alt)}"
            return True, ""
        
        elif rule_name == "has_form_structure":
            component = output.get("component", {})
            properties = component.get("properties", {})
            if "fields" not in properties:
                return False, "Form missing 'fields' array"
            return True, ""
        
        elif rule_name == "has_validation":
            component = output.get("component", {})
            properties = component.get("properties", {})
            fields = properties.get("fields", [])
            
            for field in fields:
                if "validation" not in field.get("properties", {}):
                    return False, f"Field '{field.get('id')}' missing validation"
            
            return True, ""
        
        elif rule_name == "has_event_handlers":
            has_events = self._has_event_handlers(output)
            if not has_events:
                return False, "No event handlers found"
            return True, ""
        
        elif rule_name == "has_data_source":
            component = output.get("component", {})
            properties = component.get("properties", {})
            if "dataSource" not in properties:
                return False, "Missing 'dataSource' in component"
            return True, ""
        
        else:
            # Unknown rule, skip
            return True, ""
    
    def _has_theme_references(self, obj: Any) -> bool:
        """Check if object has theme token references"""
        if isinstance(obj, dict):
            for value in obj.values():
                if self._has_theme_references(value):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if self._has_theme_references(item):
                    return True
        elif isinstance(obj, str):
            if re.search(r'\{[^}]+\}', obj):
                return True
        
        return False
    
    def _find_invalid_theme_tokens(self, obj: Any, path: str = "") -> List[str]:
        """Find invalid theme token references"""
        invalid = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                invalid.extend(self._find_invalid_theme_tokens(value, current_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                invalid.extend(self._find_invalid_theme_tokens(item, f"{path}[{i}]"))
        
        elif isinstance(obj, str):
            # Check for token references
            token_refs = re.findall(r'\{([^}]+)\}', obj)
            for ref in token_refs:
                if not self._is_valid_theme_token(ref):
                    invalid.append(f"{{{ref}}}")
        
        return invalid
    
    def _is_valid_theme_token(self, token_path: str) -> bool:
        """Check if theme token exists"""
        if not self.theme:
            return True  # Skip validation if no theme loaded
        
        parts = token_path.split('.')
        value = self.theme.get('tokens', {})
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return False
        
        return value is not None
    
    def _find_missing_alt_text(self, obj: Any, path: str = "") -> List[str]:
        """Find images missing alt text"""
        missing = []
        
        if isinstance(obj, dict):
            # Check if this is an image object
            if obj.get("type") == "image" or "src" in obj:
                if "alt" not in obj:
                    missing.append(path or "image")
            
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                missing.extend(self._find_missing_alt_text(value, current_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                missing.extend(self._find_missing_alt_text(item, f"{path}[{i}]"))
        
        return missing
    
    def _has_event_handlers(self, obj: Any) -> bool:
        """Check if object has event handlers"""
        if isinstance(obj, dict):
            if "events" in obj or "onClick" in obj or "onChange" in obj:
                return True
            
            for value in obj.values():
                if self._has_event_handlers(value):
                    return True
        
        elif isinstance(obj, list):
            for item in obj:
                if self._has_event_handlers(item):
                    return True
        
        return False
    
    def _print_test_result(self, result: Dict[str, Any]) -> None:
        """Print test result"""
        status_icon = {
            'PASS': '✅',
            'FAIL': '❌',
            'WARN': '⚠️',
            'SKIP': '⏭️'
        }.get(result['status'], '❓')
        
        print(f"{status_icon} {result['test_id']}: {result['name']}")
        
        for error in result['errors']:
            print(f"   ❌ {error}")
        
        for warning in result['warnings']:
            print(f"   ⚠️  {warning}")
    
    def generate_report(self, output_format: str = "markdown") -> str:
        """Generate test report"""
        if output_format == "markdown":
            return self._generate_markdown_report()
        elif output_format == "json":
            return self._generate_json_report()
        elif output_format == "junit":
            return self._generate_junit_report()
        else:
            return ""
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown report"""
        lines = [
            "# Golden Test Results",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Tests:** {len(self.test_results)}",
            f"**Passed:** {sum(1 for r in self.test_results if r['status'] == 'PASS')}",
            f"**Failed:** {sum(1 for r in self.test_results if r['status'] == 'FAIL')}",
            f"**Warnings:** {sum(1 for r in self.test_results if r['status'] == 'WARN')}",
            ""
        ]
        
        # Summary by category
        by_category = {}
        for result in self.test_results:
            cat = result['category']
            if cat not in by_category:
                by_category[cat] = {'total': 0, 'passed': 0, 'failed': 0}
            
            by_category[cat]['total'] += 1
            if result['status'] == 'PASS':
                by_category[cat]['passed'] += 1
            elif result['status'] == 'FAIL':
                by_category[cat]['failed'] += 1
        
        lines.append("## Summary by Category")
        lines.append("")
        lines.append("| Category | Total | Passed | Failed |")
        lines.append("|----------|-------|--------|--------|")
        
        for cat, stats in sorted(by_category.items()):
            lines.append(f"| {cat} | {stats['total']} | {stats['passed']} | {stats['failed']} |")
        
        lines.append("")
        
        # Failed tests
        failed_tests = [r for r in self.test_results if r['status'] == 'FAIL']
        if failed_tests:
            lines.append("## Failed Tests")
            lines.append("")
            
            for result in failed_tests:
                lines.append(f"### ❌ {result['test_id']}")
                lines.append(f"**Category:** {result['category']}")
                
                for error in result['errors']:
                    lines.append(f"**Error:** {error}")
                
                lines.append("")
        
        # Passed tests
        passed_tests = [r for r in self.test_results if r['status'] == 'PASS']
        if passed_tests:
            lines.append("## Passed Tests")
            lines.append("")
            
            for result in passed_tests:
                lines.append(f"✅ {result['test_id']}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r['status'] == 'PASS'),
                "failed": sum(1 for r in self.test_results if r['status'] == 'FAIL'),
                "warnings": sum(1 for r in self.test_results if r['status'] == 'WARN')
            },
            "results": self.test_results
        }
        
        return json.dumps(report, indent=2, ensure_ascii=False)
    
    def _generate_junit_report(self) -> str:
        """Generate JUnit XML report"""
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<testsuites name="SmartSpec Golden Tests" tests="{len(self.test_results)}" '
            f'failures="{sum(1 for r in self.test_results if r["status"] == "FAIL")}" '
            f'time="0">',
            '  <testsuite name="Golden Tests">'
        ]
        
        for result in self.test_results:
            lines.append(f'    <testcase name="{result["test_id"]}" classname="{result["category"]}">')
            
            if result['status'] == 'FAIL':
                for error in result['errors']:
                    lines.append(f'      <failure message="{error}"/>')
            
            lines.append('    </testcase>')
        
        lines.append('  </testsuite>')
        lines.append('</testsuites>')
        
        return '\n'.join(lines)
    
    def save_report(self, output_file: str, content: str) -> None:
        """Save report to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)


def main():
    """Main CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SmartSpec Golden Test Validator")
    parser.add_argument("--test-id")
    parser.add_argument("--category")
    parser.add_argument("--input-file")
    parser.add_argument("--theme-file", default=".spec/theme.json")
    parser.add_argument("--verbose", type=bool, default=False)
    parser.add_argument("--output-format", default="markdown", choices=["markdown", "json", "junit"])
    parser.add_argument("--output-file", default=".spec/test_results.md")
    parser.add_argument("--fail-fast", type=bool, default=False)
    
    args = parser.parse_args()
    
    validator = GoldenTestValidator(args.theme_file)
    
    try:
        # Load theme
        print("📦 Loading theme...")
        validator.load_theme()
        
        # Load golden tests
        print("📋 Loading golden tests...")
        tests = validator.load_golden_tests()
        print(f"✅ Loaded {len(tests)} golden tests")
        
        # Filter tests
        tests = validator.filter_tests(tests, args.test_id, args.category)
        print(f"🔍 Running {len(tests)} tests...")
        print()
        
        # Run tests
        results = validator.run_tests(tests, args.fail_fast, args.verbose)
        
        # Generate report
        print()
        print("📝 Generating report...")
        report = validator.generate_report(args.output_format)
        
        # Save report
        validator.save_report(args.output_file, report)
        print(f"✅ Saved report to {args.output_file}")
        
        # Print summary
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        warnings = sum(1 for r in results if r['status'] == 'WARN')
        
        print()
        print("📊 Summary:")
        print(f"   Total: {len(results)}")
        print(f"   ✅ Passed: {passed}")
        print(f"   ❌ Failed: {failed}")
        print(f"   ⚠️  Warnings: {warnings}")
        
        # Exit with appropriate code
        if failed > 0:
            sys.exit(1)
        else:
            sys.exit(0)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
