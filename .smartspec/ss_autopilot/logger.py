"""
Comprehensive logging system for SmartSpec Autopilot.

Features:
- Structured JSON logging
- Log rotation
- Performance metrics
- Integration with error_handler
"""

from __future__ import annotations

import logging
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from logging.handlers import RotatingFileHandler


class StructuredLogger:
    """Structured logger with JSON output and rotation"""
    
    def __init__(
        self,
        name: str,
        log_dir: str = ".smartspec/logs",
        log_level: str = "INFO",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """Initialize structured logger"""
        self.name = name
        self.log_dir = Path(log_dir)
        self.logger = logging.getLogger(name)
        
        # Set log level
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # Remove existing handlers
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
            file_handler.setFormatter(JsonFormatter())
            self.logger.addHandler(file_handler)
        except Exception:
            pass
        
        # Add console handler
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            self.logger.addHandler(console_handler)
        except Exception:
            pass
        
        self.logger.propagate = False
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra={"context": kwargs})
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra={"context": kwargs})
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra={"context": kwargs})
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra={"context": kwargs})
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra={"context": kwargs})
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, extra={"context": kwargs})


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
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
            
            if hasattr(record, 'context') and record.context:
                log_data["context"] = record.context
            
            if record.exc_info:
                log_data["exception"] = self.formatException(record.exc_info)
            
            return json.dumps(log_data, ensure_ascii=False)
        except Exception:
            return f"{record.levelname}: {record.getMessage()}"


# Global logger registry
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(name: str, log_level: str = "INFO") -> StructuredLogger:
    """Get or create logger instance"""
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name=name, log_level=log_level)
    return _loggers[name]
