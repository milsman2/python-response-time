"""Loguru logger configuration for python-app-template."""

import sys

from loguru import logger


def setup_logger(level: str = "INFO"):
    """Configure and return a Loguru logger instance.

    Args:
        level (str, optional): Logging level for file outputs (e.g., "INFO", "DEBUG",
            "ERROR"). Defaults to "INFO".

    Returns:
        logger: Configured Loguru logger instance.

    """
    from .config import app_settings

    logger.remove()
    if not getattr(app_settings, "LOG_TO_STDOUT", True):
        logger.add(
            "app.log",
            serialize=True,
            level=level,
            rotation="1 MB",
            retention="10 days",
            compression="zip",
        )
    else:
        logger.add(
            sys.stdout,
            serialize=True,
            level=level,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
        logger.add(
            "app.log",
            serialize=True,
            level=level,
            rotation="1 MB",
            retention="10 days",
            compression="zip",
        )
    return logger
