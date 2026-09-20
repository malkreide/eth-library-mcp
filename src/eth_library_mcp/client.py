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

from . import __version__

# Wer fragt hier an? Ohne eigenen User-Agent geht der httpx-Default
# hinaus und der Betreiber der Datenquelle sieht bloss eine Bibliothek.
# Die Version stammt aus den Paket-Metadaten und kann nicht driften.
USER_AGENT = f"eth-library-mcp/{__version__} (+https://github.com/malkreide/eth-library-mcp)"
DISCOVERY_BASE_URL = "https://api.library.ethz.ch/discovery/v1"
PERSONS_BASE_URL = "https://api.library.ethz.ch/persons/v1"
REQUEST_TIMEOUT = 30.0

# SEC-021: Code-Layer Egress-Allow-List. Frozenset so a compromised tool
# cannot mutate the list at runtime. Documented in docs/network-egress.md.
ALLOWED_EGRESS_HOSTS: frozenset[str] = frozenset({"api.library.ethz.ch"})

# SDK-001: Shared httpx.AsyncClient managed by the MCPServer lifespan. When
# the module is imported outside a server context (e.g. unit tests), the
# client falls back to a per-call instance.
_http_client: httpx.AsyncClient | None = None

log = get_logger(__name__)


def _get_api_key() -> str | None:
    """API-Key aus Umgebungsvariable lesen (graceful degradation)."""
    return os.environ.get("ETH_LIBRARY_API_KEY")


class EgressError(PermissionError):
    """Basis für jede Abweisung durch den Egress-Guard (SEC-028).

    `retryable` ist der **Diskriminator**: ein Feld, das Code liest. Nicht der
    Meldungstext — der bricht bei der ersten Umformulierung und ist bei
    Lokalisierung sofort falsch.

    Die Basisklasse bleibt `PermissionError`, damit ein bestehendes
    `except PermissionError` um den Guard herum weiter greift. Die
    Unterscheidung entsteht eine Ebene darunter, nicht durch Wegnehmen.
    """

    retryable: bool = False


class EgressPolicyViolation(EgressError):
    """Der Zielhost steht nicht in `ALLOWED_EGRESS_HOSTS`. Deterministisch.

    Wiederholt sich beliebig oft gleich: Die Allow-List ist eine
    Konfigurationsentscheidung dieses Servers und keine Aussage über die
    Erreichbarkeit der Quelle. Ein Wiederholungsrat wäre hier falsch — siehe
    `formatting._handle_error`, das genau an `retryable` entscheidet.
    """

    retryable = False

    def __init__(self, host: str) -> None:
        self.host = host
        super().__init__(f"Egress denied: host {host!r} not in ALLOWED_EGRESS_HOSTS")


# Was hier bewusst NICHT steht: ein `EgressResolutionError` für die transiente
# Lage aus SEC-028. Dieser Guard löst nichts auf — er vergleicht den Hostnamen
# aus der URL gegen ein `frozenset`. Ein DNS-Aussetzer erreicht den Aufrufer
# deshalb als `httpx.ConnectError` bzw. `httpx.TimeoutException`, und beide
# haben in `_handle_error` längst ihren eigenen Zweig. Eine Klasse ohne
# Gegenstand anzulegen wäre die Fixture, die die Annahme ihres Autors kodiert
# und sie nicht widerlegen kann: Kein Test könnte sie je auslösen.


def _check_egress_allowed(url: str) -> None:
    """SEC-021: Verifiziert, dass der Host in der Egress-Allow-List steht."""
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_EGRESS_HOSTS:
        raise EgressPolicyViolation(host)


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

    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}
    ) as client:
        response = await client.get(url, params=request_params)
        response.raise_for_status()
        return response.json()


@asynccontextmanager
async def lifespan(_server):
    """SDK-001: pooled httpx.AsyncClient for the server's lifetime."""
    global _http_client
    log.info("server_starting", transport="any")
    async with httpx.AsyncClient(
        timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}
    ) as client:
        _http_client = client
        try:
            yield {}
        finally:
            _http_client = None
            log.info("server_stopping")
