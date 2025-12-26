"""
Performance Profiling Module for SmartSpec Autopilot

Provides comprehensive performance profiling and optimization:
- Function execution time tracking
- Memory usage monitoring
- Bottleneck identification
- Performance metrics collection
- Caching mechanisms
- Profiling decorators

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import time
import functools
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from collections import defaultdict
import threading
from .error_handler import with_error_handling


@dataclass
class PerformanceMetrics:
    """Performance metrics for a function"""
    function_name: str
    total_calls: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    last_call_time: float = 0.0
    
    def update(self, execution_time: float):
        """Update metrics with new execution time"""
        self.total_calls += 1
        self.total_time += execution_time
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.avg_time = self.total_time / self.total_calls
        self.last_call_time = execution_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "function_name": self.function_name,
            "total_calls": self.total_calls,
            "total_time": self.total_time,
            "min_time": self.min_time if self.min_time != float('inf') else 0.0,
            "max_time": self.max_time,
            "avg_time": self.avg_time,
            "last_call_time": self.last_call_time
        }


class PerformanceProfiler:
    """Performance profiler for tracking function execution"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize profiler"""
        if self._initialized:
            return
        
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.enabled = True
        self._lock = threading.Lock()
        self._initialized = True
    
    def track(self, function_name: str, execution_time: float):
        """
        Track function execution time.
        
        Args:
            function_name: Name of the function
            execution_time: Execution time in seconds
        """
        if not self.enabled:
            return
        
        with self._lock:
            if function_name not in self.metrics:
                self.metrics[function_name] = PerformanceMetrics(function_name)
            
            self.metrics[function_name].update(execution_time)
    
    def get_metrics(self, function_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get performance metrics.
        
        Args:
            function_name: Optional function name to get specific metrics
            
        Returns:
            Dict with metrics
        """
        with self._lock:
            if function_name:
                if function_name in self.metrics:
                    return self.metrics[function_name].to_dict()
                else:
                    return {"error": "Function not found"}
            else:
                return {
                    name: metrics.to_dict()
                    for name, metrics in self.metrics.items()
                }
    
    def get_bottlenecks(self, top_n: int = 10) -> list:
        """
        Get top N slowest functions.
        
        Args:
            top_n: Number of functions to return
            
        Returns:
            List of functions sorted by avg_time
        """
        with self._lock:
            sorted_metrics = sorted(
                self.metrics.values(),
                key=lambda m: m.avg_time,
                reverse=True
            )
            
            return [m.to_dict() for m in sorted_metrics[:top_n]]
    
    def reset(self, function_name: Optional[str] = None):
        """
        Reset metrics.
        
        Args:
            function_name: Optional function name to reset specific metrics
        """
        with self._lock:
            if function_name:
                if function_name in self.metrics:
                    del self.metrics[function_name]
            else:
                self.metrics.clear()
    
    def enable(self):
        """Enable profiling"""
        self.enabled = True
    
    def disable(self):
        """Disable profiling"""
        self.enabled = False


# Global profiler instance
_profiler = PerformanceProfiler()


def profile(func: Optional[Callable] = None, *, name: Optional[str] = None):
    """
    Decorator to profile function execution time.
    
    Args:
        func: Function to profile
        name: Optional custom name for the function
        
    Example:
        @profile
        def slow_function():
            time.sleep(1)
        
        @profile(name="custom_name")
        def another_function():
            pass
    """
    def decorator(f: Callable) -> Callable:
        function_name = name or f"{f.__module__}.{f.__name__}"
        
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                return result
            finally:
                execution_time = time.time() - start_time
                _profiler.track(function_name, execution_time)
        
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


class SimpleCache:
    """Simple in-memory cache with TTL support"""
    
    def __init__(self, max_size: int = 1000, ttl: Optional[int] = None):
        """
        Initialize cache.
        
        Args:
            max_size: Maximum number of items in cache
            ttl: Time to live in seconds (None = no expiration)
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, tuple] = {}  # key -> (value, timestamp)
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self.cache:
                return None
            
            value, timestamp = self.cache[key]
            
            # Check if expired
            if self.ttl and (time.time() - timestamp) > self.ttl:
                del self.cache[key]
                return None
            
            return value
    
    def set(self, key: str, value: Any):
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self._lock:
            # Evict oldest item if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                del self.cache[oldest_key]
            
            self.cache[key] = (value, time.time())
    
    def delete(self, key: str):
        """Delete key from cache"""
        with self._lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        with self._lock:
            self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "ttl": self.ttl,
                "usage_percent": (len(self.cache) / self.max_size * 100) if self.max_size > 0 else 0
            }


