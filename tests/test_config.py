"""Unit tests for config.py in python_response_time.core."""

from typing import Any, cast

import pytest
from pydantic import ValidationError

from python_response_time.core import config


def test_default_values(monkeypatch):
    """Test default configuration values."""
    monkeypatch.delenv("TARGET_URL", raising=False)
    monkeypatch.delenv("NUM_REQUESTS", raising=False)
    monkeypatch.delenv("CONNECT_TIMEOUT", raising=False)
    monkeypatch.delenv("READ_TIMEOUT", raising=False)
    monkeypatch.delenv("REQUEST_DELAY", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("VERIFY_SSL", raising=False)
    monkeypatch.delenv("LOG_TO_STDOUT", raising=False)
    monkeypatch.delenv("METRICS_PORT", raising=False)

    class TestSettings(config.Settings):
        model_config = config.SettingsConfigDict(
            env_file=None,
        )

    s = TestSettings()

    assert s.LOG_TO_STDOUT is True
    assert s.TARGET_URL == [
        "https://httpbin.org/get",
        "https://httpbin.org/status/200",
    ]
    assert s.NUM_REQUESTS == 10
    assert s.CONNECT_TIMEOUT == 1.0
    assert s.READ_TIMEOUT == 3.0
    assert s.REQUEST_DELAY == 2.0
    assert s.LOG_LEVEL == "INFO"
    assert s.VERIFY_SSL is True
    assert s.METRICS_PORT == 8000


def test_app_settings_instance():
    """Test that the module-level settings object exists."""
    assert isinstance(config.app_settings, config.Settings)


def test_env_override_num_requests(monkeypatch):
    """Test environment variable override for integer values."""
    monkeypatch.setenv("NUM_REQUESTS", "42")

    s = config.Settings()

    assert s.NUM_REQUESTS == 42


def test_env_override_metrics_port(monkeypatch):
    """Test environment variable override for METRICS_PORT."""
    monkeypatch.setenv("METRICS_PORT", "9100")

    s = config.Settings()

    assert s.METRICS_PORT == 9100


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        ("true", True),
        ("false", False),
        ("1", True),
        ("0", False),
        ("yes", True),
        ("no", False),
    ],
)
def test_bool_env_parsing(monkeypatch, env_value, expected):
    """Test boolean parsing from environment variables."""
    monkeypatch.setenv("VERIFY_SSL", env_value)

    s = config.Settings()

    assert s.VERIFY_SSL is expected


def test_log_to_stdout_env_parsing(monkeypatch):
    """Test LOG_TO_STDOUT boolean parsing from environment variable."""
    monkeypatch.setenv("LOG_TO_STDOUT", "true")

    s = config.Settings()

    assert s.LOG_TO_STDOUT is True


def test_target_url_env_override(monkeypatch):
    """Test TARGET_URL parsing from environment variable."""
    monkeypatch.setenv(
        "TARGET_URL",
        '["https://example.com", "https://test.com"]',
    )

    s = config.Settings()

    assert s.TARGET_URL == [
        "https://example.com",
        "https://test.com",
    ]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("NUM_REQUESTS", 0),
        ("NUM_REQUESTS", -1),
        ("NUM_REQUESTS", 1_000_001),
        ("CONNECT_TIMEOUT", 0),
        ("CONNECT_TIMEOUT", -1),
        ("CONNECT_TIMEOUT", 121),
        ("READ_TIMEOUT", 0),
        ("READ_TIMEOUT", -5),
        ("READ_TIMEOUT", 121),
        ("REQUEST_DELAY", 0),
        ("REQUEST_DELAY", -1),
        ("REQUEST_DELAY", 61),
    ],
)
def test_invalid_numeric_values(field, value):
    """Test numeric validation boundaries."""
    with pytest.raises(ValidationError):
        config.Settings(**{field: value})


@pytest.mark.parametrize(
    "value",
    [
        "debug",
        "trace",
        "INVALID",
        "",
        "info",
        "warn",
    ],
)
def test_invalid_log_level(value):
    """Test invalid LOG_LEVEL values."""
    with pytest.raises(ValidationError):
        config.Settings(LOG_LEVEL=value)


@pytest.mark.parametrize(
    "value",
    [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ],
)
def test_valid_log_levels(value):
    """Test valid LOG_LEVEL values."""
    s = config.Settings(LOG_LEVEL=value)

    assert s.LOG_LEVEL == value


def test_invalid_env_value(monkeypatch):
    """Test invalid environment variable values raise errors."""
    monkeypatch.setenv("NUM_REQUESTS", "not-an-int")

    with pytest.raises(ValidationError):
        config.Settings()


def test_extra_fields_forbidden():
    """Test that extra fields are rejected."""
    with pytest.raises(ValidationError):
        config.Settings(**cast(Any, {"UNKNOWN_FIELD": "bad"}))


def test_invalid_target_url_type():
    """Test invalid TARGET_URL type."""
    with pytest.raises(ValidationError):
        config.Settings(TARGET_URL=cast(Any, "not-a-list"))


def test_invalid_target_url_item_type():
    """Test invalid TARGET_URL list item types."""
    with pytest.raises(ValidationError):
        config.Settings(TARGET_URL=cast(Any, [123, 456]))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("NUM_REQUESTS", 1),
        ("NUM_REQUESTS", 1_000_000),
        ("CONNECT_TIMEOUT", 0.001),
        ("CONNECT_TIMEOUT", 120),
        ("READ_TIMEOUT", 0.001),
        ("READ_TIMEOUT", 120),
        ("REQUEST_DELAY", 0.001),
        ("REQUEST_DELAY", 60),
    ],
)
def test_valid_numeric_boundaries(field, value):
    """Test valid numeric boundary values."""
    s = config.Settings(**{field: value})

    assert getattr(s, field) == value


def test_settings_are_isolated():
    """Test separate Settings instances do not share state."""
    s1 = config.Settings(NUM_REQUESTS=10)
    s2 = config.Settings(NUM_REQUESTS=20)

    assert s1.NUM_REQUESTS == 10
    assert s2.NUM_REQUESTS == 20


def test_model_config_values():
    """Test important model configuration values."""
    cfg = config.Settings.model_config

    assert cfg.get("extra") == "forbid"
    assert cfg.get("validate_default") is True
    assert cfg.get("env_file") == ".env"
    assert cfg.get("env_file_encoding") == "utf-8"
