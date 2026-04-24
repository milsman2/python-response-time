"""Configuration settings for the HTTP benchmark."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the HTTP benchmark."""

    LOG_TO_STDOUT: Annotated[
        bool, Field(description="Whether to log to stdout (console)", strict=False)
    ] = True

    TARGET_URL: Annotated[
        list[str], Field(description="List of target endpoints for benchmarking")
    ] = ["https://httpbin.org/get", "https://httpbin.org/status/200"]
    NUM_REQUESTS: Annotated[
        int, Field(gt=0, le=1_000_000, description="Total number of requests")
    ] = 10
    CONNECT_TIMEOUT: Annotated[
        float, Field(gt=0, le=120, description="Connection timeout in seconds")
    ] = 1.0
    READ_TIMEOUT: Annotated[
        float, Field(gt=0, le=120, description="Request timeout in seconds")
    ] = 3.0
    REQUEST_DELAY: Annotated[
        float, Field(gt=0, le=60, description="Delay between requests in seconds")
    ] = 2.0
    LOG_LEVEL: Annotated[
        str, Field(pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    ] = "INFO"
    VERIFY_SSL: Annotated[
        bool, Field(description="Whether to verify SSL certificates")
    ] = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        validate_default=True,
    )


app_settings = Settings()
