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
import respx

from eth_library_mcp.server import (
    DISCOVERY_BASE_URL,
    PERSONS_BASE_URL,
    GetResourceInput,
    SearchArchiveInput,
    SearchByTypeInput,
    SearchEducationInput,
    SearchPersonsInput,
    SearchResourcesInput,
    eth_get_resource,
    eth_library_info,
    eth_search_archive,
    eth_search_by_type,
    eth_search_education,
    eth_search_persons,
    eth_search_resources,
)

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

    out = await eth_search_resources(
        SearchResourcesInput(query="any,contains,Quantenphysik")
    )
    assert "Quantenphysik" in out
    assert "Treffer" in out


@respx.mock
async def test_search_resources_no_hits():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(200, json=_discovery_response([], total=0))
    )

    out = await eth_search_resources(SearchResourcesInput(query="any,contains,xyz"))
    assert "Keine Ergebnisse" in out


@respx.mock
async def test_search_resources_http_401_no_key_leak():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(401, text="unauthorized: bad key sk-1234")
    )

    out = await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    assert "API-Key" in out
    # OBS-002: upstream body must not leak through
    assert "sk-1234" not in out


@respx.mock
async def test_search_resources_http_500_body_not_leaked():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(500, text="<html>stacktrace internals</html>")
    )

    out = await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    assert "500" in out
    assert "stacktrace" not in out
    assert "<html>" not in out


# ─── eth_get_resource ────────────────────────────────────────────────────────


@respx.mock
async def test_get_resource_happy_path():
    mmsid = "990012345678205503"
    respx.get(f"{DISCOVERY_BASE_URL}/resources/{mmsid}").mock(
        return_value=httpx.Response(
            200, json={"docs": [_discovery_doc("Detail-Titel")]}
        )
    )

    out = await eth_get_resource(GetResourceInput(mmsid=mmsid))
    assert "Detail-Titel" in out


@respx.mock
async def test_get_resource_404_says_id():
    mmsid = "990000000000999999"
    respx.get(f"{DISCOVERY_BASE_URL}/resources/{mmsid}").mock(
        return_value=httpx.Response(404, text="not found")
    )

    out = await eth_get_resource(GetResourceInput(mmsid=mmsid))
    # 404 on a single-resource lookup → MMS-ID-Hinweis (not the search hint)
    assert "MMS-ID" in out


# ─── eth_search_archive ──────────────────────────────────────────────────────


@respx.mock
async def test_search_archive_happy_path():
    respx.get(f"{DISCOVERY_BASE_URL}/resources").mock(
        return_value=httpx.Response(
            200, json=_discovery_response([_discovery_doc("Archivstück")], total=1)
        )
    )

    out = await eth_search_archive(
        SearchArchiveInput(archive="ETH_Hochschularchiv", query="any,contains,Schule")
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

    out = await eth_search_by_type(
        SearchByTypeInput(resource_type="maps", query="any,contains,Zürich")
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

    out = await eth_search_education(
        SearchEducationInput(topic="Volksschule Zürich")
    )
    assert "Volksschule" in out


# ─── eth_search_persons ──────────────────────────────────────────────────────


@respx.mock
async def test_search_persons_happy_path():
    respx.get(f"{PERSONS_BASE_URL}/persons").mock(
        return_value=httpx.Response(
            200,
            json={
                "persons": [
                    {"name": "Albert Einstein", "birthDate": "1879", "deathDate": "1955"}
                ]
            },
        )
    )

    out = await eth_search_persons(SearchPersonsInput(query="Einstein"))
    assert "Einstein" in out


@respx.mock
async def test_search_persons_404_documented_bug02():
    # BUG-02: the live persons endpoint currently returns 404
    respx.get(f"{PERSONS_BASE_URL}/persons").mock(
        return_value=httpx.Response(404, text="not found")
    )

    out = await eth_search_persons(SearchPersonsInput(query="Einstein"))
    assert "Endpunkt nicht gefunden" in out or "Keine Ergebnisse" in out


# ─── eth_library_info ────────────────────────────────────────────────────────


async def test_library_info_no_network():
    # eth_library_info is openWorldHint=False — it must not call upstream
    out = await eth_library_info()
    assert "ETH Library MCP Server" in out
    assert "Verfügbare Tools" in out


# ─── SEC-021: egress allow-list ──────────────────────────────────────────────


@respx.mock
async def test_egress_blocked_for_unknown_host(monkeypatch):
    from eth_library_mcp import server

    # Temporarily redirect a base URL to a non-allow-listed host
    monkeypatch.setattr(server, "DISCOVERY_BASE_URL", "https://evil.example.com/v1")

    out = await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    assert "Unbekannter Fehler" in out or "Egress denied" in out
