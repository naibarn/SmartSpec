#!/usr/bin/env python3
"""
SmartSpec Evidence Verification Script (Strict Mode)

This script verifies evidence hooks in tasks.md using strict evidence-based verification.
It treats checkboxes as non-authoritative and verifies each task via explicit evidence hooks.
"""

import os
import re
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


# Valid evidence types according to specification
VALID_EVIDENCE_TYPES = {'code', 'test', 'ui', 'docs'}

# Non-compliant types that should be rejected  
NON_COMPLIANT_TYPES = {'file_exists', 'test_exists', 'command'}

class EvidenceVerifier:
    def __init__(self, tasks_path: str, project_root: str, output_dir: str):
        self.tasks_path = Path(tasks_path)
        self.output_dir = Path(output_dir)
        self.workspace_root = Path(project_root).resolve()
        
        # Verification results
        self.results = {
            "workflow": "smartspec_verify_tasks_progress_strict",
            "version": "6.0.3-fixed",
            "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "inputs": {
                "tasks_path": str(tasks_path),
                "spec_id": self._extract_spec_id()
            },
            "totals": {
                "tasks": 0,
                "verified": 0,
                "not_verified": 0,
                "manual": 0,
                "missing_hooks": 0,
                "invalid_scope": 0
            },
            "results": [],
            "writes": {"reports": []},
            "next_steps": []
        }
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.run_dir = self.output_dir / self.results["run_id"]
        self.run_dir.mkdir(parents=True, exist_ok=True)

    def _extract_spec_id(self) -> str:
        """Extract spec ID from tasks file header"""
        try:
            with open(self.tasks_path, 'r') as f:
                for line in f:
                    if line.startswith('spec_id:'):
                        return line.split(':')[1].strip()
        except Exception:
            pass
        return "unknown"

    def _is_safe_path(self, path: str) -> bool:
        """Check if path is within workspace bounds"""
        try:
            resolved = (self.workspace_root / path).resolve()
            return str(resolved).startswith(str(self.workspace_root.resolve()))
        except Exception:
            return False

    def _check_file_exists(self, file_path: str) -> Tuple[bool, str]:
        """Check if file exists and is safe to access"""
        if not self._is_safe_path(file_path):
            return False, "invalid_scope"
        
        full_path = self.workspace_root / file_path
        if full_path.exists() and full_path.is_file():
            return True, "ok"
        return False, "not_found"

    def _check_directory_exists(self, dir_path: str) -> Tuple[bool, str]:
        """Check if directory exists and is safe to access"""
        if not self._is_safe_path(dir_path):
            return False, "invalid_scope"
        
        full_path = self.workspace_root / dir_path
        if full_path.exists() and full_path.is_dir():
            return True, "ok"
        return False, "not_found"

    def _search_in_file(self, file_path: str, content: str) -> Tuple[bool, str]:
        """Search for specific content in a file"""
        exists, scope = self._check_file_exists(file_path)
        if not exists:
            return False, scope
        
        try:
            with open(self.workspace_root / file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                if content in file_content:
                    return True, "ok"
                return False, "content_not_found"
        except Exception as e:
            return False, f"read_error: {str(e)}"


    def _parse_evidence_params(self, evidence_string: str) -> Dict[str, str]:
        """Parse evidence parameters supporting quoted values"""
        params = {}
        
        # Pattern: key=value or key="value with spaces"
        pattern = r'(\w+)=(?:"([^"]*)"|(\S+))'
        matches = re.findall(pattern, evidence_string)
        
        for match in matches:
            key = match[0]
            value = match[1] if match[1] else match[2]
            params[key] = value
        
        return params

    def _verify_code_evidence(self, evidence: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Verify code evidence hook"""
        # Parse evidence: code path=<path> [symbol=<symbol>] [contains=<content>]
        parts = evidence.split()
        evidence_dict = {"type": "code", "raw": evidence}
        
        path = None
        symbol = None
        contains = None
        
        for part in parts[1:]:  # Skip "code"
            if part.startswith('path='):
                path = part[5:]
            elif part.startswith('symbol='):
                symbol = part[7:]
            elif part.startswith('contains='):
                contains = part[9:]
        
        evidence_dict.update({"path": path, "symbol": symbol, "contains": contains})
        
        # Verify evidence
        if not path:
            evidence_dict.update({"matched": False, "scope": "invalid", "why": "Missing path parameter"})
            return evidence_dict
        
        # Debug output
        print(f"DEBUG: Checking path: {path}")
        
        # Check if path exists (file or directory)
        exists, scope = self._check_file_exists(path)
        if not exists:
            dir_exists, dir_scope = self._check_directory_exists(path)
            print(f"DEBUG: Directory check for {path}: exists={dir_exists}, scope={dir_scope}")
            exists, scope = dir_exists, dir_scope
        print(f"DEBUG: Final path check for {path}: exists={exists}, scope={scope}")
        if not exists:
            evidence_dict.update({"matched": False, "scope": scope, "why": f"Path not found or invalid scope: {path}"})
            return evidence_dict
        
        # If symbol or contains specified, search for it
        if symbol or contains:
            search_content = symbol or contains
            found, reason = self._search_in_file(path, search_content)
            if found:
                evidence_dict.update({"matched": True, "scope": "ok", "why": f"Found {search_content}"})
            else:
                evidence_dict.update({"matched": False, "scope": "ok", "why": f"Content not found: {search_content}"})
        else:
            evidence_dict.update({"matched": True, "scope": "ok", "why": "File exists"})
        
        evidence_dict["pointer"] = path
        return evidence_dict

    def _verify_test_evidence(self, evidence: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Verify test evidence hook"""
        # Parse evidence: test path=<path> [contains=<content>] [command=<cmd>]
        parts = evidence.split()
        evidence_dict = {"type": "test", "raw": evidence}
        
        path = None
        contains = None
        command = None
        
        for part in parts[1:]:  # Skip "test"
            if part.startswith('path='):
                path = part[5:]
            elif part.startswith('contains='):
                contains = part[9:]
            elif part.startswith('command='):
                command = part[8:]
        
        evidence_dict.update({"path": path, "contains": contains, "command": command})
        
        # Verify evidence
        if not path:
            evidence_dict.update({"matched": False, "scope": "invalid", "why": "Missing path parameter"})
            return evidence_dict
        
        # Check if path exists (file or directory)
        exists, scope = self._check_file_exists(path)
        if not exists:
            # Try as directory
            exists, scope = self._check_directory_exists(path)
            if not exists:
                evidence_dict.update({"matched": False, "scope": scope, "why": f"Path not found or invalid scope: {path}"})
                return evidence_dict
        
        # If contains specified, search for it
        if contains:
            # If path is a directory, search in files within it
            if (self.workspace_root / path).is_dir():
                found = False
                for root, dirs, files in os.walk(self.workspace_root / path):
                    for file in files:
                        if file.endswith('.ts') or file.endswith('.js') or file.endswith('.json'):
                            file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(file_path, self.workspace_root)
                            found_in_file, _ = self._search_in_file(rel_path, contains)
                            if found_in_file:
                                found = True
                                break
                    if found:
                        break
                
                if found:
                    evidence_dict.update({"matched": True, "scope": "ok", "why": f"Found {contains} in directory"})
                else:
                    evidence_dict.update({"matched": False, "scope": "ok", "why": f"Content not found in directory: {contains}"})
            else:
                # Search in specific file
                found, reason = self._search_in_file(path, contains)
                if found:
                    evidence_dict.update({"matched": True, "scope": "ok", "why": f"Found {contains}"})
                else:
                    evidence_dict.update({"matched": False, "scope": "ok", "why": f"Content not found: {contains}"})
        else:
            evidence_dict.update({"matched": True, "scope": "ok", "why": "Test path exists"})
        
        evidence_dict["pointer"] = path
        return evidence_dict

    def _verify_docs_evidence(self, evidence: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Verify docs evidence hook"""
        # Parse evidence: docs path=<path> [heading=<heading>] [contains=<content>]
        parts = evidence.split()
        evidence_dict = {"type": "docs", "raw": evidence}
        
        path = None
        heading = None
        contains = None
        
        for part in parts[1:]:  # Skip "docs"
            if part.startswith('path='):
                path = part[5:]
            elif part.startswith('heading='):
                heading = part[8:]
            elif part.startswith('contains='):
                contains = part[9:]
        
        evidence_dict.update({"path": path, "heading": heading, "contains": contains})
        
        # Verify evidence
        if not path:
            evidence_dict.update({"matched": False, "scope": "invalid", "why": "Missing path parameter"})
            return evidence_dict
        
        # Check if path exists (file or directory)
        exists, scope = self._check_file_exists(path)
        if not exists:
            dir_exists, dir_scope = self._check_directory_exists(path)
            print(f"DEBUG: Directory check for {path}: exists={dir_exists}, scope={dir_scope}")
            exists, scope = dir_exists, dir_scope
        # Debug log
        print(f"DEBUG: Check exists for {path}: exists={exists}, scope={scope}")
        if not exists:
            evidence_dict.update({"matched": False, "scope": scope, "why": f"Path not found or invalid scope: {path}"})
            return evidence_dict
        
        # If heading or contains specified, search for it
        if heading or contains:
            search_content = heading or contains
            found, reason = self._search_in_file(path, search_content)
            if found:
                evidence_dict.update({"matched": True, "scope": "ok", "why": f"Found {search_content}"})
            else:
                evidence_dict.update({"matched": False, "scope": "ok", "why": f"Content not found: {search_content}"})
        else:
            evidence_dict.update({"matched": True, "scope": "ok", "why": "Documentation exists"})
        
        evidence_dict["pointer"] = path
        return evidence_dict

    def _verify_ui_evidence(self, evidence: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Verify UI evidence hook"""
        # Parse evidence: ui screen=<screen> [route=<route>] [component=<comp>] [states=<states>]
        parts = evidence.split()
        evidence_dict = {"type": "ui", "raw": evidence}
        
        screen = None
        route = None
        component = None
        states = None
        
        for part in parts[1:]:  # Skip "ui"
            if part.startswith('screen='):
                screen = part[7:]
            elif part.startswith('route='):
                route = part[6:]
            elif part.startswith('component='):
                component = part[10:]
            elif part.startswith('states='):
                states = part[7:]
        
        evidence_dict.update({"screen": screen, "route": route, "component": component, "states": states})
        
        # UI evidence typically needs manual verification
        evidence_dict.update({
            "matched": False,
            "scope": "needs_manual",
            "why": "UI evidence requires manual verification",
            "pointer": f"screen: {screen}" if screen else "ui_component"
        })
        
        return evidence_dict


    def _suggest_conversion(self, evidence_type: str, params: Dict[str, str]) -> str:
        """Suggest how to convert non-compliant evidence type"""
        if evidence_type == 'file_exists':
            path = params.get('path', '')
            if 'test' in path.lower():
                return f"Convert to: evidence: test path={path}"
            else:
                return f"Convert to: evidence: code path={path}"
        
        elif evidence_type == 'test_exists':
            path = params.get('path', '')
            name = params.get('name', '')
            if name:
                return f"Convert to: evidence: test path={path} contains=\"{name}\""
            else:
                return f"Convert to: evidence: test path={path}"
        
        elif evidence_type == 'command':
            cmd = params.get('cmd', '')
            if 'tsc' in cmd:
                return "Convert to: evidence: code path=tsconfig.json"
            elif 'eslint' in cmd or 'lint' in cmd:
                return "Convert to: evidence: code path=.eslintrc.js"
            else:
                return "Convert to: evidence: code path=<relevant-file>"
        
        return "Use migrate_evidence_hooks.py to convert"

    def _verify_evidence_hook(self, evidence_line: str) -> Dict[str, Any]:
        """Verify a single evidence hook - FIXED to reject non-compliant types"""
        # Parse evidence line
        # Strip list marker
        evidence_line = evidence_line.strip().lstrip('- ').strip()
        if not evidence_line.startswith('evidence:'):
            return {
                "matched": False,
                "confidence": "low",
                "scope": "invalid",
                "why": "Invalid evidence format (must start with 'evidence:')",
                "raw": evidence_line
            }
        
        # Remove "evidence:" prefix
        evidence_content = evidence_line.strip()[9:].strip()
        
        # Extract evidence type
        parts = evidence_content.split(maxsplit=1)
        if not parts:
            return {
                "matched": False,
                "confidence": "low",
                "scope": "invalid",
                "why": "Missing evidence type",
                "raw": evidence_line
            }
        
        evidence_type = parts[0]
        params_string = parts[1] if len(parts) > 1 else ""
        
        # Parse parameters
        params = self._parse_evidence_params(params_string)
        
        # FIX #1: Check for non-compliant types
        if evidence_type in NON_COMPLIANT_TYPES:
            suggestion = self._suggest_conversion(evidence_type, params)
            return {
                "type": evidence_type,
                "raw": evidence_line,
                "matched": False,
                "confidence": "low",
                "scope": "invalid",
                "why": f"Non-compliant evidence type '{evidence_type}' is not supported by verifier",
                "suggestion": suggestion,
                "pointer": params.get('path', evidence_type)
            }
        
        # Check for valid types
        if evidence_type not in VALID_EVIDENCE_TYPES:
            return {
                "type": evidence_type,
                "raw": evidence_line,
                "matched": False,
                "confidence": "low",
                "scope": "invalid",
                "why": f"Unknown evidence type '{evidence_type}'. Valid types: {', '.join(VALID_EVIDENCE_TYPES)}",
                "pointer": evidence_type
            }
        
        # Route to type-specific verifier (simplified - use params dict)
        if evidence_type == 'code':
            return self._verify_code_evidence(evidence_line, params)
        elif evidence_type == 'test':
            return self._verify_test_evidence(evidence_line, params)
        elif evidence_type == 'docs':
            return self._verify_docs_evidence(evidence_line, params)
        elif evidence_type == 'ui':
            return self._verify_ui_evidence(evidence_line, params)
        
        return {
            "type": evidence_type,
            "raw": evidence_line,
            "matched": False,
            "confidence": "low",
            "scope": "invalid",
            "why": f"Unsupported evidence type: {evidence_type}"
        }


    def _calculate_task_confidence(self, evidence_results: List[Dict[str, Any]]) -> Tuple[str, str]:
        """Calculate confidence level and verification status for a task"""
        if not evidence_results:
            return "low", "missing_hooks"
        
        # Count matches by confidence level
        high_confidence_matches = 0
        medium_confidence_matches = 0
        total_valid = 0
        
        for evidence in evidence_results:
            if evidence["scope"] == "invalid_scope":
                continue  # Skip invalid scope evidence
            
            total_valid += 1
            if evidence["matched"] and evidence["scope"] == "ok":
                high_confidence_matches += 1
            elif not evidence["matched"] and evidence["scope"] == "ok":
                medium_confidence_matches += 1
        
        if total_valid == 0:
            return "low", "invalid_scope"
        
        # Calculate confidence
        if high_confidence_matches > 0:
            confidence = "high"
            status = "verified"
        elif medium_confidence_matches > 0:
            confidence = "medium"
            status = "not_verified"
        else:
            confidence = "low"
            status = "not_verified"
        
        # Check for UI evidence that needs manual verification
        has_ui_evidence = any(e.get("type") == "ui" for e in evidence_results)
        if has_ui_evidence and confidence == "low":
            status = "needs_manual"
        
        return confidence, status


    def _generate_suggested_hooks(self, task_title: str, task_id: str, failed_evidence: List[Dict[str, Any]]) -> List[str]:
        """Generate suggested evidence hooks for not_verified tasks - IMPROVED"""
        suggestions = []
        
        # Extract file path from title if present
        path_match = re.search(r'`([^`]+)`', task_title)
        if path_match:
            path = path_match.group(1)
            suggestions.append(f"evidence: code path={path}")
            
            # Extract symbol from title
            symbol_match = re.search(r'(\w+Service|\w+Client|\w+Model|\w+Controller|\w+Handler|\w+Util)', task_title)
            if symbol_match:
                symbol = symbol_match.group(1)
                suggestions.append(f"evidence: code path={path} symbol={symbol}")
        
        # Suggest test evidence
        test_path_base = task_id.lower().replace('tsk-', '').replace('-', '_')
        suggestions.append(f"evidence: test path=tests/unit/{test_path_base}.test.ts contains=\"{task_id}\"")
        
        # If there are failed evidence hooks with suggestions, include them
        for ev in failed_evidence:
            if 'suggestion' in ev and ev['suggestion']:
                suggestions.append(ev['suggestion'])
        
        # Remove duplicates
        seen = set()
        unique_suggestions = []
        for s in suggestions:
            if s not in seen:
                seen.add(s)
                unique_suggestions.append(s)
        
        return unique_suggestions[:5]


    def _parse_tasks_and_verify(self):
        """Parse tasks file and verify all evidence hooks"""
        try:
            with open(self.tasks_path, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading tasks file: {e}")
            sys.exit(1)
        
        # Split into lines and process
        lines = content.split('\n')
        current_task = None
        current_evidence = []
        
        for line in lines:
            # Check for task line
            task_match = re.match(r'^- \[([ x])\] (TSK-[A-Z]+-\d+) (.+)$', line)
            if task_match:
                # Process previous task
                if current_task:
                    self._process_task(current_task, current_evidence)
                
                # Start new task
                checkbox, task_id, title = task_match.groups()
                current_task = {
                    "task_id": task_id,
                    "title": title.strip(),
                    "checkbox": checkbox,
                    "evidence": [],
                    "status": "not_verified",
                    "confidence": "low"
                }
                current_evidence = []
            
            # Check for evidence line
            elif line.strip().startswith('- evidence:'):
                if current_task:
                    current_evidence.append(line.strip())
                    print(f"DEBUG: Found evidence line: {line.strip()}")
        
        # Process last task
        if current_task:
            self._process_task(current_task, current_evidence)
        
        # Update totals
        self.results["totals"]["tasks"] = len(self.results["results"])

    def _process_task(self, task: Dict[str, Any], evidence_lines: List[str]):
        """Process a single task and its evidence"""
        evidence_results = []
        print(f"DEBUG: Processing task {task['task_id']} with {len(evidence_lines)} evidence lines")
        
        for evidence_line in evidence_lines:
            print(f"DEBUG: About to verify: {evidence_line}")
            result = self._verify_evidence_hook(evidence_line)
            print(f"DEBUG: Verification result: {result}")
            evidence_results.append(result)
        
        # Calculate confidence and status
        confidence, status = self._calculate_task_confidence(evidence_results)
        
        # Generate suggested hooks if needed
        suggested_hooks = []
        if status in ["missing_hooks", "needs_manual", "not_verified"]:
            suggested_hooks = self._generate_suggested_hooks(task["title"], task["task_id"], [])
            suggested_hooks.extend(self._generate_suggested_hooks(task["title"], task["task_id"], []))
        
        # Determine why
        if status == "verified":
            why = "Evidence hooks satisfied"
        elif status == "missing_hooks":
            why = "No evidence hooks found"
        elif status == "needs_manual":
            why = "UI evidence requires manual verification"
        elif status == "invalid_scope":
            why = "Evidence points outside workspace"
        else:
            why = "Evidence hooks not satisfied"
        
        task_result = {
            "task_id": task["task_id"],
            "title": task["title"],
            "checkbox": task["checkbox"],
            "verified": status == "verified",
            "confidence": confidence,
            "status": status,
            "evidence": evidence_results,
            "suggested_hooks": suggested_hooks,
            "why": why
        }
        
        self.results["results"].append(task_result)
        
        # Update totals
        if status == "verified":
            self.results["totals"]["verified"] += 1
        elif status == "needs_manual":
            self.results["totals"]["manual"] += 1
        elif status == "missing_hooks":
            self.results["totals"]["missing_hooks"] += 1
        elif status == "invalid_scope":
            self.results["totals"]["invalid_scope"] += 1
        else:
            self.results["totals"]["not_verified"] += 1

    def _generate_markdown_report(self) -> str:
        """Generate markdown verification report"""
        report = f"""# Task Verification Report: {self.results['inputs']['spec_id']}

**Generated:** {datetime.now().isoformat()}  
**Run ID:** {self.results['run_id']}  
**Tasks File:** {self.results['inputs']['tasks_path']}

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | {self.results['totals']['tasks']} |
| Verified Done | {self.results['totals']['verified']} |
| Not Verified | {self.results['totals']['not_verified']} |
| Needs Manual Check | {self.results['totals']['manual']} |
| Missing Evidence Hooks | {self.results['totals']['missing_hooks']} |
| Invalid Evidence Scope | {self.results['totals']['invalid_scope']} |

## Task Details

"""
        
        # Group tasks by status
        verified_tasks = [t for t in self.results['results'] if t['status'] == 'verified']
        not_verified_tasks = [t for t in self.results['results'] if t['status'] == 'not_verified']
        manual_tasks = [t for t in self.results['results'] if t['status'] == 'needs_manual']
        missing_hooks_tasks = [t for t in self.results['results'] if t['status'] == 'missing_hooks']
        invalid_scope_tasks = [t for t in self.results['results'] if t['status'] == 'invalid_scope']
        
        if verified_tasks:
            report += "### ✅ Verified Tasks\n\n"
            for task in verified_tasks:
                report += f"- **{task['task_id']}**: {task['title']} (confidence: {task['confidence']})\n"
            report += "\n"
        
        if not_verified_tasks:
            report += "### ❌ Not Verified Tasks\n\n"
            for task in not_verified_tasks:
                report += f"- **{task['task_id']}**: {task['title']} (confidence: {task['confidence']})\n"
                report += f"  - Why: {task['why']}\n"
                if task['suggested_hooks']:
                    report += "  - Suggested hooks:\n"
                    for hook in task['suggested_hooks']:
                        report += f"    - {hook}\n"
                report += "\n"
        
        if manual_tasks:
            report += "### 👁️ Needs Manual Verification\n\n"
            for task in manual_tasks:
                report += f"- **{task['task_id']}**: {task['title']}\n"
                report += f"  - Why: {task['why']}\n"
                report += "\n"
        
        if missing_hooks_tasks:
            report += "### ⚠️ Missing Evidence Hooks\n\n"
            for task in missing_hooks_tasks:
                report += f"- **{task['task_id']}**: {task['title']}\n"
                if task['suggested_hooks']:
                    report += "  - Suggested hooks:\n"
                    for hook in task['suggested_hooks']:
                        report += f"    - {hook}\n"
                report += "\n"
        
        if invalid_scope_tasks:
            report += "### 🚫 Invalid Evidence Scope\n\n"
            for task in invalid_scope_tasks:
                report += f"- **{task['task_id']}**: {task['title']}\n"
                report += f"  - Why: {task['why']}\n"
                report += "\n"
        
        # Evidence gaps and remediation
        report += """## Evidence Gaps & Remediation

### Common Issues

1. **Missing Code Evidence**: Add `evidence: code path=<file_path>` for implementation files
2. **Missing Test Evidence**: Add `evidence: test path=<test_file_path>` for test files
3. **UI Components**: UI evidence requires manual verification
4. **Invalid Paths**: Ensure evidence paths are within the workspace

### Remediation Templates

```bash
# For code implementation
evidence: code path=packages/auth-lib/src/services/example.service.ts

# For tests
evidence: test path=tests/unit/example.test.ts

# For UI components
evidence: ui screen=ExampleScreen states=loading,empty,error,success

# For documentation
evidence: docs path=docs/example.md heading="Example Section"
```

## Next Steps

1. **Update Checkboxes** (optional):
   ```bash
   /smartspec_sync_tasks_checkboxes {tasks_path} --apply
   ```

2. **Generate Implementation Prompts**:
   ```bash
   /smartspec_report_implement_prompter --spec {spec_path} --tasks {tasks_path} --strict
   ```

3. **Address Evidence Gaps**: Add missing evidence hooks for unverified tasks

---

**Report Generation:** smartspec_verify_tasks_progress_strict v6.0.3  
**Platform:** kilo  
**Mode:** strict evidence-based verification
"""
        
        return report

    def run(self):
        """Run the verification process"""
        print(f"Starting evidence verification for {self.tasks_path}")
        
        # Parse and verify
        self._parse_tasks_and_verify()
        
        # Generate reports
        markdown_report = self._generate_markdown_report()
        
        # Write reports
        report_path = self.run_dir / "report.md"
        summary_path = self.run_dir / "summary.json"
        
        with open(report_path, 'w') as f:
            f.write(markdown_report)
        
        with open(summary_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        self.results["writes"]["reports"] = [str(report_path), str(summary_path)]
        
        # Add next steps
        self.results["next_steps"] = [
            {
                "cmd": f"/smartspec_sync_tasks_checkboxes {self.tasks_path} --apply",
                "why": "Update checkboxes based on verification results"
            },
            {
                "cmd": f"/smartspec_report_implement_prompter --spec specs/core/{self.results['inputs']['spec_id']}/spec.md --tasks {self.tasks_path} --strict",
                "why": "Generate implementation prompts for unverified tasks"
            }
        ]
        
        print(f"Verification complete. Reports written to {self.run_dir}")
        print(f"Summary: {self.results['totals']['verified']}/{self.results['totals']['tasks']} tasks verified")
        
        return self.results



def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="SmartSpec Evidence Verification Script (Strict Mode - FIXED)"
    )
    parser.add_argument(
        "tasks_md",
        help="Path to tasks.md file"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory)"
    )
    parser.add_argument(
        "--out",
        default=".spec/reports/verify-tasks-progress",
        help="Output directory for reports (default: .spec/reports/verify-tasks-progress)"
    )
    
    args = parser.parse_args()
    
    # Validate tasks file exists
    if not os.path.exists(args.tasks_md):
        print(f"Error: Tasks file not found: {args.tasks_md}")
        return 1
    
    # Create verifier and run
    verifier = EvidenceVerifier(
        tasks_path=args.tasks_md,
        project_root=args.project_root,
        output_dir=args.out
    )
    
    results = verifier.run()
    
    # Exit with appropriate code
    if results["totals"]["verified"] == results["totals"]["tasks"]:
        return 0  # All verified
    elif results["totals"]["invalid_scope"] > 0:
        return 1  # Validation error
    else:
        return 0  # Success with some unverified


if __name__ == "__main__":
    sys.exit(main())
