"""Tests für eth-library-mcp.

Was hier aufgezeichnet ist, ist nicht eine Antwort, sondern der Vertrag: welche
Routen das Gateway führt. Die Discovery-API verlangt einen Schlüssel, also gibt
es keine Antwort, die man datieren könnte — die Payloads stehen weiterhin als
Literale im Testmodul und `tests/fixtures/PROVENANCE.md` sagt das ausdrücklich.

Aufzeichenbar war trotzdem genau das, woran der Befund hängt: Das Gateway
routet **vor** der Schlüsselprüfung, also unterscheidet es selbst zwischen
«Route da, Schlüssel fehlt» (401) und «Route gibt es nicht» (404). Siehe
`TestGatewayRoutes`.
"""

import pytest
from pydantic import ValidationError

from tests.fixture_data import route_status

# ─── Import-Tests ─────────────────────────────────────────────────────────────


def test_import_server():
    """MCP-Server ist importierbar."""
    from eth_library_mcp.server import mcp

    assert mcp is not None


def test_import_version():
    """__version__ entspricht der Version der installierten Distribution.

    Vorher stand hier das Literal "0.3.0" — dieselbe von Hand gepflegte Zahl,
    die im Paket auf 0.3.3 stand. Der Test hat die Drift also nicht erkannt,
    sondern festgeschrieben. Jetzt wird gegen die Metadaten geprüft.
    """
    from importlib.metadata import version

    from eth_library_mcp import __version__

    assert __version__ == version("eth-library-mcp")


# ─── Hilfsfunktionen ─────────────────────────────────────────────────────────


def test_first_empty():
    """_first gibt leeren String bei leerer Liste."""
    from eth_library_mcp.server import _first

    assert _first([]) == ""


def test_first_value():
    """_first gibt erstes Element als String."""
    from eth_library_mcp.server import _first

    assert _first(["hello", "world"]) == "hello"
    assert _first([42]) == "42"


def test_format_resource_summary():
    """_format_resource_summary formatiert ein Dokument als Markdown-Zeile."""
    from eth_library_mcp.server import _format_resource_summary

    doc = {
        "pnx": {
            "display": {
                "title": ["Test Buch"],
                "creator": ["Max Muster"],
                "creationdate": ["2024"],
                "type": ["book"],
            },
            "addata": {"doi": ["10.1234/test"]},
        },
        "context": {"mmsid": "990001"},
    }
    result = _format_resource_summary(doc)
    assert "**Test Buch**" in result
    assert "Max Muster" in result
    assert "990001" in result


def test_format_resource_summary_empty():
    """_format_resource_summary verarbeitet leere Daten."""
    from eth_library_mcp.server import _format_resource_summary

    result = _format_resource_summary({})
    assert "Kein Titel" in result


def test_format_resource_detail():
    """_format_resource_detail erzeugt Markdown-Dokument."""


def test_handle_error_timeout():
    """_handle_error: Timeout-Fehlermeldung."""
    import httpx

    from eth_library_mcp.server import _handle_error

    err = httpx.TimeoutException("timeout")
    result = _handle_error(err, "Test")
    assert "Zeitüberschreitung" in result


def test_handle_error_connect():
    """_handle_error: Verbindungsfehler."""
    import httpx

    from eth_library_mcp.server import _handle_error

    err = httpx.ConnectError("connection failed")
    result = _handle_error(err, "Test")
    assert "Verbindungsfehler" in result


# ─── Pydantic Input-Validierung ──────────────────────────────────────────────


def test_search_resources_input_valid():
    """SearchResourcesInput akzeptiert gültige Eingaben."""
    from eth_library_mcp.server import SearchResourcesInput

    inp = SearchResourcesInput(query="any,contains,test")
    assert inp.query == "any,contains,test"
    assert inp.limit == 10
    assert inp.sort == "rank"


def test_search_resources_input_invalid_sort():
    """SearchResourcesInput lehnt ungültige Sortierung ab."""
    from eth_library_mcp.server import SearchResourcesInput

    with pytest.raises(ValidationError):
        SearchResourcesInput(query="test", sort="invalid")


def test_search_resources_input_invalid_type():
    """SearchResourcesInput lehnt ungültigen Ressourcentyp ab."""
    from eth_library_mcp.server import SearchResourcesInput

    with pytest.raises(ValidationError):
        SearchResourcesInput(query="test", resource_type="invalid_type")


def test_search_archive_input_valid():
    """SearchArchiveInput akzeptiert gültige Archivkennung."""
    from eth_library_mcp.server import SearchArchiveInput

    inp = SearchArchiveInput(archive="ETH_Hochschularchiv")
    assert inp.archive == "ETH_Hochschularchiv"


def test_search_archive_input_invalid():
    """SearchArchiveInput lehnt ungültige Archivkennung ab."""
    from eth_library_mcp.server import SearchArchiveInput

    with pytest.raises(ValidationError):
        SearchArchiveInput(archive="INVALID_ARCHIVE")


def test_search_education_input_valid():
    """SearchEducationInput akzeptiert gültige Eingaben."""
    from eth_library_mcp.server import SearchEducationInput

    inp = SearchEducationInput(topic="Volksschule Zürich")
    assert inp.topic == "Volksschule Zürich"
    assert inp.limit == 15


