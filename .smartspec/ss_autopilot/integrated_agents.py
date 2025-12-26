"""
Integrated Agents - Pre-configured wrapped agents

Exports all agents with integration features enabled:
- Advanced logging
- Input validation
- Performance profiling
- Caching (where appropriate)
- Rate limiting (where appropriate)

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

from .agent_wrapper import wrap_agent
from .orchestrator_agent import OrchestratorAgent
from .status_agent import StatusAgent
from .intent_parser_agent import IntentParserAgent
from .workflow_loader import WorkflowCatalog


# ============================================================================
# Orchestrator Agent (with caching)
# ============================================================================

def get_orchestrator_agent(workflows_dir: str = None) -> 'AgentWrapper':
    """
    Get wrapped orchestrator agent with all features enabled.
    
    Features:
    - Logging: ✅ (all operations)
    - Validation: ✅ (all inputs)
    - Profiling: ✅ (all operations)
    - Caching: ✅ (state reads, workflow searches)
    - Rate limiting: ❌ (not needed for orchestrator)
    
    Args:
        workflows_dir: Path to workflows directory
        
    Returns:
        Wrapped OrchestratorAgent
        
    Example:
        >>> agent = get_orchestrator_agent()
        >>> state = agent.read_state("spec-core-001")
    """
    if workflows_dir:
        agent = OrchestratorAgent(workflows_dir)
    else:
        agent = OrchestratorAgent()
    
    return wrap_agent(
        agent,
        "orchestrator",
        enable_logging=True,
        enable_validation=True,
        enable_profiling=True,
        enable_caching=True,  # Cache state reads
        enable_rate_limiting=False
    )


# ============================================================================
# Status Agent (with caching)
# ============================================================================

def get_status_agent() -> 'AgentWrapper':
    """
    Get wrapped status agent with all features enabled.
    
    Features:
    - Logging: ✅ (all queries)
    - Validation: ✅ (all inputs)
    - Profiling: ✅ (all operations)
    - Caching: ✅ (status queries)
    - Rate limiting: ❌ (not needed)
    
    Returns:
        Wrapped StatusAgent
        
    Example:
        >>> agent = get_status_agent()
        >>> status = agent.query("What is the status of spec-core-001?")
    """
    agent = StatusAgent()
    
    return wrap_agent(
        agent,
        "status",
        enable_logging=True,
        enable_validation=True,
        enable_profiling=True,
        enable_caching=True,  # Cache status queries
        enable_rate_limiting=False
    )


# ============================================================================
# Intent Parser Agent (with rate limiting)
# ============================================================================

def get_intent_parser_agent() -> 'AgentWrapper':
    """
    Get wrapped intent parser agent with all features enabled.
    
    Features:
    - Logging: ✅ (all parses)
    - Validation: ✅ (all inputs)
    - Profiling: ✅ (all operations)
    - Caching: ✅ (parsed intents)
    - Rate limiting: ✅ (prevent abuse)
    
    Returns:
        Wrapped IntentParserAgent
        
    Example:
        >>> agent = get_intent_parser_agent()
        >>> intent = agent.parse("Create a new spec for user authentication")
    """
    agent = IntentParserAgent()
    
    return wrap_agent(
        agent,
        "intent_parser",
        enable_logging=True,
        enable_validation=True,
        enable_profiling=True,
        enable_caching=True,  # Cache parsed intents
        enable_rate_limiting=True  # Prevent abuse
    )


# ============================================================================
# Workflow Catalog (with caching)
# ============================================================================

def get_workflow_catalog(workflows_dir: str = None) -> 'AgentWrapper':
    """
    Get wrapped workflow catalog with all features enabled.
    
    Features:
    - Logging: ✅ (all searches)
    - Validation: ✅ (all inputs)
    - Profiling: ✅ (all operations)
    - Caching: ✅ (workflow searches)
    - Rate limiting: ❌ (not needed)
    
    Args:
        workflows_dir: Path to workflows directory
        
    Returns:
        Wrapped WorkflowCatalog
        
    Example:
        >>> catalog = get_workflow_catalog()
        >>> workflows = catalog.search("generate spec")
    """
    if workflows_dir:
        catalog = WorkflowCatalog(workflows_dir)
    else:
        catalog = WorkflowCatalog()
    
    return wrap_agent(
        catalog,
        "workflow_catalog",
        enable_logging=True,
        enable_validation=True,
        enable_profiling=True,
        enable_caching=True,  # Cache workflow searches
        enable_rate_limiting=False
    )


# ============================================================================
# Convenience Functions
# ============================================================================

def get_all_agents(workflows_dir: str = None) -> dict:
    """
    Get all wrapped agents in a dictionary.
    
    Args:
        workflows_dir: Path to workflows directory
        
    Returns:
        Dictionary of wrapped agents
        
    Example:
        >>> agents = get_all_agents()
        >>> orchestrator = agents['orchestrator']
        >>> status = agents['status']
    """
    return {
        'orchestrator': get_orchestrator_agent(workflows_dir),
        'status': get_status_agent(),
        'intent_parser': get_intent_parser_agent(),
        'workflow_catalog': get_workflow_catalog(workflows_dir)
    }


# ============================================================================
# Export
# ============================================================================

__all__ = [
    'get_orchestrator_agent',
    'get_status_agent',
    'get_intent_parser_agent',
    'get_workflow_catalog',
    'get_all_agents',
]
