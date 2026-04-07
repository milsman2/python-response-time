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

| Variable         | Type   | Default                  | Description                                 |
|------------------|--------|--------------------------|---------------------------------------------|
| TARGET_URL       | str    | https://httpbin.org/get  | Target endpoint for benchmarking            |
| NUM_REQUESTS     | int    | 10                       | Total number of requests                    |
| CONNECT_TIMEOUT  | float  | 1.0                      | Connection timeout in seconds               |
| READ_TIMEOUT     | float  | 3.0                      | Request timeout in seconds                  |
| REQUEST_DELAY    | float  | 0.1                      | Delay between requests in seconds           |
| LOG_LEVEL        | str    | INFO                     | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| VERIFY_SSL       | bool   | True                     | Whether to verify SSL certificates          |

Example `.env`:

```
TARGET_URL=https://example.com/api
NUM_REQUESTS=100
CONNECT_TIMEOUT=2.0
READ_TIMEOUT=5.0
REQUEST_DELAY=0.5
LOG_LEVEL=DEBUG
VERIFY_SSL=False
```

## DevOps & Pythonic Practices

- **Pre-flight checks**: One command (`uv run checks`) runs ruff, isort, black, and pytest with coverage.
- **Strict config validation**: Pydantic v2 ensures all settings are valid before running.
- **Logging**: Loguru provides both human-friendly console logs and persistent file logs with rotation and compression.
- **Modern packaging**: Uses `pyproject.toml` for dependencies, scripts, and tool config.
- **CI/CD ready**: Semantic release and coverage tools are pre-configured.
- **Type annotations**: All code is type-annotated for clarity and safety.

tests/

## Architecture

### Graceful Shutdown & Signal Handling

- Signal handling is modular: the signal handler function is defined at module scope and can be reused or tested independently.
- `register_signals` simply registers this handler for SIGINT/SIGTERM, and the handler itself is not nested or dynamically created.
- This makes the shutdown logic more testable, maintainable, and explicit.

## Project Structure

```
src/python_response_time/
    main.py         # Benchmark runner, entry point, signal registration
    pre_flight.py   # DevOps checks
    core/
        config.py   # Pydantic v2 settings
        logging.py  # Loguru setup
        startup.py  # Signal handler and registration logic
tests/
    test_basic.py   # Pytest-based config tests
```

## CI/CD Pipeline

- Linting, testing, and Docker image build are triggered on every push and pull request.
- The pipeline is not affected by the signal handler refactor; no changes are required for this architectural update.
- See `.github/workflows/ci-cd.yaml` for details.

## License

MIT
