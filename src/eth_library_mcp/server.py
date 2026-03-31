"""
ETH Library MCP Server
=======================
MCP-Server für die ETH-Bibliothek Zürich.
Ermöglicht Claude und anderen KI-Assistenten den Zugriff auf 30+ Millionen
Ressourcen der grössten naturwissenschaftlichen Bibliothek der Schweiz.

APIs:
  - Discovery API:          30+ Mio. Bücher, Bilder, Zeitschriften, Karten
  - Persons API:            Personen mit Linked-Data-Anreicherung (Wikidata)
                            ⚠ Endpunkt-URL muss via developer.library.ethz.ch
                              verifiziert werden (BUG-02 – aktuelle URL gibt 404)

Authentifizierung:
  Kostenloser API-Key via https://developer.library.ethz.ch
  Umgebungsvariable: ETH_LIBRARY_API_KEY
"""

import json
import logging
import os
from typing import Any, Literal

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

# ─── Logging ──────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ─── API-Konfiguration ────────────────────────────────────────────────────────

DISCOVERY_BASE_URL = "https://api.library.ethz.ch/discovery/v1"
PERSONS_BASE_URL = "https://api.library.ethz.ch/persons/v1"
# Hinweis: PERSONS_BASE_URL ist als potenziell defekt markiert (BUG-02).
# Korrekten Endpunkt via https://developer.library.ethz.ch verifizieren.

REQUEST_TIMEOUT = 30.0

# ─── Typ-Aliase für Literal-Validierung ──────────────────────────────────────

SortOption = Literal["rank", "title", "author", "date"]

ResourceType = Literal[
    "books",
    "journals",
    "articles",
    "maps",
    "images",
    "archival_materials",
    "scores",
    "databases",
    "audios",
    "videos",
]

ArchiveKey = Literal[
    "ETH_Hochschularchiv",
    "ETH_MaxFrischArchiv",
    "ETH_ThomasMannArchiv",
    "ETH_GraphischeSammlung",
    "ETH_Bildarchiv",
]

# ─── Bekannte Ressourcentypen (facet_rtype) ───────────────────────────────────

RESOURCE_TYPES: dict[str, str] = {
    "books": "Bücher / Books",
    "journals": "Zeitschriften / Journals",
    "articles": "Artikel / Articles",
    "maps": "Karten / Maps",
    "images": "Bilder / Images",
    "archival_materials": "Archivmaterialien / Archival Materials",
    "scores": "Noten / Scores",
    "databases": "Datenbanken / Databases",
    "audios": "Audiomaterialien / Audios",
    "videos": "Videomaterialien / Videos",
}

# ─── Bekannte Archivquellen (facet_data_source) ───────────────────────────────

ARCHIVE_SOURCES: dict[str, str] = {
    "ETH_Hochschularchiv": "Hochschularchiv ETH Zürich",
    "ETH_MaxFrischArchiv": "Max Frisch Archiv",
    "ETH_ThomasMannArchiv": "Thomas-Mann-Archiv",
    "ETH_GraphischeSammlung": "Graphische Sammlung",
    "ETH_Bildarchiv": "Bildarchiv (E-Pics)",
}

# ─── Sortiermöglichkeiten ─────────────────────────────────────────────────────

SORT_OPTIONS = list(SortOption.__args__)  # type: ignore[attr-defined]


# ─── HTTP-Client ──────────────────────────────────────────────────────────────


def _get_api_key() -> str | None:
    """API-Key aus Umgebungsvariable lesen (graceful degradation)."""
    return os.environ.get("ETH_LIBRARY_API_KEY")


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

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, params=request_params)
        response.raise_for_status()
        return response.json()


# ─── Formatierungshilfsfunktionen ─────────────────────────────────────────────


def _first(lst: list[Any]) -> str:
    """Erstes Element einer Liste als String, leer wenn nicht vorhanden."""
    return str(lst[0]) if lst else ""


def _add_field(lines: list[str], label: str, value: str) -> None:
    """Fügt ein Feld zur Detailansicht hinzu, falls vorhanden."""
    if value:
        lines.append(f"**{label}:** {value}")


