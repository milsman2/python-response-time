"""Loguru logger configuration for python-app-template."""

import sys
from typing import Any, cast

from loguru import logger

from python_response_time.core.config import app_settings


def setup_logger(level: str = "INFO") -> Any:
    """Configure the Loguru logger."""
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
    return cast(Any, logger)
