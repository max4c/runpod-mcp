"""
Logging configuration for RunPod MCP.
"""

import os
import logging
import logging.handlers
import sys
from typing import Optional, Dict, Any

def configure_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> None:
    """Configure logging for the MCP server.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (default: None, logs to stderr)
        log_format: Log format string (default: timestamp, level, name, message)
    """
    if log_format is None:
        log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Configure console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Configure file handler if log_file is provided
    if log_file:
        os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set levels for third-party libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    # Log initial message
    logging.info(f"Logging configured with level {logging.getLevelName(level)}")
    if log_file:
        logging.info(f"Logging to file: {log_file}")
    
def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name) 