def test_search_by_type_input_valid():
    """SearchByTypeInput akzeptiert gültigen Typ."""
    from eth_library_mcp.server import SearchByTypeInput

    inp = SearchByTypeInput(resource_type="maps")
    assert inp.resource_type == "maps"


def test_search_by_type_input_invalid():
    """SearchByTypeInput lehnt ungültigen Typ ab."""
    from eth_library_mcp.server import SearchByTypeInput

    with pytest.raises(ValidationError):
        SearchByTypeInput(resource_type="invalid")


def test_get_resource_input_valid():
    """GetResourceInput akzeptiert gültige MMS-ID."""
    from eth_library_mcp.server import GetResourceInput

    inp = GetResourceInput(mmsid="990075811280205503")
    assert inp.mmsid == "990075811280205503"
    assert inp.include_availability is True


# ─── Konstanten ──────────────────────────────────────────────────────────────


def test_resource_types_complete():
    """Alle 10 Ressourcentypen definiert."""
    from eth_library_mcp.server import RESOURCE_TYPES

    assert len(RESOURCE_TYPES) == 10
    assert "books" in RESOURCE_TYPES
    assert "maps" in RESOURCE_TYPES
    assert "images" in RESOURCE_TYPES


def test_archive_sources_complete():
    """Alle 5 Archive definiert."""
    from eth_library_mcp.server import ARCHIVE_SOURCES

    assert len(ARCHIVE_SOURCES) == 5
    assert "ETH_Hochschularchiv" in ARCHIVE_SOURCES
    assert "ETH_Bildarchiv" in ARCHIVE_SOURCES


# ---------------------------------------------------------------------------
# Der Vertrag: welche Routen das Gateway führt
# ---------------------------------------------------------------------------


class TestGatewayRoutes:
    """Warum das Personen-Werkzeug entfernt ist statt repariert.

    Im Code stand die Notiz: *«BUG-02: Der Persons-API-Endpunkt gibt aktuell
    HTTP 404 zurück. Die korrekte URL muss via developer.library.ethz.ch
    verifiziert werden.»* Die offene Frage war, ob bloss die URL falsch ist.

    Sie lässt sich ohne API-Key entscheiden, weil das Gateway **vor** der
    Schlüsselprüfung routet: Eine vorhandene Route antwortet mit 401
    («Schlüssel fehlt»), eine nicht vorhandene mit 404. Die aufgezeichneten
    Kontrollen zeigen genau diesen Unterschied — und ohne sie belegte die
    Messung nur, dass jemand einen 404 bekommen hat.
    """

    def test_the_gateway_distinguishes_missing_key_from_missing_route(self):
        # Kontrolle 1: ein erfundener Pfad unter einer vorhandenen Route.
        assert route_status("control_discovery_unknown_path") == 404
        # ... während die Route selbst nach dem Schlüssel fragt.
        assert route_status("discovery_resources") == 401
        assert route_status("discovery_resource_by_id") == 401

    def test_the_persons_api_is_gone_not_merely_locked(self):
        assert route_status("persons_persons") == 404
        assert route_status("persons_root") == 404
        # Kontrolle 2: eine Version, die es nie gab — dieselbe Antwort.
        assert route_status("control_persons_v2") == 404
        assert route_status("persons_persons") != route_status("discovery_resources"), (
            "Persons und Discovery antworten gleich — dann trennt die Messung "
            "nichts mehr und der Befund gehört neu erhoben."
        )

    def test_no_tool_still_offers_the_persons_api(self):
        """Eine Fähigkeit, die es nicht gibt, darf nicht angeboten werden."""
        import eth_library_mcp.server as srv

        assert not hasattr(srv, "eth_search_persons")
        assert not hasattr(srv, "SearchPersonsInput")


@pytest.mark.live
class TestLiveGatewayRoutes:
    """Dieselbe Unterscheidung gegen den echten Host — ohne API-Key.

    Dieses Repo hatte **gar keine** Live-Tests: `pytest -m live` sammelte null
    ein. Nichts darin war je gegen die Quelle gehalten worden. Diese beiden
    brauchen keinen Schlüssel und sagen trotzdem etwas: Sie melden, wenn die
    Personen-API zurückkommt (dann gehört das Werkzeug wieder her) oder wenn
    Discovery seine Route verliert (dann sind fünf Werkzeuge betroffen).
    """

    def test_discovery_route_still_exists(self):
        import httpx

        from eth_library_mcp.client import DISCOVERY_BASE_URL

        r = httpx.get(f"{DISCOVERY_BASE_URL}/resources", timeout=45)
        assert r.status_code == route_status("discovery_resources"), (
            f"Discovery antwortet mit {r.status_code} statt "
            f"{route_status('discovery_resources')} — fünf Werkzeuge hängen daran."
        )

    def test_persons_route_is_still_gone(self):
        import httpx

        from eth_library_mcp.client import PERSONS_BASE_URL

        r = httpx.get(f"{PERSONS_BASE_URL}/persons", timeout=45)
        assert r.status_code == 404, (
            f"Die Personen-API antwortet mit {r.status_code} statt 404 — die "
            "Route ist zurück, und das entfernte Werkzeug gehört geprüft."
        )
