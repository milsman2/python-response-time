"""Configuration settings for the HTTP benchmark."""

from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the HTTP benchmark."""

    TARGET_URL: Annotated[
        str, Field(description="Target endpoint for benchmarking")
    ] = "https://httpbin.org/get"
    NUM_REQUESTS: Annotated[
        int, Field(gt=0, le=1_000_000, description="Total number of requests")
    ] = 10
    CONCURRENCY: Annotated[
        int, Field(gt=0, le=10_000, description="Concurrent requests")
    ] = 1
    TIMEOUT: Annotated[
        float, Field(gt=0, le=120, description="Request timeout in seconds")
    ] = 10.0
    REQUEST_DELAY: Annotated[
        float, Field(gt=0, le=60, description="Delay between requests in seconds")
    ] = 0.1
    LOG_LEVEL: Annotated[
        str, Field(pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    ] = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",
        validate_default=True,
    )


app_settings = Settings()
