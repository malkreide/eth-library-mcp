"""
HTTP client layer for the ETH Library APIs.

Extracted from server.py per audit ARCH-004 (Inversion of Control). The
tool layer talks to the upstream APIs only through `_http_get`. Lifespan
management (SDK-001), egress allow-listing (SEC-021), API-key loading and
error normalisation all live here.
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import urlparse

import httpx

from eth_library_mcp.logging_config import get_logger

DISCOVERY_BASE_URL = "https://api.library.ethz.ch/discovery/v1"
PERSONS_BASE_URL = "https://api.library.ethz.ch/persons/v1"
REQUEST_TIMEOUT = 30.0

# SEC-021: Code-Layer Egress-Allow-List. Frozenset so a compromised tool
# cannot mutate the list at runtime. Documented in docs/network-egress.md.
ALLOWED_EGRESS_HOSTS: frozenset[str] = frozenset({"api.library.ethz.ch"})

# SDK-001: Shared httpx.AsyncClient managed by the FastMCP lifespan. When
# the module is imported outside a server context (e.g. unit tests), the
# client falls back to a per-call instance.
_http_client: httpx.AsyncClient | None = None

log = get_logger(__name__)


def _get_api_key() -> str | None:
    """API-Key aus Umgebungsvariable lesen (graceful degradation)."""
    return os.environ.get("ETH_LIBRARY_API_KEY")


def _check_egress_allowed(url: str) -> None:
    """SEC-021: Verifiziert, dass der Host in der Egress-Allow-List steht."""
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_EGRESS_HOSTS:
        raise PermissionError(
            f"Egress denied: host {host!r} not in ALLOWED_EGRESS_HOSTS"
        )


async def _http_get(
    base_url: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Zentrale Funktion für alle ETH-Bibliothek API-Anfragen.
    Fügt automatisch den API-Key hinzu und behandelt Fehler konsistent.
    """
    api_key = _get_api_key()

    request_params: dict[str, Any] = params or {}
    if api_key:
        request_params["apikey"] = api_key

    url = f"{base_url}{path}"
    _check_egress_allowed(url)

    log.debug("upstream_request", url=url, has_key=api_key is not None)

    if _http_client is not None:
        response = await _http_client.get(url, params=request_params)
        response.raise_for_status()
        return response.json()

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, params=request_params)
        response.raise_for_status()
        return response.json()


@asynccontextmanager
async def lifespan(_server):
    """SDK-001: pooled httpx.AsyncClient for the server's lifetime."""
    global _http_client
    log.info("server_starting", transport="any")
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        _http_client = client
        try:
            yield {}
        finally:
            _http_client = None
            log.info("server_stopping")
