"""Die vier Zusicherungen, die der Audit als ungedeckt gemessen hat (OPS-010).

Der Re-Audit vom 19.9.2026 fuhr sechs Mutationen gegen die Suite. Zwei
schlugen an, vier nicht:

| Mutation | Vorher |
|---|---|
| Egress-Pruefung entschaerft (`raise` -> `return`) | 0 Tests rot |
| `readOnlyHint` aus einem Werkzeug geloescht | 0 Tests rot |
| Generischer Maskierungszweig gibt `{Typ}: {e}` aus | 0 Tests rot |
| `SOURCE_ATTRIBUTION` nicht mehr angehaengt | 0 Tests rot |
| CORS-Default auf `["*"]` (Positivkontrolle) | 6 Tests rot |
| HTTP-Status-Body durchgereicht (Positivkontrolle) | 1 Test rot |

Die beiden Positivkontrollen sind wichtig: Sie belegen, dass die Methode
ueberhaupt etwas findet. Ohne sie waere «4 von 6 ungedeckt» von «der
Mutationslauf ist kaputt» nicht zu unterscheiden.

Alle vier ungedeckten Zusicherungen tragen anderswo im Katalog eigene Checks
(SEC-021, ARCH-009, OBS-002, CH-004). Sie waren also nicht vergessen, sondern
nur behauptet — im Code vorhanden, in der Doku beschrieben, von nichts
festgehalten. Das ist die Lage, vor der CLAUDE.md unter «Tests» warnt: Ein
Test, der gruen bleibt, wenn man die Implementierung entfernt, prueft nichts.

## Warum diese Tests am Verhalten messen und nicht am Quelltext

Ein `assert "readOnlyHint" in open("server.py").read()` waere gruen, solange
die Zeichenkette irgendwo steht -- auch wenn sie nie beim Aufrufer ankommt.
Gemessen wird deshalb, wo es darauf ankommt: die Annotationen am Draht, die
Egress-Sperre an der ausbleibenden Anfrage, die Maskierung an der Ausgabe.

`scripts/gegenprobe.py` faehrt genau die Mutationen aus der Tabelle und sagt,
welcher Test dabei faellt. Was hier steht, ist also nachpruefbar und nicht
bloss behauptet.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from eth_library_mcp import client
from eth_library_mcp.formatting import (
    SOURCE_ATTRIBUTION,
    _format_resource_detail,
    _format_resource_summary,
    _handle_error,
)
from eth_library_mcp.server import (
    SearchResourcesInput,
    build_http_app,
    eth_search_resources,
)

MODERN = "2026-07-28"


# ══ M1: die Egress-Allow-List (SEC-021) ═══════════════════════════════════


def test_egress_sperrt_einen_fremden_host():
    """Die Sperre selbst, an ihrer engsten Stelle.

    Der bisherige Test lief ueber das Werkzeug und akzeptierte
    `"Unbekannter Fehler" in out or "Egress denied" in out`. Das `or` macht ihn
    unabhaengig davon gruen, ob die Sperre existiert: Ohne sie laeuft die
    Anfrage in respx' `AllMockedAssertionError` und erzeugt genau den ersten
    Text. Gemessen -- die Mutation `raise` -> `return` liess die Suite
    vollstaendig gruen.
    """
    with pytest.raises(PermissionError):
        client._check_egress_allowed("https://evil.example.com/v1/x")


def test_egress_laesst_den_erlaubten_host_durch():
    """Positivkontrolle. Ohne sie bestuende der Test darueber auch dann,
    wenn die Pruefung schlicht *alles* ablehnte."""
    client._check_egress_allowed(f"{client.DISCOVERY_BASE_URL}/resources")


@respx.mock
async def test_bei_gesperrtem_host_geht_keine_anfrage_hinaus(monkeypatch):
    """Die Zusicherung, auf die es ankommt: Es wird nicht bloss ein Fehler
    gemeldet, sondern gar nichts gesendet.

    Gemessen wird das an der Routen-Zaehlung von respx, nicht am Rueckgabetext.
    Der Text taugt hier nicht: Eine gescheiterte Anfrage und eine gesperrte
    erzeugen dieselbe Meldung (SEC-028, eigener Befund). Die Zahl der
    ausgehenden Anfragen unterscheidet die beiden Faelle eindeutig.
    """
    from eth_library_mcp import server

    route = respx.get(url__startswith="https://evil.example.com").mock(
        return_value=httpx.Response(200, json={"docs": []})
    )
    monkeypatch.setattr(server, "DISCOVERY_BASE_URL", "https://evil.example.com/v1")

    await eth_search_resources(SearchResourcesInput(query="any,contains,x"))

    assert route.call_count == 0, (
        "Die Anfrage ist hinausgegangen — die Egress-Allow-List hat nicht gegriffen."
    )


@respx.mock
async def test_beim_erlaubten_host_geht_die_anfrage_hinaus():
    """Positivkontrolle zur Zeile darueber.

    Ohne sie waere `call_count == 0` auch dann erfuellt, wenn das Werkzeug
    ueberhaupt keine Anfrage mehr stellt -- die Sperre haette dann nichts
    bewiesen, und der Test bliebe trotzdem gruen.
    """
    route = respx.get(url__startswith=client.DISCOVERY_BASE_URL).mock(
        return_value=httpx.Response(200, json={"docs": []})
    )
    await eth_search_resources(SearchResourcesInput(query="any,contains,x"))
    assert route.call_count == 1


# ══ M2: die Werkzeug-Annotationen (ARCH-009) ══════════════════════════════


def _envelope(method: str) -> dict[str, Any]:
    from mcp_types import CLIENT_CAPABILITIES_META_KEY, PROTOCOL_VERSION_META_KEY

    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {
            "_meta": {
                PROTOCOL_VERSION_META_KEY: MODERN,
                CLIENT_CAPABILITIES_META_KEY: {},
            }
        },
    }


def _unwrap(response: httpx.Response) -> dict[str, Any]:
    body = response.text
    for line in body.splitlines():
        if line.startswith("data: "):
            body = line[len("data: ") :]
    return json.loads(body)


async def _werkzeuge_am_draht() -> list[dict[str, Any]]:
    """`tools/list` durch den echten ASGI-Stack.

    Bewusst nicht `dir(server)`: Die Frage ist, was beim Aufrufer ankommt.
    Eine Annotation, die im Quelltext steht und unterwegs verlorengeht, ist
    fuer einen Client nicht vorhanden.
    """
    app = build_http_app()
    async with app.router.lifespan_context(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1:8000") as c:
            antwort = await c.post(
                "/mcp",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                    "Host": "127.0.0.1:8000",
                    "MCP-Protocol-Version": MODERN,
                    "Mcp-Method": "tools/list",
                },
                json=_envelope("tools/list"),
            )
    nutzlast = _unwrap(antwort)
    assert "result" in nutzlast, f"tools/list antwortete mit {nutzlast!r}"
    return nutzlast["result"]["tools"]


@pytest.mark.anyio
async def test_jedes_werkzeug_ist_als_nur_lesend_annotiert():
    """`readOnlyHint` ist die Grundlage der Aussage, dieser Server sei read-only.

    Gemessen: Das Loeschen der Annotation aus einem einzigen Werkzeug liess die
    Suite vollstaendig gruen. Geprueft wird hier jedes Werkzeug einzeln und
    namentlich, damit die Fehlermeldung sagt, welches es war.
    """
    werkzeuge = await _werkzeuge_am_draht()
    # Positivkontrolle: es gibt ueberhaupt Werkzeuge. Eine leere Liste wuerde
    # jede Aussage darunter erfuellen.
    assert werkzeuge, "tools/list lieferte keine Werkzeuge"

    ohne = [
        w["name"] for w in werkzeuge if (w.get("annotations") or {}).get("readOnlyHint") is not True
    ]
    assert not ohne, f"Werkzeuge ohne readOnlyHint=True: {ohne}"


@pytest.mark.anyio
async def test_kein_werkzeug_behauptet_zu_schreiben_oder_zu_zerstoeren():
    """Die Gegenrichtung derselben Zusicherung.

    `readOnlyHint: True` neben einem `destructiveHint: True` waere ein
    Widerspruch, den der erste Test nicht sieht.
    """
    werkzeuge = await _werkzeuge_am_draht()
    assert werkzeuge
    widersprueche = [
        w["name"] for w in werkzeuge if (w.get("annotations") or {}).get("destructiveHint") is True
    ]
    assert not widersprueche, f"read-only, aber destructiveHint=True: {widersprueche}"


# ══ M3b: die generische Fehlermaskierung (OBS-002) ════════════════════════


class _InternerFehler(Exception):
    """Ein Ausnahmetyp, dessen Name und Text beide verraeterisch sind."""


def test_der_generische_zweig_verraet_weder_klasse_noch_text():
    """Der Zweig, der Implementierungsdetails an das Modell gaebe.

    Der HTTP-Status-Zweig daneben ist gedeckt, dieser war es nicht: Die
    Mutation auf `f"{prefix}{type(e).__name__}: {e}"` liess die Suite gruen.
    Genau diese Mutation faellt hier.
    """
    ausgabe = _handle_error(
        _InternerFehler("interner pfad /srv/geheim und ein stacktrace-fragment"),
        "Suche",
    )
    assert "_InternerFehler" not in ausgabe
    assert "interner pfad" not in ausgabe
    assert "stacktrace" not in ausgabe
    # Positivkontrolle: es kommt ueberhaupt eine Meldung, und sie nennt den
    # Kontext. Ohne diese Zeile bestuende der Test auch bei leerer Ausgabe.
    assert "Suche" in ausgabe
    assert "Unbekannter Fehler" in ausgabe


def test_die_gedeckten_zweige_bleiben_unterscheidbar():
    """Gegenkontrolle zur Maskierung: Sie darf nicht alles gleich machen.

    Ein `_handle_error`, das jede Ausnahme auf denselben Satz abbildet, waere
    nach dem Test darueber ebenfalls gruen -- und wertlos. Die Zweige mit
    eigener Aussage muessen eine eigene Aussage behalten.
    """
    zeit = _handle_error(httpx.TimeoutException("egal"), "Suche")
    verbindung = _handle_error(httpx.ConnectError("egal"), "Suche")
    generisch = _handle_error(_InternerFehler("egal"), "Suche")

    assert "Zeitüberschreitung" in zeit
    assert "Verbindungsfehler" in verbindung
    assert len({zeit, verbindung, generisch}) == 3, (
        "Die drei Fehlerarten sind nicht mehr unterscheidbar."
    )


# ══ M4: die Quellenangabe (CH-004) ════════════════════════════════════════


def _werkzeugaufrufe() -> dict[str, Any]:
    """Je Werkzeug ein Aufrufer, der die Coroutine erst beim Rufen erzeugt.

    Die Liste steht ausgeschrieben statt ueber `dir(server)` erzeugt: Jedes
    Werkzeug braucht andere Pflichtfelder, und eine Schleife, die das errät,
    wuerde bei einem neuen Werkzeug still ueberspringen statt fehlzuschlagen.
    Ein Test darunter zaehlt ab, dass hier wirklich alle stehen.

    Zurueckgegeben werden **Aufrufer**, nicht Coroutinen. Eine erste Fassung
    erzeugte sie sofort -- der Waechter-Test brauchte nur die Namen und liess
    die uebrigen ungenutzt liegen, was pro Lauf dreissig
    `coroutine was never awaited`-Warnungen erzeugte. Nichts schlug fehl, und
    genau deshalb waere es geblieben.
    """
    from eth_library_mcp import server as s

    return {
        "eth_search_resources": lambda: s.eth_search_resources(
            s.SearchResourcesInput(query="test")
        ),
        "eth_get_resource": lambda: s.eth_get_resource(s.GetResourceInput(mmsid="991234567890")),
        "eth_search_archive": lambda: s.eth_search_archive(
            s.SearchArchiveInput(archive=next(iter(s.ARCHIVE_SOURCES)), query="test")
        ),
        "eth_search_by_type": lambda: s.eth_search_by_type(
            s.SearchByTypeInput(resource_type=next(iter(s.RESOURCE_TYPES)), query="test")
        ),
        "eth_search_education": lambda: s.eth_search_education(
            s.SearchEducationInput(topic="Volksschule")
        ),
    }


@pytest.mark.parametrize("name", sorted(_werkzeugaufrufe()))
@pytest.mark.anyio
async def test_jede_werkzeugantwort_traegt_die_quellenangabe(name):
    """CH-004 verlangt die Quellenangabe an jeder ausgelieferten Antwort.

    Gemessen: Das Entfernen des Anhaengens liess die Suite gruen -- die Angabe
    konnte still verschwinden.

    Eine erste Fassung dieses Tests prueste die **Formatierer** statt der
    Antworten und fiel sofort: `_format_resource_summary` traegt die Angabe
    gar nicht. Das war kein Befund, sondern meine falsche Annahme -- angehaengt
    wird einmal pro Antwort, an fuenf Stellen (`formatting.py:107` und vier in
    `server.py`), nicht einmal pro Datensatz. Der Test misst jetzt dort, wo der
    Aufrufer sie sieht.
    """
    aufruf = _werkzeugaufrufe()[name]
    with respx.mock(assert_all_called=False) as mock:
        mock.get(url__startswith=client.DISCOVERY_BASE_URL).mock(
            return_value=httpx.Response(
                200,
                json={"docs": [{"title": "Ein Buch", "mmsid": "991"}], "info": {"total": 1}},
            )
        )
        ausgabe = await aufruf()

    # Positivkontrolle: die Antwort ist ueberhaupt eine Antwort und keine
    # Fehlermeldung. Ohne sie bestuende der Test auch dann, wenn jeder Aufruf
    # scheiterte -- sofern die Fehlermeldung zufaellig die Angabe traegt.
    assert "Fehler bei" not in ausgabe, f"{name} lieferte eine Fehlermeldung: {ausgabe[:120]}"
    assert SOURCE_ATTRIBUTION in ausgabe


def test_die_liste_der_geprueften_werkzeuge_ist_vollstaendig():
    """Der Waechter ueber der handgeschriebenen Liste.

    Ohne ihn koennte ein neues Werkzeug dazukommen, dessen Antwort die
    Quellenangabe nicht traegt -- und der Test darueber bliebe gruen, weil er
    es nie aufruft. Das ist dieselbe Klasse Luecke, die dieser PR schliesst.
    """
    from eth_library_mcp import server as s

    vorhanden = {n for n in dir(s) if n.startswith("eth_") and callable(getattr(s, n, None))}
    geprueft = set(_werkzeugaufrufe())
    # `eth_library_info` fragt keine Quelle ab und liefert keine Datensaetze.
    ungeprueft = vorhanden - geprueft - {"eth_library_info"}
    assert not ungeprueft, f"Werkzeuge ohne Quellenangaben-Test: {sorted(ungeprueft)}"


def test_der_detailformatierer_traegt_die_quellenangabe():
    """`_format_resource_detail` haengt sie selbst an (`formatting.py:107`).

    Die vier Suchwerkzeuge tun es in `server.py`; dieser Formatierer ist die
    fuenfte Stelle und braucht seinen eigenen Nachweis.
    """
    assert SOURCE_ATTRIBUTION in _format_resource_detail({"title": "Ein Buch", "mmsid": "991"})


def test_der_kurzformatierer_traegt_sie_bewusst_nicht():
    """Festgehalten, damit die Aufteilung nicht fuer einen Fehler gehalten wird.

    `_format_resource_summary` erzeugt eine Zeile innerhalb einer Liste. Die
    Angabe steht einmal unter der ganzen Antwort, nicht hinter jedem Eintrag --
    sonst stuende sie bei zwanzig Treffern zwanzigmal da. Wer das aendert,
    aendert eine Entscheidung und nicht bloss eine Zeile.
    """
    assert SOURCE_ATTRIBUTION not in _format_resource_summary({"title": "Ein Buch"})


def test_die_quellenangabe_nennt_lizenz_und_herkunft():
    """Die Konstante selbst, damit sie nicht zu einem leeren String verkuemmert.

    Ohne diese Zeile bestuende der Test darueber auch bei
    `SOURCE_ATTRIBUTION = ""` -- eine leere Zeichenkette steckt in jeder
    Ausgabe.
    """
    assert "ETH-Bibliothek" in SOURCE_ATTRIBUTION
    assert "Public Domain" in SOURCE_ATTRIBUTION
    assert "developer.library.ethz.ch" in SOURCE_ATTRIBUTION
