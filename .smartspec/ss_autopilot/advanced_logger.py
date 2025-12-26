"""
Advanced Logging Module for SmartSpec Autopilot

Provides advanced logging features:
- Structured JSON logging
- Request tracing with correlation IDs
- Performance metrics logging
- Context managers for scoped logging
- Log aggregation support
- Distributed tracing

Author: SmartSpec Team
Date: 2025-12-26
Version: 1.0.0
"""

import logging
import json
import time
import uuid
import threading
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .error_handler import with_error_handling


# Thread-local storage for correlation ID
_thread_local = threading.local()


@dataclass
class LogContext:
    """Log context with correlation ID and metadata"""
    correlation_id: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    start_time: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "correlation_id": self.correlation_id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "metadata": self.metadata,
            "elapsed_time": time.time() - self.start_time
        }


class AdvancedLogger:
    """Advanced logger with structured logging and tracing"""
    
    def __init__(
        self,
        name: str,
        log_dir: str = ".smartspec/logs",
        log_level: str = "INFO",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        enable_metrics: bool = True
    ):
        """
        Initialize advanced logger.
        
        Args:
            name: Logger name
            log_dir: Log directory path
            log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            max_bytes: Max log file size before rotation
            backup_count: Number of backup files to keep
            enable_metrics: Enable performance metrics logging
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.enable_metrics = enable_metrics
        
        # Create logger
        self.logger = logging.getLogger(name)
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        self.logger.handlers = []
        
        # Create log directory
        try:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        
        # Add file handler with rotation
        try:
            log_file = self.log_dir / f"{name}.log"
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(StructuredJsonFormatter())
            self.logger.addHandler(file_handler)
        except Exception:
            pass
        
        # Metrics tracking
        self.metrics: Dict[str, List[float]] = {}
        self._metrics_lock = threading.Lock()
        
        self.logger.propagate = False
    
    def _get_context(self) -> Optional[LogContext]:
        """Get current log context from thread-local storage"""
        return getattr(_thread_local, 'context', None)
    
    def _set_context(self, context: LogContext):
        """Set log context in thread-local storage"""
        _thread_local.context = context
    
    def _clear_context(self):
        """Clear log context from thread-local storage"""
        if hasattr(_thread_local, 'context'):
            delattr(_thread_local, 'context')
    
    @with_error_handling
    def log(
        self,
        level: str,
        message: str,
        **kwargs
    ):
        """
        Log message with context.
        
        Args:
            level: Log level (debug, info, warning, error, critical)
            message: Log message
            **kwargs: Additional context
        """
        context = self._get_context()
        
        extra = {
            "context": kwargs,
            "log_context": context.to_dict() if context else None
        }
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.log("debug", message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.log("info", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.log("warning", message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.log("error", message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.log("critical", message, **kwargs)
    
    @with_error_handling
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        context = self._get_context()
        
        extra = {
            "context": kwargs,
            "log_context": context.to_dict() if context else None
        }
        
        self.logger.exception(message, extra=extra)
    
    @with_error_handling
    def metric(self, name: str, value: float, **kwargs):
        """
        Log performance metric.
        
        Args:
            name: Metric name
            value: Metric value
            **kwargs: Additional metadata
        """
        if not self.enable_metrics:
            return
        
        with self._metrics_lock:
            if name not in self.metrics:
                self.metrics[name] = []
            self.metrics[name].append(value)
        
        self.info(
            f"Metric: {name}",
            metric_name=name,
            metric_value=value,
            **kwargs
        )
    
    @with_error_handling
    def get_metrics(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get metrics statistics.
        
        Args:
            name: Optional metric name, or all if None
            
        Returns:
            Dict with metrics statistics
        """
        with self._metrics_lock:
            if name:
                if name not in self.metrics:
                    return {"error": f"Metric {name} not found"}
                
                values = self.metrics[name]
                return {
                    "name": name,
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "total": sum(values)
                }
            else:
                return {
                    metric_name: {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "total": sum(values)
                    }
                    for metric_name, values in self.metrics.items()
                }
    
    @contextmanager
    def trace(
        self,
        operation: str,
        **metadata
    ):
        """
        Context manager for tracing operations.
        
        Args:
            operation: Operation name
            **metadata: Additional metadata
            
        Usage:
            with logger.trace("database_query", table="users"):
                # operation code
                pass
        """
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        
        # Create context
        context = LogContext(
            correlation_id=correlation_id,
            metadata={"operation": operation, **metadata}
        )
        
        # Set context
        self._set_context(context)
        
        # Log start
        self.info(f"START: {operation}", **metadata)
        
        start_time = time.time()
        
        try:
            yield context
            
            # Log success
            elapsed = time.time() - start_time
            self.info(
                f"END: {operation}",
                elapsed_time=elapsed,
                status="success",
                **metadata
            )
            
            # Log metric
            if self.enable_metrics:
                self.metric(f"{operation}_duration", elapsed)
        
        except Exception as e:
            # Log error
            elapsed = time.time() - start_time
            self.error(
                f"ERROR: {operation}",
                elapsed_time=elapsed,
                status="error",
                error=str(e),
                **metadata
            )
            raise
        
        finally:
            # Clear context
            self._clear_context()
    
    @contextmanager
    def request_context(
        self,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        **metadata
    ):
        """
        Context manager for request-scoped logging.
        
        Args:
            request_id: Optional request ID
            user_id: Optional user ID
            session_id: Optional session ID
            **metadata: Additional metadata
            
        Usage:
            with logger.request_context(request_id="req-123", user_id="user-456"):
                # request handling code
                logger.info("Processing request")
        """
        # Generate IDs if not provided
        correlation_id = str(uuid.uuid4())
        request_id = request_id or str(uuid.uuid4())
        
        # Create context
        context = LogContext(
            correlation_id=correlation_id,
            request_id=request_id,
            user_id=user_id,
            session_id=session_id,
            metadata=metadata
        )
        
        # Set context
        self._set_context(context)
        
        try:
            yield context
        finally:
            # Clear context
            self._clear_context()


class StructuredJsonFormatter(logging.Formatter):
    """Enhanced JSON formatter with correlation ID support"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        try:
            log_data = {
                "timestamp": datetime.fromtimestamp(record.created).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }
            
            # Add context if present
            if hasattr(record, 'context') and record.context:
                log_data["context"] = record.context
            
            # Add log context (correlation ID, etc.)
            if hasattr(record, 'log_context') and record.log_context:
                log_data["trace"] = record.log_context
            
            # Add exception if present
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_data, ensure_ascii=False)
        
        except Exception:
            return f"{record.levelname}: {record.getMessage()}"


# Global logger registry
_loggers: Dict[str, AdvancedLogger] = {}
_lock = threading.Lock()


def get_logger(
    name: str,
    log_level: str = "INFO",
    enable_metrics: bool = True
) -> AdvancedLogger:
    """
    Get or create advanced logger instance.
    
    Args:
        name: Logger name
        log_level: Log level
        enable_metrics: Enable performance metrics
        
    Returns:
        AdvancedLogger instance
    """
    with _lock:
        if name not in _loggers:
            _loggers[name] = AdvancedLogger(
                name=name,
                log_level=log_level,
                enable_metrics=enable_metrics
            )
        return _loggers[name]


# Export all
__all__ = [
    'LogContext',
    'AdvancedLogger',
    'StructuredJsonFormatter',
    'get_logger',
]
