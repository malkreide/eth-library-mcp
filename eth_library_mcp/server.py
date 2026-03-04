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

Changelog v0.2.0:
  - BUG-01 BEHOBEN: pyproject.toml Package-Pfad korrigiert (src/ entfernt)
  - BUG-03 BEHOBEN: sort-Parameter als Literal["rank","title","author","date"]
  - BUG-04 BEHOBEN: resource_type als vollständiger Literal-Typ
  - BUG-05 BEHOBEN: Ungenutzte Konstanten aus api_client entfernt
  - BUG-06 BEHOBEN: Persons-Response-Parsing robust (data/items/hits Keys)
  - BUG-07 BEHOBEN: Kontext-spezifische 404-Fehlermeldung
  - OFFEN BUG-02: Persons-API-URL muss manuell verifiziert werden
"""

import json
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

from .api_client import (
    ARCHIVE_SOURCES,
    DISCOVERY_BASE_URL,
    PERSONS_BASE_URL,
    RESOURCE_TYPES,
    SORT_OPTIONS,
    ArchiveKey,
    ResourceType,
    SortOption,
    eth_api_request,
    format_resource_detail,
    format_resource_summary,
    handle_api_error,
    parse_persons_response,
)

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
    # BUG-03 BEHOBEN: Literal-Typ verhindert ungültige Sortierungswerte
    sort: Optional[SortOption] = Field(
        default="rank",
        description=f"Sortierung: {', '.join(SORT_OPTIONS)}",
    )
    # BUG-04 BEHOBEN: Literal-Typ verhindert stille Leerantworten bei falschem Typ
    resource_type: Optional[ResourceType] = Field(
        default=None,
        description=(
            f"Ressourcentyp-Filter. Mögliche Werte: {', '.join(RESOURCE_TYPES.keys())}"
        ),
    )
    language: Optional[str] = Field(
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

        data = await eth_api_request(DISCOVERY_BASE_URL, "/resources", api_params)

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
            lines.append(f"{i}. {format_resource_summary(doc)}")

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
        return handle_api_error(e, f"Suche nach '{params.query}'", is_search=True)


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

        data = await eth_api_request(
            DISCOVERY_BASE_URL, f"/resources/{params.mmsid}", api_params
        )

        doc = data.get("docs", [{}])[0] if data.get("docs") else data
        return format_resource_detail(doc)

    except Exception as e:
        # BUG-07 BEHOBEN: is_search=False für ID-Abruf → spezifische 404-Meldung
        return handle_api_error(e, f"Abruf MMS-ID '{params.mmsid}'", is_search=False)


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

        data = await eth_api_request(DISCOVERY_BASE_URL, "/resources", api_params)

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
            lines.append(f"{i}. {format_resource_summary(doc)}")

        if total > params.offset + len(docs):
            next_offset = params.offset + params.limit
            lines.append(
                f"\n*Weitere Einträge verfügbar. offset={next_offset} verwenden.*"
            )

        return "\n".join(lines)

    except Exception as e:
        return handle_api_error(e, f"Archivsuche '{archive_name}'", is_search=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL 4: Ressourcentyp-Suche
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class SearchByTypeInput(BaseModel):
    """Input für die typgefilterte Suche."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    # BUG-04 BEHOBEN: Literal-Typ verhindert stille Leerantworten
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

        data = await eth_api_request(DISCOVERY_BASE_URL, "/resources", api_params)

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
            lines.append(f"{i}. {format_resource_summary(doc)}")

        if total > params.offset + len(docs):
            next_offset = params.offset + params.limit
            lines.append(
                f"\n*Weitere Einträge: offset={next_offset} verwenden "
                f"({total - next_offset:,} verbleibend)*"
            )

        return "\n".join(lines)

    except Exception as e:
        return handle_api_error(e, f"Typ-Suche '{type_label}'", is_search=True)


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

    Nützlich für: Autor-Recherche, Nachlass-Suche, Identifikation von
    ETH-Professorinnen und -Professoren oder bekannten Persönlichkeiten
    in den ETH-Archiven.

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

        data = await eth_api_request(PERSONS_BASE_URL, "/persons", api_params)

        # BUG-06 BEHOBEN: Robustes Parsing via dedizierter Funktion
        persons = parse_persons_response(data)

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
        # BUG-07 BEHOBEN: is_search=True → 404 nicht als 'ID nicht gefunden' angezeigt
        return handle_api_error(e, f"Personensuche '{params.query}'", is_search=True)


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
    # BUG-04 BEHOBEN: Literal-Typ für resource_type
    resource_type: Optional[ResourceType] = Field(
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

    Durchsucht Titel, Schlagworte und Volltexte gleichzeitig nach dem Thema.
    Kombiniert Titel- und Themensuche für beste Treffer.

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

        data = await eth_api_request(DISCOVERY_BASE_URL, "/resources", api_params)

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
            lines.append(f"{i}. {format_resource_summary(doc)}")

        if total > params.limit:
            lines.append(
                f"\n*Insgesamt {total:,} Treffer. "
                f"eth_search_resources mit offset für weitere Seiten nutzen.*"
            )

        return "\n".join(lines)

    except Exception as e:
        return handle_api_error(e, f"Bildungssuche '{params.topic}'", is_search=True)


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
# EINSTIEGSPUNKT – Dual Transport (stdio + SSE)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main() -> None:
    """
    Startet den ETH Library MCP Server.
    Transport-Auswahl via Umgebungsvariable MCP_TRANSPORT:
      - 'sse': Cloud-Deployment (z.B. Render.com) mit SSE-Transport
      - Standard: stdio für lokale Claude Desktop / Claude Code Nutzung
    """
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        port = int(os.environ.get("PORT", "8000"))
        host = os.environ.get("HOST", "0.0.0.0")
        mcp.run(transport="sse", host=host, port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
