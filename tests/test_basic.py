"""Tests for config settings in python_response_time.core."""

from python_response_time.core import app_settings


def test_target_url():
    """TARGET_URL should be a non-empty string starting with http(s)."""
    url = app_settings.TARGET_URL
    assert isinstance(url, str)
    assert url.startswith("http")
    assert len(url) > 0


def test_num_requests():
    """NUM_REQUESTS should be an int > 0 and <= 1_000_000."""
    n = app_settings.NUM_REQUESTS
    assert isinstance(n, int)
    assert 0 < n <= 1_000_000


def test_log_level():
    """LOG_LEVEL should be a valid log level string."""
    level = app_settings.LOG_LEVEL
    assert level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
