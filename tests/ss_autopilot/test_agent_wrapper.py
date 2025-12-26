"""
Unit tests for agent_wrapper.py

Tests:
- AgentWrapper creation
- Method wrapping
- Logging integration
- Input validation
- Rate limiting
- Performance profiling
- Caching
"""

import pytest
import time
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.agent_wrapper import AgentWrapper, wrap_agent
from ss_autopilot.rate_limiter import RateLimitConfig


# ============================================================================
# Mock Agent for Testing
# ============================================================================

class MockAgent:
    """Mock agent for testing"""
    
    def __init__(self):
        self.call_count = 0
    
    def simple_method(self, value: str) -> str:
        """Simple method that returns input"""
        self.call_count += 1
        return f"processed: {value}"
    
    def method_with_kwargs(self, a: int, b: int = 10) -> int:
        """Method with kwargs"""
        self.call_count += 1
        return a + b
    
    def slow_method(self) -> str:
        """Slow method for profiling tests"""
        self.call_count += 1
        time.sleep(0.01)
        return "done"
    
    def error_method(self):
        """Method that raises error"""
        self.call_count += 1
        raise ValueError("Test error")


# ============================================================================
# Test AgentWrapper
# ============================================================================

class TestAgentWrapper:
    """Test AgentWrapper class"""
    
    def test_wrapper_creation(self):
        """Test creating wrapper"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent")
        
        assert wrapper.agent == agent
        assert wrapper.agent_name == "mock_agent"
        assert wrapper.enable_logging is True
    
    def test_method_wrapping(self):
        """Test that methods are wrapped"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_logging=False)
        
        # Call wrapped method
        result = wrapper.simple_method("test")
        
        assert result == "processed: test"
        assert agent.call_count == 1
    
    def test_logging_integration(self):
        """Test logging integration"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_logging=True)
        
        # Should not raise exception
        result = wrapper.simple_method("test")
        assert result == "processed: test"
    
    def test_input_validation(self):
        """Test input validation"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_validation=True)
        
        # Safe input
        result = wrapper.simple_method("safe_value")
        assert result == "processed: safe_value"
        
        # Path traversal attempt
        with pytest.raises(Exception):
            wrapper.simple_method("../../../etc/passwd")
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        agent = MockAgent()
        # Use tier name instead of RateLimitConfig object
        wrapper = AgentWrapper(
            agent,
            "mock_agent",
            enable_rate_limiting=True,
            rate_limit_config="strict"  # Use predefined tier
        )
        
        # Note: strict tier allows 10 requests per 60 seconds
        # This test is simplified - just verify rate limiting is enabled
        result = wrapper.simple_method("test1")
        assert result == "processed: test1"
    
    def test_performance_profiling(self):
        """Test performance profiling"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_profiling=True)
        
        # Call slow method
        wrapper.slow_method()
        
        # Check that profiling data exists
        from ss_autopilot.performance_profiler import _profiler
        metrics = _profiler.get_metrics("mock_agent.slow_method")
        
        assert metrics is not None
        assert metrics.get("total_calls", 0) >= 1
    
    def test_caching(self):
        """Test result caching"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_caching=True)
        
        # First call - cache miss
        result1 = wrapper.simple_method("test")
        count1 = agent.call_count
        
        # Second call - cache hit
        result2 = wrapper.simple_method("test")
        count2 = agent.call_count
        
        assert result1 == result2
        assert count2 == count1  # Should not increment (cache hit)
    
    def test_error_handling(self):
        """Test error handling"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent", enable_logging=True)
        
        # Should propagate exception
        with pytest.raises(ValueError, match="Test error"):
            wrapper.error_method()


# ============================================================================
# Test wrap_agent
# ============================================================================

class TestWrapAgent:
    """Test wrap_agent convenience function"""
    
    def test_wrap_agent(self):
        """Test wrapping agent with convenience function"""
        agent = MockAgent()
        wrapped = wrap_agent(agent, "mock_agent")
        
        assert isinstance(wrapped, AgentWrapper)
        assert wrapped.agent == agent
    
    def test_wrap_agent_with_options(self):
        """Test wrapping with options"""
        agent = MockAgent()
        wrapped = wrap_agent(
            agent,
            "mock_agent",
            enable_caching=True,
            enable_profiling=False
        )
        
        assert wrapped.enable_caching is True
        assert wrapped.enable_profiling is False


# ============================================================================
# Integration Tests
# ============================================================================

class TestAgentWrapperIntegration:
    """Integration tests for agent wrapper"""
    
    def test_full_integration(self):
        """Test all features together"""
        agent = MockAgent()
        wrapper = AgentWrapper(
            agent,
            "mock_agent",
            enable_logging=True,
            enable_validation=True,
            enable_profiling=True,
            enable_caching=True
        )
        
        # Call method multiple times
        result1 = wrapper.simple_method("test")
        result2 = wrapper.simple_method("test")  # Cache hit
        result3 = wrapper.method_with_kwargs(5, b=15)
        
        assert result1 == "processed: test"
        assert result2 == "processed: test"
        assert result3 == 20
        
        # Check profiling
        from ss_autopilot.performance_profiler import _profiler
        metrics = _profiler.get_metrics("mock_agent.simple_method")
        assert metrics is not None
    
    def test_attribute_delegation(self):
        """Test that attributes are delegated to wrapped agent"""
        agent = MockAgent()
        wrapper = AgentWrapper(agent, "mock_agent")
        
        # Access attribute through wrapper
        assert wrapper.call_count == agent.call_count


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
