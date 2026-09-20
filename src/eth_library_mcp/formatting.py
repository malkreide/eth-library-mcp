"""
Markdown-rendering helpers for tool outputs.

Extracted from server.py per audit ARCH-004. Pure functions, no HTTP.
CH-004: every formatted resource carries an explicit Public-Domain source
attribution so downstream consumers preserve provenance.
"""

from __future__ import annotations

from typing import Any

import httpx
from mcp.types import CallToolResult, TextContent

from eth_library_mcp.client import EgressError
from eth_library_mcp.logging_config import get_logger

log = get_logger(__name__)

# CH-004: per-record source line appended to every formatted resource.
SOURCE_ATTRIBUTION = "Quelle: ETH-Bibliothek (Public Domain) · https://developer.library.ethz.ch"

# SEC-028: Die beiden Saetze, an denen die Wiederholungsfrage haengt. Sie
# stehen als Konstanten da, weil ein Test sie sonst gegen eine Formulierung
# prueft und nicht gegen eine Entscheidung.
KEINE_WIEDERHOLUNG = "Ein erneuter Versuch ändert daran nichts."
WIEDERHOLUNG_MOEGLICH = "Ein erneuter Versuch kann helfen."


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


def _wiederholungsrat(e: Exception) -> str:
    """SEC-028: Der Wiederholungsrat entscheidet sich am Diskriminator.

    Gelesen wird `retryable` — ein Feld —, nicht der Typname und nicht der
    Meldungstext. Wer das Attribut auf einer Egress-Ausnahme umstellt, stellt
    damit auch die Auskunft an den Aufrufer um; genau das prüft die Gegenprobe.
    """
    return WIEDERHOLUNG_MOEGLICH if getattr(e, "retryable", False) else KEINE_WIEDERHOLUNG


def _handle_error(
    e: Exception,
    context: str = "",
    is_search: bool = True,
) -> str:
    """
    Baut die Meldung für den **Fehlerkanal** (FID-003).

    Der Rückgabewert ist kein Tool-Ergebnis mehr: Die Werkzeuge werfen ihn als
    `ToolError`, damit der Aufrufer `isError` sieht. Bis 0.4.1 kam dieselbe
    Zeichenkette als gewöhnliches, erfolgreiches Result an — ein Transport-
    oder Autorisierungsfehler war damit von einer Auskunft über den Bestand
    nicht zu unterscheiden.

    OBS-002: Keine Leakage von Upstream-Body oder Exception-Klassennamen
    an den LLM. Details landen im stderr-JSON-Log.

    Kontext-spezifische 404-Meldung:
      is_search=True  → Endpunkt nicht gefunden (NICHT: Leermenge)
      is_search=False → Ressource mit dieser ID nicht gefunden
    """
    prefix = f"Fehler bei {context}: " if context else "Fehler: "

    # SEC-028: Der Policy-Verstoss zuerst, vor jedem anderen Zweig. Bis 0.4.1
    # fiel er in den generischen Schlusszweig und kam als «Unbekannter Fehler.
    # Bitte später erneut versuchen.» an — zeichengleich mit einem
    # ValueError, und mit einem Wiederholungsrat für eine Absage, die bei
    # jedem Versuch gleich ausfällt.
    #
    # Die Grenze dieses Zweigs, damit sie niemand fuer eine Entscheidung haelt:
    # Der Wortlaut passt zu jeder Abweisung, die dieser Guard heute erzeugt --
    # es gibt genau eine Unterklasse, und sie ist deterministisch. Kaeme je
    # eine mit `retryable = True` dazu, braucht sie einen eigenen Zweig: Der
    # Satz «keine Stoerung der Quelle» waere fuer sie falsch. Ein Zweig auf
    # Vorrat steht hier nicht, weil ihn nichts ausloesen koennte und er damit
    # ungeprueft mitliefe.
    if isinstance(e, EgressError):
        host = getattr(e, "host", "")
        genannt = f"{host!r} " if host else ""
        return (
            f"{prefix}Die Zieladresse {genannt}steht nicht in der Egress-Allow-List "
            "(ALLOWED_EGRESS_HOSTS) dieses Servers. Das ist eine "
            "Konfigurationsentscheidung, keine Störung der Quelle. "
            f"{_wiederholungsrat(e)} "
            "Soll der Host erreichbar sein, gehört er in die Allow-List "
            "(docs/network-egress.md)."
        )

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
                # FID-003: Hier stand «Keine Ergebnisse oder Endpunkt nicht
                # gefunden». Der Satz führte eine Aussage über den Bestand und
                # eine über die Konfiguration zusammen — und BUG-02 war in
                # diesem Repo genau der Fall «Route weg, HTTP 404», der hier
                # als mögliche Leermenge angeboten wurde.
                return (
                    f"{prefix}Der Suchendpunkt wurde nicht gefunden (HTTP 404). "
                    "Das ist KEINE Leermenge: Die Abfrage ist nicht beantwortet "
                    "worden, es wurde nicht gesucht. Basis-URL und Endpunkt "
                    "prüfen — eine breitere Suchanfrage hilft hier nicht."
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


def ergebnis(
    markdown: str,
    *,
    returned: int,
    total: int | None = None,
    hint: str | None = None,
) -> CallToolResult:
    """Ein Werkzeug-Ergebnis mit maschinenlesbarem nächsten Schritt (FID-003).

    Der Text-Block bleibt Markdown — er ist das, was das Modell liest.
    Daneben steht `structuredContent` mit drei Feldern:

    | Feld | Bedeutung |
    |---|---|
    | `returned` | Anzahl Datensätze **in dieser Antwort** |
    | `total` | Gesamttreffer laut Quelle, `null` wenn die Quelle keinen nennt |
    | `hint` | nächster Suchversuch — gesetzt **nur** bei `returned == 0` |

    Warum ein Feld und nicht bloss der Fliesstext: Der Hinweis war bis 0.4.1
    vom Ergebnis nicht trennbar. Ein Konsument, der wissen will, ob überhaupt
    etwas zurückkam, musste Markdown lesen.

    Die Bedingung an `hint` ist hier eine Zusicherung und keine Konvention:
    Ein Hinweis neben Treffern schickte das Modell zum Verbreitern, obwohl die
    Suche geliefert hat. Ein Fehlschlag trägt gar keinen `hint` — er verlässt
    die Werkzeuge als `ToolError` und kommt mit `isError` an.
    """
    if hint is not None and returned:
        raise ValueError(
            f"hint bei returned={returned} gesetzt — der Leermengen-Hinweis "
            "gehört ausschliesslich an eine Antwort ohne Treffer."
        )
    return CallToolResult(
        content=[TextContent(type="text", text=markdown)],
        structured_content={"returned": returned, "total": total, "hint": hint},
    )
