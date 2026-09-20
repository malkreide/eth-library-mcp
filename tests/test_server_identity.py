"""Spec 2026-07-28: die Identitaet, die dieser Server in jede Antwort stempelt.

Die Revision fuehrt `_meta.io.modelcontextprotocol/serverInfo` ein (spec
#3002): **jedes** Resultat der modernen Aera traegt den `Implementation`-Block,
nicht mehr nur der `initialize`-Handshake wie in den Aeren davor. Damit wird
aus einem einmaligen Feld eine Angabe, die der Server bei jedem Aufruf
wiederholt — und `version` ist im `Implementation` dieser Revision ein
Pflichtfeld.

Das SDK fuellt es nicht. `mcp/server/lowlevel/server.py::server_info` sagt es
selbst: «An unversioned server reports an empty `version`; the SDK never
substitutes its own». Gemessen am zusammengebauten ASGI-Stack antwortete
dieser Server vor dieser Datei mit `"version": ""` — in beiden Aeren, bei jedem
Aufruf, waehrend `server.json` der Registry `0.3.4` meldete. Das Manifest sagte
mehr ueber den Server aus als der Server selbst.

Gemessen statt zurueckgelesen: die Zusicherungen fahren einen echten
POST durch `build_http_app()`. Ein Blick auf `mcp.version` waere auch dann
gruen, wenn das Argument am Konstruktor verlorenginge oder das SDK den Stempel
gar nicht setzte — genau die Klasse Fehler, die dieses Repo schon einmal mit
einem Konstanten-Pin statt einer Messung hatte.
"""

from __future__ import annotations

import json
import pathlib
import tomllib
from importlib.metadata import version as _distribution_version
from typing import Any

import httpx
from mcp.server.mcpserver import MCPServer
from mcp_types import (
    CLIENT_CAPABILITIES_META_KEY,
    PROTOCOL_VERSION_META_KEY,
    SERVER_INFO_META_KEY,
)

from eth_library_mcp import DESCRIPTION, HOMEPAGE_URL
from eth_library_mcp.server import SERVER_TITLE, build_http_app

REPO = pathlib.Path(__file__).resolve().parents[1]

# Die moderne Revision. Bewusst hier wiederholt und nicht aus dem SDK gezogen:
# faellt diese Datei, weil das SDK weitergezogen ist, soll sie es sagen — und
# `tests/test_protocol_version.py` haelt den Pin selbst.
MODERN = "2026-07-28"


def _envelope(method: str) -> dict[str, Any]:
    """Der Pro-Request-Envelope der modernen Aera.

    Die beiden `_meta`-Schluessel sind Pflicht; ohne sie routet das SDK die
    Anfrage gar nicht erst modern (`mcp/shared/inbound.py`, Sprosse 1).
    """
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "_meta": {
                PROTOCOL_VERSION_META_KEY: MODERN,
                CLIENT_CAPABILITIES_META_KEY: {},
            }
        },
    }


def _unwrap(response: httpx.Response) -> dict[str, Any]:
    """JSON aus der Antwort, SSE-Rahmen abgestreift, falls vorhanden."""
    body = response.text
    for line in body.splitlines():
        if line.startswith("data: "):
            body = line[len("data: ") :]
    return json.loads(body)


async def _modern_result(method: str) -> dict[str, Any]:
    """Ein moderner Request durch den echten ASGI-Stack, `result` zurueck.

    `Mcp-Protocol-Version` und `Mcp-Method` muessen den Envelope spiegeln,
    sonst antwortet das SDK mit HEADER_MISMATCH statt mit einem Resultat —
    die Header sind Teil der Revision, nicht Beiwerk.
    """
    app = build_http_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://127.0.0.1:8000"
        ) as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "Host": "127.0.0.1:8000",
                    "MCP-Protocol-Version": MODERN,
                    "Mcp-Method": method,
                },
                json=_envelope(method),
            )
    payload = _unwrap(response)
    assert "result" in payload, f"{method} antwortete mit {payload!r}"
    return payload["result"]


async def _modern_server_info(method: str) -> dict[str, Any]:
    result = await _modern_result(method)
    stamp = result.get("_meta", {}).get(SERVER_INFO_META_KEY)
    assert stamp is not None, (
        f"{method} trug keinen {SERVER_INFO_META_KEY}-Stempel; Spec 2026-07-28 "
        "verlangt ihn auf jedem Resultat der modernen Aera"
    )
    return stamp


