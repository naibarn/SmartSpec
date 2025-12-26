"""
Dynamic Routing - Advanced LangGraph routing capabilities

Provides:
- Dynamic route selection based on state
- Conditional branching
- Multi-path routing
- Route history tracking
- Route optimization

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

from typing import Dict, Any, List, Callable, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time

from .error_handler import with_error_handling
from .advanced_logger import get_logger


class RouteCondition(Enum):
    """Route condition types"""
    ALWAYS = "always"
    IF_TRUE = "if_true"
    IF_FALSE = "if_false"
    IF_EQUALS = "if_equals"
    IF_CONTAINS = "if_contains"
    IF_GREATER = "if_greater"
    IF_LESS = "if_less"
    CUSTOM = "custom"


@dataclass
class Route:
    """
    Represents a route in the workflow.
    
    Attributes:
        name: Route name
        target: Target node
        condition: Condition type
        condition_value: Value for condition check
        condition_func: Custom condition function
        priority: Route priority (higher = checked first)
        metadata: Additional metadata
    """
    name: str
    target: str
    condition: RouteCondition = RouteCondition.ALWAYS
    condition_value: Any = None
    condition_func: Optional[Callable[[Dict[str, Any]], bool]] = None
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def evaluate(self, state: Dict[str, Any], state_key: Optional[str] = None) -> bool:
        """
        Evaluate if this route should be taken.
        
        Args:
            state: Current workflow state
            state_key: State key to check (for non-CUSTOM conditions)
            
        Returns:
            True if route should be taken
        """
        if self.condition == RouteCondition.ALWAYS:
            return True
        
        if self.condition == RouteCondition.CUSTOM:
            if self.condition_func:
                return self.condition_func(state)
            return False
        
        # For other conditions, need state_key
        if not state_key or state_key not in state:
            return False
        
        value = state[state_key]
        
        if self.condition == RouteCondition.IF_TRUE:
            return bool(value)
        
        if self.condition == RouteCondition.IF_FALSE:
            return not bool(value)
        
        if self.condition == RouteCondition.IF_EQUALS:
            return value == self.condition_value
        
        if self.condition == RouteCondition.IF_CONTAINS:
            if isinstance(value, (list, tuple, set)):
                return self.condition_value in value
            if isinstance(value, str):
                return str(self.condition_value) in value
            return False
        
        if self.condition == RouteCondition.IF_GREATER:
            try:
                return float(value) > float(self.condition_value)
            except (TypeError, ValueError):
                return False
        
        if self.condition == RouteCondition.IF_LESS:
            try:
                return float(value) < float(self.condition_value)
            except (TypeError, ValueError):
                return False
        
        return False


@dataclass
class RouteHistory:
    """Route history entry"""
    from_node: str
    to_node: str
    route_name: str
    timestamp: float
    state_snapshot: Dict[str, Any]


class DynamicRouter:
    """
    Dynamic routing engine for LangGraph workflows.
    
    Features:
    - Multiple route conditions
    - Priority-based routing
    - Route history tracking
    - Default fallback routes
    """
    
    def __init__(self):
        """Initialize dynamic router"""
        self.logger = get_logger("dynamic_router")
        self.routes: Dict[str, List[Route]] = {}  # node -> routes
        self.history: List[RouteHistory] = []
        self.default_routes: Dict[str, str] = {}  # node -> default target
        
        self.logger.info("DynamicRouter initialized")
    
    @with_error_handling
    def add_route(
        self,
        from_node: str,
        route: Route
    ):
        """
        Add a route from a node.
        
        Args:
            from_node: Source node name
            route: Route to add
        """
        if from_node not in self.routes:
            self.routes[from_node] = []
        
        self.routes[from_node].append(route)
        
        # Sort by priority (descending)
        self.routes[from_node].sort(key=lambda r: r.priority, reverse=True)
        
        self.logger.info(
            "Route added",
            from_node=from_node,
            route_name=route.name,
            target=route.target,
            condition=route.condition.value,
            priority=route.priority
        )
    
    @with_error_handling
    def add_conditional_route(
        self,
        from_node: str,
        target: str,
        condition: RouteCondition,
        condition_value: Any = None,
        condition_func: Optional[Callable] = None,
        priority: int = 0,
        name: Optional[str] = None
    ):
        """
        Add a conditional route (convenience method).
        
        Args:
            from_node: Source node
            target: Target node
            condition: Condition type
            condition_value: Value for condition
            condition_func: Custom condition function
            priority: Route priority
            name: Route name (auto-generated if not provided)
        """
        if not name:
            name = f"{from_node}_to_{target}"
        
        route = Route(
            name=name,
            target=target,
            condition=condition,
            condition_value=condition_value,
            condition_func=condition_func,
            priority=priority
        )
        
        self.add_route(from_node, route)
    
    @with_error_handling
    def set_default_route(self, from_node: str, target: str):
        """
        Set default route for a node.
        
        Args:
            from_node: Source node
            target: Default target node
        """
        self.default_routes[from_node] = target
        self.logger.info("Default route set", from_node=from_node, target=target)
    
    @with_error_handling
    def route(
        self,
        from_node: str,
        state: Dict[str, Any],
        state_key: Optional[str] = None
    ) -> str:
        """
        Determine next node based on state.
        
        Args:
            from_node: Current node
            state: Current state
            state_key: State key to check for conditions
            
        Returns:
            Target node name
        """
        # Check if we have routes for this node
        if from_node not in self.routes:
            # Use default route if available
            if from_node in self.default_routes:
                target = self.default_routes[from_node]
                self._record_history(from_node, target, "default", state)
                return target
            
            # No routes defined
            self.logger.warning("No routes defined for node", from_node=from_node)
            return "END"
        
        # Evaluate routes in priority order
        for route in self.routes[from_node]:
            if route.evaluate(state, state_key):
                self._record_history(from_node, route.target, route.name, state)
                
                self.logger.info(
                    "Route selected",
                    from_node=from_node,
                    to_node=route.target,
                    route_name=route.name,
                    condition=route.condition.value
                )
                
                return route.target
        
        # No route matched, use default
        if from_node in self.default_routes:
            target = self.default_routes[from_node]
            self._record_history(from_node, target, "default_fallback", state)
            return target
        
        # No default, end workflow
        self.logger.warning("No route matched, ending workflow", from_node=from_node)
        return "END"
    
    def _record_history(
        self,
        from_node: str,
        to_node: str,
        route_name: str,
        state: Dict[str, Any]
    ):
        """Record route history"""
        entry = RouteHistory(
            from_node=from_node,
            to_node=to_node,
            route_name=route_name,
            timestamp=time.time(),
            state_snapshot=state.copy()
        )
        self.history.append(entry)
    
    @with_error_handling
    def get_history(
        self,
        from_node: Optional[str] = None,
        to_node: Optional[str] = None,
        limit: int = 100
    ) -> List[RouteHistory]:
        """
        Get route history.
        
        Args:
            from_node: Filter by source node
            to_node: Filter by target node
            limit: Maximum results
            
        Returns:
            List of RouteHistory
        """
        history = self.history
        
        if from_node:
            history = [h for h in history if h.from_node == from_node]
        
        if to_node:
            history = [h for h in history if h.to_node == to_node]
        
        return history[-limit:]
    
    @with_error_handling
    def get_route_stats(self) -> Dict[str, Any]:
        """
        Get routing statistics.
        
        Returns:
            Statistics dictionary
        """
        total_routes = sum(len(routes) for routes in self.routes.values())
        
        # Count route usage
        route_usage = {}
        for entry in self.history:
            key = f"{entry.from_node} -> {entry.to_node}"
            route_usage[key] = route_usage.get(key, 0) + 1
        
        # Most used routes
        most_used = sorted(
            route_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "total_nodes_with_routes": len(self.routes),
            "total_routes": total_routes,
            "total_default_routes": len(self.default_routes),
            "total_history_entries": len(self.history),
            "route_usage": route_usage,
            "most_used_routes": dict(most_used)
        }
    
    @with_error_handling
    def clear_history(self):
        """Clear route history"""
        self.history.clear()
        self.logger.info("Route history cleared")


# ============================================================================
# Helper Functions
# ============================================================================

def create_simple_router(routes: Dict[str, str]) -> DynamicRouter:
    """
    Create a simple router with direct node-to-node routes.
    
    Args:
        routes: Dictionary of {from_node: to_node}
        
    Returns:
        DynamicRouter instance
    
    Example:
        router = create_simple_router({
            "SPEC": "PLAN",
            "PLAN": "IMPLEMENT",
            "IMPLEMENT": "TEST",
            "TEST": "DEPLOY"
        })
    """
    router = DynamicRouter()
    
    for from_node, to_node in routes.items():
        router.add_conditional_route(
            from_node=from_node,
            target=to_node,
            condition=RouteCondition.ALWAYS
        )
    
    return router


def create_conditional_router(
    routes: Dict[str, List[Tuple[str, str, Any]]]
) -> DynamicRouter:
    """
    Create a router with conditional routes.
    
    Args:
        routes: Dictionary of {from_node: [(target, condition_type, condition_value), ...]}
        
    Returns:
        DynamicRouter instance
    
    Example:
        router = create_conditional_router({
            "SPEC": [
                ("PLAN", "if_equals", "approved"),
                ("SPEC", "if_equals", "rejected")
            ]
        })
    """
    router = DynamicRouter()
    
    for from_node, node_routes in routes.items():
        for i, (target, condition_type, condition_value) in enumerate(node_routes):
            condition = RouteCondition(condition_type)
            router.add_conditional_route(
                from_node=from_node,
                target=target,
                condition=condition,
                condition_value=condition_value,
                priority=len(node_routes) - i  # First route has highest priority
            )
    
    return router


# Export all
__all__ = [
    'RouteCondition',
    'Route',
    'RouteHistory',
    'DynamicRouter',
    'create_simple_router',
    'create_conditional_router',
]
