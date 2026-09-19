"""Was der Server ueber sich selbst behauptet, muss stimmen.

Der Audit vom 19.9.2026 fand drei Stellen, an denen 0.4.0 etwas Falsches ueber
sich sagte -- alle drei in einem Release, dessen CHANGELOG-Eintrag genau diese
Aufraeumarbeit fuer die uebrigen Dateien auffuehrt:

- die `instructions` bewarben `eth_search_persons`, ein Werkzeug, das derselbe
  Release entfernt hat. Sie gehen im Handshake und in `server/discover` an
  jeden Client;
- `eth_library_info` meldete `**Version:** 0.3.0`, waehrend das Paket bei 0.4.0
  stand;
- `SECURITY.md` nannte `mcp[cli]>=1.0.0,<2.0.0`, gepinnt war `>=2.0.0,<3`.

Keine davon hat ein Gate gesehen. `check_version_sync.py` meldete sogar
ausdruecklich «keine hartkodierte Version in src/» -- es kannte die Form nicht,
in der die Zahl dort stand.

## Warum diese Tests auf Invarianten zeigen und nicht auf Zahlen

Ein Test, der `assert "0.4.1" in ausgabe` schreibt, ist keine Pruefung der
Version, sondern eine weitere Kopie davon -- und er bricht beim naechsten
Bump, also genau dann, wenn alles richtig laeuft. Verglichen wird deshalb
gegen `__version__` beziehungsweise gegen `pyproject.toml`: Das bricht nur,
wenn zwei Stellen auseinanderlaufen, die zusammengehoeren.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

from eth_library_mcp import __version__, server

WURZEL = Path(__file__).resolve().parent.parent


def flach(text: str) -> str:
    """Zeilenumbrueche und Mehrfach-Leerzeichen zu je einem Leerzeichen.

    Ohne das prueft eine Textsuche die Formatierung statt des Inhalts: Der
    Satz steht da, nur mit einem Umbruch an der Stelle, an der das Muster ein
    Leerzeichen erwartet.
    """
    return re.sub(r"\s+", " ", text or "").strip()


# ── Die `instructions` ─────────────────────────────────────────────────────


def _werkzeugnamen() -> set[str]:
    """Die Werkzeuge, die es wirklich gibt — aus dem Modul, nicht aus einer Liste."""
    return {
        name
        for name in dir(server)
        if name.startswith("eth_") and callable(getattr(server, name, None))
    }


def test_die_instructions_bewerben_kein_entferntes_werkzeug():
    """Die `instructions` sind die Selbstvorstellung des Servers.

    Sie bewarben nach 0.4.0 weiter die Personen-Suche. Geprueft wird hier
    nicht gegen eine Verbotsliste — die muesste jemand pflegen, und genau das
    ist beim letzten Mal unterblieben —, sondern gegen die Sachlage: Das
    Werkzeug existiert nicht, also darf sein Gegenstand nicht als verfuegbar
    angekuendigt werden.
    """
    assert "eth_search_persons" not in _werkzeugnamen(), (
        "Das Werkzeug ist zurueck — dann gehoert dieser Test angepasst, nicht die instructions."
    )
    text = flach(server.mcp.instructions or "")
    assert "Personen-Suche" not in text
    assert "Wikidata" not in text


def test_die_instructions_beschreiben_den_server_ueberhaupt():
    """Positivkontrolle zum Test darueber.

    Ohne sie bestuende jener auch dann, wenn die `instructions` leer waeren
    oder das Attribut anders hiesse — eine Abwesenheitspruefung an einem Feld,
    das es nicht mehr gibt, ist immer gruen.
    """
    text = flach(server.mcp.instructions or "")
    assert "ETH-Bibliothek" in text
    assert "Discovery API" in text


# ── Die Version in der Werkzeugausgabe ─────────────────────────────────────


@pytest.mark.anyio
async def test_eth_library_info_meldet_die_paketversion():
    """Die einzige Versionsangabe, die ein Nutzer dieses Servers zu sehen bekommt.

    Verglichen wird gegen `__version__`, nicht gegen eine aufgeschriebene
    Zahl. Ein Literal hier waere die sechste Versions-Stelle und wuerde beim
    naechsten Bump die Pipeline anhalten, statt Drift zu finden.
    """
    ausgabe = await server.eth_library_info()
    assert f"**Version:** {__version__}" in ausgabe


@pytest.mark.anyio
async def test_eth_library_info_nennt_keine_fremde_versionsnummer():
    """Gegenprobe zur Zeile darueber.

    Sie allein wuerde auch bestehen, wenn daneben noch eine zweite, veraltete
    Nummer im Text staende — genau die Lage, die 0.4.0 ausgeliefert hat.
    """
    ausgabe = await server.eth_library_info()
    gefunden = set(re.findall(r"(?i)\bversion\b[^0-9\n]{0,12}?(\d+\.\d+(?:\.\d+)?)", ausgabe))
    assert gefunden <= {__version__}, (
        f"Fremde Versionsangaben in eth_library_info: {sorted(gefunden - {__version__})}"
    )


# ── Die Abhaengigkeits-Deckel in der Dokumentation ─────────────────────────


def _grundname(spezifikation: str) -> str:
    """Der Verteilungsname ohne Extras und ohne Versionsbedingung.

    Diese Funktion gibt es, weil ihr Fehlen den Test hier still wirkungslos
    gemacht hat. Die erste Fassung trennte auf der einen Seite auch an `[`
    und bekam `mcp`, auf der anderen nicht und bekam `mcp[cli]`. Damit fand
    die Suche den Eintrag nie, uebersprang ihn ohne ein Wort — und der Test
    blieb gruen, als die Gegenprobe genau den Deckel zuruecksetzte, gegen den
    er geschrieben ist. Aufgefallen ist das nur durch die Mutation; die
    Vollstaendigkeitszeile unten war erfuellt, weil die drei anderen
    Abhaengigkeiten ohne Extra durchliefen — sie zaehlte, dass ueberhaupt
    etwas geprueft wurde, nicht ob das Richtige dabei war. Deshalb steht
    darunter jetzt zusaetzlich der Name.
    """
    return re.split(r"[<>=!\[ ]", spezifikation, maxsplit=1)[0].strip()


def _pyproject_deckel() -> dict[str, str]:
    daten = tomllib.loads((WURZEL / "pyproject.toml").read_text(encoding="utf-8"))
    return {_grundname(eintrag): eintrag for eintrag in daten["project"]["dependencies"]}


@pytest.mark.parametrize("datei", ["SECURITY.md", "SECURITY.de.md"])
def test_die_security_md_nennt_die_tatsaechlichen_deckel(datei):
    """`SECURITY.md` nannte zwei Releases lang die Deckel der Vorgaenger-Major.

    Geprueft wird jede Abhaengigkeit, die die Datei ueberhaupt erwaehnt: Steht
    dort ein Deckel fuer `mcp[cli]`, muss es der aus `pyproject.toml` sein.
    Was die Datei nicht nennt, verlangt dieser Test auch nicht — sonst
    erzwaenge er eine Vollstaendigkeit, die niemand beschlossen hat.
    """
    text = flach((WURZEL / datei).read_text(encoding="utf-8"))
    deckel = _pyproject_deckel()
    genannt = set(re.findall(r"`([a-zA-Z0-9_.\-]+(?:\[[a-z]+\])?[<>=][^`]+)`", text))

    geprueft: set[str] = set()
    for angabe in genannt:
        name = _grundname(angabe)
        if name not in deckel:
            continue
        geprueft.add(name)
        assert angabe == deckel[name], (
            f"{datei} nennt `{angabe}`, pyproject.toml fuehrt `{deckel[name]}`"
        )

    assert geprueft, (
        f"{datei} nennt keinen einzigen Deckel, den pyproject.toml kennt — "
        "entweder ist die Tabelle weg oder das Suchmuster greift nicht. "
        "Beides ist ein Befund, kein Bestehen."
    )
    # Das SDK ist die Abhaengigkeit, deren Deckel in 0.4.0 eine Major-Version
    # zurueckhing. Ihn hier namentlich zu verlangen ist keine Willkuer: Ohne
    # diese Zeile darf der Test die eine Angabe ueberspringen, um die es geht,
    # und meldet trotzdem Erfolg — gemessen, genau so ist es passiert.
    assert "mcp" in geprueft, (
        f"{datei} nennt keinen Deckel fuer `mcp` — dann prueft dieser Test "
        "die Abhaengigkeit nicht mehr, wegen der es ihn gibt."
    )
