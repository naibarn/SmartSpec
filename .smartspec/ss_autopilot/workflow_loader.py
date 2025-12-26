"""
Workflow Loader - Load and parse all SmartSpec workflows.

This module loads all 59 workflows from .smartspec/workflows/
and provides a searchable catalog.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import re


class Workflow:
    """Represents a SmartSpec workflow"""
    
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.content = ""
        self.metadata = {}
        self._parse()
    
    def _parse(self):
        """Parse workflow file to extract metadata"""
        if not self.path.exists():
            return
        
        with open(self.path, encoding='utf-8') as f:
            self.content = f.read()
        
        # Extract title (first # heading)
        title_match = re.search(r'^#\s+(.+?)$', self.content, re.MULTILINE)
        self.metadata['title'] = title_match.group(1) if title_match else self.name
        
        # Extract description (first paragraph after title)
        desc_match = re.search(r'^#.+?\n\n(.+?)(?:\n\n|\n#)', self.content, re.MULTILINE | re.DOTALL)
        self.metadata['description'] = desc_match.group(1).strip() if desc_match else ""
        
        # Extract purpose
        purpose_match = re.search(r'(?:Purpose|เป้าหมาย|จุดประสงค์):\s*(.+?)(?:\n\n|\n#)', self.content, re.IGNORECASE | re.DOTALL)
        self.metadata['purpose'] = purpose_match.group(1).strip() if purpose_match else ""
        
        # Extract when to use
        when_match = re.search(r'(?:When to use|เมื่อไหร่ควรใช้):\s*(.+?)(?:\n\n|\n#)', self.content, re.IGNORECASE | re.DOTALL)
        self.metadata['when_to_use'] = when_match.group(1).strip() if when_match else ""
        
        # Extract parameters (look for ## Parameters section)
        params_match = re.search(r'##\s+(?:Parameters|พารามิเตอร์).+?\n(.+?)(?:\n##|\Z)', self.content, re.IGNORECASE | re.DOTALL)
        if params_match:
            params_text = params_match.group(1)
            # Extract parameter names (look for --param or `--param`)
            param_names = re.findall(r'`?--([a-z-]+)`?', params_text)
            self.metadata['parameters'] = param_names
        else:
            self.metadata['parameters'] = []
        
        # Categorize based on name
        self.metadata['category'] = self._categorize()
    
    def _categorize(self) -> str:
        """Categorize workflow based on name"""
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
    
    def __repr__(self):
        return f"Workflow(name='{self.name}', category='{self.metadata['category']}')"


class WorkflowCatalog:
    """Catalog of all SmartSpec workflows"""
    
    def __init__(self, workflows_dir: str = "/home/ubuntu/SmartSpec/.smartspec/workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows: Dict[str, Workflow] = {}
        self.load_all()
    
    def load_all(self):
        """Load all workflows from directory"""
        if not self.workflows_dir.exists():
            print(f"Warning: Workflows directory not found: {self.workflows_dir}")
            return
        
        for workflow_file in self.workflows_dir.glob("smartspec_*.md"):
            name = workflow_file.stem  # e.g., "smartspec_generate_spec"
            workflow = Workflow(name, workflow_file)
            self.workflows[name] = workflow
        
        print(f"Loaded {len(self.workflows)} workflows")
    
    def get(self, name: str) -> Optional[Workflow]:
        """Get workflow by name"""
        return self.workflows.get(name)
    
    def search(self, query: str) -> List[Workflow]:
        """Search workflows by query"""
        query_lower = query.lower()
        results = []
        
        for workflow in self.workflows.values():
            # Search in name, title, description, purpose
            if (query_lower in workflow.name.lower() or
                query_lower in workflow.metadata.get('title', '').lower() or
                query_lower in workflow.metadata.get('description', '').lower() or
                query_lower in workflow.metadata.get('purpose', '').lower()):
                results.append(workflow)
        
        return results
    
    def get_by_category(self, category: str) -> List[Workflow]:
        """Get all workflows in a category"""
        return [w for w in self.workflows.values() if w.metadata['category'] == category]
    
    def list_categories(self) -> List[str]:
        """List all categories"""
        categories = set(w.metadata['category'] for w in self.workflows.values())
        return sorted(categories)
    
    def get_core_development_loop(self) -> List[Workflow]:
        """Get workflows for core development loop"""
        core_names = [
            'smartspec_generate_spec',
            'smartspec_generate_spec_from_prompt',
            'smartspec_generate_plan',
            'smartspec_generate_tasks',
            'smartspec_implement_tasks',
            'smartspec_sync_tasks_checkboxes',
            'smartspec_verify_tasks_progress_strict'
        ]
        
        return [self.workflows[name] for name in core_names if name in self.workflows]
    
    def recommend_workflow(self, state: Dict[str, Any]) -> Optional[Workflow]:
        """
        Recommend next workflow based on state.
        
        This is a simplified version. The full Orchestrator Agent
        will use LLM + decision tree for better recommendations.
        """
        # Has spec?
        if not state.get('has_spec', False):
            return self.get('smartspec_generate_spec')
        
        # Has plan?
        if not state.get('has_plan', False):
            return self.get('smartspec_generate_plan')
        
        # Has tasks?
        if not state.get('has_tasks', False):
            return self.get('smartspec_generate_tasks')
        
        # Implementation status
        impl_status = state.get('implementation_status', 'NOT_STARTED')
        
        if impl_status == 'NOT_STARTED':
            return self.get('smartspec_implement_tasks')
        
        elif impl_status == 'IN_PROGRESS':
            completion_rate = state.get('tasks_completion_rate', 0.0)
            needs_sync = state.get('needs_sync', False)
            
            if needs_sync or completion_rate >= 0.5:
                if not state.get('did_sync_tasks', False):
                    return self.get('smartspec_sync_tasks_checkboxes')
            
            return self.get('smartspec_implement_tasks')
        
        elif impl_status == 'COMPLETED':
            # Has tests?
            if not state.get('has_tests', False):
                return self.get('smartspec_generate_tests')
            
            # Tests passed?
            if not state.get('tests_passed', False):
                return self.get('smartspec_test_suite_runner')
            
            # Quality gate?
            if not state.get('quality_gate_passed', False):
                return self.get('smartspec_quality_gate')
            
            # Has docs?
            if not state.get('has_docs', False):
                return self.get('smartspec_docs_generator')
            
            # All done!
            return None
        
        return None
    
    def summary(self) -> str:
        """Get summary of catalog"""
        lines = [
            f"Workflow Catalog Summary",
            f"=" * 50,
            f"Total workflows: {len(self.workflows)}",
            f"",
            f"By category:"
        ]
        
        for category in self.list_categories():
            workflows = self.get_by_category(category)
            lines.append(f"  {category}: {len(workflows)} workflows")
        
        return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    # Load catalog
    catalog = WorkflowCatalog()
    
    # Print summary
    print(catalog.summary())
    print()
    
    # Get core development loop
    print("Core Development Loop:")
    for workflow in catalog.get_core_development_loop():
        print(f"  - {workflow.name}")
    print()
    
    # Search
    print("Search 'implement':")
    for workflow in catalog.search('implement'):
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
    print(f"  Title: {recommended.metadata.get('title', '') if recommended else 'N/A'}")
