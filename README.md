# python-response-time

A Pythonic, DevOps-friendly HTTP benchmarking tool leveraging Pydantic v2 for robust configuration, Loguru for structured logging, and a modern, testable workflow.

## Features

- **Configurable HTTP benchmarking** via environment variables or `.env` file (Pydantic v2 + pydantic-settings)
- **Structured logging** with Loguru (console and file, colorized, with rotation)
- **Pre-flight DevOps checks**: auto-formatting, linting, and test coverage in one command
- **Modern Python packaging**: `pyproject.toml`-based, ready for CI/CD
- **Type-safe, validated settings**: all config is validated at startup
- **Tested and type-checked**: includes pytest-based tests for all config
- **CLI entrypoints** for both benchmarking and checks

## Quickstart

```bash
# Install with all dev dependencies
uv pip install -e '.[build]'

# Run the HTTP benchmark
uv run python-response-time

# Run all pre-flight DevOps checks (format, lint, test)
uv run checks
```

## Configuration

All settings are managed with Pydantic v2 and can be set via environment variables or a `.env` file:

| Variable      | Type   | Default                  | Description                        |
|---------------|--------|--------------------------|------------------------------------|
| TARGET_URL    | str    | https://httpbin.org/get  | Target endpoint for benchmarking   |
| NUM_REQUESTS  | int    | 10                       | Total number of requests           |
| CONCURRENCY   | int    | 2                        | Number of concurrent requests      |
| TIMEOUT       | float  | 10.0                     | Request timeout (seconds)          |
| LOG_LEVEL     | str    | INFO                     | Log level (DEBUG, INFO, etc.)      |

Example `.env`:

```
TARGET_URL=https://example.com/api
NUM_REQUESTS=100
CONCURRENCY=5
TIMEOUT=5.0
LOG_LEVEL=DEBUG
```

## DevOps & Pythonic Practices

- **Pre-flight checks**: One command (`uv run checks`) runs ruff, isort, black, and pytest with coverage.
- **Strict config validation**: Pydantic v2 ensures all settings are valid before running.
- **Logging**: Loguru provides both human-friendly console logs and persistent file logs with rotation and compression.
- **Modern packaging**: Uses `pyproject.toml` for dependencies, scripts, and tool config.
- **CI/CD ready**: Semantic release and coverage tools are pre-configured.
- **Type annotations**: All code is type-annotated for clarity and safety.

## Project Structure

```
src/python_response_time/
    main.py         # Benchmark runner
    pre_flight.py   # DevOps checks
    core/
        config.py   # Pydantic v2 settings
        logging.py  # Loguru setup
tests/
    test_basic.py   # Pytest-based config tests
```

## License

MIT
