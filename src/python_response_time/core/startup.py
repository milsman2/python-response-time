"""Startup utilities: signal handling and interruptible sleep (K8s-safe)."""

import signal
import time
from functools import partial
from threading import Event
from types import FrameType

from loguru import logger
from rich.console import Console


def handle_shutdown(
    signum: int,
    frame: FrameType | None,
    shutdown_event: Event,
    console: Console,
) -> None:
    """Handle SIGTERM / SIGINT (idempotent)."""
    if shutdown_event.is_set():
        return
    shutdown_event.set()
    console.print("\n[yellow]Shutdown signal received... stopping gracefully[/yellow]")
    logger.warning(
        {
            "event": "shutdown",
            "signal": signum,
        }
    )
    logger.debug(f"Signal frame: {frame}")


def _handler(
    signum: int,
    frame: FrameType | None,
    shutdown_event: Event,
    console: Console,
) -> None:
    """Thin wrapper to adapt signal handler signature."""
    handle_shutdown(signum, frame, shutdown_event, console)


def register_signals(shutdown_event: Event, console: Console) -> None:
    """Register signal handlers for graceful shutdown."""
    handler = partial(
        _handler,
        shutdown_event=shutdown_event,
        console=console,
    )

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def sleep_interruptible(seconds: float, shutdown_event: Event) -> None:
    """Sleep in small increments, exiting early if shutdown is triggered.

    K8s-safe: ensures fast shutdown (<100ms granularity)
    """
    step = 0.05
    end = time.monotonic() + seconds

    while time.monotonic() < end:
        if shutdown_event.is_set():
            return
        time.sleep(step)
