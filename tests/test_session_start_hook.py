"""Der SessionStart-Hook darf melden, aber niemals blockieren.

Was hier festgehalten wird, steht sonst nur als Absicht im Skript — und eine
Absicht faellt nicht um, wenn jemand eine Zeile umstellt. Die beiden Zusagen,
die den Hook tragen, sind gegenlaeufig und deshalb einzeln geprueft:

1. Er meldet die fehlenden Commits, wenn welche fehlen (sonst waere er nur
   teure Stille), und schweigt bei 0.
2. Er beendet sich unter allen Umstaenden mit 0 und ohne Ausgabe — kein Netz,
   kein Remote, kein Repo, detached HEAD. Ein Hook, der bei Netzproblemen die
   Arbeit anhaelt, wird abgeschaltet und schuetzt danach gar nichts.

Der Default-Branch wird dabei ermittelt, nicht geraten: `test_master` faellt,
sobald jemand "main" fest verdrahtet. Genau diese Annahme hat im Portfolio
schon einmal einen Branch 15 Commits alt werden lassen.
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import time

import pytest

_HOOK = (
    pathlib.Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "check-clone-freshness.sh"
)

_GIT_ENV = {
    "GIT_AUTHOR_NAME": "Test",
    "GIT_AUTHOR_EMAIL": "test@example.invalid",
    "GIT_COMMITTER_NAME": "Test",
    "GIT_COMMITTER_EMAIL": "test@example.invalid",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
}


def _git(*args: str, cwd: pathlib.Path) -> str:
    ergebnis = subprocess.run(
        ["git", *args],
        cwd=cwd,
        env={**os.environ, **_GIT_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    return ergebnis.stdout


def _commit(repo: pathlib.Path, text: str) -> None:
    (repo / "datei.txt").write_text(text, encoding="utf-8")
    _git("add", "datei.txt", cwd=repo)
    _git("commit", "-m", text, cwd=repo)


def _lauf(repo: pathlib.Path, **umgebung: str) -> subprocess.CompletedProcess[str]:
    """Den Hook fahren — so, wie Claude Code ihn faehrt."""
    return subprocess.run(
        [str(_HOOK)],
        cwd=str(repo),
        env={**os.environ, **_GIT_ENV, "CLAUDE_PROJECT_DIR": str(repo), **umgebung},
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.fixture
def welt(tmp_path: pathlib.Path):
    """Baut origin (bare) + Quelle + Klon und liefert einen Vorspul-Schalter.

    Der Klon haengt anfangs auf demselben Commit wie origin.
    """

    def bauen(zweig: str = "main"):
        origin = tmp_path / "origin.git"
        quelle = tmp_path / "quelle"
        klon = tmp_path / "klon"

        subprocess.run(
            ["git", "init", "--bare", "--initial-branch", zweig, str(origin)],
            env={**os.environ, **_GIT_ENV},
            capture_output=True,
            check=True,
        )
        quelle.mkdir()
        _git("init", "--initial-branch", zweig, cwd=quelle)
        _commit(quelle, "erster")
        _git("remote", "add", "origin", str(origin), cwd=quelle)
        _git("push", "-u", "origin", zweig, cwd=quelle)

        subprocess.run(
            ["git", "clone", str(origin), str(klon)],
            env={**os.environ, **_GIT_ENV},
            capture_output=True,
            check=True,
        )

        def vorspulen(anzahl: int) -> None:
            for nummer in range(anzahl):
                _commit(quelle, f"neu-{nummer}")
            _git("push", "origin", zweig, cwd=quelle)

        return klon, origin, vorspulen

    return bauen


def test_meldet_wie_viele_commits_fehlen(welt):
    klon, _origin, vorspulen = welt()
    vorspulen(3)

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert "3 Commit(s) hinter origin/main" in ergebnis.stdout


def test_schweigt_wenn_nichts_fehlt(welt):
    klon, _origin, _vorspulen = welt()

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""


def test_master_wird_erkannt_und_nicht_geraten(welt):
    """Drei Server im Portfolio heissen ihren Standard-Branch `master`."""
    klon, _origin, vorspulen = welt(zweig="master")
    vorspulen(2)

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert "2 Commit(s) hinter origin/master" in ergebnis.stdout
    assert "origin/main" not in ergebnis.stdout


def test_detached_head_meldet_statt_zu_scheitern(welt):
    klon, _origin, vorspulen = welt()
    vorspulen(2)
    _git("checkout", "--detach", "HEAD", cwd=klon)

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert "2 Commit(s) hinter origin/main" in ergebnis.stdout


def test_eigene_commits_werden_nicht_als_rueckstand_gezaehlt(welt):
    klon, _origin, vorspulen = welt()
    vorspulen(2)
    _commit(klon, "eigene arbeit")

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert "2 Commit(s) hinter origin/main" in ergebnis.stdout
    assert "lokal 1 voraus" in ergebnis.stdout


def test_ohne_remote_still(tmp_path: pathlib.Path):
    repo = tmp_path / "allein"
    repo.mkdir()
    _git("init", "--initial-branch", "main", cwd=repo)
    _commit(repo, "erster")

    ergebnis = _lauf(repo)

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""


def test_ausserhalb_eines_git_repos_still(tmp_path: pathlib.Path):
    kein_repo = tmp_path / "kein_repo"
    kein_repo.mkdir()

    ergebnis = _lauf(kein_repo)

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""


def test_repo_ohne_commits_still(tmp_path: pathlib.Path):
    repo = tmp_path / "leer"
    repo.mkdir()
    _git("init", "--initial-branch", "main", cwd=repo)

    ergebnis = _lauf(repo)

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""


def test_verschwundenes_remote_blockiert_nicht(welt):
    """Origin weg, kein gecachter Rueckstand: schweigen statt scheitern."""
    klon, origin, _vorspulen = welt()
    shutil.rmtree(origin)

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""


def test_ohne_netz_faellt_er_auf_den_letzten_fetch_zurueck(welt):
    """Der zuletzt geholte Stand untertreibt vielleicht — er luegt nicht."""
    klon, origin, vorspulen = welt()
    vorspulen(2)
    _git("fetch", "origin", "main", cwd=klon)
    shutil.rmtree(origin)

    ergebnis = _lauf(klon)

    assert ergebnis.returncode == 0
    assert "2 Commit(s) hinter origin/main" in ergebnis.stdout
    assert "letzten Fetch" in ergebnis.stdout


def test_haengendes_remote_laeuft_in_die_zeitgrenze(welt):
    """Ein nicht routbares Remote darf den Sessionstart nicht anhalten.

    Gemessen wird echte Zeit: eine Fake-Uhr koennte diese Zusicherung nicht
    widerlegen. Die Schranke liegt bewusst weit ueber der Zeitgrenze — sie
    faellt, wenn `timeout` fehlt, nicht wenn der Rechner kurz laedt.
    """
    klon, _origin, _vorspulen = welt()
    _git("remote", "set-url", "origin", "git://10.255.255.1/leer.git", cwd=klon)
    _git("update-ref", "-d", "refs/remotes/origin/main", cwd=klon)
    _git("update-ref", "-d", "refs/remotes/origin/HEAD", cwd=klon)

    beginn = time.monotonic()
    ergebnis = _lauf(klon, CLAUDE_CLONE_CHECK_TIMEOUT="1")
    gedauert = time.monotonic() - beginn

    assert ergebnis.returncode == 0
    assert ergebnis.stdout == ""
    assert gedauert < 20, f"Hook brauchte {gedauert:.1f}s — die Zeitgrenze greift nicht"


def _hook_mit_offenem_stdin(
    repo: pathlib.Path, ausgabe: pathlib.Path, pfad_praefix: pathlib.Path
) -> int:
    """Den Hook fahren, ohne stdin je zu schliessen — und ohne zu warten.

    `subprocess.PIPE` plus »nie schreiben, nie schliessen« ist der Fall, den
    `exec </dev/null` abfangen muss: stdin existiert, liefert aber nie EOF.
    """
    with ausgabe.open("wb") as ziel:
        prozess = subprocess.Popen(
            [str(_HOOK)],
            cwd=str(repo),
            env={
                **os.environ,
                **_GIT_ENV,
                "CLAUDE_PROJECT_DIR": str(repo),
                "PATH": f"{pfad_praefix}{os.pathsep}{os.environ['PATH']}",
            },
            stdin=subprocess.PIPE,
            stdout=ziel,
            stderr=subprocess.DEVNULL,
        )
        try:
            return prozess.wait(timeout=15)
        except subprocess.TimeoutExpired:
            prozess.kill()
            prozess.wait()
            pytest.fail("Hook wartet auf eine Eingabe — `exec </dev/null` fehlt")
        finally:
            if prozess.stdin is not None:
                prozess.stdin.close()


def test_offenes_stdin_haelt_den_hook_nicht_an(welt, tmp_path: pathlib.Path):
    """Nichts im Hook darf je auf eine Eingabe warten.

    Claude Code schreibt das Hook-JSON nach stdin; ein Aufruf von Hand erbt das
    Terminal. Wartet irgendein Kindprozess darauf — ein Credential-Helper, ssh,
    ein `git`, das nachfragt —, haengt der Sessionstart, und zwar unbegrenzt:
    die Zeitgrenzen im Skript liegen nur um die Netzaufrufe.

    Stellvertretend dafuer steht hier ein `git`, das stdin liest, bis es
    geschlossen wird. Mit `exec </dev/null` bekommt es sofort EOF; ohne
    wartet es auf ein stdin, das nie schliesst.
    """
    klon, _origin, _vorspulen = welt()

    attrappen = tmp_path / "pfad"
    attrappen.mkdir()
    falsches_git = attrappen / "git"
    falsches_git.write_text("#!/bin/sh\ncat >/dev/null\nexit 1\n", encoding="utf-8")
    falsches_git.chmod(0o755)

    ausgabe = tmp_path / "ausgabe.txt"
    rueckgabe = _hook_mit_offenem_stdin(klon, ausgabe, attrappen)

    assert rueckgabe == 0
    assert ausgabe.read_text(encoding="utf-8") == ""


def test_hook_json_auf_stdin_stoert_ihn_nicht(welt):
    """So faehrt Claude Code ihn wirklich: das Ereignis-JSON liegt auf stdin."""
    klon, _origin, vorspulen = welt()
    vorspulen(3)

    ergebnis = subprocess.run(
        [str(_HOOK)],
        cwd=str(klon),
        env={**os.environ, **_GIT_ENV, "CLAUDE_PROJECT_DIR": str(klon)},
        input='{"hook_event_name":"SessionStart","source":"startup"}',
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert ergebnis.returncode == 0
    assert "3 Commit(s) hinter origin/main" in ergebnis.stdout
