"""
Unit tests for performance_profiler.py

Tests:
- PerformanceMetrics tracking
- PerformanceProfiler singleton
- @profile decorator
- SimpleCache operations
- @cached decorator
- BottleneckAnalyzer
"""

import pytest
import time
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.performance_profiler import (
    PerformanceMetrics,
    PerformanceProfiler,
    profile,
    SimpleCache,
    cached,
    BottleneckAnalyzer,
    _profiler
)


# ============================================================================
# Pytest Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def reset_profiler():
    """Reset global profiler before each test"""
    _profiler.reset()
    _profiler.enable()
    yield
    _profiler.reset()


# ============================================================================
# Test PerformanceMetrics
# ============================================================================

class TestPerformanceMetrics:
    """Test PerformanceMetrics class"""
    
    def test_initial_metrics(self):
        """Test initial metrics values"""
        metrics = PerformanceMetrics("test_function")
        assert metrics.function_name == "test_function"
        assert metrics.total_calls == 0
        assert metrics.total_time == 0.0
    
    def test_update_metrics(self):
        """Test updating metrics"""
        metrics = PerformanceMetrics("test_function")
        
        metrics.update(1.0)
        assert metrics.total_calls == 1
        assert metrics.total_time == 1.0
        assert metrics.avg_time == 1.0
        assert metrics.min_time == 1.0
        assert metrics.max_time == 1.0
    
    def test_multiple_updates(self):
        """Test multiple updates"""
        metrics = PerformanceMetrics("test_function")
        
        metrics.update(1.0)
        metrics.update(2.0)
        metrics.update(3.0)
        
        assert metrics.total_calls == 3
        assert metrics.total_time == 6.0
        assert metrics.avg_time == 2.0
        assert metrics.min_time == 1.0
        assert metrics.max_time == 3.0
    
    def test_to_dict(self):
        """Test converting to dictionary"""
        metrics = PerformanceMetrics("test_function")
        metrics.update(1.5)
        
        result = metrics.to_dict()
        assert result["function_name"] == "test_function"
        assert result["total_calls"] == 1
        assert result["avg_time"] == 1.5


# ============================================================================
# Test PerformanceProfiler
# ============================================================================

