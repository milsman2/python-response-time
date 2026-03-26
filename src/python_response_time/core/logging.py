"""Loguru logger configuration for python-app-template."""

import sys

from loguru import logger

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


def setup_logger(level: str = "INFO"):
    """Configure and return a Loguru logger instance.

    Args:
        level (str, optional): Logging level for file outputs (e.g., "INFO", "DEBUG",
            "ERROR"). Defaults to "INFO".

    Returns:
        logger: Configured Loguru logger instance.

    """
    logger.remove()
    if level.upper() == "SILENT":
        logger.add(
            "app.log",
            format=log_format,
            level="ERROR",
            rotation="1 MB",
            retention="10 days",
            compression="zip",
        )
    else:
        logger.add(
            sys.stdout,
            format=log_format,
            level=level,
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
        logger.add(
            "app.log",
            format=log_format,
            level=level,
            rotation="1 MB",
            retention="10 days",
            compression="zip",
        )
    return logger