def _format_resource_summary(doc: dict[str, Any]) -> str:
    """Formatiert einen einzelnen Discovery-Eintrag als kompakte Markdown-Zeile."""
    pnx = doc.get("pnx", {})
    display = pnx.get("display", {})
    addata = pnx.get("addata", {})

    title = _first(display.get("title", []))
    creator = _first(display.get("creator", []))
    date = _first(display.get("creationdate", []))
    rtype = _first(display.get("type", []))
    mmsid = doc.get("context", {}).get("mmsid", "")
    doi = _first(addata.get("doi", []))

    parts = [f"**{title or 'Kein Titel'}**"]
    if creator:
        parts.append(f"von {creator}")
    if date:
        parts.append(f"({date})")
    if rtype:
        parts.append(f"[{rtype}]")
    if mmsid:
        parts.append(f"MMS-ID: `{mmsid}`")
    if doi:
        parts.append(f"DOI: {doi}")

    return " – ".join(parts)


def _format_resource_detail(doc: dict[str, Any]) -> str:
    """Formatiert einen Discovery-Eintrag als detailliertes Markdown-Dokument."""
    pnx = doc.get("pnx", {})
    display = pnx.get("display", {})
    addata = pnx.get("addata", {})
    links = doc.get("delivery", {}).get("link", [])

    lines: list[str] = []

    title = _first(display.get("title", []))
    lines.append(f"# {title or 'Kein Titel'}")
    lines.append("")

    _add_field(lines, "Autor/in", _first(display.get("creator", [])))
    _add_field(lines, "Mitwirkende", ", ".join(display.get("contributor", [])))
    _add_field(lines, "Jahr", _first(display.get("creationdate", [])))
    _add_field(lines, "Typ", _first(display.get("type", [])))
    _add_field(lines, "Sprache", _first(display.get("language", [])))
    _add_field(lines, "Verlag", _first(display.get("publisher", [])))
    _add_field(lines, "Erscheinungsort", _first(display.get("place", [])))
    _add_field(lines, "ISSN", _first(addata.get("issn", [])))
    _add_field(lines, "ISBN", _first(addata.get("isbn", [])))
    _add_field(lines, "DOI", _first(addata.get("doi", [])))
    _add_field(lines, "MMS-ID", doc.get("context", {}).get("mmsid", ""))

    subjects = display.get("subject", [])
    if subjects:
        lines.append(f"**Schlagworte:** {', '.join(subjects[:10])}")

    description = _first(display.get("description", []))
    if description:
        lines.append("")
        lines.append(f"**Beschreibung:** {description[:500]}")

    if links:
        lines.append("")
        lines.append("**Links:**")
        for link in links[:5]:
            label = link.get("displayLabel", "Link")
            href = link.get("linkURL", "")
            if href:
                lines.append(f"- [{label}]({href})")

    return "\n".join(filter(None, lines))


