"""
Agent Wrapper - Integration layer for new modules

Wraps existing agents with:
- Advanced logging
- Input validation
- Rate limiting
- Performance profiling
- Caching

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

from typing import Any, Callable, Dict, Optional
from functools import wraps
import inspect
import time

from .advanced_logger import get_logger
from .input_validator import PathValidator, InputValidator
from .rate_limiter import RateLimiter, RateLimitConfig
from .performance_profiler import _profiler as profiler
from .advanced_cache import MultiLevelCache


class AgentWrapper:
    """
    Wrapper that adds advanced features to existing agents.
    
    Features:
    - Logging with correlation IDs
    - Input validation
    - Rate limiting
    - Performance profiling
    - Result caching
    """
    
    def __init__(
        self,
        agent: Any,
        agent_name: str,
        enable_logging: bool = True,
        enable_validation: bool = True,
        enable_rate_limiting: bool = False,
        enable_profiling: bool = True,
        enable_caching: bool = False,
        rate_limit_config: Optional[RateLimitConfig] = None
    ):
        """
        Initialize agent wrapper.
        
        Args:
            agent: Agent instance to wrap
            agent_name: Name of the agent (for logging)
            enable_logging: Enable advanced logging
            enable_validation: Enable input validation
            enable_rate_limiting: Enable rate limiting
            enable_profiling: Enable performance profiling
            enable_caching: Enable result caching
            rate_limit_config: Rate limit configuration
        """
        self.agent = agent
        self.agent_name = agent_name
        self.enable_logging = enable_logging
        self.enable_validation = enable_validation
        self.enable_rate_limiting = enable_rate_limiting
        self.enable_profiling = enable_profiling
        self.enable_caching = enable_caching
        
        # Initialize modules
        if self.enable_logging:
            self.logger = get_logger(agent_name)
        
        if self.enable_validation:
            self.path_validator = PathValidator()
            self.input_validator = InputValidator()
        
        if self.enable_rate_limiting:
            if rate_limit_config:
                self.rate_limiter = RateLimiter(rate_limit_config)
            else:
                # Use default moderate tier
                self.rate_limiter = RateLimiter.from_tier("moderate")
        
        if self.enable_caching:
            self.cache = MultiLevelCache(
                l1_max_size=100,
                l2_max_size=1000
            )
        
        # Wrap all public methods
        self._wrap_methods()
    
    def _wrap_methods(self):
        """Wrap all public methods of the agent"""
        for name in dir(self.agent):
            # Skip private methods and non-callables
            if name.startswith('_'):
                continue
            
            attr = getattr(self.agent, name)
            if not callable(attr):
                continue
            
            # Wrap the method
            wrapped = self._wrap_method(name, attr)
            setattr(self, name, wrapped)
    
    def _wrap_method(self, method_name: str, method: Callable) -> Callable:
        """
        Wrap a single method with all enabled features.
        
        Args:
            method_name: Name of the method
            method: Method to wrap
            
        Returns:
            Wrapped method
        """
        @wraps(method)
        def wrapper(*args, **kwargs):
            operation_name = f"{self.agent_name}.{method_name}"
            
            # 1. Logging - Start
            if self.enable_logging:
                self.logger.info(
                    f"Starting {operation_name}",
                    args=str(args)[:100],  # Truncate for readability
                    kwargs=str(kwargs)[:100]
                )
            
            # 2. Input Validation
            if self.enable_validation:
                try:
                    self._validate_inputs(args, kwargs)
                except Exception as e:
                    if self.enable_logging:
                        self.logger.error(
                            f"Input validation failed for {operation_name}",
                            error=str(e)
                        )
                    raise
            
            # 3. Rate Limiting
            if self.enable_rate_limiting:
                identifier = f"{self.agent_name}_{method_name}"
                rate_result = self.rate_limiter.check_rate_limit(identifier)
                
                # Unwrap if needed
                if isinstance(rate_result, dict) and "result" in rate_result:
                    rate_info = rate_result["result"]
                else:
                    rate_info = rate_result
                
                # Check if allowed
                allowed = rate_info.get("allowed", True) if isinstance(rate_info, dict) else True
                if not allowed:
                    error_msg = f"Rate limit exceeded for {operation_name}"
                    if self.enable_logging:
                        self.logger.warning(error_msg)
                    raise RuntimeError(error_msg)
            
            # 4. Caching - Check cache
            if self.enable_caching:
                cache_key = self._make_cache_key(method_name, args, kwargs)
                cached_result = self.cache.get(cache_key)
                
                # Unwrap if needed (cache methods have @with_error_handling)
                if isinstance(cached_result, dict) and "result" in cached_result:
                    cached = cached_result["result"]
                else:
                    cached = cached_result
                
                if cached is not None:
                    if self.enable_logging:
                        self.logger.info(f"Cache hit for {operation_name}")
                    return cached
            
            # 5. Performance Profiling - Start timer
            start_time = time.time() if self.enable_profiling else None
            
            # 6. Execute method
            try:
                result = method(*args, **kwargs)
                
                # Track execution time
                if self.enable_profiling and start_time:
                    execution_time = time.time() - start_time
                    profiler.track(operation_name, execution_time)
                
                # 7. Caching - Store result
                if self.enable_caching:
                    cache_key = self._make_cache_key(method_name, args, kwargs)
                    self.cache.set(cache_key, result, ttl=300)  # 5 minutes
                
                # 8. Logging - Success
                if self.enable_logging:
                    self.logger.info(
                        f"Completed {operation_name}",
                        status="success"
                    )
                
                return result
            
            except Exception as e:
                # 9. Logging - Error
                if self.enable_logging:
                    self.logger.error(
                        f"Error in {operation_name}",
                        error=str(e),
                        error_type=type(e).__name__
                    )
                raise
            
            finally:
                # 10. Performance Profiling - Record
                pass  # Profiling handled by track()
        
        return wrapper
    
    def _validate_inputs(self, args: tuple, kwargs: dict):
        """
        Validate inputs.
        
        Args:
            args: Positional arguments
            kwargs: Keyword arguments
            
        Raises:
            ValueError: If input validation fails
        """
        # Validate string inputs
        for arg in args:
            if isinstance(arg, str):
                # Check for path traversal
                if '/' in arg or '\\' in arg:
                    if not self.path_validator.is_safe_path(arg):
                        raise ValueError(f"Unsafe path detected: {arg}")
        
        for key, value in kwargs.items():
            if isinstance(value, str):
                # Check for path traversal
                if '/' in value or '\\' in value:
                    if not self.path_validator.is_safe_path(value):
                        raise ValueError(f"Unsafe path detected in {key}: {value}")
    
    def _make_cache_key(self, method_name: str, args: tuple, kwargs: dict) -> str:
        """
        Make cache key from method name and arguments.
        
        Args:
            method_name: Method name
            args: Positional arguments
            kwargs: Keyword arguments
            
        Returns:
            Cache key string
        """
        # Simple key generation
        key_parts = [self.agent_name, method_name]
        
        # Add args
        for arg in args:
            if isinstance(arg, (str, int, float, bool)):
                key_parts.append(str(arg))
        
        # Add kwargs
        for k, v in sorted(kwargs.items()):
            if isinstance(v, (str, int, float, bool)):
                key_parts.append(f"{k}={v}")
        
        return ":".join(key_parts)
    
    def __getattr__(self, name: str):
        """Delegate attribute access to wrapped agent"""
        return getattr(self.agent, name)


def wrap_agent(
    agent: Any,
    agent_name: str,
    **kwargs
) -> AgentWrapper:
    """
    Convenience function to wrap an agent.
    
    Args:
        agent: Agent instance to wrap
        agent_name: Name of the agent
        **kwargs: Additional arguments for AgentWrapper
        
    Returns:
        Wrapped agent
        
    Example:
        >>> from .orchestrator_agent import OrchestratorAgent
        >>> agent = OrchestratorAgent()
        >>> wrapped = wrap_agent(agent, "orchestrator", enable_caching=True)
        >>> state = wrapped.read_state("spec-001")
    """
    return AgentWrapper(agent, agent_name, **kwargs)


# Export all
__all__ = [
    'AgentWrapper',
    'wrap_agent',
]
