"""Core metrics for the application."""

from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["status"])

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["status"],
    buckets=(0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)


def start_metrics_server(port: int = 8000):
    """Start the Prometheus metrics server."""
    start_http_server(port)
