"""
ETH Library API Client
======================
Gemeinsamer HTTP-Client und Hilfsfunktionen für alle ETH-Bibliothek APIs.
Basiert auf dem gleichen Muster wie der Zurich Open Data MCP Server.

Changelog v0.3.0:
  - BUG-02 BEHOBEN: Persons-API korrekt implementiert (/{code} + /enrichment)
  - NEU: PersonsSourceCode Typ-Alias für Datenpools (hsa, ba, erara, mfa, sar)
  - NEU: PERSONS_SOURCES Dict mit Datenpool-Beschreibungen
  - NEU: format_person_enrichment() für Persons-Enrichment-Darstellung

Changelog v0.2.0:
  - BUG-05: Ungenutzte Konstanten RESEARCH_BASE_URL, ETHORAMA_BASE_URL entfernt
  - BUG-06: Persons-Response-Parsing robust gegen weitere Schlüssel ('data', 'items', 'hits')
  - BUG-07: Kontext-spezifische 404-Fehlermeldung (Suche vs. ID-Abruf)
  - NEU: Typ-Aliase SortOption, ResourceType, ArchiveKey für Literal-Validierung
"""

import logging
import os
from typing import Any, Literal

import httpx

# ─── Logging ──────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ─── API-Konfiguration ────────────────────────────────────────────────────────

DISCOVERY_BASE_URL = "https://api.library.ethz.ch/discovery/v1"
PERSONS_BASE_URL = "https://api.library.ethz.ch/persons/v1"
# BUG-02 BEHOBEN (v0.3.0): Korrekte Endpunkte laut OpenAPI-Spec:
#   GET /{code}       → Personenliste aus Datenpool (hsa, ba, erara, mfa, sar)
#   GET /enrichment   → Personen-Enrichment via Wikidata QID oder GND-ID
# Quelle: https://raw.githubusercontent.com/eth-library/opendata-apis/main/persons-v1.yaml

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

PersonsSourceCode = Literal["hsa", "ba", "erara", "mfa", "sar"]

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

# ─── Personen-Datenpools (Persons API v1) ────────────────────────────────────

PERSONS_SOURCES: dict[str, str] = {
    "hsa": "Hochschularchiv (HSA)",
    "ba": "E-Pics Bildarchiv (BA)",
    "erara": "e-rara",
    "mfa": "Max Frisch-Archiv (MFA)",
    "sar": "Alle Quellen (HSA + BA + e-rara + MFA)",
}

# ─── Sortiermöglichkeiten ─────────────────────────────────────────────────────

SORT_OPTIONS = list(SortOption.__args__)  # type: ignore[attr-defined]


# ─── HTTP-Client ──────────────────────────────────────────────────────────────


def get_api_key() -> str | None:
    """API-Key aus Umgebungsvariable lesen (graceful degradation)."""
    return os.environ.get("ETH_LIBRARY_API_KEY")


async def eth_api_request(
    base_url: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Zentrale Funktion für alle ETH-Bibliothek API-Anfragen.
    Fügt automatisch den API-Key hinzu und behandelt Fehler konsistent.
    """
    api_key = get_api_key()

    request_params: dict[str, Any] = params or {}
    if api_key:
        request_params["apikey"] = api_key

    url = f"{base_url}{path}"

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.get(url, params=request_params)
        response.raise_for_status()
        return response.json()


# ─── Formatierungshilfsfunktionen ─────────────────────────────────────────────


def format_resource_summary(doc: dict[str, Any]) -> str:
    """
    Formatiert einen einzelnen Discovery-Eintrag als kompakte Markdown-Zeile.
    """
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


def format_resource_detail(doc: dict[str, Any]) -> str:
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


def parse_persons_response(data: Any) -> list[dict[str, Any]]:
    """
    Robustes Parsing der Persons-API-Antwort.

    BUG-06: Unterstützt verschiedene Response-Strukturen der ETH Persons API:
    - Direkte Liste: [...]
    - Wrapper mit 'persons', 'results', 'data', 'items' oder 'hits' Key
    Loggt eine Warnung wenn keine bekannte Struktur erkannt wird.
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


def format_person_enrichment(data: dict[str, Any]) -> str:
    """
    Formatiert Persons-Enrichment-Daten als Markdown-Dokument.

    Die Enrichment-API liefert angereicherte Informationen aus:
    Wikidata, Metagrid, DNB Entityfacts, beacon.findbuch.
    """
    lines: list[str] = []

    # Name aus verschiedenen möglichen Feldern extrahieren
    name = (
        data.get("name")
        or data.get("label")
        or data.get("preferredName")
        or "Unbekannt"
    )
    lines.append(f"# {name}")
    lines.append("")

    # Lebensdaten
    birth = data.get("birthDate", data.get("dateOfBirth", ""))
    death = data.get("deathDate", data.get("dateOfDeath", ""))
    if birth or death:
        lines.append(f"**Lebensdaten:** {birth}–{death}")

    # Beschreibung / Biografie
    desc = data.get("description", data.get("biographicalOrHistoricalInformation", ""))
    if desc:
        lines.append(f"**Beschreibung:** {desc[:500]}")

    # Berufe / Tätigkeiten
    professions = data.get("professionOrOccupation", [])
    if professions:
        if isinstance(professions, list):
            lines.append(f"**Beruf:** {', '.join(str(p) for p in professions[:5])}")
        else:
            lines.append(f"**Beruf:** {professions}")

    # Externe Links
    links_section: list[str] = []
    wikidata = data.get("wikidata", data.get("wikidataId", data.get("qid", "")))
    if wikidata:
        qid = wikidata if wikidata.startswith("Q") else wikidata
        links_section.append(f"- [Wikidata](https://www.wikidata.org/wiki/{qid})")

    gnd = data.get("gnd", data.get("gndId", data.get("gndIdentifier", "")))
    if gnd:
        links_section.append(
            f"- [GND / DNB](https://d-nb.info/gnd/{gnd}) (ID: `{gnd}`)"
        )

    metagrid = data.get("metagrid", data.get("metagridUrl", ""))
    if metagrid:
        links_section.append(f"- [Metagrid]({metagrid})")

    if links_section:
        lines.append("")
        lines.append("**Externe Links:**")
        lines.extend(links_section)

    return "\n".join(filter(None, lines))


def handle_api_error(
    e: Exception,
    context: str = "",
    is_search: bool = True,
) -> str:
    """
    Einheitliche, hilfreiche Fehlermeldungen – kein Hard-Failure.

    BUG-07: Kontext-spezifische 404-Meldung:
      is_search=True  → 'Keine Ergebnisse oder Endpunkt nicht gefunden'
      is_search=False → 'Ressource mit dieser ID nicht gefunden'

    Muster: graceful degradation aus dem Swiss Transport MCP übernommen.
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


# ─── Private Hilfsfunktionen ──────────────────────────────────────────────────


def _first(lst: list[Any]) -> str:
    """Erstes Element einer Liste als String, leer wenn nicht vorhanden."""
    return str(lst[0]) if lst else ""


def _add_field(lines: list[str], label: str, value: str) -> None:
    """Fügt ein Feld zur Detailansicht hinzu, falls vorhanden."""
    if value:
        lines.append(f"**{label}:** {value}")