def _parse_persons_response(data: Any) -> list[dict[str, Any]]:
    """
    Robustes Parsing der Persons-API-Antwort.

    Unterstützt verschiedene Response-Strukturen der ETH Persons API:
    - Direkte Liste: [...]
    - Wrapper mit 'persons', 'results', 'data', 'items' oder 'hits' Key
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("persons", "results", "data", "items", "hits"):
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    return value

        logger.warning(
            "Persons-API: Unbekannte Response-Struktur. "
            "Bekannte Keys: %s. Gefundene Keys: %s",
            ["persons", "results", "data", "items", "hits"],
            list(data.keys()),
        )

    return []


def _handle_error(
    e: Exception,
    context: str = "",
    is_search: bool = True,
) -> str:
    """
    Einheitliche, hilfreiche Fehlermeldungen – kein Hard-Failure.

    Kontext-spezifische 404-Meldung:
      is_search=True  → 'Keine Ergebnisse oder Endpunkt nicht gefunden'
      is_search=False → 'Ressource mit dieser ID nicht gefunden'
    """
    prefix = f"Fehler bei {context}: " if context else "Fehler: "

    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        if status == 401:
            return (
                f"{prefix}Kein gültiger API-Key. "
                "Bitte ETH_LIBRARY_API_KEY Umgebungsvariable setzen. "
                "Kostenlose Registrierung: https://developer.library.ethz.ch"
            )
        elif status == 403:
            return f"{prefix}Zugriff verweigert (HTTP 403)."
        elif status == 404:
            if is_search:
                return (
                    f"{prefix}Keine Ergebnisse oder Endpunkt nicht gefunden (HTTP 404). "
                    "Bitte Suchanfrage oder API-Endpunkt prüfen."
                )
            else:
                return (
                    f"{prefix}Ressource mit dieser ID nicht gefunden (HTTP 404). "
                    "Bitte MMS-ID prüfen."
                )
        elif status == 429:
            return f"{prefix}Rate-Limit erreicht (HTTP 429). Bitte kurz warten."
        return f"{prefix}HTTP-Fehler {status}: {e.response.text[:200]}"
    elif isinstance(e, httpx.TimeoutException):
        return f"{prefix}Zeitüberschreitung. ETH-Bibliothek API nicht erreichbar."
    elif isinstance(e, httpx.ConnectError):
        return f"{prefix}Verbindungsfehler. Internetverbindung prüfen."
    return f"{prefix}{type(e).__name__}: {e}"


# ─── Server-Initialisierung ───────────────────────────────────────────────────

mcp = FastMCP(
    "eth_library_mcp",
    instructions=(
        "MCP Server für die ETH-Bibliothek Zürich. "
        "Bietet Zugriff auf über 30 Millionen Bücher, Zeitschriften, Bilder, Karten "
        "und Archivmaterialien via Discovery API (api.library.ethz.ch). "
        "Ebenfalls verfügbar: Personen-Suche mit Wikidata-Verlinkung. "
        "Bekannte Archive: Hochschularchiv ETH, Max Frisch Archiv, Thomas-Mann-Archiv, "
        "Graphische Sammlung, Bildarchiv (E-Pics). "
        "Für den Zugriff ist ein kostenloser API-Key erforderlich "
        "(developer.library.ethz.ch). "
        "Alle Metadaten sind frei nutzbar (Public Domain / CC0)."
    ),
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 1: Ressourcen suchen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchResourcesInput(BaseModel):
    """Input für die allgemeine Ressourcen-Suche."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ...,
        description=(
            "Suchanfrage im Format 'Feld,Operator,Wert'. "
            "Felder: any, title, creator, sub (Thema). "
            "Operatoren: contains, exact, begins_with. "
            "Beispiele: 'any,contains,Volksschule' oder "
            "'title,contains,Zürich;sub,contains,Geschichte' (AND-Verknüpfung mit ;). "
            "Logische Operatoren: AND, OR, NOT. Wildcards (*) möglich."
        ),
        min_length=1,
        max_length=500,
    )
    limit: int = Field(
        default=10,
        description="Anzahl Ergebnisse (1–100, Standard: 10)",
        ge=1,
        le=100,
    )
    offset: int = Field(
        default=0,
        description="Offset für Pagination (Standard: 0)",
        ge=0,
    )
    sort: SortOption | None = Field(
        default="rank",
        description=f"Sortierung: {', '.join(SORT_OPTIONS)}",
    )
    resource_type: ResourceType | None = Field(
        default=None,
        description=(
            f"Ressourcentyp-Filter. Mögliche Werte: {', '.join(RESOURCE_TYPES.keys())}"
        ),
    )
    language: str | None = Field(
        default=None,
        description="Sprachfilter: 'de', 'en', 'fr', 'it', etc.",
    )
    open_access_only: bool = Field(
        default=False,
        description="Nur Open-Access-Ressourcen anzeigen",
    )
    response_lang: str = Field(
        default="de",
        description="Sprache für API-Antwortfelder: 'de' oder 'en'",
    )


