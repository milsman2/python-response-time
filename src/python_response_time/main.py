"""Python Response Time Benchmark (production-safe, Docker/K8s friendly)."""

import signal
import threading
import time

import requests
from loguru import logger
from rich.console import Console

from python_response_time.core import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    app_settings,
    setup_logger,
    start_metrics_server,
)

setup_logger(app_settings.LOG_LEVEL)
console = Console()

shutdown_event = threading.Event()


def handle_shutdown(*_):
    """Handle SIGTERM / SIGINT."""
    shutdown_event.set()
    console.print("\n[yellow]Shutdown signal received... stopping gracefully[/yellow]")


def register_signals():
    """Register signal handlers for graceful shutdown."""
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)


def sleep_interruptible(seconds: float):
    """Sleep in small increments, checking for shutdown signal."""
    step = 0.1
    elapsed = 0.0

    while elapsed < seconds:
        if shutdown_event.is_set():
            return
        try:
            time.sleep(step)
        except KeyboardInterrupt:
            shutdown_event.set()
            return
        elapsed += step


def run_app():
    """Run the main application logic."""
    console.print("[bold cyan]HTTP Benchmark Starting...[/bold cyan]")
    console.print(f"Target: {app_settings.TARGET_URL}")
    console.print(f"Requests: {app_settings.NUM_REQUESTS}")
    console.print(f"Concurrency: {app_settings.CONCURRENCY}")
    console.print(f"Timeout: {app_settings.TIMEOUT}s")
    console.print(f"Delay: {app_settings.REQUEST_DELAY}s")
    console.print(f"SSL Verify: {app_settings.VERIFY_SSL}\n")

    session = requests.Session()

    try:
        for i in range(app_settings.NUM_REQUESTS):
            if shutdown_event.is_set():
                break
            start_time = time.perf_counter()
            try:
                response = session.get(
                    str(app_settings.TARGET_URL),
                    timeout=app_settings.TIMEOUT,
                    verify=app_settings.VERIFY_SSL,
                )
                elapsed = time.perf_counter() - start_time
                console.print(
                    f"{i + 1:>4} | {response.status_code} | {elapsed * 1000:.2f} ms"
                )
                logger.info(
                    {
                        "request": i + 1,
                        "status": response.status_code,
                        "response_time_ms": elapsed * 1000,
                        "url": str(app_settings.TARGET_URL),
                    }
                )
                REQUEST_COUNT.labels(status=str(response.status_code)).inc()
                REQUEST_LATENCY.observe(elapsed)
            except requests.exceptions.SSLError as e:
                console.print(f"{i + 1:>4} | SSL ERROR")
                logger.error(
                    {
                        "request": i + 1,
                        "error": "ssl_error",
                        "details": str(e),
                    }
                )
            except requests.RequestException as e:
                REQUEST_COUNT.labels(status="error").inc()
                console.print(f"{i + 1:>4} | ERROR")
                logger.error(
                    {
                        "request": i + 1,
                        "error": "request_error",
                        "details": str(e),
                    }
                )
            if app_settings.REQUEST_DELAY > 0:
                sleep_interruptible(app_settings.REQUEST_DELAY)
    finally:
        session.close()
        console.print("\n[green]Benchmark stopped gracefully[/green]")


if __name__ == "__main__":
    """Run the application."""
    register_signals()
    start_metrics_server(port=8000)
    try:
        run_app()
    except KeyboardInterrupt:
        shutdown_event.set()
        console.print("\n[yellow]Interrupted (Ctrl+C). Exiting cleanly...[/yellow]")
    finally:
        shutdown_event.set()
        console.print("[green]Cleanup complete[/green]")
