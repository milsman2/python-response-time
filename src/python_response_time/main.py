"""Main entry point for the Python Response Time application."""

import time

import requests
from rich.console import Console

from python_response_time.core import app_settings, setup_logger

console = Console()


def run_app():
    """Run HTTP benchmark and display results via Rich."""
    logger = setup_logger(app_settings.LOG_LEVEL)
    console.print("[bold cyan]HTTP Benchmark Starting...[/bold cyan]")
    console.print(f"Target: {app_settings.TARGET_URL}")
    console.print(f"Requests: {app_settings.NUM_REQUESTS}")
    console.print(f"Concurrency: {app_settings.CONCURRENCY}")
    console.print(f"Timeout: {app_settings.TIMEOUT}s")
    console.print(f"Delay: {app_settings.REQUEST_DELAY}s")
    console.print(f"SSL Verify: {app_settings.VERIFY_SSL}\n")

    session = requests.Session()

    console.print("[bold green]Running benchmark...[/bold green]\n")

    for i in range(app_settings.NUM_REQUESTS):
        start_time = time.perf_counter()
        try:
            response = session.get(
                str(app_settings.TARGET_URL),
                timeout=app_settings.TIMEOUT,
                verify=app_settings.VERIFY_SSL,
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                f"Request {i + 1}: {response.status_code} in {elapsed_ms:.2f} ms"
            )

        except requests.exceptions.SSLError as e:
            console.print(f"[red]Request {i + 1} SSL error: {e}[/red]")

        except requests.RequestException as e:
            console.print(f"[red]Request {i + 1} failed: {e}[/red]")

        finally:
            if app_settings.REQUEST_DELAY > 0:
                time.sleep(app_settings.REQUEST_DELAY)


if __name__ == "__main__":
    run_app()