# ─── Der lasttragende Fall ───────────────────────────────────────────────────


async def test_der_stempel_nennt_die_installierte_version() -> None:
    """Der Befund, gegen den diese Datei geschrieben ist.

    `version` ist im `Implementation` der Revision Pflicht, und der Server
    meldete den leeren String. Verglichen wird gegen die Distributions-
    Metadaten, nicht gegen ein Literal: ein Literal hier wuerde dieselbe Drift
    festschreiben, die `tests/test_server.py::test_import_version` schon einmal
    festgeschrieben hat.
    """
    info = await _modern_server_info("tools/list")

    assert info.get("version") == _distribution_version("eth-library-mcp"), (
        f"der Stempel meldet version={info.get('version')!r}. Ein leerer Wert "
        "heisst: `version=` fehlt am `MCPServer`-Konstruktor — das SDK setzt "
        "nichts ein."
    )


async def test_der_stempel_steht_auf_einer_gewoehnlichen_methode() -> None:
    """Die Neuerung der Revision, benannt.

    Vor 2026-07-28 stand die Identitaet nur im `initialize`-Resultat. Ein Test
    nur auf `server/discover` waere auch gegen einen Server gruen, der sie
    weiterhin bloss an einer Stelle fuehrt. `tools/list` ist der Gegenbeweis:
    eine Methode, die es in beiden Aeren gibt.
    """
    info = await _modern_server_info("tools/list")

    # Verglichen wird gegen den Distributionsnamen, nicht gegen ein Literal.
    # Bis zum 20.9.2026 stand hier `eth_library_mcp` -- der Modulpfad, nicht
    # der Name, unter dem dieser Server zu beziehen ist. Ein Literal haette
    # die Abweichung mitgepflegt statt sie zu melden; genau diese Klasse
    # Fehler hat `test_import_version` in diesem Repo schon einmal
    # festgeschrieben.
    assert info.get("name") == _pyproject()["name"]


async def test_auch_die_auskunftsmethode_traegt_die_identitaet() -> None:
    """`server/discover` ist die Methode, die die Revision neu einfuehrt —
    und die erste, die ein Client ohne Handshake aufruft."""
    info = await _modern_server_info("server/discover")

    assert info.get("version") == _distribution_version("eth-library-mcp")


async def test_auch_der_handshake_traegt_die_identitaet() -> None:
    """Die Identitaet ist nicht auf die moderne Aera beschraenkt.

    `Implementation` fuehrt `version` in beiden Aeren, und das `initialize`-
    Resultat baut es aus denselben Konstruktor-Argumenten. Ohne diese
    Zusicherung koennte der Fix still auf «nur modern» zurueckfallen — die
    Tests oben blieben gruen, waehrend jeder heutige Client wieder die leere
    Version saehe. Gemessen ueber dieselbe Revision, die
    `tests/test_protocol_version.py` als Obergrenze pinnt.
    """
    app = build_http_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://127.0.0.1:8000"
        ) as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "Host": "127.0.0.1:8000",
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2025-11-25",
                        "capabilities": {},
                        "clientInfo": {"name": "legacy-client", "version": "1"},
                    },
                },
            )
    info = _unwrap(response)["result"]["serverInfo"]

    assert info.get("version") == _distribution_version("eth-library-mcp")
    assert info.get("title") == SERVER_TITLE


# ─── Negativkontrolle ────────────────────────────────────────────────────────


async def test_ein_server_ohne_identitaet_meldet_die_leere_version() -> None:
    """Gleiches SDK, gleicher Stack, kein `version=`.

    Ohne diese Zeile sagen die Tests oben nicht, dass WIR die Version setzen —
    sie waeren auch an dem Tag gruen, an dem das SDK selbst eine einsetzt. Dann
    naemlich pruefen sie das SDK und nicht diesen Server. Faellt dieser Test,
    ist genau das passiert und die Zusicherungen oben sind neu zu bewerten.
    """
    kontrolle = MCPServer("kontrolle")
    app = kontrolle.streamable_http_app(host="127.0.0.1")
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://127.0.0.1:8000"
        ) as client:
            response = await client.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "Host": "127.0.0.1:8000",
                    "MCP-Protocol-Version": MODERN,
                    "Mcp-Method": "tools/list",
                },
                json=_envelope("tools/list"),
            )
    stamp = _unwrap(response)["result"]["_meta"][SERVER_INFO_META_KEY]

    assert stamp.get("version") == "", (
        "das SDK setzt inzwischen selbst eine Version ein; die Zusicherungen "
        "oben messen damit nicht mehr, dass dieser Server sie setzt"
    )


