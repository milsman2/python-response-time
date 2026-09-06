# python-response-time

A small, Pythonic HTTP benchmark for measuring response latency against one or more endpoints while exposing Prometheus metrics and handling shutdown signals cleanly.

## What it does

This project runs a sequential HTTP benchmark against configured URLs and prints timing information for each request. It also starts a Prometheus metrics server so you can scrape request counts and latency histograms.

Key behaviors:

- Sends requests to a configurable list of target URLs
- Validates settings with Pydantic v2
- Logs structured events with Loguru
- Supports graceful shutdown on SIGINT and SIGTERM
- Exposes metrics on a local Prometheus endpoint
- Provides a `checks` command for linting and test validation

## Features

- Configurable benchmark settings via environment variables or a `.env` file
- Multi-target benchmarking using `TARGET_URL` as a list of endpoints
- Timeout controls for connection and read phases
- Optional request delay between iterations
- Prometheus metrics for request totals and latency distribution
- Structured console logging with log level control
- DevOps smoke checks via a dedicated script entry point

## Quickstart

Install the project in editable mode:

```bash
python -m pip install -e '.[build]'
```

Run the benchmark:

```bash
python-response-time
```

Or with `uv`:

```bash
uv pip install -e '.[build]'
uv run python-response-time
```

Run the project validation checks:

```bash
uv run checks
```

## Configuration

Settings are defined in `src/python_response_time/core/config.py` and are loaded from environment variables or a `.env` file. Values are validated at startup.

| Variable | Type | Default | Description |
|---|---:|---:|---|
| `LOG_TO_STDOUT` | bool | `true` | Whether to emit logs to stdout |
| `TARGET_URL` | list[str] | `["https://httpbin.org/get", "https://httpbin.org/status/200"]` | Target endpoints for benchmarking |
| `NUM_REQUESTS` | int | `10` | Total number of requests to send for each URL |
| `CONNECT_TIMEOUT` | float | `1.0` | Connection timeout in seconds |
| `READ_TIMEOUT` | float | `3.0` | Read timeout in seconds |
| `REQUEST_DELAY` | float | `2.0` | Delay between requests in seconds |
| `LOG_LEVEL` | str | `INFO` | Supported values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `VERIFY_SSL` | bool | `true` | Whether to verify SSL certificates |
| `METRICS_PORT` | int | `8000` | Port for the Prometheus metrics endpoint |

Example `.env`:

```env
LOG_TO_STDOUT=true
TARGET_URL=["https://example.com", "https://example.com/api"]
NUM_REQUESTS=25
CONNECT_TIMEOUT=2.0
READ_TIMEOUT=5.0
REQUEST_DELAY=0.5
LOG_LEVEL=DEBUG
VERIFY_SSL=false
METRICS_PORT=8000
```

> `TARGET_URL` is parsed as a list. Use valid JSON array syntax when setting it in the environment or `.env` file.

## Metrics

When the application starts, it exposes Prometheus metrics on `http://localhost:8000/metrics` by default.

The metrics include:

- Request counts by HTTP status or timeout category
- Request latency distribution by status code

## Behavior notes

- The benchmark loops sequentially through each URL in `TARGET_URL`.
- It exits early when a shutdown event is triggered.
- A Kubernetes-safe interruptible sleep is used between requests to allow fast, graceful shutdown.
- Any connection timeout, read timeout, SSL error, or request error is recorded and reported without crashing the whole run.

## Development and checks

The project exposes a `checks` script defined in `pyproject.toml`:

```bash
uv run checks
```

This runs:

1. `ruff check . --fix`
2. `black .`
3. `ruff check .`
4. `coverage run -m pytest`

## Project structure

```text
src/
  python_response_time/
    __init__.py
    main.py
    pre_flight.py
    core/
      __init__.py
      config.py
      logging.py
      metrics.py
      startup.py
tests/
  test_basic.py
  test_config.py
```

## License

MIT
