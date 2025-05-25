"""
Structured logging configuration for AGOR.

Provides consistent logging across all modules with structured output
suitable for multi-agent coordination and debugging.
"""

import logging
import sys

import structlog


def configure_logging(level: str = "INFO") -> structlog.BoundLogger:
    """Configure structured logging for AGOR.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=getattr(logging, level.upper())
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger(name: str = "agor") -> structlog.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name (typically module name)

    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)


# Default logger instance
log = get_logger()