# ─── Die uebrigen Identitaetsfelder ──────────────────────────────────────────


async def test_der_stempel_nennt_den_anzeigenamen() -> None:
    """`name` ist der programmatische Bezeichner (`eth_library_mcp`), `title`
    der Name fuer Menschen. Ohne `title` zeigt ein Client den Bezeichner."""
    info = await _modern_server_info("tools/list")

    assert info.get("title") == SERVER_TITLE
    assert info.get("title") != info.get("name")


async def test_der_stempel_nennt_die_beschreibung() -> None:
    """Getrennt von der Homepage unten, damit die Gegenprobe zeigen kann,
    welches der beiden Argumente fehlt: ein Test mit beiden Zusicherungen
    faellt bei jedem der beiden gleich und benennt keines."""
    info = await _modern_server_info("tools/list")

    assert info.get("description") == DESCRIPTION


async def test_der_stempel_nennt_die_homepage() -> None:
    info = await _modern_server_info("tools/list")

    assert info.get("websiteUrl") == HOMEPAGE_URL


# ─── Gegen Drift zu den Manifesten ───────────────────────────────────────────


def _pyproject() -> dict[str, Any]:
    return tomllib.loads((REPO / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def test_beschreibung_und_homepage_kommen_aus_den_paketmetadaten() -> None:
    """Der Grund, warum die beiden Werte nicht als Literal in `src/` stehen.

    `scripts/check_version_sync.py` haelt ausschliesslich ZAHLEN synchron. Eine
    von Hand gepflegte Beschreibung in `server.py` haette daher kein Gate und
    waere genau die Kopie, die niemand mitbewegt. Hier steht der Vergleich, den
    es sonst nirgends gibt.
    """
    project = _pyproject()

    assert DESCRIPTION == project["description"]
    assert HOMEPAGE_URL == project["urls"]["Homepage"]


def test_die_identitaet_deckt_sich_mit_dem_registry_manifest() -> None:
    """`server.json` ist, was die MCP-Registry ueber diesen Server anzeigt.

    Es nannte Homepage und Beschreibung, waehrend der Server selbst beides
    verschwieg. Wenn beide Seiten sie jetzt fuehren, muessen sie dasselbe
    sagen — sonst zeigt die Registry etwas anderes an als der laufende Server.
    """
    manifest = json.loads((REPO / "server.json").read_text(encoding="utf-8"))

    assert manifest["websiteUrl"] == HOMEPAGE_URL


def test_der_bezeichner_ist_ueberall_derselbe() -> None:
    """Vier Stellen nennen den Namen dieses Servers. Sie muessen sich decken.

    Der Stempel am Draht steht bewusst NICHT in dieser Liste: Ihn misst
    `test_der_stempel_steht_auf_einer_gewoehnlichen_methode` gegen
    `pyproject.toml`. Hier stehen die drei Stellen, die kein Draht beruehrt --
    ein Vergleich unter Dateien, der ohne laufenden Server auskommt.

    Der Registry-Name traegt eine Namensraum-Vorsilbe (`io.github.<owner>/`).
    Verglichen wird deshalb sein Suffix; die Vorsilbe gehoert der Registry und
    nicht diesem Server.
    """
    name = _pyproject()["name"]
    manifest = json.loads((REPO / "server.json").read_text(encoding="utf-8"))

    assert manifest["packages"][0]["identifier"] == name
    assert manifest["name"].split("/")[-1] == name
    # Positivkontrolle: Der Registry-Name traegt ueberhaupt eine Vorsilbe.
    # Ohne diese Zeile bestuende die Zusicherung darueber auch an einem
    # `name`, der gar keinen Schraegstrich enthaelt — dann verglichen wir
    # den ganzen String mit sich selbst.
    assert "/" in manifest["name"]
