"""Fehlerkanal (FID-003) und Egress-Taxonomie (SEC-028).

Zwei Befunde des Re-Audits vom 19.9.2026, beide `high`, beide an derselben
Stelle: Ein Fehlschlag der Quelle erreichte den Aufrufer als gewoehnliches,
erfolgreiches Tool-Result.

## FID-003 -- Leermenge ist nicht Abwesenheit

Gemessen am 19.9.2026 ueber den echten ASGI-Stack: Ein `httpx.ConnectError`
lieferte `isError: False` mit dem Text «Verbindungsfehler. Internetverbindung
pruefen.» im Ergebnisfeld. Die Positivkontrolle derselben Messung zeigte, dass
der Fehlerkanal existiert und funktioniert -- ein Validierungsfehler kam sehr
wohl mit `isError: True` an. Der Server hat ihn fuer Upstream-Ausfaelle nur nie
benutzt.

Dazu kam die 404-Vermischung: «Keine Ergebnisse oder Endpunkt nicht gefunden
(HTTP 404)» fuehrte eine Aussage ueber den Bestand und eine ueber die
Konfiguration in einem Satz zusammen. BUG-02 war in diesem Repo genau der Fall
«Route weg, HTTP 404» -- der hier als moegliche Leermenge angeboten wurde.

## SEC-028 -- Policy-Verstoss ist keine Stoerung

Gemessen: `_handle_error(PermissionError("Egress denied: ..."), "Suche")`
ergab «Unbekannter Fehler. Bitte spaeter erneut versuchen.» -- zeichengleich
mit dem Ergebnis fuer `ValueError("boom")`, und mit einem Wiederholungsrat fuer
eine Absage, die bei jedem Versuch gleich ausfaellt.

## Warum die Messungen durch den ASGI-Stack laufen

`isError` entsteht in der SDK-Schicht und ist am Rueckgabewert der Funktion
nicht zu sehen. Ein Test, der die Funktion direkt ruft, kann die Zusicherung
deshalb nicht widerlegen -- genau der Testtyp, der den Befund zwei Releases
lang hat stehen lassen.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from eth_library_mcp import client
from eth_library_mcp.client import EgressError, EgressPolicyViolation
from eth_library_mcp.formatting import (
    KEINE_WIEDERHOLUNG,
    WIEDERHOLUNG_MOEGLICH,
    _handle_error,
    ergebnis,
)
from tests.hilfen import aufruf_am_draht, strukturiert, text

SUCHE = {"params": {"query": "any,contains,Test"}}


def _treffer(anzahl: int = 1) -> dict:
    return {
        "docs": [{"pnx": {"display": {"title": ["Ein Buch"]}}}] * anzahl,
        "info": {"total": anzahl},
    }


async def _am_draht(antwort=None, seite=None) -> dict:
    """Eine Suche durch den vollen Stack, mit gemockter Quelle."""
    with respx.mock(assert_all_called=False) as mock:
        route = mock.get(url__startswith=client.DISCOVERY_BASE_URL)
        route.mock(side_effect=seite) if seite is not None else route.mock(return_value=antwort)
        return await aufruf_am_draht("eth_search_resources", SUCHE)


# ══ FID-003: Fehlschlaege landen im Fehlerkanal ═══════════════════════════


@pytest.mark.anyio
async def test_ein_treffer_ist_kein_fehler():
    """Positivkontrolle, und sie steht bewusst zuerst.

    Ohne sie waere jede `isError`-Zusicherung darunter auch dann erfuellt,
    wenn der Server auf *alles* mit einem Fehler antwortete. Ein Kanal, der
    immer anschlaegt, unterscheidet nichts.
    """
    resultat = await _am_draht(httpx.Response(200, json=_treffer()))
    assert resultat["isError"] is False
    assert resultat["structuredContent"]["returned"] == 1


@pytest.mark.anyio
async def test_eine_leermenge_ist_kein_fehler():
    """Die zweite Haelfte derselben Abgrenzung.

    Null Treffer ist ein gueltiges Ergebnis. Es als `isError` zu melden waere
    das Gegenstueck des Befunds -- und im Katalog ebenfalls ein Fail
    («Leermenge als isError maskiert»).
    """
    resultat = await _am_draht(httpx.Response(200, json={"docs": [], "info": {"total": 0}}))
    assert resultat["isError"] is False
    assert resultat["structuredContent"]["returned"] == 0
    assert resultat["structuredContent"]["hint"], (
        "Die Leermenge traegt keinen naechsten Schritt — das Modell muesste raten."
    )


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("bezeichnung", "antwort", "seite"),
    [
        ("HTTP 401", httpx.Response(401, text="unauthorized"), None),
        ("HTTP 403", httpx.Response(403, text="forbidden"), None),
        ("HTTP 404", httpx.Response(404, text="nope"), None),
        ("HTTP 429", httpx.Response(429, text="slow down"), None),
        ("HTTP 500", httpx.Response(500, text="boom"), None),
        ("Verbindungsfehler", None, httpx.ConnectError("kaputt")),
        ("Zeitueberschreitung", None, httpx.TimeoutException("zu lange")),
    ],
)
async def test_ein_upstream_ausfall_kommt_mit_iserror_an(bezeichnung, antwort, seite):
    """Die Zusicherung des Befunds, je Fehlerklasse einzeln.

    Parametrisiert und nicht in einer Schleife, damit die Fehlermeldung sagt,
    welche Klasse zurueckgefallen ist. Eine Schleife haette beim ersten
    Fehlschlag aufgehoert und die uebrigen ungeprueft gelassen.
    """
    resultat = await _am_draht(antwort, seite)
    assert resultat["isError"] is True, f"{bezeichnung} kam als erfolgreiches Ergebnis an"
    # Und er traegt keine Felder, die nach einer Auskunft ueber den Bestand
    # aussehen: kein `returned: 0`, kein Leermengen-Hinweis.
    assert resultat.get("structuredContent") is None, (
        f"{bezeichnung} traegt strukturierte Ergebnisfelder — "
        "ein Fehlschlag ist keine Aussage ueber den Bestand."
    )


@pytest.mark.anyio
async def test_der_404_auf_einer_suche_wird_nicht_als_leermenge_erzaehlt():
    """Die Vermischung, gegen die FID-003 steht.

    Bis 0.4.1 lautete der Zweig woertlich «Keine Ergebnisse oder Endpunkt
    nicht gefunden (HTTP 404). Bitte Suchanfrage oder API-Endpunkt pruefen.»
    Ein Modell konnte daraus nicht schliessen, ob es breiter suchen oder die
    Konfiguration pruefen soll -- und BUG-02 war in diesem Repo genau der
    zweite Fall.
    """
    resultat = await _am_draht(httpx.Response(404, text="nope"))
    meldung = resultat["content"][0]["text"]

    assert resultat["isError"] is True
    assert "Keine Ergebnisse" not in meldung, "Der 404 wird weiterhin als Leermenge angeboten"
    assert "nicht gefunden" in meldung and "Endpunkt" in meldung
    # Der naechste Schritt zeigt auf die Konfiguration, nicht auf die Query.
    assert "Basis-URL" in meldung


def test_der_404_auf_einem_einzelabruf_zeigt_weiter_auf_die_id():
    """Gegenkontrolle zur Zeile darueber: Der Kontext bleibt unterscheidbar.

    Ein `_handle_error`, das beide 404-Lagen auf denselben Satz abbildet,
    waere nach dem Test darueber ebenfalls gruen. Beim Einzelabruf ist die
    MMS-ID sehr wohl der naechste Schritt.
    """
    suche = _handle_error(_status(404), "Suche", is_search=True)
    abruf = _handle_error(_status(404), "Abruf", is_search=False)
    assert "MMS-ID" in abruf
    assert "MMS-ID" not in suche
    assert suche != abruf


def _status(code: int) -> httpx.HTTPStatusError:
    anfrage = httpx.Request("GET", "https://api.library.ethz.ch/discovery/v1/resources")
    return httpx.HTTPStatusError(
        "egal", request=anfrage, response=httpx.Response(code, request=anfrage)
    )


# ══ FID-003: der Hinweis haengt an der Leermenge, nicht am Ergebnis ═══════


def test_ein_hinweis_neben_treffern_wird_abgewiesen():
    """`ergebnis()` laesst die Kombination gar nicht erst entstehen.

    Ein `hint` neben Treffern schickt das Modell zum Verbreitern, obwohl die
    Suche geliefert hat. Die Bedingung steht als Zusicherung im Bauer und
    nicht als Konvention in einem Kommentar -- eine Konvention haette den
    Befund nicht verhindert, der diesen Test veranlasst hat.
    """
    with pytest.raises(ValueError, match="ohne Treffer"):
        ergebnis("egal", returned=3, hint="breiter suchen")


def test_der_bauer_laesst_die_beiden_erlaubten_faelle_durch():
    """Positivkontrolle. Ohne sie bestuende der Test darueber auch bei einem
    `ergebnis()`, das jede Kombination abweist."""
    ergebnis("egal", returned=3)
    ergebnis("egal", returned=0, hint="breiter suchen")


# ══ SEC-028: Policy-Verstoss und Stoerung bleiben unterscheidbar ══════════


def test_der_policy_verstoss_nennt_die_allow_list_und_den_host():
    """Bis 0.4.1 fiel er in den generischen Schlusszweig.

    Gemessen war die Ausgabe «Fehler bei Suche: Unbekannter Fehler. Bitte
    spaeter erneut versuchen.» -- zeichengleich mit der fuer ein
    `ValueError('boom')`.
    """
    meldung = _handle_error(EgressPolicyViolation("evil.example.com"), "Suche")
    assert "evil.example.com" in meldung
    assert "ALLOWED_EGRESS_HOSTS" in meldung
    assert "Unbekannter Fehler" not in meldung


def test_der_policy_verstoss_bekommt_keinen_wiederholungsrat():
    """Die Umkehrung von Kriterium 3: Eine deterministische Absage darf nicht
    wie eine Stoerung klingen.

    «Bitte spaeter erneut versuchen» war fuer eine Konfigurationsentscheidung
    falsch -- die Absage faellt bei jedem Versuch gleich aus.
    """
    meldung = _handle_error(EgressPolicyViolation("evil.example.com"), "Suche")
    assert KEINE_WIEDERHOLUNG in meldung
    assert WIEDERHOLUNG_MOEGLICH not in meldung
    assert "später erneut" not in meldung


def test_der_wiederholungsrat_haengt_am_diskriminator_und_nicht_am_typnamen():
    """Der Kern von SEC-028, an der Stelle gemessen, wo er wirkt.

    Gelesen wird `retryable` -- ein Feld. Wer es umstellt, stellt die Auskunft
    an den Aufrufer mit um. Eine Unterscheidung ueber den Meldungstext wuerde
    bei der ersten Umformulierung brechen; diese hier nicht.

    Der Typ unten ist derselbe `EgressError` mit demselben Namen. Faellt der
    Test, entscheidet die Meldung an etwas anderem als am Diskriminator.
    """

    class _TransienteAbweisung(EgressError):
        retryable = True

    voruebergehend = _TransienteAbweisung("egal")
    voruebergehend.host = "api.library.ethz.ch"

    assert WIEDERHOLUNG_MOEGLICH in _handle_error(voruebergehend, "Suche")
    assert KEINE_WIEDERHOLUNG in _handle_error(EgressPolicyViolation("evil.example.com"), "Suche")


def test_die_transiente_lage_nennt_die_egress_policy_nicht():
    """Negative Kontrolle aus Modus 2 des Checks.

    Ein Verbindungsfehler schickt niemanden in die Allow-List. Wer dort sucht,
    sucht eine Zeile fuer einen Host, der erlaubt ist -- genau der zweite
    Schaden aus dem Befund, der SEC-028 ausgeloest hat.
    """
    for stoerung in (httpx.ConnectError("kaputt"), httpx.TimeoutException("zu lange")):
        meldung = _handle_error(stoerung, "Suche")
        assert "Egress" not in meldung
        assert "ALLOWED_EGRESS_HOSTS" not in meldung
        assert "Allow-List" not in meldung


def test_policy_verstoss_und_stoerung_sind_drei_verschiedene_meldungen():
    """Die Zusicherung, die das Paar erst zu einem Nachweis macht.

    Die beiden Tests darueber sind je fuer sich auch dann gruen, wenn
    `_handle_error` alles auf denselben Satz abbildete, der zufaellig beide
    Woerter enthaelt. Hier faellt die Zusammenlegung auf.
    """
    verstoss = _handle_error(EgressPolicyViolation("evil.example.com"), "Suche")
    verbindung = _handle_error(httpx.ConnectError("kaputt"), "Suche")
    unbekannt = _handle_error(ValueError("boom"), "Suche")
    assert len({verstoss, verbindung, unbekannt}) == 3


def test_der_diskriminator_ist_auf_dem_policy_verstoss_gesetzt():
    """Das Feld selbst, damit es nicht still verschwindet.

    Ohne diese Zeile bliebe der Test ueber den Wiederholungsrat auch dann
    gruen, wenn `retryable` ganz entfiele: `getattr(e, "retryable", False)`
    faellt dann auf `False` zurueck und liefert dieselbe Meldung -- aus dem
    falschen Grund.
    """
    assert EgressPolicyViolation("x").retryable is False
    assert "retryable" in vars(EgressPolicyViolation)


def test_der_policy_verstoss_bleibt_ein_permissionerror():
    """Rueckwaertskompatibilitaet, festgehalten statt vorausgesetzt.

    `EgressError` erbt bewusst von `PermissionError`, damit ein bestehendes
    `except PermissionError` um den Guard weiter greift. Die Unterscheidung
    entsteht eine Ebene darunter und nicht durch Wegnehmen.
    """
    assert issubclass(EgressPolicyViolation, PermissionError)
    with pytest.raises(PermissionError):
        client._check_egress_allowed("https://evil.example.com/v1/x")


@pytest.mark.anyio
async def test_der_gesperrte_host_erreicht_den_aufrufer_als_iserror(monkeypatch):
    """Beide Befunde zusammen, am Draht.

    SEC-028 liefert die Meldung, FID-003 den Kanal. Bis 0.4.1 war beides
    falsch: ein erfolgreiches Result mit «Unbekannter Fehler. Bitte spaeter
    erneut versuchen.»
    """
    from eth_library_mcp import server

    monkeypatch.setattr(server, "DISCOVERY_BASE_URL", "https://evil.example.com/v1")
    resultat = await aufruf_am_draht("eth_search_resources", SUCHE)
    meldung = resultat["content"][0]["text"]

    assert resultat["isError"] is True
    assert "ALLOWED_EGRESS_HOSTS" in meldung
    assert "später erneut" not in meldung


# ══ Der Hinweis steht an allen Werkzeugen, nicht nur am ersten ════════════


def _leersuchen() -> dict:
    """Je Werkzeug ein Aufruf, der garantiert nichts findet."""
    from eth_library_mcp import server as s

    return {
        "eth_search_resources": lambda: s.eth_search_resources(
            s.SearchResourcesInput(query="any,contains,zzz")
        ),
        "eth_get_resource": lambda: s.eth_get_resource(s.GetResourceInput(mmsid="991234567890")),
        "eth_search_archive": lambda: s.eth_search_archive(
            s.SearchArchiveInput(archive=next(iter(s.ARCHIVE_SOURCES)), query="any,contains,zzz")
        ),
        "eth_search_by_type": lambda: s.eth_search_by_type(
            s.SearchByTypeInput(
                resource_type=next(iter(s.RESOURCE_TYPES)), query="any,contains,zzz"
            )
        ),
        "eth_search_education": lambda: s.eth_search_education(
            s.SearchEducationInput(topic="zzz nichts")
        ),
    }


@pytest.mark.anyio
@pytest.mark.parametrize("name", sorted(_leersuchen()))
async def test_jede_leermenge_traegt_einen_konkreten_naechsten_schritt(name):
    """FID-003, Kriterium 1 und 2, je Werkzeug.

    Zwei der fuenf Werkzeuge nannten bis 0.4.1 ueberhaupt keinen naechsten
    Schritt: `eth_search_archive` und `eth_search_by_type` meldeten bloss
    «Keine Treffer». Der Hinweis muss ausserdem *konkret* sein -- er nennt
    hier eine Abfrage, die man woertlich absetzen kann.
    """
    with respx.mock(assert_all_called=False) as mock:
        mock.get(url__startswith=client.DISCOVERY_BASE_URL).mock(
            return_value=httpx.Response(200, json={"docs": [], "info": {"total": 0}})
        )
        resultat = await _leersuchen()[name]()

    felder = strukturiert(resultat)
    assert felder["returned"] == 0
    assert felder["hint"], f"{name} laesst das Modell bei null Treffern raten"
    # Konkret heisst: eine absetzbare Abfrage oder ein benanntes Werkzeug,
    # kein «versuchen Sie eine andere Suche».
    assert "any,contains," in felder["hint"] or "eth_" in felder["hint"], (
        f"{name} gibt einen Allgemeinplatz statt eines naechsten Versuchs: {felder['hint']!r}"
    )
    assert felder["hint"] in text(resultat), (
        f"{name}: Feld und Text sagen Verschiedenes — der Hinweis ist doppelt gepflegt."
    )


def test_die_liste_der_leergeprueften_werkzeuge_ist_vollstaendig():
    """Der Waechter ueber der handgeschriebenen Liste.

    Ein neues Werkzeug ohne Leermengen-Hinweis bliebe sonst ungeprueft, weil
    der Test es nie aufruft. Dieselbe Luecke, die OPS-010 geschlossen hat.
    """
    from eth_library_mcp import server as s

    vorhanden = {n for n in dir(s) if n.startswith("eth_") and callable(getattr(s, n, None))}
    # `eth_library_info` fragt keine Quelle ab und hat keine Leermenge.
    ungeprueft = vorhanden - set(_leersuchen()) - {"eth_library_info"}
    assert not ungeprueft, f"Werkzeuge ohne Leermengen-Test: {sorted(ungeprueft)}"


@pytest.mark.anyio
async def test_eine_gescheiterte_suche_traegt_keinen_leermengen_hinweis():
    """Kriterium 8: Der Fehlerpfad hat seinen eigenen naechsten Schritt.

    Der Leermengen-Hinweis zeigt auf die Query. Bei einem Fehlschlag ist die
    Abfrage nie angekommen -- dort zeigt er in die falsche Richtung.
    """
    resultat = await _am_draht(httpx.Response(401, text="unauthorized"))
    meldung = resultat["content"][0]["text"]

    # Geprueft wird der RAT, nicht das Vorkommen der Query-Syntax: Die Meldung
    # nennt die gescheiterte Abfrage als Kontext, und darin steht
    # `any,contains,` voellig zu Recht. Eine erste Fassung verbot die
    # Zeichenkette und schlug genau daran an -- ein Fehlalarm, kein Befund.
    for verbreiterung in ("Breiter suchen", "Trunkierung", "englischen Begriff"):
        assert verbreiterung not in meldung
    assert "ETH_LIBRARY_API_KEY" in meldung
