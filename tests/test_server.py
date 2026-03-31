"""Tests für eth-library-mcp."""

import pytest
from pydantic import ValidationError

# ─── Import-Tests ─────────────────────────────────────────────────────────────


def test_import_server():
    """MCP-Server ist importierbar."""
    from eth_library_mcp.server import mcp

    assert mcp is not None


def test_import_version():
    """Package exportiert __version__."""
    from eth_library_mcp import __version__

    assert __version__ == "0.2.0"


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
    from eth_library_mcp.server import _format_resource_detail

    doc = {
        "pnx": {
            "display": {
                "title": ["Detailtest"],
                "creator": ["Autorin"],
                "creationdate": ["2023"],
                "type": ["article"],
                "language": ["de"],
                "subject": ["Thema1", "Thema2"],
                "description": ["Eine Beschreibung"],
            },
            "addata": {"isbn": ["978-3-1234"]},
        },
        "context": {"mmsid": "990002"},
        "delivery": {"link": []},
    }
    result = _format_resource_detail(doc)
    assert "# Detailtest" in result
    assert "Autorin" in result
    assert "978-3-1234" in result


def test_parse_persons_response_list():
    """_parse_persons_response: direkte Liste."""
    from eth_library_mcp.server import _parse_persons_response

    data = [{"name": "Einstein"}]
    assert _parse_persons_response(data) == [{"name": "Einstein"}]


def test_parse_persons_response_dict():
    """_parse_persons_response: Wrapper-Dict mit verschiedenen Keys."""
    from eth_library_mcp.server import _parse_persons_response

    for key in ("persons", "results", "data", "items", "hits"):
        data = {key: [{"name": "Test"}]}
        result = _parse_persons_response(data)
        assert len(result) == 1
        assert result[0]["name"] == "Test"


def test_parse_persons_response_unknown():
    """_parse_persons_response: unbekannte Struktur gibt leere Liste."""
    from eth_library_mcp.server import _parse_persons_response

    assert _parse_persons_response({"unknown": []}) == []
    assert _parse_persons_response("invalid") == []


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


def test_search_persons_input_valid():
    """SearchPersonsInput akzeptiert gültige Eingaben."""
    from eth_library_mcp.server import SearchPersonsInput

    inp = SearchPersonsInput(query="Einstein Albert")
    assert inp.query == "Einstein Albert"
    assert inp.limit == 10


def test_search_persons_input_too_short():
    """SearchPersonsInput lehnt zu kurze Query ab."""
    from eth_library_mcp.server import SearchPersonsInput

    with pytest.raises(ValidationError):
        SearchPersonsInput(query="E")


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
