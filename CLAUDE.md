# CLAUDE.md

## Teil 1 — Portfolio-Konventionen

### Vor der Arbeit

Klon-Aktualität prüfen — Standard-Branch ermitteln, nicht `main` annehmen:

```bash
B=$(git ls-remote --symref origin HEAD | sed -n 's|^ref: refs/heads/\([^[:space:]]*\).*|\1|p')
git fetch origin "${B:?Standard-Branch nicht ermittelbar}" &&
  git rev-list --count HEAD..FETCH_HEAD
```

Drei Server im Portfolio heissen ihren Standard-Branch `master`
(`openlex-mcp`, `swiss-courts-mcp`, `swisstopo-mcp`); dort scheitert ein fest
verdrahtetes `origin/main` mit «couldn't find remote ref main». Wer das für ein
Netzproblem hält, arbeitet weiter auf genau dem veralteten Klon, vor dem dieser
Absatz warnt. Den `:?`-Schutz nicht weglassen: Bei leerem `B` fetcht git still
den Remote-HEAD und endet mit 0.

Ein veralteter Klon erzeugt eine rote CI, deren Ursache nicht im Diff steht.
Am 3.8.2026 zweimal passiert — beide Male fehlten genau die Commits, die
das Gate einführten, an dem der Branch scheiterte.

Gates lokal fahren, mit der GEPINNTEN ruff-Version aus der CI. Eine andere
Version meldet Abweichungen, die niemand verursacht hat.

### Tests

Gegenprobe ist Pflicht. Ein Test, der grün bleibt, wenn man die
Implementierung entfernt, prüft nichts. Jede neue Zusicherung einzeln
neutralisieren und zeigen, dass genau die zugehörigen Tests fallen.

Zwei Fallen, die beide grün blieben:

- Eine Fake-Uhr, die nur beim Schlafen vorrückt, kann eine Zusicherung über
  echte Zeit nicht widerlegen.
- `monkeypatch.setattr(modul.asyncio, "sleep", ...)` greift ins Modul
  `asyncio` selbst und entschärft die Mechanik im ganzen Prozess. Patche
  einen Modul-Alias (`_sleep = asyncio.sleep`), nicht das fremde Modul.

Handgeschriebene Fixtures kodieren die Annahme des Autors und können sie
nicht widerlegen. Mindestens eine aufgezeichnete Antwort pro externem
Endpunkt, mit Aufnahmedatum.

### Wenn etwas rot ist

Roter Live-Test: erst die Quelle abfragen, dann einordnen. Nicht aus der
Fehlermeldung schliessen. Am 3.8.2026 hiess «nicht gefunden» nicht, dass der
Datensatz weg war, sondern dass die Quelle die Schreibweise ihrer Kopfzeile
gewechselt hatte — vier von sechs Datensätzen produktiv kaputt, alle
Unit-Tests grün.

PR ohne jeden Check ist selten ein Repo ohne CI, meistens ein
Merge-Konflikt: GitHub berechnet dafür keinen Merge-Commit und startet nichts.

Ein Codex-Review auf einem PR wird beantwortet oder behoben, nie ignoriert.

## Teil 2 — Dieses Repo

### ruff-Version

**`ruff==0.16.1`**, gepinnt an genau einer Stelle: im `dev`-Extra von
`pyproject.toml`. Die CI installiert von dort und pinnt nicht selbst
nach. Eine `.pre-commit-config.yaml` gibt es nicht.

`pip install -e ".[dev]"` liefert damit lokal dieselbe ruff-Version wie die
CI. Keinen zweiten Pin einbauen — zwei Pins driften auseinander, und dann
weicht der lokale Lauf wieder still von der CI ab.
`tests/test_werkzeug_versionen.py` hält das fest, statt es zu behaupten: Der
Absatz hier kann nicht umfallen, der Test schon. Er kennt dabei alle gängigen
Installationsformen (`--upgrade`, Anführungszeichen, `pip3`,
`uv tool install`, `uv run --with`) und beide Workflow-Endungen; eine engere
Fassung war grün, weil sie nicht hinsah.

Vor dem Lauf `ruff --version` prüfen: ein älteres ruff früher im `PATH`
schlägt den Pin, ohne dass der Install etwas meldet.

### Gate-Befehle (wörtlich aus `ci.yml`, in dieser Reihenfolge)

```bash
pip install -e ".[dev]"
PYTHONPATH=src pytest tests/ -m "not live"
python scripts/check_ruff_pin.py
ruff check src/ tests/ scripts/
ruff format --check src/ tests/ scripts/
python scripts/check_version_sync.py
```

Matrix: Python 3.11, 3.12, 3.13. Trigger: Push und PR auf `main`. Alle Gates
laufen in einem Job auf allen drei Feldern — keine `if:`-Ausnahme, kein
zweiter lint-Job. Ein `fail-fast: false` steht nicht da: Eine rote 3.11
bricht 3.12 und 3.13 ab, bevor sie etwas sagen.

### Live-Tests

Die CI schliesst sie per `-m "not live"` aus; gefahren werden sie täglich
06:17 UTC von `.github/workflows/live-tests.yml` (cron, dazu
`workflow_dispatch` von Hand). Ein roter Lauf öffnet ein Issue mit Label
`live-test-failure` — oder kommentiert das offene, statt ein zweites
aufzumachen. Damit ist DRIFT-005 geschlossen.

Hier stand «5 von 10 geprüften Servern des Portfolios verletzen ihn
weiterhin». Nachgezählt am 16.08.2026 über 22 Klone: **alle 22 fahren einen
geplanten Live-Lauf**, die Zahl war also überholt. Eine Kennzahl über *andere*
Repos gehört ohnehin in den Audit-Katalog und nicht hierher — sie veraltet
still, weil sie sich in diesem Repo durch nichts überprüfen lässt.

Der Workflow bricht ab, wenn `pytest -m live` **null** Tests einsammelt
(Exit-Code 5). Ein grüner Lauf ohne Tests sieht wie Abdeckung aus und ist
schlimmer als kein Lauf — so fing dieses Repo an.

**Nach 60 Tagen ohne Repo-Aktivität deaktiviert GitHub den cron-Trigger.**
Ein ruhiger Server verliert seine Überwachung also genau dann, wenn niemand
hinsieht — und zwar lautlos: der Workflow bleibt stehen, er läuft nur nicht
mehr. Vor dem Schluss «seit Wochen nichts kaputt» erst prüfen, ob überhaupt
noch gefahren wird (Actions-Seite, letzter Lauf). Wiedereinschalten geht dort
per Knopf; ein Commit allein reicht nicht.

Beide Live-Tests brauchen keinen API-Key: sie messen, welche Routen das
Gateway führt (401 = Route da, Schlüssel fehlt; 404 = Route weg). Wer eine
Zusicherung ergänzt, die einen Schlüssel braucht, muss vorher
`ETH_LIBRARY_API_KEY` als Secret hinterlegen — sonst wird der Lauf rot,
ohne dass die Quelle etwas dafür kann.

Fixture-Herkunft und was bewusst *nicht* aufgezeichnet ist:
`tests/fixtures/PROVENANCE.md` (Stand 2026-08-08).
