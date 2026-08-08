#!/usr/bin/env python3
"""Zeichnet auf, was ohne API-Key aufzeichenbar ist: die Routen des Gateways.

    python scripts/record_fixtures.py

WARUM ES DAS GIBT. Ein handgeschriebener Mock kodiert die Annahme seines
Autors und kann sie deshalb prinzipiell nicht widerlegen: Produktivcode und
Fixture stammen aus demselben Kopf, derselben Stunde, derselben Lektuere der
Doku. Wo beide irren, irren beide gleich, und die Suite bleibt dauerhaft
gruen.

WAS HIER NICHT AUFGEZEICHNET WIRD. Die Discovery-API verlangt einen
`ETH_LIBRARY_API_KEY`; ohne ihn kommt keine Antwort, die man datieren koennte.
`tests/fixtures/PROVENANCE.md` fuehrt diese Payloads deshalb ausdruecklich als
NICHT AUFGEZEICHNET, statt ihnen ein Datum anzuschreiben, das nicht stimmt.

WAS STATTDESSEN AUFGEZEICHNET WIRD, ist der Vertrag, den die Quelle auch ohne
Schluessel preisgibt: **welche Routen das Gateway ueberhaupt fuehrt.** Das ist
kein Ersatzgegenstand, sondern genau der, an dem der Befund haengt.

DER BEFUND. Im Code stand seit laengerem eine Notiz:

    ⚠ HINWEIS BUG-02: Der Persons-API-Endpunkt (/persons/v1/persons) gibt
    aktuell HTTP 404 zurueck. Die korrekte URL muss via
    developer.library.ethz.ch verifiziert werden.

Die offene Frage war, ob bloss die URL falsch ist. Sie laesst sich ohne
Schluessel entscheiden, und zwar mit einer Kontrolle:

    /discovery/v1/resources        -> 401  (Route da, Schluessel fehlt)
    /discovery/v1/resources/<id>   -> 401  (auch Unterpfade)
    /discovery/v1/<erfunden>       -> 404  (Route nicht da)
    /persons/v1/persons            -> 404
    /persons/v1/search             -> 404
    /persons/v1                    -> 404

Das Gateway routet also **vor** der Schluesselpruefung: Ein 401 heisst «diese
Route gibt es», ein 404 heisst «diese nicht». Damit ist die Persons-API nicht
verschlossen, sondern **weg** — kein Schluessel der Welt macht das Werkzeug
wieder funktionsfaehig.

Die Kontrollzeile mit dem erfundenen Pfad gehoert zur Aufzeichnung. Ohne sie
belegte die Messung nur, dass ICH eine 404 bekomme; mit ihr belegt sie, was
das Gateway unterscheidet. Genau diesen Unterschied — die eigene Adressliste
gegen den Bestand der Quelle — hat dieses Portfolio schon zweimal verwechselt.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(ROOT / "src"))

# Die Basis-URLs kommen aus dem Produktivcode, nicht aus einer Abschrift. Ein
# Aufzeichnungsskript, das eine andere Adresse fragt als der Server, misst den
# falschen Gegenstand — und das faellt niemandem auf, weil das Ergebnis
# plausibel aussieht.
from eth_library_mcp.client import (  # noqa: E402
    DISCOVERY_BASE_URL,
    PERSONS_BASE_URL,
)


# Jede Zeile: (Bezeichnung, URL, was sie belegen soll).
#
# `control_*` sind die Kontrollen. Ein erfundener Pfad unter einer Route, die
# es gibt, zeigt, was das Gateway mit Unbekanntem macht — und erst dadurch
# bekommt der 404 auf `/persons/...` eine Bedeutung.
def _probes() -> list[tuple[str, str, str]]:
    return [
        (
            "discovery_resources",
            f"{DISCOVERY_BASE_URL}/resources",
            "der Pfad, den fuenf der sechs Werkzeuge bauen",
        ),
        (
            "discovery_resource_by_id",
            f"{DISCOVERY_BASE_URL}/resources/991",
            "ein Unterpfad derselben Route",
        ),
        (
            "control_discovery_unknown_path",
            f"{DISCOVERY_BASE_URL}/diesen-pfad-gibt-es-nicht",
            "KONTROLLE: erfundener Pfad unter einer vorhandenen Route",
        ),
        (
            "persons_persons",
            f"{PERSONS_BASE_URL}/persons",
            "der Pfad, den das Personen-Werkzeug baute",
        ),
        (
            "persons_root",
            PERSONS_BASE_URL,
            "die Wurzel der Personen-API",
        ),
        (
            "control_persons_v2",
            f"{PERSONS_BASE_URL.replace('/v1', '/v2')}/persons",
            "KONTROLLE: eine Version, die es nie gab",
        ),
    ]


def record() -> int:
    FIXTURES.mkdir(parents=True, exist_ok=True)
    recorded_at = datetime.now(UTC).strftime("%Y-%m-%d")
    entries: list[dict] = []
    skipped: list[dict] = []

    def write(name: str, payload: object, url: str, rule: str) -> None:
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        (FIXTURES / name).write_text(text, encoding="utf-8")
        entries.append(
            {
                "name": name,
                "url": url,
                "rule": rule,
                "bytes": len(text.encode("utf-8")),
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
        )
        print(f"ok  {name:<26} {len(text.encode('utf-8')):>7} B")

    with httpx.Client(timeout=45.0, follow_redirects=True) as c:
        routes: dict[str, dict] = {}
        for label, url, why in _probes():
            # Ohne Schluessel. Das ist der Punkt: Die Unterscheidung, um die es
            # geht, macht das Gateway vor der Schluesselpruefung.
            r = c.get(url)
            routes[label] = {"url": url, "status": r.status_code, "why": why}
            print(f"    {r.status_code}  {label:<30} {url}")

        by = {k: v["status"] for k, v in routes.items()}
        if by["discovery_resources"] != 401:
            raise SystemExit(
                f"Discovery antwortet ohne Schluessel mit {by['discovery_resources']}, "
                "nicht 401 — dann traegt die Unterscheidung 401/404 nicht mehr, "
                "und der Befund gehoert neu gemessen."
            )
        if by["control_discovery_unknown_path"] != 404:
            raise SystemExit(
                "Ein erfundener Pfad antwortet nicht mehr mit 404 — ohne diese "
                "Kontrolle belegt die Messung nichts."
            )
        if by["persons_persons"] == 401:
            raise SystemExit(
                "Die Personen-API antwortet wieder mit 401 — die Route ist "
                "zurueck. Dann ist der Befund ueberholt und das Werkzeug "
                "gehoert wiederhergestellt, nicht die Fixture nachgezogen."
            )
        write(
            "api_routes.json",
            {"recorded_at": recorded_at, "routes": routes},
            "https://api.library.ethz.ch/…",
            "Statuscode je Pfad, ohne API-Key abgefragt — samt zweier "
            "Kontrollen mit erfundenen Pfaden. Erst die Kontrollen machen aus "
            "«ich bekomme 404» die Aussage «diese Route fuehrt das Gateway "
            "nicht»: Es routet vor der Schluesselpruefung, also heisst 401 "
            "«Route da» und 404 «Route weg»",
        )

    if not os.environ.get("ETH_LIBRARY_API_KEY"):
        skipped.append(
            {
                "name": "discovery_*.json",
                "url": f"{DISCOVERY_BASE_URL}/resources",
                "why": "ETH_LIBRARY_API_KEY nicht gesetzt — die Discovery-API "
                "antwortet ohne Schluessel mit HTTP 401 "
                "(`FailedToResolveAPIKey`). NICHT aufgezeichnet.",
            }
        )
        print("--  discovery_*.json         uebersprungen (kein API-Key)")

    _write_provenance(recorded_at, entries, skipped)
    print(f"\nPROVENANCE.md geschrieben, Aufzeichnungsdatum {recorded_at}")
    return 0


def _write_provenance(recorded_at: str, entries: list[dict], skipped: list[dict]) -> None:
    lines = [
        "# Herkunft der Fixtures",
        "",
        "**Erzeugt von `scripts/record_fixtures.py`. Nicht von Hand pflegen.**",
        "",
        f"Aufgezeichnet am **{recorded_at}** von `api.library.ethz.ch`.",
        "",
        "Ohne Datum ist «aufgezeichnet» nach zwei Jahren von «ausgedacht» nicht",
        "mehr zu unterscheiden — die Datei sieht gleich aus.",
        "",
        "## Was hier aufgezeichnet ist, ist der Vertrag und nicht die Antwort",
        "",
        "Die Discovery-API verlangt einen Schluessel; ohne ihn gibt es keine",
        "Antwort, die man datieren koennte. Aufzeichenbar ist trotzdem etwas,",
        "und zwar genau das, woran der Befund haengt: **welche Routen das",
        "Gateway fuehrt.** Es routet vor der Schluesselpruefung, also",
        "unterscheidet es selbst zwischen «Route da, Schluessel fehlt» (401)",
        "und «Route gibt es nicht» (404).",
        "",
        "Die beiden `control_*`-Zeilen in `api_routes.json` gehoeren zur",
        "Messung und sind kein Beiwerk. Ohne sie belegt die Aufzeichnung nur,",
        "dass jemand einen 404 bekommen hat; mit ihnen belegt sie, was das",
        "Gateway unterscheidet. Der Unterschied zwischen der eigenen",
        "Adressliste und dem Bestand der Quelle ist in diesem Portfolio schon",
        "zweimal verwechselt worden.",
        "",
    ]
    for e in entries:
        lines += [
            f"## `{e['name']}`",
            "",
            f"- **Quelle:** `{e['url']}`",
            f"- **Aufgezeichnet:** {recorded_at}",
            f"- **Auswahl:** {e['rule']}",
            f"- **Groesse:** {e['bytes']} B",
            f"- **SHA-256:** `{e['sha256']}`",
            "",
        ]
    if skipped:
        lines += ["## NICHT aufgezeichnet", ""]
        for s in skipped:
            lines += [
                f"### `{s['name']}`",
                "",
                f"- **Quelle:** `{s['url']}`",
                f"- **Grund:** {s['why']}",
                "",
            ]
        lines += [
            "Diese Payloads stehen weiterhin als Literale im Testmodul. Sie sind",
            "damit **ausgedacht** und tragen kein Datum — das ist der",
            "Ist-Zustand und keine Nachlaessigkeit dieses Laufs. Wer einen",
            "Schluessel hat, setzt `ETH_LIBRARY_API_KEY` und laesst das Skript",
            "erneut laufen.",
            "",
            "Die 401 ist am Pfad des Servers selbst gemessen, nicht an einem",
            "benachbarten — und die Kontrollen oben zeigen, dass sie",
            "«Schluessel fehlt» heisst und nicht «Route weg».",
            "",
        ]
    (FIXTURES / "PROVENANCE.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    try:
        raise SystemExit(record())
    except httpx.HTTPError as exc:
        print(f"FEHLER: Quelle nicht erreichbar: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
