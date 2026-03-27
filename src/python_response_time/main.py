"""Main entry point for the Python Response Time application."""

import time

import requests
from loguru import logger

from python_response_time.core import app_settings, setup_logger

setup_logger(app_settings.LOG_LEVEL)


def run_app():
    """Run a simple HTTP benchmark against the configured target URL."""
    logger.info(f"Target URL: {app_settings.TARGET_URL}")
    logger.info(f"Number of Requests: {app_settings.NUM_REQUESTS}")
    logger.info(f"Concurrency: {app_settings.CONCURRENCY}")
    logger.info(f"Timeout: {app_settings.TIMEOUT} seconds")
    logger.info(f"Request Delay: {app_settings.REQUEST_DELAY} seconds")
    logger.info(f"SSL Verify: {app_settings.VERIFY_SSL}")

    session = requests.Session()

    logger.info("Starting HTTP benchmark...")

    for i in range(app_settings.NUM_REQUESTS):
        start_time = time.time()

        try:
            response = session.get(
                str(app_settings.TARGET_URL),
                timeout=app_settings.TIMEOUT,
                verify=app_settings.VERIFY_SSL,
            )
            response.raise_for_status()

            elapsed_time_ms = (time.time() - start_time) * 1000
            logger.info(
                f"Request {i + 1}: {response.status_code} - {elapsed_time_ms:.2f} ms"
            )

        except requests.exceptions.SSLError as e:
            logger.error(f"Request {i + 1} SSL error: {e}")

        except requests.RequestException as e:
            logger.error(f"Request {i + 1} failed: {e}")

        finally:
            if app_settings.REQUEST_DELAY > 0:
                time.sleep(app_settings.REQUEST_DELAY)


if __name__ == "__main__":
    run_app()
