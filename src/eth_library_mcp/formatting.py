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


def _mmsid(doc: dict[str, Any]) -> str:
    """Alma-MMS-ID eines Discovery-Eintrags.

    Die Discovery API liefert `context` als String (`"L"` fuer den lokalen
    Index), nicht als Objekt mit `mmsid`. Die ID steht in
    `pnx.display.mms[0]`; als Rueckfall dient `pnx.control.sourcerecordid[0]`.
    Ein `context`-Objekt mit `mmsid` wird weiterhin gelesen, falls eine
    aeltere Antwortform auftaucht.
    """
    context = doc.get("context")
    if isinstance(context, dict) and context.get("mmsid"):
        return str(context["mmsid"])
    pnx = doc.get("pnx", {})
    mms = _first(pnx.get("display", {}).get("mms", []))
    if mms:
        return mms
    return _first(pnx.get("control", {}).get("sourcerecordid", []))


def _format_resource_summary(doc: dict[str, Any]) -> str:
    """Formatiert einen einzelnen Discovery-Eintrag als kompakte Markdown-Zeile."""
    pnx = doc.get("pnx", {})
    display = pnx.get("display", {})
    addata = pnx.get("addata", {})

    title = _first(display.get("title", []))
    creator = _first(display.get("creator", []))
    date = _first(display.get("creationdate", []))
    rtype = _first(display.get("type", []))
    mmsid = _mmsid(doc)
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
    _add_field(lines, "MMS-ID", _mmsid(doc))

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


def _ist_wiederholbar(e: Exception) -> bool:
    """Die eine Stelle, an der die Wiederholungsfrage entschieden wird (SEC-028).

    Vorrang hat das Feld `retryable` — ein Wert, den Code liest, nicht der
    Typname und nicht der Meldungstext. Wer es auf einer Egress-Ausnahme
    umstellt, stellt damit auch die Auskunft an den Aufrufer um; genau das
    prüft die Gegenprobe.

    Darunter, und nur darunter, steht ein Rückfall am Typ. Die httpx-Klassen
    führen kein solches Feld, und eines anzuflanschen hiesse, fremde Klassen zu
    bemalen. Wo ein Feld da ist, gewinnt es — der Rückfall kann eine gesetzte
    Marke nicht überstimmen.

    Wiederholbar ist, was beim nächsten Versuch anders ausfallen kann: ein
    Zeitablauf, ein Verbindungsabbruch, ein 429 und ein 5xx. Alles übrige fällt
    gleich aus, ein Programmfehler in diesem Server zuallererst.
    """
    marke = getattr(e, "retryable", None)
    if marke is not None:
        return bool(marke)
    if isinstance(e, (httpx.TimeoutException, httpx.ConnectError)):
        return True
    if isinstance(e, httpx.HTTPStatusError):
        status = e.response.status_code
        return status == 429 or status >= 500
    return False


def _wiederholungsrat(e: Exception) -> str:
    """Der Satz zur Entscheidung aus `_ist_wiederholbar`.

    Er steht an JEDEM Zweig von `_handle_error`, genau einmal. Ein Zweig ohne
    ihn überliesse die Wiederholungsfrage dem Tonfall der übrigen Wörter —
    und genau daran ist SEC-028 aufgefallen.
    """
    return WIEDERHOLUNG_MOEGLICH if _ist_wiederholbar(e) else KEINE_WIEDERHOLUNG


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

    SEC-028: **Jeder** Zweig schliesst mit genau einem der beiden Sätze aus
    `_wiederholungsrat`. Die Wiederholungsfrage ist damit an jeder Ausgabe
    beantwortet und nicht bloss am Tonfall der übrigen Wörter abzulesen —
    ein Zweig, der sie offenlässt, überlässt die Entscheidung dem Modell.
    """
    prefix = f"Fehler bei {context}: " if context else "Fehler: "

    # SEC-028: Der Policy-Verstoss zuerst, vor jedem anderen Zweig. Bis 0.4.1
    # fiel er in den generischen Schlusszweig und kam als «Unbekannter Fehler.
    # Bitte später erneut versuchen.» an — zeichengleich mit einem
    # ValueError, und mit einem Wiederholungsrat für eine Absage, die bei
    # jedem Versuch gleich ausfällt. Den Wiederholungsrat im Schlusszweig hat
    # erst der 20.9.2026 geraeumt; der Satz oben zitiert 0.4.1 und nicht den
    # Stand darunter.
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
                f"{_wiederholungsrat(e)} "
                "Bitte ETH_LIBRARY_API_KEY Umgebungsvariable setzen. "
                "Kostenlose Registrierung: https://developer.library.ethz.ch"
            )
        elif status == 403:
            return f"{prefix}Zugriff verweigert (HTTP 403). {_wiederholungsrat(e)}"
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
                    f"worden, es wurde nicht gesucht. {_wiederholungsrat(e)} "
                    "Basis-URL und Endpunkt prüfen — eine breitere Suchanfrage "
                    "hilft hier nicht."
                )
            else:
                return (
                    f"{prefix}Ressource mit dieser ID nicht gefunden (HTTP 404). "
                    f"{_wiederholungsrat(e)} Bitte MMS-ID prüfen."
                )
        elif status == 429:
            return (
                f"{prefix}Rate-Limit erreicht (HTTP 429). {_wiederholungsrat(e)} Bitte kurz warten."
            )
        # OBS-002: Upstream-Response-Body NICHT durchreichen — er kann Proxy-
        # Errors, Stacktraces oder andere Internals enthalten.
        return f"{prefix}HTTP-Fehler {status}. {_wiederholungsrat(e)}"
    elif isinstance(e, httpx.TimeoutException):
        return (
            f"{prefix}Zeitüberschreitung. ETH-Bibliothek API nicht erreichbar. "
            f"{_wiederholungsrat(e)}"
        )
    elif isinstance(e, httpx.ConnectError):
        return f"{prefix}Verbindungsfehler. Internetverbindung prüfen. {_wiederholungsrat(e)}"
    # Was hier ankommt, ist keine Auskunft der Quelle mehr. Ein AttributeError,
    # ein KeyError, ein TypeError entsteht in DIESEM Server — und zwar
    # deterministisch: Dieselbe Antwort erzeugt beim naechsten Aufruf denselben
    # Fehler. Bis hierher stand an dieser Stelle «Unbekannter Fehler. Bitte
    # später erneut versuchen.», also ein Wiederholungsrat fuer eine Lage, die
    # sich durch Wiederholen nicht aendert. Der Fehler, der diesen Absatz
    # veranlasst hat, ist genau so durchgerutscht: Der MMS-ID-AttributeError
    # traf JEDE Suche mit mindestens einem Treffer und erreichte den Aufrufer
    # als Stoerung, die sich gleich legen werde.
    #
    # OBS-002 bleibt unberuehrt: Exception-Klasse und `str(e)` gehen ins
    # stderr-Log, nicht an den Aufrufer. Die Meldung sagt deshalb, WO die
    # Einzelheiten stehen, statt sie mitzuliefern — fuer den Betreiber ist das
    # der naechste Schritt, und einen anderen gibt es hier nicht.
    log.error("unhandled_exception", exc_type=type(e).__name__, exc=str(e))
    return (
        f"{prefix}Dieser Server konnte die Anfrage nicht verarbeiten. Das ist "
        "ein Fehler in diesem Server, keine Störung der Quelle. "
        f"{_wiederholungsrat(e)} "
        "Die Einzelheiten stehen im stderr-Log des Servers, unter dem Ereignis "
        "'unhandled_exception'."
    )


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
