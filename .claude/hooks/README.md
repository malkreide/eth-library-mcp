# SessionStart-Hook: Klon-Aktualität

`check-clone-freshness.sh` meldet beim Sessionstart, wie viele Commits der
ausgecheckte Stand hinter `origin/<default-branch>` liegt. Liegt er nicht
zurück, sagt er nichts.

Registriert ist er in [`../settings.json`](../settings.json). JSON kennt keine
Kommentare — die Begründung steht deshalb hier und im Kopf des Skripts.

## Warum

Ein veralteter Klon hat am 3.8.2026 zweimal eine rote CI erzeugt, deren
Ursache nicht im Diff stand: die fehlenden Commits waren jeweils genau die,
die das Gate einführten, an dem der Branch scheiterte. Gesucht wurde beide
Male in den falschen Dateien — im eigenen Diff, der in Ordnung war.

Die Prüfung kostet eine Sekunde und ersetzt diese Fehlersuche.

## Was er zusichert

**1. Er blockiert die Session nie.** Kein Netz, kein Remote, detached HEAD,
flatterndes DNS, fehlendes `timeout`, Repo ohne Commits, gar kein Repo — jeder
dieser Fälle geht still durch, Exit-Code 0, keine Ausgabe. Das ist die oberste
Anforderung, nicht die zweite: ein Hook, der bei Netzproblemen die Arbeit
anhält, wird nach dem zweiten Mal abgeschaltet und schützt danach gar nichts.

Konkret heißt das im Skript: kein `set -e`, `exec </dev/null` (nichts wartet je
auf eine Eingabe), `GIT_TERMINAL_PROMPT=0` samt Askpass-Attrappen (git fragt
nie nach Zugangsdaten), jeder Netzaufruf unter `timeout`, die ganze Logik in
einer Funktion, deren Ergebnis verworfen wird, und ein `exit 0` am Ende. In
`settings.json` steht zusätzlich ein `"timeout": 20` als zweites Netz.

**2. Kurzes Timeout.** `CLAUDE_CLONE_CHECK_TIMEOUT` (Vorgabe 5 Sekunden) gilt
pro Netzaufruf. Im Normalfall fällt genau einer an: `git ls-remote --symref
origin HEAD` liefert Default-Branch und Remote-SHA in einem Zug. Nur wenn
dabei schon feststeht, dass Commits fehlen, folgt ein `git fetch`. Wer aktuell
ist, zahlt also einen Roundtrip und bekommt Stille.

**3. Ausgabe nur bei tatsächlichem Rückstand.** Bei 0 schweigt er. Eigene,
noch nicht gepushte Commits zählen nicht als Rückstand — sie werden getrennt
als »lokal N voraus« ausgewiesen.

**4. Der Default-Branch wird ermittelt, nicht angenommen.** Drei Server im
Portfolio heißen ihren Standard-Branch `master`; die Annahme »main« hat schon
einmal einen Branch 15 Commits alt werden lassen. Reihenfolge: `ls-remote
--symref` (maßgeblich, bemerkt auch eine Umbenennung), sonst der lokal
gecachte `refs/remotes/origin/HEAD`. Lässt er sich nicht ermitteln, schweigt
der Hook — er rät nicht.

## Ohne Netz

Ist das Remote nicht erreichbar, fällt der Hook auf den zuletzt geholten Stand
(`refs/remotes/origin/<branch>`) zurück und kennzeichnet das in der Ausgabe.
Diese Zahl kann untertreiben, aber was sie meldet, fehlt wirklich. Gibt es auch
den nicht, schweigt er.

## Prüfen und Debuggen

```bash
# von Hand fahren — verhält sich wie beim Sessionstart
./.claude/hooks/check-clone-freshness.sh; echo "exit=$?"

# Fehler sichtbar machen (sonst nach /dev/null)
CLAUDE_CLONE_CHECK_DEBUG=1 ./.claude/hooks/check-clone-freshness.sh
```

Die Zusicherungen hängen nicht an diesem Text, sondern an
`tests/test_session_start_hook.py` — ein Absatz fällt nicht um, ein Test schon.
Die Tests bauen echte Repos in `tmp_path` (inklusive eines mit `master` als
Default-Branch) und laufen ohne Internet in rund zwei Sekunden.
