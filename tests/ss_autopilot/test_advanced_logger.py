"""
Unit tests for advanced_logger.py

Tests:
- LogContext
- AdvancedLogger basic logging
- Request tracing
- Performance metrics
- Context managers
- Structured JSON formatting
"""

import pytest
import time
import json
from pathlib import Path

# Import from the module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".smartspec"))

from ss_autopilot.advanced_logger import (
    LogContext,
    AdvancedLogger,
    StructuredJsonFormatter,
    get_logger
)


# ============================================================================
# Helper Functions
# ============================================================================

def unwrap(result):
    """Unwrap result from @with_error_handling decorator"""
    if isinstance(result, dict) and "result" in result:
        return result["result"]
    return result


# ============================================================================
# Test LogContext
# ============================================================================

class TestLogContext:
    """Test LogContext class"""
    
    def test_log_context_creation(self):
        """Test creating log context"""
        context = LogContext(
            correlation_id="corr-123",
            request_id="req-456",
            user_id="user-789"
        )
        
        assert context.correlation_id == "corr-123"
        assert context.request_id == "req-456"
        assert context.user_id == "user-789"
    
    def test_log_context_to_dict(self):
        """Test converting log context to dict"""
        context = LogContext(
            correlation_id="corr-123",
            metadata={"key": "value"}
        )
        
        data = context.to_dict()
        
        assert data["correlation_id"] == "corr-123"
        assert data["metadata"]["key"] == "value"
        assert "elapsed_time" in data


# ============================================================================
# Test AdvancedLogger
# ============================================================================

class TestAdvancedLogger:
    """Test AdvancedLogger class"""
    
    def test_logger_creation(self):
        """Test creating advanced logger"""
        logger = AdvancedLogger(
            name="test_logger",
            log_dir="/tmp/test_logs"
        )
        
        assert logger.name == "test_logger"
        assert logger.enable_metrics is True
    
    def test_basic_logging(self):
        """Test basic logging methods"""
        logger = AdvancedLogger(name="test_basic")
        
        # Should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_logging_with_context(self):
        """Test logging with additional context"""
        logger = AdvancedLogger(name="test_context")
        
        logger.info("Test message", user_id="user-123", action="login")
        # Should not raise exceptions
    
    def test_exception_logging(self):
        """Test exception logging"""
        logger = AdvancedLogger(name="test_exception")
        
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.exception("An error occurred")
        # Should not raise exceptions


# ============================================================================
# Test Performance Metrics
# ============================================================================

class TestPerformanceMetrics:
    """Test performance metrics logging"""
    
    def test_metric_logging(self):
        """Test logging metrics"""
        logger = AdvancedLogger(name="test_metrics", enable_metrics=True)
        
        logger.metric("response_time", 0.5)
        logger.metric("response_time", 0.7)
        logger.metric("response_time", 0.3)
        
        stats = unwrap(logger.get_metrics("response_time"))
        
        assert stats["count"] == 3
        assert stats["min"] == 0.3
        assert stats["max"] == 0.7
        assert stats["avg"] == pytest.approx(0.5, rel=0.1)
    
    def test_multiple_metrics(self):
        """Test tracking multiple metrics"""
        logger = AdvancedLogger(name="test_multi_metrics", enable_metrics=True)
        
        logger.metric("metric_a", 10)
        logger.metric("metric_b", 20)
        
        all_stats = unwrap(logger.get_metrics())
        
        assert "metric_a" in all_stats
        assert "metric_b" in all_stats
        assert all_stats["metric_a"]["count"] == 1
        assert all_stats["metric_b"]["count"] == 1
    
    def test_metrics_disabled(self):
        """Test metrics when disabled"""
        logger = AdvancedLogger(name="test_no_metrics", enable_metrics=False)
        
        logger.metric("test_metric", 100)
        
        # Should not track metrics
        assert len(logger.metrics) == 0


# ============================================================================
# Test Context Managers
# ============================================================================

class TestContextManagers:
    """Test context managers for scoped logging"""
    
    def test_trace_context(self):
        """Test trace context manager"""
        logger = AdvancedLogger(name="test_trace", enable_metrics=True)
        
        with logger.trace("test_operation", param="value") as context:
            assert context.correlation_id is not None
            assert context.metadata["operation"] == "test_operation"
            time.sleep(0.01)  # Simulate work
        
        # Check metrics were logged
        stats = unwrap(logger.get_metrics("test_operation_duration"))
        assert stats["count"] == 1
        assert stats["min"] > 0
    
    def test_trace_with_exception(self):
        """Test trace context with exception"""
        logger = AdvancedLogger(name="test_trace_error")
        
        with pytest.raises(ValueError):
            with logger.trace("failing_operation"):
                raise ValueError("Test error")
    
    def test_request_context(self):
        """Test request context manager"""
        logger = AdvancedLogger(name="test_request")
        
        with logger.request_context(
            request_id="req-123",
            user_id="user-456"
        ) as context:
            assert context.request_id == "req-123"
            assert context.user_id == "user-456"
            
            # Log within context
            logger.info("Processing request")
    
    def test_nested_contexts(self):
        """Test nested context managers"""
        logger = AdvancedLogger(name="test_nested")
        
        with logger.request_context(request_id="req-123"):
            logger.info("Outer context")
            
            with logger.trace("inner_operation"):
                logger.info("Inner context")


# ============================================================================
# Test get_logger
# ============================================================================

class TestGetLogger:
    """Test get_logger function"""
    
    def test_get_logger(self):
        """Test getting logger instance"""
        logger1 = get_logger("test_get")
        logger2 = get_logger("test_get")
        
        # Should return same instance
        assert logger1 is logger2
    
    def test_get_logger_with_options(self):
        """Test getting logger with options"""
        logger = get_logger(
            "test_options",
            log_level="DEBUG",
            enable_metrics=False
        )
        
        assert logger.name == "test_options"
        assert logger.enable_metrics is False


# ============================================================================
# Integration Tests
# ============================================================================

class TestAdvancedLoggerIntegration:
    """Integration tests for advanced logger"""
    
    def test_full_workflow(self):
        """Test complete logging workflow"""
        logger = AdvancedLogger(name="test_workflow", enable_metrics=True)
        
        # Request context
        with logger.request_context(request_id="req-001", user_id="user-001"):
            logger.info("Request started")
            
            # Trace operation
            with logger.trace("database_query", table="users"):
                time.sleep(0.01)
                logger.info("Query executed")
            
            # Log metric
            logger.metric("request_size", 1024)
            
            logger.info("Request completed")
        
        # Check metrics
        stats = unwrap(logger.get_metrics())
        assert "database_query_duration" in stats
        assert "request_size" in stats
    
    def test_concurrent_logging(self):
        """Test logging from multiple threads"""
        import threading
        
        logger = AdvancedLogger(name="test_concurrent", enable_metrics=True)
        
        def worker(worker_id):
            with logger.request_context(user_id=f"user-{worker_id}"):
                logger.info(f"Worker {worker_id} started")
                time.sleep(0.01)
                logger.metric("worker_time", 0.01)
                logger.info(f"Worker {worker_id} completed")
        
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Check metrics
        stats = unwrap(logger.get_metrics("worker_time"))
        assert stats["count"] == 5


# ============================================================================
# Pytest Markers
# ============================================================================

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit
