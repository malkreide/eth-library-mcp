"""OBS-002: Der API-Schluessel darf in keinem Log stehen.

Der Audit vom 19.9.2026 hat gemessen, dass er in jedem stand. Nicht im
eigenen Log dieses Servers -- `client.py` schreibt `has_key=True` --, sondern
in dem von httpx, das die vollstaendige URL samt `?apikey=...` auf INFO
protokolliert, sobald `configure_logging()` den Root-Logger scharf stellt:

    HTTP Request: GET https://api.library.ethz.ch/discovery/v1/resources
    ?q=test&apikey=sk-GEHEIM-TESTSCHLUESSEL-999 "HTTP/1.1 200 OK"

`SECURITY.md` und `docs/secret-management.md` sagten zu diesem Zeitpunkt beide
woertlich, der Schluessel werde nie geloggt.

## Warum jeder Test hier eine Positivkontrolle hat

Ein Test, der nur prueft, dass eine Zeichenkette *fehlt*, besteht auch dann,
wenn ueberhaupt nichts geloggt wurde -- weil der Logger falsch konfiguriert
ist, weil die Anfrage nie lief, weil die Sonde kaputt ist. Er misst dann die
eigene Wirkungslosigkeit und meldet sie als Erfolg. Deshalb prueft jeder Test
hier zusaetzlich, dass die erwartete Zeile **da** ist und nur der Schluessel
darin ersetzt wurde.

Das ist dieselbe Falle wie in CLAUDE.md unter «Eine Null ist eine Behauptung»:
«0 Treffer» heisst entweder «nichts da» oder «Muster greift nicht», und ohne
Gegenkontrolle sind die beiden ununterscheidbar.
"""

from __future__ import annotations

import logging
import re

import httpx
import pytest
import respx

from eth_library_mcp import client
from eth_library_mcp.logging_config import (
    PLATZHALTER,
    configure_logging,
    get_logger,
    redigiere_datensatz,
    redigiere_geheimnisse,
)

SCHLUESSEL = "sk-GEHEIM-TESTSCHLUESSEL-999"


@pytest.fixture(autouse=True)
def _schluessel_in_der_umgebung(monkeypatch):
    monkeypatch.setenv("ETH_LIBRARY_API_KEY", SCHLUESSEL)


# ── Die Funktion selbst ────────────────────────────────────────────────────


def test_der_wert_aus_der_umgebung_wird_ersetzt():
    text = f"irgendwas {SCHLUESSEL} irgendwas"
    assert SCHLUESSEL not in redigiere_geheimnisse(text)
    assert PLATZHALTER in redigiere_geheimnisse(text)


def test_auch_ein_fremder_wert_unter_bekanntem_parameternamen_faellt(monkeypatch):
    """Das Muster deckt ab, was der Wertvergleich nicht sehen kann.

    Ein Schluessel, der nicht aus dieser Umgebung stammt -- URL-kodiert, aus
    einer fremden Konfiguration, aus einem Testfixture -- wird vom
    `str.replace`-Weg nie gefunden. Ohne den Musterweg waere die Redaktion
    genau dort blind, wo sie niemand prueft.
    """
    monkeypatch.delenv("ETH_LIBRARY_API_KEY", raising=False)
    text = "GET https://example.test/x?q=1&apikey=voellig-anderer-wert"
    redigiert = redigiere_geheimnisse(text)
    assert "voellig-anderer-wert" not in redigiert
    # Positivkontrolle: der Rest der Zeile ueberlebt, die Redaktion frisst
    # nicht den ganzen Text.
    assert "https://example.test/x?q=1" in redigiert


def test_ein_kurzer_wert_zerlegt_die_zeile_nicht(monkeypatch):
    """Ein einzeichiger Schluessel darf nicht jedes Vorkommen ersetzen.

    Ohne die Laengenpruefung wuerde `str.replace("a", ...)` jede Zeile
    unlesbar machen -- und zwar still, weil nichts fehlschlaegt.
    """
    monkeypatch.setenv("ETH_LIBRARY_API_KEY", "a")
    text = "GET https://api.library.ethz.ch/discovery/v1/resources?q=karte"
    assert redigiere_geheimnisse(text) == text


def test_ohne_schluessel_in_der_umgebung_bleibt_harmloser_text_unveraendert(monkeypatch):
    monkeypatch.delenv("ETH_LIBRARY_API_KEY", raising=False)
    text = "server_starting transport=any"
    assert redigiere_geheimnisse(text) == text


# ── Der stdlib-Weg: fremde Bibliotheken, allen voran httpx ─────────────────