class TestPerformanceProfiler:
    """Test PerformanceProfiler class"""
    
    def test_singleton_pattern(self):
        """Test singleton pattern"""
        profiler1 = PerformanceProfiler()
        profiler2 = PerformanceProfiler()
        assert profiler1 is profiler2
    
    def test_track_function(self):
        """Test tracking function execution"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        profiler.track("test_func", 1.0)
        
        metrics = profiler.get_metrics("test_func")
        assert metrics["total_calls"] == 1
        assert metrics["total_time"] == 1.0
    
    def test_get_all_metrics(self):
        """Test getting all metrics"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        profiler.track("func1", 1.0)
        profiler.track("func2", 2.0)
        
        all_metrics = profiler.get_metrics()
        assert "func1" in all_metrics
        assert "func2" in all_metrics
    
    def test_get_bottlenecks(self):
        """Test getting bottlenecks"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        profiler.track("slow_func", 5.0)
        profiler.track("fast_func", 0.1)
        
        bottlenecks = profiler.get_bottlenecks(top_n=2)
        assert len(bottlenecks) == 2
        assert bottlenecks[0]["function_name"] == "slow_func"
    
    def test_reset_specific_function(self):
        """Test resetting specific function metrics"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        profiler.track("func1", 1.0)
        profiler.track("func2", 2.0)
        
        profiler.reset("func1")
        
        metrics = profiler.get_metrics("func1")
        assert metrics == {"error": "Function not found"}
        
        metrics = profiler.get_metrics("func2")
        assert metrics["total_calls"] == 1
    
    def test_enable_disable(self):
        """Test enabling and disabling profiler"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        profiler.enable()
        profiler.track("func1", 1.0)
        assert len(profiler.get_metrics()) == 1
        
        profiler.disable()
        profiler.track("func2", 2.0)
        assert len(profiler.get_metrics()) == 1  # func2 not tracked


# ============================================================================
# Test @profile Decorator
# ============================================================================

class TestProfileDecorator:
    """Test @profile decorator"""
    
    def test_profile_decorator(self):
        """Test basic profile decorator"""
        _profiler.reset()
        
        @profile
        def test_function():
            time.sleep(0.01)
            return "result"
        
        result = test_function()
        assert result == "result"
        
        # Check metrics were recorded
        all_metrics = _profiler.get_metrics()
        assert len(all_metrics) > 0
    
    def test_profile_with_custom_name(self):
        """Test profile decorator with custom name"""
        _profiler.reset()
        
        @profile(name="custom_function")
        def test_function():
            return "result"
        
        test_function()
        
        metrics = _profiler.get_metrics("custom_function")
        assert metrics["total_calls"] == 1
    
    def test_profile_multiple_calls(self):
        """Test profiling multiple calls"""
        _profiler.reset()
        
        @profile
        def test_function():
            pass
        
        # Call multiple times
        for _ in range(5):
            test_function()
        
        all_metrics = _profiler.get_metrics()
        # Find the metric (key includes module name)
        metric = next(m for m in all_metrics.values() if "test_function" in m["function_name"])
        assert metric["total_calls"] == 5


# ============================================================================
# Test SimpleCache
# ============================================================================

class TestSimpleCache:
    """Test SimpleCache class"""
    
    def test_cache_set_get(self):
        """Test basic cache set and get"""
        cache = SimpleCache()
        
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        cache = SimpleCache()
        assert cache.get("nonexistent") is None
    
    def test_cache_ttl(self):
        """Test cache TTL expiration"""
        cache = SimpleCache(ttl=1)  # 1 second TTL
        
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Wait for expiration
        time.sleep(1.1)
        assert cache.get("key1") is None
    
    def test_cache_max_size(self):
        """Test cache max size eviction"""
        cache = SimpleCache(max_size=2)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # Should evict oldest
        
        # key1 should be evicted
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
    
    def test_cache_delete(self):
        """Test cache delete"""
        cache = SimpleCache()
        
        cache.set("key1", "value1")
        cache.delete("key1")
        
        assert cache.get("key1") is None
    
    def test_cache_clear(self):
        """Test cache clear"""
        cache = SimpleCache()
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_cache_stats(self):
        """Test cache statistics"""
        cache = SimpleCache(max_size=10, ttl=300)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        stats = cache.get_stats()
        assert stats["size"] == 2
        assert stats["max_size"] == 10
        assert stats["ttl"] == 300
        assert stats["usage_percent"] == 20.0


# ============================================================================
# Test @cached Decorator
# ============================================================================

class TestCachedDecorator:
    """Test @cached decorator"""
    
    def test_cached_decorator(self):
        """Test basic cached decorator"""
        cache = SimpleCache()
        call_count = [0]
        
        @cached(cache)
        def expensive_function(x):
            call_count[0] += 1
            return x * 2
        
        # First call - should execute
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count[0] == 1
        
        # Second call - should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count[0] == 1  # Not incremented
    
    def test_cached_with_key_func(self):
        """Test cached decorator with custom key function"""
        cache = SimpleCache()
        
        @cached(cache, key_func=lambda user_id: f"user_{user_id}")
        def get_user(user_id):
            return {"id": user_id, "name": f"User{user_id}"}
        
        user1 = get_user(1)
        user1_cached = get_user(1)
        
        assert user1 == user1_cached
    
    def test_cached_different_args(self):
        """Test cached decorator with different arguments"""
        cache = SimpleCache()
        call_count = [0]
        
        @cached(cache)
        def add(x, y):
            call_count[0] += 1
            return x + y
        
        result1 = add(1, 2)
        result2 = add(1, 2)  # Cached
        result3 = add(2, 3)  # Different args
        
        assert result1 == 3
        assert result2 == 3
        assert result3 == 5
        assert call_count[0] == 2  # Only 2 actual calls


# ============================================================================
# Test BottleneckAnalyzer
# ============================================================================

class TestBottleneckAnalyzer:
    """Test BottleneckAnalyzer class"""
    
    def test_analyze_empty(self):
        """Test analyzing with no data"""
        profiler = PerformanceProfiler()
        profiler.reset()
        
        analyzer = BottleneckAnalyzer(profiler)
        result = analyzer.analyze()
        
        assert result["success"] is True
        assert result["bottlenecks"] == []
    
    def test_analyze_with_slow_functions(self):
        """Test analyzing with slow functions"""
        _profiler.reset()
        
        # Track a slow function
        _profiler.track("slow_func", 2.0)
        
        analyzer = BottleneckAnalyzer(_profiler)
        result = analyzer.analyze()
        
        # Unwrap if wrapped
        analysis = result.get("result", result)
        
        assert analysis["success"] is True
        assert analysis["slow_functions"] == 1
        assert len(analysis["bottlenecks"]) > 0
    
    def test_get_report(self):
        """Test generating performance report"""
        _profiler.reset()
        
        _profiler.track("func1", 1.5)
        _profiler.track("func2", 0.5)
        
        analyzer = BottleneckAnalyzer(_profiler)
        result = analyzer.get_report()
        
        # @with_error_handling wraps result
        if isinstance(result, dict) and "result" in result:
            report = result["result"]
        else:
            report = result
        
        assert isinstance(report, str)
        assert "Performance Analysis Report" in report
        assert "func1" in report


# ============================================================================
# Integration Tests
# ============================================================================

class TestPerformanceIntegration:
    """Integration tests for performance module"""
    
    def test_profile_and_analyze(self):
        """Test profiling and analyzing together"""
        _profiler.reset()
        
        @profile
        def slow_function():
            time.sleep(0.01)
        
        @profile
        def fast_function():
            pass
        
        # Call functions
        slow_function()
        fast_function()
        
        # Analyze
        analyzer = BottleneckAnalyzer(_profiler)
        result = analyzer.analyze()
        
        # Unwrap if wrapped by @with_error_handling
        analysis = result.get("result", result)
        
        assert analysis["success"] is True
        assert analysis["total_functions"] >= 2
    
    def test_cache_and_profile(self):
        """Test caching with profiling"""
        _profiler.reset()
        cache = SimpleCache()
        
        @profile
        @cached(cache)
        def expensive_function(x):
            time.sleep(0.01)
            return x * 2
        
        # First call - slow
        result1 = expensive_function(5)
        
        # Second call - fast (cached)
        result2 = expensive_function(5)
        
        assert result1 == result2 == 10
        
        # Check metrics
        all_metrics = _profiler.get_metrics()
        assert len(all_metrics) > 0


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