def cached(cache: SimpleCache, key_func: Optional[Callable] = None):
    """
    Decorator to cache function results.
    
    Args:
        cache: SimpleCache instance
        key_func: Optional function to generate cache key from args/kwargs
        
    Example:
        cache = SimpleCache(max_size=100, ttl=300)
        
        @cached(cache)
        def expensive_function(x, y):
            return x + y
        
        @cached(cache, key_func=lambda x: f"user_{x}")
        def get_user(user_id):
            return fetch_user(user_id)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: use function name + args
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


class BottleneckAnalyzer:
    """Analyzer for identifying performance bottlenecks"""
    
    def __init__(self, profiler: PerformanceProfiler = None):
        """
        Initialize analyzer.
        
        Args:
            profiler: PerformanceProfiler instance (uses global if None)
        """
        self.profiler = profiler or _profiler
    
    @with_error_handling
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze performance metrics and identify bottlenecks.
        
        Returns:
            Dict with analysis results
        """
        metrics = self.profiler.get_metrics()
        
        if not metrics:
            return {
                "success": True,
                "bottlenecks": [],
                "recommendations": ["No performance data collected yet"]
            }
        
        # Identify bottlenecks
        bottlenecks = []
        recommendations = []
        
        # Find slow functions (avg_time > 1 second)
        slow_functions = [
            m for m in metrics.values()
            if m.get("avg_time", 0) > 1.0
        ]
        
        if slow_functions:
            bottlenecks.extend(slow_functions)
            recommendations.append(
                f"พบ {len(slow_functions)} functions ที่ช้า (avg > 1s) - พิจารณา optimize หรือใช้ caching"
            )
        
        # Find frequently called functions (> 1000 calls)
        frequent_functions = [
            m for m in metrics.values()
            if m.get("total_calls", 0) > 1000
        ]
        
        if frequent_functions:
            recommendations.append(
                f"พบ {len(frequent_functions)} functions ที่ถูกเรียกบ่อย (> 1000 ครั้ง) - พิจารณาใช้ caching"
            )
        
        # Find functions with high variance (max_time > 10 * min_time)
        high_variance_functions = [
            m for m in metrics.values()
            if m.get("max_time", 0) > 10 * m.get("min_time", 1)
        ]
        
        if high_variance_functions:
            recommendations.append(
                f"พบ {len(high_variance_functions)} functions ที่มี variance สูง - ตรวจสอบ edge cases"
            )
        
        # Calculate total time spent
        total_time = sum(m.get("total_time", 0) for m in metrics.values())
        
        return {
            "success": True,
            "total_functions": len(metrics),
            "total_time": total_time,
            "bottlenecks": bottlenecks,
            "slow_functions": len(slow_functions),
            "frequent_functions": len(frequent_functions),
            "high_variance_functions": len(high_variance_functions),
            "recommendations": recommendations
        }
    
    @with_error_handling
    def get_report(self) -> str:
        """
        Generate performance report.
        
        Returns:
            Formatted report string
        """
        analysis_result = self.analyze()
        
        # @with_error_handling wraps result in {"success": True, "result": ...}
        if "result" in analysis_result:
            analysis = analysis_result["result"]
        else:
            analysis = analysis_result
        
        if not analysis.get("success"):
            return "Error generating report"
        
        report = []
        report.append("=" * 60)
        report.append("Performance Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"Total Functions Tracked: {analysis.get('total_functions', 0)}")
        report.append(f"Total Execution Time: {analysis.get('total_time', 0):.2f}s")
        report.append("")
        
        report.append("Bottlenecks:")
        report.append("-" * 60)
        
        bottlenecks = self.profiler.get_bottlenecks(top_n=10)
        for i, bottleneck in enumerate(bottlenecks, 1):
            report.append(f"{i}. {bottleneck['function_name']}")
            report.append(f"   Avg Time: {bottleneck['avg_time']:.4f}s")
            report.append(f"   Total Calls: {bottleneck['total_calls']}")
            report.append(f"   Total Time: {bottleneck['total_time']:.2f}s")
            report.append("")
        
        report.append("Recommendations:")
        report.append("-" * 60)
        for i, rec in enumerate(analysis['recommendations'], 1):
            report.append(f"{i}. {rec}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


# Export all
__all__ = [
    'PerformanceMetrics',
    'PerformanceProfiler',
    'profile',
    'SimpleCache',
    'cached',
    'BottleneckAnalyzer',
    '_profiler',  # Global profiler instance
]
