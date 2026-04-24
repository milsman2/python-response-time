"""Tests for config settings in python_response_time.core."""

from python_response_time.core import app_settings


def test_target_urls():
    """TARGET_URL should be a non-empty string starting with http(s)."""
    urls = app_settings.TARGET_URL
    assert isinstance(urls, list)
    assert all(isinstance(url, str) for url in urls)
    assert all(url.startswith("http") for url in urls)
    assert all(len(url) > 0 for url in urls)


def test_num_requests():
    """NUM_REQUESTS should be an int > 0 and <= 1_000_000."""
    n = app_settings.NUM_REQUESTS
    assert isinstance(n, int)
    assert 0 < n <= 1_000_000


def test_log_level():
    """LOG_LEVEL should be a valid log level string."""
    level = app_settings.LOG_LEVEL
    assert level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
