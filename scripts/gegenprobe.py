#!/usr/bin/env python3
"""Faehrt die dokumentierten Mutationen und sagt, welcher Test dabei faellt.

## Warum es dieses Skript gibt

CLAUDE.md verlangt unter «Tests»: «Jede neue Zusicherung einzeln neutralisieren
und zeigen, dass genau die zugehoerigen Tests fallen.» Bis zum 20.9.2026 war
das eine Handarbeit -- und der Re-Audit hat gemessen, was dabei herauskommt:
Von sechs Zusicherungen liessen sich **vier** entfernen, ohne dass ein einziger
Test fiel (Befund OPS-010). Der Egress-Schutz, die Werkzeug-Annotationen, die
Fehlermaskierung und die Quellenangabe waren im Code vorhanden, in der Doku
beschrieben -- und von nichts festgehalten.

Eine Handarbeit, die vier von sechs Luecken uebersieht, ist keine Pruefung.
Deshalb steht die Liste jetzt hier, ausgeschrieben und ausfuehrbar.

Seit FID-003 und SEC-028 sind es dreizehn Eintraege: die sechs von OPS-010 plus
die sieben Zusicherungen, die mit dem Fehlerkanal und der Egress-Taxonomie
dazukamen.
Die Liste waechst mit jedem Befund, den jemand behebt -- das ist ihr Zweck.

## Was es nicht ist

Kein allgemeines Mutationstest-Werkzeug. Es faehrt **genau die** Mutationen,
die jemand als beschreibenswert eingetragen hat -- die Zusicherungen, auf die
es diesem Server ankommt. Eine Vollabdeckung ueber alle Zeilen waere eine
andere Aufgabe und braeuchte ein anderes Werkzeug.

## Die Positivkontrollen sind Pflicht, nicht Zierde

Zwei Eintraege unten sind `positivkontrolle=True`: Mutationen, von denen
bekannt ist, dass sie anschlagen. Schlagen **sie** nicht an, misst der Lauf
nichts -- dann ist die Suite gar nicht gelaufen, der Pfad falsch, die Kopie
unvollstaendig. Ohne sie waere «alle Mutationen ueberlebt» von «das Skript ist
kaputt» nicht zu unterscheiden. Genau diese Verwechslung beschreibt CLAUDE.md
unter «Eine Null ist eine Behauptung».

## Aufruf

    python scripts/gegenprobe.py            # alle Mutationen
    python scripts/gegenprobe.py --nur M1   # eine einzelne
    python scripts/gegenprobe.py --json     # maschinenlesbar

Exit 0 nur, wenn jede Mutation mindestens einen Test fallen laesst **und**
beide Positivkontrollen anschlagen.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent

# Was in die Arbeitskopie muss, damit die Suite laeuft. Bewusst eine Liste und
# kein `cp -r .`: Ein vollstaendiger Klon zoege `.git` und `audits/` mit und
# machte jeden Lauf um Groessenordnungen langsamer.
MITZUNEHMEN = (
    "src",
    "tests",
    "scripts",
    "pyproject.toml",
    "SECURITY.md",
    "SECURITY.de.md",
    "README.md",
    "README.de.md",
    "CLAUDE.md",
    "CONTRIBUTING.md",
    "server.json",
    ".github",
)


@dataclass(frozen=True)
class Mutation:
    """Eine Zusicherung, neutralisiert."""

    kennung: str
    zusicherung: str
    datei: str
    alt: str
    neu: str
    erwartet: tuple[str, ...] = ()
    positivkontrolle: bool = False
    bemerkung: str = ""


MUTATIONEN: list[Mutation] = [
    Mutation(
        kennung="M1",
        zusicherung="Egress-Allow-List (SEC-021)",
        datei="src/eth_library_mcp/client.py",
        alt="        raise EgressPolicyViolation(host)",
        neu="        return",
        erwartet=("test_egress_sperrt_einen_fremden_host", "test_bei_gesperrtem_host"),
        bemerkung=(
            "Vor dem 20.9.2026 ungedeckt: Der einzige Test akzeptierte "
            '"Unbekannter Fehler" ODER "Egress denied" und war damit '
            "unabhaengig von der Sperre gruen."
        ),
    ),
    Mutation(
        kennung="M2",
        zusicherung="Werkzeug-Annotationen (ARCH-009)",
        datei="src/eth_library_mcp/server.py",
        alt='        "readOnlyHint": True,',
        neu="",
        erwartet=("test_jedes_werkzeug_ist_als_nur_lesend_annotiert",),
        bemerkung="Trifft alle Vorkommen; eines genuegte fuer den Befund.",
    ),
    Mutation(
        kennung="M3",
        zusicherung="Generische Fehlermaskierung (OBS-002)",
        datei="src/eth_library_mcp/formatting.py",
        alt='    return f"{prefix}Unbekannter Fehler. Bitte später erneut versuchen."',
        neu='    return f"{prefix}{type(e).__name__}: {e}"',
        erwartet=("test_der_generische_zweig_verraet_weder_klasse_noch_text",),
        bemerkung="Der Zweig, der Implementierungsdetails an das Modell gaebe.",
    ),
    Mutation(
        kennung="M4",
        zusicherung="Quellenangabe je Antwort (CH-004)",
        datei="src/eth_library_mcp/formatting.py",
        alt='    lines.append(f"*{SOURCE_ATTRIBUTION}*")',
        neu="",
        erwartet=("test_der_detailformatierer_traegt_die_quellenangabe",),
    ),
    Mutation(
        kennung="M5",
        zusicherung="Upstream-Ausfaelle landen im Fehlerkanal (FID-003)",
        datei="src/eth_library_mcp/server.py",
        alt=(
            "        raise ToolError("
            "_handle_error(e, f\"Suche nach '{params.query}'\", is_search=True)) from e"
        ),
        neu=(
            "        return ergebnis("
            "_handle_error(e, f\"Suche nach '{params.query}'\", is_search=True), returned=0)"
        ),
        erwartet=("test_ein_upstream_ausfall_kommt_mit_iserror_an",),
        bemerkung=(
            "Stellt den Stand von 0.4.1 wieder her: Ein Transport- oder "
            "Autorisierungsfehler kommt als gewoehnliches, erfolgreiches "
            "Tool-Result an."
        ),
    ),
    Mutation(
        kennung="M6",
        zusicherung="Policy-Verstoss hat einen eigenen Zweig (SEC-028)",
        datei="src/eth_library_mcp/formatting.py",
        alt="    if isinstance(e, EgressError):",
        neu="    if False and isinstance(e, EgressError):",
        erwartet=(
            "test_der_policy_verstoss_nennt_die_allow_list_und_den_host",
            "test_policy_verstoss_und_stoerung_sind_drei_verschiedene_meldungen",
        ),
        bemerkung=(
            "Ohne den Zweig faellt die Absage in den generischen Schluss und "
            "wird zeichengleich mit der fuer ein ValueError."
        ),
    ),
    Mutation(
        kennung="M7",
        zusicherung="Wiederholungsrat haengt am Diskriminator (SEC-028)",
        datei="src/eth_library_mcp/formatting.py",
        alt=(
            '    return WIEDERHOLUNG_MOEGLICH if getattr(e, "retryable", False) '
            "else KEINE_WIEDERHOLUNG"
        ),
        neu="    return WIEDERHOLUNG_MOEGLICH",
        erwartet=("test_der_policy_verstoss_bekommt_keinen_wiederholungsrat",),
        bemerkung=(
            "Gibt einer deterministischen Absage wieder einen "
            "Wiederholungsrat -- der Befund, mit dem SEC-028 anfing."
        ),
    ),
    Mutation(
        kennung="M8",
        zusicherung="Leermenge traegt einen maschinenlesbaren naechsten Schritt (FID-003)",
        datei="src/eth_library_mcp/formatting.py",
        alt='        structured_content={"returned": returned, "total": total, "hint": hint},',
        neu='        structured_content={"returned": returned, "total": total, "hint": None},',
        erwartet=("test_jede_leermenge_traegt_einen_konkreten_naechsten_schritt",),
        bemerkung=(
            "Der Hinweis bliebe im Fliesstext stehen und waere vom Ergebnis "
            "wieder nicht trennbar -- der Zustand vor 0.4.1."
        ),
    ),
    Mutation(
        kennung="M9",
        zusicherung="Kein Leermengen-Hinweis neben Treffern (FID-003)",
        datei="src/eth_library_mcp/formatting.py",
        alt="    if hint is not None and returned:",
        neu="    if False:",
        erwartet=("test_ein_hinweis_neben_treffern_wird_abgewiesen",),
        bemerkung="Ein Hinweis neben Treffern schickt das Modell zum Verbreitern.",
    ),
    Mutation(
        kennung="M10",
        zusicherung="404 auf einer Suche ist keine Leermenge (FID-003)",
        datei="src/eth_library_mcp/formatting.py",
        alt='                    f"{prefix}Der Suchendpunkt wurde nicht gefunden (HTTP 404). "',
        neu=(
            '                    f"{prefix}Keine Ergebnisse oder Endpunkt '
            'nicht gefunden (HTTP 404). "'
        ),
        erwartet=("test_der_404_auf_einer_suche_wird_nicht_als_leermenge_erzaehlt",),
        bemerkung=(
            "Der Wortlaut von 0.4.1. Er fuehrte eine Aussage ueber den Bestand "
            "und eine ueber die Konfiguration in einem Satz zusammen."
        ),
    ),
    Mutation(
        kennung="M11",
        zusicherung="Die transiente Lage nennt die Egress-Policy nicht (SEC-028)",
        datei="src/eth_library_mcp/formatting.py",
        alt='        return f"{prefix}Verbindungsfehler. Internetverbindung prüfen."',
        neu=(
            '        return f"{prefix}Verbindungsfehler. Egress-Allow-List '
            'und Internetverbindung prüfen."'
        ),
        erwartet=("test_die_transiente_lage_nennt_die_egress_policy_nicht",),
        bemerkung=(
            "Der zweite Schaden aus dem Ursprungsbefund: Wer wegen eines "
            "DNS-Zuckens in der Allow-List sucht, sucht eine Zeile fuer einen "
            "Host, der erlaubt ist."
        ),
    ),
    Mutation(
        kennung="P1",
        zusicherung="CORS faellt nicht auf Wildcard zurueck (SDK-004)",
        datei="src/eth_library_mcp/server.py",
        alt="        allow_origins=origins,",
        neu='        allow_origins=origins or ["*"],',
        positivkontrolle=True,
        bemerkung="Bekannt anschlagend. Faellt sie nicht, misst der Lauf nichts.",
    ),
    Mutation(
        kennung="P2",
        zusicherung="Upstream-Body wird nicht durchgereicht (OBS-002)",
        datei="src/eth_library_mcp/formatting.py",
        alt='        return f"{prefix}HTTP-Fehler {status}."',
        neu='        return f"{prefix}HTTP-Fehler {status}: {e.response.text}"',
        positivkontrolle=True,
        bemerkung="Bekannt anschlagend.",
    ),
]


@dataclass
class Ergebnis:
    mutation: Mutation
    angewandt: bool
    gefallen: list[str] = field(default_factory=list)
    treffer: int = 0
    meldung: str = ""

    @property
    def in_ordnung(self) -> bool:
        return self.angewandt and bool(self.gefallen)


_FEHLGESCHLAGEN = re.compile(r"^FAILED (\S+?)::([^\s\[]+)", re.M)


def _kopiere(ziel: Path) -> None:
    for name in MITZUNEHMEN:
        quelle = WURZEL / name
        if not quelle.exists():
            continue
        if quelle.is_dir():
            shutil.copytree(quelle, ziel / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(quelle, ziel / name)


def _suite(arbeitsverzeichnis: Path) -> tuple[list[str], int]:
    """Faehrt die Suite und gibt die gefallenen Testnamen zurueck."""
    lauf = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-m", "not live", "-q", "--no-header"],
        cwd=arbeitsverzeichnis,
        env={"PYTHONPATH": "src", "PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(Path.home())},
        capture_output=True,
        text=True,
    )
    ausgabe = lauf.stdout + lauf.stderr
    namen = sorted({m.group(2) for m in _FEHLGESCHLAGEN.finditer(ausgabe)})
    return namen, lauf.returncode


def grundlast() -> set[str]:
    """Welche Tests in einer UNMUTIERTEN Kopie fallen.

    Diese Funktion gibt es, weil ihr Fehlen den ersten Lauf dieses Skripts
    wertlos gemacht hat. Die Kopie traegt kein `.git`, und
    `tests/test_session_start_hook.py` prueft einen Git-Hook -- dort fielen in
    **jedem** Lauf dieselben 13 Tests, unabhaengig von der Mutation. Jede Zeile
    meldete «OK», und keine davon war eine Messung: Die Kulisse allein reichte
    fuer den Befund «Tests werden rot».

    Der Grundlast-Lauf trennt Kulisse von Wirkung. Was hier faellt, wird von
    jedem Mutationsergebnis abgezogen.
    """
    with tempfile.TemporaryDirectory(prefix="gegenprobe-grundlast-") as tmp:
        kopie = Path(tmp)
        _kopiere(kopie)
        gefallen, _ = _suite(kopie)
        return set(gefallen)


def fahre(mutation: Mutation, kulisse: set[str]) -> Ergebnis:
    with tempfile.TemporaryDirectory(prefix=f"gegenprobe-{mutation.kennung}-") as tmp:
        kopie = Path(tmp)
        _kopiere(kopie)

        ziel = kopie / mutation.datei
        text = ziel.read_text(encoding="utf-8")
        treffer = text.count(mutation.alt)
        if treffer == 0:
            return Ergebnis(
                mutation,
                angewandt=False,
                meldung=(
                    f"Das Muster steht nicht in {mutation.datei}. Entweder wurde die "
                    "Zusicherung umgeschrieben -- dann gehoert dieser Eintrag "
                    "nachgezogen -- oder sie ist ganz verschwunden."
                ),
            )
        ziel.write_text(text.replace(mutation.alt, mutation.neu), encoding="utf-8")

        gefallen, _ = _suite(kopie)
        # Nur was die Mutation ZUSAETZLICH umbringt, zaehlt.
        durch_mutation = sorted(set(gefallen) - kulisse)
        return Ergebnis(mutation, angewandt=True, gefallen=durch_mutation, treffer=treffer)


def main() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--nur", metavar="KENNUNG", help="nur diese Mutation fahren")
    zerleger.add_argument("--json", action="store_true", help="maschinenlesbar ausgeben")
    argumente = zerleger.parse_args()

    auswahl = [m for m in MUTATIONEN if not argumente.nur or m.kennung == argumente.nur]
    if not auswahl:
        print(f"Keine Mutation mit der Kennung {argumente.nur!r}.", file=sys.stderr)
        return 2

    im_repo, rueckgabe = _suite(WURZEL)
    if rueckgabe != 0:
        print(
            "Die Suite ist schon ohne Mutation rot:\n  " + "\n  ".join(im_repo),
            file=sys.stderr,
        )
        print("Ein Gegenprobe-Lauf auf roter Grundlage sagt nichts.", file=sys.stderr)
        return 2

    kulisse = grundlast()
    if not argumente.json:
        print(f"Ausgangslage im Repo gruen. {len(auswahl)} Mutation(en).")
        if kulisse:
            print(
                f"Grundlast in der Arbeitskopie: {len(kulisse)} Test(s) fallen dort "
                "auch ohne Mutation und werden abgezogen."
            )
        print()

    ergebnisse = [fahre(m, kulisse) for m in auswahl]

    if argumente.json:
        print(
            json.dumps(
                [
                    {
                        "kennung": e.mutation.kennung,
                        "zusicherung": e.mutation.zusicherung,
                        "angewandt": e.angewandt,
                        "positivkontrolle": e.mutation.positivkontrolle,
                        "gefallen": e.gefallen,
                        "in_ordnung": e.in_ordnung,
                        "meldung": e.meldung,
                    }
                    for e in ergebnisse
                ],
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        for e in ergebnisse:
            art = "Positivkontrolle" if e.mutation.positivkontrolle else "Zusicherung"
            zeichen = "OK  " if e.in_ordnung else "LUECKE"
            print(f"{zeichen} {e.mutation.kennung}  {art}: {e.mutation.zusicherung}")
            if not e.angewandt:
                print(f"       {e.meldung}")
            elif e.gefallen:
                print(f"       {len(e.gefallen)} Test(s) rot: {', '.join(e.gefallen[:4])}")
            else:
                print("       KEIN Test wird rot — die Zusicherung ist ungedeckt.")
            print()

    luecken = [e for e in ergebnisse if not e.in_ordnung]
    kontrollen = [e for e in ergebnisse if e.mutation.positivkontrolle]
    stumme_kontrolle = [e for e in kontrollen if not e.in_ordnung]

    if stumme_kontrolle and not argumente.json:
        print(
            "Eine Positivkontrolle hat NICHT angeschlagen. Dieser Lauf misst nichts "
            "-- vor dem Deuten der uebrigen Zeilen zuerst das Skript pruefen.",
            file=sys.stderr,
        )
    return 1 if luecken else 0


if __name__ == "__main__":
    raise SystemExit(main())
