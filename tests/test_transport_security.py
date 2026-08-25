"""SEC-005, eingehende Haelfte: Host- und Origin-Pruefung des Transports.

`build_http_app` uebergab weder `transport_security=` noch `host=`. Das ist
nicht «ungeschuetzt», sondern **falsch geschuetzt**: `streamable_http_app`
synthetisiert bei fehlendem `transport_security` und Loopback-`host` selbst
eine Freigabeliste (`mcp/server/mcpserver/server.py`), und die kennt nur
Loopback.

Gemessen am zusammengebauten Stack, mit `ETH_LIBRARY_CORS_ORIGINS` gesetzt:

    Host 127.0.0.1:8000, Origin https://client.example -> 403 Invalid Origin
    Host testserver,     Origin https://client.example -> 421 Invalid Host
    Host mcp.example.ch, ohne Origin                   -> 421 Invalid Host

Die Variable war damit wirkungslos — CORS liess durch, das SDK wies ab.

**Warum die CORS-Suite das nicht finden konnte:** sie schickt ausschliesslich
Preflights, und die beantwortet `CORSMiddleware`, bevor die App ueberhaupt
erreicht wird. Eine Zusicherung ueber die Transportschicht braucht eine echte
Anfrage. Jeder Test hier schickt deshalb ein echtes `initialize`.
"""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from eth_library_mcp.server import build_http_app, build_transport_security

ORIGIN = "https://client.example"

INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-11-25",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"},
    },
}
HEADERS = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}


@pytest.fixture(autouse=True)
def _saubere_umgebung(monkeypatch: pytest.MonkeyPatch):
    """Beide Variablen pro Test aus der Umgebung nehmen.

    Ohne das haengt das Ergebnis daran, was die Testumgebung zufaellig gesetzt
    hat — ein Test, der von aussen umgestellt werden kann, misst nicht den Code.
    """
    monkeypatch.delenv("ETH_LIBRARY_CORS_ORIGINS", raising=False)
    monkeypatch.delenv("ETH_LIBRARY_ALLOWED_HOSTS", raising=False)


def _initialize(app, base_url: str, origin: str | None = None) -> int:
    kopf = dict(HEADERS)
    if origin is not None:
        kopf["Origin"] = origin
    with TestClient(app, base_url=base_url) as c:
        return c.post("/mcp", json=INIT, headers=kopf).status_code


# ── Der eigentliche Fix ─────────────────────────────────────────────────────


def test_die_konfigurierte_origin_kommt_durch_den_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Das ist der Befund. Vorher 403, weil die SDK-Liste nur Loopback kannte."""
    monkeypatch.setenv("ETH_LIBRARY_CORS_ORIGINS", ORIGIN)
    app = build_http_app("127.0.0.1", 8000)
    assert _initialize(app, "http://127.0.0.1:8000", ORIGIN) == 200


def test_eine_nicht_konfigurierte_origin_wird_abgewiesen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Die Gegenkontrolle. Ohne sie waere der Test darueber auch gegen eine
    Transportschicht gruen, die jede Origin durchwinkt — was die Pruefung
    abschaffen wuerde, statt sie zu reparieren."""
    monkeypatch.setenv("ETH_LIBRARY_CORS_ORIGINS", ORIGIN)
    app = build_http_app("127.0.0.1", 8000)
    assert _initialize(app, "http://127.0.0.1:8000", "https://woanders.example") == 403


def test_ein_echter_hostname_braucht_die_allowlist() -> None:
    """Der zweite Befund: `--host 0.0.0.0` ist in README.md dokumentiert und
    antwortete auf jede Anfrage 421, weil `host=` nicht durchgereicht wurde."""
    app = build_http_app("0.0.0.0", 8000)  # noqa: S104 — der dokumentierte Fall
    # Ohne ETH_LIBRARY_ALLOWED_HOSTS gibt es nichts zu raten: Schutz aus,
    # aber erreichbar — statt einer geratenen Liste, die das 421 reproduziert.
    assert _initialize(app, "http://mcp.example.ch") == 200


def test_mit_allowlist_bleibt_der_schutz_an(monkeypatch: pytest.MonkeyPatch) -> None:
    """Je Anfrage eine frische App: der `StreamableHTTPSessionManager` einer
    App laesst sich nur einmal starten, ein zweites `TestClient`-Lifespan auf
    demselben Objekt stirbt an seinem eigenen RuntimeError statt am Hostnamen —
    der Test haette dann nicht gemessen, was er behauptet."""
    monkeypatch.setenv("ETH_LIBRARY_ALLOWED_HOSTS", "mcp.example.ch")
    assert _initialize(build_http_app("0.0.0.0", 8000), "http://mcp.example.ch") == 200  # noqa: S104
    # Und die Gegenkontrolle: ein fremder Name faellt jetzt durch.
    assert _initialize(build_http_app("0.0.0.0", 8000), "http://fremd.example") == 421  # noqa: S104


# ── Die Freigabeliste selbst ────────────────────────────────────────────────


def test_wildcard_bind_ohne_allowlist_schaltet_den_schutz_ab() -> None:
    """Auf 0.0.0.0 ist der erreichbare Name unbekannt, und der
    SDK-Loopback-Default ist genau eine Vermutung — er reproduziert das 421."""
    assert build_transport_security("0.0.0.0", 8000) is None  # noqa: S104


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1"])
def test_alle_loopback_formen_zaehlen_als_lokal(host: str) -> None:
    assert build_transport_security(host, 8000) is not None


def test_die_konfigurierten_origins_stehen_in_der_liste(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ETH_LIBRARY_CORS_ORIGINS", "https://a.test,*")
    sec = build_transport_security("127.0.0.1", 8000)
    assert sec is not None
    assert "https://a.test" in sec.allowed_origins
    # `*` ist hier nicht ausdrueckbar: Origins werden literal verglichen.
    # Literal uebernommen waere es ein Eintrag, der nichts erlaubt.
    assert "*" not in sec.allowed_origins


def test_loopback_bleibt_neben_der_allowlist_erreichbar(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sonst brechen Container-Health-Checks, die auf 127.0.0.1 sprechen."""
    monkeypatch.setenv("ETH_LIBRARY_ALLOWED_HOSTS", "mcp.example.ch")
    sec = build_transport_security("0.0.0.0", 8000)  # noqa: S104
    assert sec is not None
    assert "mcp.example.ch" in sec.allowed_hosts
    assert "127.0.0.1:8000" in sec.allowed_hosts
