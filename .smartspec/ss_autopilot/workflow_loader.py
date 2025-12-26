"""
Workflow Loader - Load and parse all SmartSpec workflows.

This module loads all 63 workflows from .smartspec/workflows/
and provides a searchable catalog.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import re

from .error_handler import (
    safe_file_read,
    with_error_handling,
    FileNotFoundError,
    ParseError,
    WorkflowNotFoundError
)


class Workflow:
    """Represents a SmartSpec workflow"""
    
    def __init__(self, name: str, path: Path):
        """
        Initialize Workflow.
        
        Args:
            name: Workflow name
            path: Path to workflow file
        """
        self.name = name
        self.path = path
        self.content = ""
        self.metadata = {}
        self.errors = []
        self._parse()
    
    def _parse(self):
        """
        Parse workflow file to extract metadata with error handling.
        """
        if not self.path.exists():
            self.errors.append(f"Workflow file not found: {self.path}")
            return
        
        try:
            # Read file safely
            result = safe_file_read(str(self.path))
            
            if result.get("error"):
                self.errors.append(f"Failed to read workflow: {result.get('message')}")
                return
            
            self.content = result["content"]
            
            # Extract title (first # heading)
            try:
                title_match = re.search(r'^#\s+(.+?)$', self.content, re.MULTILINE)
                self.metadata['title'] = title_match.group(1) if title_match else self.name
            except Exception as e:
                self.metadata['title'] = self.name
                self.errors.append(f"Failed to extract title: {str(e)}")
            
            # Extract description (first paragraph after title)
            try:
                desc_match = re.search(r'^#.+?\n\n(.+?)(?:\n\n|\n#)', self.content, re.MULTILINE | re.DOTALL)
                self.metadata['description'] = desc_match.group(1).strip() if desc_match else ""
            except Exception as e:
                self.metadata['description'] = ""
                self.errors.append(f"Failed to extract description: {str(e)}")
            
            # Extract purpose
            try:
                purpose_match = re.search(r'(?:Purpose|เป้าหมาย|จุดประสงค์):\s*(.+?)(?:\n\n|\n#)', self.content, re.IGNORECASE | re.DOTALL)
                self.metadata['purpose'] = purpose_match.group(1).strip() if purpose_match else ""
            except Exception as e:
                self.metadata['purpose'] = ""
                self.errors.append(f"Failed to extract purpose: {str(e)}")
            
            # Extract when to use
            try:
                when_match = re.search(r'(?:When to use|เมื่อไหร่ควรใช้):\s*(.+?)(?:\n\n|\n#)', self.content, re.IGNORECASE | re.DOTALL)
                self.metadata['when_to_use'] = when_match.group(1).strip() if when_match else ""
            except Exception as e:
                self.metadata['when_to_use'] = ""
                self.errors.append(f"Failed to extract when_to_use: {str(e)}")
            
            # Extract parameters (look for ## Parameters section)
            try:
                params_match = re.search(r'##\s+(?:Parameters|พารามิเตอร์).+?\n(.+?)(?:\n##|\Z)', self.content, re.IGNORECASE | re.DOTALL)
                if params_match:
                    params_text = params_match.group(1)
                    # Extract parameter names (look for --param or `--param`)
                    param_names = re.findall(r'`?--([a-z-]+)`?', params_text)
                    self.metadata['parameters'] = param_names
                else:
                    self.metadata['parameters'] = []
            except Exception as e:
                self.metadata['parameters'] = []
                self.errors.append(f"Failed to extract parameters: {str(e)}")
            
            # Categorize based on name
            try:
                self.metadata['category'] = self._categorize()
            except Exception as e:
                self.metadata['category'] = 'other'
                self.errors.append(f"Failed to categorize: {str(e)}")
        
        except Exception as e:
            self.errors.append(f"Unexpected error parsing workflow: {str(e)}")
    
    def _categorize(self) -> str:
        """
        Categorize workflow based on name.
        
        Returns:
            Category string
        """
        try:
            name_lower = self.name.lower()
            
            if 'generate_spec' in name_lower or 'generate_plan' in name_lower or 'generate_tasks' in name_lower:
                return 'core_development'
            elif 'implement' in name_lower:
                return 'core_development'
            elif 'sync_tasks' in name_lower or 'verify_tasks' in name_lower:
                return 'core_development'
            elif 'test' in name_lower or 'quality' in name_lower or 'validate' in name_lower:
                return 'testing_quality'
            elif 'ui' in name_lower or 'component' in name_lower or 'accessibility' in name_lower:
                return 'ui_ux'
            elif 'docs' in name_lower or 'export' in name_lower:
                return 'documentation'
            elif 'deploy' in name_lower or 'release' in name_lower or 'rollback' in name_lower:
                return 'operations'
            elif 'monitor' in name_lower or 'incident' in name_lower or 'hotfix' in name_lower:
                return 'operations'
            elif 'refactor' in name_lower or 'migration' in name_lower or 'dependency' in name_lower:
                return 'maintenance'
            elif 'security' in name_lower or 'threat' in name_lower:
                return 'security'
            elif 'nfr' in name_lower or 'performance' in name_lower or 'perf' in name_lower:
                return 'performance'
            elif 'theme' in name_lower or 'design' in name_lower or 'penpot' in name_lower:
                return 'design_system'
            elif 'project' in name_lower or 'feedback' in name_lower or 'reindex' in name_lower:
                return 'project_management'
            else:
                return 'other'
        except Exception:
            return 'other'
    
    def __repr__(self):
        return f"Workflow(name='{self.name}', category='{self.metadata.get('category', 'unknown')}')"


class WorkflowCatalog:
    """Catalog of all SmartSpec workflows"""
    
    def __init__(self, workflows_dir: str = "/home/ubuntu/SmartSpec/.smartspec/workflows"):
        """
        Initialize Workflow Catalog.
        
        Args:
            workflows_dir: Path to workflows directory
        """
        self.workflows_dir = Path(workflows_dir)
        self.workflows: Dict[str, Workflow] = {}
        self.errors = []
        self.load_all()
    
    def load_all(self):
        """
        Load all workflows from directory with error handling.
        """
        try:
            if not self.workflows_dir.exists():
                error_msg = f"Workflows directory not found: {self.workflows_dir}"
                self.errors.append(error_msg)
                print(f"Warning: {error_msg}")
                return
            
            loaded_count = 0
            failed_count = 0
            
            for workflow_file in self.workflows_dir.glob("smartspec_*.md"):
                try:
                    name = workflow_file.stem  # e.g., "smartspec_generate_spec"
                    workflow = Workflow(name, workflow_file)
                    self.workflows[name] = workflow
                    loaded_count += 1
                    
                    # Track workflow-level errors
                    if workflow.errors:
                        self.errors.extend([f"{name}: {err}" for err in workflow.errors])
                        failed_count += 1
                
                except Exception as e:
                    error_msg = f"Failed to load workflow {workflow_file.name}: {str(e)}"
                    self.errors.append(error_msg)
                    failed_count += 1
            
            print(f"Loaded {loaded_count} workflows ({failed_count} with errors)")
        
        except Exception as e:
            error_msg = f"Failed to load workflows: {str(e)}"
            self.errors.append(error_msg)
            print(f"Error: {error_msg}")
    
    @with_error_handling
    def get(self, name: str) -> Optional[Workflow]:
        """
        Get workflow by name with error handling.
        
        Args:
            name: Workflow name
            
        Returns:
            Workflow object or None if not found
        """
        try:
            workflow = self.workflows.get(name)
            if workflow is None:
                raise WorkflowNotFoundError(
                    workflow_name=name,
                    available_workflows=list(self.workflows.keys())[:5]
                )
            return workflow
        except WorkflowNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to get workflow: {str(e)}")
    
    @with_error_handling
    def search(self, query: str) -> List[Workflow]:
        """
        Search workflows by query with error handling.
        
        Args:
            query: Search query
            
        Returns:
            List of matching workflows
        """
        try:
            query_lower = query.lower()
            results = []
            
            for workflow in self.workflows.values():
                try:
                    # Search in name, title, description, purpose
                    if (query_lower in workflow.name.lower() or
                        query_lower in workflow.metadata.get('title', '').lower() or
                        query_lower in workflow.metadata.get('description', '').lower() or
                        query_lower in workflow.metadata.get('purpose', '').lower()):
                        results.append(workflow)
                except Exception:
                    # Skip workflows that fail search
                    continue
            
            return results
        
        except Exception as e:
            # Return empty list on error
            return []
    
    def get_by_category(self, category: str) -> List[Workflow]:
        """
        Get all workflows in a category with error handling.
        
        Args:
            category: Category name
            
        Returns:
            List of workflows in category
        """
        try:
            return [w for w in self.workflows.values() if w.metadata.get('category') == category]
        except Exception:
            return []
    
    def list_categories(self) -> List[str]:
        """
        List all categories with error handling.
        
        Returns:
            List of category names
        """
        try:
            categories = set(w.metadata.get('category', 'other') for w in self.workflows.values())
            return sorted(categories)
        except Exception:
            return []
    
    def get_core_development_loop(self) -> List[Workflow]:
        """
        Get workflows for core development loop with error handling.
        
        Returns:
            List of core development workflows
        """
        try:
            core_names = [
                'smartspec_generate_spec',
                'smartspec_generate_spec_from_prompt',
                'smartspec_generate_plan',
                'smartspec_generate_tasks',
                'smartspec_implement_tasks',
                'smartspec_sync_tasks_checkboxes',
                'smartspec_verify_tasks_progress_strict'
            ]
            
            workflows = []
            for name in core_names:
                if name in self.workflows:
                    workflows.append(self.workflows[name])
            
            return workflows
        
        except Exception:
            return []
    
    def recommend_workflow(self, state: Dict[str, Any]) -> Optional[Workflow]:
        """
        Recommend next workflow based on state with error handling.
        
        This is a simplified version. The full Orchestrator Agent
        will use LLM + decision tree for better recommendations.
        
        Args:
            state: Current state dict
            
        Returns:
            Recommended workflow or None if all done
        """
        try:
            # Has spec?
            if not state.get('has_spec', False):
                return self.workflows.get('smartspec_generate_spec')
            
            # Has plan?
            if not state.get('has_plan', False):
                return self.workflows.get('smartspec_generate_plan')
            
            # Has tasks?
            if not state.get('has_tasks', False):
                return self.workflows.get('smartspec_generate_tasks')
            
            # Implementation status
            impl_status = state.get('implementation_status', 'NOT_STARTED')
            
            if impl_status == 'NOT_STARTED':
                return self.workflows.get('smartspec_implement_tasks')
            
            elif impl_status == 'IN_PROGRESS':
                completion_rate = state.get('tasks_completion_rate', 0.0)
                needs_sync = state.get('needs_sync', False)
                
                if needs_sync or completion_rate >= 0.5:
                    if not state.get('did_sync_tasks', False):
                        return self.workflows.get('smartspec_sync_tasks_checkboxes')
                
                return self.workflows.get('smartspec_implement_tasks')
            
            elif impl_status == 'COMPLETED':
                # Has tests?
                if not state.get('has_tests', False):
                    return self.workflows.get('smartspec_generate_tests')
                
                # Tests passed?
                if not state.get('tests_passed', False):
                    return self.workflows.get('smartspec_test_suite_runner')
                
                # Quality gate?
                if not state.get('quality_gate_passed', False):
                    return self.workflows.get('smartspec_quality_gate')
                
                # Has docs?
                if not state.get('has_docs', False):
                    return self.workflows.get('smartspec_docs_generator')
                
                # All done!
                return None
            
            return None
        
        except Exception:
            # Return None on error (no recommendation)
            return None
    
    def summary(self) -> str:
        """
        Get summary of catalog with error handling.
        
        Returns:
            Summary string
        """
        try:
            lines = [
                f"Workflow Catalog Summary",
                f"=" * 50,
                f"Total workflows: {len(self.workflows)}",
                f""
            ]
            
            if self.errors:
                lines.append(f"⚠️  Errors: {len(self.errors)}")
                lines.append(f"")
            
            lines.append(f"By category:")
            
            for category in self.list_categories():
                workflows = self.get_by_category(category)
                lines.append(f"  {category}: {len(workflows)} workflows")
            
            return "\n".join(lines)
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"


# Example usage
if __name__ == "__main__":
    try:
        # Load catalog
        catalog = WorkflowCatalog()
        
        # Print summary
        print(catalog.summary())
        print()
        
        # Show errors if any
        if catalog.errors:
            print("Errors during loading:")
            for error in catalog.errors[:5]:  # Show first 5
                print(f"  - {error}")
            if len(catalog.errors) > 5:
                print(f"  ... and {len(catalog.errors) - 5} more")
            print()
        
        # Get core development loop
        print("Core Development Loop:")
        for workflow in catalog.get_core_development_loop():
            print(f"  - {workflow.name}")
        print()
        
        # Search
        print("Search 'implement':")
        search_result = catalog.search('implement')
        if isinstance(search_result, dict) and search_result.get("success"):
            workflows = search_result["result"]
        else:
            workflows = search_result
        
        for workflow in workflows:
            print(f"  - {workflow.name}: {workflow.metadata.get('title', '')}")
        print()
        
        # Recommend workflow
        state = {
            'has_spec': True,
            'has_plan': True,
            'has_tasks': True,
            'implementation_status': 'IN_PROGRESS',
            'tasks_completion_rate': 0.42,
            'needs_sync': False
        }
        
        recommended = catalog.recommend_workflow(state)
        print(f"Recommended workflow: {recommended.name if recommended else 'None'}")
        if recommended:
            print(f"  Title: {recommended.metadata.get('title', 'N/A')}")
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
