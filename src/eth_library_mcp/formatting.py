"""
Markdown-rendering helpers for tool outputs.

Extracted from server.py per audit ARCH-004. Pure functions, no HTTP.
CH-004: every formatted resource carries an explicit Public-Domain source
attribution so downstream consumers preserve provenance.
"""

from __future__ import annotations

from typing import Any

import httpx

from eth_library_mcp.logging_config import get_logger

log = get_logger(__name__)

# CH-004: per-record source line appended to every formatted resource.
SOURCE_ATTRIBUTION = (
    "Quelle: ETH-Bibliothek (Public Domain) · "
    "https://developer.library.ethz.ch"
)


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

    # CH-004: source attribution on every record
    lines.append("")
    lines.append(f"*{SOURCE_ATTRIBUTION}*")

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

        log.warning(
            "persons_api_unknown_structure",
            known_keys=["persons", "results", "data", "items", "hits"],
            received_keys=list(data.keys()),
        )

    return []


def _handle_error(
    e: Exception,
    context: str = "",
    is_search: bool = True,
) -> str:
    """
    Einheitliche, hilfreiche Fehlermeldungen – kein Hard-Failure.
    OBS-002: Keine Leakage von Upstream-Body oder Exception-Klassennamen
    an den LLM. Details landen in stderr-JSON-Log.

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
        # OBS-002: Upstream-Response-Body NICHT durchreichen — er kann Proxy-
        # Errors, Stacktraces oder andere Internals enthalten.
        return f"{prefix}HTTP-Fehler {status}."
    elif isinstance(e, httpx.TimeoutException):
        return f"{prefix}Zeitüberschreitung. ETH-Bibliothek API nicht erreichbar."
    elif isinstance(e, httpx.ConnectError):
        return f"{prefix}Verbindungsfehler. Internetverbindung prüfen."
    # OBS-002: Generischer Fall — interne Exception-Klasse + str(e) leaken
    # Implementations-Details an den LLM. Stattdessen generische Meldung,
    # Details landen in stderr-Log.
    log.error("unhandled_exception", exc_type=type(e).__name__, exc=str(e))
    return f"{prefix}Unbekannter Fehler. Bitte später erneut versuchen."