@mcp.tool(
    name="eth_search_resources",
    annotations={
        "title": "ETH-Bibliothek Ressourcen suchen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_search_resources(params: SearchResourcesInput) -> str:
    """
    Durchsucht den Katalog der ETH-Bibliothek mit über 30 Millionen Ressourcen.

    Nutzt die Discovery API (api.library.ethz.ch/discovery/v1/resources).
    Unterstützt Freitextsuche, Feldsuche, Facetten-Filter und Pagination.

    Args:
        params (SearchResourcesInput): Suchparameter mit:
            - query (str): Suchanfrage (z.B. 'any,contains,Quantenphysik')
            - limit (int): Anzahl Ergebnisse (1–100)
            - offset (int): Offset für Pagination
            - sort (str): Sortierung (rank/title/author/date)
            - resource_type (str): Typ-Filter (books/journals/maps/images/...)
            - language (str): Sprachfilter
            - open_access_only (bool): Nur OA-Ressourcen
            - response_lang (str): Sprache der API-Antwort

    Returns:
        str: Markdown-formatierte Ergebnisliste mit Titel, Autor, Jahr, Typ, MMS-ID
    """
    try:
        api_params: dict = {
            "q": params.query,
            "limit": str(params.limit),
            "offset": str(params.offset),
            "lang": params.response_lang,
        }

        if params.sort:
            api_params["sort"] = params.sort

        # Facetten-Filter zusammenbauen
        include_parts: list[str] = []
        if params.resource_type:
            include_parts.append(f"facet_rtype,exact,{params.resource_type}")
        if params.language:
            include_parts.append(f"facet_lang,exact,{params.language}")
        if params.open_access_only:
            include_parts.append("facet_tlevel,exact,open_access")

        if include_parts:
            api_params["qInclude"] = "|,|".join(include_parts)

        data = await _http_get(DISCOVERY_BASE_URL, "/resources", api_params)

        docs = data.get("docs", [])
        total = data.get("info", {}).get("total", 0)

        if not docs:
            return (
                f"Keine Ergebnisse für '{params.query}'. "
                "Tipp: Breitere Suche mit 'any,contains,Begriff' versuchen."
            )

        lines = [
            "## ETH-Bibliothek: Suchergebnisse",
            f"**Suche:** `{params.query}`  ",
            f"**Treffer:** {total:,} total, zeige {params.offset + 1}–"
            f"{params.offset + len(docs)}",
            "",
        ]

        for i, doc in enumerate(docs, start=params.offset + 1):
            lines.append(f"{i}. {_format_resource_summary(doc)}")

        # Pagination-Hinweis
        if total > params.offset + len(docs):
            next_offset = params.offset + params.limit
            lines.append("")
            lines.append(
                f"*Weitere Ergebnisse: offset={next_offset} verwenden "
                f"({total - next_offset:,} verbleibend)*"
            )

        return "\n".join(lines)

    except Exception as e:
        return _handle_error(e, f"Suche nach '{params.query}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 2: Einzelne Ressource abrufen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class GetResourceInput(BaseModel):
    """Input für den Abruf einer einzelnen Ressource."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    mmsid: str = Field(
        ...,
        description=(
            "Alma MMS-ID der Ressource (aus Suchergebnissen). "
            "Beispiel: '990075811280205503'"
        ),
        min_length=5,
        max_length=50,
    )
    include_availability: bool = Field(
        default=True,
        description="Verfügbarkeitsinformationen (Ausleihstatus) einbeziehen",
    )
    lang: str = Field(
        default="de",
        description="Sprache der API-Antwort: 'de' oder 'en'",
    )


@mcp.tool(
    name="eth_get_resource",
    annotations={
        "title": "ETH-Bibliothek Ressource abrufen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_get_resource(params: GetResourceInput) -> str:
    """
    Ruft eine einzelne Ressource der ETH-Bibliothek anhand ihrer MMS-ID ab.

    Liefert vollständige bibliografische Metadaten, Schlagworte,
    Beschreibung, Links und optional Verfügbarkeitsstatus.

    Args:
        params (GetResourceInput): Parameter mit:
            - mmsid (str): Alma MMS-ID (z.B. '990075811280205503')
            - include_availability (bool): Ausleihstatus einbeziehen
            - lang (str): Antwortsprache

    Returns:
        str: Vollständige Markdown-Darstellung der Ressource
    """
    try:
        api_params: dict = {
            "lang": params.lang,
            "avail": str(params.include_availability).lower(),
        }

        data = await _http_get(
            DISCOVERY_BASE_URL, f"/resources/{params.mmsid}", api_params
        )

        doc = data.get("docs", [{}])[0] if data.get("docs") else data
        return _format_resource_detail(doc)

    except Exception as e:
        return _handle_error(e, f"Abruf MMS-ID '{params.mmsid}'", is_search=False)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 3: Archiv-Suche
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchArchiveInput(BaseModel):
    """Input für die Suche in einem spezifischen Archiv."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    archive: ArchiveKey = Field(
        ...,
        description=(
            f"Archivkennung. Verfügbare Archive: "
            f"{', '.join(ARCHIVE_SOURCES.keys())}. "
            f"Bedeutung: {json.dumps(ARCHIVE_SOURCES, ensure_ascii=False)}"
        ),
    )
    query: str = Field(
        default='any,contains,"*"',
        description=(
            "Optionale Einschränkung innerhalb des Archivs. "
            "Standard: alle Inhalte abrufen. "
            "Beispiel: 'any,contains,Zürich' für Zürich-Inhalte im Archiv."
        ),
        min_length=1,
        max_length=500,
    )
    limit: int = Field(default=20, description="Anzahl Ergebnisse (1–100)", ge=1, le=100)
    offset: int = Field(default=0, description="Offset für Pagination", ge=0)


@mcp.tool(
    name="eth_search_archive",
    annotations={
        "title": "ETH-Archiv durchsuchen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_search_archive(params: SearchArchiveInput) -> str:
    """
    Durchsucht ein spezifisches Archiv oder eine Sammlung der ETH-Bibliothek.

    Verfügbare Archive:
    - ETH_Hochschularchiv: Hochschularchiv der ETH Zürich (institutionelles Gedächtnis)
    - ETH_MaxFrischArchiv: Nachlass des Schweizer Autors Max Frisch
    - ETH_ThomasMannArchiv: Archiv mit Briefen und Dokumenten von Thomas Mann
    - ETH_GraphischeSammlung: Graphische Sammlung (Drucke, Zeichnungen)
    - ETH_Bildarchiv: Bildarchiv E-Pics (Wissenschafts-/Technikgeschichte, Swissair)

    Args:
        params (SearchArchiveInput): Parameter mit:
            - archive (str): Archivkennung
            - query (str): Optionale Suche innerhalb des Archivs
            - limit (int): Ergebnisanzahl
            - offset (int): Offset für Pagination

    Returns:
        str: Markdown-Liste der Archivressourcen
    """
    archive_name = ARCHIVE_SOURCES.get(params.archive, params.archive)

    try:
        api_params: dict = {
            "q": params.query,
            "limit": str(params.limit),
            "offset": str(params.offset),
            "qInclude": f"facet_data_source,exact,{params.archive}",
            "lang": "de",
        }

        data = await _http_get(DISCOVERY_BASE_URL, "/resources", api_params)

        docs = data.get("docs", [])
        total = data.get("info", {}).get("total", 0)

        if not docs:
            return (
                f"Keine Treffer im Archiv '{archive_name}' "
                f"für Suche '{params.query}'."
            )

        lines = [
            f"## {archive_name}",
            f"**Treffer im Archiv:** {total:,} total, zeige "
            f"{params.offset + 1}–{params.offset + len(docs)}",
            "",
        ]

        for i, doc in enumerate(docs, start=params.offset + 1):
            lines.append(f"{i}. {_format_resource_summary(doc)}")

        if total > params.offset + len(docs):
            next_offset = params.offset + params.limit
            lines.append(
                f"\n*Weitere Einträge verfügbar. offset={next_offset} verwenden.*"
            )

        return "\n".join(lines)

    except Exception as e:
        return _handle_error(e, f"Archivsuche '{archive_name}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 4: Ressourcentyp-Suche
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchByTypeInput(BaseModel):
    """Input für die typgefilterte Suche."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    resource_type: ResourceType = Field(
        ...,
        description=(
            f"Ressourcentyp. Verfügbare Typen: "
            f"{json.dumps(RESOURCE_TYPES, ensure_ascii=False)}"
        ),
    )
    query: str = Field(
        default='any,contains,"*"',
        description=(
            "Optionale Suchanfrage (Standard: alle Ressourcen dieses Typs). "
            "Beispiel: 'any,contains,Zürich' für Karten von Zürich."
        ),
        min_length=1,
        max_length=500,
    )
    open_access_only: bool = Field(
        default=False,
        description="Nur frei zugängliche (Open Access) Ressourcen",
    )
    limit: int = Field(default=20, description="Anzahl Ergebnisse (1–100)", ge=1, le=100)
    offset: int = Field(default=0, description="Offset für Pagination", ge=0)


@mcp.tool(
    name="eth_search_by_type",
    annotations={
        "title": "ETH-Bibliothek nach Ressourcentyp suchen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_search_by_type(params: SearchByTypeInput) -> str:
    """
    Sucht Ressourcen eines bestimmten Typs (Karten, Bilder, Archive, etc.).

    Besonders nützlich für:
    - Alle Karten der ETH-Bibliothek: resource_type='maps'
    - Alle Bilder: resource_type='images'
    - Archivmaterialien: resource_type='archival_materials'
    - Nur Open-Access-Artikel: resource_type='articles', open_access_only=True

    Args:
        params (SearchByTypeInput): Parameter mit:
            - resource_type (str): Ressourcentyp (validierter Literal-Typ)
            - query (str): Optionale Einschränkung
            - open_access_only (bool): Nur OA-Ressourcen
            - limit (int): Ergebnisanzahl
            - offset (int): Pagination-Offset

    Returns:
        str: Markdown-Ergebnisliste nach Typ gefiltert
    """
    type_label = RESOURCE_TYPES.get(params.resource_type, params.resource_type)

    try:
        include_parts = [f"facet_rtype,exact,{params.resource_type}"]
        if params.open_access_only:
            include_parts.append("facet_tlevel,exact,open_access")

        api_params: dict = {
            "q": params.query,
            "limit": str(params.limit),
            "offset": str(params.offset),
            "qInclude": "|,|".join(include_parts),
            "sort": "rank",
            "lang": "de",
        }

        data = await _http_get(DISCOVERY_BASE_URL, "/resources", api_params)

        docs = data.get("docs", [])
        total = data.get("info", {}).get("total", 0)

        if not docs:
            return f"Keine {type_label} gefunden für Suche: '{params.query}'."

        oa_label = " (Open Access)" if params.open_access_only else ""
        lines = [
            f"## ETH-Bibliothek: {type_label}{oa_label}",
            f"**Treffer:** {total:,} total, zeige "
            f"{params.offset + 1}–{params.offset + len(docs)}",
            "",
        ]

        for i, doc in enumerate(docs, start=params.offset + 1):
            lines.append(f"{i}. {_format_resource_summary(doc)}")

        if total > params.offset + len(docs):
            next_offset = params.offset + params.limit
            lines.append(
                f"\n*Weitere Einträge: offset={next_offset} verwenden "
                f"({total - next_offset:,} verbleibend)*"
            )

        return "\n".join(lines)

    except Exception as e:
        return _handle_error(e, f"Typ-Suche '{type_label}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 5: Personen suchen
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchPersonsInput(BaseModel):
    """Input für die Personensuche."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ...,
        description=(
            "Name oder Stichwort zur Personensuche. "
            "Beispiele: 'Einstein', 'Einstein Albert', 'Frisch Max'"
        ),
        min_length=2,
        max_length=200,
    )
    limit: int = Field(default=10, description="Anzahl Ergebnisse (1–50)", ge=1, le=50)


@mcp.tool(
    name="eth_search_persons",
    annotations={
        "title": "ETH-Bibliothek Personen suchen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_search_persons(params: SearchPersonsInput) -> str:
    """
    Sucht Personen in der ETH-Bibliothek Persons API.

    ⚠ HINWEIS BUG-02: Der Persons-API-Endpunkt (/persons/v1/persons) gibt
    aktuell HTTP 404 zurück. Die korrekte URL muss via developer.library.ethz.ch
    verifiziert werden. Das Tool ist strukturell korrekt implementiert.

    Liefert Personeninformationen mit Linked-Data-Anreicherung aus:
    Wikidata, Metagrid, DNB Entityfacts, beacon.findbuch.

    Args:
        params (SearchPersonsInput): Parameter mit:
            - query (str): Name/Stichwort (z.B. 'Einstein Albert')
            - limit (int): Anzahl Ergebnisse

    Returns:
        str: Markdown-Liste gefundener Personen mit externen Verlinkungen
    """
    try:
        api_params: dict = {
            "q": params.query,
            "limit": str(params.limit),
        }

        data = await _http_get(PERSONS_BASE_URL, "/persons", api_params)

        persons = _parse_persons_response(data)

        if not persons:
            return (
                f"Keine Personen gefunden für '{params.query}'. "
                "Tipp: Vollständigen Namen (Nachname Vorname) versuchen."
            )

        lines = [
            "## ETH-Bibliothek: Personen",
            f"**Suche:** `{params.query}`  ",
            f"**Treffer:** {len(persons)}",
            "",
        ]

        for person in persons[: params.limit]:
            if isinstance(person, dict):
                name = person.get("name", person.get("label", "Unbekannt"))
                birth = person.get("birthDate", person.get("birth", ""))
                death = person.get("deathDate", person.get("death", ""))
                wikidata = person.get("wikidata", person.get("wikidataUrl", ""))
                gnd = person.get("gnd", person.get("gndId", ""))

                life = f" ({birth}–{death})" if birth or death else ""
                line = f"- **{name}**{life}"
                if wikidata:
                    line += f" | [Wikidata]({wikidata})"
                if gnd:
                    line += f" | GND: `{gnd}`"
                lines.append(line)

        return "\n".join(lines)

    except Exception as e:
        return _handle_error(e, f"Personensuche '{params.query}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 6: Schulrelevante Suche (für Schulamt-Kontext)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchEducationInput(BaseModel):
    """Input für die schulrelevante Suche."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    topic: str = Field(
        ...,
        description=(
            "Bildungsthema oder pädagogisches Stichwort. "
            "Beispiele: 'Volksschule Zürich', 'Pädagogik', 'Lehrplan', "
            "'Schulgeschichte Schweiz', 'Bildungsforschung'"
        ),
        min_length=2,
        max_length=300,
    )
    resource_type: ResourceType | None = Field(
        default=None,
        description=(
            f"Optional: Ressourcentyp-Filter. "
            f"Mögliche Werte: {', '.join(RESOURCE_TYPES.keys())}"
        ),
    )
    open_access_only: bool = Field(
        default=False,
        description="Nur frei zugängliche Ressourcen",
    )
    limit: int = Field(default=15, description="Anzahl Ergebnisse (1–50)", ge=1, le=50)


@mcp.tool(
    name="eth_search_education",
    annotations={
        "title": "ETH-Bibliothek Bildungsthemen suchen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def eth_search_education(params: SearchEducationInput) -> str:
    """
    Kuratierte Suche nach bildungsrelevanten Ressourcen in der ETH-Bibliothek.

    Optimiert für Pädagogik, Schulgeschichte, Bildungsforschung und
    didaktische Materialien. Besonders relevant für den Schulamt-Kontext.

    Args:
        params (SearchEducationInput): Parameter mit:
            - topic (str): Bildungsthema (z.B. 'Volksschule Zürich Geschichte')
            - resource_type (str): Optionaler Typ-Filter (validierter Literal-Typ)
            - open_access_only (bool): Nur OA-Ressourcen
            - limit (int): Ergebnisanzahl

    Returns:
        str: Markdown-Ergebnisliste bildungsrelevanter Ressourcen
    """
    query = f"any,contains,{params.topic}"

    try:
        include_parts: list[str] = []
        if params.resource_type:
            include_parts.append(f"facet_rtype,exact,{params.resource_type}")
        if params.open_access_only:
            include_parts.append("facet_tlevel,exact,open_access")

        api_params: dict = {
            "q": query,
            "limit": str(params.limit),
            "offset": "0",
            "sort": "rank",
            "lang": "de",
        }
        if include_parts:
            api_params["qInclude"] = "|,|".join(include_parts)

        data = await _http_get(DISCOVERY_BASE_URL, "/resources", api_params)

        docs = data.get("docs", [])
        total = data.get("info", {}).get("total", 0)

        if not docs:
            return (
                f"Keine Bildungsressourcen gefunden für '{params.topic}'. "
                "Tipp: Englischen Begriff oder breiteres Schlagwort versuchen."
            )

        oa_label = " (Open Access)" if params.open_access_only else ""
        lines = [
            f"## ETH-Bibliothek: Bildungsressourcen{oa_label}",
            f"**Thema:** {params.topic}  ",
            f"**Treffer:** {total:,} total, zeige {len(docs)}",
            "",
        ]

        for i, doc in enumerate(docs, start=1):
            lines.append(f"{i}. {_format_resource_summary(doc)}")

        if total > params.limit:
            lines.append(
                f"\n*Insgesamt {total:,} Treffer. "
                f"eth_search_resources mit offset für weitere Seiten nutzen.*"
            )

        return "\n".join(lines)

    except Exception as e:
        return _handle_error(e, f"Bildungssuche '{params.topic}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 7: Server-Info und Ressourcentypen-Übersicht
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.tool(
    name="eth_library_info",
    annotations={
        "title": "ETH-Bibliothek Server-Informationen",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def eth_library_info() -> str:
    """
    Gibt eine Übersicht über den ETH Library MCP Server zurück:
    verfügbare APIs, Ressourcentypen, Archive und Konfigurationsstatus.

    Nützlich als Einstiegspunkt vor einer Suche.

    Returns:
        str: Vollständige Markdown-Dokumentation des Servers
    """
    api_key = os.environ.get("ETH_LIBRARY_API_KEY")
    key_status = (
        "✅ Konfiguriert"
        if api_key
        else "⚠️ Nicht gesetzt (kostenlose Registrierung: developer.library.ethz.ch)"
    )

    rt_list = "\n".join(
        f"  - `{key}`: {label}" for key, label in RESOURCE_TYPES.items()
    )
    archive_list = "\n".join(
        f"  - `{key}`: {label}" for key, label in ARCHIVE_SOURCES.items()
    )

    return f"""# ETH Library MCP Server

**Version:** 0.2.0
**API-Key Status:** {key_status}
**Basis-URL:** https://api.library.ethz.ch

## Verfügbare Tools

| Tool | Beschreibung |
|------|-------------|
| `eth_search_resources` | Allgemeine Suche (30+ Mio. Ressourcen) |
| `eth_get_resource` | Einzelne Ressource via MMS-ID abrufen |
| `eth_search_archive` | Spezifisches Archiv durchsuchen |
| `eth_search_by_type` | Nach Ressourcentyp filtern |
| `eth_search_persons` | Personensuche mit Linked Data ⚠ URL-Verifikation ausstehend |
| `eth_search_education` | Kuratierte Bildungsthemen-Suche |
| `eth_library_info` | Diese Übersicht |

## Ressourcentypen (resource_type)

{rt_list}

## Verfügbare Archive (archive)

{archive_list}

## Query-Syntax

```
Feld,Operator,Wert
any,contains,Zürich        → Überall suchen
title,contains,Volksschule → Nur im Titel
creator,exact,Einstein     → Nur bei Autor
sub,contains,Pädagogik     → Nur Schlagworte

Mehrere Felder mit ; verbinden:
title,contains,Schule;sub,contains,Geschichte
```

## Lizenz

Bibliografische Metadaten: Public Domain (frei nutzbar)
API-Key: kostenlos via developer.library.ethz.ch
Kontakt: api@library.ethz.ch
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MCP RESOURCES – Statische Referenzdaten
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.resource("eth://resource-types")
async def get_resource_types() -> str:
    """Liste aller verfügbaren Ressourcentypen der ETH-Bibliothek."""
    return json.dumps(RESOURCE_TYPES, ensure_ascii=False, indent=2)


@mcp.resource("eth://archives")
async def get_archives() -> str:
    """Liste aller verfügbaren Archive und Spezialsammlungen der ETH-Bibliothek."""
    return json.dumps(ARCHIVE_SOURCES, ensure_ascii=False, indent=2)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MCP PROMPTS – Vordefinierte Workflows
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@mcp.prompt("research-workflow")
async def research_workflow(topic: str) -> str:
    """Strukturierter Recherche-Workflow für ein Thema in der ETH-Bibliothek."""
    return f"""Führe eine strukturierte Recherche zum Thema '{topic}' in der ETH-Bibliothek durch:

1. Starte mit eth_library_info für einen Überblick
2. Suche mit eth_search_resources (query: 'any,contains,{topic}', limit: 20)
3. Suche auch in den relevanten Archiven mit eth_search_archive
4. Rufe die vielversprechendsten Ressourcen via eth_get_resource für Details ab
5. Erstelle eine strukturierte Zusammenfassung der gefundenen Ressourcen

Ziel: Vollständiger Literatur- und Quellenüberblick zum Thema."""


@mcp.prompt("education-research")
async def education_research(topic: str) -> str:
    """Recherche-Workflow für Bildungsthemen (optimiert für Schulamt-Kontext)."""
    return f"""Bildungsrecherche zum Thema '{topic}' für den Schulamt-Kontext:

1. eth_search_education(topic='{topic}') – kuratierte Bildungssuche
2. eth_search_resources(query='sub,contains,{topic}', resource_type='books') – Bücher
3. eth_search_archive(archive='ETH_Hochschularchiv', query='any,contains,{topic}') – Archiv
4. Identifiziere die relevantesten Ressourcen und rufe Details ab

Fokus: Pädagogik, Schulgeschichte, Bildungsforschung, didaktische Materialien."""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EINSTIEGSPUNKT – Dual Transport (stdio + Streamable HTTP)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


if __name__ == "__main__":
    import sys

    if "--http" in sys.argv:
        port = 8000
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
        mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
    else:
        mcp.run()
