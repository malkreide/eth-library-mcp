"""Zugriff auf die aufgezeichneten Fixtures unter ``tests/fixtures/``.

Quelle, Datum, Auswahlregel und SHA-256 je Datei stehen in
``tests/fixtures/PROVENANCE.md``, geschrieben von
``scripts/record_fixtures.py``.

Zwei Dinge stehen dort ausdruecklich, weil sie hier nicht verschwiegen werden
duerfen: Die Discovery-Payloads sind **nicht** aufgezeichnet — die API verlangt
einen Schluessel —, und was stattdessen aufgezeichnet ist, ist der Vertrag: die
Routen, die das Gateway fuehrt, samt Kontrollen.

Ein fehlender Name ist ein Fehler und keine leere Struktur. Ein Loader, der bei
einem Tippfehler ``{}`` zurueckgibt, erzeugt einen Test, der nichts mehr prueft
und trotzdem Erfolg meldet.
"""

from __future__ import annotations

import copy
import json
from functools import cache
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@cache
def _load(name: str) -> Any:
    path = FIXTURES / name
    if not path.is_file():
        available = sorted(p.name for p in FIXTURES.glob("*.json"))
        raise FileNotFoundError(
            f"Keine Fixture {name!r} unter {FIXTURES}. Vorhanden: {available}. "
            "Neu aufzeichnen mit `python scripts/record_fixtures.py`."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def payload(name: str) -> Any:
    return copy.deepcopy(_load(name))


def route_status(label: str) -> int:
    """Der aufgezeichnete Statuscode einer Gateway-Route."""
    routes = _load("api_routes.json")["routes"]
    if label not in routes:
        raise KeyError(f"Keine Route {label!r} aufgezeichnet. Vorhanden: {sorted(routes)}.")
    return int(routes[label]["status"])
