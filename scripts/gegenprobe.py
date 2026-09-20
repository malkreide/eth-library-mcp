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
        alt='        raise PermissionError(f"Egress denied: host {host!r} not in ALLOWED_EGRESS_HOSTS")',
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
