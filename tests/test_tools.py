"""
Tool-layer tests with respx-mocked HTTP traffic.

Covers OPS-001 of the audit: every @mcp.tool function gets at least one
happy-path test against a stubbed Discovery / Persons API response, plus
the cross-cutting error paths (HTTP 404 / 401 / 429 / timeout).

These tests do NOT hit the live ETH Library API. Run with `pytest -m live`
for the (currently absent) live suite.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from mcp.server.mcpserver.exceptions import ToolError

from eth_library_mcp.server import (
    DISCOVERY_BASE_URL,
    GetResourceInput,
    SearchArchiveInput,
    SearchByTypeInput,
    SearchEducationInput,
    SearchResourcesInput,
    eth_get_resource,
    eth_library_info,
    eth_search_archive,
    eth_search_by_type,
    eth_search_education,
    eth_search_resources,
)
from tests.hilfen import strukturiert, text

# ─── Fixtures ────────────────────────────────────────────────────────────────


def _discovery_doc(title: str = "Sample") -> dict:
    return {
        "pnx": {
            "display": {
                "title": [title],
                "creator": ["Test Author"],
                "creationdate": ["2025"],
                "type": ["book"],
            },
            "addata": {"doi": [], "issn": [], "isbn": []},
        },
        "context": {"mmsid": "990000000000205503"},
        "delivery": {"link": []},
    }


def _discovery_response(docs: list[dict] | None = None, total: int = 0) -> dict:
    docs = docs if docs is not None else []
    return {"docs": docs, "info": {"total": total or len(docs)}}


# ─── eth_search_resources ────────────────────────────────────────────────────


@respx.mock
async def test_search_resources_happy_path():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(
            200, json=_discovery_response([_discovery_doc("Quantenphysik")], total=1)
        )
    )

    ergebnis = await eth_search_resources(SearchResourcesInput(query="any,contains,Quantenphysik"))
    out = text(ergebnis)
    assert "Quantenphysik" in out
    assert "Treffer" in out
    assert strukturiert(ergebnis)["returned"] == 1
    assert strukturiert(ergebnis)["hint"] is None, (
        "Leermengen-Hinweis neben Treffern — das Modell wuerde verbreitern, "
        "obwohl die Suche geliefert hat."
    )


@respx.mock
async def test_search_resources_no_hits():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(200, json=_discovery_response([], total=0))
    )

    ergebnis = await eth_search_resources(SearchResourcesInput(query="any,contains,xyz"))
    assert "Keine Ergebnisse" in text(ergebnis)
    felder = strukturiert(ergebnis)
    assert felder["returned"] == 0
    # FID-003: der naechste Schritt steht in einem Feld, nicht nur im Fliesstext.
    assert felder["hint"]
    assert ergebnis.is_error is False, "Null Treffer ist ein gueltiges Ergebnis, kein Fehler"


@respx.mock
async def test_search_resources_http_401_no_key_leak():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(401, text="unauthorized: bad key sk-1234")
    )

    # FID-003: Ein 401 ist ein Fehlschlag und kein Ergebnis. Bis 0.4.1 kam er
    # als gewoehnliches, erfolgreiches Tool-Result beim Aufrufer an.
    with pytest.raises(ToolError) as fehler:
        await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    out = str(fehler.value)
    assert "API-Key" in out
    # OBS-002: upstream body must not leak through
    assert "sk-1234" not in out


@respx.mock
async def test_search_resources_http_500_body_not_leaked():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(500, text="<html>stacktrace internals</html>")
    )

    with pytest.raises(ToolError) as fehler:
        await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    out = str(fehler.value)
    assert "500" in out
    assert "stacktrace" not in out
    assert "<html>" not in out


# ─── eth_get_resource ────────────────────────────────────────────────────────


@respx.mock
async def test_get_resource_happy_path():
    mmsid = "990012345678205503"
    respx.get(f"{DISCOVERY_BASE_URL}/resources/{mmsid}").mock(
        return_value=httpx.Response(200, json={"docs": [_discovery_doc("Detail-Titel")]})
    )

    ergebnis = await eth_get_resource(GetResourceInput(mmsid=mmsid))
    assert "Detail-Titel" in text(ergebnis)
    assert strukturiert(ergebnis)["returned"] == 1


@respx.mock
async def test_get_resource_404_says_id():
    mmsid = "990000000000999999"
    respx.get(f"{DISCOVERY_BASE_URL}/resources/{mmsid}").mock(
        return_value=httpx.Response(404, text="not found")
    )

    with pytest.raises(ToolError) as fehler:
        await eth_get_resource(GetResourceInput(mmsid=mmsid))
    # 404 on a single-resource lookup → MMS-ID-Hinweis (not the search hint)
    assert "MMS-ID" in str(fehler.value)


# ─── eth_search_archive ──────────────────────────────────────────────────────


@respx.mock
async def test_search_archive_happy_path():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(
            200, json=_discovery_response([_discovery_doc("Archivstück")], total=1)
        )
    )

    out = text(
        await eth_search_archive(
            SearchArchiveInput(archive="ETH_Hochschularchiv", query="any,contains,Schule")
        )
    )
    assert "Archivstück" in out
    assert "Hochschularchiv" in out


# ─── eth_search_by_type ──────────────────────────────────────────────────────


@respx.mock
async def test_search_by_type_happy_path():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(
            200, json=_discovery_response([_discovery_doc("Karte Zürich")], total=1)
        )
    )

    out = text(
        await eth_search_by_type(
            SearchByTypeInput(resource_type="maps", query="any,contains,Zürich")
        )
    )
    assert "Karte" in out


# ─── eth_search_education ────────────────────────────────────────────────────


@respx.mock
async def test_search_education_happy_path():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(
            200, json=_discovery_response([_discovery_doc("Volksschule")], total=1)
        )
    )

    out = text(await eth_search_education(SearchEducationInput(topic="Volksschule Zürich")))
    assert "Volksschule" in out


# ─── eth_library_info ────────────────────────────────────────────────────────


async def test_library_info_no_network():
    # eth_library_info is open_world_hint=False — it must not call upstream
    out = await eth_library_info()
    assert "ETH Library MCP Server" in out
    assert "Verfügbare Tools" in out


# ─── SEC-021: egress allow-list ──────────────────────────────────────────────


@respx.mock
async def test_egress_blocked_for_unknown_host(monkeypatch):
    from eth_library_mcp import server

    # Temporarily redirect a base URL to a non-allow-listed host
    monkeypatch.setattr(server, "DISCOVERY_BASE_URL", "https://evil.example.com/v1")

    # Das frueher hier stehende `or "Egress denied" in out` machte diesen Test
    # unabhaengig davon gruen, ob die Sperre ueberhaupt existiert: Ohne sie
    # laeuft die Anfrage in respx' AllMockedAssertionError und erzeugt genau
    # denselben Text. Die eigentliche Zusicherung -- dass gar keine Anfrage
    # hinausgeht -- misst tests/test_zusicherungen.py an der Routen-Zaehlung,
    # die Meldung selbst tests/test_fehlerkanal.py. Hier bleibt, dass der
    # Aufrufer keinen Erfolg gemeldet bekommt: seit FID-003 als `isError`.
    with pytest.raises(ToolError) as fehler:
        await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    assert "Fehler" in str(fehler.value)
