"""Run the Python Response Time Benchmark (K8s-safe, single-threaded)."""

import threading
import time
from threading import Event

from loguru import logger
from requests import Session
from requests.exceptions import ConnectTimeout, ReadTimeout, RequestException, SSLError
from rich.console import Console

from python_response_time.core import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    app_settings,
    register_signals,
    setup_logger,
    sleep_interruptible,
    start_metrics_server,
)


def run_app(console: Console, shutdown_event: Event) -> None:
    """Run the main benchmark loop."""
    console.print("[bold cyan]HTTP Benchmark Starting...[/bold cyan]")
    console.print(f"Target: {app_settings.TARGET_URL}")
    console.print(f"Requests: {app_settings.NUM_REQUESTS}")
    console.print(f"Delay: {app_settings.REQUEST_DELAY}s")
    console.print(f"SSL Verify: {app_settings.VERIFY_SSL}\n")

    session = Session()

    try:
        for i in range(app_settings.NUM_REQUESTS):
            if shutdown_event.is_set():
                break
            request_id = i + 1
            logger.info({"event": "request_start", "request": request_id})
            start_time = time.perf_counter()
            try:
                response = session.get(
                    str(app_settings.TARGET_URL),
                    timeout=(
                        app_settings.CONNECT_TIMEOUT,
                        app_settings.READ_TIMEOUT,
                    ),
                    verify=app_settings.VERIFY_SSL,
                )
                elapsed = time.perf_counter() - start_time
                console.print(
                    f"{request_id:>4} | "
                    f"{response.status_code} | "
                    f"{elapsed * 1000:.2f} ms"
                )
                logger.info(
                    {
                        "event": "request_complete",
                        "request": request_id,
                        "status": response.status_code,
                        "response_time_ms": elapsed * 1000,
                    }
                )
                REQUEST_COUNT.labels(status=str(response.status_code)).inc()
                REQUEST_LATENCY.labels(status=str(response.status_code)).observe(
                    elapsed
                )
            except ConnectTimeout:
                console.print(f"{request_id:>4} | CONNECT_TIMEOUT")
                logger.warning(
                    {
                        "event": "connect_timeout",
                        "request": request_id,
                    }
                )
                REQUEST_COUNT.labels(status="connect_timeout").inc()
            except ReadTimeout:
                console.print(f"{request_id:>4} | READ_TIMEOUT")
                logger.warning(
                    {
                        "event": "read_timeout",
                        "request": request_id,
                    }
                )
                REQUEST_COUNT.labels(status="read_timeout").inc()
            except SSLError as e:
                console.print(f"{request_id:>4} | SSL_ERROR")
                logger.error(
                    {
                        "event": "ssl_error",
                        "request": request_id,
                        "details": str(e),
                    }
                )
                REQUEST_COUNT.labels(status="ssl_error").inc()
            except RequestException as e:
                console.print(f"{request_id:>4} | ERROR")
                logger.error(
                    {
                        "event": "request_error",
                        "request": request_id,
                        "details": str(e),
                    }
                )
                REQUEST_COUNT.labels(status="error").inc()
            if app_settings.REQUEST_DELAY > 0:
                sleep_interruptible(app_settings.REQUEST_DELAY, shutdown_event)
    finally:
        session.close()
        console.print("\n[green]Benchmark stopped gracefully[/green]")


def main() -> None:
    """Application entrypoint."""
    setup_logger(app_settings.LOG_LEVEL)
    console = Console()
    shutdown_event = threading.Event()
    register_signals(shutdown_event, console)
    start_metrics_server(port=8000)
    try:
        run_app(console, shutdown_event)
    finally:
        shutdown_event.set()
        console.print("[green]Cleanup complete[/green]")


if __name__ == "__main__":
    main()
