"""
Logging infrastructure for the Scheduling Assistant application.
Provides centralized logging with file rotation, console output, and structured logging.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import colorlog
from datetime import datetime


class SchedulingLogger:
    """
    Centralized logging system for the Scheduling Assistant.
    
    Features:
    - Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - File rotation (10MB per file, keep 5 backup files)
    - Colored console output
    - Structured logging with context
    - Separate logs for different components (app, agents, negotiations, errors)
    """
    
    def __init__(self, log_dir: str = "logs", app_name: str = "SchedulingAssistant"):
        """
        Initialize the logging system.
        
        Args:
            log_dir: Directory to store log files
            app_name: Name of the application for log identification
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.app_name = app_name
        
        # Create loggers for different components
        self.app_logger = self._setup_logger("app", "app.log", logging.INFO)
        self.agent_logger = self._setup_logger("agents", "agents.log", logging.DEBUG)
        self.negotiation_logger = self._setup_logger("negotiations", "negotiations.log", logging.INFO)
        self.error_logger = self._setup_logger("errors", "errors.log", logging.ERROR)
        
    def _setup_logger(self, name: str, filename: str, level: int) -> logging.Logger:
        """
        Set up a logger with file and console handlers.
        
        Args:
            name: Logger name
            filename: Log file name
            level: Minimum log level
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(f"{self.app_name}.{name}")
        logger.setLevel(logging.DEBUG)  # Capture all levels, handlers will filter
        
        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / filename,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler with colors
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(level)
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def log_app(self, message: str, level: str = "INFO", **kwargs):
        """Log application-level events."""
        self._log(self.app_logger, message, level, **kwargs)
    
    def log_agent(self, agent_name: str, action: str, details: dict, level: str = "DEBUG"):
        """Log agent-specific actions."""
        message = f"[{agent_name}] {action}"
        if details:
            message += f" | {details}"
        self._log(self.agent_logger, message, level)
    
    def log_negotiation(self, round_num: int, event: str, details: dict, level: str = "INFO"):
        """Log negotiation events."""
        message = f"Round {round_num} | {event}"
        if details:
            message += f" | {details}"
        self._log(self.negotiation_logger, message, level)
    
    def log_error(self, error: Exception, context: dict = None, level: str = "ERROR"):
        """Log errors with full context."""
        message = f"Error: {type(error).__name__}: {str(error)}"
        if context:
            message += f" | Context: {context}"
        self._log(self.error_logger, message, level)
        
        # Also log to app logger for visibility
        self._log(self.app_logger, message, "ERROR")
    
    def _log(self, logger: logging.Logger, message: str, level: str, **kwargs):
        """Internal method to log with specified level."""
        level_map = {
            "DEBUG": logger.debug,
            "INFO": logger.info,
            "WARNING": logger.warning,
            "ERROR": logger.error,
            "CRITICAL": logger.critical
        }
        log_func = level_map.get(level.upper(), logger.info)
        
        # Add extra context if provided
        if kwargs:
            message += f" | {kwargs}"
        
        log_func(message)
    
    def log_performance(self, operation: str, duration_ms: float, details: dict = None):
        """Log performance metrics."""
        message = f"Performance | {operation} | {duration_ms:.2f}ms"
        if details:
            message += f" | {details}"
        self.log_app(message, level="INFO")
    
    def log_user_action(self, action: str, user_id: str = "default", details: dict = None):
        """Log user interactions with the UI."""
        message = f"User Action | {user_id} | {action}"
        if details:
            message += f" | {details}"
        self.log_app(message, level="INFO")
    
    def get_logger(self, component: str) -> logging.Logger:
        """
        Get a specific logger by component name.
        
        Args:
            component: One of 'app', 'agents', 'negotiations', 'errors'
            
        Returns:
            Logger instance
        """
        loggers = {
            "app": self.app_logger,
            "agents": self.agent_logger,
            "negotiations": self.negotiation_logger,
            "errors": self.error_logger
        }
        return loggers.get(component, self.app_logger)


# Global logger instance
_global_logger: Optional[SchedulingLogger] = None


def get_logger() -> SchedulingLogger:
    """Get or create the global logger instance."""
    global _global_logger
    if _global_logger is None:
        _global_logger = SchedulingLogger()
    return _global_logger


def init_logger(log_dir: str = "logs", app_name: str = "SchedulingAssistant") -> SchedulingLogger:
    """
    Initialize the global logger with custom settings.
    
    Args:
        log_dir: Directory to store log files
        app_name: Name of the application
        
    Returns:
        Configured logger instance
    """
    global _global_logger
    _global_logger = SchedulingLogger(log_dir=log_dir, app_name=app_name)
    return _global_logger