def test_ein_url_objekt_in_den_argumenten_wird_redigiert():
    """httpx uebergibt seine URL als Objekt, nicht als Zeichenkette.

    Wer nur `isinstance(wert, str)` prueft, laesst genau den gemessenen Fall
    durch -- die URL kommt als `httpx.URL` in `record.args`.
    """
    datensatz = logging.LogRecord(
        name="httpx",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='HTTP Request: %s %s "%s %d %s"',
        args=(
            "GET",
            httpx.URL(f"https://api.library.ethz.ch/x?q=1&apikey={SCHLUESSEL}"),
            "HTTP/1.1",
            200,
            "OK",
        ),
        exc_info=None,
    )
    gerendert = redigiere_datensatz(datensatz).getMessage()
    assert SCHLUESSEL not in gerendert
    # Positivkontrolle: die Zeile ist noch die Zeile.
    assert "api.library.ethz.ch" in gerendert
    assert "200" in gerendert


@pytest.mark.anyio
async def test_der_schluessel_steht_nach_einer_echten_anfrage_in_keinem_handler(caplog):
    """Der gemessene Fall, End-to-End durch `_http_get`.

    Gemessen wird ueber `caplog`, und das ist hier kein Behelf, sondern die
    schaerfere Messung: `caplog` haengt einen **eigenen** Handler ein, der von
    der Redaktion nichts weiss. Sieht selbst der den Schluessel nicht, dann
    ist er schon vor jedem Handler verschwunden -- genau die Zusicherung, die
    die Datensatz-Fabrik gibt und die ein Handler-Filter nicht geben konnte.

    Positivkontrolle im selben Lauf: die httpx-Zeile MUSS erscheinen. Sonst
    bestuende dieser Test auch dann, wenn das Logging ganz abgeschaltet waere.
    """
    configure_logging()

    with caplog.at_level(logging.INFO, logger="httpx"):
        with respx.mock(assert_all_called=False) as mock:
            mock.get(url__startswith="https://api.library.ethz.ch").mock(
                return_value=httpx.Response(200, json={"docs": []})
            )
            await client._http_get(client.DISCOVERY_BASE_URL, "/resources", {"q": "test"})

    assert "HTTP Request" in caplog.text, (
        "httpx hat gar nicht geloggt — dieser Test kann den Schluessel dann "
        "nicht vermissen, weil nichts da ist, worin er stehen koennte."
    )
    assert SCHLUESSEL not in caplog.text
    assert f"apikey={PLATZHALTER}" in caplog.text


# ── Der structlog-Weg: die eigenen Logzeilen ───────────────────────────────


@pytest.mark.anyio
async def test_auch_die_eigene_logzeile_wird_redigiert(capfd):
    """structlog schreibt direkt nach stderr und kommt an keinem Handler vorbei.

    Deshalb genuegt der stdlib-Filter allein nicht: `_handle_error` loggt
    `exc=str(e)`, und die Textform mancher httpx-Ausnahmen fuehrt die URL mit.
    """
    configure_logging()
    get_logger("sonde").error(
        "unhandled_exception",
        exc=f"boom for url https://api.library.ethz.ch/x?q=1&apikey={SCHLUESSEL}",
    )

    stderr = capfd.readouterr().err
    assert "unhandled_exception" in stderr, "die Zeile fehlt ganz — Sonde defekt"
    assert SCHLUESSEL not in stderr
    assert PLATZHALTER in stderr


def test_wiederholtes_konfigurieren_stapelt_die_fabrik_nicht():
    """`basicConfig` ist beim zweiten Aufruf ein No-op, `setLogRecordFactory` nicht.

    Ohne die Markierung wickelte jeder Aufruf die vorige Fabrik erneut ein.
    Das Ergebnis bliebe richtig — redigierter Text noch einmal zu redigieren
    aendert nichts —, aber die Kette waechst mit jeder Konfiguration, und
    irgendwann laeuft jede Logzeile durch zwanzig Ebenen. Ein Leck, das nie
    fehlschlaegt und deshalb nie auffaellt.
    """
    configure_logging()
    fabrik_nach_erstem = logging.getLogRecordFactory()
    configure_logging()
    configure_logging()
    assert logging.getLogRecordFactory() is fabrik_nach_erstem


# ── Die Zusicherung in der Dokumentation ───────────────────────────────────


def test_die_dokumentation_behauptet_die_redaktion_nicht_ohne_deckung():
    """`SECURITY.md` sagt, der Schluessel werde nie geloggt.

    Der Satz war zwei Releases lang falsch. Er ist jetzt gedeckt — dieser Test
    haelt fest, dass er ueberhaupt noch dasteht, damit die Zusicherung nicht
    still verschwindet, waehrend die Mechanik bleibt (oder umgekehrt).
    """
    from pathlib import Path

    text = Path(__file__).resolve().parent.parent / "SECURITY.md"
    flach = re.sub(r"\s+", " ", text.read_text(encoding="utf-8"))
    assert "never logged" in flach
