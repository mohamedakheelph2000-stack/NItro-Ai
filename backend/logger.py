# logger.py - Logging setup for Nitro AI Backend
# Logging helps us track what's happening in our application
# Think of it as a diary for your server

import logging
import sys

# Import with compatibility for both local and package mode
try:
    from .config import settings
except ImportError:
    from config import settings

def setup_logger(name: str = "nitro_ai") -> logging.Logger:
    """
    Create and configure a logger for the application.
    
    Logs help you debug issues and monitor your application.
    They appear in the terminal where you run the server.
    
    Args:
        name: Name of the logger (default: "nitro_ai")
    
    Returns:
        Configured logger instance
    """
    
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Don't duplicate logs if logger already has handlers
    if logger.handlers:
        return logger
    
    # Create console handler (prints logs to terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create a formatter (defines how logs look)
    # Format: [2026-02-17 10:30:00] INFO - Your log message here
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handler
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Create a logger instance to use throughout the app
logger = setup_logger()
