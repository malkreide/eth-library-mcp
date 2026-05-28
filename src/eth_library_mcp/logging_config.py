"""
OBS-003: Structured JSON logging on stderr.

stdio-Transport (default) reserves stdout for the JSON-RPC protocol, so all
logs go to stderr. Structured JSON output makes the logs ingestible by
log shippers (Datadog, CloudWatch, Loki) without per-source parsers.

Severity levels actually used by this server:
- debug:   per-request URL + param dump (off by default)
- info:    server lifecycle (lifespan startup/shutdown)
- warning: degraded but recoverable upstream behaviour
- error:   unhandled exception classes inside _handle_error
"""

from __future__ import annotations

import logging
import sys

import structlog


def configure_logging(level: str = "INFO") -> None:
    """Idempotently configure stderr-bound structlog with JSON output."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, level.upper(), logging.INFO),
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "eth_library_mcp") -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
